# get_all_headings

Return ALL heading titles with hierarchy for an insurance policy document. Use at the start of insurance questions to understand the document structure. Also use when search_headings returns no good matches — scan all headings to find the right section.

**Parameters:**
- `doc` (str, required): Document ID, e.g. `"1"`, `"3"`, `"15"`

**Returns:** List of `{level: 2-6, title: str}` for all headings in the document.

**Example:**
```json
{"tool": "get_all_headings", "params": {"doc": "1"}}