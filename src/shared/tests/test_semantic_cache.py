#!/usr/bin/env python3
"""Tests for SemanticCache — exact match, cosine similarity, statistics."""

import pytest
import tempfile
import os
from pathlib import Path

from src.shared.scripts.semantic_cache import SemanticCache, CacheEntry


@pytest.fixture
def cache(tmp_path):
    """SemanticCache backed by a temp SQLite file."""
    db = str(tmp_path / "test_cache.db")
    c = SemanticCache(db_path=db, similarity_threshold=0.80)
    yield c
    c.close()


@pytest.fixture
def memory_cache():
    """SemanticCache backed by :memory: for fast isolated tests."""
    c = SemanticCache(db_path=":memory:", similarity_threshold=0.80)
    yield c
    c.close()


# ────────────────────────────────────────────────────────────────────
# put / get — basic behaviour
# ────────────────────────────────────────────────────────────────────

class TestPutGet:
    def test_put_returns_cache_entry(self, memory_cache):
        entry = memory_cache.put(
            query="classify customers table",
            response="customers → staging",
            task_type="entity_classification",
            model="claude-sonnet",
            wave_id="wave1",
            tokens_in=100,
            tokens_out=20,
            cost_usd=0.001,
        )
        assert isinstance(entry, CacheEntry)
        assert entry.cache_id.startswith("sc_")
        assert entry.query_text == "classify customers table"
        assert entry.hit_count == 0

    def test_put_duplicate_does_not_raise(self, memory_cache):
        for _ in range(3):
            memory_cache.put(
                query="same query",
                response="same response",
                task_type="entity_classification",
            )
        stats = memory_cache.get_statistics()
        # Only one entry stored (INSERT OR IGNORE)
        assert stats["total_entries"] == 1

    def test_get_returns_none_on_empty_cache(self, memory_cache):
        result = memory_cache.get("no entry here", task_type="lineage")
        assert result is None


# ────────────────────────────────────────────────────────────────────
# Exact match
# ────────────────────────────────────────────────────────────────────

class TestExactMatch:
    def test_exact_match_hit(self, memory_cache):
        memory_cache.put(
            query="SELECT * FROM customers",
            response="entity: customers, type: source",
            task_type="entity_classification",
        )
        hit = memory_cache.get("SELECT * FROM customers", task_type="entity_classification")
        assert hit is not None
        assert hit.response_text == "entity: customers, type: source"

    def test_exact_match_increments_hit_count(self, memory_cache):
        memory_cache.put(query="q", response="r", task_type="t")
        memory_cache.get("q", task_type="t")
        memory_cache.get("q", task_type="t")
        # Re-fetch from DB to see persisted hit_count
        hit = memory_cache.get("q", task_type="t")
        assert hit is not None
        assert hit.hit_count >= 2

    def test_exact_match_wrong_task_type_is_miss(self, memory_cache):
        memory_cache.put(query="SELECT * FROM orders", response="ok", task_type="lineage")
        miss = memory_cache.get("SELECT * FROM orders", task_type="entity_classification")
        assert miss is None

    def test_exact_match_leading_trailing_whitespace_normalised(self, memory_cache):
        memory_cache.put(query="  trim me  ", response="trimmed", task_type="t")
        # SHA256 hashes strip() the text — both variants should hit
        hit = memory_cache.get("  trim me  ", task_type="t")
        assert hit is not None


# ────────────────────────────────────────────────────────────────────
# Semantic similarity match
# ────────────────────────────────────────────────────────────────────

