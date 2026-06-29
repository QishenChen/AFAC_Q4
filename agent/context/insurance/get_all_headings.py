"""get_all_headings — Return all heading titles with hierarchy for an insurance document."""

import os
import re


def get_all_headings(doc: str):
    """Returns all headings from insurance/{doc}.md with level, title, and path."""
    filepath = os.path.join("public_dataset_upload/extracted/insurance", f"{doc}.md")
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    headings = []
    for line in lines:
        match = re.match(r"^(#{2,6})\s+(.+)", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append({"level": level, "title": title})

    return headings