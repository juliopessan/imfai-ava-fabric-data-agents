"""
Canonical Claude model pricing (USD per 1M tokens).

Single source of truth so enhanced_token_metrics.py, execution_telemetry.py
and headroom_context_manager.py never drift from each other or from
hand-picked constants. Update here when Anthropic publishes new prices.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrice:
    input_per_mtok: float
    output_per_mtok: float


# Ordered most-specific-first; get_price() matches by substring.
PRICING: dict[str, ModelPrice] = {
    "claude-opus-4": ModelPrice(input_per_mtok=15.00, output_per_mtok=75.00),
    "claude-sonnet-4": ModelPrice(input_per_mtok=3.00, output_per_mtok=15.00),
    "claude-haiku-4-5": ModelPrice(input_per_mtok=0.80, output_per_mtok=2.40),
    "claude-haiku": ModelPrice(input_per_mtok=0.80, output_per_mtok=2.40),
}

DEFAULT_MODEL = "claude-haiku-4-5"


def get_price(model: str | None) -> ModelPrice:
    """Return pricing for *model*, matching by substring. Falls back to Haiku."""
    if model:
        key = model.lower()
        for name, price in PRICING.items():
            if name in key:
                return price
    return PRICING[DEFAULT_MODEL]


def estimate_cost_usd(input_tokens: int, output_tokens: int, model: str | None = None) -> float:
    """Real cost math given real token counts. No fabricated ratios involved."""
    price = get_price(model)
    return (input_tokens / 1_000_000) * price.input_per_mtok + (
        output_tokens / 1_000_000
    ) * price.output_per_mtok
