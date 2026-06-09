"""
Tests for GovernancePolicy — artifact governance rules enforcement.
"""

import pytest
from src.shared.scripts.governance_policy import (
    GovernancePolicy, PolicySeverity, PolicyViolation,
    ArtifactNamingPolicy, ArtifactOwnershipPolicy, DataQualityPolicy,
    ReconciliationPolicy, PolicyEngine, create_default_policy_engine
)


class TestArtifactNamingPolicy:
    """Test suite for ArtifactNamingPolicy."""
    
    def test_valid_naming_snake_case(self):
        """Test valid snake_case filename."""
        policy = ArtifactNamingPolicy()
        artifact = {"filename": "discovery_inventory.md"}
        
        result = policy.validate(artifact)
        assert result is True
        assert len(policy.violations) == 0
    
    def test_invalid_naming_space(self):
        """Test invalid filename with spaces."""
        policy = ArtifactNamingPolicy()
        artifact = {"filename": "discovery inventory.md"}
        
        result = policy.validate(artifact)
        assert result is False
        assert len(policy.violations) == 1
    
    def test_invalid_naming_wrong_extension(self):
        """Test invalid file extension."""
        policy = ArtifactNamingPolicy()
        artifact = {"filename": "discovery_inventory.txt"}
        
        result = policy.validate(artifact)
        assert result is False
    
    def test_valid_json_filename(self):
        """Test valid JSON filename."""
        policy = ArtifactNamingPolicy()
        artifact = {"filename": "risk_assessment.json"}
        
        result = policy.validate(artifact)
        assert result is True
    
    def test_no_filename_provided(self):
        """Test when filename not provided."""
        policy = ArtifactNamingPolicy()
        artifact = {}
        
        result = policy.validate(artifact)
        assert result is False
        assert any("not provided" in v.message for v in policy.violations)


class TestArtifactOwnershipPolicy:
    """Test suite for ArtifactOwnershipPolicy."""
    
    def test_valid_owner(self):
        """Test valid ownership."""
        policy = ArtifactOwnershipPolicy()
        artifact = {"owner": "john.doe@company.com", "name": "users_table"}
        
        result = policy.validate(artifact)
        assert result is True
        assert len(policy.violations) == 0
    
    def test_missing_owner(self):
        """Test missing owner."""
        policy = ArtifactOwnershipPolicy()
        artifact = {"name": "users_table"}
        
        result = policy.validate(artifact)
        assert result is False
        assert any("No owner assigned" in v.message for v in policy.violations)
    
    def test_empty_owner(self):
        """Test empty owner string."""
        policy = ArtifactOwnershipPolicy()
        artifact = {"owner": "", "name": "users_table"}
        
        result = policy.validate(artifact)
        assert result is False
    
    def test_none_owner(self):
        """Test None owner."""
        policy = ArtifactOwnershipPolicy()
        artifact = {"owner": None, "name": "users_table"}
        
        result = policy.validate(artifact)
        assert result is False


class TestDataQualityPolicy:
    """Test suite for DataQualityPolicy."""
    
    def test_quality_above_threshold(self):
        """Test quality above minimum."""
        policy = DataQualityPolicy(min_quality_score=0.80)
        artifact = {"quality_score": 0.95, "name": "data"}
        
        result = policy.validate(artifact)
        assert result is True
    
    def test_quality_below_threshold(self):
        """Test quality below minimum."""
        policy = DataQualityPolicy(min_quality_score=0.80)
        artifact = {"quality_score": 0.70, "name": "data"}
        
        result = policy.validate(artifact)
        assert result is False
        assert any("below threshold" in v.message for v in policy.violations)
    
    def test_quality_defaults_to_perfect(self):
        """Test missing quality defaults to 1.0."""
        policy = DataQualityPolicy(min_quality_score=0.80)
        artifact = {"name": "data"}
        
        result = policy.validate(artifact)
        assert result is True


