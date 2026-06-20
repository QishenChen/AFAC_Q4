"""get_section — Get full text + all tables under a heading.
Full implementation extracted from Retriever.get_section.
"""

import os

from agent.tools._loader import get_indices
from agent.tools.get_doc_info import resolve_doc
from agent.tools.search_tables import get_tables_under


def get_section(doc: str, heading_path):
    """Get FULL text + ALL tables under a heading.
    heading_path is the exact title from search_headings results.
    Accepts str or list[str] for LLM tolerance.
    """
    # Auto-wrap string to list for LLM tolerance.
    # If the string contains " > " separators (from search_headings path display),
    # split into individual segments so suffix-matching works against the index.
    if isinstance(heading_path, str):
        if " > " in heading_path:
            heading_path = [s.strip() for s in heading_path.split(" > ")]
        else:
            heading_path = [heading_path]

    docs = resolve_doc(doc)
    if not docs:
        return None
    rel_path = docs[0]

    indices = get_indices()
    heading_index = indices["heading_index"]
    headings = heading_index["documents"].get(rel_path, [])
    if not headings:
        return None

    # Collect all matching headings (same title may appear as TOC entry AND real section)
    candidates = []
    for h in headings:
        h_path = h.get("path", [])
        if len(h_path) >= len(heading_path) and h_path[-len(heading_path):] == heading_path:
            candidates.append(h)

    if not candidates:
        return None

    # Prefer the heading with the largest content span (skip TOC entries with ~1-5 lines)
    target = max(candidates, key=lambda h: h["line_end"] - h["line_start"])

    filepath = os.path.join("public_dataset_upload/extracted", rel_path)
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    content = "".join(lines[target["line_start"]:target["line_end"]])

    tables = get_tables_under(doc, target["title"])
    return {
        "doc": rel_path,
        "heading": target["title"],
        "heading_path": target["path"],
        "line_start": target["line_start"],
        "line_end": target["line_end"],
        "content": content,
        "tables": tables,
    }