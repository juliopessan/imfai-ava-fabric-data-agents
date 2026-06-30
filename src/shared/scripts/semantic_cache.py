#!/usr/bin/env python3
"""
Semantic Cache — Global query cache with exact-match and cosine-similarity lookup.

Eliminates duplicate LLM calls across waves and projects by caching responses and
returning them on semantically equivalent queries.

Two lookup strategies:
  1. Exact match (SHA256 hash) — O(1), zero false positives.
  2. Semantic similarity (TF-IDF cosine within task_type bucket) — pure Python,
     no numpy, no external embeddings, no vector DB.

All storage is SQLite (same pattern as KnowledgeGraphStore).
Zero external dependencies beyond stdlib.

Estimated savings: 15–25% of LLM calls on repeated migration patterns
(schema discovery, entity classification, lineage extraction tend to repeat
across waves of the same domain).

Usage:
    cache = SemanticCache("project_cache.db", similarity_threshold=0.85)

    hit = cache.get(query="SELECT * FROM customers", task_type="entity_classification")
    if hit:
        return hit.response_text  # reuse — zero cost

    response = invoke_llm(query)
    cache.put(
        query=query, response=response,
        task_type="entity_classification", model="claude-sonnet-4-5",
        wave_id="wave2", tokens_in=500, tokens_out=200, cost_usd=0.002,
    )

    # Cross-wave: later in wave5 the same classification prompt hits the cache
    print(cache.get_statistics())
    # → {"total_hits": 14, "total_cost_avoided_usd": 0.028, ...}
"""
from __future__ import annotations

import hashlib
import math
import re
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class CacheEntry:
    """Single cached LLM response with provenance and hit tracking."""
    cache_id: str
    task_type: str
    query_hash: str
    query_text: str
    response_text: str
    model: str
    wave_id: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    hit_count: int
    created_at: str
    last_accessed: str


_SCHEMA = """
CREATE TABLE IF NOT EXISTS cache_entries (
    id            INTEGER PRIMARY KEY,
    cache_id      TEXT    NOT NULL UNIQUE,
    task_type     TEXT    NOT NULL,
    query_hash    TEXT    NOT NULL,
    query_text    TEXT    NOT NULL,
    response_text TEXT    NOT NULL,
    model         TEXT    NOT NULL DEFAULT '',
    wave_id       TEXT    NOT NULL DEFAULT '',
    tokens_in     INTEGER NOT NULL DEFAULT 0,
    tokens_out    INTEGER NOT NULL DEFAULT 0,
    cost_usd      REAL    NOT NULL DEFAULT 0.0,
    hit_count     INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL,
    last_accessed TEXT    NOT NULL,
    UNIQUE (query_hash, task_type)
);
CREATE INDEX IF NOT EXISTS idx_cache_hash      ON cache_entries(query_hash);
CREATE INDEX IF NOT EXISTS idx_cache_task_type ON cache_entries(task_type);
"""


