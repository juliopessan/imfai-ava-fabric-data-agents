"""
performance_benchmark.py
B-010 — Production-like performance benchmark stage for migration waves.

Computes rows/second for an entity load and compares against a baseline.
Produces a BenchmarkReport that must be present before production promotion.

Usage:
    from scripts.performance_benchmark import BenchmarkRun, run_benchmark

    run = BenchmarkRun(
        wave_id="WAVE-001",
        entity="orders",
        rows_processed=1_000_000,
        duration_seconds=60.0,
        baseline_rows_per_second=10_000.0,
    )
    report = run_benchmark(run)
    print(report)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class BenchmarkStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass
class BenchmarkRun:
    wave_id: str
    entity: str
    rows_processed: int
    duration_seconds: float
    baseline_rows_per_second: float
    # Optional tolerance: how far below baseline is acceptable (default 10%)
    tolerance_pct: float = 0.10


@dataclass
class BenchmarkReport:
    wave_id: str
    entity: str
    rows_per_second: float
    baseline_rows_per_second: float
    tolerance_pct: float
    status: BenchmarkStatus
    delta_pct: float          # (actual - baseline) / baseline
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __str__(self) -> str:
        sign = "+" if self.delta_pct >= 0 else ""
        return (
            f"Benchmark [{self.entity} / {self.wave_id}]: {self.status.value}\n"
            f"  Actual     : {self.rows_per_second:,.1f} rows/s\n"
            f"  Baseline   : {self.baseline_rows_per_second:,.1f} rows/s\n"
            f"  Delta      : {sign}{self.delta_pct:.1%}\n"
            f"  Tolerance  : -{self.tolerance_pct:.0%}"
        )


def run_benchmark(run: BenchmarkRun) -> BenchmarkReport:
    """Execute benchmark calculation for a single entity load."""
    if run.duration_seconds <= 0:
        raise ValueError(f"duration_seconds must be > 0, got {run.duration_seconds}")

    actual = run.rows_processed / run.duration_seconds
    delta = (actual - run.baseline_rows_per_second) / run.baseline_rows_per_second
    minimum = run.baseline_rows_per_second * (1.0 - run.tolerance_pct)
    status = BenchmarkStatus.PASS if actual >= minimum else BenchmarkStatus.FAIL

    return BenchmarkReport(
        wave_id=run.wave_id,
        entity=run.entity,
        rows_per_second=round(actual, 2),
        baseline_rows_per_second=run.baseline_rows_per_second,
        tolerance_pct=run.tolerance_pct,
        status=status,
        delta_pct=round(delta, 4),
    )
