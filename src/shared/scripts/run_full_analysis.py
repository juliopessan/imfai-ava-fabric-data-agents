#!/usr/bin/env python3
"""Orchestrator: run a sequential full-analysis workflow.

This runner attempts to execute a recommended sequence of validators and reports
if they are present in `src.shared.scripts`. For missing scripts it logs a warning
and continues. Designed to be safe to run in CI or locally.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List


SEQUENCE: List[str] = [
    "validate_wave_config",
    "validate_gate1_artifacts",
    "validate_gate2_artifacts",
    "validate_gate3_artifacts",
    "gate_score_report",
    "wave_status_tracker",
]


def module_exists(mod: str) -> bool:
    # check for module file under src/shared/scripts
    cwd = Path(__file__).resolve().parents[2]
    candidate = cwd / "shared" / "scripts" / f"{mod}.py"
    return candidate.exists()


def run_module(mod: str, target: str) -> int:
    cmd = [sys.executable, "-m", f"src.shared.scripts.{mod}", target]
    print(f"Running: {' '.join(cmd)}")
    proc = subprocess.run(cmd)
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run full analysis sequence")
    parser.add_argument("target", nargs="?", default=".", help="Path to project or artifact package")
    parser.add_argument("--stages", type=str, default=None, help="Comma-separated list of stages to run (defaults to full sequence)")
    parser.add_argument("--resume-from", type=str, default=None, help="Stage name to resume from (exclusive)")
    parser.add_argument("--mode", type=str, choices=["autonomous", "hitl"], default="autonomous", help="Run mode: autonomous or hitl (human-in-the-loop)")
    args = parser.parse_args(argv)

    # Determine stages to run
    if args.stages:
        stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    else:
        stages = SEQUENCE

    # If resume_from provided, skip stages up to and including that stage
    if args.resume_from:
        if args.resume_from not in stages:
            print(f"[WARN] resume-from stage '{args.resume_from}' not in selected stages; ignoring")
        else:
            idx = stages.index(args.resume_from)
            stages = stages[idx + 1 :]

    any_fail = False
    for mod in stages:
        if not module_exists(mod):
            print(f"[SKIP] module not found: {mod}")
            continue
        rc = run_module(mod, args.target)
        if rc != 0:
            print(f"[WARN] module {mod} returned non-zero exit code: {rc}")
            any_fail = True

        # If HITL mode, pause after each stage to allow human review/resume
        if args.mode == "hitl":
            print("\n[HITL PAUSE] Completed stage: %s" % mod)
            print("To resume, re-run this command with --resume-from %s --mode hitl" % mod)
            # Exit with a special code to indicate paused state
            return 2

    print("Full analysis run complete")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
