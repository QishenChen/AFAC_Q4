"""get_doc_info — Document resolution and metadata lookup.
Contains resolve_doc, get_doc_info, list_docs_by_domain.
"""

import glob
import json
import os
from agent.tools._loader import get_indices, DOC_REGISTRY_PATH


def _load_doc_registry():
    return get_indices()["doc_registry"]


_SUMMARIES = {}


def _load_summaries():
    """Load summary from meta.json files → {doc_id: summary}."""
    global _SUMMARIES
    if _SUMMARIES:
        return _SUMMARIES
    meta_dir = "public_dataset_upload/meta.json/meta.json"
    for fpath in glob.glob(f"{meta_dir}/*.json"):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    doc_id = item.get("doc_id") or item.get("attachment_id", "")
                    summary = item.get("summary") or item.get("one_line_summary", "")
                    if doc_id and summary:
                        _SUMMARIES[doc_id] = summary
        except Exception:
            pass
    return _SUMMARIES


def _format_doc(doc: dict) -> dict:
    """Return doc metadata with one_line_summary and without friendly_name."""
    return {
        "doc_id": doc["doc_id"],
        "rel_path": doc["rel_path"],
        "domain": doc["domain"],
        "summary": _load_summaries().get(doc["doc_id"], ""),
    }


def _fuzzy_match_doc(identifier: str, doc_registry: dict) -> list[str]:
    """Resolve a doc_id to rel_path(s)."""
    from utils.text_utils import normalize_text, fuzzy_match

    if identifier in doc_registry["by_id"]:
        return [doc_registry["by_id"][identifier]["rel_path"]]

    candidates = []
    for doc in doc_registry["all_docs"]:
        score = fuzzy_match(identifier, doc["doc_id"])
        if score > 0.3:
            candidates.append((score, doc["rel_path"]))
    candidates.sort(key=lambda x: x[0], reverse=True)

    norm_id = normalize_text(identifier)
    for doc in doc_registry["all_docs"]:
        if norm_id in normalize_text(doc["doc_id"]):
            rel = doc["rel_path"]
            if rel not in [c[1] for c in candidates]:
                candidates.append((0.5, rel))

    return [c[1] for c in candidates[:5]]


def resolve_doc(identifier: str) -> list[str]:
    """Resolve a doc identifier (doc_id only) to a list of rel_paths."""
    return _fuzzy_match_doc(identifier, _load_doc_registry())


def get_doc_info(rel_path: str) -> dict | None:
    """Get metadata for a document by its rel_path."""
    doc_registry = _load_doc_registry()
    for doc in doc_registry["all_docs"]:
        if doc["rel_path"] == rel_path:
            return _format_doc(doc)
    return None


def list_docs_by_domain(domain: str) -> list[dict]:
    """List all documents in a given domain."""
    doc_registry = _load_doc_registry()
    return [_format_doc(d) for d in doc_registry["all_docs"] if d["domain"] == domain]
