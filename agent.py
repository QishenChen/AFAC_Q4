#!/usr/bin/env python3
"""
ReACT Agent: Financial Knowledge Q&A
Loads question JSON files, runs Think→Act→Observe loop per question,
outputs answers with evidence and token usage.
"""

import json
import os
import sys
import time
import argparse

from agent.question_loader import load_questions, list_question_files, estimate_tokens
from agent.react_loop import react_solve_one
from agent.llm_reasoner import reason_on_context, get_llm_config


def main():
    parser = argparse.ArgumentParser(description="ReACT Agent for Financial Q&A")
    parser.add_argument("--questions", "-q", type=str,
                        default="public_dataset_upload/questions/group_a/financial_contracts_questions.json",
                        help="Path to question JSON file or directory")
    parser.add_argument("--qid", type=str, default=None,
                        help="Solve only a specific question by qid")
    parser.add_argument("--output", "-o", type=str, default="results/answers.json",
                        help="Output file path")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed ReACT logs")
    parser.add_argument("--llm", action="store_true", default=True,
                        help="Use LLM for final reasoning (default: True)")
    parser.add_argument("--no-llm", action="store_false", dest="llm",
                        help="Skip LLM reasoning, just dump context")
    parser.add_argument("--per-option", action="store_true", default=False,
                        help="Use per-option loops (legacy mode, 6 rounds each). Default is batch (9 rounds).")
    args = parser.parse_args()

    # Determine input files
    if os.path.isdir(args.questions):
        question_files = list_question_files(args.questions)
    else:
        question_files = [args.questions]

    os.makedirs("results", exist_ok=True)

    all_results = []
    total_prompt = 0
    total_completion = 0
    total_questions = 0

    for qfile in question_files:
        print(f"\n{'=' * 70}")
        print(f"Processing: {qfile}")
        print(f"{'=' * 70}")

        questions = load_questions(qfile)
        domain = os.path.splitext(os.path.basename(qfile))[0]

        file_prompt = 0
        file_completion = 0
        file_results = []

        # Build answers mapping for this file
        file_answers = {}

        for q in questions:
            qid = q.get("qid", "unknown")

            # Filter by qid if specified
            if args.qid and qid != args.qid:
                continue

            print(f"\n  --- {qid} ---")
            print(f"  Q: {q['question'][:80]}...")

            start_time = time.time()
            result = react_solve_one(q, batch=not args.per_option)
            elapsed = time.time() - start_time

            # Derive answer string from options_detail
            answer_format = q.get("answer_format", "multi")
            options_detail = result.get("options_detail", {})
            true_keys = sorted(k for k, v in options_detail.items() if v.get("judgment") == "TRUE")
            if answer_format == "tf":
                answer_str = "B" if options_detail.get("A", {}).get("judgment") == "FALSE" else ("A" if options_detail.get("A", {}).get("judgment") == "TRUE" else "?")
            elif answer_format == "mcq":
                answer_str = true_keys[0] if true_keys else "?"
            else:
                answer_str = "".join(true_keys) if true_keys else "?"

            # Add answer field to result (keeping all existing fields)
            result["answer"] = answer_str

            # Token accounting: prompt from API, completion = 1 per question
            api_prompt = result["token_usage"]["prompt_tokens"]
            file_prompt += api_prompt
            file_completion += 1
            total_questions += 1

            # Update result token_usage to reflect 1 completion token per question
            result["token_usage"] = {
                "prompt_tokens": api_prompt,
                "completion_tokens": 1,
                "total": api_prompt + 1,
            }

            file_answers[qid] = answer_str

            status = result["status"]

            print(f"  Status: {status} | Answer: {answer_str} | Rounds: {result['rounds']} | "
                  f"Tokens: P={api_prompt} "
                  f"C=1 "
                  f"T={api_prompt + 1} | {elapsed:.1f}s")

            if args.verbose:
                for step in result.get("log_summary", []):
                    print(f"    {step}")

            # Print option judgments
            for opt_key, opt_detail in result.get("options_detail", {}).items():
                j = opt_detail["judgment"]
                r = opt_detail["reason"][:80]
                print(f"    [{j}] {opt_key}: {r}")

            file_results.append(result)

        # File summary
        print(f"\n  File total: P={file_prompt} C={file_completion} "
              f"T={file_prompt + file_completion}")

        all_results.extend(file_results)
        total_prompt += file_prompt
        total_completion += file_completion

    # Build combined answers dict
    all_answers = {}
    for r in all_results:
        all_answers[r["qid"]] = r.get("answer", "?")

    # Grand total
    print(f"\n{'=' * 70}")
    print(f"GRAND TOTAL")
    print(f"{'=' * 70}")
    print(f"  Questions: {total_questions}")
    print(f"  Total prompt_tokens:   {total_prompt}")
    print(f"  Total completion_tokens: {total_completion}")
    print(f"  Total tokens:          {total_prompt + total_completion}")
    print(f"  Avg tokens/question:   {(total_prompt + total_completion) // max(1, total_questions)}")

    # Add summary row
    all_results.append({
        "qid": "summary",
        "answers": all_answers,
        "prompt_tokens": total_prompt,
        "completion_tokens": total_completion,
        "total_tokens": total_prompt + total_completion,
    })

    # Write output
    output = {
        "meta": {
            "total_questions": total_questions,
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "total_tokens": total_prompt + total_completion,
        },
        "results": all_results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()