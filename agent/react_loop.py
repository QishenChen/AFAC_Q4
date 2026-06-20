"""
ReACT Loop — thin dispatcher.
Routes questions to the appropriate context strategy based on answer_format and mode.
"""
# fmt: off

from agent.question_loader import check_doc_availability
from agent.llm_reasoner import get_llm_config
from agent.context.tf import solve_tf
from agent.context.batch import solve_batch
from agent.context._common import run_react_loop as react_solve_one_option


def react_solve_one(question, config=None, batch=True):
    """
    Dispatch a question to the correct solving strategy.
    
    - answer_format="tf" → solve_tf (single loop, derive A/B)
    - batch=True → solve_batch (shared retrieval, simultaneous judgment)
    - batch=False → per_option loop (one loop per option)
    """
    qid = question.get("qid", "")
    question_text = question.get("question", "")
    options = question.get("options", {})
    domain = question.get("domain", "")
    doc_ids = question.get("doc_ids", [])
    if config is None:
        config = get_llm_config()

    doc_status = check_doc_availability(doc_ids)
    available = {k: v for k, v in doc_status.items() if v.get("available")}
    if not available:
        return {
            "qid": qid, "domain": domain, "question": question_text, "status": "MISSING_DOCS",
            "options_detail": {k: {"judgment": "VAGUE", "reason": "所有文档缺失"} for k in options},
            "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total": 0},
            "rounds": 0, "log_summary": [],
        }

    # TF questions: single loop evaluating the statement → derive opposite A/B
    if question.get("answer_format") == "tf":
        return solve_tf(question, doc_status, config)

    # Batch mode: shared retrieval + simultaneous judgment
    if batch:
        return solve_batch(question, doc_status, config)

    # Per-option mode: each option gets its own loop
    options_detail = {}
    total_prompt = 0
    total_completion = 0
    all_logs = []
    for opt_key, opt_text in options.items():
        opt_result = react_solve_one_option(question, opt_key, opt_text, doc_status, config)
        options_detail[opt_key] = {
            "judgment": opt_result["judgment"],
            "reason": opt_result["reason"],
            "evidence": opt_result.get("evidence", ""),
        }
        total_prompt += opt_result["token_usage"]["prompt_tokens"]
        total_completion += opt_result["token_usage"]["completion_tokens"]
        all_logs.append(f"-- {opt_key} ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --")
        all_logs.extend(opt_result["log_summary"])

    judgments = [v["judgment"] for v in options_detail.values()]
    status = "VAGUE_ALL" if all(j == "VAGUE" for j in judgments) else (
        "PARTIAL" if "VAGUE" in judgments else "RESOLVED")

    return {
        "qid": qid, "domain": domain, "question": question_text, "status": status,
        "answer_format": question.get("answer_format", ""), "options_detail": options_detail,
        "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion,
                        "total": total_prompt + total_completion},
        "llm_model": config["model"], "rounds": "per-option", "log_summary": all_logs,
        "options_processed": len(options),
    }