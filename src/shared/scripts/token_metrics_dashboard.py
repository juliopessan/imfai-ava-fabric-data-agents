#!/usr/bin/env python3
"""
Token Metrics Dashboard — renders OBSERVED token, compression and cost metrics.

Reads the metrics interfaces that already exist in the repository:
- ``ExecutionTelemetry.generate_report()`` (execution_telemetry.py): input/output tokens
- ``CompressionStats`` (headroom_context_manager.py): compression input/output/ratio/method

Nothing is invented: a metric without an observed value is rendered as
"Indisponível", and a run without any metric renders an empty state with no
savings value. See docs/observability/TOKEN-METRICS-DASHBOARD.md.

Usage:
    python -m src.shared.scripts.token_metrics_dashboard --input runs.json --output dashboard.html
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

UNAVAILABLE = "Indisponível"
EMPTY_MESSAGE = "Sem métricas observadas para esta execução."

# Tokens per price unit. The unit of every price must be stated explicitly.
PRICE_UNITS: Dict[str, int] = {
    "per_1k_tokens": 1_000,
    "per_1m_tokens": 1_000_000,
}
PRICE_UNIT_LABELS: Dict[str, str] = {
    "per_1k_tokens": "USD / 1K tokens",
    "per_1m_tokens": "USD / 1M tokens",
}


@dataclass(frozen=True)
class ModelPrice:
    """Registered price of a model, with the unit it is expressed in."""

    input_price: float
    output_price: float
    unit: str = "per_1m_tokens"

    def __post_init__(self) -> None:
        if self.unit not in PRICE_UNITS:
            raise ValueError(f"Unknown price unit: {self.unit!r}")


# Only prices already registered in the repository
# (ExecutionTelemetry: Claude Haiku $0.80 / $2.40 per 1M tokens).
DEFAULT_PRICE_TABLE: Dict[str, ModelPrice] = {
    "claude-haiku": ModelPrice(0.80, 2.40, "per_1m_tokens"),
}


@dataclass(frozen=True)
class CompressionMetrics:
    """Observed compression of one handoff (mirrors CompressionStats)."""

    input_tokens: int
    output_tokens: int
    compression_ratio: float
    method: str = "unknown"

    @property
    def tokens_saved(self) -> int:
        return self.input_tokens - self.output_tokens


@dataclass(frozen=True)
class RunMetrics:
    """Metrics observed for one execution. ``None`` means no observed value."""

    run_id: str
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    compression: Optional[CompressionMetrics] = None

    @property
    def has_metrics(self) -> bool:
        return (
            self.input_tokens is not None
            or self.output_tokens is not None
            or self.compression is not None
        )


@dataclass(frozen=True)
class CostResult:
    amount_usd: float
    unit: str  # key of PRICE_UNITS the price table used


def compression_from_stats(stats: Any) -> CompressionMetrics:
    """Build from a ``CompressionStats`` instance or its ``to_dict()``."""
    get = stats.get if isinstance(stats, Mapping) else lambda k, d=None: getattr(stats, k, d)
    return CompressionMetrics(
        input_tokens=int(get("input_tokens")),
        output_tokens=int(get("output_tokens")),
        compression_ratio=float(get("compression_ratio")),
        method=str(get("method", "unknown")),
    )


def run_from_telemetry_report(
    run_id: str,
    report: Mapping[str, Any],
    model: Optional[str] = None,
    compression: Any = None,
) -> RunMetrics:
    """Build from ``ExecutionTelemetry.generate_report()`` (+ optional CompressionStats)."""
    metrics = report.get("metrics") or {}
    return RunMetrics(
        run_id=run_id,
        model=model,
        input_tokens=metrics.get("input_tokens"),
        output_tokens=metrics.get("output_tokens"),
        compression=compression_from_stats(compression) if compression is not None else None,
    )


def run_from_dict(data: Mapping[str, Any]) -> RunMetrics:
    """Build from a plain dict (JSON input); absent keys stay unavailable."""
    compression = data.get("compression")
    return RunMetrics(
        run_id=str(data.get("run_id", "run")),
        model=data.get("model"),
        input_tokens=data.get("input_tokens"),
        output_tokens=data.get("output_tokens"),
        compression=compression_from_stats(compression) if compression else None,
    )


def calculate_cost(
    model: Optional[str],
    input_tokens: Optional[int],
    output_tokens: Optional[int],
    price_table: Optional[Mapping[str, ModelPrice]] = None,
) -> Optional[CostResult]:
    """Cost of the observed tokens, or ``None`` when model/price/tokens are missing."""
    table = DEFAULT_PRICE_TABLE if price_table is None else price_table
    price = table.get(model) if model else None
    if price is None or input_tokens is None or output_tokens is None:
        return None
    per = PRICE_UNITS[price.unit]
    amount = (input_tokens / per) * price.input_price + (output_tokens / per) * price.output_price
    return CostResult(amount_usd=amount, unit=price.unit)


def calculate_savings_usd(
    run: RunMetrics, price_table: Optional[Mapping[str, ModelPrice]] = None
) -> Optional[float]:
    """Saved tokens (compression) valued at the model's input price; ``None`` if unknown."""
    table = DEFAULT_PRICE_TABLE if price_table is None else price_table
    price = table.get(run.model) if run.model else None
    if price is None or run.compression is None:
        return None
    return (run.compression.tokens_saved / PRICE_UNITS[price.unit]) * price.input_price


