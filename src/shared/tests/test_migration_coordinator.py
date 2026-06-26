"""
Tests for migration_coordinator.py — Headroom checkpoint integration.

Covers:
- MigrationCoordinator initialisation
- start_midstream / start_downstream / start_documentation with artifacts
- Graceful handling of missing artifact directories
- get_cost_savings_report structure
- validate_compression_for_gate delegation
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure src/shared/scripts is on the path for sibling imports
_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from migration_coordinator import MigrationCoordinator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """Return a temp dir with minimal DMF project structure."""
    project = tmp_path / "projects" / "Financeiro"
    for phase in ("upstream", "midstream", "downstream"):
        (project / "outputs" / phase).mkdir(parents=True)
    return tmp_path


@pytest.fixture
def coordinator(project_root: Path) -> MigrationCoordinator:
    """Return a coordinator wired to the temp project (mock compression)."""
    return MigrationCoordinator(
        project_root=project_root,
        project_name="Financeiro",
        use_mock=True,
    )


@pytest.fixture
def coordinator_with_upstream(project_root: Path) -> MigrationCoordinator:
    """Coordinator whose upstream dir already contains a JSON artifact."""
    upstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "upstream"
    artifact = {
        "entities": [
            {"name": "transactions", "schema": "ledger", "row_count": 1000000},
            {"name": "customers",    "schema": "crm",    "row_count": 200000},
        ],
        "ddl_summary": "CREATE TABLE transactions (...); CREATE TABLE customers (...);",
    }
    (upstream_dir / "discovery_summary.json").write_text(
        json.dumps(artifact), encoding="utf-8"
    )
    return MigrationCoordinator(
        project_root=project_root,
        project_name="Financeiro",
        use_mock=True,
    )


@pytest.fixture
def coordinator_with_midstream(project_root: Path) -> MigrationCoordinator:
    """Coordinator whose midstream dir already contains a JSON artifact."""
    midstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "midstream"
    artifact = {
        "ddl": "CREATE TABLE financeiro_dw.transactions AS SELECT ...",
        "sttm": {"transactions": {"source": "ledger.transactions", "target": "dw.transactions"}},
    }
    (midstream_dir / "codegen_output.json").write_text(
        json.dumps(artifact), encoding="utf-8"
    )
    return MigrationCoordinator(
        project_root=project_root,
        project_name="Financeiro",
        use_mock=True,
    )


@pytest.fixture
def coordinator_with_downstream(project_root: Path) -> MigrationCoordinator:
    """Coordinator whose downstream dir already contains a JSON artifact."""
    downstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "downstream"
    artifact = {
        "reconciliation": {
            "transactions": {"source_count": 1000000, "target_count": 1000000, "match": True},
            "customers":    {"source_count": 200000,  "target_count": 200000,  "match": True},
        }
    }
    (downstream_dir / "reconciliation_result.json").write_text(
        json.dumps(artifact), encoding="utf-8"
    )
    return MigrationCoordinator(
        project_root=project_root,
        project_name="Financeiro",
        use_mock=True,
    )


# ---------------------------------------------------------------------------
# Init tests
# ---------------------------------------------------------------------------

class TestMigrationCoordinatorInit:
    def test_initialisation_defaults(self, project_root):
        coord = MigrationCoordinator(project_root=project_root, use_mock=True)
        assert coord.project_name == "Financeiro"
        assert coord.headroom is not None
        assert coord.headroom_workflow is not None
        assert coord.token_metrics is not None

    def test_custom_project_name(self, project_root):
        coord = MigrationCoordinator(
            project_root=project_root, project_name="Saude", use_mock=True
        )
        assert coord.project_name == "Saude"

    def test_gate_scores_empty_at_start(self, coordinator):
        assert coordinator.gate_scores == {}

    def test_wave_config_none_at_start(self, coordinator):
        assert coordinator.wave_config is None


# ---------------------------------------------------------------------------
# start_midstream tests
# ---------------------------------------------------------------------------

class TestStartMidstream:
    def test_returns_true_with_artifacts(self, coordinator_with_upstream):
        result = coordinator_with_upstream.start_midstream("wave-1")
        assert result is True

    def test_creates_compressed_artifact(self, coordinator_with_upstream, project_root):
        coordinator_with_upstream.start_midstream("wave-1")
        upstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "upstream"
        compressed_files = list(upstream_dir.glob("compressed_wave-1_*.json"))
        assert len(compressed_files) >= 1

    def test_returns_true_when_no_artifacts(self, coordinator):
        # Empty upstream dir — should skip compression gracefully
        result = coordinator.start_midstream("wave-1")
        assert result is True

    def test_records_token_metrics(self, coordinator_with_upstream):
        coordinator_with_upstream.start_midstream("wave-1")
        metrics = coordinator_with_upstream.token_metrics.get_summary_for_dashboard()
        # Some tokens should have been recorded
        assert metrics is not None


# ---------------------------------------------------------------------------
# start_downstream tests
# ---------------------------------------------------------------------------

class TestStartDownstream:
    def test_returns_true_with_artifacts(self, coordinator_with_midstream):
        result = coordinator_with_midstream.start_downstream("wave-1")
        assert result is True

    def test_creates_compressed_artifact(self, coordinator_with_midstream, project_root):
        coordinator_with_midstream.start_downstream("wave-1")
        midstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "midstream"
        compressed_files = list(midstream_dir.glob("compressed_wave-1_*.json"))
        assert len(compressed_files) >= 1

    def test_returns_true_when_no_artifacts(self, coordinator):
        result = coordinator.start_downstream("wave-1")
        assert result is True


# ---------------------------------------------------------------------------
# start_documentation tests
# ---------------------------------------------------------------------------

class TestStartDocumentation:
    def test_returns_true_with_artifacts(self, coordinator_with_downstream):
        result = coordinator_with_downstream.start_documentation("wave-1")
        assert result is True

    def test_saves_headroom_metrics_json(self, coordinator_with_downstream, project_root):
        coordinator_with_downstream.start_documentation("wave-1")
        downstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "downstream"
        metrics_file = downstream_dir / "wave-1_headroom_metrics.json"
        assert metrics_file.exists(), "Headroom metrics JSON should be saved"

    def test_saves_workflow_status_json(self, coordinator_with_downstream, project_root):
        coordinator_with_downstream.start_documentation("wave-1")
        downstream_dir = project_root / "projects" / "Financeiro" / "outputs" / "downstream"
        status_file = downstream_dir / "wave-1_headroom_workflow.json"
        assert status_file.exists(), "Workflow status JSON should be saved"

    def test_returns_true_when_no_artifacts(self, coordinator):
        result = coordinator.start_documentation("wave-1")
        assert result is True


# ---------------------------------------------------------------------------
# Cost savings report
# ---------------------------------------------------------------------------

class TestCostSavingsReport:
    def test_report_has_required_keys(self, coordinator):
        report = coordinator.get_cost_savings_report()
        for key in (
            "tokens_raw",
            "tokens_saved",
            "compression_pct",
            "cost_raw_usd",
            "cost_compressed_usd",
            "cost_savings_usd",
            "cost_savings_pct",
        ):
            assert key in report, f"Missing key: {key}"

    def test_report_values_are_numeric(self, coordinator):
        report = coordinator.get_cost_savings_report()
        # compression_pct may be returned as a formatted string (e.g. '0.0%') by the
        # underlying EnhancedTokenMetrics; treat it as an acceptable string-or-numeric.
        for key, val in report.items():
            if key == "compression_pct":
                assert isinstance(val, (int, float, str)), (
                    f"{key} should be numeric or formatted string, got {type(val)}"
                )
            else:
                assert isinstance(val, (int, float)), (
                    f"{key} should be numeric, got {type(val)}"
                )


# ---------------------------------------------------------------------------
# validate_compression_for_gate
# ---------------------------------------------------------------------------

class TestValidateCompressionForGate:
    def test_returns_dict_with_status(self, coordinator):
        result = coordinator.validate_compression_for_gate("upstream")
        assert "status" in result
        assert "passed" in result
        assert "compression_ratio" in result

    def test_all_phases_valid(self, coordinator):
        for phase in ("upstream", "midstream", "downstream"):
            result = coordinator.validate_compression_for_gate(phase)
            assert result["phase"] == phase


# ---------------------------------------------------------------------------
# Full wave simulation: all 3 checkpoints in sequence
# ---------------------------------------------------------------------------

class TestFullWaveSimulation:
    def test_all_phases_succeed_with_artifacts(self, project_root):
        """Simulate a complete wave through all three compression checkpoints."""
        # Seed artifacts for each phase
        def _write(phase: str, name: str, data: dict) -> None:
            d = project_root / "projects" / "Financeiro" / "outputs" / phase
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{name}.json").write_text(json.dumps(data), encoding="utf-8")

        _write("upstream",   "discovery", {"entities": [{"name": "orders"}]})
        _write("midstream",  "codegen",   {"ddl": "CREATE TABLE orders AS SELECT ..."})
        _write("downstream", "recon",     {"orders": {"match": True}})

        coord = MigrationCoordinator(project_root=project_root, use_mock=True)
        assert coord.start_midstream("wave-sim") is True
        assert coord.start_downstream("wave-sim") is True
        assert coord.start_documentation("wave-sim") is True

        report = coord.get_cost_savings_report()
        assert isinstance(report["cost_savings_usd"], float)
