#!/usr/bin/env python3
"""
Distillation Exporter — Captures high-quality agent invocations for fine-tuning.

Two-phase workflow
──────────────────
Phase 1 — Capture (during pipeline execution):
  Wrap each LLM call with DistillationCapture.capture() to persist
  (system_prompt, user_message, response, metrics) in SQLite.

Phase 2 — Export (after wave completes):
  DistillationExporter.filter_samples() selects high-quality pairs.
  export_jsonl_openai() or export_jsonl_anthropic() writes fine-tuning-ready JSONL.

Quality score formula (0.0 – 1.0)
──────────────────────────────────
  0.40 × gate_score            (0.0 if not captured for this invocation)
  0.40 × compression_efficiency = max(0, 1 – tokens_out / tokens_in)
  0.20 × success_flag          (1.0 if status == "success", else 0.0)

Recommended minimum thresholds
───────────────────────────────
  min_quality_score = 0.60   (decent signal)
  min_gate_score    = 0.80   (gate passed with margin — pattern is correct)

Usage
─────
    # Phase 1 — inside pipeline execution:
    capture = DistillationCapture("distillation.db")
    sid = capture.capture(
        task_name="entity_classification",
        system_prompt="You are a migration expert...",
        user_message="Classify these tables: customers, orders, products",
        response_text="customers→staging, orders→staging, products→target",
        tokens_in=800, tokens_out=120, cost_usd=0.003,
        wave_id="wave2", gate_score=0.84,
    )

    # Phase 2 — after wave completes:
    exporter = DistillationExporter("distillation.db")
    samples = exporter.filter_samples(min_quality_score=0.70, min_gate_score=0.80)
    n = exporter.export_jsonl_openai("wave2_finetune.jsonl", samples)
    print(f"Exported {n} training pairs")   # → "Exported 12 training pairs"
"""
from __future__ import annotations

import csv
import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class DistillationSample:
    """A single (input, output) training pair with provenance metadata."""
    sample_id: str
    task_name: str
    wave_id: str
    model: str
    system_prompt: str
    user_message: str
    response_text: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    gate_score: float
    quality_score: float
    status: str
    created_at: str


_DDL = """
CREATE TABLE IF NOT EXISTS samples (
    id             INTEGER PRIMARY KEY,
    sample_id      TEXT    NOT NULL UNIQUE,
    task_name      TEXT    NOT NULL,
    wave_id        TEXT    NOT NULL DEFAULT '',
    model          TEXT    NOT NULL DEFAULT '',
    system_prompt  TEXT    NOT NULL DEFAULT '',
    user_message   TEXT    NOT NULL,
    response_text  TEXT    NOT NULL,
    tokens_in      INTEGER NOT NULL DEFAULT 0,
    tokens_out     INTEGER NOT NULL DEFAULT 0,
    cost_usd       REAL    NOT NULL DEFAULT 0.0,
    gate_score     REAL    NOT NULL DEFAULT 0.0,
    quality_score  REAL    NOT NULL DEFAULT 0.0,
    status         TEXT    NOT NULL DEFAULT 'success',
    created_at     TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_dist_wave    ON samples(wave_id);
CREATE INDEX IF NOT EXISTS idx_dist_quality ON samples(quality_score);
CREATE INDEX IF NOT EXISTS idx_dist_gate    ON samples(gate_score);
"""


def _compute_quality(
    tokens_in: int,
    tokens_out: int,
    gate_score: float,
    status: str,
) -> float:
    """
    Quality score = 0.40 × gate_score
                  + 0.40 × compression_efficiency (1 − out/in)
                  + 0.20 × success_flag
    Result is clamped to [0.0, 1.0].
    """
    success = 1.0 if status == "success" else 0.0
    if tokens_in > 0:
        efficiency = max(0.0, min(1.0, 1.0 - tokens_out / tokens_in))
    else:
        efficiency = 0.5  # neutral when unknown
    score = 0.40 * gate_score + 0.40 * efficiency + 0.20 * success
    return round(min(1.0, max(0.0, score)), 4)


