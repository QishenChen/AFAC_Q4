#!/usr/bin/env python3
"""Show LLM search keywords and their synonym expansions per question.

Reads results/keywords/{qid}/keywords.jsonl and prints a readable summary.
"""

import json
import os
import sys
from collections import defaultdict


KEYWORDS_DIR = "results/keywords"


def load_records(qid_filter: str | None = None):
    records = []
    if not os.path.isdir(KEYWORDS_DIR):
        return records
    for qid in sorted(os.listdir(KEYWORDS_DIR)):
        if qid_filter and qid != qid_filter:
            continue
        path = os.path.join(KEYWORDS_DIR, qid, "keywords.jsonl")
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def summarize_by_qid(records):
    by_qid = defaultdict(lambda: defaultdict(list))
    for r in records:
        qid = r.get("qid", "unknown")
        tool = r.get("tool_name", "unknown")
        by_qid[qid][tool].append(r)
    return by_qid


def main():
    qid_filter = sys.argv[1] if len(sys.argv) > 1 else None
    records = load_records(qid_filter)
    if not records:
        print(f"No keyword records found in {KEYWORDS_DIR}")
        return

    by_qid = summarize_by_qid(records)
    for qid in sorted(by_qid.keys()):
        print(f"\n{qid}")
        for tool in sorted(by_qid[qid].keys()):
            print(f"  {tool}")
            seen = set()
            for r in by_qid[qid][tool]:
                query = r.get("original_query", "")
                if query in seen:
                    continue
                seen.add(query)
                expanded = r.get("expanded_terms", {})
                print(f"    \"{query}\"")
                for term, syns in expanded.items():
                    print(f"      {term} -> {', '.join(syns)}")


if __name__ == "__main__":
    main()
