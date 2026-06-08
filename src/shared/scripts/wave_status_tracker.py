#!/usr/bin/env python3
"""Wave status tracker aggregates validator outputs and gate score."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import (
    validate_gate1_artifacts,
    validate_gate2_artifacts,
    validate_gate3_artifacts,
    gate_score_report,
)


def build_status(path: Path) -> dict[str, Any]:
    p = path
    g1 = validate_gate1_artifacts.validate_gate1(p)
    g2 = validate_gate2_artifacts.validate_gate_requirements(p)
    g3 = validate_gate3_artifacts.validate_gate3(p)
    score = gate_score_report.compute_score(p)

    status = {
        "path": str(p),
        "gate1": g1,
        "gate2": g2,
        "gate3": g3,
        "gateScoreReport": score,
    }
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args(argv)
    report = build_status(Path(args.path))
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
