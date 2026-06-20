"""search_text — Search raw text content of a document.
Full implementation extracted from Retriever.search_section_text.
"""

import os

from agent.tools._loader import get_indices
from agent.tools._shared import MIN_SCORE, _split_pipe_query
from agent.tools.get_doc_info import resolve_doc
from utils.text_utils import strip_html_tags, fuzzy_match


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


def search_text(doc: str, query: str, max_results: int = 10):
    """Search raw text content of a document — finds clauses, statements, non-table text.
    doc is REQUIRED. Split query into individual terms with |."""
    docs = resolve_doc(doc)
    if not docs:
        return []
    rel_path = docs[0]
    filepath = os.path.join("public_dataset_upload/extracted", rel_path)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    clean = strip_html_tags(content)
    raw_lines = clean.split("\n")
    matches = []
    for i, line in enumerate(raw_lines):
        stripped = line.strip()
        if not stripped:
            continue
        if _multi_fuzzy_match_and(query, stripped) >= MIN_SCORE:
            start = max(0, i - 2)
            end = min(len(raw_lines), i + 3)
            ctx = "\n".join(rl.strip() for rl in raw_lines[start:end] if rl.strip())
            matches.append({"line_num": i, "text": ctx[:1200]})
    return matches[:max_results]