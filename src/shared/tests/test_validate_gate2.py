from pathlib import Path

from src.shared.scripts import validate_gate2_artifacts


def test_validate_missing_dir(tmp_path: Path) -> None:
    assert validate_gate2_artifacts.validate_gate_requirements(tmp_path) is False


def test_validate_with_architecture(tmp_path: Path) -> None:
    (tmp_path / "architecture.md").write_text("# architecture")
    assert validate_gate2_artifacts.validate_gate_requirements(tmp_path) is True
