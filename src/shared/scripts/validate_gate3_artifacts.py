#!/usr/bin/env python3
"""Stub validator for Gate 3 artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_gate3(path: Path) -> dict:
    p = path
    required = ["reconciliation-report.md", "runbook.md", "reconciliation-checks.json"]
    missing = [r for r in required if not (p / r).exists()]
    completeness = (len(required) - len(missing)) / len(required)
    return {"path": str(p), "valid": len(missing) == 0, "completeness": completeness, "missing": missing}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args(argv)
    res = validate_gate3(Path(args.path))
    print(json.dumps(res))
    return 0 if res["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
