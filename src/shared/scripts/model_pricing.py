"""
Canonical Claude model pricing (USD per 1M tokens).

Single source of truth so enhanced_token_metrics.py, execution_telemetry.py
and headroom_context_manager.py never drift from each other or from
hand-picked constants. Verified against the Anthropic claude-api skill's
current-models table (cached 2026-06-04) — NOT carried over from the
original hardcoded $0.80/$2.40 Haiku constant this module replaced, which
was already stale when written. Update here when Anthropic publishes new
prices.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrice:
    input_per_mtok: float
    output_per_mtok: float


# Ordered most-specific-first; get_price() matches by substring.
PRICING: dict[str, ModelPrice] = {
    "claude-fable-5": ModelPrice(input_per_mtok=10.00, output_per_mtok=50.00),
    "claude-mythos-5": ModelPrice(input_per_mtok=10.00, output_per_mtok=50.00),
    "claude-opus-4": ModelPrice(input_per_mtok=5.00, output_per_mtok=25.00),
    "claude-sonnet-4": ModelPrice(input_per_mtok=3.00, output_per_mtok=15.00),
    "claude-haiku-4-5": ModelPrice(input_per_mtok=1.00, output_per_mtok=5.00),
    "claude-haiku": ModelPrice(input_per_mtok=1.00, output_per_mtok=5.00),
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


# Prompt-caching economics (Anthropic, verified 2026-06-04): a cache write
# costs a premium over a normal input token, a cache read costs a fraction.
CACHE_WRITE_MULTIPLIER_5M = 1.25
CACHE_WRITE_MULTIPLIER_1H = 2.0
CACHE_READ_MULTIPLIER = 0.10


def estimate_cost_with_cache_usd(
    input_tokens: int,
    output_tokens: int,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
    model: str | None = None,
    cache_ttl: str = "5m",
) -> float:
    """
    Real cost math including prompt-cache writes/reads, from the four usage
    fields the Messages API actually returns. Pass the real
    `response.usage.*` fields here — never a guessed compression ratio.
    """
    price = get_price(model)
    write_multiplier = CACHE_WRITE_MULTIPLIER_1H if cache_ttl == "1h" else CACHE_WRITE_MULTIPLIER_5M

    cost = (input_tokens / 1_000_000) * price.input_per_mtok
    cost += (cache_creation_input_tokens / 1_000_000) * price.input_per_mtok * write_multiplier
    cost += (cache_read_input_tokens / 1_000_000) * price.input_per_mtok * CACHE_READ_MULTIPLIER
    cost += (output_tokens / 1_000_000) * price.output_per_mtok
    return cost
