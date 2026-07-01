#!/usr/bin/env python3
"""End-to-end pipeline for collecting and curating financial synonyms.

Subcommands:
  seed      — generate config/financial_synonyms.json from canonical terms via LLM
  collect   — run agent.py on question files to populate keyword logs
  analyze   — compare searched terms to the reference synonym graph
  enrich    — use LLM to classify new terms and generate synonyms
  apply     — merge reference groups into config/financial_terms.json
  run-all   — execute seed → collect → analyze → enrich → apply
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.llm_reasoner import call_llm, get_llm_config
from scripts.analyze_search_keywords import (
    analyze as run_analyze,
    choose_representative,
    load_target_groups,
)


FINANCIAL_SYNONYMS_PATH = "config/financial_synonyms.json"
FINANCIAL_TERMS_PATH = "config/financial_terms.json"
KEYWORDS_DIR = "results/keywords"
ANALYSIS_DIR = os.path.join(KEYWORDS_DIR, "analysis")
NEW_TERMS_DIR = os.path.join(KEYWORDS_DIR, "new_terms")


def _now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


# ── seed ────────────────────────────────────────────────────────────────

def _load_canonical_terms():
    """Import the canonical term list from build_synonyms.py."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_synonyms", "build_synonyms.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CANONICAL_TERMS


def _parse_synonym_response(content: str, expected_terms: list[str]) -> dict[str, list[str]]:
    """Extract {term: [synonyms]} from LLM JSON response."""
    # Try direct JSON
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return {k: [s.strip() for s in (v.split("|") if isinstance(v, str) else v) if s.strip()]
                    for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass
    # Try code block
    import re
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
    if m:
        try:
            parsed = json.loads(m.group(1))
            if isinstance(parsed, dict):
                return {k: [s.strip() for s in (v.split("|") if isinstance(v, str) else v) if s.strip()]
                        for k, v in parsed.items()}
        except json.JSONDecodeError:
            pass
    return {}


def cmd_seed(args: argparse.Namespace):
    """Generate config/financial_synonyms.json from canonical terms."""
    canonical_terms = _load_canonical_terms()
    print(f"Seeding synonyms for {len(canonical_terms)} canonical terms...")

    config = get_llm_config()
    batch_size = args.batch_size
    all_groups = []

    for i in range(0, len(canonical_terms), batch_size):
        batch = canonical_terms[i : i + batch_size]
        terms_str = "\n".join(f"{j+1}. {t}" for j, t in enumerate(batch))
        system = (
            "你是一位中文金融文档专家。请为下列每个术语列出其在中文财务/保险/监管/债券/年报文档中常见的同义词或近义词（用 | 分隔）。"
            "如果某个术语没有常见同义词，就只输出该术语本身。"
            "输出格式严格为 JSON：{\"术语1\": \"同义1|同义2\", \"术语2\": \"同义1\"}。不要输出任何 JSON 以外的文字。"
        )
        print(f"  Batch {i // batch_size + 1}/{(len(canonical_terms) + batch_size - 1) // batch_size} ...", end=" ", flush=True)
        result = call_llm(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": terms_str}],
            config=config,
        )
        if result.get("error"):
            print(f"LLM error: {result['error']}")
            for t in batch:
                all_groups.append([t])
            continue
        parsed = _parse_synonym_response(result.get("content", ""), batch)
        for t in batch:
            syns = parsed.get(t, [t])
            group = [t] + [s for s in syns if s != t]
            all_groups.append(group)
        print(f"{len(parsed)} parsed")
        time.sleep(0.5)

    # Merge overlapping groups
    term_to_gid = {}
    gid = 1
    for group in all_groups:
        if not group:
            continue
        group_set = set(group)
        existing_ids = {term_to_gid[t] for t in group_set if t in term_to_gid}
        if existing_ids:
            target = min(existing_ids)
            for t in group_set:
                term_to_gid[t] = target
            for eid in existing_ids:
                if eid != target:
                    for k, v in list(term_to_gid.items()):
                        if v == eid:
                            term_to_gid[k] = target
        else:
            for t in group_set:
                term_to_gid[t] = gid
            gid += 1

    # Ensure all canonical terms are present
    for t in canonical_terms:
        if t not in term_to_gid:
            term_to_gid[t] = gid
            gid += 1

    os.makedirs(os.path.dirname(FINANCIAL_SYNONYMS_PATH) or ".", exist_ok=True)
    with open(FINANCIAL_SYNONYMS_PATH, "w", encoding="utf-8") as f:
        json.dump(term_to_gid, f, ensure_ascii=False, indent=2)

    total_groups = len(set(term_to_gid.values()))
    print(f"Saved {len(term_to_gid)} terms across {total_groups} groups to {FINANCIAL_SYNONYMS_PATH}")


# ── collect ─────────────────────────────────────────────────────────────

def cmd_collect(args: argparse.Namespace):
    """Run agent.py on question files to record search keywords."""
    if not args.questions:
        print("No --questions provided; skipping collect step.")
        return
    cmd = [sys.executable, "agent.py", "--questions", args.questions, "--output", f"results/answers.pipeline.{_now()}.json"]
    if args.qid:
        cmd += ["--qid", args.qid]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=False)


