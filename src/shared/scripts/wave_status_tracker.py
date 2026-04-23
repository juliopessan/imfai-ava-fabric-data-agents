"""
wave_status_tracker.py
Consolidates wave status across all three gates: artifact completeness,
gate scores, and overall readiness.

Consumes validate_gate_requirements() for artifact checks and provides
a unified status view per wave.

Usage:
    from scripts.wave_status_tracker import WaveStatusTracker

    tracker = WaveStatusTracker(wave_id="WAVE-001")
    tracker.set_gate_artifacts(1, present=5, total=5)
    tracker.set_gate_artifacts(2, present=4, total=5)
    tracker.set_gate_artifacts(3, present=0, total=8)
    tracker.set_gate_score(1, 88.0)
    print(tracker.summary())
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class PhaseStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    BLOCKED = "BLOCKED"


@dataclass
class GateStatus:
    gate: int
    artifacts_present: int = 0
    artifacts_total: int = 0
    gate_score: float | None = None

    @property
    def artifacts_pct(self) -> float:
        if self.artifacts_total == 0:
            return 0.0
        return round(self.artifacts_present / self.artifacts_total * 100, 1)

    @property
    def phase_status(self) -> PhaseStatus:
        if self.artifacts_present == 0:
            return PhaseStatus.NOT_STARTED
        if self.artifacts_present < self.artifacts_total:
            return PhaseStatus.IN_PROGRESS
        if self.gate_score is not None and self.gate_score < 70.0:
            return PhaseStatus.BLOCKED
        return PhaseStatus.COMPLETE


@dataclass
class WaveStatusSummary:
    wave_id: str
    gates: list[GateStatus]
    overall_pct: float
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __str__(self) -> str:
        lines = [f"Wave Status: {self.wave_id}  (overall: {self.overall_pct:.0f}%)"]
        for g in self.gates:
            score_str = f"score={g.gate_score:.1f}" if g.gate_score is not None else "score=N/A"
            lines.append(
                f"  Gate {g.gate}: {g.phase_status.value}  "
                f"artifacts={g.artifacts_present}/{g.artifacts_total} ({g.artifacts_pct}%)  "
                f"{score_str}"
            )
        return "\n".join(lines)


class WaveStatusTracker:
    """Tracks per-gate artifact completion and scores for a migration wave."""

    def __init__(self, wave_id: str) -> None:
        self.wave_id = wave_id
        self._gates: dict[int, GateStatus] = {
            1: GateStatus(gate=1),
            2: GateStatus(gate=2),
            3: GateStatus(gate=3),
        }

    def set_gate_artifacts(self, gate: int, present: int, total: int) -> None:
        if gate not in self._gates:
            raise ValueError(f"Invalid gate: {gate}. Must be 1, 2, or 3.")
        self._gates[gate].artifacts_present = present
        self._gates[gate].artifacts_total = total

    def set_gate_score(self, gate: int, score: float) -> None:
        if gate not in self._gates:
            raise ValueError(f"Invalid gate: {gate}. Must be 1, 2, or 3.")
        self._gates[gate].gate_score = score

    def summary(self) -> WaveStatusSummary:
        gates = [self._gates[g] for g in sorted(self._gates)]
        total_artifacts = sum(g.artifacts_total for g in gates)
        present_artifacts = sum(g.artifacts_present for g in gates)
        overall_pct = (
            round(present_artifacts / total_artifacts * 100, 1)
            if total_artifacts > 0
            else 0.0
        )
        return WaveStatusSummary(
            wave_id=self.wave_id,
            gates=gates,
            overall_pct=overall_pct,
        )
