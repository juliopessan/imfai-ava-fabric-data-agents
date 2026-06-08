#!/usr/bin/env python3
"""Validator for Gate 1 artifacts.

Checks presence of STTM, DQ rules, problem statement and inventory report.
Prints JSON: {path, valid, completeness, missing} and returns 0/2.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ["sttm.md", "dq-rules.md", "gate1-problem-statement.md", "inventory-report.md"]


def validate_gate1(path: Path) -> dict:
    p = path
    missing = [r for r in REQUIRED if not (p / r).exists()]
    found = len(REQUIRED) - len(missing)
    completeness = found / len(REQUIRED)
    return {"path": str(p), "valid": len(missing) == 0, "completeness": completeness, "missing": missing}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args(argv)
    res = validate_gate1(Path(args.path))
    print(json.dumps(res))
    return 0 if res["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
