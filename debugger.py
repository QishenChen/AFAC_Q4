#!/usr/bin/env python3
"""
ReACT Loop Debugger — transparent step-by-step execution viewer.
Runs a single question with full visibility into LLM ↔ Tool interaction.
LLM enabled by default. Use --no-llm to skip API calls.
"""

import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.question_loader import load_questions, check_doc_availability
from agent.llm_reasoner import get_llm_config, llm_think, reason_on_context, build_think_prompt
from agent.tools import execute_tool, build_tools_prompt
from agent.context._common import (
    MAX_ROUNDS, BATCH_MAX_ROUNDS,
    build_single_option_context, observe_result, _gather_data,
    _prune_by_keep, _parse_multi_actions,
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
        name = st.get("friendly_name", did) if st.get("available") else st.get("reason", "?")
        print(f"    {icon} {did}: {name[:60]}")
        if st.get("available"):
            available[did] = st

    if not available:
        print("\n  All documents missing — nothing to do.")
        return

    # ── Build batch question ──
    options_text = "\n".join([f"  {k}: {v}" for k, v in sorted(options.items())])
    batch_question = {
        "qid": qid, "domain": domain,
        "question": f"{question_text}\n\nAll options to evaluate:\n{options_text}",
        "options": options,
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
            plan = llm_think(batch_question, doc_status, round_log, rnd, config, max_rounds=max_rounds)
            think_dur = time.time() - think_start
            print(f" done ({fmt_duration(think_dur)})")
            llm_usage = plan.get("llm_usage", {})
            p_tok = llm_usage.get("prompt_tokens", 0)
            c_tok = llm_usage.get("completion_tokens", 0)
            prompt_tokens += p_tok
            completion_tokens += c_tok
            print(f"    Tokens: prompt={p_tok} completion={c_tok}")
            print(f"    Reasoning: {plan.get('reasoning', '')[:200]}")
            if plan.get("llm_error"):
                print(f"    ⚠ LLM ERROR: {plan['llm_error'][:200]}")
            if plan.get("llm_raw"):
                print(f"    Raw response: {plan['llm_raw'][:300]}")

        think_text = f"[THINK {rnd}] {plan.get('reasoning', '')[:150]}"
        round_log.append({"round": rnd, "phase": "THINK", "text": think_text})

        # ── Prune ──
        keep_labels = plan.get("keep") if not no_llm else None
        if keep_labels:
            before_t = len(gathered_tables)
            before_s = len(gathered_sections)
            _prune_by_keep(keep_labels, gathered_tables, gathered_sections, round_log)
            after_t = len(gathered_tables)
            after_s = len(gathered_sections)
            if before_t != after_t or before_s != after_s:
                print(f"    Pruned: tables {before_t}→{after_t}, sections {before_s}→{after_s}")
            print(f"    Keep labels: {keep_labels}")

        # ── Actions ──
        actions = _parse_multi_actions(plan, round_log, rnd)
        if not actions:
            judgment = plan.get("judgment")
            if judgment:
                print(f"\n  LLM self-judged on round {rnd}: {judgment}")
                print(f"    Evidence: {plan.get('evidence', '')[:200]}")
                round_log.append({"round": rnd, "phase": "JUDGE", "text": f"Self-judged: {judgment}"})
                # Save judgment for Final Judgment display
                saved_judgment = {"judgment": judgment, "evidence": plan.get("evidence", "")}
                break  # exit loop, go to final judgment
            # No actions, no judgment
            saved_judgment = {"judgment": "VAGUE", "evidence": ""}
            print(f"\n  LLM returned no actions and no judgment — forcing context judgment")
            break

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
                print(f"    {tool_name} → {obs.get('count', 0)} headings ({fmt_duration(act_dur)})")
                for h in obs.get("results", [])[:3]:
                    print(f"      [{h.get('label','?')}] {h.get('heading','')[:60]}")
            elif otype == "tables":
                print(f"    {tool_name} → {obs.get('count', 0)} tables ({fmt_duration(act_dur)})")
                for t in obs.get("tables", [])[:3]:
                    print(f"      [{t.get('label','?')}] {t.get('table_id','?')} {t.get('name','')[:50]}")
            elif otype == "section":
                print(f"    {tool_name} → {'found' if obs.get('found') else 'NOT FOUND'} ({fmt_duration(act_dur)})")
                if obs.get("found"):
                    print(f"      Content: {len(obs.get('content_preview',''))} chars, {obs.get('table_count',0)} tables")
            elif otype == "section_text":
                print(f"    {tool_name} → {obs.get('count', 0)} matches ({fmt_duration(act_dur)})")
                for m in obs.get("matches", [])[:2]:
                    print(f"      [{m.get('label','?')}] L{m.get('line','?')}: {m.get('text','')[:60]}")
            elif otype == "compute":
                print(f"    {tool_name} → {obs.get('result', '?')} ({fmt_duration(act_dur)})")
            elif otype == "compute_error":
                print(f"    {tool_name} → ERROR: {obs.get('error', '?')[:100]}")
            elif otype == "empty":
                print(f"    {tool_name} → NO RESULTS ({fmt_duration(act_dur)})")
            else:
                print(f"    {tool_name} → {str(obs)[:100]} ({fmt_duration(act_dur)})")

        merged_obs = {"type": "multi_action", "count": len(all_obs), "results": all_obs}
        round_log.append({"round": rnd, "phase": "OBSERVE", "text": f"", "data": merged_obs})

        # State summary
        print(f"\n  State: {len(gathered_tables)} tables, {len(gathered_sections)} sections gathered")

        round_elapsed = time.time() - t0
        total_elapsed += round_elapsed
        print(f"  Round duration: {fmt_duration(round_elapsed)}")

        # On last round, force-judge
        if rnd == max_rounds:
            print(f"\n  ⚠ Last round ({rnd}/{max_rounds}) — forcing judgment via reason_on_context")

    # ── Final judgment ──
    print_header("Final Judgment")

    # Use LLM self-judgment directly (same logic as batch.py)
    judgment = saved_judgment.get("judgment", "VAGUE") if 'saved_judgment' in dir() else "VAGUE"
    evidence = saved_judgment.get("evidence", "") if 'saved_judgment' in dir() else ""

    if isinstance(judgment, dict):
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
        options_detail = {}
        parts = judgment.split("|")
        for part in parts:
            if ":" in part:
                k, v = part.split(":", 1)
                k, v = k.strip(), v.strip()
                if k in options:
                    options_detail[k] = {"judgment": v, "reason": "LLM self-judged", "evidence": evidence}
        for key in sorted(options.keys()):
            if key not in options_detail:
                options_detail[key] = {"judgment": "VAGUE", "reason": "Not in self-judgment", "evidence": ""}
    else:
        options_detail = {k: {"judgment": "VAGUE", "reason": "Insufficient evidence", "evidence": evidence} for k in sorted(options.keys())}

    print(f"  Using LLM self-judgment (no second LLM call)")
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
    parser.add_argument("--questions", "-q", default="public_dataset_upload/questions/group_a/financial_contracts_questions.json")
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