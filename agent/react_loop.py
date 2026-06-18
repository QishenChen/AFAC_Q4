"""
ReACT Loop: LLM-driven Think → Act → Observe → Think ...
Each OPTION gets its own independent ReACT loop (up to 6 rounds).
LLM can request MULTIPLE tools per round — they execute in parallel.
"""

import json
import re

from agent.tools import execute_tool
from agent.question_loader import check_doc_availability, estimate_tokens
from agent.llm_reasoner import llm_think, reason_on_context, get_llm_config

MAX_ROUNDS = 6


def format_table_for_context(table: dict) -> str:
    lines = []
    lines.append(f"【表格 ID: {table.get('table_id', '?')}】")
    lines.append(f"文档: {table.get('doc_path', '?')}")
    lines.append(f"章节: {table.get('heading_title', '?')}")
    lines.append(f"名称: {table.get('name', '?')}")
    if table.get("unit"):
        lines.append(f"单位: {table['unit']}")
    headers = table.get("headers", [])
    if headers:
        lines.append(f"列: {' | '.join(headers)}")
    for row in table.get("data", []):
        if row:
            lines.append(f"  {' | '.join(str(c) for c in row)}")
    return "\n".join(lines)


def build_single_option_context(question, option_key, option_text, gathered_tables, gathered_sections, doc_status):
    parts = []
    parts.append(f"问题: {question.get('question', '')}")
    parts.append(f"待判断选项: {option_key}: {option_text}")
    parts.append("")
    parts.append("--- 文档状态 ---")
    for doc_id, status in doc_status.items():
        parts.append(f"  {doc_id}: {'✓' if status.get('available') else '✗'} {status.get('friendly_name', '')}")
    parts.append("")
    parts.append(f"--- 检索到的表格 (共 {len(gathered_tables)} 个) ---")
    for t in gathered_tables:
        parts.append(format_table_for_context(t))
        parts.append("")
    parts.append(f"--- 检索到的章节内容 (共 {len(gathered_sections)} 个) ---")
    for s in gathered_sections:
        parts.append(f"【章节】{s.get('heading', '?')}")
        content = s.get("content", "")
        if len(content) > 3000:
            content = content[:3000] + "\n...(truncated)"
        parts.append(content)
        parts.append("")
    return "\n".join(parts)


def observe_result(tool_name, act_result):
    if not act_result:
        return {"type": "empty", "summary": "No results returned"}
    if tool_name in ("search_headings", "search_headings_doc"):
        hr = act_result if isinstance(act_result, list) else []
        return {"type": "headings", "count": len(hr), "results": [f"{h.get('doc','')} > {h.get('title','')}" for h in hr[:5]]}
    if tool_name == "get_section":
        if act_result:
            from utils.text_utils import strip_html_tags
            tables_found = act_result.get("tables", [])
            return {"type": "section", "found": True, "heading": act_result.get("heading", "")[:100],
                    "content_preview": strip_html_tags(act_result.get("content", ""))[:2000],
                    "table_count": len(tables_found),
                    "tables": [format_table_for_context(t) for t in tables_found[:4]]}
        return {"type": "section", "found": False}
    if tool_name == "search_tables":
        tr = act_result if isinstance(act_result, list) else []
        return {"type": "tables", "count": len(tr), "tables": [format_table_for_context(t) for t in tr[:4]]}
    if tool_name == "search_section_text":
        st = act_result if isinstance(act_result, list) else []
        return {"type": "section_text", "count": len(st), "matches": [f"L{m.get('line_num','?')}: {m.get('text','')}" for m in st[:5]]}
    if tool_name == "compute":
        res = act_result.get("result") if isinstance(act_result, dict) else act_result
        err = act_result.get("error") if isinstance(act_result, dict) else None
        if err:
            return {"type": "compute_error", "error": err}
        return {"type": "compute", "result": res}
    return {"type": "raw", "preview": str(act_result)[:1000]}


