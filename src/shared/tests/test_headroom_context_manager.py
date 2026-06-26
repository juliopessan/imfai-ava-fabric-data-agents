"""
Tests for headroom_context_manager.py.

Focus: the manager must never silently fabricate a compression ratio. On a
platform without the Headroom native engine (e.g. Windows — no `_core`
wheel), it must fall back to real_compressor and label the method honestly.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from headroom_context_manager import HeadroomContextManager


@pytest.fixture
def manager() -> HeadroomContextManager:
    # use_mock=True forces the real_compressor fallback deterministically,
    # regardless of whether headroom._core happens to be importable.
    return HeadroomContextManager(use_mock=True)


class TestCheckHeadroom:
    def test_forced_mock_reports_unavailable(self, manager):
        assert manager.headroom_available is False


class TestCompressHandoff:
    def test_method_is_never_the_old_fabricated_label(self, manager):
        data = {"rows": [{"a": i, "b": i * 2} for i in range(20)]}
        _, stats = manager.compress_handoff(data, "discovery-scout", "data-architect")
        assert stats.method not in ("mock", "headroom")
        assert stats.method.startswith("python-real")

    def test_tokens_are_measured_not_guessed(self, manager):
        data = {"rows": [{"a": i, "b": i * 2} for i in range(20)]}
        _, stats = manager.compress_handoff(data, "discovery-scout", "data-architect")
        assert stats.input_tokens > 0
        assert stats.tokens_saved == stats.input_tokens - stats.output_tokens
        assert stats.compression_ratio == pytest.approx(
            stats.tokens_saved / stats.input_tokens, rel=1e-6
        )

    def test_repeated_calls_are_deterministic(self, manager):
        data = {"rows": [{"a": i} for i in range(20)]}
        _, first = manager.compress_handoff(data, "a", "b")
        _, second = manager.compress_handoff(data, "a", "b")
        assert first.compression_ratio == second.compression_ratio

    def test_tiny_artifact_reports_zero_savings_honestly(self, manager):
        _, stats = manager.compress_handoff({"a": 1}, "a", "b")
        assert stats.tokens_saved == 0
        assert stats.compression_ratio == 0.0


class TestGetStats:
    def test_aggregates_real_measurements(self, manager):
        manager.compress_handoff({"rows": [{"a": i} for i in range(20)]}, "a", "b")
        manager.compress_handoff({"rows": [{"x": i} for i in range(20)]}, "b", "c")
        stats = manager.get_stats()
        assert stats["total_handoffs"] == 2
        assert stats["method"] != "mock"
        assert stats["total_tokens_saved"] >= 0
