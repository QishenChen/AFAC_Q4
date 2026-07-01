#!/usr/bin/env python3
"""Analyze agent search keywords and discover synonym groups via online embeddings.

Reads results/keywords/*/keywords.jsonl, compares each unknown term against a
reference synonym graph (by default config/financial_synonyms.json) using an
OpenAI-compatible embedding API, and either proposes a merge into that group or
creates a directory for manual review of new terms.
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict
from datetime import datetime

import numpy as np

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.llm_reasoner import get_llm_config


DEFAULT_KEYWORDS_DIR = "results/keywords"
DEFAULT_TARGET_PATH = "config/financial_synonyms.json"
DEFAULT_CONFIG_PATH = "config/financial_terms.json"
DEFAULT_EMBED_MODEL = "text-embedding-v3"
DEFAULT_THRESHOLD = 0.90
DEFAULT_MARGIN = 0.05
DEFAULT_BATCH_SIZE = 10


def choose_representative(terms: set[str]) -> str:
    """Pick a representative canonical from a synonym group."""
    return sorted(terms, key=lambda t: (-len(t), t))[0]


def load_target_groups(target_path: str):
    """Load a synonym graph from either financial_terms.json or financial_synonyms.json format."""
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Format 1: {"synonyms": {"canonical": ["syn1", ...]}}
    if isinstance(data, dict) and "synonyms" in data:
        raw_groups = data["synonyms"]
        canonical_to_group = {}
        term_to_canonical = {}
        for canonical, syns in raw_groups.items():
            group = set(syns)
            group.add(canonical)
            canonical_to_group[canonical] = group
            for t in group:
                term_to_canonical[t] = canonical
        return canonical_to_group, term_to_canonical

    # Format 2: {"term": group_id, ...}
    groups_by_id = defaultdict(set)
    for term, gid in data.items():
        groups_by_id[gid].add(term)

    canonical_to_group = {}
    term_to_canonical = {}
    for gid, terms in groups_by_id.items():
        canonical = choose_representative(terms)
        canonical_to_group[canonical] = terms
        for t in terms:
            term_to_canonical[t] = canonical
    return canonical_to_group, term_to_canonical


def load_keyword_records(keywords_dir: str, qid_filter: str | None = None):
    """Load all keyword records from the keyword tracker directory."""
    records = []
    if not os.path.isdir(keywords_dir):
        return records
    for qid in sorted(os.listdir(keywords_dir)):
        qpath = os.path.join(keywords_dir, qid)
        if not os.path.isdir(qpath):
            continue
        if qid_filter and qid != qid_filter:
            continue
        path = os.path.join(qpath, "keywords.jsonl")
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def extract_terms(records: list[dict]):
    """Extract and deduplicate query terms from keyword records."""
    term_info = defaultdict(lambda: {"count": 0, "qids": set(), "queries": set()})
    for r in records:
        query = r.get("original_query", "")
        qid = r.get("qid", "unknown")
        if not query:
            continue
        for term in query.split("|"):
            term = term.strip()
            if not term or len(term) < 2:
                continue
            info = term_info[term]
            info["count"] += 1
            info["qids"].add(qid)
            info["queries"].add(query)
    return term_info


def safe_dir_name(term: str) -> str:
    """Make a term safe for use as a directory name."""
    return re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", term).strip("_") or "term"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between a vector and a matrix of vectors."""
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    if b.ndim == 1:
        b = b[np.newaxis, :]
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b, axis=1)
    if a_norm == 0:
        return np.zeros(len(b), dtype=np.float32)
    b_norm = np.where(b_norm == 0, 1e-10, b_norm)
    return np.dot(b, a) / (b_norm * a_norm)


