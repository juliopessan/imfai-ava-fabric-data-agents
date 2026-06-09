"""Shared pytest fixtures for DMF governance tests."""

import pytest
import json
import tempfile
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        
        # Create standard DMF project structure
        (project_path / "wave-config.yaml").touch()
        (project_path / "outputs" / "upstream").mkdir(parents=True)
        (project_path / "outputs" / "midstream").mkdir(parents=True)
        (project_path / "outputs" / "downstream").mkdir(parents=True)
        
        yield project_path


@pytest.fixture
def sample_wave_config():
    """Sample wave-config.yaml structure."""
    return {
        "wave_id": "bradesco-wave-001",
        "project_name": "Bradesco Migration",
        "discovery_owner": "alice@company.com",
        "target_platform": "databricks",
        "entities": [
            {"name": "customers", "source_schema": "crm"},
            {"name": "transactions", "source_schema": "ledger"}
        ],
        "gates": {
            "gate1_required": True,
            "gate2_required": True,
            "gate3_required": True
        }
    }


@pytest.fixture
def sample_gate1_artifacts():
    """Sample Gate 1 (Upstream) artifacts."""
    return {
        "discovery_inventory": {
            "total_tables": 45,
            "total_views": 12,
            "total_schemas": 8
        },
        "data_lineage": {
            "lineage_paths": 34,
            "dependencies": 67
        },
        "risk_assessment": {
            "high_risk_entities": 3,
            "medium_risk_entities": 8
        }
    }


@pytest.fixture
def sample_gate2_artifacts():
    """Sample Gate 2 (Midstream) artifacts."""
    return {
        "data_model": {
            "entities": 45,
            "relationships": 23,
            "attributes": 234
        },
        "architecture_decisions": {
            "decisions_count": 12,
            "assumptions_count": 8
        },
        "data_contracts": {
            "contracts": 15,
            "sla_definitions": 10
        }
    }


@pytest.fixture
def sample_gate3_artifacts():
    """Sample Gate 3 (Downstream) artifacts."""
    return {
        "deployment": {
            "ddl_objects": 45,
            "etl_jobs": 12,
            "tests_defined": 78
        },
        "reconciliation": {
            "row_count_passed": 43,
            "schema_diff_passed": 45
        },
        "validation": {
            "dbt_tests_passed": 156,
            "dq_rules_passed": 89
        }
    }


@pytest.fixture
def gate_score_formula():
    """GateScore calculation formula."""
    return {
        "completude_weight": 0.35,
        "quality_weight": 0.25,
        "residual_risk_weight": 0.20,
        "reconciliation_weight": 0.20,
        "approval_threshold": 0.85,
        "conditional_threshold": 0.70
    }


@pytest.fixture
def mock_logger(caplog):
    """Mock logger that captures log records."""
    import logging
    return caplog.records


class MockValidator:
    """Base mock validator for testing."""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data and return results."""
        return {
            "valid": True,
            "errors": [],
            "warnings": [],
            "score": 1.0
        }
