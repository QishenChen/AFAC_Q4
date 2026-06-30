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


import time

def call_llm(messages: list[dict], config: dict | None = None, max_retries: int = 2,
             log_qid: str = "", round_num: int = 0) -> dict:
    """
    Call an OpenAI-compatible LLM API with retry on transient failures.
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
        "thinking": {"type": "disabled"},
    }

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=(10, 15))
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]
            # Debug: log raw LLM responses per question
            import datetime
            if log_qid:
                os.makedirs("results/raw_responses", exist_ok=True)
                with open(f"results/raw_responses/{log_qid}.txt", "a", encoding="utf-8") as df:
                    df.write(f"\n=== Round {round_num} {datetime.datetime.now()} ===\n")
                    df.write(f"MESSAGES:\n{json.dumps(messages, ensure_ascii=False, indent=2)[:8000]}\n")
                    df.write(f"RESPONSE:\n{content}\n")
                    df.write(f"Usage: {result.get('usage', {})}\n")
            else:
                with open("/tmp/llm_debug.log", "a", encoding="utf-8") as df:
                    df.write(f"\n=== {datetime.datetime.now()} ===\n")
                    df.write(f"Response:\n{content}\n")
                    df.write(f"Usage: {result.get('usage', {})}\n")
            return {
                "content": content,
                "usage": result.get("usage", {}),
                "error": None,
            }
        except requests.exceptions.Timeout:
            last_error = f"API timeout (attempt {attempt + 1}/{max_retries + 1})"
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 0
            if status_code in (429, 503) and attempt < max_retries:
                last_error = f"HTTP {status_code} (attempt {attempt + 1}/{max_retries + 1})"
                time.sleep(2 ** attempt * 2)
            else:
                return {"error": f"HTTP {status_code}: {e}", "content": "", "usage": {}}
        except requests.exceptions.RequestException as e:
            last_error = f"Request failed: {e}"
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except (KeyError, IndexError) as e:
            return {"error": f"Unexpected response: {e}", "content": "", "usage": {}}

    return {"error": last_error or "API request failed after retries", "content": "", "usage": {}}


def parse_json_from_response(content: str) -> dict:
    """Extract JSON object from LLM response (may be wrapped in markdown or have trailing text)."""
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

from agent.tools import build_tools_prompt


def build_think_prompt(question: dict, doc_status: dict, round_log: list[dict], round_num: int, max_rounds: int = 6) -> list[dict]:
    """Build the messages for the THINK step."""
    options = question.get("options", {})
    domain = question.get("domain", "")
    tools_desc = build_tools_prompt(domain)

    # Summarize what we've observed so far
    obs_summary = ""
    search_history_parts = []
    for r in round_log:
        phase = r.get("phase", "")
        # For OBSERVE phases, use the full data (tables etc) not truncated text
        if phase == "OBSERVE" and r.get("data"):
            obs_data = r["data"]
            # For data-heavy observations (including multi_action), include table previews
            if obs_data.get("type") == "all_headings":
                text = json.dumps(obs_data, ensure_ascii=False)[:6000]
            elif obs_data.get("type") in ("section", "tables", "multi_action"):
                text = json.dumps(obs_data, ensure_ascii=False)[:3000]
            else:
                text = json.dumps(obs_data, ensure_ascii=False)[:1000]
        else:
            text = r.get("text", "")[:1000]
        obs_summary += f"[{phase}] {text}\n"
        # Collect ACT entries for search history
        if phase == "ACT":
            search_history_parts.append(r.get("text", "")[:200])

    search_history = "\n".join(search_history_parts) if search_history_parts else "(None yet)"

    # Dynamic judgment format based on number of options
    if len(options) > 1:
        judge_format_example = '"judgment": "A:TRUE|B:FALSE"'
    else:
        judge_format_example = '"judgment": "TRUE"'

    # Build the judge format example (strip outer quotes for display)
    _jfe = judge_format_example.replace('"judgment": ', '').strip('"')
    system = f"""You are a ReACT agent that retrieves financial data from documents to answer questions.

{tools_desc}

Respond with JSON: {{"actions": [...], "keep": {{"A": ["R1"], "B": ["R3"]}}, "reasoning": {{"A": "{{R1}} reveals ...", "B": "{{R3}} reveals ..."}}, "judgment": "{_jfe}"}}
(Remove "judgment" field when not ready to judge any option)

