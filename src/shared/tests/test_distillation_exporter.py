#!/usr/bin/env python3
"""Tests for DistillationCapture and DistillationExporter."""

import csv
import json
import pytest
import tempfile
from pathlib import Path

from src.shared.scripts.distillation_exporter import (
    DistillationCapture,
    DistillationExporter,
    DistillationSample,
    _compute_quality,
)


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "distillation_test.db")


@pytest.fixture
def capture(db_path):
    c = DistillationCapture(db_path=db_path)
    yield c
    c.close()


@pytest.fixture
def exporter(db_path):
    e = DistillationExporter(db_path=db_path)
    yield e
    e.close()


@pytest.fixture
def capture_and_exporter(db_path):
    """Both sharing the same DB — typical pipeline usage."""
    c = DistillationCapture(db_path=db_path)
    e = DistillationExporter(db_path=db_path)
    yield c, e
    c.close()
    e.close()


# ────────────────────────────────────────────────────────────────────
# Quality score formula
# ────────────────────────────────────────────────────────────────────

class TestQualityScore:
    def test_perfect_quality(self):
        # gate_score=1.0, efficiency=(1-0/100)=1.0, success=1.0
        score = _compute_quality(tokens_in=100, tokens_out=0, gate_score=1.0, status="success")
        assert score == pytest.approx(1.0)

    def test_zero_quality_on_failure_no_gate(self):
        # gate_score=0, efficiency=(1-100/100)=0, success=0
        score = _compute_quality(tokens_in=100, tokens_out=100, gate_score=0.0, status="error")
        assert score == pytest.approx(0.0)

    def test_partial_quality(self):
        # gate_score=0.84 → 0.40*0.84 = 0.336
        # efficiency=(1-120/800)=0.85 → 0.40*0.85 = 0.340
        # success=1.0 → 0.20*1.0 = 0.200
        # total = 0.876
        score = _compute_quality(
            tokens_in=800, tokens_out=120, gate_score=0.84, status="success"
        )
        assert score == pytest.approx(0.876, abs=0.001)

    def test_unknown_tokens_uses_neutral_efficiency(self):
        # tokens_in=0 → efficiency=0.5 (neutral)
        score = _compute_quality(tokens_in=0, tokens_out=0, gate_score=0.0, status="success")
        assert score == pytest.approx(0.40 * 0.0 + 0.40 * 0.5 + 0.20 * 1.0)

    def test_clamped_to_one(self):
        score = _compute_quality(tokens_in=1000, tokens_out=1, gate_score=1.0, status="success")
        assert score <= 1.0

    def test_clamped_to_zero(self):
        # Artificially pass tokens_out > tokens_in — should not go negative
        score = _compute_quality(tokens_in=10, tokens_out=9999, gate_score=0.0, status="error")
        assert score >= 0.0


# ────────────────────────────────────────────────────────────────────
# DistillationCapture
# ────────────────────────────────────────────────────────────────────

