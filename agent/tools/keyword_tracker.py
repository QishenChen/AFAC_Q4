"""keyword_tracker — Persist LLM search keywords and their synonym expansions."""

import json
import os
from datetime import datetime


KEYWORDS_DIR = "results/keywords"


def _ensure_dir(qid: str) -> str:
    path = os.path.join(KEYWORDS_DIR, qid)
    os.makedirs(path, exist_ok=True)
    return path


def record_search_keywords(qid: str, tool_name: str, original_query: str,
                           synonym_sets: dict[str, set[str]]):
    """Append one record of a search query and its synonym expansion.

    Args:
        qid: Question id, e.g. 'ins_a_002'.
        tool_name: Tool that performed the search, e.g. 'search_text'.
        original_query: Query string exactly as issued by the LLM.
        synonym_sets: Mapping from each original term to its expanded synonym set.
    """
    if not original_query or not original_query.strip():
        return
    qid = qid or "unknown"
    path = _ensure_dir(qid)
    record = {
        "timestamp": datetime.now().isoformat(),
        "qid": qid,
        "tool_name": tool_name,
        "original_query": original_query,
        "expanded_terms": {k: sorted(v) for k, v in synonym_sets.items()},
    }
    filepath = os.path.join(path, "keywords.jsonl")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
