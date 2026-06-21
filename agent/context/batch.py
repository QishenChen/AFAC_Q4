"""Batch evaluation — one shared retrieval loop gathering context for ALL options,
then simultaneous judgment via reason_on_context (MCQ, max 9 rounds)."""

import json
from agent.tools import execute_tool
from agent.llm_reasoner import get_llm_config
from agent.context._common import (
    MAX_ROUNDS, BATCH_MAX_ROUNDS,
    build_single_option_context, observe_result, _gather_data, _prune_by_keep, _parse_multi_actions,
)
from agent.context._common import run_react_loop


def solve_batch(question, doc_status, config=None):
    """
    Batch evaluation: one shared retrieval loop gathering context for ALL options,
    then simultaneous judgment via reason_on_context.
    """
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    question_text = question.get("question", "")
    options = question.get("options", {})
    if config is None:
        config = get_llm_config()

    # Build a question that presents ALL options at once
    options_text = "\n".join([f"  {k}: {v}" for k, v in sorted(options.items())])
    batch_question = {
        "qid": qid, "domain": domain,
        "question": f"{question_text}\n\nAll options to evaluate:\n{options_text}",
        "options": options,
        "doc_ids": question.get("doc_ids", []),
    }
    opt_result = run_react_loop(batch_question, "all", "Evaluate all options",
                                doc_status, config, max_rounds=BATCH_MAX_ROUNDS)

    total_prompt = opt_result["token_usage"]["prompt_tokens"]
    total_completion = opt_result["token_usage"]["completion_tokens"]

    # Use LLM self-judgment directly — no second reason_on_context call
    judgment = opt_result.get("judgment")
    evidence = opt_result.get("evidence", "")
    reasoning = opt_result.get("reason", "")

    if isinstance(judgment, dict):
        # LLM returned per-option judgments: {"A": "TRUE", "B": "TRUE", ...}
        options_detail = {}
        for key in sorted(options.keys()):
            val = judgment.get(key, "VAGUE")
            if isinstance(val, str):
                options_detail[key] = {"judgment": val, "reason": "LLM self-judged", "evidence": evidence}
            elif isinstance(val, dict):
                options_detail[key] = val
            else:
                options_detail[key] = {"judgment": "VAGUE", "reason": "No judgment returned", "evidence": ""}
    elif isinstance(judgment, str) and ":" in judgment:
        # LLM returned pipe-separated format: "A:TRUE|B:TRUE|C:FALSE|D:TRUE"
        options_detail = {}
        parts = judgment.split("|")
        for part in parts:
            if ":" in part:
                k, v = part.split(":", 1)
                k, v = k.strip(), v.strip()
                if k in options:
                    options_detail[k] = {"judgment": v, "reason": "LLM self-judged", "evidence": evidence}
        # Fill in missing
        for key in sorted(options.keys()):
            if key not in options_detail:
                options_detail[key] = {"judgment": "VAGUE", "reason": "Not in self-judgment", "evidence": ""}
    else:
        # LLM gave flat VAGUE or no judgment → all VAGUE
        options_detail = {k: {"judgment": "VAGUE", "reason": "Insufficient evidence", "evidence": evidence} for k in sorted(options.keys())}

    all_logs = [f"-- Batch ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --"]
    all_logs.extend(opt_result["log_summary"])

    judgments = [v["judgment"] for v in options_detail.values()]
    status = "VAGUE_ALL" if all(j == "VAGUE" for j in judgments) else (
        "PARTIAL" if "VAGUE" in judgments else "RESOLVED")

    return {
        "qid": qid, "domain": domain, "question": question_text, "status": status,
        "answer_format": question.get("answer_format", ""), "options_detail": options_detail,
        "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion,
                        "total": total_prompt + total_completion},
        "llm_model": config["model"], "rounds": "batch", "log_summary": all_logs,
        "options_processed": len(options),
    }