# ── analyze ─────────────────────────────────────────────────────────────

def cmd_analyze(args: argparse.Namespace):
    """Run the embedding-based analyzer."""
    ns = SimpleNamespace(
        keywords_dir=KEYWORDS_DIR,
        target=FINANCIAL_SYNONYMS_PATH,
        config=FINANCIAL_TERMS_PATH,
        model=args.embed_model,
        threshold=args.threshold,
        margin=args.margin,
        qid=args.qid,
        apply=False,
    )
    run_analyze(ns)


# ── enrich ──────────────────────────────────────────────────────────────

def _enrich_one_term(term: str, info: dict, canonical_to_group: dict, config: dict) -> dict:
    """Ask LLM to classify a new term and suggest synonyms."""
    top_groups = info.get("top_similar_groups", [])[:5]
    groups_text = "\n".join(
        f"- {g['canonical']} ({', '.join(sorted(canonical_to_group.get(g['canonical'], set()))[:8])})"
        for g in top_groups
    )
    prompt = f"""新搜索词："{term}"
出现次数：{info.get('count', 0)}
示例查询：{', '.join(info.get('example_queries', []))}

现有最相似的同义词组：
{groups_text}

请判断该新搜索词应：
1. 合并到某个现有组（如果是同义词/简称/变体），或
2. 创建一个新同义词组（如果是新概念），并列出 2-5 个同义词。

严格输出 JSON：
{{"action": "merge", "target_canonical": "..."}}
或
{{"action": "new", "synonyms": ["...", "..."]}}
不要输出 JSON 以外的文字。"""

    result = call_llm(
        messages=[{"role": "user", "content": prompt}],
        config=config,
    )
    if result.get("error"):
        return {"action": "unknown", "error": result["error"]}
    try:
        parsed = json.loads(result.get("content", ""))
    except json.JSONDecodeError:
        import re
        m = re.search(r"\{[\s\S]*\}", result.get("content", ""))
        try:
            parsed = json.loads(m.group()) if m else {}
        except Exception:
            parsed = {}
    return parsed