def _gather_data(tool_name, act_result, gathered_tables, gathered_sections, doc_status):
    """Collect data from tool results into gathered_tables/sections."""
    if tool_name == "get_section" and act_result:
        gathered_sections.append(act_result)
        for t in act_result.get("tables", []):
            gathered_tables.append(t)
    elif tool_name == "search_tables":
        tr = act_result if isinstance(act_result, list) else []
        gathered_tables.extend(tr)
    elif tool_name == "search_section_text" and act_result:
        available = [k for k, v in doc_status.items() if v.get("available")]
        for match in (act_result if isinstance(act_result, list) else []):
            gathered_sections.append({
                "heading": f"文本匹配 L{match.get('line_num', '?')}",
                "doc": doc_status.get(available[0], {}).get("rel_path", "") if available else "",
                "content": match.get("text", ""),
            })


def _parse_multi_actions(plan, round_log, rnd):
    """Parse LLM response into list of action dicts. Supports old single-tool format and new multi-action format."""
    actions = plan.get("actions", None)
    if actions is not None:
        return actions  # new format: {"actions": [...], "reasoning": "..."}
    # Legacy format: {"tool": "...", "params": {...}, "reasoning": "..."}
    if plan.get("tool") and plan.get("tool") != "done":
        return [{"tool": plan["tool"], "params": plan.get("params", {})}]
    return []  # done or empty


def react_solve_one_option(question, option_key, option_text, doc_status, config=None):
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    if config is None:
        config = get_llm_config()

    prompt_tokens = 0
    completion_tokens = 0
    round_log = []
    gathered_tables = []
    gathered_sections = []

    # For T/F questions, include the parent question statement so LLM knows what to evaluate
    parent_question = question.get("question", "")
    if question.get("answer_format") == "tf":
        mini_question = {
            "qid": f"{qid}_{option_key}", "domain": domain,
            "question": f"判断以下陈述是否正确: {parent_question}",
            "options": {option_key: option_text},
            "doc_ids": question.get("doc_ids", []),
        }
    else:
        mini_question = {
            "qid": f"{qid}_{option_key}", "domain": domain,
            "question": f"判断选项 {option_key} 是否正确: {option_text}",
            "options": {option_key: option_text},
            "doc_ids": question.get("doc_ids", []),
        }

    available = {k: v for k, v in doc_status.items() if v.get("available")}
    if not available:
        return {"option": option_key, "judgment": "VAGUE", "reason": "所有文档缺失", "evidence": "",
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total": 0}, "rounds": 0, "log_summary": []}

    think0 = f"[THINK 0] Option {option_key}: 检查文档"
    round_log.append({"round": 0, "phase": "THINK", "text": think0})
    obs0 = f"[OBSERVE 0] 可用: {list(available.keys())}"
    round_log.append({"round": 0, "phase": "OBSERVE", "text": obs0})

    for rnd in range(1, MAX_ROUNDS + 1):
        plan = llm_think(mini_question, doc_status, round_log, rnd, config)
        think_text = f"[THINK {rnd}] {plan.get('reasoning', '')[:150]}"
        llm_usage = plan.get("llm_usage", {})
        prompt_tokens += llm_usage.get("prompt_tokens", 0)
        completion_tokens += llm_usage.get("completion_tokens", 0)
        round_log.append({"round": rnd, "phase": "THINK", "text": think_text})

        actions = _parse_multi_actions(plan, round_log, rnd)
        if not actions:
            # LLM signaled done — check if it included a judgment
            judgment = plan.get("judgment")
            evidence = plan.get("evidence", "")
            if judgment:
                return {
                    "option": option_key,
                    "judgment": judgment,
                    "reason": plan.get("reasoning", ""),
                    "evidence": evidence,
                    "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total": prompt_tokens + completion_tokens},
                    "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
                    "log_summary": [r["text"][:150] for r in round_log],
                }
            # No judgment but LLM thinks done — force reason_on_context now
            context = build_single_option_context(question, option_key, option_text, gathered_tables, gathered_sections, doc_status)
            llm_reasoning = reason_on_context(context, mini_question, config)
            prompt_tokens += llm_reasoning.get("llm_prompt_tokens", 0)
            completion_tokens += llm_reasoning.get("llm_completion_tokens", 0)
            opt_detail = llm_reasoning.get("options_detail", {}).get(option_key, {})
            return {
                "option": option_key,
                "judgment": opt_detail.get("judgment", "VAGUE"),
                "reason": opt_detail.get("reason", "No judgment from LLM — forced via context"),
                "evidence": opt_detail.get("evidence", ""),
                "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total": prompt_tokens + completion_tokens},
                "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
                "log_summary": [r["text"][:150] for r in round_log],
            }

        all_obs = []
        for action in actions:
            tool_name = action.get("tool", "search_headings")
            params = action.get("params", {})
            act_text = f"[ACT {rnd}] {tool_name}({json.dumps(params, ensure_ascii=False)[:150]})"
            round_log.append({"round": rnd, "phase": "ACT", "text": act_text})

            result = execute_tool(tool_name, **params)
            act_result = result.get("result", {})

            _gather_data(tool_name, act_result, gathered_tables, gathered_sections, doc_status)
            obs = observe_result(tool_name, act_result)
            all_obs.append({f"tool_{tool_name}": obs})

        merged_obs = {"type": "multi_action", "count": len(all_obs), "results": all_obs}
        obs_text = f"[OBSERVE {rnd}] {json.dumps(merged_obs, ensure_ascii=False)[:8000]}"
        round_log.append({"round": rnd, "phase": "OBSERVE", "text": obs_text, "data": merged_obs})

        # On last round, force-judge via reason_on_context if LLM didn't self-judge
        if rnd == MAX_ROUNDS:
            context = build_single_option_context(question, option_key, option_text, gathered_tables, gathered_sections, doc_status)
            llm_reasoning = reason_on_context(context, mini_question, config)
            prompt_tokens += llm_reasoning.get("llm_prompt_tokens", 0)
            completion_tokens += llm_reasoning.get("llm_completion_tokens", 0)
            opt_detail = llm_reasoning.get("options_detail", {}).get(option_key, {})
            return {
                "option": option_key,
                "judgment": opt_detail.get("judgment", "VAGUE"),
                "reason": opt_detail.get("reason", "Unable to determine"),
                "evidence": opt_detail.get("evidence", ""),
                "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total": prompt_tokens + completion_tokens},
                "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
                "log_summary": [r["text"][:150] for r in round_log],
            }

    # Fallback: loop exhausted without judgment or done signal
    return {
        "option": option_key,
        "judgment": "VAGUE",
        "reason": "Loop exhausted without judgment",
        "evidence": "",
        "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total": prompt_tokens + completion_tokens},
        "rounds": MAX_ROUNDS,
        "log_summary": [r["text"][:150] for r in round_log],
    }