- "reasoning" (REQUIRED): Per-option breakdown. One entry per option still under investigation.
  Remove entries for options already judged.
  Write compactly by citing clues inline, e.g. "{{R1}} reveals X; {{R3}} reveals Y; therefore A is TRUE."
  Do not repeat the full evidence text — reference the label and state the inferred fact.
- "keep" (REQUIRED): Dict mapping option→labels. Example: {{"A": ["R1","R2"], "B": ["R3"]}}
  IMPORTANT: "keep" may contain at most 5 clue labels total across all options. Keep ONLY the most important / decisive clues; drop weaker ones.
- "judgment" (OPTIONAL): Include TRUE/FALSE for options you are confident about. Skip unsure ones.
  Example: "A:TRUE|D:TRUE" = A and D resolved, B and C still investigating.
  Include judgment AS SOON AS you are confident — do NOT wait for all options.
  When judgment covers ALL options, set actions=[] to stop.
- Use compute() for ALL numeric calculations. Never do arithmetic in your head.

RULES:
- TRUE = data clearly supports. FALSE = data clearly contradicts.
- When confident, include judgment IMMEDIATELY — do not wait.
- If a search returns no results, paraphrase and retry with different keywords. Never give up after one attempt.
  Never mark an option FALSE due to missing data — FALSE only when documents explicitly contradict the claim.
  If data remains absent after thorough search, simply omit judgment for that option.
- Search for both explicit and implicit indicators. A fact may be implied through regulatory references,
  compliance language, or contextual clues without being stated verbatim.
- Only set actions=[] when ALL options judged. {max_rounds} rounds total.
- Rounds 1–({max_rounds//2}): search_headings, search_text, search_tables. Rounds {max_rounds//2 + 1}+: get_section allowed.
- Issue SEPARATE search actions per option — do NOT use one generic query for all options.
- Keep queries to 2–3 keywords maximum. More keywords dilute results and match noise.
  If results are irrelevant, drop keywords and retry with fewer or different terms — not more.
  Use only core nouns, numbers, and key verbs. Strip all filler words and redundant modifiers.
- For search_headings, use diverse loosely-related keywords to cover more possible areas.
  Do not restrict searches to the option's exact terms — think about what topic areas
  could contain relevant information.
- When using search_tables, you can either (a) search by keywords to discover relevant tables, or
  (b) target a specific table by table_id or heading_title if you already know which one contains the
  information. In either case, inspect the returned table data and extract the exact value
  before judging 
- You may issue multiple searches in a single round to exhaust all promising angles. Use as many
  parallel actions as needed within the round limit, especially when earlier searches were inconclusive.
  Use Chinese keywords by default. Use | separator. No text outside JSON."""

    user = f"""Question: {question.get('question', '')}

Options to evaluate:
{json.dumps(options, ensure_ascii=False, indent=2)}

Document status:
{doc_status}

Searches already performed:
{search_history}

Previous rounds:
{obs_summary if obs_summary else '(First round — no observations yet)'}

Round {round_num}/{max_rounds}: Based on the observations above, what tool should you use next? Or should you stop and answer?
Return ONLY JSON."""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def llm_think(question: dict, doc_status: dict, round_log: list[dict], round_num: int, config: dict | None = None, max_rounds: int = 6, log_qid: str = "") -> dict:
    """
    LLM-driven THINK step. Returns a plan dict with "tool" and "params".
    """
    if config is None:
        config = get_llm_config()

    messages = build_think_prompt(question, doc_status, round_log, round_num, max_rounds=max_rounds)
    result = call_llm(messages, config, log_qid=log_qid or question.get("qid", ""), round_num=round_num)

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
            "llm_usage": result.get("usage", {}),
        }

    parsed = parse_json_from_response(result["content"])
    if parsed.get("error"):
        # Better fallback: extract keywords from options text, use | separator
        all_text = " ".join(question.get("options", {}).values())
        terms = re.findall(r'[\u4e00-\u9fff]{2,}', all_text)
        query = "|".join(list(dict.fromkeys(terms))[:8]) or question.get("question", "")[:80]
        return {
            "tool": "search_headings",
            "params": {"query": query, "domain": question.get("domain", ""), "max_results": 10},
            "reasoning": f"LLM JSON parse failed, keyword fallback from options",
            "llm_raw": result["content"][:200],
            "llm_usage": result.get("usage", {}),
        }

    return _build_think_response(result, parsed)


def _build_think_response(result: dict, parsed: dict) -> dict:
    """Build response dict from parsed JSON, preserving usage whether success or fallback."""
    usage = result.get("usage", {})
    response = {
        "reasoning": parsed.get("reasoning", ""),
        "llm_usage": usage,
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