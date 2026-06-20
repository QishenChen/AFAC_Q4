"""get_doc_info — Document resolution and metadata lookup.
Contains resolve_doc, get_doc_info, list_docs_by_domain.
"""

import os
from agent.tools._loader import get_indices, DOC_REGISTRY_PATH


def _load_doc_registry():
    return get_indices()["doc_registry"]


def _fuzzy_match_doc(identifier: str, doc_registry: dict) -> list[str]:
    """Resolve a doc_id or friendly_name to rel_path(s)."""
    from utils.text_utils import normalize_text, fuzzy_match

    if identifier in doc_registry["by_id"]:
        return [doc_registry["by_id"][identifier]["rel_path"]]
    if identifier in doc_registry["by_name"]:
        return [doc_registry["by_name"][identifier]["rel_path"]]

    candidates = []
    for doc in doc_registry["all_docs"]:
        score_doc_id = fuzzy_match(identifier, doc["doc_id"])
        score_name = fuzzy_match(identifier, doc["friendly_name"])
        score = max(score_doc_id, score_name)
        if score > 0.3:
            candidates.append((score, doc["rel_path"]))
    candidates.sort(key=lambda x: x[0], reverse=True)

    norm_id = normalize_text(identifier)
    for doc in doc_registry["all_docs"]:
        if norm_id in normalize_text(doc["doc_id"]) or norm_id in normalize_text(doc["friendly_name"]):
            rel = doc["rel_path"]
            if rel not in [c[1] for c in candidates]:
                candidates.append((0.5, rel))

    return [c[1] for c in candidates[:5]]


def resolve_doc(identifier: str) -> list[str]:
    """Resolve a doc identifier (id/name) to a list of rel_paths."""
    return _fuzzy_match_doc(identifier, _load_doc_registry())


def get_doc_info(rel_path: str) -> dict | None:
    """Get metadata for a document by its rel_path."""
    doc_registry = _load_doc_registry()
    for doc in doc_registry["all_docs"]:
        if doc["rel_path"] == rel_path:
            return doc
    return None


def list_docs_by_domain(domain: str) -> list[dict]:
    """List all documents in a given domain."""
    doc_registry = _load_doc_registry()
    return [d for d in doc_registry["all_docs"] if d["domain"] == domain]