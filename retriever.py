"""
Multi-layer retrieval engine.
Provides APIs to search documents by heading, keyword, and retrieve tables.
Uses heading_index.json + table_index.json + financial_terms.json.
No embedding models used — purely structural + token-based matching.
"""

import json
import os
import re
from collections import defaultdict

from utils.text_utils import (
    normalize_text,
    tokenize_chinese,
    token_overlap_score,
    fuzzy_match,
    is_heading_line,
    strip_html_tags,
    extract_year_from_text,
)

INDICES_DIR = "indices"
HEADING_INDEX_PATH = os.path.join(INDICES_DIR, "heading_index.json")
TABLE_INDEX_PATH = os.path.join(INDICES_DIR, "table_index.json")
DOC_REGISTRY_PATH = os.path.join(INDICES_DIR, "doc_registry.json")
FINANCIAL_TERMS_PATH = "config/financial_terms.json"

# Minimum fuzzy match score to consider a table/heading relevant
MIN_SCORE = 0.15

# Financial keywords for filtering search_by_year results
FINANCIAL_KEYWORDS = {
    "利率", "资产", "负债", "利润", "收入", "成本", "费用", "现金", "资金",
    "净利", "毛利", "营收", "损益", "权益", "股本", "分红", "股利",
    "发行", "注册", "信用", "评级", "额度", "限额", "金额", "价格",
    "收益率", "回报率", "增长率", "占比", "比率", "比例",
    "EBITDA", "ROE", "EPS",
}


def _split_pipe_query(query: str) -> list[str]:
    """Split a pipe-delimited query into individual terms."""
    if "|" in query:
        return [t.strip() for t in query.split("|") if t.strip()]
    return [query]


def _multi_fuzzy_match(query: str, target: str) -> float:
    """
    If query contains pipe, score = max of individual term matches.
    Otherwise normal fuzzy_match.
    """
    terms = _split_pipe_query(query)
    if len(terms) <= 1:
        return fuzzy_match(query, target)
    return max(fuzzy_match(t, target) for t in terms)


FINANCIAL_KW_PATTERN = re.compile(
    "|".join(re.escape(kw) for kw in FINANCIAL_KEYWORDS)
)


