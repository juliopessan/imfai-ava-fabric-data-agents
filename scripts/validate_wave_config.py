"""
validate_wave_config.py
B-017 — Enforces that every wave config declares a primary AND fallback
discovery owner. Used by CI and by gate pre-checks.

Usage (standalone):
    python -m scripts.validate_wave_config <wave_config.yaml>
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


@dataclass
class WaveConfigValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        lines = [f"Wave config validation: {'PASS' if self.is_valid else 'FAIL'}"]
        for e in self.errors:
            lines.append(f"  ERROR   {e}")
        for w in self.warnings:
            lines.append(f"  WARNING {w}")
        return "\n".join(lines)


def validate_wave_config(config_path: Path) -> WaveConfigValidationResult:
    """Validate discovery ownership and required fields in a wave YAML config.

    B-017: the wave config MUST contain:
      discovery_owner_primary   — string, non-empty
      discovery_owner_fallback  — string, non-empty, different from primary
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not config_path.exists():
        return WaveConfigValidationResult(
            is_valid=False,
            errors=[f"Config file not found: {config_path}"],
        )

    if not _YAML_AVAILABLE:
        return WaveConfigValidationResult(
            is_valid=False,
            errors=["PyYAML is not installed. Run: pip install pyyaml"],
        )

    try:
        with config_path.open(encoding="utf-8") as fh:
            config = yaml.safe_load(fh) or {}
    except Exception as exc:  # noqa: BLE001
        return WaveConfigValidationResult(is_valid=False, errors=[f"YAML parse error: {exc}"])

    # B-017 checks
    primary = config.get("discovery_owner_primary", "").strip()
    fallback = config.get("discovery_owner_fallback", "").strip()

    if not primary:
        errors.append("discovery_owner_primary is missing or empty (B-017)")
    if not fallback:
        errors.append("discovery_owner_fallback is missing or empty (B-017)")
    if primary and fallback and primary == fallback:
        warnings.append(
            f"discovery_owner_primary and fallback are both '{primary}'. "
            "They should be different agents."
        )

    # B-008: non-dry-run waves MUST reference a validated runbook
    is_dry_run = config.get("dry_run", False)
    environment = (config.get("environment") or "").strip().upper()
    if environment in ("UAT", "PROD") and not is_dry_run:
        runbook_path = config.get("runbook_path", "").strip()
        if not runbook_path:
            errors.append(
                "runbook_path is required for non-dry-run UAT/PROD waves (B-008). "
                "Set dry_run: true or provide a runbook_path."
            )
        else:
            # Resolve relative to config file directory
            resolved = (config_path.parent / runbook_path).resolve()
            if not resolved.exists():
                errors.append(
                    f"runbook_path '{runbook_path}' does not exist (B-008). "
                    "Ensure the execution runbook is present before running."
                )

    # Optional wave metadata checks
    if not config.get("wave_id"):
        warnings.append("wave_id is not set — recommended for audit traceability")
    if not environment:
        warnings.append("environment is not set (DEV/UAT/PROD)")

    return WaveConfigValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate wave config YAML (B-017: discovery owner enforcement)"
    )
    parser.add_argument("config", help="Path to wave config YAML file")
    args = parser.parse_args(argv)

    result = validate_wave_config(Path(args.config).resolve())
    print(result)
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
