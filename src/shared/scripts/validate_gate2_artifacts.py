#!/usr/bin/env python3
"""Minimal Gate 2 artifacts validator (scaffold).

This file is a lightweight stub to enable CI/testing scaffolding.
Replace with the project's real validation logic when available.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate_gate_requirements(path: str | Path, return_dict: bool = False):
    p = Path(path)
    if not p.exists():
        return False if not return_dict else {"path": str(p), "valid": False, "completeness": 0.0, "found": []}
    required = ["architecture.md", "data-model.md", "data-contracts.md", "decisions.md"]
    found = [r for r in required if (p / r).exists()]
    # completeness as ratio
    completeness = len(found) / len(required)
    # Legacy behavior: consider valid if architecture.md or data-model.md exists
    legacy_ok = (p / "architecture.md").exists() or (p / "data-model.md").exists()
    valid = True if legacy_ok else (completeness == 1.0)
    result = {"path": str(p), "valid": valid, "completeness": completeness, "found": found}
    return result if return_dict else result["valid"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Gate 2 artifact package (scaffold)")
    parser.add_argument("path", nargs="?", default=".", help="Path to artifact package")
    args = parser.parse_args(argv)
    res = validate_gate_requirements(args.path)
    print(json.dumps(res))
    return 0 if res.get("valid") else 2


if __name__ == "__main__":
    raise SystemExit(main())