class Retriever:
    """
    Main retrieval interface.
    Loads indices lazily and provides query methods.
    """

    def __init__(self):
        self.heading_index = None
        self.table_index = None
        self.doc_registry = None
        self.financial_terms = None
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return
        with open(HEADING_INDEX_PATH, "r", encoding="utf-8") as f:
            self.heading_index = json.load(f)
        with open(TABLE_INDEX_PATH, "r", encoding="utf-8") as f:
            self.table_index = json.load(f)
        with open(DOC_REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.doc_registry = json.load(f)
        with open(FINANCIAL_TERMS_PATH, "r", encoding="utf-8") as f:
            self.financial_terms = json.load(f)
        self._loaded = True

    # ─── Document resolution ───────────────────────────────

    def resolve_doc(self, identifier: str) -> list[str]:
        self._ensure_loaded()
        if identifier in self.doc_registry["by_id"]:
            return [self.doc_registry["by_id"][identifier]["rel_path"]]
        if identifier in self.doc_registry["by_name"]:
            return [self.doc_registry["by_name"][identifier]["rel_path"]]
        candidates = []
        for doc in self.doc_registry["all_docs"]:
            score_doc_id = fuzzy_match(identifier, doc["doc_id"])
            score_name = fuzzy_match(identifier, doc["friendly_name"])
            score = max(score_doc_id, score_name)
            if score > 0.3:
                candidates.append((score, doc["rel_path"]))
        candidates.sort(key=lambda x: x[0], reverse=True)
        norm_id = normalize_text(identifier)
        for doc in self.doc_registry["all_docs"]:
            if norm_id in normalize_text(doc["doc_id"]) or norm_id in normalize_text(doc["friendly_name"]):
                rel = doc["rel_path"]
                if rel not in [c[1] for c in candidates]:
                    candidates.append((0.5, rel))
        return [c[1] for c in candidates[:5]]

    def get_doc_info(self, rel_path: str) -> dict | None:
        self._ensure_loaded()
        for doc in self.doc_registry["all_docs"]:
            if doc["rel_path"] == rel_path:
                return doc
        return None

    def list_docs_by_domain(self, domain: str) -> list[dict]:
        self._ensure_loaded()
        return [d for d in self.doc_registry["all_docs"] if d["domain"] == domain]

    # ─── Heading retrieval ─────────────────────────────────

    def get_section(self, doc: str, heading_path) -> dict | None:
        self._ensure_loaded()
        # Auto-wrap string to list for LLM tolerance
        if isinstance(heading_path, str):
            heading_path = [heading_path]
        docs = self.resolve_doc(doc)
        if not docs:
            return None
        rel_path = docs[0]
        headings = self.heading_index["documents"].get(rel_path, [])
        if not headings:
            return None
        target = None
        for h in headings:
            h_path = h.get("path", [])
            if len(h_path) >= len(heading_path) and h_path[-len(heading_path):] == heading_path:
                target = h
                if len(h_path) == len(heading_path):
                    break
        if target is None:
            return None
        filepath = os.path.join("public_dataset_upload/extracted", rel_path)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        content = "".join(lines[target["line_start"]:target["line_end"]])
        tables = self.get_tables_under(doc, target["title"])
        return {
            "doc": rel_path,
            "heading": target["title"],
            "heading_path": target["path"],
            "line_start": target["line_start"],
            "line_end": target["line_end"],
            "content": content,
            "tables": tables,
        }

    def search_headings(self, query: str, domain: str | None = None, max_results: int = 20, doc_filter: str | None = None) -> list[dict]:
        self._ensure_loaded()
        query_terms = _split_pipe_query(query)
        if len(query_terms) > 1:
            all_results = {}
            for qt in query_terms[:4]:
                for r in self.search_headings(qt, domain=domain, max_results=max_results * 2, doc_filter=doc_filter):
                    key = f"{r['doc']}::{r['title']}::{r['line_start']}"
                    if key not in all_results or r["score"] > all_results[key]["score"]:
                        all_results[key] = r
            merged = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
            return merged[:max_results]

        tokens = tokenize_chinese(query)
        candidates = defaultdict(float)
        for tok in tokens:
            entries = self.heading_index["inverted_index"].get(tok, [])
            for entry in entries:
                key = f"{entry['doc']}::{entry['title']}::{entry['line_start']}"
                candidates[key] += 1.0 / len(tokens)
        results = []
        for key, index_score in candidates.items():
            doc, title, line_start = key.rsplit("::", 2)
            if doc_filter and doc != doc_filter:
                continue
            if domain:
                doc_info = self.get_doc_info(doc)
                if not doc_info or doc_info.get("domain") != domain:
                    continue
            fuzzy = fuzzy_match(query, title)
            final_score = 0.5 * index_score + 0.5 * fuzzy
            if final_score < MIN_SCORE:
                continue
            for h in self.heading_index["documents"].get(doc, []):
                if h["title"] == title and h["line_start"] == int(line_start):
                    results.append({
                        "doc": doc,
                        "title": title,
                        "path": h["path"],
                        "level": h["level"],
                        "line_start": h["line_start"],
                        "line_end": h["line_end"],
                        "score": round(final_score, 3),
                    })
                    break
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    def search_section_text(self, doc: str, query: str, max_results: int = 10) -> list[dict]:
        """Search raw text content of a document — finds clauses, statements, non-table text."""
        self._ensure_loaded()
        docs = self.resolve_doc(doc)
        if not docs:
            return []
        rel_path = docs[0]
        filepath = os.path.join("public_dataset_upload/extracted", rel_path)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        clean = strip_html_tags(content)
        lines = [l.strip() for l in clean.split("\n") if l.strip()]
        matches = []
        for i, line in enumerate(lines):
            if _multi_fuzzy_match(query, line) >= MIN_SCORE:
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                ctx = "\n".join(lines[start:end])
                matches.append({"line_num": i, "text": ctx[:1200]})
        return matches[:max_results]

    # ─── Table retrieval ───────────────────────────────────

    def get_tables_under(self, doc: str, heading_title: str) -> list[dict]:
        self._ensure_loaded()
        docs = self.resolve_doc(doc)
        if not docs:
            return []
        rel_path = docs[0]
        key = f"{rel_path}::{heading_title}"
        table_ids = self.table_index["by_heading"].get(key, [])
        tables = []
        for tid in table_ids:
            t = self.get_table(tid)
            if t:
                tables.append(t)
        return tables

    def get_table(self, table_id: str) -> dict | None:
        self._ensure_loaded()
        for t in self.table_index["tables"]:
            if t["table_id"] == table_id:
                return t
        return None

    def search_tables(self, query: str, domain: str | None = None, max_results: int = 20, doc_filter: str | None = None) -> list[dict]:
        self._ensure_loaded()
        results = []
        for t in self.table_index["tables"]:
            if domain:
                doc_info = self.get_doc_info(t["doc_path"])
                if not doc_info or doc_info.get("domain") != domain:
                    continue
            if doc_filter and t["doc_path"] != doc_filter:
                continue

            # Multi-term pipe matching — search name, headers, context, AND data rows
            name_score = _multi_fuzzy_match(query, t["name"])
            header_text = " ".join(t["headers"])
            header_score = _multi_fuzzy_match(query, header_text)
            context_score = _multi_fuzzy_match(query, t.get("context_before", ""))
            # Also match against data rows (first column often has indicator names like "资产负债率")
            data_text = " ".join(str(r[0]) for r in t.get("data", []) if r)
            data_score = _multi_fuzzy_match(query, data_text)
            score = 0.35 * name_score + 0.20 * header_score + 0.15 * context_score + 0.30 * data_score

            if score >= MIN_SCORE:
                results.append({**t, "score": round(score, 3)})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]

    def search_doc(self, doc: str, query: str, max_results: int = 20) -> list[dict]:
        """Search for tables within a single document."""
        self._ensure_loaded()
        docs = self.resolve_doc(doc)
        if not docs:
            return []
        return self.search_tables(query, doc_filter=docs[0], max_results=max_results)

    def get_tables_by_doc(self, doc: str) -> list[dict]:
        self._ensure_loaded()
        docs = self.resolve_doc(doc)
        if not docs:
            return []
        rel_path = docs[0]
        table_ids = self.table_index["by_doc"].get(rel_path, [])
        tables = []
        for tid in table_ids:
            t = self.get_table(tid)
            if t:
                tables.append(t)
        return tables

    # ─── Combined search ───────────────────────────────────

    def search(self, query: str, domain: str | None = None, max_results: int = 30, doc_filter: str | None = None) -> list[dict]:
        self._ensure_loaded()
        heading_results = self.search_headings(query, domain=domain, max_results=max_results, doc_filter=doc_filter)
        table_results = self.search_tables(query, domain=domain, max_results=max_results, doc_filter=doc_filter)
        combined = []
        for h in heading_results:
            combined.append({
                "type": "heading",
                "doc": h["doc"], "title": h["title"],
                "heading_path": h["path"],
                "line_start": h["line_start"], "line_end": h["line_end"],
                "score": h["score"],
            })
        for t in table_results:
            combined.append({
                "type": "table",
                "table_id": t["table_id"], "doc": t["doc_path"],
                "name": t["name"], "heading_title": t["heading_title"],
                "headers": t["headers"], "row_count": t["row_count"],
                "unit": t.get("unit"), "score": t["score"],
            })
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:max_results]

    # ─── Synonym expansion ─────────────────────────────────

    def expand_query(self, query: str) -> str:
        self._ensure_loaded()
        synonyms = self.financial_terms.get("synonyms", {})
        expanded_terms = [query]
        for canonical, syns in synonyms.items():
            for syn in syns:
                if syn in query:
                    expanded_terms.append(canonical)
                    for other in syns:
                        if other not in query and other not in expanded_terms:
                            expanded_terms.append(other)
        return " ".join(expanded_terms)

    # ─── Year-filtered search ──────────────────────────────

    def search_by_year(self, year: str, query: str = "", domain: str | None = None, max_results: int = 20) -> list[dict]:
        self._ensure_loaded()
        year_str = str(year)
        results = []
        for t in self.table_index["tables"]:
            if domain:
                doc_info = self.get_doc_info(t["doc_path"])
                if not doc_info or doc_info.get("domain") != domain:
                    continue
            header_text = " ".join(t["headers"])
            context_text = t.get("context_before", "")
            name_text = t["name"]
            combined_text = f"{header_text} {context_text} {name_text}"
            if year_str not in combined_text:
                continue
            # Post-filter: table must also contain a financial keyword
            if not FINANCIAL_KW_PATTERN.search(combined_text):
                continue
            score = 1.0
            if query:
                score = _multi_fuzzy_match(query, combined_text)
            if score >= MIN_SCORE:
                results.append({**t, "score": round(score, 3)})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]


