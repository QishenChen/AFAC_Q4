"""search_tables — Table search, get, and listing.
Contains: search_tables, get_table, get_tables_under, search_doc, get_tables_by_doc.
Full implementations extracted from Retriever.
"""

from agent.tools._loader import get_indices
from agent.tools._shared import MIN_SCORE, _split_pipe_query
from agent.tools.get_doc_info import get_doc_info, resolve_doc
from utils.text_utils import fuzzy_match


def _multi_fuzzy_match(query: str, target: str) -> float:
    """
    If query contains pipe, score = max of individual term matches.
    Otherwise normal fuzzy_match.
    """
    terms = _split_pipe_query(query)
    if len(terms) <= 1:
        return fuzzy_match(query, target)
    return max(fuzzy_match(t, target) for t in terms)


def _multi_fuzzy_match_and(query: str, target: str) -> float:
    """
    Geometric mean of individual term scores — requires ALL terms present (AND logic).
    Returns 0 if any term scores 0.
    """
    terms = _split_pipe_query(query)
    if len(terms) <= 1:
        return fuzzy_match(query, target)
    scores = [fuzzy_match(t, target) for t in terms]
    if any(s == 0 for s in scores):
        return 0.0
    prod = 1.0
    for s in scores:
        prod *= s
    return prod ** (1.0 / len(scores))


def get_table(table_id: str) -> dict | None:
    """Get a single table by its table_id (e.g. 'T_02828')."""
    indices = get_indices()
    table_index = indices["table_index"]
    for t in table_index["tables"]:
        if t["table_id"] == table_id:
            return t
    return None


def get_tables_under(doc: str, heading_title: str) -> list[dict]:
    """Get all tables under a specific heading in a document."""
    indices = get_indices()
    table_index = indices["table_index"]
    docs = resolve_doc(doc)
    if not docs:
        return []
    rel_path = docs[0]
    key = f"{rel_path}::{heading_title}"
    table_ids = table_index["by_heading"].get(key, [])
    tables = []
    for tid in table_ids:
        t = get_table(tid)
        if t:
            tables.append(t)
    return tables


def get_tables_by_doc(doc: str) -> list[dict]:
    """Get all tables in a document."""
    indices = get_indices()
    table_index = indices["table_index"]
    docs = resolve_doc(doc)
    if not docs:
        return []
    rel_path = docs[0]
    table_ids = table_index["by_doc"].get(rel_path, [])
    tables = []
    for tid in table_ids:
        t = get_table(tid)
        if t:
            tables.append(t)
    return tables


def search_doc(doc: str, query: str, max_results: int = 20) -> list[dict]:
    """Search for tables within a single document."""
    docs = resolve_doc(doc)
    if not docs:
        return []
    return search_tables(query, doc_filter=docs[0], max_results=max_results)


def search_tables(query: str | None = None, domain: str | None = None, max_results: int = 20,
                  doc_filter: str | None = None, doc: str | None = None,
                  table_id: str | None = None, heading_title: str | None = None):
    """
    Unified table access:
      - If table_id: return single table by ID
      - If heading_title + doc: return tables under that heading
      - Otherwise: keyword search
    """
    # Unified dispatch
    if table_id:
        t = get_table(table_id)
        return [t] if t else []
    if heading_title and doc:
        return get_tables_under(doc, heading_title)

    # Resolve doc_filter from doc param
    if doc and not doc_filter:
        docs = resolve_doc(doc)
        doc_filter = docs[0] if docs else None

    indices = get_indices()
    table_index = indices["table_index"]

    if not query:
        return []

    results = []
    for t in table_index["tables"]:
        if domain:
            doc_info = get_doc_info(t["doc_path"])
            if not doc_info or doc_info.get("domain") != domain:
                continue
        if doc_filter and t["doc_path"] != doc_filter:
            continue

        # Multi-term pipe matching — search name, headers, context, AND data rows
        name_score = _multi_fuzzy_match(query, t["name"])
        header_text = " ".join(t["headers"])
        header_score = _multi_fuzzy_match(query, header_text)
        context_score = _multi_fuzzy_match(query, t.get("context_before", ""))
        data_text = " ".join(str(c) for r in t.get("data", []) if r for c in r if c)
        data_score = _multi_fuzzy_match(query, data_text)
        score = 0.35 * name_score + 0.20 * header_score + 0.15 * context_score + 0.30 * data_score

        if score >= MIN_SCORE:
            results.append({**t, "score": round(score, 3)})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]