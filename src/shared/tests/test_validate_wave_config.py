import tempfile
import unittest
from pathlib import Path

from scripts.validate_wave_config import validate_wave_config


def _write_config(directory: str, content: str) -> Path:
    p = Path(directory) / "wave-config.yaml"
    p.write_text(content, encoding="utf-8")
    return p


class ValidateWaveConfigTests(unittest.TestCase):
    def test_fails_when_discovery_primary_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(tmp, "wave_id: WAVE-001\nenvironment: DEV\n")
            result = validate_wave_config(cfg)
            self.assertFalse(result.is_valid)
            self.assertTrue(any("primary" in e for e in result.errors))

    def test_fails_when_discovery_fallback_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(
                tmp,
                "wave_id: WAVE-001\nenvironment: DEV\ndiscovery_owner_primary: discovery-scout\n",
            )
            result = validate_wave_config(cfg)
            self.assertFalse(result.is_valid)
            self.assertTrue(any("fallback" in e for e in result.errors))

    def test_passes_with_valid_discovery_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(
                tmp,
                (
                    "wave_id: WAVE-001\n"
                    "environment: DEV\n"
                    "discovery_owner_primary: discovery-scout\n"
                    "discovery_owner_fallback: inventory-scout\n"
                ),
            )
            result = validate_wave_config(cfg)
            self.assertTrue(result.is_valid)
            self.assertEqual([], result.errors)

    def test_warns_when_primary_and_fallback_are_same(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(
                tmp,
                (
                    "wave_id: WAVE-001\n"
                    "environment: DEV\n"
                    "discovery_owner_primary: discovery-scout\n"
                    "discovery_owner_fallback: discovery-scout\n"
                ),
            )
            result = validate_wave_config(cfg)
            self.assertTrue(result.is_valid)   # warnings don't fail
            self.assertTrue(len(result.warnings) > 0)

    def test_fails_when_file_not_found(self) -> None:
        result = validate_wave_config(Path("/nonexistent/wave-config.yaml"))
        self.assertFalse(result.is_valid)

    # B-008 tests
    def test_fails_when_prod_wave_missing_runbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(
                tmp,
                (
                    "wave_id: WAVE-001\n"
                    "environment: PROD\n"
                    "dry_run: false\n"
                    "discovery_owner_primary: discovery-scout\n"
                    "discovery_owner_fallback: inventory-scout\n"
                ),
            )
            result = validate_wave_config(cfg)
            self.assertFalse(result.is_valid)
            self.assertTrue(any("runbook" in e.lower() for e in result.errors))

    def test_passes_when_prod_wave_has_valid_runbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # Create the runbook file
            runbook = Path(tmp) / "runbook.md"
            runbook.write_text("# Runbook", encoding="utf-8")
            cfg = _write_config(
                tmp,
                (
                    "wave_id: WAVE-001\n"
                    "environment: PROD\n"
                    "dry_run: false\n"
                    "runbook_path: runbook.md\n"
                    "discovery_owner_primary: discovery-scout\n"
                    "discovery_owner_fallback: inventory-scout\n"
                ),
            )
            result = validate_wave_config(cfg)
            self.assertTrue(result.is_valid)

    def test_dry_run_prod_does_not_require_runbook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _write_config(
                tmp,
                (
                    "wave_id: WAVE-001\n"
                    "environment: PROD\n"
                    "dry_run: true\n"
                    "discovery_owner_primary: discovery-scout\n"
                    "discovery_owner_fallback: inventory-scout\n"
                ),
            )
            result = validate_wave_config(cfg)
            self.assertTrue(result.is_valid)


if __name__ == "__main__":
    unittest.main()
