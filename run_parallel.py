#!/usr/bin/env python3
"""Run agent.py on all 5 question categories in parallel using subprocesses."""

import os
import sys
import json
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

QUESTION_DIR = "public_dataset_upload/questions/group_a"
RESULTS_DIR = "results"
CATEGORIES = [
    "financial_contracts_questions",
    "financial_reports_questions",
    "insurance_questions",
    "regulatory_questions",
    "research_questions",
]


def run_category(category: str) -> tuple[str, str, dict | None]:
    """Run agent.py for one category. Returns (category, output_path, data_or_None)."""
    questions_file = os.path.join(QUESTION_DIR, f"{category}.json")
    output_file = os.path.join(RESULTS_DIR, f"{category}_answers.json")

    print(f"[{category}] Starting...")
    start = time.time()

    result = subprocess.run(
        [sys.executable, "agent.py",
         "--questions", questions_file,
         "--output", output_file],
        capture_output=True,
        text=True,
        timeout=3600,  # 1 hour per category
    )

    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"[{category}] FAILED after {elapsed:.0f}s")
        print(f"  stderr: {result.stderr[-500:]}")
        return category, output_file, None

    print(f"[{category}] Done in {elapsed:.0f}s")
    # Print last few lines of stdout
    for line in result.stdout.strip().split("\n")[-5:]:
        print(f"  {line}")

    # Load the output
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return category, output_file, data
    return category, output_file, None


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    all_results = []
    total_prompt = 0
    total_completion = 0
    questions_count = 0

    start_time = time.time()

    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(run_category, cat): cat for cat in CATEGORIES}

        for future in as_completed(futures):
            cat, out_path, data = future.result()
            if data is None:
                print(f"\n⚠ {cat} failed — skipping in merge")
                continue

            meta = data.get("meta", {})
            total_prompt += meta.get("total_prompt_tokens", 0)
            total_completion += meta.get("total_completion_tokens", 0)
            results = data.get("results", [])
            questions_count += len([r for r in results if r.get("qid") != "summary"])

            # Keep only question results, skip per-file summary rows
            for r in results:
                if r.get("qid") == "summary":
                    # Add token counts from file-level summary
                    total_prompt += r.get("prompt_tokens", 0)
                    total_completion += r.get("completion_tokens", 0)
                    continue
                all_results.append(r)

    # Add grand summary
    all_results.append({
        "qid": "summary",
        "answers": {r["qid"]: r.get("answer", "?") for r in all_results},
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "total_tokens": total_prompt + total_completion,
    })

    total_elapsed = time.time() - start_time

    output = {
        "meta": {
            "total_questions": questions_count,
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "total_tokens": total_prompt + total_completion,
            "parallel_elapsed_s": int(total_elapsed),
        },
        "results": all_results,
    }

    merged_path = os.path.join(RESULTS_DIR, "all_answers.json")
    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 70}")
    print(f"ALL DONE in {total_elapsed:.0f}s ({total_elapsed / 60:.1f}m)")
    print(f"  Questions: {questions_count}")
    print(f"  Total prompt_tokens:    {total_prompt}")
    print(f"  Total completion_tokens: {total_completion}")
    print(f"  Total tokens:           {total_prompt + total_completion}")
    print(f"  Merged to: {merged_path}")


if __name__ == "__main__":
    main()