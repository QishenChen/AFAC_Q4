#!/usr/bin/env python3
"""Analyze word frequencies across all extracted markdown documents using jieba."""

import json
import os
import re
import jieba

EXTRACTED_DIR = "public_dataset_upload/extracted"
OUTPUT_FILE = "config/common_words.json"
MIN_COUNT = 5  # Minimum occurrences to include
TOP_N = 200  # Top N words to output


def main():
    freq = {}
    total_docs = 0
    total_words = 0

    for root, dirs, files in os.walk(EXTRACTED_DIR):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    text = f.read()
                # Remove markdown syntax
                text = re.sub(r"#+ ", "", text)
                text = re.sub(r"\*+", "", text)
                text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
                text = re.sub(r"\n+", " ", text)
                words = jieba.lcut(text)
                # Filter: only Chinese words with 2+ chars
                chinese_words = [w for w in words if re.match(r"^[\u4e00-\u9fff]{2,}$", w)]
                for w in chinese_words:
                    freq[w] = freq.get(w, 0) + 1
                    total_words += 1
                total_docs += 1
            except Exception as e:
                print(f"Warning: {fpath}: {e}")

    # Filter and sort
    filtered = {w: c for w, c in freq.items() if c >= MIN_COUNT}
    sorted_words = sorted(filtered.items(), key=lambda x: -x[1])[:TOP_N]

    result = {
        "total_docs": total_docs,
        "total_words": total_words,
        "unique_words": len(freq),
        "words": [{"word": w, "count": c} for w, c in sorted_words],
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Analyzed {total_docs} documents, {total_words} words, {len(freq)} unique")
    print(f"\nTop {TOP_N} words:")
    print(f"{'Word':12s} {'Count':8s}")
    print("-" * 22)
    for w, c in sorted_words:
        print(f"{w:12s} {c:8d}")
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()