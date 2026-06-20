"""
Agent Tools — auto-registry.
Scans this directory for tool modules (*.py) and their prompt cards (*.md).
Provides TOOLS dict and execute_tool() for the ReACT loop.
"""
# fmt: off

import os
import importlib.util

# ── Lightweight registration ──────────────────────────────
# Each tool is registered here with its function reference.
# Internal tools (no .md) are included but not in LLM prompts.

from agent.tools.search_headings import search_headings
from agent.tools.search_tables import search_tables
from agent.tools.search_text import search_text
from agent.tools.get_section import get_section
from agent.tools.compute import compute
from agent.tools.expand_query import expand_query
from agent.tools.get_doc_info import get_doc_info

TOOLS = {
    # ── Heading search ──
    "search_headings": {
        "name": "search_headings",
        "desc": "Search section headings by keyword. Use | to separate terms. Set doc to limit to one document.",
        "params": ["query: str", "doc: str|None", "domain: str|None", "max_results: int=10"],
        "fn": search_headings,
    },
    # ── Table search (unified) ──
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
        "fn": search_tables,
    },
    # ── Raw text search ──
    "search_text": {
        "name": "search_text",
        "desc": "Search RAW TEXT (not tables) in a document. Split query into individual terms with |. doc is REQUIRED.",
        "params": ["doc: str", "query: str — use | to split terms", "max_results: int=8"],
        "fn": search_text,
    },
    # Alias: LLM sometimes uses legacy retriever.py name
    "search_section_text": {
        "name": "search_section_text",
        "desc": "Alias for search_text — search raw text in a document.",
        "params": ["doc: str", "query: str", "max_results: int=8"],
        "fn": search_text,
    },
    # ── Full section content + tables ──
    "get_section": {
        "name": "get_section",
        "desc": "Get FULL text + ALL tables under a heading. heading_path is the exact title from search_headings results.",
        "params": ["doc: str", "heading_path: str|list[str] — e.g. '二、财务报表' or ['二、财务报表']"],
        "fn": get_section,
    },
    # ── Unit-aware calculator ──
    "compute": {
        "name": "compute",
        "desc": "Evaluate arithmetic with unit-aware numbers. Supports 万亿/亿/万/千/万元/千元/百/元/M/K/B/%. Always return ground-truth numbers.",
        "params": [
            "expression: str — e.g. '(32,619,022千元 - 40,254,346万元) / 345百万 * 100'",
            "output_unit: str|None — format result as 千/万/亿/% etc. (omit for raw number)",
        ],
        "fn": compute,
    },
    # ── Utility (not exposed to LLM prompt) ──
    "expand_query": {
        "name": "expand_query",
        "desc": "Expand query with financial synonyms (internal use).",
        "params": ["query: str"],
        "fn": expand_query,
    },
    "get_doc_info": {
        "name": "get_doc_info",
        "desc": "Get metadata for a document.",
        "params": ["rel_path: str"],
        "fn": get_doc_info,
    },
}


def execute_tool(name: str, **kwargs) -> dict:
    """Execute a tool by name. Returns {"result": ..., "error": ...}."""
    if name not in TOOLS:
        return {"error": f"Unknown tool: {name}", "result": None}
    try:
        fn = TOOLS[name]["fn"]
        result = fn(**kwargs)
        return {"result": result, "error": None}
    except Exception as e:
        return {"error": str(e), "result": None}


def build_tools_prompt() -> str:
    """Build the LLM-facing tools description by reading .md files for public tools."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    lines = ["Available tools (use | to separate multiple keywords, e.g. \"利润|资产|负债\"):", ""]
    prompt_order = ["search_headings", "search_tables", "search_text", "get_section", "compute"]
    for name in prompt_order:
        md_path = os.path.join(_dir, f"{name}.md")
        if os.path.isfile(md_path):
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            lines.append(content)
            lines.append("")
    return "\n".join(lines)