class TestDistillationCapture:
    def test_capture_returns_sample_id(self, capture):
        sid = capture.capture(
            task_name="entity_classification",
            user_message="Classify table customers",
            response_text="customers → staging",
        )
        assert sid.startswith("ds_")

    def test_capture_persists_sample(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="lineage_extraction",
            user_message="Extract lineage from INSERT INTO stg SELECT * FROM src",
            response_text="src → stg (INSERT)",
            wave_id="wave3",
            tokens_in=400,
            tokens_out=60,
            gate_score=0.85,
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        assert len(samples) == 1
        s = samples[0]
        assert s.task_name == "lineage_extraction"
        assert s.wave_id == "wave3"
        assert s.tokens_in == 400

    def test_capture_computes_quality(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="t",
            user_message="u",
            response_text="r",
            tokens_in=800,
            tokens_out=120,
            gate_score=0.84,
            status="success",
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        assert samples[0].quality_score == pytest.approx(0.876, abs=0.001)

    def test_capture_with_system_prompt(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="classification",
            system_prompt="You are a migration expert.",
            user_message="Classify orders",
            response_text="orders → target",
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        assert samples[0].system_prompt == "You are a migration expert."

    def test_capture_error_status(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="t",
            user_message="u",
            response_text="r",
            status="error",
            gate_score=0.0,
            tokens_in=100,
            tokens_out=100,
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        assert samples[0].status == "error"
        assert samples[0].quality_score == 0.0

    def test_context_manager(self, db_path):
        with DistillationCapture(db_path=db_path) as c:
            sid = c.capture(task_name="t", user_message="u", response_text="r")
        assert sid.startswith("ds_")


# ────────────────────────────────────────────────────────────────────
# DistillationExporter — filter_samples
# ────────────────────────────────────────────────────────────────────

class TestFilterSamples:
    def _populate(self, cap):
        cap.capture(
            task_name="entity_classification", user_message="u1", response_text="r1",
            wave_id="wave1", tokens_in=800, tokens_out=120, gate_score=0.90, status="success"
        )
        cap.capture(
            task_name="lineage", user_message="u2", response_text="r2",
            wave_id="wave2", tokens_in=200, tokens_out=180, gate_score=0.30, status="success"
        )
        cap.capture(
            task_name="entity_classification", user_message="u3", response_text="r3",
            wave_id="wave1", tokens_in=500, tokens_out=50, gate_score=0.82, status="success"
        )

    def test_filter_by_quality_score(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._populate(cap)
        high = exp.filter_samples(min_quality_score=0.70)
        low = exp.filter_samples(min_quality_score=0.0)
        assert len(high) < len(low)
        assert all(s.quality_score >= 0.70 for s in high)

    def test_filter_by_gate_score(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._populate(cap)
        samples = exp.filter_samples(min_quality_score=0.0, min_gate_score=0.80)
        assert all(s.gate_score >= 0.80 for s in samples)

    def test_filter_by_wave_id(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._populate(cap)
        samples = exp.filter_samples(min_quality_score=0.0, wave_id="wave1")
        assert all(s.wave_id == "wave1" for s in samples)
        assert len(samples) == 2

    def test_filter_by_task_name(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._populate(cap)
        samples = exp.filter_samples(min_quality_score=0.0, task_name="lineage")
        assert all(s.task_name == "lineage" for s in samples)

    def test_filter_by_max_cost(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="t", user_message="u", response_text="r", cost_usd=0.05)
        cap.capture(task_name="t", user_message="u2", response_text="r2", cost_usd=0.50)
        samples = exp.filter_samples(min_quality_score=0.0, max_cost_usd=0.10)
        assert all(s.cost_usd <= 0.10 for s in samples)

    def test_results_ordered_by_quality_desc(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._populate(cap)
        samples = exp.filter_samples(min_quality_score=0.0)
        scores = [s.quality_score for s in samples]
        assert scores == sorted(scores, reverse=True)

    def test_empty_db_returns_empty_list(self, exporter):
        assert exporter.filter_samples() == []


# ────────────────────────────────────────────────────────────────────
# Export — JSONL OpenAI format
# ────────────────────────────────────────────────────────────────────

class TestExportJsonlOpenAI:
    def _make_samples(self, cap):
        cap.capture(
            task_name="classification",
            system_prompt="You are a migration agent.",
            user_message="Classify orders table",
            response_text="orders → staging",
        )
        cap.capture(
            task_name="classification",
            system_prompt="",
            user_message="Classify products table",
            response_text="products → target",
        )

    def test_export_returns_count(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._make_samples(cap)
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "train.jsonl"
        n = exp.export_jsonl_openai(str(out), samples)
        assert n == 2

    def test_export_valid_jsonl(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        self._make_samples(cap)
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "train.jsonl"
        exp.export_jsonl_openai(str(out), samples)
        lines = out.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        for line in lines:
            obj = json.loads(line)
            assert "messages" in obj
            roles = [m["role"] for m in obj["messages"]]
            assert "user" in roles
            assert "assistant" in roles

    def test_system_prompt_included_when_present(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="t",
            system_prompt="Be concise.",
            user_message="u",
            response_text="r",
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "out.jsonl"
        exp.export_jsonl_openai(str(out), samples)
        obj = json.loads(out.read_text().strip())
        assert obj["messages"][0]["role"] == "system"

    def test_system_prompt_omitted_when_empty(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="t", user_message="u", response_text="r", system_prompt="")
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "out.jsonl"
        exp.export_jsonl_openai(str(out), samples)
        obj = json.loads(out.read_text().strip())
        assert obj["messages"][0]["role"] == "user"


# ────────────────────────────────────────────────────────────────────
# Export — JSONL Anthropic format
# ────────────────────────────────────────────────────────────────────

class TestExportJsonlAnthropic:
    def test_anthropic_format_structure(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="t",
            system_prompt="Be a migration expert.",
            user_message="Classify table",
            response_text="→ staging",
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "anthropic.jsonl"
        n = exp.export_jsonl_anthropic(str(out), samples)
        assert n == 1
        obj = json.loads(out.read_text().strip())
        assert "system" in obj
        assert obj["system"] == "Be a migration expert."
        assert obj["messages"][0]["role"] == "user"
        assert obj["messages"][1]["role"] == "assistant"

    def test_anthropic_no_system_prompt(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="t", user_message="u", response_text="r")
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "anthropic.jsonl"
        exp.export_jsonl_anthropic(str(out), samples)
        obj = json.loads(out.read_text().strip())
        assert "system" not in obj


# ────────────────────────────────────────────────────────────────────
# Export — CSV
# ────────────────────────────────────────────────────────────────────

class TestExportCsv:
    def test_csv_has_header_and_rows(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="t", user_message="classify customers", response_text="→ staging")
        cap.capture(task_name="t", user_message="classify orders", response_text="→ target")
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "review.csv"
        n = exp.export_csv(str(out), samples)
        assert n == 2
        with open(out, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert "quality_score" in rows[0]
        assert "user_message_preview" in rows[0]

    def test_csv_preview_truncated(self, tmp_path, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="t",
            user_message="A" * 300,
            response_text="B" * 300,
        )
        samples = exp.filter_samples(min_quality_score=0.0)
        out = tmp_path / "review.csv"
        exp.export_csv(str(out), samples, preview_chars=50)
        with open(out, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows[0]["user_message_preview"]) <= 50
        assert len(rows[0]["response_preview"]) <= 50


# ────────────────────────────────────────────────────────────────────
# Statistics
# ────────────────────────────────────────────────────────────────────

class TestGetStatistics:
    def test_statistics_empty(self, exporter):
        stats = exporter.get_statistics([])
        assert stats == {"total_samples": 0}

    def test_statistics_keys(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(
            task_name="entity_classification",
            user_message="u", response_text="r",
            tokens_in=500, tokens_out=80, cost_usd=0.005, gate_score=0.85,
        )
        stats = exp.get_statistics()
        required = {
            "total_samples", "avg_quality_score", "min_quality_score",
            "max_quality_score", "total_cost_usd", "total_tokens_in",
            "total_tokens_out", "by_task_name",
        }
        assert required.issubset(stats.keys())

    def test_statistics_by_task_name(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="lineage", user_message="u1", response_text="r1")
        cap.capture(task_name="lineage", user_message="u2", response_text="r2")
        cap.capture(task_name="classification", user_message="u3", response_text="r3")
        stats = exp.get_statistics()
        assert stats["by_task_name"]["lineage"] == 2
        assert stats["by_task_name"]["classification"] == 1

    def test_statistics_none_reads_all(self, capture_and_exporter):
        cap, exp = capture_and_exporter
        cap.capture(task_name="t", user_message="u", response_text="r")
        # Passing None reads all samples from DB
        stats = exp.get_statistics(None)
        assert stats["total_samples"] == 1
