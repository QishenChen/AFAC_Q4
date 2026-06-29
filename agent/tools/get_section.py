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

    # Defense in depth:
    # 1. Reject paths that live inside a table-of-contents section.
    # 2. If the same title appears twice (TOC + real section), keep the later occurrence.
    # 3. Prefer markdown headings over html_table-extracted headings.
    # 4. Use span as a final tiebreaker.
    TOC_MARKERS = {"条款目录", "阅读指引", "目次", "目录", "contents", "table of contents"}

    def _in_toc(path):
        normalized = " ".join(p.lower() for p in path)
        return any(m in normalized for m in TOC_MARKERS)

    non_toc = [c for c in candidates if not _in_toc(c.get("path", []))]
    if not non_toc:
        non_toc = candidates  # fallback: use everything if all were flagged

    by_title = {}
    for c in non_toc:
        title = c["title"]
        if title not in by_title or c["line_start"] > by_title[title]["line_start"]:
            by_title[title] = c
    deduped = list(by_title.values())

    def _score(h):
        span = h["line_end"] - h["line_start"]
        source_score = 1 if h.get("source") == "md" else 0
        return (source_score, span)

    target = max(deduped, key=_score)

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