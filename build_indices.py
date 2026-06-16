#!/usr/bin/env python3
"""
One-shot script to build all indices in order:
  1. heading_index.json + doc_registry.json (via indexer.py)
  2. table_index.json (via table_extractor.py, depends on heading_index)
"""

import subprocess
import sys
import os
import json
import time


def run_module(module_name: str):
    """Run a Python module and check exit code."""
    print(f"\n{'=' * 60}")
    print(f"Running: {module_name}")
    print(f"{'=' * 60}")
    start = time.time()
    result = subprocess.run([sys.executable, module_name], capture_output=False)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"ERROR: {module_name} failed with exit code {result.returncode}")
        sys.exit(1)
    print(f"  Completed in {elapsed:.1f}s")


def verify_indices():
    """Verify that all index files exist and are valid JSON."""
    indices_dir = "indices"
    required = ["heading_index.json", "doc_registry.json", "table_index.json"]
    for name in required:
        path = os.path.join(indices_dir, name)
        if not os.path.exists(path):
            print(f"ERROR: Missing {path}")
            return False
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  ✓ {name} — valid JSON ({_summarize(data, name)})")
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {name}: {e}")
            return False
    return True


def _summarize(data: dict, name: str) -> str:
    """Brief summary of an index file."""
    if name == "heading_index.json":
        docs = data.get("documents", {})
        n_docs = len(docs)
        n_headings = sum(len(v) for v in docs.values())
        n_inverted = len(data.get("inverted_index", {}))
        return f"{n_docs} docs, {n_headings} headings, {n_inverted} inverted keys"
    elif name == "doc_registry.json":
        n_docs = len(data.get("all_docs", []))
        return f"{n_docs} documents"
    elif name == "table_index.json":
        n_tables = data.get("total", 0)
        n_docs = len(data.get("by_doc", {}))
        return f"{n_tables} tables across {n_docs} docs"
    return ""


def main():
    print("Building financial knowledge retrieval indices...\n")

    # Step 1: Build heading index + doc registry
    run_module("indexer.py")

    # Step 2: Build table index (depends on heading index)
    run_module("table_extractor.py")

    # Verify
    print(f"\n{'=' * 60}")
    print("Verification")
    print(f"{'=' * 60}")
    if verify_indices():
        print("\nAll indices built successfully!")
    else:
        print("\nSome indices failed verification.")
        sys.exit(1)


if __name__ == "__main__":
    main()