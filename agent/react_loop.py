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


def _make_label(label_counter):
    """Generate next label R1, R2, R3..."""
    lbl = f"R{label_counter[0]}"
    label_counter[0] += 1
    return lbl


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


def observe_result(tool_name, act_result, label_counter=None):
    if label_counter is None:
        label_counter = [1]
    if not act_result:
        return {"type": "empty", "summary": "No results returned"}
    if tool_name in ("search_headings", "search_headings_doc"):
        hr = act_result if isinstance(act_result, list) else []
        items = []
        for h in hr[:5]:
            lbl = _make_label(label_counter)
            items.append({
                "label": lbl,
                "heading": h.get("title", ""),
                "doc": h.get("doc", ""),
                "path": " > ".join(h.get("path", [])),
            })
        return {"type": "headings", "count": len(hr), "results": items}
    if tool_name == "get_section":
        if act_result:
            from utils.text_utils import strip_html_tags
            tables_found = act_result.get("tables", [])
            tbl_items = []
            for t in tables_found[:4]:
                lbl = _make_label(label_counter)
                tbl_items.append({
                    "label": lbl, "table_id": t.get("table_id", ""),
                    "name": t.get("name", ""), "text": format_table_for_context(t),
                })
            return {"type": "section", "found": True, "heading": act_result.get("heading", "")[:100],
                    "content_preview": strip_html_tags(act_result.get("content", ""))[:2000],
                    "table_count": len(tables_found), "tables": tbl_items}
        return {"type": "section", "found": False}
    if tool_name == "search_tables":
        tr = act_result if isinstance(act_result, list) else []
        items = []
        for t in tr[:4]:
            lbl = _make_label(label_counter)
            items.append({
                "label": lbl, "table_id": t.get("table_id", ""),
                "name": t.get("name", ""), "text": format_table_for_context(t),
            })
        return {"type": "tables", "count": len(tr), "tables": items}
    if tool_name == "search_text":
        st = act_result if isinstance(act_result, list) else []
        items = []
        for m in st[:5]:
            lbl = _make_label(label_counter)
            items.append({
                "label": lbl, "line": m.get("line_num", "?"),
                "text": m.get("text", ""),
            })
        return {"type": "section_text", "count": len(st), "matches": items}
    if tool_name == "compute":
        res = act_result.get("result") if isinstance(act_result, dict) else act_result
        err = act_result.get("error") if isinstance(act_result, dict) else None
        if err:
            return {"type": "compute_error", "error": err}
        return {"type": "compute", "result": res}
    return {"type": "raw", "preview": str(act_result)[:1000]}


def _gather_data(tool_name, act_result, gathered_tables, gathered_sections, doc_status, obs_result=None):
    """Collect data from tool results into gathered_tables/sections. Attach labels for pruning."""
    label_map = {}
    if obs_result:
        # Build label→item mapping from the observation for later pruning
        for key, lst in [("tables", gathered_tables), ("headings", None)]:
            pass  # handled per-tool below

    if tool_name == "get_section" and act_result:
        gathered_sections.append(act_result)
        for t in act_result.get("tables", []):
            gathered_tables.append(t)
    elif tool_name == "search_tables":
        tr = act_result if isinstance(act_result, list) else []
        # Attach labels to gathered tables so _prune_by_keep can find them
        obs_data = obs_result or {}
        tbl_entries = obs_data.get("tables", [])
        for i, t in enumerate(tr):
            if i < len(tbl_entries):
                t["__label__"] = tbl_entries[i].get("label", "")
        gathered_tables.extend(tr)
    elif tool_name == "search_text" and act_result:
        available = [k for k, v in doc_status.items() if v.get("available")]
        obs_data = obs_result or {}
        matches = obs_data.get("matches", [])
        for i, match in enumerate(act_result if isinstance(act_result, list) else []):
            lbl = matches[i].get("label", "") if i < len(matches) else ""
            gathered_sections.append({
                "heading": f"文本匹配 L{match.get('line_num', '?')}",
                "doc": doc_status.get(available[0], {}).get("rel_path", "") if available else "",
                "content": match.get("text", ""),
                "__label__": lbl,
            })


