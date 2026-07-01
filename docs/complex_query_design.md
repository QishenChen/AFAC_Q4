# Financial Document Intelligence Platform — Design

> Extension of `agent/` into a complete document Q&A system.
> Four task types: `extract` · `reasoning` · `output` · `qa`

---

## Layer Architecture

```
┌──────────────────────────────────────────────┐
│              Interface                        │
│  MCP Server  ·  REST API  ·  Chat CLI        │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────┴──────────────────────────┐
│         Intelligence                         │
│  Planner (WHAT)  +  Executor (HOW)           │
│  Task types: extract | reasoning | output | qa│
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────┴──────────────────────────┐
│            Capabilities (Tools)               │
│  search · extract · verify · compute         │
│  dedup · synthesize · decompose · compare    │
└───────────────────┬──────────────────────────┘
                    │
┌───────────────────┴──────────────────────────┐
│              Data                             │
│  ingest · parse · index · cache              │
└──────────────────────────────────────────────┘
```

---

## 1. Planner (strategic — decides WHAT)

One LLM call per query. Takes user question + available document catalog.
Returns a **high‑level execution plan** — no keywords, no tool params.

### Plan schema

```json
{
  "task_type": "extract | reasoning | output | qa",
  "objective": "what the user wants",
  "target_scope": ["document areas to search"],
  "exclude_scope": ["areas to skip"],
  "output_shape": "list | table | paragraph | choices"
}
```

### The four task types

| task_type | Meaning | Example query |
|-----------|---------|---------------|
| `extract` | Collect specific facts/entities from docs | "List all construction cities" |
| `reasoning` | Analyze, compare, compute, draw conclusions | "Compare R&D efficiency of BYD vs CATL" |
| `output` | Synthesize/summarize into free text | "Summarize key risks in this bond" |
| `qa` | Fixed‑option MCQ/TF/multi‑choice | "Which statements are correct?" |

### Planner output examples

**Extraction query** — "中国建筑在哪些城市有施工项目？"
```json
{
  "task_type": "extract",
  "objective": "Find all cities where the company has construction projects",
  "target_scope": ["项目相关章节", "工程披露章节", "业务分部章节"],
  "exclude_scope": ["风险因素章节", "会计政策章节"],
  "output_shape": "list"
}
```

**Reasoning query** — "Compare R&D spending of BYD and CATL 2022-2024"
```json
{
  "task_type": "reasoning",
  "objective": "Compare R&D efficiency (R&D/revenue ratio) between two companies",
  "target_scope": ["BYD年报 研发投入章节", "CATL年报 研发投入章节"],
  "output_shape": "table"
}
```

**Output query** — "What are the key risk factors in this bond?"
```json
{
  "task_type": "output",
  "objective": "Summarize all risk factors mentioned in the bond document",
  "target_scope": ["风险因素章节", "重大事项提示"],
  "output_shape": "paragraph"
}
```

**QA query** — delegates to existing `agent/context/`.
```json
{
  "task_type": "qa",
  "objective": "Answer the multi-choice question",
  "delegate": "agent/context/"
}
```

---

## 2. Executor (tactical — decides HOW)

Generic loop. Takes a plan, executes it, calls Planner again if stuck.

### Core loop

```
load plan

for each task_type:
  ├── extract:
  │     for each target area:
  │       generate keywords → search → extract → verify → dedup
  │       if saturation (2 rounds no new) → done with this area
  │
  ├── reasoning:
  │     extract per‑entity data → compute ratios/differences
  │     → compare → format table
  │
  ├── output:
  │     broad retrieval across target areas → rerank
  │     → LLM synthesize with inline citations
  │
  └── qa:
        delegate to existing agent/context/ (ReACT loop)

if stuck or low confidence:
    → call Planner: "here's what we found, suggest new target areas"
    → new plan replaces old, continue
```

### Keyword generation (Executor's job)

The Executor takes a target area like `"项目相关章节"` and the entity type from the Planner. It then **generates keywords dynamically** using LLM:

```
"Given target area '项目相关章节' and entity type '城市/地点',
generate 2-3 keyword queries to find relevant sections."
→ "项目|工程|施工", "位于|地址|坐落"
```

The Planner never touches this. Executor owns search strategy.

### Saturation (when to stop)

After each round, count new entities found. If 2 consecutive rounds produce 0 new entities, the area is saturated — move to next target area.

### Rewrite loop

If saturation happens but confidence is low (found only 2 entities from a construction company that likely has 30+), the Executor calls Planner:

```
"We searched '项目相关章节' and '工程披露章节' and found only 2 cities.
Confidence is low. Suggest additional target areas to search."
```

Planner returns new target areas. Executor continues.

---

## 3. Tools (Capability Layer)

### Existing (reused)

| Tool | Purpose |
|------|---------|
| `search_text`, `search_headings`, `search_tables` | Keyword retrieval |
| `get_section` | Read full section content |
| `compute` | Arithmetic with unit handling |
| `get_doc_info` | Document metadata |

### New

| Tool | Purpose |
|------|---------|
| `extract_entities` | LLM extracts entities from text chunks. Must output `{"entity":..., "quote":"exact source text", "line":N}` |
| `verify_entity` | Python: `quote in source_document` → boolean |
| `deduplicate` | LLM clusters similar names ("深圳"/"深圳市" → "深圳市") |
| `synthesize` | LLM generates free‑text answer from retrieved chunks with inline citations |
| `decompose` | Break complex reasoning query into sub‑steps |
| `search_scope` | Search within specific document sections |

---

## 4. Quality Control

| Layer | Mechanism |
|-------|-----------|
| Quote requirement | Every extracted entity must include exact source text |
| Python verification | Quote must exist verbatim in original document |
| Saturation check | Stop only when no new results appear |
| Confidence scoring | LLM self‑rates each extraction |
| Rewrite loop | If stuck, Planner suggests new search angles |

---

## 5. Interfaces

### MCP Server — for LLM‑powered IDEs

Exposes Planner + Executor as tools that Cline/Cursor/etc. can call.
Users ask questions in natural language directly in their editor.

### REST API — for web apps

`POST /query` — full Planner → Executor pipeline  
`POST /extract` — extraction only  
`POST /summarize` — synthesis only  
`POST /ask` — MCQ/TF QA only (existing ReACT)

### Chat CLI — for development

`python3 chat.py "中国建筑有哪些施工项目城市？"`

---

## 6. What stays unchanged

- `agent/tools/` — current search + compute tools
- `agent/context/` — MCQ/TF/multi strategies
- `agent/llm_reasoner.py` — LLM API
- `agent/react_loop.py` — dispatcher
- `run_parallel.py`, `debugger.py`

## New files

```
agent/
  strategies/
    planner.py          # LLM → high‑level plan (WHAT)
    executor.py         # Generic loop (HOW), all task types
agent/
  tools/
    extract_entities.py # Quote‑verified extraction
    synthesize.py       # LLM summarization with citations
    decompose.py        # Break complex query into sub‑steps
    compare_entities.py # Side‑by‑side comparison
    search_scope.py     # Section‑scoped search
server/
    mcp_server.py       # MCP tool exposure
    api.py              # REST endpoints
```

## Implementation effort: ~30 hours