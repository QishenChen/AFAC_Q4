# search_headings

Search section headings by keyword. Split query into individual terms with `|`. Set `doc` to limit scope to one document.

**Parameters:**
- `query` (str, required): Keywords separated by `|`, e.g. `"利润|资产|负债"`
- `doc` (str, optional): Document ID to limit search scope
- `domain` (str, optional): Filter by domain
- `max_results` (int, default=10): Maximum number of results

**Returns:** List of heading objects with `title`, `doc`, `path`.

**Example:**
```json
{"tool": "search_headings", "params": {"query": "资产负债表|利润表", "doc": "text01"}}