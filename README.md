# AFAC Q4 — Financial QA ReACT Agent

基于 ReACT（Think → Act → Observe）架构的金融知识问答代理。通过多层级检索（标题、表格、段落文本）从已解析的财报、保险、监管文档中提取数据，由 LLM 驱动推理并回答问题。

## 项目结构

```
├── agent.py                  # 入口：加载问题 → 运行 ReACT → 输出结果
├── debugger.py               # 透明调试器：逐步展示 ReACT 循环（LLM ↔ 工具交互）
├── retriever.py              # 向后兼容门面（所有实现已迁移至 agent/tools/）
├── indexer.py                # 索引构建器（解析 Markdown 文档 → 生成索引 JSON）
├── build_indices.py          # 一键重建所有检索索引
├── table_extractor.py        # PDF 表格提取
├── run_mineru_extraction.py  # MinerU 批量文档解析
├── agent/
│   ├── __init__.py           # 顶层导出
│   ├── react_loop.py         # ReACT 调度器（75 行，按题型路由）
│   ├── llm_reasoner.py       # LLM 调用封装（DashScope Qwen）+ Think / Judge prompt
│   ├── tools.py              # 向后兼容 shim（从 agent.tools 重导出）
│   ├── question_loader.py    # 问题 JSON 加载 + 文档可用性检查
│   ├── context/              # 题型求解策略（每种题型独立）
│   │   ├── _common.py        # 共享 ReACT 循环引擎 + 工具函数
│   │   ├── batch.py          # 多选批量模式（共享检索，最多 9 轮）
│   │   ├── per_option.py     # 多选逐选项模式（最多 6 轮）
│   │   └── tf.py             # 判断题模式（A/B 逻辑对立面）
│   └── tools/                # 检索 + 计算工具（.py 实现 + .md 提示卡）
│       ├── __init__.py       # 工具注册表 + execute_tool()
│       ├── _loader.py        # 共享索引加载器
│       ├── _shared.py        # 共享辅助函数
│       ├── _unit_parser.py   # 单位感知算术引擎
│       ├── search_headings.py / .md
│       ├── search_tables.py / .md
│       ├── search_text.py / .md
│       ├── get_section.py / .md
│       ├── compute.py / .md
│       ├── expand_query.py
│       └── get_doc_info.py
├── config/
│   └── financial_terms.json
├── indices/
│   ├── doc_registry.json
│   ├── table_index.json
│   └── heading_index.json
├── utils/
│   └── text_utils.py
├── public_dataset_upload/
│   ├── questions/group_a/
│   └── extracted/
└── results/
    └── answers.json
```

## 快速开始

### 1. 环境配置

```bash
pip install requests
```

### 2. 设置 API Key

通过 `.env` 文件：
```bash
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

或设置环境变量：
```bash
export LLM_API_KEY="sk-your-dashscope-api-key"
export LLM_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_MODEL="qwen-plus-latest"
```

### 3. 重建索引

```bash
python3 build_indices.py
```

### 4. 运行问答

**调试器（推荐）：**
```bash
python3 debugger.py --qid fc_a_001 --mode batch
```

**批量运行：**
```bash
python3 agent.py -q public_dataset_upload/questions/group_a/ --verbose
```

## 架构

### ReACT 循环

```
Round 0: 检查可用文档
Round 1–9 (batch) / 1–6 (per-option):
  THINK   → LLM 决定调用哪些工具，可输出部分判断
  ACT     → 执行工具调用
  OBSERVE → 汇总结果，已解决选项自动剪枝
```

### 工具列表

| # | 工具 | 用途 |
|---|------|------|
| 1 | search_headings | 按关键词搜索文档标题 |
| 2 | search_tables | 表格搜索（关键词/ID/标题） |
| 3 | search_text | 搜索文档原始段落文本 |
| 4 | get_section | 获取标题下完整文本 + 表格 |
| 5 | compute | 单位感知算术计算器 |

### keep dict 格式

```json
{"keep": {"A": ["R1","R2"], "D": ["R6","R7"]}, "judgment": "A:TRUE|D:TRUE", "actions": [...]}
```

已解决的选项（TRUE/FALSE）及其标签将从未来上下文自动剪枝。

## 配置

| 环境变量 | 默认值 | 说明 |
|---------|-------|------|
| LLM_API_KEY | 需配置 | DashScope API Key |
| LLM_MODEL | qwen-plus-latest | 模型名称 |
| LLM_TEMPERATURE | 0.0 | 确定性输出 |

ReACT 参数在 `agent/context/_common.py`：`MAX_ROUNDS=6`, `BATCH_MAX_ROUNDS=9`。

## 重建索引

```bash
python3 build_indices.py
```
