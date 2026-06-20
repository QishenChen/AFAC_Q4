"""compute — Unit-aware arithmetic calculator.
Wraps the _unit_parser.evaluate_expression.
Supports 万亿/亿/万/千/百/元/万元/千元/百万元/亿元/万亿元/千万 + M/K/B/%.
"""

from agent.tools._unit_parser import evaluate_expression


def compute(expression: str, output_unit: str | None = None):
    """Evaluate arithmetic with unit-aware numbers.
    
    Args:
        expression: str — e.g. '(32,619,022千元 - 40,254,346万元) / 345百万 * 100'
        output_unit: str|None — format result as 千/万/亿/% etc. (omit for raw number)
    
    Returns:
        dict with "result" (and optionally "unit", "formatted"), or {"error": ...}
    """
    return evaluate_expression(expression, output_unit)