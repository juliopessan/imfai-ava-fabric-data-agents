"""
Tests for anthropic_client.py — real harness wrapper (model routing +
prompt caching + usage capture), exercised with a mocked Anthropic client.

No live API key is used or required: a fake client object stands in for
`anthropic.Anthropic()`, matching the response shape documented in the
claude-api skill (response.usage.*, response.content[].text/.type,
response.stop_reason). This verifies the harness's own logic — request
shape, cost math, model selection — without spending real money. Live
validation against the real API is deferred to whoever sets
ANTHROPIC_API_KEY and runs this against the network.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import anthropic_client
import model_pricing


class FakeMessages:
    def __init__(self, response):
        self._response = response
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return self._response


class FakeClient:
    def __init__(self, response):
        self.messages = FakeMessages(response)


def _fake_response(
    text="hello",
    input_tokens=1000,
    output_tokens=200,
    cache_creation_input_tokens=0,
    cache_read_input_tokens=0,
    stop_reason="end_turn",
):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        usage=SimpleNamespace(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_input_tokens=cache_creation_input_tokens,
            cache_read_input_tokens=cache_read_input_tokens,
        ),
        stop_reason=stop_reason,
    )


class TestInvokeAgent:
    def test_routes_to_correct_model_by_task(self):
        client = FakeClient(_fake_response())
        result = anthropic_client.invoke_agent(
            "validate_gate_score", "system prompt", "do the thing", client=client
        )
        assert result.model == "claude-haiku-4-5"
        assert client.messages.last_kwargs["model"] == "claude-haiku-4-5"

    def test_complex_task_routes_to_opus(self):
        client = FakeClient(_fake_response())
        result = anthropic_client.invoke_agent(
            "generate_adr", "system prompt", "design it", client=client
        )
        assert result.model == "claude-opus-4-8"

    def test_system_prompt_carries_cache_control(self):
        client = FakeClient(_fake_response())
        anthropic_client.invoke_agent(
            "validate_gate_score", "stable spec content", "task", client=client
        )
        system_blocks = client.messages.last_kwargs["system"]
        assert system_blocks[0]["text"] == "stable spec content"
        assert system_blocks[0]["cache_control"] == {"type": "ephemeral", "ttl": "1h"}

    def test_custom_cache_ttl_is_passed_through(self):
        client = FakeClient(_fake_response())
        anthropic_client.invoke_agent(
            "validate_gate_score", "spec", "task", client=client, cache_ttl="5m"
        )
        system_blocks = client.messages.last_kwargs["system"]
        assert system_blocks[0]["cache_control"]["ttl"] == "5m"

    def test_extracts_real_usage_fields(self):
        client = FakeClient(
            _fake_response(
                input_tokens=5000,
                output_tokens=300,
                cache_creation_input_tokens=4000,
                cache_read_input_tokens=1000,
            )
        )
        result = anthropic_client.invoke_agent(
            "validate_gate_score", "spec", "task", client=client
        )
        assert result.input_tokens == 5000
        assert result.output_tokens == 300
        assert result.cache_creation_input_tokens == 4000
        assert result.cache_read_input_tokens == 1000

    def test_extracts_response_text(self):
        client = FakeClient(_fake_response(text="the actual answer"))
        result = anthropic_client.invoke_agent(
            "validate_gate_score", "spec", "task", client=client
        )
        assert result.text == "the actual answer"

    def test_cost_uses_real_cache_math_not_guessed(self):
        client = FakeClient(
            _fake_response(
                input_tokens=0,
                output_tokens=0,
                cache_creation_input_tokens=1_000_000,
                cache_read_input_tokens=0,
            )
        )
        result = anthropic_client.invoke_agent(
            "validate_gate_score", "spec", "task", client=client, cache_ttl="1h"
        )
        # Haiku input price * 2.0 (1h cache write multiplier) for 1M tokens
        price = model_pricing.get_price("claude-haiku-4-5")
        expected = price.input_per_mtok * model_pricing.CACHE_WRITE_MULTIPLIER_1H
        assert result.cost_usd == pytest.approx(expected, rel=1e-6)

    def test_stop_reason_is_passed_through(self):
        client = FakeClient(_fake_response(stop_reason="max_tokens"))
        result = anthropic_client.invoke_agent(
            "validate_gate_score", "spec", "task", client=client
        )
        assert result.stop_reason == "max_tokens"


class TestGetClient:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        anthropic_client._client = None
        with pytest.raises(anthropic_client.AnthropicNotConfigured):
            anthropic_client.get_client()


class TestCountTokensReal:
    def test_calls_count_tokens_endpoint(self):
        class FakeCountClient:
            def __init__(self):
                self.messages = SimpleNamespace(
                    count_tokens=lambda **kw: SimpleNamespace(input_tokens=42)
                )

        result = anthropic_client.count_tokens_real(
            "claude-haiku-4-5", "some text", client=FakeCountClient()
        )
        assert result == 42


class TestCacheCostMath:
    def test_cache_read_is_cheaper_than_input(self):
        cost_full = model_pricing.estimate_cost_with_cache_usd(
            input_tokens=1_000_000, output_tokens=0, model="claude-opus-4-8"
        )
        cost_cached = model_pricing.estimate_cost_with_cache_usd(
            input_tokens=0,
            output_tokens=0,
            cache_read_input_tokens=1_000_000,
            model="claude-opus-4-8",
        )
        assert cost_cached < cost_full
        assert cost_cached == pytest.approx(cost_full * 0.10, rel=1e-6)

    def test_1h_cache_write_costs_more_than_5m(self):
        cost_5m = model_pricing.estimate_cost_with_cache_usd(
            input_tokens=0,
            output_tokens=0,
            cache_creation_input_tokens=1_000_000,
            model="claude-haiku-4-5",
            cache_ttl="5m",
        )
        cost_1h = model_pricing.estimate_cost_with_cache_usd(
            input_tokens=0,
            output_tokens=0,
            cache_creation_input_tokens=1_000_000,
            model="claude-haiku-4-5",
            cache_ttl="1h",
        )
        assert cost_1h > cost_5m
