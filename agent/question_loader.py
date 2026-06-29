"""
Load question JSON files and check document availability.
"""

import glob
import json
import os

from agent.tools.get_doc_info import get_doc_info, resolve_doc


def load_questions(filepath: str) -> list[dict]:
    """Load a question JSON file. Returns list of question dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)
    return questions


def check_doc_availability(doc_ids: list[str]) -> dict[str, dict]:
    """
    Check which doc_ids exist in the registry.
    Returns dict: {doc_id: {available: bool, info: {...}} or {available: false, reason: str}}
    """
    result = {}
    for doc_id in doc_ids:
        rel_paths = resolve_doc(doc_id)
        if not rel_paths:
            result[doc_id] = {
                "available": False,
                "reason": f"doc_id '{doc_id}' not found in extracted documents",
            }
            continue

        info = get_doc_info(rel_paths[0])
        if info is None:
            result[doc_id] = {
                "available": False,
                "reason": f"doc_id '{doc_id}' resolved but metadata not found",
            }
            continue

        result[doc_id] = {
            "available": True,
            "rel_path": info["rel_path"],
            "domain": info["domain"],
            "summary": info.get("summary", ""),
        }

    return result


def list_question_files(questions_dir: str = "public_dataset_upload/questions/group_a") -> list[str]:
    """List all question JSON files in a directory."""
    files = []
    for fname in sorted(os.listdir(questions_dir)):
        if fname.endswith(".json"):
            files.append(os.path.join(questions_dir, fname))
    return files


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation: ~4 Chinese chars = 1 token, ~0.75 English words = 1 token.
    For simplicity: len(text) // 3 (mixed Chinese/English average).
    """
    if not text:
        return 0
    # Count Chinese characters
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    non_chinese = len(text) - chinese_chars
    # ~1.5 Chinese chars per token, ~4 English chars per token
    tokens = int(chinese_chars / 1.3 + non_chinese / 3.5)
    return max(1, tokens)
