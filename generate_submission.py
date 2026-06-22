#!/usr/bin/env python3
"""Generate submission CSV from results/answers.json + question files.
For "?" answers, randomly picks a valid option key."""

import csv
import json
import os
import random
import sys

QUESTION_DIR = "public_dataset_upload/questions/group_a"
RESULTS_PATH = sys.argv[1] if len(sys.argv) > 1 else "results/answers.json"
OUTPUT_CSV = sys.argv[2] if len(sys.argv) > 2 else "results/submission.csv"


def load_all_questions() -> dict[str, dict]:
    """Load all questions from group_a/ and return {qid: question_dict}."""
    questions = {}
    for fname in sorted(os.listdir(QUESTION_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(QUESTION_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            for q in json.load(f):
                questions[q["qid"]] = q
    return questions


def pick_random_option(options: dict, answer_format: str) -> str:
    """Pick a random valid option key based on answer format."""
    keys = sorted(options.keys())
    if answer_format == "tf":
        return random.choice(["A", "B"])  # TF always A/B
    if answer_format == "mcq":
        return random.choice(keys)  # single character
    # multi
    return random.choice(keys)


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"ERROR: {RESULTS_PATH} not found. Run agent.py first.")
        sys.exit(1)

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = load_all_questions()

    rows = []
    total_prompt = 0
    total_completion = 0
    total_total = 0

    for result in data.get("results", []):
        qid = result.get("qid", "")
        if qid == "summary":
            total_prompt += result.get("prompt_tokens", 0)
            total_completion += result.get("completion_tokens", 0)
            total_total += result.get("total_tokens", 0)
            continue

        answer = result.get("answer", "?")
        prompt_tokens = result.get("token_usage", {}).get("prompt_tokens", 0)
        completion_tokens = result.get("token_usage", {}).get("completion_tokens", 0)
        total = result.get("token_usage", {}).get("total", 0)

        total_prompt += prompt_tokens
        total_completion += completion_tokens
        total_total += total

        # If answer is "?", randomly pick one
        if answer == "?":
            q = questions.get(qid, {})
            options = q.get("options", {"A": "", "B": ""})
            answer_format = q.get("answer_format", "multi")
            answer = pick_random_option(options, answer_format)
            print(f"  {qid}: ? → random {answer}")

        rows.append([qid, answer, str(prompt_tokens), str(completion_tokens), str(total)])

    # Summary row
    rows.append(["summary", "", str(total_prompt), str(total_completion), str(total_total)])

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["qid", "answer", "prompt_tokens", "completion_tokens", "total_tokens"])
        writer.writerows(rows)

    print(f"\nWrote {len(rows) - 1} questions + summary to {OUTPUT_CSV}")
    print(f"  Total prompt_tokens:    {total_prompt}")
    print(f"  Total completion_tokens: {total_completion}")
    print(f"  Total total_tokens:      {total_total}")


if __name__ == "__main__":
    main()