class SemanticCache:
    """
    Persistent semantic cache for LLM responses.

    Lookup order:
      1. Exact SHA256 hash match — instant, no false positives.
      2. Cosine similarity on bag-of-words within same task_type bucket.
         Pure Python: no numpy, no external embeddings required.

    All hits increment hit_count and update last_accessed.
    """

    def __init__(
        self,
        db_path: str = "semantic_cache.db",
        similarity_threshold: float = 0.85,
    ) -> None:
        self.db_path = str(db_path)
        self.similarity_threshold = similarity_threshold
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        """Explicitly close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SemanticCache":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(
        self,
        query: str,
        task_type: str,
        model: str = "",
    ) -> Optional[CacheEntry]:
        """
        Look up a cached response.

        Returns a CacheEntry on hit (exact or semantic), None on miss.
        model is reserved for future per-model partitioning — not used in
        lookup today so a hit on claude-haiku is also valid for claude-sonnet.
        """
        entry = self._exact_match(query, task_type)
        if entry:
            self._record_hit(entry.cache_id)
            return entry

        entry = self._semantic_match(query, task_type)
        if entry:
            self._record_hit(entry.cache_id)
            return entry

        return None

    def put(
        self,
        query: str,
        response: str,
        task_type: str,
        model: str = "",
        wave_id: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
    ) -> CacheEntry:
        """Store a new cache entry. Silently ignores exact duplicates."""
        now = datetime.now(timezone.utc).isoformat()
        entry = CacheEntry(
            cache_id=f"sc_{uuid.uuid4().hex[:12]}",
            task_type=task_type,
            query_hash=self._hash(query),
            query_text=query,
            response_text=response,
            model=model,
            wave_id=wave_id,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
            hit_count=0,
            created_at=now,
            last_accessed=now,
        )
        self._conn.execute(
            """INSERT OR IGNORE INTO cache_entries
               (cache_id, task_type, query_hash, query_text, response_text,
                model, wave_id, tokens_in, tokens_out, cost_usd,
                hit_count, created_at, last_accessed)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                entry.cache_id, entry.task_type, entry.query_hash,
                entry.query_text, entry.response_text, entry.model,
                entry.wave_id, entry.tokens_in, entry.tokens_out,
                entry.cost_usd, entry.hit_count, entry.created_at,
                entry.last_accessed,
            ),
        )
        self._conn.commit()
        return entry

    def invalidate_wave(self, wave_id: str) -> int:
        """Remove all entries belonging to a wave. Returns deleted count."""
        cur = self._conn.execute(
            "DELETE FROM cache_entries WHERE wave_id = ?", (wave_id,)
        )
        self._conn.commit()
        return cur.rowcount

    def get_statistics(self) -> Dict:
        """Summary: total entries, hits, cost avoided, tokens avoided."""
        row = self._conn.execute("""
            SELECT
                COUNT(*)             AS total_entries,
                SUM(hit_count)       AS total_hits,
                SUM(cost_usd)        AS total_cost_stored_usd,
                SUM(cost_usd * hit_count) AS total_cost_avoided_usd,
                SUM(tokens_in)       AS total_tokens_in_stored,
                SUM(tokens_in * hit_count) AS total_tokens_avoided
            FROM cache_entries
        """).fetchone()
        by_type = self._conn.execute("""
            SELECT task_type, COUNT(*) AS entries, SUM(hit_count) AS hits
            FROM cache_entries
            GROUP BY task_type
        """).fetchall()
        return {
            "total_entries": row["total_entries"] or 0,
            "total_hits": row["total_hits"] or 0,
            "total_cost_stored_usd": round(row["total_cost_stored_usd"] or 0.0, 6),
            "total_cost_avoided_usd": round(row["total_cost_avoided_usd"] or 0.0, 6),
            "total_tokens_avoided": row["total_tokens_avoided"] or 0,
            "similarity_threshold": self.similarity_threshold,
            "by_task_type": [
                {
                    "task_type": r["task_type"],
                    "entries": r["entries"],
                    "hits": r["hits"] or 0,
                }
                for r in by_type
            ],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Lowercase word tokenizer — no external dependencies."""
        return re.findall(r"[a-z0-9_]+", text.lower())

    @staticmethod
    def _tf_vector(tokens: List[str]) -> Dict[str, float]:
        """Term-frequency vector. Keys: word, values: relative frequency."""
        if not tokens:
            return {}
        counts: Dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        total = len(tokens)
        return {word: count / total for word, count in counts.items()}

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        """Cosine similarity between two TF vectors. Pure Python."""
        if not a or not b:
            return 0.0
        dot = sum(a.get(w, 0.0) * v for w, v in b.items())
        mag_a = math.sqrt(sum(v * v for v in a.values()))
        mag_b = math.sqrt(sum(v * v for v in b.values()))
        if mag_a == 0.0 or mag_b == 0.0:
            return 0.0
        return dot / (mag_a * mag_b)

    def _similarity(self, text_a: str, text_b: str) -> float:
        vec_a = self._tf_vector(self._tokenize(text_a))
        vec_b = self._tf_vector(self._tokenize(text_b))
        return self._cosine(vec_a, vec_b)

    def _row_to_entry(self, row: sqlite3.Row) -> CacheEntry:
        _fields = {f.name for f in CacheEntry.__dataclass_fields__.values()}
        return CacheEntry(**{k: row[k] for k in row.keys() if k in _fields})

    def _exact_match(self, query: str, task_type: str) -> Optional[CacheEntry]:
        q_hash = self._hash(query)
        row = self._conn.execute(
            "SELECT * FROM cache_entries WHERE query_hash = ? AND task_type = ? LIMIT 1",
            (q_hash, task_type),
        ).fetchone()
        return self._row_to_entry(row) if row else None

    def _semantic_match(self, query: str, task_type: str) -> Optional[CacheEntry]:
        """Scan all entries of same task_type; return best cosine match above threshold."""
        rows = self._conn.execute(
            "SELECT * FROM cache_entries WHERE task_type = ?",
            (task_type,),
        ).fetchall()
        best_score = 0.0
        best_entry: Optional[CacheEntry] = None
        for row in rows:
            score = self._similarity(query, row["query_text"])
            if score > best_score:
                best_score = score
                best_entry = self._row_to_entry(row)
        if best_score >= self.similarity_threshold:
            return best_entry
        return None

    def _record_hit(self, cache_id: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self._conn.execute(
            "UPDATE cache_entries SET hit_count = hit_count + 1, last_accessed = ? WHERE cache_id = ?",
            (now, cache_id),
        )
        self._conn.commit()
