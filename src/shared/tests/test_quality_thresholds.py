"""
Tests for QualityThresholdRegistry — entity-tier quality rules and SLA enforcement.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.quality_thresholds import (
    QualityThreshold, QualityThresholdRegistry, RiskLevel, create_default_registry
)


class TestRiskLevel:
    """Test suite for RiskLevel enum."""
    
    def test_risk_level_values(self):
        """Test all risk levels exist."""
        assert RiskLevel.CRITICAL.value == "critical"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.LOW.value == "low"


class TestQualityThresholdRegistry:
    """Test suite for QualityThresholdRegistry."""
    
    def test_initialization(self):
        """Test registry initialization."""
        registry = QualityThresholdRegistry()
        assert len(registry.thresholds) == 0
    
    def test_register_entity_default_thresholds(self):
        """Test registering entity with default thresholds."""
        registry = QualityThresholdRegistry()
        threshold = registry.register_entity("customers", RiskLevel.HIGH)
        
        assert threshold.entity_name == "customers"
        assert threshold.risk_level == RiskLevel.HIGH
        assert threshold.min_completude == 0.95
        assert threshold.min_quality == 0.95
        assert threshold.max_error_count == 1
        assert threshold.sla_availability == 99.9
    
    def test_register_entity_critical_risk(self):
        """Test critical risk thresholds."""
        registry = QualityThresholdRegistry()
        threshold = registry.register_entity("payments", RiskLevel.CRITICAL)
        
        assert threshold.min_completude == 1.0
        assert threshold.min_quality == 0.98
        assert threshold.max_error_count == 0
        assert threshold.sla_availability == 99.99
        assert threshold.sla_rto_hours == 1
    
    def test_register_entity_low_risk(self):
        """Test low risk thresholds."""
        registry = QualityThresholdRegistry()
        threshold = registry.register_entity("logs", RiskLevel.LOW)
        
        assert threshold.min_completude == 0.85
        assert threshold.min_quality == 0.80
        assert threshold.max_error_count == 5
        assert threshold.sla_availability == 99.0
    
    def test_register_entity_custom_thresholds(self):
        """Test registering with custom thresholds."""
        registry = QualityThresholdRegistry()
        custom = {
            "min_completude": 0.99,
            "max_error_count": 0,
            "sla_availability": 99.95
        }
        
        threshold = registry.register_entity("transactions", RiskLevel.HIGH, custom)
        
        assert threshold.min_completude == 0.99
        assert threshold.min_quality == 0.95  # Still defaults from HIGH
        assert threshold.max_error_count == 0
        assert threshold.sla_availability == 99.95
    
    def test_get_threshold_existing(self):
        """Test retrieving existing threshold."""
        registry = QualityThresholdRegistry()
        registry.register_entity("users", RiskLevel.MEDIUM)
        
        threshold = registry.get_threshold("users")
        assert threshold is not None
        assert threshold.entity_name == "users"
    
    def test_get_threshold_nonexistent(self):
        """Test retrieving non-existent threshold."""
        registry = QualityThresholdRegistry()
        threshold = registry.get_threshold("nonexistent")
        assert threshold is None
    
    def test_validate_entity_quality_pass_all(self):
        """Test validation passes when all metrics good."""
        registry = QualityThresholdRegistry()
        registry.register_entity("data", RiskLevel.MEDIUM)
        
        is_valid, violations = registry.validate_entity_quality("data", 0.95, 0.92, 1)
        assert is_valid is True
        assert len(violations) == 0
    
    def test_validate_entity_quality_low_completude(self):
        """Test validation fails on low completude."""
        registry = QualityThresholdRegistry()
        registry.register_entity("data", RiskLevel.MEDIUM)
        
        is_valid, violations = registry.validate_entity_quality("data", 0.80, 0.92, 0)
        assert is_valid is False
        assert any("Completude" in v for v in violations)
    
    def test_validate_entity_quality_low_quality(self):
        """Test validation fails on low quality."""
        registry = QualityThresholdRegistry()
        registry.register_entity("data", RiskLevel.MEDIUM)
        
        is_valid, violations = registry.validate_entity_quality("data", 0.92, 0.75, 0)
        assert is_valid is False
        assert any("Quality" in v for v in violations)
    
    def test_validate_entity_quality_too_many_errors(self):
        """Test validation fails on error count."""
        registry = QualityThresholdRegistry()
        registry.register_entity("data", RiskLevel.MEDIUM)
        
        is_valid, violations = registry.validate_entity_quality("data", 0.92, 0.92, 5)
        assert is_valid is False
        assert any("Error count" in v for v in violations)
    
    def test_validate_entity_quality_unregistered(self):
        """Test validation fails for unregistered entity."""
        registry = QualityThresholdRegistry()
        
        is_valid, violations = registry.validate_entity_quality("unknown", 0.95, 0.95, 0)
        assert is_valid is False
        assert any("not registered" in v for v in violations)
    
    def test_validate_entity_quality_critical_zero_errors(self):
        """Test critical entities tolerate zero errors only."""
        registry = QualityThresholdRegistry()
        registry.register_entity("critical_data", RiskLevel.CRITICAL)
        
        # Pass with 0 errors
        is_valid, _ = registry.validate_entity_quality("critical_data", 1.0, 0.98, 0)
        assert is_valid is True
        
        # Fail with 1 error
        is_valid, violations = registry.validate_entity_quality("critical_data", 1.0, 0.98, 1)
        assert is_valid is False
    
    def test_get_sla_report(self):
        """Test SLA report generation."""
        registry = QualityThresholdRegistry()
        registry.register_entity("customers", RiskLevel.HIGH)
        
        report = registry.get_sla_report("customers")
        assert report is not None
        assert report["entity_name"] == "customers"
        assert report["risk_level"] == "high"
        assert report["sla_availability_percentage"] == 99.9
        assert report["rto_hours"] == 4
        assert report["rpo_minutes"] == 15
    
    def test_get_sla_report_nonexistent(self):
        """Test SLA report for non-existent entity."""
        registry = QualityThresholdRegistry()
        report = registry.get_sla_report("nonexistent")
        assert report is None
    
    def test_save_and_load_from_file(self):
        """Test persistence to/from file."""
        registry1 = QualityThresholdRegistry()
        registry1.register_entity("customers", RiskLevel.HIGH)
        registry1.register_entity("products", RiskLevel.MEDIUM)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "thresholds.json"
            registry1.save_to_file(filepath)
            
            registry2 = QualityThresholdRegistry.load_from_file(filepath)
            
            assert len(registry2.thresholds) == 2
            assert registry2.get_threshold("customers").risk_level == RiskLevel.HIGH
            assert registry2.get_threshold("products").risk_level == RiskLevel.MEDIUM


class TestCreateDefaultRegistry:
    """Test suite for create_default_registry helper."""
    
    def test_create_with_risk_mapping(self):
        """Test creating registry with entity risk mapping."""
        entities = ["users", "orders", "products"]
        risk_mapping = {
            "users": "high",
            "orders": "critical",
            "products": "medium"
        }
        
        registry = create_default_registry(entities, risk_mapping)
        
        assert registry.get_threshold("users").risk_level == RiskLevel.HIGH
        assert registry.get_threshold("orders").risk_level == RiskLevel.CRITICAL
        assert registry.get_threshold("products").risk_level == RiskLevel.MEDIUM
    
    def test_create_defaults_to_medium(self):
        """Test entities default to medium risk if not in mapping."""
        entities = ["data1", "data2"]
        risk_mapping = {"data1": "high"}
        
        registry = create_default_registry(entities, risk_mapping)
        
        assert registry.get_threshold("data1").risk_level == RiskLevel.HIGH
        assert registry.get_threshold("data2").risk_level == RiskLevel.MEDIUM
