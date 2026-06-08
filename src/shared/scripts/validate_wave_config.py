#!/usr/bin/env python3
"""Validate wave-config.yaml contents.

Checks required properties: 'wave_id' or 'name', 'discovery_owner_primary', and 'scope' (list).
Outputs JSON: {path, valid, errors} and returns 0 if valid else 2.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml


def validate_wave_config(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return False, [f"file not found: {path}"]
    try:
        data = yaml.safe_load(path.read_text()) or {}
    except Exception as ex:
        return False, [f"yaml parse error: {ex}"]

    if not (data.get("wave_id") or data.get("name")):
        errors.append("missing 'wave_id' or 'name'")
    if not data.get("discovery_owner_primary"):
        errors.append("missing 'discovery_owner_primary'")
    scope = data.get("scope") or data.get("entities")
    if not scope or not isinstance(scope, (list, tuple)):
        errors.append("missing or invalid 'scope' (expected list of entities)")

    return (len(errors) == 0), errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="wave-config.yaml")
    args = parser.parse_args(argv)
    p = Path(args.path)
    ok, errors = validate_wave_config(p)
    out = {"path": str(p), "valid": ok, "errors": errors}
    print(json.dumps(out))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