class TestSemanticMatch:
    def test_similar_query_hits_above_threshold(self, memory_cache):
        """Same vocabulary, different order → cosine should be > 0.80."""
        memory_cache.put(
            query="classify table customers entity type source",
            response="customers → source",
            task_type="entity_classification",
        )
        # Reordered tokens — cosine similarity is high because TF vectors share words
        hit = memory_cache.get(
            "entity type source customers table classify",
            task_type="entity_classification",
        )
        assert hit is not None
        assert hit.response_text == "customers → source"

    def test_dissimilar_query_is_miss(self, memory_cache):
        """Completely different vocabulary → cosine below threshold."""
        memory_cache.put(
            query="classify table customers entity type source",
            response="customers → source",
            task_type="entity_classification",
        )
        miss = memory_cache.get(
            "payment gateway timeout configuration retry limit",
            task_type="entity_classification",
        )
        assert miss is None

    def test_threshold_boundary_respected(self):
        """Strict threshold (0.99) rejects partial match; lenient (0.50) accepts it.

        stored:  8 tokens  classify orders table entity lineage migration source target
        queried: 6 tokens  classify orders table entity lineage migration
        cosine ≈ 0.866  → above 0.50, below 0.99
        """
        strict = SemanticCache(db_path=":memory:", similarity_threshold=0.99)
        lenient = SemanticCache(db_path=":memory:", similarity_threshold=0.50)
        try:
            stored = "classify orders table entity lineage migration source target"
            alt    = "classify orders table entity lineage migration"
            for c in (strict, lenient):
                c.put(query=stored, response="orders → target", task_type="t")
            assert strict.get(alt, task_type="t") is None
            assert lenient.get(alt, task_type="t") is not None
        finally:
            strict.close()
            lenient.close()

    def test_empty_query_does_not_raise(self, memory_cache):
        result = memory_cache.get("", task_type="entity_classification")
        assert result is None


# ────────────────────────────────────────────────────────────────────
# invalidate_wave
# ────────────────────────────────────────────────────────────────────

class TestInvalidateWave:
    def test_invalidate_removes_wave_entries(self, memory_cache):
        memory_cache.put(query="q1", response="r1", task_type="t", wave_id="wave1")
        memory_cache.put(query="q2", response="r2", task_type="t", wave_id="wave1")
        memory_cache.put(query="q3", response="r3", task_type="t", wave_id="wave2")

        deleted = memory_cache.invalidate_wave("wave1")
        assert deleted == 2

        # wave2 entry survives
        assert memory_cache.get_statistics()["total_entries"] == 1

    def test_invalidate_nonexistent_wave_returns_zero(self, memory_cache):
        assert memory_cache.invalidate_wave("ghost_wave") == 0


# ────────────────────────────────────────────────────────────────────
# Statistics
# ────────────────────────────────────────────────────────────────────

class TestStatistics:
    def test_statistics_empty_cache(self, memory_cache):
        stats = memory_cache.get_statistics()
        assert stats["total_entries"] == 0
        assert stats["total_hits"] == 0
        assert stats["total_cost_avoided_usd"] == 0.0

    def test_statistics_after_put_and_hit(self, memory_cache):
        memory_cache.put(
            query="q", response="r", task_type="entity_classification",
            wave_id="w1", tokens_in=200, cost_usd=0.01,
        )
        memory_cache.get("q", task_type="entity_classification")
        stats = memory_cache.get_statistics()

        assert stats["total_entries"] == 1
        assert stats["total_hits"] == 1
        assert stats["total_cost_stored_usd"] == pytest.approx(0.01)
        assert stats["total_cost_avoided_usd"] == pytest.approx(0.01)  # 1 hit × 0.01
        assert stats["total_tokens_avoided"] == 200

    def test_statistics_by_task_type(self, memory_cache):
        memory_cache.put(query="a", response="ra", task_type="lineage")
        memory_cache.put(query="b", response="rb", task_type="entity_classification")
        stats = memory_cache.get_statistics()
        types = {b["task_type"] for b in stats["by_task_type"]}
        assert "lineage" in types
        assert "entity_classification" in types

    def test_statistics_contains_threshold(self, memory_cache):
        stats = memory_cache.get_statistics()
        assert "similarity_threshold" in stats
        assert stats["similarity_threshold"] == 0.80


# ────────────────────────────────────────────────────────────────────
# Context manager
# ────────────────────────────────────────────────────────────────────

class TestContextManager:
    def test_context_manager(self, tmp_path):
        db = str(tmp_path / "cm_test.db")
        with SemanticCache(db_path=db) as c:
            c.put(query="hello", response="world", task_type="t")
            hit = c.get("hello", task_type="t")
            assert hit is not None
