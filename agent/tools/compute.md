# compute

Evaluate arithmetic with unit-aware numbers. Supports Chinese units (万亿/亿/万/千/百/元/万元/千元/百万元/亿元/万亿元/千万), English units (M/K/B), and percentage (%). Always return ground-truth numbers — do NOT manually recalculate.

**Parameters:**
- `expression` (str, required): Arithmetic expression with unit-aware numbers, e.g. `"(32,619,022千元 - 40,254,346万元) / 345百万 * 100"`
- `output_unit` (str, optional): Format result as `千`/`万`/`亿`/`%` etc. Omit for raw number.

**Returns:** `{"result": <float>, "unit": "<output_unit>", "formatted": "<value><unit>"}` or `{"error": "..."}`

**When to use:**
- Growth rate: `compute("(new - old) / old", output_unit="%")`
- Unit conversion: `compute("133,219,982千元", output_unit="亿")`
- Sum comparison: `compute("A + B")`
- Ratio: `compute("part / whole", output_unit="%")`
- Cross-unit compare: `compute("1,050,187百万 > 423,701,834千元 * 2")`

**Examples:**
```json
{"tool": "compute", "params": {"expression": "(500亿元 + 300亿元) / 2", "output_unit": "亿"}}
```
```json
{"tool": "compute", "params": {"expression": "(1,050,187百万 - 423,701,834千元) / 1,050,187百万", "output_unit": "%"}}