#!/usr/bin/env python3
"""
Real Anthropic API client wrapper — model routing + prompt caching + real
usage capture.

Why this file exists: nothing in this repo ever made a programmatic LLM call.
The 21 agents are `.chatmode.md` specs interpreted by GitHub Copilot/Claude
Code when a human invokes them; migration_coordinator.py and friends are
deterministic Python orchestration. model_router.py existed but was never
wired to anything. This module is the harness layer that makes the rest of
the cost-instrumentation chain (model_router.py, model_pricing.py,
real_compressor.py, observability_setup.py) actually mean something for code
that *does* call a model directly, instead of staying parallel infrastructure
nothing exercises.

Requires ANTHROPIC_API_KEY in the environment for real calls. Tests inject a
fake client via the `client=` parameter — see test_anthropic_client.py.
"""
from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import model_pricing
import model_router

logger = logging.getLogger(__name__)


class AnthropicNotConfigured(RuntimeError):
    """Raised when ANTHROPIC_API_KEY isn't set and no test client was injected."""


@dataclass
class InvocationResult:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    cost_usd: float
    stop_reason: Optional[str]


_client = None


def get_client():
    """Lazily construct the real Anthropic client. Raises if not configured."""
    global _client
    if _client is None:
        try:
            import anthropic
        except ImportError as exc:
            raise AnthropicNotConfigured("The 'anthropic' package is not installed.") from exc
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise AnthropicNotConfigured(
                "ANTHROPIC_API_KEY is not set — no real Anthropic call can be made. "
                "Inject a test client via the `client=` parameter for offline testing."
            )
        _client = anthropic.Anthropic()
    return _client


def invoke_agent(
    task_name: str,
    system_prompt: str,
    user_content: str,
    *,
    context: dict | None = None,
    cache_ttl: str = "1h",
    client: Any = None,
) -> InvocationResult:
    """
    Invoke a Claude model for *task_name*. The model is chosen by
    model_router.py (Haiku/Sonnet/Opus by task complexity); *system_prompt*
    — the stable spec/agent-instruction content — is marked with
    `cache_control` so repeated calls for the same agent hit the prompt
    cache instead of re-billing the full system prompt every time.

    *client* can be injected for tests: anything exposing
    `.messages.create(...)` with the same response shape as the real SDK.
    """
    router = model_router.get_router()
    config = router.get_config(task_name, context)
    real_client = client or get_client()

    response = real_client.messages.create(
        model=config.deployment,
        max_tokens=config.max_tokens,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral", "ttl": cache_ttl},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )

    usage = response.usage
    input_tokens = getattr(usage, "input_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0
    cache_creation = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0

    cost = model_pricing.estimate_cost_with_cache_usd(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_creation_input_tokens=cache_creation,
        cache_read_input_tokens=cache_read,
        model=config.deployment,
        cache_ttl=cache_ttl,
    )

    text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    logger.info(
        "invoke_agent(%s) -> %s: in=%d out=%d cache_write=%d cache_read=%d cost=$%.6f",
        task_name, config.deployment, input_tokens, output_tokens, cache_creation, cache_read, cost,
    )

    return InvocationResult(
        text=text,
        model=config.deployment,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_creation_input_tokens=cache_creation,
        cache_read_input_tokens=cache_read,
        cost_usd=cost,
        stop_reason=getattr(response, "stop_reason", None),
    )


def count_tokens_real(model: str, text: str, client: Any = None) -> int:
    """
    Real Claude token count via the Messages API's count_tokens endpoint.

    Prefer this over real_compressor.count_tokens (tiktoken) whenever a live
    client is available — tiktoken is OpenAI's tokenizer and undercounts
    Claude tokens by ~15-20%+ on typical text, more on code.
    """
    real_client = client or get_client()
    result = real_client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return result.input_tokens