class OnlineEmbeddingAnalyzer:
    def __init__(self, model_name: str, config: dict, cache_path: str | None = None):
        import requests

        self.model = model_name
        self.config = config
        self.requests = requests
        self.cache_path = cache_path
        self.cache = {}
        if cache_path and os.path.isfile(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    for k, v in raw.items():
                        self.cache[k] = np.asarray(v, dtype=np.float32)
            except Exception:
                self.cache = {}
        self.group_embeddings = {}
        self.canonical_to_group = {}

    def _call_api(self, texts: list[str]) -> dict[str, np.ndarray]:
        """Call the embedding API for a batch of texts."""
        if not texts:
            return {}
        texts = [t for t in texts if t]
        api_base = self.config.get("api_base", "").rstrip("/")
        api_key = self.config.get("api_key", "")
        if not api_base or not api_key:
            raise RuntimeError("Missing API base or key for embeddings")
        url = f"{api_base}/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {"model": self.model, "input": texts}
        resp = self.requests.post(url, headers=headers, json=payload, timeout=(10, 60))
        resp.raise_for_status()
        data = resp.json()
        result = {}
        for item in data.get("data", []):
            idx = item.get("index")
            emb = item.get("embedding")
            if idx is not None and emb is not None and idx < len(texts):
                result[texts[idx]] = np.asarray(emb, dtype=np.float32)
        return result

    def _get_embeddings(self, texts: list[str]) -> dict[str, np.ndarray]:
        """Fetch embeddings with caching and small batching."""
        texts = list(dict.fromkeys(texts))
        missing = [t for t in texts if t not in self.cache]
        for i in range(0, len(missing), DEFAULT_BATCH_SIZE):
            batch = missing[i : i + DEFAULT_BATCH_SIZE]
            try:
                batch_embs = self._call_api(batch)
                self.cache.update(batch_embs)
            except Exception as e:
                print(f"Embedding API error for batch {i}: {e}")
                for t in batch:
                    self.cache[t] = np.zeros(1, dtype=np.float32)
            time.sleep(0.2)
        return {t: self.cache[t] for t in texts if t in self.cache}

    def _save_cache(self):
        if not self.cache_path:
            return
        os.makedirs(os.path.dirname(self.cache_path) or ".", exist_ok=True)
        serializable = {k: v.tolist() for k, v in self.cache.items()}
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def fit(self, canonical_to_group: dict[str, set[str]]):
        """Compute mean embeddings for each synonym group."""
        self.canonical_to_group = canonical_to_group
        all_terms = []
        group_indices = []
        for canonical, group in canonical_to_group.items():
            terms = sorted(group)
            all_terms.extend(terms)
            group_indices.extend([canonical] * len(terms))
        if not all_terms:
            return
        embs = self._get_embeddings(all_terms)
        group_embs = defaultdict(list)
        for canonical, term in zip(group_indices, all_terms):
            emb = embs.get(term)
            if emb is not None and emb.shape[0] > 1:
                group_embs[canonical].append(emb)
        for canonical, embs_list in group_embs.items():
            if embs_list:
                self.group_embeddings[canonical] = np.mean(embs_list, axis=0)
        self._save_cache()

    def classify(self, term: str, threshold: float, margin: float):
        """Return (action, target_canonical, similarity, top_groups)."""
        if not self.group_embeddings:
            return "new", None, 0.0, []
        emb = self._get_embeddings([term]).get(term)
        if emb is None or emb.shape[0] <= 1:
            return "new", None, 0.0, []
        group_canonicals = list(self.group_embeddings.keys())
        group_matrix = np.stack([self.group_embeddings[c] for c in group_canonicals], axis=0)
        sims = cosine_similarity(emb, group_matrix)
        ranked_idx = np.argsort(sims)[::-1]
        ranked = [(group_canonicals[i], float(sims[i])) for i in ranked_idx]
        if not ranked:
            return "new", None, 0.0, []
        best_canonical, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0
        top_groups = [{"canonical": c, "similarity": round(s, 4)} for c, s in ranked[:3]]
        if best_score >= threshold and (best_score - second_score) >= margin:
            return "merge", best_canonical, best_score, top_groups
        return "new", None, best_score, top_groups


def analyze(args: argparse.Namespace):
    records = load_keyword_records(args.keywords_dir, args.qid)
    if not records:
        print(f"No keyword records found in {args.keywords_dir}")
        return

    term_info = extract_terms(records)
    print(f"Loaded {len(records)} keyword records, {len(term_info)} unique terms")

    canonical_to_group, term_to_canonical = load_target_groups(args.target)
    print(f"Loaded {len(canonical_to_group)} reference synonym groups from {args.target}")

    known_terms = {}
    unknown_terms = {}
    for term, info in term_info.items():
        if term in term_to_canonical:
            canonical = term_to_canonical[term]
            known_terms[term] = {
                "canonical": canonical,
                "group": sorted(canonical_to_group[canonical]),
                "count": info["count"],
                "qids": sorted(info["qids"]),
            }
        else:
            unknown_terms[term] = info

    print(f"  Known: {len(known_terms)}, Unknown: {len(unknown_terms)}")

    cache_path = os.path.join(args.keywords_dir, "analysis", "embedding_cache.json")
    config = get_llm_config()
    analyzer = OnlineEmbeddingAnalyzer(args.model, config, cache_path=cache_path)

    if unknown_terms:
        print("Computing embeddings for reference synonym groups...")
        analyzer.fit(canonical_to_group)
        print("Classifying unknown terms...")

    proposed_merges = {}
    new_terms = {}

    for term, info in unknown_terms.items():
        action, target, score, top_groups = analyzer.classify(term, args.threshold, args.margin)
        base = {
            "count": info["count"],
            "qids": sorted(info["qids"]),
            "example_queries": sorted(info["queries"])[:5],
            "top_similar_groups": top_groups,
        }
        if action == "merge" and target:
            group_after = sorted(canonical_to_group.get(target, {target}) | {term})
            proposed_merges[term] = {
                **base,
                "target_canonical": target,
                "similarity": round(score, 4),
                "group_after_merge": group_after,
            }
        else:
            new_terms[term] = base

    analyzer._save_cache()

    # Write analysis outputs
    analysis_dir = os.path.join(args.keywords_dir, "analysis")
    new_terms_dir = os.path.join(args.keywords_dir, "new_terms")
    os.makedirs(analysis_dir, exist_ok=True)
    shutil.rmtree(new_terms_dir, ignore_errors=True)
    os.makedirs(new_terms_dir, exist_ok=True)

    with open(os.path.join(analysis_dir, "known_terms.json"), "w", encoding="utf-8") as f:
        json.dump(known_terms, f, ensure_ascii=False, indent=2)

    with open(os.path.join(analysis_dir, "proposed_merges.json"), "w", encoding="utf-8") as f:
        json.dump(proposed_merges, f, ensure_ascii=False, indent=2)

    new_summary = {
        "total_unknown": len(unknown_terms),
        "proposed_merges": len(proposed_merges),
        "new_terms": len(new_terms),
        "terms": sorted(new_terms.keys()),
    }
    with open(os.path.join(analysis_dir, "new_terms_summary.json"), "w", encoding="utf-8") as f:
        json.dump(new_summary, f, ensure_ascii=False, indent=2)

    for term, info in new_terms.items():
        d = os.path.join(new_terms_dir, safe_dir_name(term))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "info.json"), "w", encoding="utf-8") as f:
            json.dump({"term": term, **info}, f, ensure_ascii=False, indent=2)

    # Optional: apply merges to config
    if args.apply and proposed_merges:
        backup_path = f"{args.config}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(args.config, backup_path)
        with open(args.config, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        # Map each term already in financial_terms.json to its canonical key
        config_term_to_canonical = {}
        for canonical, syns in config_data.get("synonyms", {}).items():
            config_term_to_canonical[canonical] = canonical
            for s in syns:
                config_term_to_canonical[s] = canonical

        for term, merge_info in proposed_merges.items():
            target = merge_info["target_canonical"]
            target_group = set(merge_info.get("group_after_merge", [target, term]))

            # Prefer an existing financial_terms.json group that overlaps with the target group
            existing_canonical = None
            for t in target_group:
                if t in config_term_to_canonical:
                    existing_canonical = config_term_to_canonical[t]
                    break

            if existing_canonical is None:
                # No overlapping group in financial_terms.json — import the whole reference group
                existing_canonical = target
                config_data["synonyms"][existing_canonical] = sorted(target_group)
                for t in target_group:
                    config_term_to_canonical[t] = existing_canonical
            else:
                if term not in config_data["synonyms"][existing_canonical]:
                    config_data["synonyms"][existing_canonical].append(term)
                    config_term_to_canonical[term] = existing_canonical

        with open(args.config, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        print(f"Applied {len(proposed_merges)} merges; backup at {backup_path}")

    print("\nSummary:")
    print(f"  Known terms:            {len(known_terms)}")
    print(f"  Proposed merges:        {len(proposed_merges)}")
    print(f"  New terms (directories): {len(new_terms)}")
    print(f"\nOutputs written to:")
    print(f"  {analysis_dir}/known_terms.json")
    print(f"  {analysis_dir}/proposed_merges.json")
    print(f"  {analysis_dir}/new_terms_summary.json")
    print(f"  {new_terms_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Analyze agent search keywords and discover synonyms via online embeddings.")
    parser.add_argument("--keywords-dir", default=DEFAULT_KEYWORDS_DIR, help="Directory containing qid keyword logs")
    parser.add_argument("--target", default=DEFAULT_TARGET_PATH, help="Reference synonym graph (financial_synonyms.json or financial_terms.json)")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH, help="Path to financial_terms.json (used for --apply)")
    parser.add_argument("--model", default=DEFAULT_EMBED_MODEL, help="Embedding model name")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Cosine similarity threshold for merging")
    parser.add_argument("--margin", type=float, default=DEFAULT_MARGIN, help="Margin between top two similarity scores")
    parser.add_argument("--qid", default=None, help="Limit analysis to a single qid")
    parser.add_argument("--apply", action="store_true", help="Apply proposed merges to config/financial_terms.json")
    args = parser.parse_args()
    analyze(args)


if __name__ == "__main__":
    main()
