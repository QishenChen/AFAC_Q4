"""
Text normalization, tokenization, and fuzzy matching utilities for Chinese financial text.
Uses character n-grams with IDF-weighted scoring (common words down-weighted).
"""

import json
import math
import os
import re
import unicodedata

# ── Load word frequency weights ──
_WORD_WEIGHTS = {}
_WORD_WEIGHTS_MAX = 1.0

def _load_word_weights():
    """Load `config/common_words.json` to compute IDF-like weights for fuzzy matching."""
    global _WORD_WEIGHTS, _WORD_WEIGHTS_MAX
    if _WORD_WEIGHTS:
        return
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "common_words.json")
    if not os.path.isfile(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        total = data.get("total_words", 1)
        word_list = data.get("words", [])
        for entry in word_list:
            w = entry["word"]
            count = entry["count"]
            # IDF-style log scale: common words → low weight, rare → high weight
            _WORD_WEIGHTS[w] = math.log(total / (count + 1))
        _WORD_WEIGHTS_MAX = max(_WORD_WEIGHTS.values()) if _WORD_WEIGHTS else 1.0
    except Exception:
        pass

_load_word_weights()


def normalize_text(text: str) -> str:
    """Normalize text: NFKC unicode, lowercase, collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def is_heading_line(line: str):
    """
    Check if a line is a markdown heading.
    Returns (True, level, title) or (False, 0, '').
    """
    match = re.match(r"^(#{1,6})\s+(.+)$", line)
    if match:
        level = len(match.group(1))
        title = match.group(2).strip()
        return True, level, title
    return False, 0, ""


def extract_inline_heading_from_html(line: str):
    """
    Detect heading patterns embedded inside HTML <td> cells, like:
    '1.1 保险责任' or '1.1.4 养老保险金领取标准' inside a table row.
    Returns (True, level_offset, title) where level_offset is added to the parent heading level.
    """
    # Match patterns like "1.1 保险责任" or "1.1.4 养老保险金领取标准"
    match = re.match(r"^\s*(\d+(?:\.\d+)+)\s+(.+)$", line)
    if match:
        num = match.group(1)
        title = match.group(2).strip()
        # depth = number of dot-segments (1.1 = 2 segments => level +1)
        depth = num.count(".") + 1
        return True, depth, f"{num} {title}"
    return False, 0, ""


def tokenize_chinese(text: str) -> list[str]:
    """
    Tokenize Chinese text into character bigrams + trigrams + full match.
    Bigrams provide baseline recall; trigrams + full match add specificity.
    Unigrams are excluded to reduce noise from single-character matches.
    """
    text = normalize_text(text)
    chars = re.findall(r"[\u4e00-\u9fff]", text)
    tokens = []
    if len(chars) >= 2:
        tokens.extend("".join(chars[i:i + 2]) for i in range(len(chars) - 1))  # bigrams
    if len(chars) >= 3:
        tokens.extend("".join(chars[i:i + 3]) for i in range(len(chars) - 2))  # trigrams
    if len(chars) >= 4:
        tokens.append("".join(chars))  # full match
    alpha_tokens = re.findall(r"[a-zA-Z0-9]+", text)
    tokens.extend(t.lower() for t in alpha_tokens)
    return list(set(tokens))


def token_overlap_score(query_tokens: list[str], target_tokens: list[str]) -> float:
    """Weighted overlap score. Common words get lower weight via IDF."""
    if not query_tokens or not target_tokens:
        return 0.0
    q_set = set(query_tokens)
    c_set = set(target_tokens)
    intersection = q_set & c_set
    if not intersection:
        return 0.0
    if _WORD_WEIGHTS:
        # Weighted: sum IDF weights of overlapping tokens / max possible
        weighted = sum(_WORD_WEIGHTS.get(t, _WORD_WEIGHTS_MAX) for t in intersection)
        max_weighted = sum(_WORD_WEIGHTS.get(t, _WORD_WEIGHTS_MAX) for t in q_set)
        return weighted / max(1, max_weighted)
    return len(intersection) / min(len(q_set), len(c_set))


def fuzzy_match(query: str, candidate: str, threshold: float = 0.3) -> float:
    """Fuzzy match a query against a candidate string using character n-gram overlap."""
    q_tokens = tokenize_chinese(query)
    c_tokens = tokenize_chinese(candidate)
    return token_overlap_score(q_tokens, c_tokens)


def strip_html_tags(text: str) -> str:
    """Remove HTML tags from text, leaving only content."""
    return re.sub(r"<[^>]+>", "", text)


def parse_html_table_cells(html: str):
    """
    Parse a <table> HTML string into rows of cells.
    Returns list of list of strings (stripped of HTML inside cells).
    Handles rowspan/colspan minimally by repeating cells.
    """
    # Find all rows
    rows = re.findall(r"<tr>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
    result = []
    for row_html in rows:
        cells = re.findall(r"<(?:td|th)[^>]*>(.*?)</(?:td|th)>", row_html, re.DOTALL | re.IGNORECASE)
        # Strip inner HTML tags
        clean_cells = [strip_html_tags(c).strip() for c in cells]
        result.append(clean_cells)
    return result


def extract_unit_hint(text: str) -> str | None:
    """
    Detect unit declarations like '单位：万元', '单位：千元', '单位：元'.
    Returns the unit string or None.
    """
    match = re.search(r"单位[：:]\s*(.+?)(?:$|\n)", text)
    if match:
        return match.group(1).strip()
    return None


def extract_year_from_text(text: str) -> list[str]:
    """Extract 4-digit years from text, e.g., '2024', '2025'."""
    return re.findall(r"\b(20\d{2})\b", text)