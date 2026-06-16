"""
Tool wrappers around the Retriever for use in the ReACT loop.
All search tools accept an optional 'doc' parameter to limit scope.
No separate _doc variants needed — just set doc="text01".
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retriever import Retriever

_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def _resolve_doc(doc: str) -> str | None:
    """Resolve a doc_id to rel_path, or None if not found."""
    docs = get_retriever().resolve_doc(doc)
    return docs[0] if docs else None


def _search_tables_unified(query=None, doc=None, domain=None, table_id=None, heading_title=None, max_results=8):
    """Unified table access: by table_id, by heading_title, or by keyword query."""
    r = get_retriever()
    if table_id:
        t = r.get_table(table_id)
        return [t] if t else []
    if heading_title and doc:
        return r.get_tables_under(doc, heading_title)
    doc_filter = _resolve_doc(doc) if doc else None
    return r.search_tables(query, domain=domain, max_results=max_results, doc_filter=doc_filter)


TOOLS = {
    # ── Heading search ──
    "search_headings": {
        "name": "search_headings",
        "desc": "Search section headings by keyword. Use | to separate terms. Set doc to limit to one document.",
        "params": ["query: str", "doc: str|None", "domain: str|None", "max_results: int=10"],
        "fn": lambda query, doc=None, domain=None, max_results=10: (
            get_retriever().search_headings(query, domain=domain, max_results=max_results,
                                             doc_filter=_resolve_doc(doc) if doc else None)
        ),
    },
    # ── Table search (unified: keyword / by-ID / by-heading) ──
    "search_tables": {
        "name": "search_tables",
        "desc": "Search tables by keyword, or fetch by table_id, or get all under a heading. Use | for multi-keyword queries.",
        "params": [
            "query: str|None — keyword search (use | to separate). Omit for table_id/heading_title lookup",
            "doc: str|None — limit to one document",
            "domain: str|None — filter by domain",
            "table_id: str|None — single table by ID (e.g. 'T_02828')",
            "heading_title: str|None — all tables under this heading (requires doc)",
            "max_results: int=8",
        ],
        "fn": lambda query=None, doc=None, domain=None, table_id=None, heading_title=None, max_results=8: (
            _search_tables_unified(query, doc, domain, table_id, heading_title, max_results)
        ),
    },
    # ── Raw text search ──
    "search_section_text": {
        "name": "search_section_text",
        "desc": "Search RAW TEXT (not tables) in a document. Finds clauses, disclosures, narrative content. doc is REQUIRED.",
        "params": ["doc: str", "query: str", "max_results: int=8"],
        "fn": lambda doc, query, max_results=8: get_retriever().search_section_text(doc, query, max_results=max_results),
    },
    # ── Full section content + tables ──
    "get_section": {
        "name": "get_section",
        "desc": "Get FULL text + ALL tables under a heading. heading_path is the exact title from search_headings results.",
        "params": ["doc: str", "heading_path: str|list[str] — e.g. '二、财务报表' or ['二、财务报表']"],
        "fn": lambda doc, heading_path: get_retriever().get_section(doc, heading_path),
    },
    # ── Utility (not exposed to LLM prompt) ──
    "expand_query": {
        "name": "expand_query",
        "desc": "Expand query with financial synonyms (internal use).",
        "params": ["query: str"],
        "fn": lambda query: get_retriever().expand_query(query),
    },
    "get_doc_info": {
        "name": "get_doc_info",
        "desc": "Get metadata for a document.",
        "params": ["rel_path: str"],
        "fn": lambda rel_path: get_retriever().get_doc_info(rel_path),
    },
}


def execute_tool(name: str, **kwargs) -> dict:
    if name not in TOOLS:
        return {"error": f"Unknown tool: {name}", "result": None}
    try:
        fn = TOOLS[name]["fn"]
        result = fn(**kwargs)
        return {"result": result, "error": None}
    except Exception as e:
        return {"error": str(e), "result": None}