"""
Tests for EntityQualityReporter — Quality metrics tracking and reporting.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.entity_quality_reporter import (
    EntityQualityReporter, EntityQualityMetric
)


class TestEntityQualityReporter:
    """Test suite for EntityQualityReporter."""
    
    def test_initialization(self):
        """Test reporter initialization."""
        reporter = EntityQualityReporter()
        assert len(reporter.metrics) == 0
    
    def test_add_metric(self):
        """Test adding a quality metric."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        
        assert len(reporter.metrics) == 1
        assert reporter.metrics[0].entity_name == "customers"
    
    def test_get_metrics_for_entity(self):
        """Test retrieving metrics for entity."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        reporter.add_metric("orders", "gate_1", 0.90, 0.88, 2)
        
        customer_metrics = reporter.get_metrics_for_entity("customers")
        assert len(customer_metrics) == 1
        assert customer_metrics[0].entity_name == "customers"
    
    def test_get_metrics_for_nonexistent_entity(self):
        """Test retrieving metrics for non-existent entity."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        
        metrics = reporter.get_metrics_for_entity("nonexistent")
        assert len(metrics) == 0
    
    def test_calculate_trends_stable(self):
        """Test trend calculation for stable entity."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        reporter.add_metric("customers", "gate_2", 0.95, 0.91, 1)
        
        trends = reporter.calculate_trends()
        assert trends["customers"] == "stable"
    
    def test_calculate_trends_improving(self):
        """Test trend calculation for improving entity."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.80, 1)
        reporter.add_metric("customers", "gate_2", 0.95, 0.90, 1)
        
        trends = reporter.calculate_trends()
        assert trends["customers"] == "improving"
    
    def test_calculate_trends_declining(self):
        """Test trend calculation for declining entity."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.95, 1)
        reporter.add_metric("customers", "gate_2", 0.95, 0.85, 1)
        
        trends = reporter.calculate_trends()
        assert trends["customers"] == "declining"
    
    def test_generate_entity_report_valid(self):
        """Test generating entity report."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        reporter.add_metric("customers", "gate_2", 0.96, 0.94, 0)
        
        report = reporter.generate_entity_report("customers")
        assert report["entity_name"] == "customers"
        assert report["metric_count"] == 2
        assert "average_quality" in report
        assert "recommendations" in report
    
    def test_generate_entity_report_nonexistent(self):
        """Test generating report for non-existent entity."""
        reporter = EntityQualityReporter()
        
        report = reporter.generate_entity_report("nonexistent")
        assert "error" in report
    
    def test_recommendations_low_completude(self):
        """Test recommendations for low completude."""
        reporter = EntityQualityReporter()
        reporter.add_metric("data", "gate_1", 0.85, 0.92, 0)
        
        report = reporter.generate_entity_report("data")
        recs = report["recommendations"]
        assert any("completude" in r.lower() for r in recs)
    
    def test_recommendations_low_quality(self):
        """Test recommendations for low quality."""
        reporter = EntityQualityReporter()
        reporter.add_metric("data", "gate_1", 0.95, 0.75, 0)
        
        report = reporter.generate_entity_report("data")
        recs = report["recommendations"]
        assert any("quality" in r.lower() for r in recs)
    
    def test_recommendations_high_error_count(self):
        """Test recommendations for high errors."""
        reporter = EntityQualityReporter()
        reporter.add_metric("data", "gate_1", 0.95, 0.90, 10)
        
        report = reporter.generate_entity_report("data")
        recs = report["recommendations"]
        assert any("error" in r.lower() for r in recs)
    
    def test_generate_summary_report(self):
        """Test generating summary report."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        reporter.add_metric("orders", "gate_1", 0.90, 0.88, 2)
        
        report = reporter.generate_summary_report()
        assert "total_entities" in report
        assert report["total_entities"] == 2
        assert "average_quality" in report
        assert "entity_details" in report
    
    def test_save_report(self):
        """Test saving report to file."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        
        report = reporter.generate_summary_report()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.json"
            reporter.save_report(report, output_path)
            
            assert output_path.exists()
            with open(output_path) as f:
                saved = json.load(f)
            
            assert saved["total_entities"] == 1
    
    def test_to_list(self):
        """Test converting metrics to list."""
        reporter = EntityQualityReporter()
        reporter.add_metric("customers", "gate_1", 0.95, 0.92, 1)
        reporter.add_metric("orders", "gate_1", 0.90, 0.88, 2)
        
        metrics_list = reporter.to_list()
        assert len(metrics_list) == 2
        assert all(isinstance(m, dict) for m in metrics_list)
