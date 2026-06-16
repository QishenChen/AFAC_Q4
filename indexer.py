"""
Heading-based document indexer.
Builds a tree of headings per document and a flat inverted keyword index.

Output:
  indices/heading_index.json
  indices/doc_registry.json
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

from utils.text_utils import (
    normalize_text,
    is_heading_line,
    extract_inline_heading_from_html,
    tokenize_chinese,
    strip_html_tags,
)

EXTRACTED_DIR = "public_dataset_upload/extracted"
INDICES_DIR = "indices"


def find_all_md_files(base_dir: str) -> list[str]:
    """Recursively find all .md files."""
    md_files = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".md"):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, base_dir)
                md_files.append(rel_path)
    return sorted(md_files)


def parse_headings(filepath: str) -> list[dict]:
    """
    Parse headings from a markdown file.
    Returns list of heading dicts: {level, title, line_start, line_end, children}.
    Also detects inline headings inside HTML tables (e.g. '1.1 保险责任').
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    headings = []
    # First pass: detect all heading lines (both markdown and HTML-embedded)
    for lineno, line in enumerate(lines):
        is_h, level, title = is_heading_line(line)
        if is_h:
            headings.append({
                "level": level,
                "title": title,
                "line_start": lineno,
                "line_end": None,
                "children": [],
                "source": "md",
            })
        else:
            # Check for inline heading in HTML table cell
            stripped = strip_html_tags(line).strip()
            is_ih, depth, ih_title = extract_inline_heading_from_html(stripped)
            if is_ih:
                # Determine level: if we're inside a table, this is typically under an h2
                # We'll assign a provisional level; the tree builder will adjust
                headings.append({
                    "level": None,  # Will be resolved during tree building
                    "title": ih_title,
                    "line_start": lineno,
                    "line_end": None,
                    "children": [],
                    "source": "html_table",
                    "depth_hint": depth,
                })

    # Compute line_end for each heading (end = start of next heading at same or higher level, or EOF)
    for i, h in enumerate(headings):
        if h["level"] is not None:
            current_level = h["level"]
        else:
            # Not known yet; will be set during tree building
            h["line_end"] = len(lines)
            continue

        end = len(lines)
        for j in range(i + 1, len(headings)):
            next_h = headings[j]
            next_level = next_h.get("level")
            if next_level is not None and next_level <= current_level:
                end = next_h["line_start"]
                break
        h["line_end"] = end

    return headings


def build_heading_tree(headings: list[dict]) -> list[dict]:
    """
    Build a tree from a flat heading list using a parent stack.
    For headings with level=None (HTML-embedded), assign level based on parent context.
    """
    if not headings:
        return []

    root = []
    stack = []  # (node, level)

    for h in headings:
        if h["level"] is not None:
            level = h["level"]
        elif h.get("depth_hint") is not None:
            # Infer level from parent: parent_level + depth_hint, capped at 6
            parent_level = stack[-1][1] if stack else 2
            level = min(parent_level + h["depth_hint"], 6)
            h["level"] = level
        else:
            level = 3  # default fallback
            h["level"] = level

        node = {k: v for k, v in h.items()}

        # Pop from stack until we find a parent with level < current level
        while stack and stack[-1][1] >= level:
            stack.pop()

        if not stack:
            root.append(node)
        else:
            stack[-1][0]["children"].append(node)

        stack.append((node, level))

    return root


def extract_content(filepath: str, line_start: int, line_end: int) -> str:
    """Extract text content between line_start and line_end (0-indexed, exclusive end)."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    snippet = "".join(lines[line_start:line_end])
    return snippet


def build_inverted_index(all_headings: dict) -> dict:
    """
    Build a keyword → [(doc, heading_path, heading_title, line_start, line_end)] inverted index.
    """
    inverted = defaultdict(list)
    for doc_path, headings in all_headings.items():
        for h in headings:
            tokens = tokenize_chinese(h["title"])
            for tok in tokens:
                inverted[tok].append({
                    "doc": doc_path,
                    "title": h["title"],
                    "level": h["level"],
                    "line_start": h["line_start"],
                    "line_end": h["line_end"],
                })
    # Convert defaultdict to regular dict for JSON
    return dict(inverted)


def build_doc_registry(md_files: list[str], all_trees: dict) -> dict:
    """
    Build a doc_registry mapping:
      - doc_id (stem) → rel_path
      - friendly_name (first H1) → rel_path
      - rel_path → {doc_id, friendly_name, domain}
    """
    registry = {"by_id": {}, "by_name": {}, "all_docs": []}

    for rel_path in md_files:
        # Derive doc_id from filename stem
        stem = os.path.splitext(os.path.basename(rel_path))[0]
        # Domain from parent directory
        parts = Path(rel_path).parts
        domain = parts[0] if len(parts) > 0 else "unknown"

        # Find H1 title
        tree = all_trees.get(rel_path, [])
        friendly_name = tree[0]["title"] if tree else stem

        doc_info = {
            "doc_id": stem,
            "friendly_name": friendly_name,
            "rel_path": rel_path,
            "domain": domain,
        }

        registry["by_id"][stem] = doc_info
        registry["by_name"][friendly_name] = doc_info
        registry["all_docs"].append(doc_info)

    return registry


def main():
    os.makedirs(INDICES_DIR, exist_ok=True)

    print("Finding markdown files...")
    md_files = find_all_md_files(EXTRACTED_DIR)
    print(f"  Found {len(md_files)} .md files")

    all_trees = {}
    for rel_path in md_files:
        abs_path = os.path.join(EXTRACTED_DIR, rel_path)
        headings_flat = parse_headings(abs_path)
        tree = build_heading_tree(headings_flat)
        all_trees[rel_path] = tree

    # Flatten trees for indexing
    def flatten_tree(nodes, path_prefix=None):
        if path_prefix is None:
            path_prefix = []
        result = []
        for node in nodes:
            current_path = path_prefix + [node["title"]]
            result.append({
                "title": node["title"],
                "level": node["level"],
                "line_start": node["line_start"],
                "line_end": node["line_end"],
                "path": current_path,
                "source": node.get("source", "md"),
            })
            if node.get("children"):
                result.extend(flatten_tree(node["children"], current_path))
        return result

    all_flat = {}
    for doc, tree in all_trees.items():
        all_flat[doc] = flatten_tree(tree)

    print("Building heading index...")
    heading_index = {
        "documents": {},
        "inverted_index": {},
    }

    for doc, flat_nodes in all_flat.items():
        heading_index["documents"][doc] = flat_nodes

    inverted = build_inverted_index(all_flat)
    heading_index["inverted_index"] = inverted

    heading_index_path = os.path.join(INDICES_DIR, "heading_index.json")
    with open(heading_index_path, "w", encoding="utf-8") as f:
        json.dump(heading_index, f, ensure_ascii=False, indent=2)
    print(f"  Saved heading_index.json ({len(all_flat)} documents, {sum(len(v) for v in all_flat.values())} headings, {len(inverted)} inverted keys)")

    print("Building doc registry...")
    doc_registry = build_doc_registry(md_files, all_trees)
    registry_path = os.path.join(INDICES_DIR, "doc_registry.json")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(doc_registry, f, ensure_ascii=False, indent=2)
    print(f"  Saved doc_registry.json ({len(md_files)} documents)")

    return heading_index, doc_registry


if __name__ == "__main__":
    main()