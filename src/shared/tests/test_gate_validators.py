"""Tests for Gate artifact validators and GateScore calculator."""

import pytest
import json
import yaml
from pathlib import Path
from src.shared.scripts.validate_gate1_artifacts import Gate1ArtifactsValidator
from src.shared.scripts.validate_gate2_artifacts import Gate2ArtifactsValidator
from src.shared.scripts.validate_gate3_artifacts import Gate3ArtifactsValidator
from src.shared.scripts.gate_score_report import GateScoreCalculator


class TestGate1Validator:
    """Test Gate 1 artifact validation."""
    
    def test_gate1_missing_directory(self, temp_project_dir):
        """Test Gate 1 fails when directory missing."""
        validator = Gate1ArtifactsValidator(temp_project_dir / "nonexistent")
        result = validator.validate()
        assert result.valid is False
        assert len(result.errors) > 0
    
    def test_gate1_missing_required_artifacts(self, temp_project_dir):
        """Test Gate 1 fails with missing required artifacts."""
        upstream_dir = temp_project_dir / "outputs" / "upstream"
        upstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create only some required artifacts
        (upstream_dir / "discovery_inventory.md").write_text("# Inventory\nTest content")
        
        validator = Gate1ArtifactsValidator(upstream_dir)
        result = validator.validate()
        
        assert result.valid is False
        assert result.completude < 1.0
        assert len(result.artifacts_missing) > 0
    
    def test_gate1_all_required_artifacts(self, temp_project_dir):
        """Test Gate 1 passes with all required artifacts."""
        upstream_dir = temp_project_dir / "outputs" / "upstream"
        upstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all required artifacts
        (upstream_dir / "discovery_inventory.md").write_text("# Inventory\n" + "x" * 100)
        (upstream_dir / "data_lineage_map.md").write_text("# Lineage\n" + "x" * 100)
        (upstream_dir / "STTM_BUSINESS_REQUIREMENTS.md").write_text("# STTM\nBusiness requirements")
        (upstream_dir / "as_is_architecture.md").write_text("# Architecture\n" + "x" * 100)
        (upstream_dir / "risk_assessment.json").write_text(json.dumps({"risks": []}))
        
        validator = Gate1ArtifactsValidator(upstream_dir)
        result = validator.validate()
        
        assert result.valid is True
        assert result.completude == 1.0
        assert len(result.artifacts_missing) == 0


class TestGate2Validator:
    """Test Gate 2 artifact validation."""
    
    def test_gate2_missing_required_artifacts(self, temp_project_dir):
        """Test Gate 2 fails with missing required artifacts."""
        midstream_dir = temp_project_dir / "outputs" / "midstream"
        midstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create only some artifacts
        (midstream_dir / "logical_data_model.json").write_text(json.dumps({"entities": []}))
        
        validator = Gate2ArtifactsValidator(midstream_dir)
        result = validator.validate()
        
        assert result.valid is False
        assert len(result.artifacts_missing) > 0
    
    def test_gate2_all_required_artifacts(self, temp_project_dir):
        """Test Gate 2 passes with all required artifacts."""
        midstream_dir = temp_project_dir / "outputs" / "midstream"
        midstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all required artifacts
        (midstream_dir / "logical_data_model.json").write_text(json.dumps({"entities": []}))
        (midstream_dir / "target_architecture.json").write_text(json.dumps({"services": []}))
        (midstream_dir / "ARCHITECTURE.md").write_text("# Architecture\n" + "x" * 200)
        (midstream_dir / "ARCHITECTURE_DECISIONS.md").write_text("# Decisions\n" + "x" * 100)
        (midstream_dir / "MONITORING_SPEC.md").write_text("# Monitoring\n" + "x" * 100)
        (midstream_dir / "DATA_CONTRACTS.md").write_text("# Contracts\nSLA: 99.9%")
        
        validator = Gate2ArtifactsValidator(midstream_dir)
        result = validator.validate()
        
        assert result.valid is True
        assert result.completude == 1.0