class TestReconciliationPolicy:
    """Test suite for ReconciliationPolicy."""
    
    def test_all_reconciliation_checks_passed(self):
        """Test all reconciliation checks passing."""
        policy = ReconciliationPolicy()
        artifact = {
            "name": "gate3_results",
            "reconciliation": {
                "row_count_validation": "PASSED",
                "schema_validation": "PASSED",
                "data_quality_validation": "PASSED"
            }
        }
        
        result = policy.validate(artifact)
        assert result is True
        assert len(policy.violations) == 0
    
    def test_row_count_validation_failed(self):
        """Test row count validation failure."""
        policy = ReconciliationPolicy()
        artifact = {
            "name": "gate3_results",
            "reconciliation": {
                "row_count_validation": "FAILED",
                "schema_validation": "PASSED",
                "data_quality_validation": "PASSED"
            }
        }
        
        result = policy.validate(artifact)
        assert result is False
        assert any("row_count_validation" in v.message for v in policy.violations)
    
    def test_missing_reconciliation_checks(self):
        """Test missing reconciliation checks."""
        policy = ReconciliationPolicy()
        artifact = {
            "name": "gate3_results",
            "reconciliation": {}
        }
        
        result = policy.validate(artifact)
        assert result is False
        assert len(policy.violations) >= 1  # At least one missing check fails validation


class TestPolicyEngine:
    """Test suite for PolicyEngine."""
    
    def test_register_policy(self):
        """Test registering a policy."""
        engine = PolicyEngine()
        policy = ArtifactNamingPolicy()
        
        engine.register_policy(policy)
        assert "ArtifactNaming" in engine.policies
    
    def test_enforce_single_policy_pass(self):
        """Test enforcement with single passing policy."""
        engine = PolicyEngine()
        engine.register_policy(ArtifactNamingPolicy())
        
        artifact = {"filename": "discovery_inventory.md"}
        all_pass, violations = engine.enforce(artifact)
        
        assert all_pass is True
        assert len(violations) == 0
    
    def test_enforce_single_policy_fail(self):
        """Test enforcement with single failing policy."""
        engine = PolicyEngine()
        engine.register_policy(ArtifactNamingPolicy())
        
        artifact = {"filename": "discovery inventory.md"}
        all_pass, violations = engine.enforce(artifact)
        
        assert all_pass is False
        assert len(violations) == 1
    
    def test_enforce_multiple_policies(self):
        """Test enforcement with multiple policies."""
        engine = PolicyEngine()
        engine.register_policy(ArtifactNamingPolicy())
        engine.register_policy(ArtifactOwnershipPolicy())
        
        artifact = {"filename": "discovery_inventory.md"}  # Valid name, no owner
        all_pass, violations = engine.enforce(artifact)
        
        assert all_pass is False
        assert len(violations) == 1  # Only ownership fails
    
    def test_get_violations_by_severity(self):
        """Test grouping violations by severity."""
        engine = PolicyEngine()
        engine.register_policy(DataQualityPolicy(min_quality_score=0.80))  # WARNING
        engine.register_policy(ArtifactOwnershipPolicy())  # ERROR
        
        artifact = {"quality_score": 0.70}  # Fails quality
        all_pass, violations = engine.enforce(artifact)
        
        by_severity = engine.get_violations_by_severity(violations)
        assert len(by_severity[PolicySeverity.WARNING]) > 0
    
    def test_get_summary(self):
        """Test violation summary generation."""
        engine = PolicyEngine()
        engine.register_policy(ArtifactNamingPolicy())
        engine.register_policy(ArtifactOwnershipPolicy())
        
        artifact = {"filename": "discovery inventory.md"}
        all_pass, violations = engine.enforce(artifact)
        
        summary = engine.get_summary(violations)
        assert len(summary) > 0
        assert "error" in summary.lower() or "warning" in summary.lower()


class TestCreateDefaultPolicyEngine:
    """Test suite for create_default_policy_engine helper."""
    
    def test_default_engine_has_policies(self):
        """Test default engine has policies."""
        engine = create_default_policy_engine()
        
        assert len(engine.policies) >= 4
        assert "ArtifactNaming" in engine.policies
        assert "ArtifactOwnership" in engine.policies
        assert "DataQuality" in engine.policies
        assert "Reconciliation" in engine.policies
    
    def test_default_engine_enforce_good_artifact(self):
        """Test default engine on good artifact."""
        engine = create_default_policy_engine()
        
        artifact = {
            "filename": "discovery_inventory.md",
            "owner": "team@company.com",
            "quality_score": 0.95,
            "name": "test",
            "reconciliation": {
                "row_count_validation": "PASSED",
                "schema_validation": "PASSED",
                "data_quality_validation": "PASSED"
            }
        }
        
        all_pass, violations = engine.enforce(artifact)
        assert all_pass is True