# --------------------------------------------------------------------------- rendering

_CSS = """
:root{--orange:#ff6b00;--grey:#5b5b5b;--line:#e2e2e2}
*{box-sizing:border-box}
body{margin:0;padding:24px;font-family:Segoe UI,Arial,sans-serif;color:#1a1a1a;background:#fafafa}
h1{margin:0 0 4px;font-size:24px}
.subtitle{margin:0 0 20px;color:var(--grey);font-size:14px}
.runs{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.run{background:#fff;border:1px solid var(--line);border-top:4px solid var(--orange);padding:16px;min-width:0}
.run h2{margin:0 0 12px;font-size:16px;overflow-wrap:anywhere}
dl{display:grid;grid-template-columns:1fr auto;gap:8px 12px;margin:0}
dt{color:var(--grey);font-size:13px}
dd{margin:0;font-weight:600;text-align:right;overflow-wrap:anywhere}
.na{color:var(--grey);font-weight:400;font-style:italic}
.empty{margin:0;padding:12px;background:#fff7f0;border:1px dashed var(--orange);color:var(--grey)}
.note{margin:12px 0 0;font-size:12px;color:var(--grey)}
@media (max-width:600px){body{padding:12px}h1{font-size:20px}.runs{grid-template-columns:1fr}}
"""


def _value(testid: str, text: Optional[str]) -> str:
    if text is None:
        return f'<dd class="na" data-testid="{testid}">{UNAVAILABLE}</dd>'
    return f'<dd data-testid="{testid}">{escape(text)}</dd>'


def _row(label: str, testid: str, text: Optional[str]) -> str:
    return f"<dt>{escape(label)}</dt>{_value(testid, text)}"


def _tokens(value: Optional[int]) -> Optional[str]:
    return None if value is None else f"{value:,}"


def _render_run(run: RunMetrics, price_table: Optional[Mapping[str, ModelPrice]]) -> str:
    title = f'<h2 data-testid="run-title">{escape(run.run_id)}</h2>'
    if not run.has_metrics:
        return (
            f'<article class="run" data-testid="run">{title}'
            f'<p class="empty" data-testid="empty-state">{EMPTY_MESSAGE}</p></article>'
        )

    comp = run.compression
    cost = calculate_cost(run.model, run.input_tokens, run.output_tokens, price_table)
    rows = [
        _row("Modelo", "model", run.model),
        _row("Tokens de entrada", "input-tokens", _tokens(run.input_tokens)),
        _row("Tokens de saída", "output-tokens", _tokens(run.output_tokens)),
        _row(
            "Taxa de compressão",
            "compression-ratio",
            None if comp is None else f"{comp.compression_ratio * 100:.1f}%",
        ),
        _row("Método de compressão", "compression-method", None if comp is None else comp.method),
        _row(
            "Tokens economizados",
            "tokens-saved",
            None if comp is None else _tokens(comp.tokens_saved),
        ),
    ]
    savings = calculate_savings_usd(run, price_table)
    if savings is not None:
        rows.append(_row("Economia estimada (USD)", "savings-usd", f"{savings:.6f}"))
    rows.append(
        _row("Custo (USD)", "cost-usd", None if cost is None else f"{cost.amount_usd:.6f}")
    )
    rows.append(
        _row(
            "Unidade de preço",
            "price-unit",
            None if cost is None else PRICE_UNIT_LABELS[cost.unit],
        )
    )
    note = ""
    if comp is not None and comp.method == "mock":
        note = '<p class="note" data-testid="mock-note">Compressão simulada (mock), não medida.</p>'
    return f'<article class="run" data-testid="run">{title}<dl>{"".join(rows)}</dl>{note}</article>'


def render_dashboard(
    runs: List[RunMetrics], price_table: Optional[Mapping[str, ModelPrice]] = None
) -> str:
    """Render a self-contained, responsive HTML page for the given runs."""
    if runs:
        body = "".join(_render_run(r, price_table) for r in runs)
    else:
        body = f'<p class="empty" data-testid="empty-state">{EMPTY_MESSAGE}</p>'
    return (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>Token Metrics Dashboard</title><style>{_CSS}</style></head><body>"
        "<h1>Token Metrics Dashboard</h1>"
        '<p class="subtitle">Valores observados de tokens, compressão e custo.</p>'
        f'<main class="runs" data-testid="runs">{body}</main></body></html>'
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Token Metrics Dashboard")
    parser.add_argument("--input", required=True, help="JSON file: list of runs")
    parser.add_argument("--output", required=True, help="HTML file to write")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    runs = [run_from_dict(item) for item in data]
    Path(args.output).write_text(render_dashboard(runs), encoding="utf-8")
    print(f"Dashboard written to {args.output}")


if __name__ == "__main__":
    main()