def react_solve_one(question, config=None):
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
        return {"qid": qid, "domain": domain, "question": question_text, "status": "MISSING_DOCS",
                "options_detail": {k: {"judgment": "VAGUE", "reason": "所有文档缺失"} for k in options},
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total": 0}, "rounds": 0, "log_summary": []}

    options_detail = {}
    total_prompt = 0
    total_completion = 0
    all_logs = []
    for opt_key, opt_text in options.items():
        opt_result = react_solve_one_option(question, opt_key, opt_text, doc_status, config)
        options_detail[opt_key] = {"judgment": opt_result["judgment"], "reason": opt_result["reason"], "evidence": opt_result.get("evidence", "")}
        total_prompt += opt_result["token_usage"]["prompt_tokens"]
        total_completion += opt_result["token_usage"]["completion_tokens"]
        all_logs.append(f"-- {opt_key} ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --")
        all_logs.extend(opt_result["log_summary"])

    judgments = [v["judgment"] for v in options_detail.values()]
    status = "VAGUE_ALL" if all(j == "VAGUE" for j in judgments) else ("PARTIAL" if "VAGUE" in judgments else "RESOLVED")

    return {"qid": qid, "domain": domain, "question": question_text, "status": status,
            "answer_format": question.get("answer_format", ""), "options_detail": options_detail,
            "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion, "total": total_prompt + total_completion},
            "llm_model": config["model"], "rounds": "per-option", "log_summary": all_logs, "options_processed": len(options)}