# ─── Convenience singleton ────────────────────────────────

_retriever_instance = None

def get_retriever() -> Retriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = Retriever()
    return _retriever_instance


# ─── CLI demo ─────────────────────────────────────────────

if __name__ == "__main__":
    r = Retriever()
    print("=" * 60)
    print("Retrieval Engine Demo")
    print("=" * 60)
    print("\n--- Document Resolution ---")
    for name in ["比亚迪", "陕国投", "保险", "csrc_0001"]:
        docs = r.resolve_doc(name)
        print(f"  '{name}' → {docs[:3]}")
    print("\n--- Heading Search: '营业收入' ---")
    results = r.search_headings("营业收入", max_results=5)
    for res in results:
        print(f"  [{res['score']:.3f}] {res['doc']} → {' > '.join(res['path'])}")
    print("\n--- Table Search: '资产总额' ---")
    results = r.search_tables("资产总额", max_results=5)
    for res in results:
        print(f"  [{res['score']:.3f}] {res['doc_path']} → {res['name']}")
    print("\n--- Combined Search: '营业收入 2024' ---")
    results = r.search("营业收入 2024", max_results=10)
    for res in results:
        title = res.get("title") or res.get("name", "")
        print(f"  [{res['score']:.3f}] [{res['type']}] {res['doc']} → {title}")
    print("\n--- Query Expansion ---")
    query = "比亚迪 2024 年营收和净利"
    expanded = r.expand_query(query)
    print(f"  Original: {query}")
    print(f"  Expanded: {expanded}")
    print("\n--- Year Search: 2024 tables ---")
    results = r.search_by_year("2024", max_results=5)
    for res in results:
        print(f"  {res['doc_path']} → {res['name']} [{res['headers'][:3]}]")
    print("\nDone.")