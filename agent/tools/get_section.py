"""get_section — Get full text + all tables under a heading.
Full implementation extracted from Retriever.get_section.
"""

import os
import re

from agent.tools._loader import get_indices
from agent.tools.get_doc_info import resolve_doc
from agent.tools.search_tables import get_tables_under


def _normalize_heading(text: str) -> str:
    """Normalize a heading title for fuzzy matching.

    - Strips all non-Chinese characters.
    - Removes leading chapter prefixes like 第八章.
    This handles section-number mismatches (6. vs 6.2), Unicode bullets,
    extra whitespace, and trailing page numbers (....10).
    """
    # Remove leading chapter prefixes: 第八章 / 第1章
    text = re.sub(r"^第[一二三四五六七八九十\d]+章\s*", "", text)
    # Keep only CJK unified ideographs (Chinese characters)
    text = "".join(c for c in text if "\u4e00" <= c <= "\u9fff")
    return text


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

    # Collect all matching headings (same title may appear as TOC entry AND real section).
    # Use normalized titles so that "6.\u5982\u4f55\u9000\u4fdd" can match the real heading "\uf07a \u5982\u4f55\u9000\u4fdd".
    normalized_heading_path = [_normalize_heading(p) for p in heading_path]
    query_title = normalized_heading_path[-1]

    candidates = []
    for h in headings:
        h_path = h.get("path", [])
        normalized_h_path = [_normalize_heading(p) for p in h_path]
        path_match = (
            len(normalized_h_path) >= len(normalized_heading_path)
            and normalized_h_path[-len(normalized_heading_path):] == normalized_heading_path
        )
        title_match = _normalize_heading(h["title"]) == query_title
        if path_match or title_match:
            candidates.append(h)

    if not candidates:
        return None

    # Defense in depth:
    # 1. Reject paths that live inside a table-of-contents section.
    # 2. If the same title appears twice (TOC + real section), keep the later occurrence.
    # 3. Prefer markdown headings over html_table-extracted headings.
    # 4. Use span as a final tiebreaker.
    TOC_MARKERS = {"条款目录", "阅读指引", "目次", "目录", "contents", "table of contents"}

    def _has_page_number(title):
        # TOC entries often end with page numbers: ....10, ..... 25, . 16
        return bool(re.search(r"[\.\s]+\d+\s*$", title))

    def _in_toc(path, title):
        normalized = " ".join(p.lower() for p in path)
        if any(m in normalized for m in TOC_MARKERS):
            return True
        if _has_page_number(title):
            return True
        return False

    non_toc = [c for c in candidates if not _in_toc(c.get("path", []), c.get("title", ""))]
    pool = non_toc if non_toc else candidates  # fallback to TOC if no real section matches

    by_title = {}
    for c in pool:
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