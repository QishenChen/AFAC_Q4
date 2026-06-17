# AFAC Q4 — Financial QA ReACT Agent

基于 ReACT（Think → Act → Observe）架构的金融知识问答代理。通过多层级检索（标题、表格、段落文本）从已解析的财报、保险、监管文档中提取数据，由 LLM 驱动推理并回答问题。

## 项目结构

```
├── agent.py                  # 入口：加载问题 → 运行 ReACT → 输出结果
├── retriever.py              # 多层级检索引擎（标题索引 + 表格索引 + 同义词扩展）
├── indexer.py                # 索引构建器（解析 Markdown 文档 → 生成索引 JSON）
├── build_indices.py          # 一键重建所有检索索引
├── table_extractor.py        # PDF 表格提取
├── run_mineru_extraction.py  # MinerU 批量文档解析
├── agent/
│   ├── react_loop.py         # ReACT 循环（每个选项独立运行，最多 6 轮 Think→Act→Observe）
│   ├── llm_reasoner.py       # LLM 调用封装（DashScope Qwen）+ Think / Judge prompt
│   ├── tools.py              # 工具注册表（5 个嵌入式工具暴露给 LLM + 1 个内部工具）
│   └── question_loader.py    # 问题 JSON 加载 + 文档可用性检查
├── config/
│   └── financial_terms.json  # 金融术语同义词映射
├── indices/                  # 检索索引
│   ├── doc_registry.json     # 文档注册表（doc_id → 路径/域名映射）
│   ├── table_index.json      # 表格内容索引
│   └── heading_index.json    # 标题层级索引（需通过 build_indices.py 生成，~188 MB）
├── utils/
│   └── text_utils.py         # 文本标准化、中文分词、模糊匹配
├── public_dataset_upload/
│   ├── questions/group_a/    # 五类评测问题（financial_reports / contracts / insurance / regulatory / research）
│   └── extracted/            # 已解析的 Markdown 文档（财报/合同/保险/监管/研报）
└── results/
    └── answers.json          # 问答结果输出
```

## 快速开始

### 1. 环境配置

```bash
pip install requests
```

### 2. 设置 API Key

```bash
export LLM_API_KEY="sk-your-dashscope-api-key"
export LLM_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_MODEL="qwen-plus-latest"
```

