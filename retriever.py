"""
Retrieval engine — compatibility facade.
All implementations moved to agent/tools/ modules.
This file re-exports for backward compatibility.
"""

from agent.tools.get_doc_info import resolve_doc, get_doc_info, list_docs_by_domain
from agent.tools.search_headings import search_headings
from agent.tools.search_tables import search_tables, search_doc, get_table, get_tables_under, get_tables_by_doc
from agent.tools.search_text import search_text as search_section_text
from agent.tools.get_section import get_section
from agent.tools.expand_query import expand_query
from agent.tools._loader import get_indices

# Re-export the singleton helper
from agent.tools._loader import get_indices as _get_indices

def get_retriever():
    """Backward-compatible singleton — returns a thin wrapper."""
    return _RetrieverFacade()


class _RetrieverFacade:
    """Thin wrapper that delegates all methods to agent.tools modules."""

    def resolve_doc(self, identifier):
        return resolve_doc(identifier)

    def get_doc_info(self, rel_path):
        return get_doc_info(rel_path)

    def list_docs_by_domain(self, domain):
        return list_docs_by_domain(domain)

    def search_headings(self, query, domain=None, max_results=20, doc_filter=None):
        return search_headings(query, domain=domain, max_results=max_results, doc_filter=doc_filter)

    def search_section_text(self, doc, query, max_results=10):
        return search_section_text(doc, query, max_results=max_results)

    def get_section(self, doc, heading_path):
        return get_section(doc, heading_path)

    def search_tables(self, query, domain=None, max_results=20, doc_filter=None):
        return search_tables(query, domain=domain, max_results=max_results, doc_filter=doc_filter)

    def get_table(self, table_id):
        return get_table(table_id)

    def get_tables_under(self, doc, heading_title):
        return get_tables_under(doc, heading_title)

    def get_tables_by_doc(self, doc):
        return get_tables_by_doc(doc)

    def search_doc(self, doc, query, max_results=20):
        return search_doc(doc, query, max_results=max_results)

    def search(self, query, domain=None, max_results=30, doc_filter=None):
        heading_results = search_headings(query, domain=domain, max_results=max_results, doc_filter=doc_filter)
        table_results = search_tables(query, domain=domain, max_results=max_results, doc_filter=doc_filter)
        combined = []
        for h in heading_results:
            combined.append({
                "type": "heading", "doc": h["doc"], "title": h["title"],
                "heading_path": h["path"], "line_start": h["line_start"],
                "line_end": h["line_end"], "score": h["score"],
            })
        for t in table_results:
            combined.append({
                "type": "table", "table_id": t["table_id"], "doc": t["doc_path"],
                "name": t["name"], "heading_title": t["heading_title"],
                "headers": t["headers"], "row_count": t["row_count"],
                "unit": t.get("unit"), "score": t["score"],
            })
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:max_results]

    def expand_query(self, query):
        return expand_query(query)

    def search_by_year(self, year, query="", domain=None, max_results=20):
        import re
        from agent.tools._shared import MIN_SCORE
        from utils.text_utils import fuzzy_match

        FINANCIAL_KW_PATTERN = re.compile(
            "|".join(re.escape(kw) for kw in {
                "利率", "资产", "负债", "利润", "收入", "成本", "费用", "现金", "资金",
                "净利", "毛利", "营收", "损益", "权益", "股本", "分红", "股利",
                "发行", "注册", "信用", "评级", "额度", "限额", "金额", "价格",
                "收益率", "回报率", "增长率", "占比", "比率", "比例",
                "EBITDA", "ROE", "EPS",
            })
        )

        def _multi_fuzzy_match(q, target):
            from agent.tools._shared import _split_pipe_query
            terms = _split_pipe_query(q)
            if len(terms) <= 1:
                return fuzzy_match(q, target)
            return max(fuzzy_match(t, target) for t in terms)

        indices = _get_indices()
        table_index = indices["table_index"]
        year_str = str(year)
        results = []
        for t in table_index["tables"]:
            if domain:
                doc_info = get_doc_info(t["doc_path"])
                if not doc_info or doc_info.get("domain") != domain:
                    continue
            header_text = " ".join(t["headers"])
            context_text = t.get("context_before", "")
            name_text = t["name"]
            combined_text = f"{header_text} {context_text} {name_text}"
            if year_str not in combined_text:
                continue
            if not FINANCIAL_KW_PATTERN.search(combined_text):
                continue
            score = 1.0
            if query:
                score = _multi_fuzzy_match(query, combined_text)
            if score >= MIN_SCORE:
                results.append({**t, "score": round(score, 3)})
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]


# ─── CLI demo ─────────────────────────────────────────────

if __name__ == "__main__":
    r = _RetrieverFacade()
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