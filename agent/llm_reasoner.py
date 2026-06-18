"""
LLM Reasoner — calls DashScope API (qwen) for:
  1. ReACT THINK steps (decide next tool + params)
  2. Final judgment of options (TRUE/FALSE/VAGUE)
"""

import json
import os
import re
import requests

from agent.question_loader import estimate_tokens

# ── Load .env file ──
def _load_dotenv(path: str = ".env"):
    """Load key=value pairs from a .env file into os.environ (simple, no dependencies)."""
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip()
            if key and val and key not in os.environ:
                os.environ[key] = val

_load_dotenv()

# ── Default config ──
DEFAULT_CONFIG = {
    "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": "",
    "model": "qwen-plus-latest",
    "temperature": 0.0,
    "max_tokens": 2048,
}


def get_llm_config():
    """Get LLM configuration from environment (loaded from .env or system env)."""
    return {
        "api_base": os.environ.get("LLM_API_BASE", DEFAULT_CONFIG["api_base"]),
        "api_key": os.environ.get("LLM_API_KEY", os.environ.get("OPENAI_API_KEY", DEFAULT_CONFIG["api_key"])),
        "model": os.environ.get("LLM_MODEL", DEFAULT_CONFIG["model"]),
        "temperature": float(os.environ.get("LLM_TEMPERATURE", str(DEFAULT_CONFIG["temperature"]))),
        "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", str(DEFAULT_CONFIG["max_tokens"]))),
    }


def call_llm(messages: list[dict], config: dict | None = None) -> dict:
    """
    Call an OpenAI-compatible LLM API.
    Returns {"content": str, "usage": dict} or {"error": str}
    """
    if config is None:
        config = get_llm_config()

    api_key = config.get("api_key", "")
    if not api_key:
        return {"error": "No API key configured"}

    url = f"{config['api_base'].rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": config["model"],
        "messages": messages,
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"],
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        # Debug: log raw LLM responses
        import datetime
        with open("/tmp/llm_debug.log", "a", encoding="utf-8") as df:
            df.write(f"\n=== {datetime.datetime.now()} ===\n")
            df.write(f"Response:\n{content}\n")
            df.write(f"Usage: {result.get('usage', {})}\n")
        return {
            "content": content,
            "usage": result.get("usage", {}),
            "error": None,
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}", "content": "", "usage": {}}
    except (KeyError, IndexError) as e:
        return {"error": f"Unexpected response: {e}", "content": "", "usage": {}}


def parse_json_from_response(content: str) -> dict:
    """Extract JSON object from LLM response (may be wrapped in markdown)."""
    # Try direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Try extracting from markdown code block
    m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # Try finding any JSON object
    m = re.search(r'\{[\s\S]*\}', content)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"error": "No JSON found", "raw": content[:500]}


# ── ReACT THINK prompt ──

TOOLS_DESC = """
Available tools (use | to separate multiple keywords, e.g. "利润|资产|负债"):

1. search_headings(query, doc=None, domain=None) — Search section headings by keyword.
2. search_tables(query=None, doc=None, domain=None, table_id=None, heading_title=None) — Unified table access:
   • keyword search: set query (use | for multi-keyword), optional doc/domain
   • by ID: set table_id="T_02828"
   • under heading: set doc + heading_title
3. search_text(doc, query) — Search RAW TEXT (not tables) in a doc. doc is REQUIRED.
4. get_section(doc, heading_path) — Get FULL text + ALL tables under a heading.
5. compute(expression) — Evaluate arithmetic with unit-aware numbers. Supports 万亿/亿/万/千/百/元/M/K/B/%.
   The result is ground truth — do NOT question or re-compute it.
6. get_doc_info(rel_path) — Get document metadata.
"""


