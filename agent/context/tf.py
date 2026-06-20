"""TF question solving — single loop evaluating the statement, then derive logically-opposite A/B."""

from agent.llm_reasoner import get_llm_config
from agent.context._common import run_react_loop


def solve_tf(question, doc_status, config=None):
    """
    For TF questions: run ONE loop evaluating the statement itself,
    then derive logically-opposite A (正确) and B (错误) options.
    """
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    question_text = question.get("question", "")
    if config is None:
        config = get_llm_config()

    # Run one loop evaluating whether the statement is correct
    one_question = {
        "qid": qid, "domain": domain,
        "question": f"判断以下陈述是否正确: {question_text}",
        "options": {"statement": question_text},
        "doc_ids": question.get("doc_ids", []),
    }
    opt_result = run_react_loop(one_question, "statement", question_text, doc_status, config)

    judgment = opt_result["judgment"]
    evidence = opt_result.get("evidence", "")
    reasoning = opt_result.get("reason", "")
    total_prompt = opt_result["token_usage"]["prompt_tokens"]
    total_completion = opt_result["token_usage"]["completion_tokens"]

    # Derive logically-opposite A/B
    if judgment == "TRUE":
        options_detail = {
            "A": {"judgment": "TRUE", "reason": reasoning, "evidence": evidence},
            "B": {"judgment": "FALSE", "reason": "陈述已证实为正确 (A=正确)，故错误选项 (B) 不成立", "evidence": evidence},
        }
    elif judgment == "FALSE":
        options_detail = {
            "A": {"judgment": "FALSE", "reason": reasoning, "evidence": evidence},
            "B": {"judgment": "TRUE", "reason": "陈述被证实为错误 (A=正确 不成立)，故错误选项 (B) 成立", "evidence": evidence},
        }
    else:
        options_detail = {
            "A": {"judgment": "VAGUE", "reason": reasoning, "evidence": evidence},
            "B": {"judgment": "VAGUE", "reason": "证据不足，无法判断", "evidence": "文档中未检索到明确支持或反驳的信息"},
        }

    all_logs = [f"-- Statement ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --"]
    all_logs.extend(opt_result["log_summary"])

    status = "VAGUE_ALL" if judgment == "VAGUE" else "RESOLVED"

    return {
        "qid": qid, "domain": domain, "question": question_text, "status": status,
        "answer_format": "tf", "options_detail": options_detail,
        "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion,
                        "total": total_prompt + total_completion},
        "llm_model": config["model"], "rounds": "per-option", "log_summary": all_logs,
        "options_processed": 2,
    }