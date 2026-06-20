# search_tables

Unified table access — search by keyword, fetch by table_id, or get all tables under a heading.

**Parameters:**
- `query` (str, optional): Keywords separated by `|`, e.g. `"力诺投资|资产负债率"`. Omit for table_id/heading_title lookup.
- `doc` (str, optional): Document ID to limit search scope
- `domain` (str, optional): Filter by domain
- `table_id` (str, optional): Single table by ID, e.g. `"T_02828"`
- `heading_title` (str, optional): All tables under this heading (requires `doc`)
- `max_results` (int, default=8): Maximum number of results

**Returns:** List of table objects with `table_id`, `doc_path`, `heading_title`, `name`, `headers`, `data`, `unit`.

**Examples:**
```json
{"tool": "search_tables", "params": {"doc": "text10", "query": "力诺投资|资产负债率"}}
```
```json
{"tool": "search_tables", "params": {"table_id": "T_02828"}}
```
```json
{"tool": "search_tables", "params": {"doc": "text10", "heading_title": "二、财务报表"}}