API Key 从 [DashScope 控制台](https://dashscope.aliyun.com/) 获取。若不设置环境变量，需在 `agent/llm_reasoner.py` 的 `DEFAULT_CONFIG` 中直接填入。

### 3. 重建索引（首次使用或文档更新后）

```bash
python3 build_indices.py
```

生成三个索引文件：
- `indices/heading_index.json` — 标题层级索引（约 188 MB，已加入 .gitignore）
- `indices/table_index.json` — 表格内容索引
- `indices/doc_registry.json` — 文档注册表

### 4. 运行问答

**单个问题测试：**

```bash
python3 agent.py -q public_dataset_upload/questions/group_a/financial_reports_questions.json --qid fin_a_001 -v
```

**完整批量运行：**

```bash
python3 agent.py -q public_dataset_upload/questions/group_a/financial_reports_questions.json
```

**运行所有五类问题：**

```bash
python3 agent.py -q public_dataset_upload/questions/group_a/
```

**命令行参数：**

| 参数 | 说明 |
|------|------|
| `-q, --questions` | 问题 JSON 文件或目录路径 |
| `--qid` | 仅运行指定 qid 的问题 |
| `-o, --output` | 输出 JSON 文件路径（默认 `results/answers.json`） |
| `-v, --verbose` | 打印详细 ReACT 日志 |
| `--no-llm` | 跳过 LLM 推理，仅输出上下文 |

## 架构

### ReACT 循环

每个问题的每个选项独立运行（最多 6 轮）：

```
Round 0: 检查可用文档
Round 1–6:
  THINK   → LLM 决定调用哪些工具（可并行多个）
  ACT     → 执行工具调用
  OBSERVE → 汇总工具返回结果，格式化供 LLM 阅读
```

LLM 可在任意轮次给出判断（TRUE / FALSE / VAGUE）。第 6 轮仍未判断时，系统自动调用 `reason_on_context` 强制裁决（将所有检索到的表格和章节拼接为上下文，交由 LLM 一次性判断）。

### 工具列表

| # | 工具 | 参数 | 用途 |
|---|------|------|------|
| 1 | `search_headings` | `query`, `doc?`, `domain?`, `max_results?` | 按关键词搜索文档标题 |
| 2 | `search_tables` | `query?`, `doc?`, `domain?`, `table_id?`, `heading_title?`, `max_results?` | 三模式统一：关键词搜索 / 按 ID 获取单表 / 按标题获取下属所有表格 |
| 3 | `search_section_text` | `doc`, `query`, `max_results?` | 搜索文档原始段落文本（条款、披露、叙事内容） |
| 4 | `get_section` | `doc`, `heading_path` | 获取标题下完整文本 + 所有表格 |
| 5 | `get_doc_info` | `rel_path` | 获取文档元信息 |

另有 `expand_query`（同义词扩展）为内部工具，不在 LLM 提示词中暴露。

`search_tables` 的三种调用模式：

| 模式 | 参数示例 |
|------|---------|
| 关键词搜索 | `{"query": "营业收入\|2025", "doc": "annual_byd_2025_report"}` |
| 按 ID 获取 | `{"table_id": "T_02828"}` |
| 按标题获取 | `{"doc": "annual_byd_2025_report", "heading_title": "二、财务报表"}` |

### 检索层

```
LLM 提问
  ↓ 调用工具
Retriever
  ├── search_headings   → heading_index（倒排索引 + 模糊匹配）
  ├── search_tables     → table_index（名称/表头/数据行多维模糊匹配）
  └── search_section_text → 原始 Markdown 正文模糊搜索
```

评分策略（`search_tables`）：

| 字段 | 权重 |
|------|------|
| 表格名称 (`name`) | 35% |
| 表头 (`headers`) | 20% |
| 上下文文本 | 15% |
| 数据行首列 | 30% |

最低匹配阈值 0.15。查询中使用 `|` 分割多个关键词时，取各关键词的最高匹配分。

## 结果格式

`results/answers.json` 结构：

```json
{
  "meta": {
    "total_questions": 20,
    "total_prompt_tokens": 3512659,
    "total_completion_tokens": 20,
    "total_tokens": 3512679
  },
  "results": [
    {
      "qid": "fin_a_001",
      "answer": "AB",
      "domain": "financial_reports",
      "question": "根据比亚迪连续两年的年度报告...",
      "status": "RESOLVED",
      "answer_format": "multi",
      "options_detail": {
        "A": { "judgment": "TRUE", "reason": "...", "evidence": "T_02828 / 营业收入合计 / 2025年 / 803,964,958,000.00" },
        "B": { "judgment": "TRUE", "reason": "...", "evidence": "T_02823 / 归属于上市公司股东的净利润 / 2025 年 / 32,619,022,000.00" },
        "C": { "judgment": "FALSE", "reason": "...", "evidence": "T_02840 / ..." },
        "D": { "judgment": "FALSE", "reason": "...", "evidence": "T_02515, T_02839" }
      },
      "token_usage": { "prompt_tokens": 276977, "completion_tokens": 1, "total": 276978 },
      "llm_model": "qwen-plus-latest",
      "log_summary": ["-- A (6 rounds, 63368 tokens) --", "..."],
      "options_processed": 4
    },
    {
      "qid": "summary",
      "answers": {
        "fin_a_001": "AB",
        "fin_a_002": "ABD",
        "...": "..."
      },
      "prompt_tokens": 3512659,
      "completion_tokens": 20,
      "total_tokens": 3512679
    }
  ]
}
```

**answer 字段规则：**

| 题型 | answer 示例 | 说明 |
|------|-----------|------|
| multi（多选） | `"ABD"` | TRUE 的选项拼接 |
| tf（判断） | `"A"` / `"B"` | A=正确（TRUE）, B=错误（FALSE） |
| mcq（单选） | `"D"` | 唯一 TRUE 的选项 |
| 全部 VAGUE | `"?"` | 无 TRUE 选项 |

**token 统计规则：**
- `prompt_tokens`: 仅统计 API 返回的实际 prompt tokens（不含任何启发式估算）
- `completion_tokens`: 每题固定为 1（代表最终答案 token）
- `total_tokens`: prompt + completion 之和

## 配置

### LLM 配置

默认配置在 `agent/llm_reasoner.py` 中，可通过环境变量覆盖：

| 环境变量 | 默认值 | 说明 |
|---------|-------|------|
| `LLM_API_KEY` | （空，需配置） | DashScope API Key |
| `LLM_API_BASE` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | API 地址 |
| `LLM_MODEL` | `qwen-plus-latest` | 模型名称 |
| `LLM_TEMPERATURE` | `0.0` | 确定性输出 |
| `LLM_MAX_TOKENS` | `2048` | 单次调用最大 Token |

### ReACT 参数

在 `agent/react_loop.py` 中：

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `MAX_ROUNDS` | `6` | 每个选项的最大思考轮数 |

### 检索参数

在 `retriever.py` 中：

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `MIN_SCORE` | `0.15` | 模糊匹配最低阈值 |

## 重建索引

当原始文档更新后，重新生成检索索引：

```bash
python3 build_indices.py
```

该命令会扫描 `public_dataset_upload/extracted/` 下所有 `.md` 文件，生成：
- 标题层级索引
- 表格内容索引
- 文档注册表

`heading_index.json` 文件约 188 MB，已加入 `.gitignore`，不在仓库中存储。