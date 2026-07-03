"""Batch evaluation — one shared retrieval loop gathering context for ALL options,
then simultaneous judgment via reason_on_context (MCQ, max 9 rounds)."""

import json
import os
from agent.tools import execute_tool
from agent.llm_reasoner import get_llm_config, reason_on_context
from agent.context._common import (
    MAX_ROUNDS, BATCH_MAX_ROUNDS,
    build_single_option_context, observe_result, _gather_data, _prune_by_keep, _parse_multi_actions,
    _sanitize_filename,
)
from agent.context._common import run_react_loop
from agent.tools.get_doc_info import _load_doc_registry


def _build_fallback_context(qid, keep_labels, doc_ids):
    """Build a flat context of document sources + full kept evidence."""
    doc_registry = _load_doc_registry()
    doc_lines = []
    for did in sorted(doc_ids):
        info = doc_registry.get("by_id", {}).get(did, {})
        name = info.get("friendly_name", "") or did
        doc_lines.append(f"{did}: {name} doc_id: {did}")

    evidence_parts = []
    for lbl in sorted(keep_labels):
        safe = _sanitize_filename(lbl)
        path = f"results/search_results/{qid}/{safe}.json"
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("note"):
            continue
        content = (
            data.get("text", "")
            or data.get("content_preview", "")
            or json.dumps(data, ensure_ascii=False, indent=2)
        )
        evidence_parts.append(f"{lbl}:\n{content[:1200]}")

    parts = ["Documents:\n" + "\n".join(doc_lines)]
    if evidence_parts:
        parts.append("Evidence:\n" + "\n\n".join(evidence_parts))
    return "\n\n".join(parts)[:12000]


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

    # Build a question that presents ALL options at once.
    # The active options are rendered dynamically by build_think_prompt; do not
    # embed them here, or resolved options would remain visible in the prompt
    # after being pruned from mini_question["options"].
    batch_question = {
        "qid": qid, "domain": domain,
        "question": question_text,
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

    # Fallback final judgment when the ReACT loop is under-confident
    answer_format = question.get("answer_format", "")
    true_count = sum(1 for d in options_detail.values() if d.get("judgment") == "TRUE")
    needs_fallback = (
        (answer_format == "multi" and true_count < 2) or
        (answer_format == "mcq" and true_count == 0)
    )
    all_logs = [f"-- Batch ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --"]
    all_logs.extend(opt_result["log_summary"])

    if needs_fallback:
        keep_labels = opt_result.get("cumulative_keep", [])
        fallback_context = _build_fallback_context(qid, keep_labels, question.get("doc_ids", []))
        full_context = f"Question: {question_text}\n\n{fallback_context}"
        fallback = reason_on_context(full_context, question, config)
        fb_detail = fallback.get("options_detail", {})
        for key in sorted(options.keys()):
            detail = fb_detail.get(key, {})
            options_detail[key] = {
                "judgment": detail.get("judgment", "VAGUE"),
                "reason": "[FALLBACK] " + detail.get("reason", "Final judgment from kept evidence"),
                "evidence": detail.get("evidence", ""),
            }
        total_prompt += fallback.get("llm_prompt_tokens", 0)
        total_completion += fallback.get("llm_completion_tokens", 0)
        all_logs.append("-- Fallback final judgment (keep-based) triggered --")

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