def _prune_by_keep(keep_labels, gathered_tables, gathered_sections, round_log):
    """Remove items not in keep_labels from gathered context and round_log observations."""
    if not keep_labels:
        return
    keep = set(keep_labels)
    # Prune gathered_tables
    gathered_tables[:] = [t for t in gathered_tables if t.get("__label__") in keep]
    # Prune gathered_sections
    gathered_sections[:] = [s for s in gathered_sections if s.get("__label__") in keep]
    # Prune round_log OBSERVE entries
    for entry in round_log:
        if entry.get("phase") != "OBSERVE" or not entry.get("data"):
            continue
        data = entry["data"]
        for result_group in data.get("results", []):
            for tool_name, obs in result_group.items():
                # Filter tables
                if "tables" in obs:
                    obs["tables"] = [t for t in obs["tables"] if t.get("label") in keep]
                    obs["table_count"] = len(obs.get("tables", []))
                # Filter headings
                if "results" in obs and obs.get("type") == "headings":
                    obs["results"] = [h for h in obs["results"] if h.get("label") in keep]
                    obs["count"] = len(obs.get("results", []))
                # Filter section_text matches
                if "matches" in obs:
                    obs["matches"] = [m for m in obs["matches"] if m.get("label") in keep]
                    obs["count"] = len(obs.get("matches", []))


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
    label_counter = [1]  # mutable counter for global R1, R2, ...

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

        # Prune irrelevant clues before executing actions
        keep_labels = plan.get("keep")
        if keep_labels:
            _prune_by_keep(keep_labels, gathered_tables, gathered_sections, round_log)

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

            obs = observe_result(tool_name, act_result, label_counter)
            _gather_data(tool_name, act_result, gathered_tables, gathered_sections, doc_status, obs_result=obs)
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


def _solve_tf_question(question, doc_status, config):
    """
    For TF questions: run ONE loop evaluating the statement itself,
    then derive logically-opposite A (正确) and B (错误) options.
    """
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    question_text = question.get("question", "")

    # Run one loop evaluating whether the statement is correct
    one_question = {
        "qid": qid, "domain": domain,
        "question": f"判断以下陈述是否正确: {question_text}",
        "options": {"statement": question_text},
        "doc_ids": question.get("doc_ids", []),
    }
    opt_result = react_solve_one_option(one_question, "statement", question_text, doc_status, config)

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
        "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion, "total": total_prompt + total_completion},
        "llm_model": config["model"], "rounds": "per-option", "log_summary": all_logs, "options_processed": 2,
    }


def _solve_batch_options(question, doc_status, config):
    """
    Batch evaluation: one shared retrieval loop gathering context for ALL options,
    then simultaneous judgment via reason_on_context.
    """
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    question_text = question.get("question", "")
    options = question.get("options", {})

    # Build a question that presents ALL options at once
    options_text = "\n".join([f"  {k}: {v}" for k, v in sorted(options.items())])
    batch_question = {
        "qid": qid, "domain": domain,
        "question": f"{question_text}\n\nAll options to evaluate:\n{options_text}",
        "options": {"all": f"Evaluate all {len(options)} options simultaneously"},
        "doc_ids": question.get("doc_ids", []),
    }
    opt_result = react_solve_one_option(batch_question, "all", "Evaluate all options", doc_status, config)

    total_prompt = opt_result["token_usage"]["prompt_tokens"]
    total_completion = opt_result["token_usage"]["completion_tokens"]
    gathered_tables = []  # Not accessible from react_solve_one_option directly
    gathered_sections = []

    # Now do the simultaneous judgment using reason_on_context
    # We need to rebuild the context from the gathered data
    context = build_single_option_context(question, "ALL", "All options", gathered_tables, gathered_sections, doc_status)
    llm_reasoning = reason_on_context(context, question, config)
    total_prompt += llm_reasoning.get("llm_prompt_tokens", 0)
    total_completion += llm_reasoning.get("llm_completion_tokens", 0)
    options_detail = llm_reasoning.get("options_detail", {})

    # Fill in any missing options with VAGUE
    for key in sorted(options.keys()):
        if key not in options_detail:
            options_detail[key] = {"judgment": "VAGUE", "reason": "No judgment returned", "evidence": ""}

    all_logs = [f"-- Batch ({opt_result['rounds']} rounds, {opt_result['token_usage']['total']} tokens) --"]
    all_logs.extend(opt_result["log_summary"])
    all_logs.append(f"-- Batch judgment ({total_prompt} prompt, {total_completion} completion) --")

    judgments = [v["judgment"] for v in options_detail.values()]
    status = "VAGUE_ALL" if all(j == "VAGUE" for j in judgments) else ("PARTIAL" if "VAGUE" in judgments else "RESOLVED")

    return {"qid": qid, "domain": domain, "question": question_text, "status": status,
            "answer_format": question.get("answer_format", ""), "options_detail": options_detail,
            "token_usage": {"prompt_tokens": total_prompt, "completion_tokens": total_completion, "total": total_prompt + total_completion},
            "llm_model": config["model"], "rounds": "batch", "log_summary": all_logs, "options_processed": len(options)}


def react_solve_one(question, config=None, batch=False):
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

    # TF questions: single loop evaluating the statement → derive opposite A/B
    if question.get("answer_format") == "tf":
        return _solve_tf_question(question, doc_status, config)

    # Batch mode: shared retrieval + simultaneous judgment
    if batch:
        return _solve_batch_options(question, doc_status, config)

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
