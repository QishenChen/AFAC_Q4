"""search_text — Search raw text content of a document.
Full implementation extracted from Retriever.search_section_text.
"""

import os

from agent.tools._loader import get_indices
from agent.tools._shared import MIN_SCORE, _split_pipe_query
from agent.tools.expand_query import expand_query_to_sets
from agent.tools.keyword_tracker import record_search_keywords
from agent.tools.get_doc_info import resolve_doc
from utils.text_utils import strip_html_tags, normalize_text


def _synonym_set_score(synonym_sets: dict[str, set[str]], target: str) -> float:
    """Synonym-normalized exact-match score.

    For each original query term, count how many of its synonyms are present
    in the target and divide by the synonym-set size. The final score is the
    sum across all original terms.
    """
    total = 0.0
    for syns in synonym_sets.values():
        if not syns:
            continue
        matched = sum(1 for syn in syns if syn in target)
        total += matched / len(syns)
    return total


def search_text(doc: str, query: str, max_results: int = 10, qid: str | None = None):
    """Search raw text content of a document — finds clauses, statements, non-table text.
    doc is REQUIRED. Split query into individual terms with |.
    Duplicate context windows are collapsed and a short note is appended when that happens."""
    docs = resolve_doc(doc)
    if not docs:
        return []
    rel_path = docs[0]
    filepath = os.path.join("public_dataset_upload/extracted", rel_path)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    clean = strip_html_tags(content)
    raw_lines = clean.split("\n")

    synonym_sets = expand_query_to_sets(query)
    record_search_keywords(qid or doc, "search_text", query, synonym_sets)

    matches = []
    seen = set()
    duplicates_skipped = 0
    for i, line in enumerate(raw_lines):
        stripped = line.strip()
        if not stripped:
            continue
        score = _synonym_set_score(synonym_sets, stripped)
        if score >= MIN_SCORE:
            # Skip exact duplicate lines (same normalized line text) to avoid redundant context.
            norm_line = normalize_text(stripped)
            if norm_line in seen:
                duplicates_skipped += 1
                continue
            seen.add(norm_line)
            start = max(0, i - 2)
            end = min(len(raw_lines), i + 3)
            ctx = "\n".join(rl.strip() for rl in raw_lines[start:end] if rl.strip())
            matches.append({"line_num": i, "text": ctx[:1200], "score": round(score, 3)})

    matches.sort(key=lambda x: x["score"], reverse=True)
    if duplicates_skipped > 0:
        matches.append({
            "line_num": -1,
            "text": f"[NOTE] {duplicates_skipped} duplicate search result(s) were omitted.",
            "score": 0.0,
            "note": True,
        })
    return matches[:max_results]
