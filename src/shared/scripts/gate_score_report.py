#!/usr/bin/env python3
"""Stub gate score reporter that computes a dummy GateScore."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import validate_gate1_artifacts, validate_gate2_artifacts, validate_gate3_artifacts


def compute_score(path: Path) -> dict[str, Any]:
    # Run gate validators and build simple metrics
    g1 = validate_gate1_artifacts.validate_gate1(path)
    g2 = validate_gate2_artifacts.validate_gate_requirements(path, return_dict=True)
    g3 = validate_gate3_artifacts.validate_gate3(path)

    # completeness metrics in [0,1]
    c1 = g1.get("completeness", 0)
    c2 = g2.get("completeness", 0) if isinstance(g2, dict) else 0
    c3 = g3.get("completeness", 0)

    # Heuristic quality and risk scores (placeholders)
    quality = (c1 + c2 + c3) / 3
    risk_residual = max(0.0, 1.0 - quality)
    reconciliation = c3

    gateScore = 0.35 * c1 + 0.25 * quality + 0.20 * risk_residual + 0.20 * reconciliation

    decision = "APPROVED" if gateScore >= 0.85 else ("APPROVED_WITH_REMARKS" if gateScore >= 0.7 else "BLOCKED")

    return {
        "path": str(path),
        "gateScore": round(gateScore, 3),
        "components": {"completeness_gate1": c1, "completeness_gate2": c2, "completeness_gate3": c3},
        "decision": decision,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args(argv)
    report = compute_score(Path(args.path))
    print(json.dumps(report))
    return 0 if report["decision"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
