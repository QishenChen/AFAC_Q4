# search_text

Search RAW TEXT (not tables) within a document. Split query into individual terms with `|` (e.g. `"净利润|下滑|2025"`, not `"净利润下滑"`). `doc` is REQUIRED.

**Parameters:**
- `doc` (str, required): Document ID to search within
- `query` (str, required): Keywords separated by `|`
- `max_results` (int, default=8): Maximum number of results

**Returns:** List of text match objects with `line_num`, `text`, `doc`.

**Example:**
```json
{"tool": "search_text", "params": {"doc": "text10", "query": "力诺投资|资产负债率|净利润"}}