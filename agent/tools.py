"""
Tool wrappers around the Retriever for use in the ReACT loop.
All search tools accept an optional 'doc' parameter to limit scope.
No separate _doc variants needed — just set doc="text01".
"""

import json
import os
import re
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


# ── Unit-aware arithmetic ──

# Map of Chinese/English unit suffixes → multiplier
_UNIT_SUFFIXES = [
    (r'万亿元', 1_000_000_000_000),    # compound: must precede 万亿/亿/万
    (r'万亿', 1_000_000_000_000),
    (r'亿元', 100_000_000),            # compound: must precede 亿
    (r'亿', 100_000_000),
    (r'千万', 10_000_000),
    (r'百万元', 1_000_000),           # compound: must precede 百万/万元
    (r'百万', 1_000_000),
    (r'万元', 10_000),                # compound: must precede 万
    (r'万', 10_000),
    (r'千元', 1_000),                 # compound: must precede 千
    (r'千', 1_000),
    (r'百', 100),
    (r'百元', 100),
    (r'元', 1),                       # bare 元 (note: not 元/股 after regex tokenizes)
    (r'\bB\b', 1_000_000_000),        # billion
    (r'\bM\b', 1_000_000),            # million
    (r'\bK\b', 1_000),                # thousand
    (r'%', 0.01),
]


def _parse_value_with_unit(token):
    """
    Parse a human-readable number into a float.
    Handles: commas, negative in (), Chinese units (万亿/亿/万/千/百/元), M/K/B, %.
    Examples:
        "32,619,022千元" → 32619022000.0
        "(1,234)" → -1234.0
        "6.97%" → 0.0697
        "23.5M" → 23500000.0
    """
    s = token.strip()
    # Handle negative in parentheses: (1,234,456)
    if s.startswith('(') and s.endswith(')'):
        s = '-' + s[1:-1]
    # Remove commas
    s = s.replace(',', '').replace('，', '')

    # Try: suffix match
    for suffix_pat, multiplier in _UNIT_SUFFIXES:
        m = re.search(suffix_pat, s)
        if m:
            # Remove the suffix and trailing characters after it
            num_part = s[:m.start()].strip()
            if num_part.startswith('-'):
                sign = -1
                num_part = num_part[1:]
            else:
                sign = 1
            try:
                return sign * float(num_part) * multiplier
            except ValueError:
                pass

    # No suffix matched: try plain float
    try:
        return float(s)
    except ValueError:
        pass
    return None


def _format_result(value, output_unit):
    """Format a raw numeric result into the requested unit."""
    if output_unit is None:
        return {"result": round(value, 6) if isinstance(value, float) else value}

    unit_map = {
        '万亿': 1_000_000_000_000, '亿': 100_000_000, '千万': 10_000_000,
        '百万': 1_000_000, '万': 10_000, '千': 1_000, '百': 100,
        '%': 100,  # multiply by 100 for percentage display
    }
    multiplier = unit_map.get(output_unit)
    if multiplier is None:
        # For % we need special handling — it's already a ratio, just *100
        return {"result": round(value, 6)}

    converted = value / multiplier if output_unit != '%' else value * 100
    return {
        "result": round(converted, 6),
        "unit": output_unit,
        "formatted": f"{round(converted, 4)}{output_unit}",
    }


def _evaluate_expression(expr, output_unit=None):
    """Replace unit-aware tokens with their numeric values, then eval."""

    def _replace_callback(m):
        token = m.group(0)
        val = _parse_value_with_unit(token)
        return str(val) if val is not None else token

    # Pattern: digits (with optional commas) followed by optional Chinese/English unit suffix.
    # Put longer/compound suffixes BEFORE shorter ones: 万元 before 万, 千元 before 千.
    _VALUE_PAT = re.compile(
        r'\d[\d,，.]*\s*(?:万亿元|万亿|亿元|千万|百万元|百万|万元|千元|万|千|百|亿|元|M|K|B|%)\b'
    )
    resolved = _VALUE_PAT.sub(_replace_callback, expr)

    # Handle negatives in parentheses: (1,234.56) → -1234.56
    _PAREN_PAT = re.compile(r'\([\d,，.]+\)')
    resolved = _PAREN_PAT.sub(_replace_callback, resolved)

    # Strip commas from plain numbers (not yet converted by unit suffix)
    resolved = re.sub(r'(?<=\d),(?=\d)', '', resolved)
    resolved = re.sub(r'(?<=\d)，(?=\d)', '', resolved)

    # Safety: allow only digits, +-*/(). and whitespace
    if not re.match(r'^[\d+\-*/().\s]+$', resolved):
        return {"error": f"Expression has unsafe characters after resolving: {resolved[:100]}"}

    try:
        result = eval(resolved)
        return _format_result(result, output_unit)
    except Exception as e:
        return {"error": f"Evaluation failed: {e}"}


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
    # ── Unit-aware calculator ──
    "compute": {
        "name": "compute",
        "desc": "Evaluate arithmetic with unit-aware numbers. Supports 万亿/亿/万/千/万元/千元/百/元/M/K/B/%. Always return ground-truth numbers.",
        "params": [
            "expression: str — e.g. '(32,619,022千元 - 40,254,346万元) / 345百万 * 100'",
            "output_unit: str|None — format result as 千/万/亿/% etc. (omit for raw number)",
        ],
        "fn": lambda expression, output_unit=None: _evaluate_expression(expression, output_unit),
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