def cmd_enrich(args: argparse.Namespace):
    """Use LLM to classify new terms and update financial_synonyms.json."""
    if not os.path.isfile(FINANCIAL_SYNONYMS_PATH):
        print(f"{FINANCIAL_SYNONYMS_PATH} not found. Run 'seed' first.")
        return
    if not os.path.isdir(NEW_TERMS_DIR):
        print(f"{NEW_TERMS_DIR} not found. Run 'analyze' first.")
        return

    with open(FINANCIAL_SYNONYMS_PATH, "r", encoding="utf-8") as f:
        term_to_gid = json.load(f)
    canonical_to_group, _ = load_target_groups(FINANCIAL_SYNONYMS_PATH)
    next_gid = max(term_to_gid.values(), default=0) + 1

    config = get_llm_config()
    report = {"merged": [], "new_groups": [], "failed": []}

    dirs = sorted(d for d in os.listdir(NEW_TERMS_DIR) if os.path.isdir(os.path.join(NEW_TERMS_DIR, d)))
    for dname in dirs:
        info_path = os.path.join(NEW_TERMS_DIR, dname, "info.json")
        if not os.path.isfile(info_path):
            continue
        with open(info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        term = info.get("term", dname)
        print(f"Enriching: {term} ...", end=" ", flush=True)
        decision = _enrich_one_term(term, info, canonical_to_group, config)
        info["llm_decision"] = decision
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

        action = decision.get("action")
        if action == "merge":
            target = decision.get("target_canonical", "")
            if target in term_to_gid:
                gid = term_to_gid[target]
                term_to_gid[term] = gid
                # Make the newly merged term visible to subsequent enrich calls
                canonical_to_group.setdefault(target, set()).add(term)
                report["merged"].append({"term": term, "target": target, "group": sorted(canonical_to_group.get(target, {target}))})
                print(f"merged → {target}")
            else:
                report["failed"].append({"term": term, "reason": f"target {target} not found"})
                print("failed (target not found)")
        elif action == "new":
            syns = [s.strip() for s in decision.get("synonyms", []) if s.strip() and s.strip() != term]
            group = {term} | set(syns)
            for t in group:
                term_to_gid[t] = next_gid
            canonical_to_group[term] = group
            report["new_groups"].append({"canonical": term, "group_id": next_gid, "terms": sorted(group)})
            next_gid += 1
            print(f"new group ({len(group)} terms)")
        else:
            report["failed"].append({"term": term, "reason": f"invalid action {action}"})
            print("failed (invalid action)")
        time.sleep(0.3)

    with open(FINANCIAL_SYNONYMS_PATH, "w", encoding="utf-8") as f:
        json.dump(term_to_gid, f, ensure_ascii=False, indent=2)

    report_path = os.path.join(ANALYSIS_DIR, "enrichment_report.json")
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nEnrichment done: {len(report['merged'])} merged, {len(report['new_groups'])} new groups, {len(report['failed'])} failed")
    print(f"Report saved to {report_path}")

    # Adaptive post-merge: newly created groups that are substrings/superstrings of existing groups
    # should be merged (e.g. 中金 / 中金公司).
    post_merged = _post_merge_substring_new_groups(report.get("new_groups", []))
    if post_merged:
        print(f"Post-merge: combined {post_merged} substring-related groups")


def _post_merge_substring_new_groups(new_groups: list[dict]) -> int:
    """Merge newly created groups with existing groups when one name is a substring of the other."""
    if not new_groups:
        return 0
    new_canonicals = {g["canonical"] for g in new_groups}
    if not new_canonicals:
        return 0

    with open(FINANCIAL_SYNONYMS_PATH, "r", encoding="utf-8") as f:
        term_to_gid = json.load(f)
    canonical_to_group, _ = load_target_groups(FINANCIAL_SYNONYMS_PATH)

    merged = 0
    for new_c in sorted(new_canonicals, key=len):
        if new_c not in canonical_to_group:
            continue
        best_target = None
        for other_c in list(canonical_to_group.keys()):
            if other_c == new_c:
                continue
            if new_c in other_c or other_c in new_c:
                # Prefer existing (non-new) group as parent; otherwise longer name
                if other_c not in new_canonicals:
                    best_target = other_c
                    break
                if best_target is None or len(other_c) > len(best_target):
                    best_target = other_c
        if not best_target:
            continue

        parent, child = (best_target, new_c) if len(best_target) >= len(new_c) else (new_c, best_target)
        parent_gid = term_to_gid[parent]
        combined = canonical_to_group[parent] | canonical_to_group[child]
        canonical_to_group[parent] = combined
        if child in canonical_to_group:
            del canonical_to_group[child]
        for t in combined:
            term_to_gid[t] = parent_gid
        merged += 1
        print(f"  post-merge: {child} → {parent}")

    with open(FINANCIAL_SYNONYMS_PATH, "w", encoding="utf-8") as f:
        json.dump(term_to_gid, f, ensure_ascii=False, indent=2)
    return merged


# ── apply ───────────────────────────────────────────────────────────────

def cmd_apply(args: argparse.Namespace):
    """Merge reference groups into config/financial_terms.json."""
    if not os.path.isfile(FINANCIAL_SYNONYMS_PATH):
        print(f"{FINANCIAL_SYNONYMS_PATH} not found. Run 'seed'/'enrich' first.")
        return

    with open(FINANCIAL_TERMS_PATH, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    # Build term -> canonical map for existing runtime config
    config_term_to_canonical = {}
    for canonical, syns in config_data.get("synonyms", {}).items():
        config_term_to_canonical[canonical] = canonical
        for s in syns:
            config_term_to_canonical[s] = canonical

    canonical_to_group, _ = load_target_groups(FINANCIAL_SYNONYMS_PATH)

    added_canonicals = []
    updated_canonicals = []
    for canonical, group in canonical_to_group.items():
        existing_canonical = None
        for t in group:
            if t in config_term_to_canonical:
                existing_canonical = config_term_to_canonical[t]
                break

        if existing_canonical is None:
            rep = choose_representative(group)
            config_data["synonyms"][rep] = sorted(group)
            for t in group:
                config_term_to_canonical[t] = rep
            added_canonicals.append(rep)
        else:
            before = set(config_data["synonyms"][existing_canonical])
            after = before | group
            if after != before:
                config_data["synonyms"][existing_canonical] = sorted(after)
                for t in after:
                    config_term_to_canonical[t] = existing_canonical
                updated_canonicals.append(existing_canonical)

    backup_path = f"{FINANCIAL_TERMS_PATH}.bak.{_now()}"
    shutil.copy2(FINANCIAL_TERMS_PATH, backup_path)
    with open(FINANCIAL_TERMS_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f"Applied {len(added_canonicals)} new groups and updated {len(updated_canonicals)} existing groups.")
    print(f"Backup saved to {backup_path}")


# ── run-all ─────────────────────────────────────────────────────────────

def cmd_run_all(args: argparse.Namespace):
    """Execute the full pipeline, iterating analyze → enrich until convergence."""
    if args.seed:
        cmd_seed(args)
    if args.collect:
        cmd_collect(args)

    for iteration in range(1, args.iterations + 1):
        print(f"\n=== Pipeline iteration {iteration}/{args.iterations} ===")
        cmd_analyze(args)
        if not args.skip_enrich and os.path.isdir(NEW_TERMS_DIR) and os.listdir(NEW_TERMS_DIR):
            before_groups = _count_groups(FINANCIAL_SYNONYMS_PATH)
            cmd_enrich(args)
            after_groups = _count_groups(FINANCIAL_SYNONYMS_PATH)
            if after_groups == before_groups:
                print("No new groups created — converged.")
                break
        else:
            print("No new terms to enrich — converged.")
            break

    if args.apply:
        cmd_apply(args)
    print("\nPipeline complete.")


def _count_groups(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return len(set(data.values()))


# ── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="End-to-end synonym collection pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_seed = sub.add_parser("seed", help="Generate config/financial_synonyms.json from canonical terms")
    p_seed.add_argument("--batch-size", type=int, default=20, help="LLM batch size for synonym generation")

    p_collect = sub.add_parser("collect", help="Run agent on question files to record keywords")
    p_collect.add_argument("--questions", required=True, help="Question JSON file or directory")
    p_collect.add_argument("--qid", default=None, help="Limit to a single qid")

    p_analyze = sub.add_parser("analyze", help="Analyze searched terms vs reference synonym graph")
    p_analyze.add_argument("--embed-model", default="text-embedding-v3", help="Embedding model name")
    p_analyze.add_argument("--threshold", type=float, default=0.90, help="Merge similarity threshold")
    p_analyze.add_argument("--margin", type=float, default=0.05, help="Top-2 similarity margin")
    p_analyze.add_argument("--qid", default=None, help="Limit to a single qid")

    p_enrich = sub.add_parser("enrich", help="Use LLM to classify new terms and generate synonyms")

    p_apply = sub.add_parser("apply", help="Merge reference groups into config/financial_terms.json")

    p_run = sub.add_parser("run-all", help="Run the full pipeline")
    p_run.add_argument("--questions", required=True, help="Question JSON file or directory")
    p_run.add_argument("--qid", default=None, help="Limit to a single qid")
    p_run.add_argument("--embed-model", default="text-embedding-v3", help="Embedding model name")
    p_run.add_argument("--threshold", type=float, default=0.90, help="Merge similarity threshold")
    p_run.add_argument("--margin", type=float, default=0.05, help="Top-2 similarity margin")
    p_run.add_argument("--seed", action="store_true", help="Run seed step")
    p_run.add_argument("--collect", action="store_true", help="Run collect step")
    p_run.add_argument("--skip-enrich", action="store_true", help="Skip LLM enrichment step")
    p_run.add_argument("--apply", action="store_true", help="Apply merged groups to financial_terms.json")
    p_run.add_argument("--iterations", type=int, default=3, help="Max analyze → enrich iterations")

    args = parser.parse_args()

    if args.command == "seed":
        cmd_seed(args)
    elif args.command == "collect":
        cmd_collect(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "enrich":
        cmd_enrich(args)
    elif args.command == "apply":
        cmd_apply(args)
    elif args.command == "run-all":
        cmd_run_all(args)


if __name__ == "__main__":
    main()
