"""
Table extractor and namer.
Extracts all HTML <table> blocks from markdown files, parses them into structured data,
and assigns descriptive names based on heading context.

Output:
  indices/table_index.json
"""

import json
import os
import re
from pathlib import Path

from utils.text_utils import (
    normalize_text,
    parse_html_table_cells,
    extract_unit_hint,
    strip_html_tags,
)

EXTRACTED_DIR = "public_dataset_upload/extracted"
INDICES_DIR = "indices"
HEADING_INDEX_PATH = os.path.join(INDICES_DIR, "heading_index.json")


def find_all_md_files(base_dir: str) -> list[str]:
    """Recursively find all .md files."""
    md_files = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".md"):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, base_dir)
                md_files.append(rel_path)
    return sorted(md_files)


def extract_tables_from_md(filepath: str) -> list[dict]:
    """
    Extract all <table> blocks from a markdown file.
    Returns list of table dicts with raw_html, line_num, parsed rows.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    tables = []
    # Find all <table>...</table> blocks with their position in the file
    pattern = re.compile(r"<table>(.*?)</table>", re.DOTALL | re.IGNORECASE)

    # To get line numbers, split into lines and track table positions
    lines = content.split("\n")
    char_pos = 0
    line_map = []  # char_pos -> line_number
    for i, line in enumerate(lines):
        line_map.append((char_pos, i))
        char_pos += len(line) + 1  # +1 for newline

    def char_to_line(char_index: int) -> int:
        for cp, ln in reversed(line_map):
            if cp <= char_index:
                return ln
        return 0

    for match in pattern.finditer(content):
        html = match.group(0)
        inner_html = match.group(1)
        line_num = char_to_line(match.start())
        rows = parse_html_table_cells(html)
        tables.append({
            "raw_html": html,
            "line_num": line_num,
            "rows": rows,
            "row_count": len(rows),
            "col_count": max(len(r) for r in rows) if rows else 0,
        })

    return tables


def find_heading_for_line(headings: list[dict], line_num: int) -> dict | None:
    """
    Find the deepest heading that contains the given line number.
    Returns the heading dict with path info.
    """
    best = None
    for h in headings:
        if h["line_start"] <= line_num < h["line_end"]:
            if best is None or h["level"] > best["level"]:
                best = h
    return best


def get_context_before(filepath: str, line_num: int, num_lines: int = 5) -> str:
    """Get up to num_lines of text preceding the given line (exclusive)."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    start = max(0, line_num - num_lines)
    context_lines = lines[start:line_num]
    # Strip HTML tags and join
    return " ".join(strip_html_tags(l).strip() for l in context_lines if strip_html_tags(l).strip())


def generate_table_name(heading: dict | None, context: str, rows: list[list[str]]) -> str:
    """
    Generate a descriptive name for the table.
    Priority:
      1. Heading path (most reliable)
      2. Context text hints (unit declarations, labels)
      3. Table header row (column names summary)
    """
    parts = []

    # Part 1: heading context
    if heading:
        path = heading.get("path", [heading["title"]])
        # Take the last 2-3 meaningful segments
        meaningful = [p for p in path if p and len(p) > 2]
        parts.append(" > ".join(meaningful[-2:]))

    # Part 2: context hints
    if context:
        context_clean = normalize_text(context)[:80]
        # Look for descriptive patterns
        hint_patterns = [
            r"下表[^。]*[：:]",
            r"如下[^。]*[：:]",
            r"具体[^。]*[：:]",
        ]
        for pat in hint_patterns:
            m = re.search(pat, context_clean)
            if m:
                hint = m.group(0).strip()
                parts.append(hint)
                break

    # Part 3: header row summary
    if rows and rows[0]:
        header = rows[0]
        # Take first 3 meaningful column names
        col_names = [h for h in header[:3] if h and len(h) > 1]
        if col_names:
            parts.append(f"[{', '.join(col_names)}]")

    name = " / ".join(parts) if parts else "未命名表格"
    return name


def extract_unit_from_table(table: dict, context: str) -> str | None:
    """Determine the unit of the table values."""
    # Check context before table
    unit = extract_unit_hint(context)
    if unit:
        return unit
    # Check first row for unit hints
    if table["rows"]:
        first_row_text = " ".join(str(c) for c in table["rows"][0])
        unit = extract_unit_hint(first_row_text)
        if unit:
            return unit
    return None


def main():
    os.makedirs(INDICES_DIR, exist_ok=True)

    print("Loading heading index...")
    with open(HEADING_INDEX_PATH, "r", encoding="utf-8") as f:
        heading_index = json.load(f)
    documents_headings = heading_index["documents"]

    print("Finding markdown files...")
    md_files = find_all_md_files(EXTRACTED_DIR)
    print(f"  Processing {len(md_files)} .md files")

    all_tables = []
    table_id_counter = 1

    for rel_path in md_files:
        abs_path = os.path.join(EXTRACTED_DIR, rel_path)
        tables = extract_tables_from_md(abs_path)

        if not tables:
            continue

        doc_headings = documents_headings.get(rel_path, [])

        for table in tables:
            heading = find_heading_for_line(doc_headings, table["line_num"])
            context = get_context_before(abs_path, table["line_num"], num_lines=6)
            name = generate_table_name(heading, context, table["rows"])
            unit = extract_unit_from_table(table, context)

            # Build table record
            table_record = {
                "table_id": f"T_{table_id_counter:05d}",
                "doc_path": rel_path,
                "name": name,
                "heading_path": heading.get("path", []) if heading else [],
                "heading_title": heading.get("title", "") if heading else "",
                "line_num": table["line_num"],
                "row_count": table["row_count"],
                "col_count": table["col_count"],
                "headers": table["rows"][0] if table["rows"] else [],
                "data": table["rows"][1:] if len(table["rows"]) > 1 else [],
                "unit": unit,
                "context_before": context[-200:],  # last 200 chars
            }

            all_tables.append(table_record)
            table_id_counter += 1

    # Build indices for fast lookup
    table_index = {
        "tables": all_tables,
        "by_doc": {},
        "by_heading": {},
        "total": len(all_tables),
    }

    for t in all_tables:
        doc = t["doc_path"]
        if doc not in table_index["by_doc"]:
            table_index["by_doc"][doc] = []
        table_index["by_doc"][doc].append(t["table_id"])

        heading_title = t["heading_title"]
        if heading_title:
            key = f"{doc}::{heading_title}"
            if key not in table_index["by_heading"]:
                table_index["by_heading"][key] = []
            table_index["by_heading"][key].append(t["table_id"])

    table_index_path = os.path.join(INDICES_DIR, "table_index.json")
    with open(table_index_path, "w", encoding="utf-8") as f:
        json.dump(table_index, f, ensure_ascii=False, indent=2)

    print(f"  Extracted {len(all_tables)} tables from {len(table_index['by_doc'])} documents")
    print(f"  Saved table_index.json")

    # Print summary
    domains = {}
    for t in all_tables:
        domain = Path(t["doc_path"]).parts[0]
        domains[domain] = domains.get(domain, 0) + 1
    for domain, count in sorted(domains.items()):
        print(f"    {domain}: {count} tables")

    return table_index


if __name__ == "__main__":
    main()