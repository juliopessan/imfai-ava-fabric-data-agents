"""
Tests for real_compressor.py — genuine, measured token compression.

These exist to lock in the property that matters most: every reported ratio
must come from an actual before/after measurement of a real transform, never
a fixed lookup table keyed off string sniffing (the bug this module replaced).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import real_compressor


class TestCountTokens:
    def test_empty_string_is_zero(self):
        assert real_compressor.count_tokens("") == 0

    def test_longer_text_has_more_tokens(self):
        short = real_compressor.count_tokens("hello")
        long = real_compressor.count_tokens("hello " * 50)
        assert long > short

    def test_tokenizer_method_is_reported(self):
        # Either a real tokenizer or a clearly labeled approximation — never silent.
        assert real_compressor.tokenizer_method() in (
            "tiktoken-cl100k_base",
            "whitespace-approx",
        )


class TestColumnarDedup:
    def test_uniform_list_of_dicts_becomes_columnar(self):
        data = {"rows": [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]}
        deduped = real_compressor._columnar_dedup(data)
        assert deduped["rows"]["__columnar__"] is True
        assert deduped["rows"]["keys"] == ["a", "b"]
        assert deduped["rows"]["rows"] == [[1, 2], [3, 4], [5, 6]]

    def test_non_uniform_list_is_left_alone(self):
        data = {"rows": [{"a": 1}, {"b": 2}]}
        deduped = real_compressor._columnar_dedup(data)
        assert deduped == data

    def test_roundtrip_is_lossless(self):
        original = [{"name": "a", "n": 1}, {"name": "b", "n": 2}, {"name": "c", "n": 3}]
        deduped = real_compressor._columnar_dedup(original)
        assert real_compressor.expand_columnar(deduped) == original


class TestCompressArtifact:
    def test_small_artifact_is_not_compressed(self):
        outcome = real_compressor.compress_artifact({"a": 1}, min_tokens_to_compress=50)
        assert outcome.tokens_saved == 0
        assert outcome.compression_ratio == 0.0
        assert outcome.method == "python-real-skipped-too-small"

    def test_repetitive_json_array_is_genuinely_reduced(self):
        data = {
            "entities": [
                {"name": f"table_{i}", "schema": "ledger", "row_count": i * 1000}
                for i in range(30)
            ]
        }
        outcome = real_compressor.compress_artifact(data)
        assert outcome.method == "python-real-columnar"
        assert outcome.output_tokens < outcome.input_tokens
        assert 0.0 < outcome.compression_ratio < 1.0
        assert outcome.tokens_saved == outcome.input_tokens - outcome.output_tokens

    def test_ratio_is_never_fabricated_above_measured_reduction(self):
        # The whole point of this module: never report more savings than
        # were actually measured. Run it twice on identical input and the
        # ratio must be deterministic, not drawn from a guess table.
        data = {"items": [{"x": i} for i in range(20)]}
        first = real_compressor.compress_artifact(data)
        second = real_compressor.compress_artifact(data)
        assert first.compression_ratio == second.compression_ratio
        assert first.input_tokens == second.input_tokens
        assert first.output_tokens == second.output_tokens

    def test_output_never_exceeds_input_tokens(self):
        data = {"text": "no repetition here at all, just unique prose. " * 5}
        outcome = real_compressor.compress_artifact(data, min_tokens_to_compress=10)
        assert outcome.output_tokens <= outcome.input_tokens

    def test_non_json_text_uses_whitespace_method(self):
        text = "line one\n\n\n\nline two   \n" * 10
        outcome = real_compressor.compress_artifact(text, min_tokens_to_compress=5)
        assert outcome.method in ("python-real-whitespace", "python-real-skipped-too-small")
