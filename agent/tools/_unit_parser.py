"""
Unit-aware numeric parsing for Chinese/English financial numbers.
Supports: 万亿/亿/万/千/百/元/万元/千元/百万元/亿元/万亿元/千万 + M/K/B/%.
Also handles negative-in-parentheses and comma-separated thousands.
"""

import re

# Map of Chinese/English unit suffixes → multiplier
# Ordered: compound suffixes BEFORE their shorter components (longest match first)
_UNIT_SUFFIXES = [
    (r'万亿元', 1_000_000_000_000),    # compound: must precede 万亿/亿/万
    (r'万亿', 1_000_000_000_000),
    (r'亿元', 100_000_000),            # compound: must precede 亿
    (r'亿', 100_000_000),
    (r'千万', 10_000_000),
    (r'百万元', 1_000_000),           # compound: must precede 百万/万元
    (r'百万', 1_000_000),
    (r'万元', 10_000),                # compound: must precede 万
    (r'万', 10_000),
    (r'千元', 1_000),                 # compound: must precede 千
    (r'千', 1_000),
    (r'百', 100),
    (r'百元', 100),
    (r'元', 1),                       # bare 元 (note: not 元/股 after regex tokenizes)
    (r'\bB\b', 1_000_000_000),        # billion
    (r'\bM\b', 1_000_000),            # million
    (r'\bK\b', 1_000),                # thousand
    (r'%', 0.01),
]

# Regex pattern for value tokens: digits, optional commas/decimals, then a unit suffix
_VALUE_PAT = re.compile(
    r'\d[\d,，.]*\s*(?:万亿元|万亿|亿元|千万|百万元|百万|万元|千元|万|千|百|亿|元|M|K|B|%)\b'
)

# Regex for negative numbers in parentheses: (1,234.56)
_PAREN_PAT = re.compile(r'\([\d,，.]+\)')


def _parse_value_with_unit(token):
    """
    Parse a human-readable number into a float.
    Handles: commas, negative in (), Chinese units (万亿/亿/万/千/百/元), M/K/B, %.
    Examples:
        "32,619,022千元" → 32619022000.0
        "(1,234)" → -1234.0
        "6.97%" → 0.0697
        "23.5M" → 23500000.0
    """
    s = token.strip()
    # Handle negative in parentheses: (1,234,456)
    if s.startswith('(') and s.endswith(')'):
        s = '-' + s[1:-1]
    # Remove commas
    s = s.replace(',', '').replace('，', '')

    # Try: suffix match
    for suffix_pat, multiplier in _UNIT_SUFFIXES:
        m = re.search(suffix_pat, s)
        if m:
            # Remove the suffix and trailing characters after it
            num_part = s[:m.start()].strip()
            if num_part.startswith('-'):
                sign = -1
                num_part = num_part[1:]
            else:
                sign = 1
            try:
                return sign * float(num_part) * multiplier
            except ValueError:
                pass

    # No suffix matched: try plain float
    try:
        return float(s)
    except ValueError:
        pass
    return None


def _format_result(value, output_unit):
    """Format a raw numeric result into the requested unit."""
    if output_unit is None:
        return {"result": round(value, 6) if isinstance(value, float) else value}

    unit_map = {
        '万亿': 1_000_000_000_000, '亿': 100_000_000, '亿元': 100_000_000,
        '千万': 10_000_000, '百万': 1_000_000, '百万元': 1_000_000,
        '万': 10_000, '万元': 10_000,
        '千': 1_000, '千元': 1_000, '百': 100,
        '%': 100,  # multiply by 100 for percentage display
    }
    multiplier = unit_map.get(output_unit)
    if multiplier is None:
        # For % we need special handling — it's already a ratio, just *100
        return {"result": round(value, 6)}

    converted = value / multiplier if output_unit != '%' else value * 100
    return {
        "result": round(converted, 6),
        "unit": output_unit,
        "formatted": f"{round(converted, 4)}{output_unit}",
    }


def evaluate_expression(expr, output_unit=None):
    """Replace unit-aware tokens with their numeric values, then eval.

    Args:
        expr: str — e.g. '(32,619,022千元 - 40,254,346万元) / 345百万 * 100'
        output_unit: str|None — format result as 千/万/亿/% etc. (omit for raw number)

    Returns:
        dict with "result" (and optionally "unit", "formatted"), or {"error": ...}
    """

    def _replace_callback(m):
        token = m.group(0)
        val = _parse_value_with_unit(token)
        return str(val) if val is not None else token

    resolved = _VALUE_PAT.sub(_replace_callback, expr)

    # Handle negatives in parentheses: (1,234.56) → -1234.56
    resolved = _PAREN_PAT.sub(_replace_callback, resolved)

    # Strip commas from plain numbers (not yet converted by unit suffix)
    resolved = re.sub(r'(?<=\d),(?=\d)', '', resolved)
    resolved = re.sub(r'(?<=\d)，(?=\d)', '', resolved)

    # Safety: allow only digits, +-*/(). and whitespace
    if not re.match(r'^[\d+\-*/().\s]+$', resolved):
        return {"error": f"Expression has unsafe characters after resolving: {resolved[:100]}"}

    try:
        result = eval(resolved)
        return _format_result(result, output_unit)
    except Exception as e:
        return {"error": f"Evaluation failed: {e}"}