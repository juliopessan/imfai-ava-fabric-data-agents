"""
kpi_dashboard_report.py
B-015 — Wave KPI dashboard report artifact.

Consumes wave execution metrics (first-pass rate, rollback count, MTTR,
cycle time) and produces a structured per-KPI report with actual vs target
comparison and a PASS/FAIL status for each KPI.

Usage:
    from scripts.kpi_dashboard_report import (
        WaveExecutionMetrics,
        generate_kpi_dashboard_report,
    )

    metrics = WaveExecutionMetrics(
        wave_id="WAVE-001",
        first_pass_rate_pct=98.5,
        rollback_count=0,
        mttr_minutes=0.0,
        cycle_time_minutes=120.0,
    )
    report = generate_kpi_dashboard_report(metrics)
    for row in report.rows:
        print(row.kpi_id, row.actual, row.status)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ReportStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"


@dataclass
class WaveExecutionMetrics:
    """Execution-level metrics collected after a migration wave completes."""
    wave_id: str
    first_pass_rate_pct: float   # % entities migrated without rollback on first try
    rollback_count: int          # number of rollback events during the wave
    mttr_minutes: float          # mean time to recovery (minutes)
    cycle_time_minutes: float    # total elapsed time from start to validated (minutes)


@dataclass
class KPIReportRow:
    """One row in the KPI dashboard report."""
    kpi_id: str
    kpi_name: str
    actual: str           # human-readable actual value string
    target: str           # human-readable target string
    status: ReportStatus


@dataclass
class KPIDashboardReport:
    """Full KPI dashboard report for a single wave."""
    wave_id: str
    rows: list[KPIReportRow]
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ---------------------------------------------------------------------------
# KPI definitions: thresholds and targets
# ---------------------------------------------------------------------------

_KPI_SPECS = [
    {
        "kpi_id": "first_pass_rate",
        "kpi_name": "First-Pass Rate",
        "target": "≥ 95%",
        "threshold": 95.0,
        "comparison": "gte",
        "unit": "pct",
        "field": "first_pass_rate_pct",
    },
    {
        "kpi_id": "rollback_count",
        "kpi_name": "Rollback Count",
        "target": "= 0",
        "threshold": 0,
        "comparison": "lte",
        "unit": "count",
        "field": "rollback_count",
    },
    {
        "kpi_id": "mttr",
        "kpi_name": "Mean Time to Recovery",
        "target": "≤ 60 min",
        "threshold": 60.0,
        "comparison": "lte",
        "unit": "minutes",
        "field": "mttr_minutes",
    },
    {
        "kpi_id": "cycle_time",
        "kpi_name": "Migration Cycle Time",
        "target": "≤ 240 min",
        "threshold": 240.0,
        "comparison": "lte",
        "unit": "minutes",
        "field": "cycle_time_minutes",
    },
]


def _evaluate_status(comparison: str, actual: float, threshold: float) -> ReportStatus:
    if comparison == "gte":
        return ReportStatus.PASS if actual >= threshold else ReportStatus.FAIL
    if comparison == "lte":
        return ReportStatus.PASS if actual <= threshold else ReportStatus.FAIL
    return ReportStatus.PARTIAL


def generate_kpi_dashboard_report(metrics: WaveExecutionMetrics) -> KPIDashboardReport:
    """Generate a per-KPI dashboard report from wave execution metrics.

    Args:
        metrics: Execution data collected after the wave completes.

    Returns:
        KPIDashboardReport with one KPIReportRow per KPI.
    """
    rows: list[KPIReportRow] = []
    for spec in _KPI_SPECS:
        actual_val = getattr(metrics, spec["field"])
        status = _evaluate_status(spec["comparison"], float(actual_val), float(spec["threshold"]))
        unit = spec["unit"]
        if unit == "pct":
            actual_str = f"{actual_val:.1f}%"
        elif unit == "minutes":
            actual_str = f"{actual_val:.1f} min"
        else:
            actual_str = str(actual_val)
        rows.append(KPIReportRow(
            kpi_id=spec["kpi_id"],
            kpi_name=spec["kpi_name"],
            actual=actual_str,
            target=spec["target"],
            status=status,
        ))
    return KPIDashboardReport(wave_id=metrics.wave_id, rows=rows)
