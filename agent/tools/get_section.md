# get_section

Get FULL text + ALL tables under a heading. `heading_path` is the exact title from `search_headings` results.

**Parameters:**
- `doc` (str, required): Document ID
- `heading_path` (str or list[str], required): Exact heading title. **Strip trailing page number dots/numbers** (e.g. `".. .. 181"`, `". 174"`, `"..262"`) from the title before passing.

**Returns:** Object with `heading`, `content` (full text), `tables` (list of table objects).
