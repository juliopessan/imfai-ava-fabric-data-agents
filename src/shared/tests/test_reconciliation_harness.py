"""
Tests for ReconciliationHarness — Gate 3 reconciliation validation.
"""

import pytest
from src.shared.scripts.reconciliation_harness import (
    ReconciliationHarness, ReconciliationType, ReconciliationStatus
)


class TestReconciliationHarness:
    """Test suite for ReconciliationHarness."""
    
    def test_initialization(self):
        """Test harness initialization."""
        harness = ReconciliationHarness()
        assert len(harness.entity_results) == 0
        assert harness.wave_report is None
    
    def test_row_count_check_passed(self):
        """Test row count check that passes."""
        harness = ReconciliationHarness()
        check = harness.run_row_count_check("orders", 1000, 999, threshold=0.99)
        
        assert check.status == ReconciliationStatus.PASSED
        assert check.entity_name == "orders"
        assert check.source_count == 1000
        assert check.target_count == 999
        assert "match" in check.message.lower()
    
    def test_row_count_check_warning(self):
        """Test row count check that warns."""
        harness = ReconciliationHarness()
        check = harness.run_row_count_check("orders", 1000, 960, threshold=0.99)
        
        assert check.status == ReconciliationStatus.WARNING
        assert "variance acceptable" in check.message.lower()
    
    def test_row_count_check_failed(self):
        """Test row count check that fails."""
        harness = ReconciliationHarness()
        check = harness.run_row_count_check("orders", 1000, 900, threshold=0.99)
        
        assert check.status == ReconciliationStatus.FAILED
        assert "mismatch" in check.message.lower()
    
    def test_schema_check_passed(self):
        """Test schema check that passes."""
        harness = ReconciliationHarness()
        check = harness.run_schema_check("orders", source_columns=10, target_columns=10, matching_columns=10)
        
        assert check.status == ReconciliationStatus.PASSED
        assert check.check_type == ReconciliationType.SCHEMA
    
    def test_schema_check_warning(self):
        """Test schema check that warns."""
        harness = ReconciliationHarness()
        # 19/20 = 95% match, which is >= 0.95 and < 0.98
        check = harness.run_schema_check("orders", source_columns=20, target_columns=20, matching_columns=19)
        
        assert check.status == ReconciliationStatus.WARNING
    
    def test_schema_check_failed(self):
        """Test schema check that fails."""
        harness = ReconciliationHarness()
        check = harness.run_schema_check("orders", source_columns=10, target_columns=10, matching_columns=9)
        
        assert check.status == ReconciliationStatus.FAILED
    
    def test_data_quality_check_passed(self):
        """Test data quality check that passes."""
        harness = ReconciliationHarness()
        check = harness.run_data_quality_check(
            "orders", null_count=5, duplicate_count=5, total_records=1000, threshold=0.95
        )
        
        assert check.status == ReconciliationStatus.PASSED
        assert check.check_type == ReconciliationType.DATA_QUALITY
    
    def test_data_quality_check_warning(self):
        """Test data quality check that warns."""
        harness = ReconciliationHarness()
        check = harness.run_data_quality_check(
            "orders", null_count=50, duplicate_count=30, total_records=1000, threshold=0.95
        )
        
        assert check.status == ReconciliationStatus.WARNING
    
    def test_data_quality_check_failed(self):
        """Test data quality check that fails."""
        harness = ReconciliationHarness()
        check = harness.run_data_quality_check(
            "orders", null_count=100, duplicate_count=100, total_records=1000, threshold=0.95
        )
        
        assert check.status == ReconciliationStatus.FAILED
    
    def test_add_entity_check_single(self):
        """Test adding single check to entity."""
        harness = ReconciliationHarness()
        check = harness.run_row_count_check("orders", 1000, 999, threshold=0.99)
        harness.add_entity_check("orders", check)
        
        assert "orders" in harness.entity_results
        assert len(harness.entity_results["orders"].checks) == 1
        assert harness.entity_results["orders"].overall_status == ReconciliationStatus.PASSED
    
    def test_add_entity_check_multiple(self):
        """Test adding multiple checks to entity."""
        harness = ReconciliationHarness()
        check1 = harness.run_row_count_check("orders", 1000, 999, threshold=0.99)
        check2 = harness.run_schema_check("orders", 10, 10, 10)
        check3 = harness.run_data_quality_check("orders", 5, 5, 1000)
        
        harness.add_entity_check("orders", check1)
        harness.add_entity_check("orders", check2)
        harness.add_entity_check("orders", check3)
        
        assert len(harness.entity_results["orders"].checks) == 3
        assert harness.entity_results["orders"].passed_count == 3
    
    def test_add_entity_check_mixed_status(self):
        """Test entity with mixed check results."""
        harness = ReconciliationHarness()
        check1 = harness.run_row_count_check("orders", 1000, 999, threshold=0.99)  # PASSED
        check2 = harness.run_schema_check("orders", 10, 10, 9)  # FAILED
        
        harness.add_entity_check("orders", check1)
        harness.add_entity_check("orders", check2)
        
        assert harness.entity_results["orders"].overall_status == ReconciliationStatus.FAILED
    
    def test_calculate_wave_reconciliation_all_passed(self):
        """Test wave reconciliation with all entities passed."""
        harness = ReconciliationHarness()
        
        check1 = harness.run_row_count_check("orders", 1000, 999)
        harness.add_entity_check("orders", check1)
        
        check2 = harness.run_row_count_check("customers", 500, 499)
        harness.add_entity_check("customers", check2)
        
        report = harness.calculate_wave_reconciliation("wave-001", "test-project")
        
        assert report.total_entities == 2
        assert report.passed_entities == 2
        assert report.failed_entities == 0
        assert report.reconciliation_score == pytest.approx(1.0, rel=1e-5)
        assert report.can_proceed_to_production is True
    
    def test_calculate_wave_reconciliation_some_failed(self):
        """Test wave reconciliation with failed entities."""
        harness = ReconciliationHarness()
        
        check1 = harness.run_row_count_check("orders", 1000, 999)  # PASSED
        harness.add_entity_check("orders", check1)
        
        check2 = harness.run_row_count_check("customers", 500, 300)  # FAILED
        harness.add_entity_check("customers", check2)
        
        report = harness.calculate_wave_reconciliation("wave-001", "test-project")
        
        assert report.passed_entities == 1
        assert report.failed_entities == 1
        assert report.can_proceed_to_production is False
    
    def test_calculate_wave_reconciliation_low_score(self):
        """Test wave reconciliation with score below 0.95."""
        harness = ReconciliationHarness()
        
        # Add multiple checks with mixed results
        for i in range(20):
            if i < 18:
                check = harness.run_row_count_check(f"entity_{i}", 1000, 999)  # PASSED
            else:
                check = harness.run_row_count_check(f"entity_{i}", 1000, 500)  # FAILED
            harness.add_entity_check(f"entity_{i}", check)
        
        report = harness.calculate_wave_reconciliation("wave-001", "test-project")
        
        # 18 passed out of 20 = 0.90 score
        assert report.reconciliation_score < 0.95
        assert report.can_proceed_to_production is False
    
    def test_get_failed_entities(self):
        """Test filtering failed entities."""
        harness = ReconciliationHarness()
        
        check1 = harness.run_row_count_check("orders", 1000, 999)  # PASSED
        check2 = harness.run_row_count_check("customers", 500, 300)  # FAILED
        
        harness.add_entity_check("orders", check1)
        harness.add_entity_check("customers", check2)
        
        failed = harness.get_failed_entities()
        assert len(failed) == 1
        assert failed[0].entity_name == "customers"
    
    def test_generate_remediation_plan(self):
        """Test remediation plan generation."""
        harness = ReconciliationHarness()
        
        check1 = harness.run_row_count_check("orders", 1000, 500)  # FAILED
        check2 = harness.run_schema_check("customers", 10, 10, 8)  # FAILED
        
        harness.add_entity_check("orders", check1)
        harness.add_entity_check("customers", check2)
        
        plan = harness.generate_remediation_plan()
        
        assert "orders" in plan
        assert "customers" in plan
        assert len(plan["orders"]) == 1
        assert len(plan["customers"]) == 1
    
    def test_get_reconciliation_summary(self):
        """Test summary generation."""
        harness = ReconciliationHarness()
        
        check = harness.run_row_count_check("orders", 1000, 999)
        harness.add_entity_check("orders", check)
        
        harness.calculate_wave_reconciliation("wave-001", "test-project")
        summary = harness.get_reconciliation_summary()
        
        assert "Wave Reconciliation Summary" in summary
        assert "wave-001" in summary
        assert "test-project" in summary
        assert "Can Proceed to Production" in summary
