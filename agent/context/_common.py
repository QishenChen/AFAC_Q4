"""
Shared context utilities and ReACT loop engine for all question-solving strategies.
"""

import json
import os
from agent.tools import execute_tool
from agent.llm_reasoner import llm_think, get_llm_config

MAX_ROUNDS = 12
BATCH_MAX_ROUNDS = 12
MAX_KEEP_CLUES = 5


def format_table_for_context(table: dict) -> str:
    """Format a table dict into a readable text block for LLM context."""
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
    """Assemble context for a single option's judgment."""
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
    """Parse a tool execution result into a structured observation."""
    if label_counter is None:
        label_counter = [1]
    if not act_result:
        return {"type": "empty", "summary": "No results returned"}
    if tool_name == "search_headings":
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
    if tool_name == "get_section" and act_result:
        gathered_sections.append(act_result)
        for t in act_result.get("tables", []):
            gathered_tables.append(t)
    elif tool_name == "search_tables":
        tr = act_result if isinstance(act_result, list) else []
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


def _sanitize_filename(name: str) -> str:
    """Replace path separators and other unsafe chars so a label can be used as a filename."""
    for ch in "/\\:?*\"<>|":
        name = name.replace(ch, "_")
    return name


def _save_search_results(qid, obs):
    """Save labeled search results into results/search_results/{qid}/{label}.json"""
    search_dir = f"results/search_results/{qid}"
    os.makedirs(search_dir, exist_ok=True)
    items = obs.get("results") or obs.get("tables") or obs.get("matches") or []
    for item in items:
        lbl = item.get("label")
        if lbl:
            safe_lbl = _sanitize_filename(lbl)
            with open(f"{search_dir}/{safe_lbl}.json", "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
    if obs.get("type") == "section" and obs.get("found"):
        lbl = f"section_{obs.get('heading','')[:30]}"
        safe_lbl = _sanitize_filename(lbl)
        with open(f"{search_dir}/{safe_lbl}.json", "w", encoding="utf-8") as f:
            json.dump({"heading": obs.get("heading",""), "content": obs.get("content_preview","")}, f, ensure_ascii=False, indent=2)


def _prune_by_keep(keep_input, gathered_tables, gathered_sections, round_log):
    """Remove items not in keep_labels from gathered context and round_log observations.
    Accepts either a flat list ["R1","R3"] or a dict {"A": ["R1","R2"], "B": ["R3"]}.
    Enforces MAX_KEEP_CLUES by truncating to the first labels deterministically.
    """
    if not keep_input:
        return
    if isinstance(keep_input, dict):
        # Dict format: {"A": ["R1","R2"], "B": ["R3"]} → flatten
        keep = set()
        for labels in keep_input.values():
            keep.update(labels)
    elif isinstance(keep_input, list):
        keep = set(keep_input)
    else:
        return

    # Aggressive compression: cap total kept clues at MAX_KEEP_CLUES
    original_count = len(keep)
    if original_count > MAX_KEEP_CLUES:
        sorted_labels = sorted(keep, key=lambda x: (len(x), x))
        dropped = sorted_labels[MAX_KEEP_CLUES:]
        keep = set(sorted_labels[:MAX_KEEP_CLUES])
        # Warn in the most recent THINK entry or append a system note
        warning = f"[COMPRESS] keep had {original_count} clues; truncated to {MAX_KEEP_CLUES} ({keep}). Dropped: {dropped}"
        for entry in reversed(round_log):
            if entry.get("phase") == "THINK":
                entry["text"] = f"{entry.get('text', '')}\n{warning}"
                break

    gathered_tables[:] = [t for t in gathered_tables if t.get("__label__") in keep]
    gathered_sections[:] = [s for s in gathered_sections if s.get("__label__") in keep]
    for entry in round_log:
        if entry.get("phase") != "OBSERVE" or not entry.get("data"):
            continue
        data = entry["data"]
        for result_group in data.get("results", []):
            for tool_name, obs in result_group.items():
                if "tables" in obs:
                    obs["tables"] = [t for t in obs["tables"] if t.get("label") in keep]
                    obs["table_count"] = len(obs.get("tables", []))
                if "results" in obs and obs.get("type") == "headings":
                    obs["results"] = [h for h in obs["results"] if h.get("label") in keep]
                    obs["count"] = len(obs.get("results", []))
                if "matches" in obs:
                    obs["matches"] = [m for m in obs["matches"] if m.get("label") in keep]
                    obs["count"] = len(obs.get("matches", []))


def _parse_multi_actions(plan, round_log, rnd):
    """Parse LLM response into list of action dicts."""
    actions = plan.get("actions", None)
    if actions is not None:
        return actions
    if plan.get("tool") and plan.get("tool") != "done":
        return [{"tool": plan["tool"], "params": plan.get("params", {})}]
    return []


# ── Core ReACT loop engine (shared by per_option, batch, and tf) ──

def run_react_loop(question, option_key, option_text, doc_status, config=None, max_rounds=MAX_ROUNDS):
    """Core ReACT loop: Think → Act → Observe. Returns judgment, evidence, tokens, log."""
    qid = question.get("qid", "")
    domain = question.get("domain", "")
    if config is None:
        config = get_llm_config()

    prompt_tokens = 0
    completion_tokens = 0
    round_log = []
    gathered_tables = []
    gathered_sections = []
    label_counter = [1]
    accumulated_judgment = {}  # {option_key: "TRUE|FALSE|VAGUE"}

    # Build initial mini_question
    parent_question = question.get("question", "")
    if question.get("answer_format") == "tf":
        mini_question = {
            "qid": f"{qid}_{option_key}", "domain": domain,
            "question": f"判断以下陈述是否正确: {parent_question}",
            "options": {option_key: option_text},
            "doc_ids": question.get("doc_ids", []),
        }
    else:
        orig_options = question.get("options", {})
        mini_options = dict(orig_options) if len(orig_options) > 1 else {option_key: option_text}
        mini_question = {
            "qid": f"{qid}_{option_key}", "domain": domain,
            "question": question.get("question", f"判断选项 {option_key} 是否正确: {option_text}"),
            "options": mini_options,
            "doc_ids": question.get("doc_ids", []),
        }

    available = {k: v for k, v in doc_status.items() if v.get("available")}
    if not available:
        return {"option": option_key, "judgment": "VAGUE", "reason": "所有文档缺失", "evidence": "",
                "token_usage": {"prompt_tokens": 0, "completion_tokens": 0, "total": 0},
                "rounds": 0, "log_summary": []}

    think0 = f"[THINK 0] Option {option_key}: 检查文档"
    round_log.append({"round": 0, "phase": "THINK", "text": think0})
    obs0 = f"[OBSERVE 0] 可用: {list(available.keys())}"
    round_log.append({"round": 0, "phase": "OBSERVE", "text": obs0})

    for rnd in range(1, max_rounds + 1):
        plan = llm_think(mini_question, doc_status, round_log, rnd, config, max_rounds=max_rounds, log_qid=qid)
        reasoning = plan.get("reasoning", "")
        if isinstance(reasoning, dict):
            reasoning_display = json.dumps(reasoning, ensure_ascii=False)
        else:
            reasoning_display = str(reasoning)
        think_text = f"[THINK {rnd}] {reasoning_display[:150]}"
        llm_usage = plan.get("llm_usage", {})
        prompt_tokens += llm_usage.get("prompt_tokens", 0)
        completion_tokens += llm_usage.get("completion_tokens", 0)
        round_log.append({"round": rnd, "phase": "THINK", "text": think_text,
                          "reasoning_dict": plan.get("reasoning") if isinstance(plan.get("reasoning"), dict) else {}})

        # Prune irrelevant clues before executing actions
        keep_input = plan.get("keep")
        if keep_input:
            _prune_by_keep(keep_input, gathered_tables, gathered_sections, round_log)

        actions = _parse_multi_actions(plan, round_log, rnd)

        # Accumulate partial judgments (may come alongside actions)
        round_judgment = plan.get("judgment")
        if round_judgment:
            if isinstance(round_judgment, str) and ":" in round_judgment:
                for part in round_judgment.split("|"):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        accumulated_judgment[k.strip()] = v.strip()
            elif isinstance(round_judgment, dict):
                accumulated_judgment.update(round_judgment)
            elif isinstance(round_judgment, str) and round_judgment in ("TRUE", "FALSE"):
                # Single-option plain judgment ("TRUE"/"FALSE") → map to remaining option key
                remaining = list(mini_question.get("options", {}).keys())
                if len(remaining) == 1:
                    accumulated_judgment[remaining[0]] = round_judgment

            # Prune resolved options + their labels from future context
            # keep_input format: {"A": ["R1","R2"], "B": ["R3"]} or list ["R1","R3"]
            resolved_labels_to_remove = set()
            for opt_key, verdict in accumulated_judgment.items():
                if verdict in ("TRUE", "FALSE") and opt_key in mini_question.get("options", {}):
                    # Remove this option from prompt
                    del mini_question["options"][opt_key]
                    # Prune resolved keys from all past THINK reasoning dicts
                    for entry in round_log:
                        if entry.get("phase") == "THINK" and isinstance(entry.get("text"), str) and "{" in entry.get("text", ""):
                            pass  # THINK text is already truncated, skip
                        if entry.get("phase") == "THINK" and isinstance(entry.get("reasoning_dict"), dict):
                            entry["reasoning_dict"].pop(opt_key, None)
                    # Collect its labels for pruning
                    if isinstance(keep_input, dict) and opt_key in keep_input:
                        resolved_labels_to_remove.update(keep_input[opt_key])
                    elif isinstance(keep_input, list):
                        resolved_labels_to_remove.update(keep_input)

            # Prune resolved labels from gathered data AND round_log observations
            if resolved_labels_to_remove:
                gathered_tables[:] = [t for t in gathered_tables if t.get("__label__") not in resolved_labels_to_remove]
                gathered_sections[:] = [s for s in gathered_sections if s.get("__label__") not in resolved_labels_to_remove]
                # Also prune from round_log so future prompts don't see resolved evidence
                for entry in round_log:
                    if entry.get("phase") != "OBSERVE" or not entry.get("data"):
                        continue
                    data = entry["data"]
                    for result_group in data.get("results", []):
                        for tool_name, obs in result_group.items():
                            if "tables" in obs:
                                obs["tables"] = [t for t in obs["tables"] if t.get("label") not in resolved_labels_to_remove]
                            if "results" in obs and obs.get("type") == "headings":
                                obs["results"] = [h for h in obs["results"] if h.get("label") not in resolved_labels_to_remove]
                            if "matches" in obs:
                                obs["matches"] = [m for m in obs["matches"] if m.get("label") not in resolved_labels_to_remove]

            # TF auto-derive: if exactly 2 options total and 1 judged, derive the opposite
            remaining_opts = set(mini_question.get("options", {}).keys())
            all_known = set(accumulated_judgment.keys()) | remaining_opts
            if len(all_known) == 2 and len(accumulated_judgment) == 1:
                judged_val = list(accumulated_judgment.values())[0]
                remaining_key = list(remaining_opts)[0]
                if judged_val == "TRUE":
                    accumulated_judgment[remaining_key] = "FALSE"
                elif judged_val == "FALSE":
                    accumulated_judgment[remaining_key] = "TRUE"
                mini_question["options"].pop(remaining_key, None)

        # ── Termination: check options, not actions ──
        # If ALL options resolved, terminate immediately — ignore any remaining actions
        if not mini_question.get("options"):
            return {
                "option": option_key, "judgment": accumulated_judgment,
                "reason": "All options resolved via incremental judgment",
                "evidence": plan.get("evidence", ""),
                "gathered_tables": gathered_tables, "gathered_sections": gathered_sections,
                "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                                "total": prompt_tokens + completion_tokens},
                "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
                "log_summary": [r["text"][:150] for r in round_log],
            }

        # LLM produced 0 actions but options remain — force another round
        if not actions:
            continue

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
            _save_search_results(qid, obs)
            all_obs.append({f"tool_{tool_name}": obs})

        merged_obs = {"type": "multi_action", "count": len(all_obs), "results": all_obs}
        obs_text = f"[OBSERVE {rnd}] {json.dumps(merged_obs, ensure_ascii=False)[:8000]}"
        round_log.append({"round": rnd, "phase": "OBSERVE", "text": obs_text, "data": merged_obs})

        if rnd == max_rounds:
            resolved = dict(accumulated_judgment) if accumulated_judgment else None
            return {
                "option": option_key,
                "judgment": resolved or "VAGUE",
                "reason": f"Loop exhausted — {len(accumulated_judgment)} options resolved" if accumulated_judgment else "Loop exhausted without judgment",
                "evidence": "",
                "gathered_tables": gathered_tables, "gathered_sections": gathered_sections,
                "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                                "total": prompt_tokens + completion_tokens},
                "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
                "log_summary": [r["text"][:150] for r in round_log],
            }

    resolved = dict(accumulated_judgment) if accumulated_judgment else None
    return {
        "option": option_key,
        "judgment": resolved or "VAGUE",
        "reason": f"Loop exhausted — {len(accumulated_judgment)} options resolved" if accumulated_judgment else "Loop exhausted without judgment",
        "evidence": "", "gathered_tables": gathered_tables, "gathered_sections": gathered_sections,
        "token_usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                        "total": prompt_tokens + completion_tokens},
        "rounds": max_rounds,
        "log_summary": [r["text"][:150] for r in round_log],
    }
