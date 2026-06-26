#!/usr/bin/env python3
"""Merge rerun_*.json results into existing all_answers.json, replacing old entries."""

import json
import os
import glob

ALL_ANSWERS = "results/all_answers.json"
RERUN_PATTERN = "results/rerun_*.json"


def main():
    if not os.path.exists(ALL_ANSWERS):
        print(f"ERROR: {ALL_ANSWERS} not found")
        return

    with open(ALL_ANSWERS, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", [])
    # Build lookup: qid → index
    qid_to_idx = {}
    for i, r in enumerate(results):
        qid = r.get("qid", "")
        if qid and qid != "summary":
            qid_to_idx[qid] = i

    updated = 0
    for fpath in sorted(glob.glob(RERUN_PATTERN)):
        qid = os.path.basename(fpath).replace("rerun_", "").replace(".json", "")
        with open(fpath, "r", encoding="utf-8") as f:
            rerun_data = json.load(f)

        rerun_results = rerun_data.get("results", [])
        for rr in rerun_results:
            rqid = rr.get("qid", "")
            if rqid == "summary":
                continue
            if rqid in qid_to_idx:
                old_idx = qid_to_idx[rqid]
                old_answer = results[old_idx].get("answer", "?")
                new_answer = rr.get("answer", "?")
                results[old_idx] = rr  # replace entire entry
                print(f"  {rqid}: {old_answer} → {new_answer}")
                updated += 1
            else:
                results.append(rr)
                qid_to_idx[rqid] = len(results) - 1
                print(f"  {rqid}: (new) {rr.get('answer', '?')}")
                updated += 1

    # Rebuild summary row
    all_answers = {}
    total_prompt = 0
    total_completion = 0
    question_count = 0
    for r in results:
        qid = r.get("qid", "")
        if qid == "summary":
            continue
        all_answers[qid] = r.get("answer", "?")
        total_prompt += r.get("token_usage", {}).get("prompt_tokens", 0)
        total_completion += r.get("token_usage", {}).get("completion_tokens", 0)
        question_count += 1

    # Remove old summary, add new
    results = [r for r in results if r.get("qid") != "summary"]
    results.append({
        "qid": "summary",
        "answers": all_answers,
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "total_tokens": total_prompt + total_completion,
    })

    data["results"] = results
    data["meta"]["total_questions"] = question_count
    data["meta"]["total_prompt_tokens"] = total_prompt
    data["meta"]["total_completion_tokens"] = total_completion
    data["meta"]["total_tokens"] = total_prompt + total_completion

    with open(ALL_ANSWERS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nUpdated {updated} questions in {ALL_ANSWERS}")
    print(f"  Total questions: {question_count}")
    print(f"  Total prompt_tokens: {total_prompt}")
    print(f"  Total completion_tokens: {total_completion}")
    print(f"  Total tokens: {total_prompt + total_completion}")


if __name__ == "__main__":
    main()