def build_think_prompt(question: dict, doc_status: dict, round_log: list[dict], round_num: int) -> list[dict]:
    """Build the messages for the THINK step."""
    options = question.get("options", {})

    # Summarize what we've observed so far
    obs_summary = ""
    for r in round_log:
        phase = r.get("phase", "")
        # For OBSERVE phases, use the full data (tables etc) not truncated text
        if phase == "OBSERVE" and r.get("data"):
            obs_data = r["data"]
            # For data-heavy observations (including multi_action), include table previews
            if obs_data.get("type") in ("section", "tables", "multi_action"):
                text = json.dumps(obs_data, ensure_ascii=False)[:8000]
            else:
                text = json.dumps(obs_data, ensure_ascii=False)[:2000]
        else:
            text = r.get("text", "")[:1000]
        obs_summary += f"[{phase}] {text}\n"

    system = f"""You are a ReACT agent that retrieves financial data from documents to answer questions.

{TOOLS_DESC}

You must respond with a JSON object. You can request MULTIPLE tools in one round — they will run in parallel.

Format when you need more data:
{{"actions": [{{"tool": "search_tables", "params": {{"doc": "text10", "query": "力诺投资|资产负债率"}}}}, {{"tool": "search_text", "params": {{"doc": "text10", "query": "力诺投资|资产负债率"}}}}], "keep": ["R1", "R3"], "reasoning": "I need both table data and raw text from text10. R2 is irrelevant."}}

Format when you are CONFIDENT and ready to judge (any round):
{{"actions": [], "keep": ["R1", "R4", "R8"], "reasoning": "brief explain", "judgment": "TRUE|FALSE|VAGUE", "evidence": "table ID / row / data"}}

IMPORTANT RULES:

1. MANDATORY TOOLS:
   - EVERY observation must include "keep" listing relevant labels (e.g. "keep": ["R1","R3"]).
     Irrelevant clues clutter context and cause wrong answers.
   - EVERY numerical calculation MUST call compute(). Never do arithmetic in your head —
     you WILL make errors with unit conversion, decimal placement, and percentages.
   - Examples that REQUIRE compute():
     * Growth rate: compute("(new - old) / old", output_unit="%")
     * Unit conversion: compute("133,219,982千元", output_unit="亿")
     * Sum comparison: compute("A + B")
     * Ratio: compute("part / whole", output_unit="%")
     * Cross-unit compare: compute("1,050,187百万 > 423,701,834千元 * 2")

2. JUDGMENT RULES:
   - TRUE = data clearly supports the claim. FALSE = data clearly contradicts. VAGUE = insufficient.
   - Do NOT judge unless confident. Round 6: you MUST judge even if uncertain, use VAGUE.
   - Match document claims to question claims semantically, not literally.

3. TOOL PREFERENCE:
   - Rounds 1–3: search_headings, search_text, search_tables (low cost)
   - Rounds 4+: get_section allowed (high cost, use only when needed)
   - Never judge based on heading titles alone — always read the actual data.

4. FORMAT:
   - Use Chinese keywords. Use | to separate.
   - Do NOT include any text outside the JSON."""

    user = f"""Question: {question.get('question', '')}

Options to evaluate:
{json.dumps(options, ensure_ascii=False, indent=2)}

Document status:
{doc_status}

Previous rounds:
{obs_summary if obs_summary else '(First round — no observations yet)'}

Round {round_num}: Based on the observations above, what tool should I use next? Or should I stop and answer?
Return ONLY JSON."""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def llm_think(question: dict, doc_status: dict, round_log: list[dict], round_num: int, config: dict | None = None) -> dict:
    """
    LLM-driven THINK step. Returns a plan dict with "tool" and "params".
    """
    if config is None:
        config = get_llm_config()

    messages = build_think_prompt(question, doc_status, round_log, round_num)
    result = call_llm(messages, config)

    if result.get("error"):
        # Fallback: use basic heuristic
        all_text = question.get("question", "") + " " + " ".join(question.get("options", {}).values())
        terms = re.findall(r'[\u4e00-\u9fff]{2,}', all_text)
        query = " ".join(list(dict.fromkeys(terms))[:8])
        return {
            "tool": "search_headings",
            "params": {"query": query, "domain": question.get("domain", ""), "max_results": 10},
            "reasoning": f"LLM error, fallback to heading search: {result['error']}",
            "llm_error": result["error"],
        }

    parsed = parse_json_from_response(result["content"])
    if parsed.get("error"):
        return {
            "tool": "search_headings",
            "params": {"query": question.get("question", "")[:80], "domain": question.get("domain", ""), "max_results": 10},
            "reasoning": f"LLM JSON parse failed, fallback",
            "llm_raw": result["content"][:200],
        }

    response = {
        "reasoning": parsed.get("reasoning", ""),
        "llm_usage": result.get("usage", {}),
    }
    # New format: {"actions": [...], "reasoning": "..."}
    if "actions" in parsed:
        response["actions"] = parsed["actions"]
    else:
        # Legacy format: {"tool": "...", "params": {...}, "reasoning": "..."}
        response["tool"] = parsed.get("tool", "done")
        response["params"] = parsed.get("params", {})
    # Propagate judgment, evidence, and keep if the LLM provided them
    if "judgment" in parsed:
        response["judgment"] = parsed["judgment"]
    if "evidence" in parsed:
        response["evidence"] = parsed["evidence"]
    if "keep" in parsed:
        response["keep"] = parsed["keep"]
    return response


# ── Final judgment prompt ──

def build_judgment_prompt(context: str, question: dict) -> list[dict]:
    """Build prompt for final TRUE/FALSE/VAGUE judgment."""
    options = question.get("options", {})
    system = """You are a precise financial document analyst. Judge each option based ONLY on the provided context.

TRUE = context clearly supports the claim with specific data.
FALSE = context clearly contradicts the claim with specific data.
VAGUE = insufficient data, missing documents, or ambiguous evidence.

Return ONLY a JSON object (no other text):
{"options": {"A": {"judgment": "TRUE|FALSE|VAGUE", "reason": "brief reason", "evidence": "table ID / row / value"}}}"""

    user = f"QUESTION: {question.get('question', '')}\n\nOPTIONS:\n{json.dumps(options, ensure_ascii=False, indent=2)}\n\nCONTEXT:\n{context}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def reason_on_context(context: str, question: dict, config: dict | None = None) -> dict:
    """Final LLM reasoning on gathered context."""
    if config is None:
        config = get_llm_config()

    messages = build_judgment_prompt(context, question)
    result = call_llm(messages, config)

    if result.get("error"):
        options = question.get("options", {})
        return {
            "options_detail": {k: {"judgment": "VAGUE", "reason": f"LLM error: {result['error']}", "evidence": ""}
                              for k in options},
            "llm_prompt_tokens": 0, "llm_completion_tokens": 0,
            "llm_api_usage": {}, "llm_model": config["model"], "llm_error": result["error"],
        }

    parsed = parse_json_from_response(result["content"])
    usage = result.get("usage", {})

    options = question.get("options", {})
    llm_options = parsed.get("options", {}) if not parsed.get("error") else {}

    options_detail = {}
    for key in sorted(options.keys()):
        opt = llm_options.get(key, {})
        options_detail[key] = {
            "judgment": opt.get("judgment", "VAGUE"),
            "reason": opt.get("reason", "Unable to determine from context"),
            "evidence": opt.get("evidence", ""),
        }

    return {
        "options_detail": options_detail,
        "llm_prompt_tokens": usage.get("prompt_tokens", 0),
        "llm_completion_tokens": usage.get("completion_tokens", 0),
        "llm_api_usage": usage,
        "llm_model": config["model"],
    }