class DistillationCapture:
    """
    Records agent invocations for later distillation export.

    Designed to wrap any LLM call site — call capture() immediately after a
    successful invoke_agent() with the content and quality signals.
    Thread-safe via SQLite's check_same_thread=False.
    """

    def __init__(self, db_path: str = "distillation_capture.db") -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_DDL)
        self._conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "DistillationCapture":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def capture(
        self,
        task_name: str,
        user_message: str,
        response_text: str,
        *,
        wave_id: str = "",
        model: str = "",
        system_prompt: str = "",
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        gate_score: float = 0.0,
        status: str = "success",
    ) -> str:
        """
        Capture one invocation.

        Returns the generated sample_id.
        Duplicate sample_ids are silently ignored (INSERT OR IGNORE).
        """
        quality = _compute_quality(tokens_in, tokens_out, gate_score, status)
        sample_id = f"ds_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()

        self._conn.execute(
            """INSERT OR IGNORE INTO samples
               (sample_id, task_name, wave_id, model, system_prompt, user_message,
                response_text, tokens_in, tokens_out, cost_usd, gate_score,
                quality_score, status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                sample_id, task_name, wave_id, model, system_prompt,
                user_message, response_text, tokens_in, tokens_out,
                cost_usd, gate_score, quality, status, now,
            ),
        )
        self._conn.commit()
        return sample_id


class DistillationExporter:
    """
    Reads captured samples and exports fine-tuning datasets.

    Export formats:
      export_jsonl_openai()     → {"messages": [{role,content}, ...]}
      export_jsonl_anthropic()  → {"system": "...", "messages": [...]}
      export_csv()              → human-review CSV with previews
    """

    def __init__(self, db_path: str = "distillation_capture.db") -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        # Idempotent — safe to run on a DB created by DistillationCapture
        self._conn.executescript(_DDL)
        self._conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "DistillationExporter":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def filter_samples(
        self,
        min_quality_score: float = 0.60,
        min_gate_score: float = 0.0,
        max_cost_usd: Optional[float] = None,
        wave_id: Optional[str] = None,
        task_name: Optional[str] = None,
    ) -> List[DistillationSample]:
        """Return samples matching the given quality filters, ordered by quality desc."""
        sql = "SELECT * FROM samples WHERE quality_score >= ? AND gate_score >= ?"
        params: list = [min_quality_score, min_gate_score]

        if max_cost_usd is not None:
            sql += " AND cost_usd <= ?"
            params.append(max_cost_usd)
        if wave_id is not None:
            sql += " AND wave_id = ?"
            params.append(wave_id)
        if task_name is not None:
            sql += " AND task_name = ?"
            params.append(task_name)

        sql += " ORDER BY quality_score DESC"
        rows = self._conn.execute(sql, params).fetchall()
        _fields = {f.name for f in DistillationSample.__dataclass_fields__.values()}
        return [
            DistillationSample(**{k: row[k] for k in row.keys() if k in _fields})
            for row in rows
        ]

    def export_jsonl_openai(
        self,
        output_path: str | Path,
        samples: List[DistillationSample],
    ) -> int:
        """
        Write OpenAI fine-tuning JSONL.
        Each line: {"messages": [{"role":"system",...}, {"role":"user",...}, {"role":"assistant",...}]}
        system message is omitted when system_prompt is empty.
        Returns number of lines written.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for s in samples:
                messages = []
                if s.system_prompt:
                    messages.append({"role": "system", "content": s.system_prompt})
                messages.append({"role": "user", "content": s.user_message})
                messages.append({"role": "assistant", "content": s.response_text})
                f.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
                count += 1
        return count

    def export_jsonl_anthropic(
        self,
        output_path: str | Path,
        samples: List[DistillationSample],
    ) -> int:
        """
        Write Anthropic fine-tuning JSONL.
        Each line: {"system": "...", "messages": [{"role":"user",...}, {"role":"assistant",...}]}
        system key is omitted when system_prompt is empty.
        Returns number of lines written.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for s in samples:
                record: Dict = {
                    "messages": [
                        {"role": "user", "content": s.user_message},
                        {"role": "assistant", "content": s.response_text},
                    ]
                }
                if s.system_prompt:
                    record["system"] = s.system_prompt
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
        return count

    def export_csv(
        self,
        output_path: str | Path,
        samples: List[DistillationSample],
        preview_chars: int = 120,
    ) -> int:
        """
        Write CSV for human review.
        Full prompt/response text is truncated to preview_chars for readability.
        Returns number of rows written (excluding header).
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "sample_id", "task_name", "wave_id", "model",
            "quality_score", "gate_score", "tokens_in", "tokens_out",
            "cost_usd", "status", "created_at",
            "user_message_preview", "response_preview",
        ]
        count = 0
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in samples:
                writer.writerow({
                    "sample_id": s.sample_id,
                    "task_name": s.task_name,
                    "wave_id": s.wave_id,
                    "model": s.model,
                    "quality_score": s.quality_score,
                    "gate_score": s.gate_score,
                    "tokens_in": s.tokens_in,
                    "tokens_out": s.tokens_out,
                    "cost_usd": s.cost_usd,
                    "status": s.status,
                    "created_at": s.created_at,
                    "user_message_preview": s.user_message[:preview_chars],
                    "response_preview": s.response_text[:preview_chars],
                })
                count += 1
        return count

    def get_statistics(
        self, samples: Optional[List[DistillationSample]] = None
    ) -> Dict:
        """
        Summary statistics.
        If samples is None, reads all captured samples from the DB (no filter).
        """
        if samples is None:
            samples = self.filter_samples(min_quality_score=0.0)
        if not samples:
            return {"total_samples": 0}

        scores = [s.quality_score for s in samples]
        by_task: Dict[str, int] = {}
        for s in samples:
            by_task[s.task_name] = by_task.get(s.task_name, 0) + 1

        return {
            "total_samples": len(samples),
            "avg_quality_score": round(sum(scores) / len(scores), 4),
            "min_quality_score": round(min(scores), 4),
            "max_quality_score": round(max(scores), 4),
            "total_cost_usd": round(sum(s.cost_usd for s in samples), 6),
            "total_tokens_in": sum(s.tokens_in for s in samples),
            "total_tokens_out": sum(s.tokens_out for s in samples),
            "by_task_name": by_task,
        }