class TestGate3Validator:
    """Test Gate 3 artifact validation."""
    
    def test_gate3_fails_without_reconciliation(self, temp_project_dir):
        """Test Gate 3 critical failure without reconciliation."""
        downstream_dir = temp_project_dir / "outputs" / "downstream"
        downstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all artifacts except reconciliation
        (downstream_dir / "DDL_DELTA_TABLES.sql").write_text("CREATE TABLE test (id INT)")
        (downstream_dir / "ETL_CONSOLIDACAO_DATABRICKS_JOB.py").write_text("def main(): pass")
        (downstream_dir / "deployment_execution.json").write_text(json.dumps({"status": "completed"}))
        # Missing: validation_reconciliation.json
        (downstream_dir / "ROW_COUNT_RECONCILIATION.md").write_text("# Reconciliation")
        (downstream_dir / "SCHEMA_DIFF_VALIDATION.md").write_text("# Schema Diff")
        
        validator = Gate3ArtifactsValidator(downstream_dir)
        result = validator.validate()
        
        assert result.valid is False
        assert result.reconciliation == 0.0
    
    def test_gate3_reconciliation_passed(self, temp_project_dir):
        """Test Gate 3 passes with reconciliation."""
        downstream_dir = temp_project_dir / "outputs" / "downstream"
        downstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all required artifacts
        (downstream_dir / "DDL_DELTA_TABLES.sql").write_text("CREATE TABLE test (id INT)")
        (downstream_dir / "ETL_CONSOLIDACAO_DATABRICKS_JOB.py").write_text("def main(): pass")
        (downstream_dir / "deployment_execution.json").write_text(json.dumps({"status": "completed"}))
        (downstream_dir / "validation_reconciliation.json").write_text(json.dumps({
            "row_count_validation": "PASSED",
            "schema_validation": "PASSED",
            "data_quality_validation": "PASSED"
        }))
        (downstream_dir / "ROW_COUNT_RECONCILIATION.md").write_text("# Reconciliation")
        (downstream_dir / "SCHEMA_DIFF_VALIDATION.md").write_text("# Schema Diff")
        
        validator = Gate3ArtifactsValidator(downstream_dir)
        result = validator.validate()
        
        assert result.valid is True
        assert result.reconciliation > 0.9


class TestGateScoreCalculator:
    """Test GateScore calculation."""
    
    def test_gate_score_approved(self):
        """Test GateScore results in approval."""
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave-001")
        result = calculator.calculate(
            completude=0.95,
            quality=0.90,
            residual_risk=0.85,
            reconciliation=1.0
        )
        
        assert result.status == "approved"
        assert result.score >= 0.85
    
    def test_gate_score_conditional(self):
        """Test GateScore results in conditional approval."""
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave-001")
        result = calculator.calculate(
            completude=0.80,
            quality=0.70,
            residual_risk=0.75,
            reconciliation=1.0
        )
        
        assert result.status == "conditional"
        assert 0.70 <= result.score < 0.85
    
    def test_gate_score_blocked(self):
        """Test GateScore results in blocked."""
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave-001")
        result = calculator.calculate(
            completude=0.50,
            quality=0.60,
            residual_risk=0.40,
            reconciliation=1.0
        )
        
        assert result.status == "blocked"
        assert result.score < 0.70
    
    def test_gate_score_weights(self):
        """Test GateScore calculation uses correct weights."""
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave-001")
        
        # All components at 1.0
        result = calculator.calculate(1.0, 1.0, 1.0, 1.0)
        assert result.score == pytest.approx(1.0, abs=0.01)
        
        # All components at 0.0
        result = calculator.calculate(0.0, 0.0, 0.0, 0.0)
        assert result.score == pytest.approx(0.0, abs=0.01)
    
    def test_gate_score_gate3_reconciliation_critical(self):
        """Test Gate 3 reconciliation importance."""
        calculator = Gate3 = GateScoreCalculator(gate_number=3, wave_id="test-wave-001")
        
        # High scores but low reconciliation
        result = calculator.calculate(
            completude=1.0,
            quality=1.0,
            residual_risk=1.0,
            reconciliation=0.5  # Low reconciliation
        )
        
        # Should still contribute to lower overall score
        assert result.score < 1.0
        assert result.reconciliation == 0.5
    
    def test_gate_score_recommendations(self):
        """Test GateScore generates recommendations."""
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave-001")
        result = calculator.calculate(0.5, 0.5, 0.5, 1.0)
        
        assert len(result.recommendations) > 0
        assert any("blocked" in r.lower() for r in result.recommendations)


class TestIntegrationGateFlow:
    """Test complete gate validation flow."""
    
    def test_complete_gate1_flow(self, temp_project_dir):
        """Test complete Gate 1 validation and scoring."""
        upstream_dir = temp_project_dir / "outputs" / "upstream"
        upstream_dir.mkdir(parents=True, exist_ok=True)
        
        # Create all Gate 1 artifacts
        (upstream_dir / "discovery_inventory.md").write_text("# Inventory\n" + "x" * 100)
        (upstream_dir / "data_lineage_map.md").write_text("# Lineage\n" + "x" * 100)
        (upstream_dir / "STTM_BUSINESS_REQUIREMENTS.md").write_text("# STTM\nRequirements")
        (upstream_dir / "as_is_architecture.md").write_text("# Architecture\n" + "x" * 100)
        (upstream_dir / "risk_assessment.json").write_text(json.dumps({"risks": [{"severity": "low"}]}))
        
        # Validate
        validator = Gate1ArtifactsValidator(upstream_dir)
        artifact_result = validator.validate()
        
        # Calculate score
        calculator = GateScoreCalculator(gate_number=1, wave_id="test-wave")
        score_result = calculator.calculate(
            completude=artifact_result.completude,
            quality=artifact_result.quality,
            residual_risk=0.85
        )
        
        assert artifact_result.valid is True
        assert score_result.status == "approved"
