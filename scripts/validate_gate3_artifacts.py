"""
validate_gate3_artifacts.py
B-006 — validates Gate 3 artifact package (downstream wave output) before
production promotion.

Also supports Gate 1 and Gate 2 via validate_gate_requirements(gate, path).

Usage (standalone):
    python -m scripts.validate_gate3_artifacts <wave_output_dir>
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- Canonical artifact requirements (mirrors orchestrator core-config.yaml) ---

GATE_3_REQUIRED: list[str] = [
    "ddl/",
    "etl/",
    "tests/",
    "documentation/",
    "wave-report.md",
    "documentation/execution-runbook.md",
    "documentation/quality-gate-evidence.md",
    "documentation/reconciliation-evidence.md",
]

GATE_2_REQUIRED: list[str] = [
    "architecture.md",
    "data-model.md",
    "decisions.md",
    "dq-rules.md",
    "monitoring-spec.md",
]

GATE_1_REQUIRED: list[str] = [
    "problem-statement.md",
    "kpis.md",
    "analytical-questions.md",
    "sttm.md",
    "dq-initial.md",
]

GATE_REQUIRED: dict[int, list[str]] = {
    1: GATE_1_REQUIRED,
    2: GATE_2_REQUIRED,
    3: GATE_3_REQUIRED,
}


@dataclass
class ValidationResult:
    is_valid: bool
    missing: list[str] = field(default_factory=list)
    present: list[str] = field(default_factory=list)
    gate: int = 3

    def __str__(self) -> str:
        lines = [f"Gate {self.gate} validation: {'PASS' if self.is_valid else 'FAIL'}"]
        for p in self.present:
            lines.append(f"  ✓  {p}")
        for m in self.missing:
            lines.append(f"  ✗  {m}  (MISSING)")
        return "\n".join(lines)


def _check_path(root: Path, artifact: str) -> bool:
    """Return True if *artifact* exists under root.  Trailing '/' = directory."""
    target = root / artifact.rstrip("/")
    return target.exists()


def validate_gate_requirements(gate: int, artifact_root: Path) -> ValidationResult:
    """Generic gate validator for gate 1, 2, or 3."""
    required = GATE_REQUIRED.get(gate, [])
    missing: list[str] = []
    present: list[str] = []
    for artifact in required:
        if _check_path(artifact_root, artifact):
            present.append(artifact)
        else:
            missing.append(artifact)
    return ValidationResult(is_valid=len(missing) == 0, missing=missing, present=present, gate=gate)


def validate_gate3_requirements(wave_root: Path) -> ValidationResult:
    """Convenience wrapper: validate Gate 3 (downstream wave) artifacts."""
    return validate_gate_requirements(3, wave_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate gate artifact package before production promotion"
    )
    parser.add_argument("path", help="Wave output directory to validate")
    parser.add_argument("--gate", type=int, default=3, choices=[1, 2, 3], help="Gate number (default: 3)")
    args = parser.parse_args(argv)

    result = validate_gate_requirements(args.gate, Path(args.path).resolve())
    print(result)
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
