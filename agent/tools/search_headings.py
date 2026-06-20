"""search_headings — Search section headings by keyword.
Full implementation extracted from Retriever.search_headings.
"""

from collections import defaultdict

from agent.tools._loader import get_indices
from agent.tools._shared import MIN_SCORE, _split_pipe_query
from agent.tools.get_doc_info import get_doc_info
from utils.text_utils import tokenize_chinese, fuzzy_match


def search_headings(query: str, doc: str | None = None, domain: str | None = None, max_results: int = 20, doc_filter: str | None = None):
    """Search section headings by keyword. Use | to separate terms. Set doc to limit to one document."""
    indices = get_indices()
    heading_index = indices["heading_index"]

    # Resolve doc_filter from doc param
    if doc and not doc_filter:
        from agent.tools.get_doc_info import resolve_doc
        docs = resolve_doc(doc)
        doc_filter = docs[0] if docs else None

    query_terms = _split_pipe_query(query)
    if len(query_terms) > 1:
        all_results = {}
        for qt in query_terms[:4]:
            for r in search_headings(qt, domain=domain, max_results=max_results * 2, doc_filter=doc_filter):
                key = f"{r['doc']}::{r['title']}::{r['line_start']}"
                if key not in all_results or r["score"] > all_results[key]["score"]:
                    all_results[key] = r
        merged = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
        return merged[:max_results]

    tokens = tokenize_chinese(query)
    candidates = defaultdict(float)
    for tok in tokens:
        entries = heading_index["inverted_index"].get(tok, [])
        for entry in entries:
            key = f"{entry['doc']}::{entry['title']}::{entry['line_start']}"
            candidates[key] += 1.0 / len(tokens)

    results = []
    for key, index_score in candidates.items():
        doc_path, title, line_start = key.rsplit("::", 2)
        if doc_filter and doc_path != doc_filter:
            continue
        if domain:
            doc_info = get_doc_info(doc_path)
            if not doc_info or doc_info.get("domain") != domain:
                continue
        fuzzy = fuzzy_match(query, title)
        final_score = 0.5 * index_score + 0.5 * fuzzy
        if final_score < MIN_SCORE:
            continue
        for h in heading_index["documents"].get(doc_path, []):
            if h["title"] == title and h["line_start"] == int(line_start):
                results.append({
                    "doc": doc_path,
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