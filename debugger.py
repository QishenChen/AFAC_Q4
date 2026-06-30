#!/usr/bin/env python3
"""
ReACT Loop Debugger — transparent step-by-step execution viewer.
Runs a single question with full visibility into LLM ↔ Tool interaction.
LLM enabled by default. Use --no-llm to skip API calls.
"""

import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.question_loader import load_questions, check_doc_availability
from agent.llm_reasoner import get_llm_config, llm_think
from agent.tools import execute_tool
from agent.context._common import (
    MAX_ROUNDS, BATCH_MAX_ROUNDS,
    build_single_option_context, observe_result, _gather_data,
    _prune_by_keep, _parse_multi_actions,
    _round_has_useful_results, _inject_all_headings,
)


def fmt_duration(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    return f"{seconds:.1f}s"


def print_separator(char="─", width=70):
    print(char * width)


def print_header(text: str):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")


def debug_one(question, config=None, no_llm=False, mode="batch", max_rounds=None):
    """Run full ReACT loop with verbose logging."""
    qid = question.get("qid", "?")
    domain = question.get("domain", "?")
    question_text = question.get("question", "")
    options = question.get("options", {})
    answer_format = question.get("answer_format", "multi")
    doc_ids = question.get("doc_ids", [])

    if config is None:
        config = get_llm_config()

    if max_rounds is None:
        max_rounds = BATCH_MAX_ROUNDS if mode == "batch" else MAX_ROUNDS

    # ── Question summary ──
    print_header("Question")
    print(f"  qid:          {qid}")
    print(f"  domain:       {domain}")
    print(f"  format:       {answer_format}")
    print(f"  mode:         {mode}")
    print(f"  max_rounds:   {max_rounds}")
    print(f"  no_llm:       {no_llm}")
    print(f"  model:        {config['model']}")
    print(f"\n  Question: {question_text[:120]}")
    print(f"\n  Options ({len(options)}):")
    for k, v in sorted(options.items()):
        print(f"    {k}: {v[:100]}")
    print(f"\n  Doc IDs: {doc_ids}")

    # ── Doc availability ──
    doc_status = check_doc_availability(doc_ids)
    print(f"\n  Document status:")
    available = {}
    for did, st in doc_status.items():
        icon = "✓" if st.get("available") else "✗"
        name = st.get("summary", st.get("rel_path", did)) if st.get("available") else st.get("reason", "?")
        print(f"    {icon} {did}: {name[:60]}")
        if st.get("available"):
            available[did] = st

    if not available:
        print("\n  All documents missing — nothing to do.")
        return

    # ── Build batch question (copy options — pruning mutates it) ──
    original_options = dict(options)
    options_text = "\n".join([f"  {k}: {v}" for k, v in sorted(options.items())])
    batch_question = {
        "qid": qid, "domain": domain,
        "question": f"{question_text}\n\nAll options to evaluate:\n{options_text}",
        "options": dict(options),
        "doc_ids": doc_ids,
    }

    # ── ReACT loop ──
    prompt_tokens = 0
    completion_tokens = 0
    round_log = []
    gathered_tables = []
    gathered_sections = []
    label_counter = [1]
    total_elapsed = 0.0
    accumulated_judgment = {}  # {option_key: "TRUE|FALSE"}
    saved_judgment = {"judgment": {}, "evidence": ""}
    consecutive_no_progress = 0
    all_headings_injected = False
    last_judgment_count = 0
    last_gathered_count = 0

    think0_text = f"[THINK 0] 检查文档: {qid}"
    round_log.append({"round": 0, "phase": "THINK", "text": think0_text})
    obs0_text = f"[OBSERVE 0] 可用: {list(available.keys())}"
    round_log.append({"round": 0, "phase": "OBSERVE", "text": obs0_text})

    print_header("ReACT Loop")

    for rnd in range(1, max_rounds + 1):
        t0 = time.time()

        print(f"\n  {'─'*66}")
        print(f"  [ROUND {rnd}/{max_rounds}]")
        print(f"  {'─'*66}")

        # ── THINK ──
        think_start = time.time()
        if no_llm:
            # Fallback to keyword extraction
            all_text = question_text + " " + " ".join(options.values())
            import re
            terms = re.findall(r'[\u4e00-\u9fff]{2,}', all_text)
            query = " ".join(list(dict.fromkeys(terms))[:8])
            plan = {
                "tool": "search_headings",
                "params": {"query": query, "domain": domain, "max_results": 10},
                "reasoning": f"[NO-LLM] Fallback keyword search",
            }
            print(f"  THINK → (no LLM, keyword fallback)")
            print(f"    Query: {query[:100]}")
        else:
            print(f"  THINK → Calling LLM (30s timeout)...", end="", flush=True)
            plan = llm_think(batch_question, doc_status, round_log, rnd, config, max_rounds=max_rounds, log_qid=qid)
            think_dur = time.time() - think_start
            print(f" done ({fmt_duration(think_dur)})")
            llm_usage = plan.get("llm_usage", {})
            p_tok = llm_usage.get("prompt_tokens", 0)
            c_tok = llm_usage.get("completion_tokens", 0)
            prompt_tokens += p_tok
            completion_tokens += c_tok
            print(f"    Tokens: prompt={p_tok} completion={c_tok}")
            reasoning_display = plan.get("reasoning", "")
            if isinstance(reasoning_display, dict):
                print(f"    Reasoning: {json.dumps(reasoning_display, ensure_ascii=False)[:200]}")
            else:
                print(f"    Reasoning: {str(reasoning_display)[:200]}")
            if plan.get("llm_error"):
                print(f"    ⚠ LLM ERROR: {plan['llm_error'][:200]}")
            if plan.get("llm_raw"):
                print(f"    Raw response: {plan['llm_raw'][:300]}")

        reasoning_raw = plan.get("reasoning", "")
        if isinstance(reasoning_raw, dict):
            reasoning_str = json.dumps(reasoning_raw, ensure_ascii=False)
        else:
            reasoning_str = str(reasoning_raw)
        think_text = f"[THINK {rnd}] {reasoning_str[:150]}"
        round_log.append({"round": rnd, "phase": "THINK", "text": think_text,
                          "reasoning_dict": plan.get("reasoning") if isinstance(plan.get("reasoning"), dict) else {}})

        # ── Prune irrelevant clues ──
        keep_labels = plan.get("keep") if not no_llm else None
        if keep_labels:
            before_t = len(gathered_tables)
            before_s = len(gathered_sections)
            # Count total labels before pruning (helps detect cap overflow)
            if isinstance(keep_labels, dict):
                before_keep_count = sum(len(v) for v in keep_labels.values() if isinstance(v, list))
            elif isinstance(keep_labels, list):
                before_keep_count = len(keep_labels)
            else:
                before_keep_count = 0
            _prune_by_keep(keep_labels, gathered_tables, gathered_sections, round_log)
            after_t = len(gathered_tables)
            after_s = len(gathered_sections)
            if before_t != after_t or before_s != after_s:
                print(f"    Pruned: tables {before_t}→{after_t}, sections {before_s}→{after_s}")
            if before_keep_count > 5:
                print(f"    ⚠ keep labels capped: {before_keep_count} → 5")
            print(f"    Keep labels: {keep_labels}")

        # ── Accumulate partial judgments + prune resolved options ──
        round_judgment = plan.get("judgment")
        if round_judgment:
            if isinstance(round_judgment, str) and ":" in round_judgment:
                for part in round_judgment.split("|"):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        accumulated_judgment[k.strip()] = v.strip()
            elif isinstance(round_judgment, dict):
                accumulated_judgment.update(round_judgment)
            print(f"    Partial judgment accumulated: {accumulated_judgment}")

            # Prune resolved options from batch_question
            resolved_labels_to_remove = set()
            for opt_key, verdict in accumulated_judgment.items():
                if verdict in ("TRUE", "FALSE") and opt_key in batch_question.get("options", {}):
                    del batch_question["options"][opt_key]
                    # Prune resolved keys from all past THINK reasoning dicts
                    for entry in round_log:
                        if entry.get("phase") == "THINK" and isinstance(entry.get("reasoning_dict"), dict):
                            entry["reasoning_dict"].pop(opt_key, None)
                    if isinstance(keep_labels, dict) and opt_key in keep_labels:
                        resolved_labels_to_remove.update(keep_labels[opt_key])
                    elif isinstance(keep_labels, list):
                        resolved_labels_to_remove.update(keep_labels)

            # Prune resolved labels from gathered data
            if resolved_labels_to_remove:
                gathered_tables[:] = [t for t in gathered_tables if t.get("__label__") not in resolved_labels_to_remove]
                gathered_sections[:] = [s for s in gathered_sections if s.get("__label__") not in resolved_labels_to_remove]
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
            remaining_opts = set(batch_question.get("options", {}).keys())
            all_known = set(accumulated_judgment.keys()) | remaining_opts
            if len(all_known) == 2 and len(accumulated_judgment) == 1:
                judged_val = list(accumulated_judgment.values())[0]
                remaining_key = list(remaining_opts)[0]
                if judged_val == "TRUE":
                    accumulated_judgment[remaining_key] = "FALSE"
                elif judged_val == "FALSE":
                    accumulated_judgment[remaining_key] = "TRUE"
                batch_question["options"].pop(remaining_key, None)
                print(f"    Auto-derived: {remaining_key}={accumulated_judgment[remaining_key]}")

        # ── Actions ──
        actions = _parse_multi_actions(plan, round_log, rnd)

        # ── Termination: check options, not actions ──
        if not batch_question.get("options"):
            print(f"\n  ✓ All options resolved on round {rnd}")
            print(f"    Final judgment: {accumulated_judgment}")
            saved_judgment = {"judgment": accumulated_judgment, "evidence": plan.get("evidence", "")}
            round_log.append({"round": rnd, "phase": "JUDGE", "text": f"All resolved: {accumulated_judgment}"})
            break

        merged_obs = None
        if actions:
            print(f"\n  Actions ({len(actions)}):")
            for i, action in enumerate(actions):
                tool_name = action.get("tool", "?")
                params = action.get("params", {})
                print(f"    [{i+1}] {tool_name}({json.dumps(params, ensure_ascii=False)[:120]})")

            # ── ACT + OBSERVE ──
            all_obs = []
            for action in actions:
                tool_name = action.get("tool", "?")
                params = action.get("params", {})
                act_text = f"[ACT {rnd}] {tool_name}({json.dumps(params, ensure_ascii=False)[:150]})"
                round_log.append({"round": rnd, "phase": "ACT", "text": act_text})

                t_act = time.time()
                result = execute_tool(tool_name, **params)
                act_dur = time.time() - t_act
                act_result = result.get("result", {})

                obs = observe_result(tool_name, act_result, label_counter)
                _gather_data(tool_name, act_result, gathered_tables, gathered_sections, doc_status, obs_result=obs)
                all_obs.append({f"tool_{tool_name}": obs})

                # Print observation summary
                otype = obs.get("type", "?")
                if otype == "headings":
                    print(f"    {tool_name} -> {obs.get('count', 0)} headings ({fmt_duration(act_dur)})")
                    for h in obs.get("results", [])[:3]:
                        print(f"      [{h.get('label','?')}] {h.get('heading','')[:60]}")
                elif otype == "all_headings":
                    print(f"    {tool_name} -> ALL {obs.get('count', 0)} headings ({fmt_duration(act_dur)})")
                    if "results" in obs:
                        for h in obs.get('results', [])[:3]:
                            print(f"      [{h.get('label','?')}] {h.get('heading','')[:60]}")
                    elif "docs" in obs:
                        for doc_id, items in obs.get("docs", {}).items():
                            print(f"      doc {doc_id}: {len(items)} headings")
                            for h in items[:2]:
                                print(f"        {h[:80]}")
                elif otype == "tables":
                    print(f"    {tool_name} -> {obs.get('count', 0)} tables ({fmt_duration(act_dur)})")
                    for t in obs.get("tables", [])[:3]:
                        print(f"      [{t.get('label','?')}] {t.get('table_id','?')} {t.get('name','')[:50]}")
                elif otype == "section":
                    print(f"    {tool_name} -> {'found' if obs.get('found') else 'NOT FOUND'} ({fmt_duration(act_dur)})")
                    if obs.get("found"):
                        print(f"      Content: {len(obs.get('content_preview',''))} chars, {obs.get('table_count',0)} tables")
                elif otype == "section_text":
                    print(f"    {tool_name} -> {obs.get('count', 0)} matches ({fmt_duration(act_dur)})")
                    for m in obs.get("matches", [])[:2]:
                        print(f"      [{m.get('label','?')}] L{m.get('line','?')}: {m.get('text','')[:60]}")
                elif otype == "compute":
                    print(f"    {tool_name} -> {obs.get('result', '?')} ({fmt_duration(act_dur)})")
                elif otype == "compute_error":
                    print(f"    {tool_name} -> ERROR: {obs.get('error', '?')[:100]}")
                elif otype == "empty":
                    print(f"    {tool_name} -> NO RESULTS ({fmt_duration(act_dur)})")
                else:
                    print(f"    {tool_name} -> {str(obs)[:100]} ({fmt_duration(act_dur)})")

            merged_obs = {"type": "multi_action", "count": len(all_obs), "results": all_obs}
            round_log.append({"round": rnd, "phase": "OBSERVE", "text": f"", "data": merged_obs})
        else:
            remaining = list(batch_question.get("options", {}).keys())
            print(f"\n  ⚠ LLM returned no actions but {sorted(remaining)} remain — forcing continuation")

        # ── No-progress detection & fallback ──
        judgment_changed = len(accumulated_judgment) > last_judgment_count
        gathered_changed = (len(gathered_tables) + len(gathered_sections)) > last_gathered_count
        useful_results = _round_has_useful_results(merged_obs)

        if judgment_changed or gathered_changed or useful_results:
            consecutive_no_progress = 0
        else:
            consecutive_no_progress += 1

        last_judgment_count = len(accumulated_judgment)
        last_gathered_count = len(gathered_tables) + len(gathered_sections)

        if (consecutive_no_progress >= 2
                and not all_headings_injected
                and rnd < max_rounds
                and domain == "insurance"):
            print(f"\n  ⚠ No progress for 2 rounds — injecting get_all_headings fallback")
            fallback_obs = _inject_all_headings(doc_status, round_log, label_counter, domain, qid)
            if fallback_obs:
                all_headings_injected = True
                consecutive_no_progress = 0
                print(f"    Injected all headings across {len(fallback_obs.get('docs', {}))} doc(s), total {fallback_obs.get('count', 0)}")
            else:
                print(f"    No headings available to inject")

        # State summary
        print(f"\n  State: {len(gathered_tables)} tables, {len(gathered_sections)} sections gathered")

        round_elapsed = time.time() - t0
        total_elapsed += round_elapsed
        print(f"  Round duration: {fmt_duration(round_elapsed)}")

        # On last round, capture accumulated partial judgment
        if rnd == max_rounds:
            print(f"\n  ⚠ Last round ({rnd}/{max_rounds}) — using accumulated partial judgment")
            saved_judgment = {"judgment": dict(accumulated_judgment), "evidence": plan.get("evidence", "")}
            round_log.append({"round": rnd, "phase": "JUDGE", "text": f"Max rounds: {accumulated_judgment}"})
            break

    # ── Final judgment: use accumulated verdicts, unjudged → VAGUE ──
    print_header("Final Judgment")

    evidence = saved_judgment.get("evidence", "")
    judgment = saved_judgment.get("judgment", {})

    options_detail = {}
    for key in sorted(original_options.keys()):
        if isinstance(judgment, dict) and key in judgment:
            verdict = judgment[key]
            options_detail[key] = {"judgment": verdict, "reason": "LLM self-judged", "evidence": evidence}
        else:
            options_detail[key] = {"judgment": "VAGUE", "reason": "Not resolved during loop", "evidence": ""}
    print(f"  Tables: {len(gathered_tables)}, Sections: {len(gathered_sections)}")

    print(f"\n  Results:")
    for k, v in sorted(options_detail.items()):
        symbol = {"TRUE": "+", "FALSE": "-", "VAGUE": "?"}.get(v["judgment"], "?")
        print(f"    [{symbol}] {k}: {v['judgment']} — {v['reason'][:100]}")
        if v.get("evidence"):
            print(f"        Evidence: {v['evidence'][:120]}")

    judgments = [v["judgment"] for v in options_detail.values()]
    status = "VAGUE_ALL" if all(j == "VAGUE" for j in judgments) else (
        "PARTIAL" if "VAGUE" in judgments else "RESOLVED")

    # ── Summary ──
    print_header("Summary")
    print(f"  Status:        {status}")
    print(f"  Rounds run:    {len([r for r in round_log if r['phase'] == 'ACT'])}")
    print(f"  Tables gathered:  {len(gathered_tables)}")
    print(f"  Sections gathered: {len(gathered_sections)}")
    print(f"  Prompt tokens:    {prompt_tokens}")
    print(f"  Completion tokens: {completion_tokens}")
    print(f"  Total tokens:      {prompt_tokens + completion_tokens}")
    print(f"  Total time:        {fmt_duration(total_elapsed)}")
    print()

    return {
        "qid": qid, "status": status, "options_detail": options_detail,
        "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
        "rounds": len([r for r in round_log if r["phase"] == "ACT"]),
    }


def main():
    parser = argparse.ArgumentParser(description="ReACT Loop Debugger")
    parser.add_argument("--questions", "-q", default="public_dataset_upload/questions/group_a/financial_reports_questions.json")
    parser.add_argument("--qid", default=None, help="Question ID to debug")
    parser.add_argument("--mode", choices=["batch", "per-option", "tf"], default="batch")
    parser.add_argument("--max-rounds", type=int, default=None)
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM calls, use keyword fallback")
    args = parser.parse_args()

    questions = load_questions(args.questions)
    target = None
    for q in questions:
        if args.qid and q.get("qid") != args.qid:
            continue
        target = q
        break

    if not target:
        print(f"Question '{args.qid}' not found in {args.questions}")
        sys.exit(1)

    debug_one(target, no_llm=args.no_llm, mode=args.mode, max_rounds=args.max_rounds)


if __name__ == "__main__":
    main()
