"""
Tests for WaveCostEstimator — Migration cost forecasting.
"""

import pytest
from src.shared.scripts.wave_cost_estimator import (
    WaveCostEstimator, ResourceTier, CostCategory
)


class TestWaveCostEstimator:
    """Test suite for WaveCostEstimator."""
    
    def test_initialization(self):
        """Test estimator initialization."""
        estimator = WaveCostEstimator()
        assert len(estimator.estimates) == 0
    
    def test_estimate_data_storage_cost(self):
        """Test data storage cost calculation."""
        estimator = WaveCostEstimator()
        cost = estimator.estimate_data_storage_cost(100.0, months=1)
        
        # 100 GB * $0.023/GB/month
        assert cost == pytest.approx(2.3, rel=1e-5)
    
    def test_estimate_compute_cost_small(self):
        """Test compute cost for small tier."""
        estimator = WaveCostEstimator()
        cost = estimator.estimate_compute_cost(100.0, ResourceTier.SMALL)
        
        # Should be proportional to data volume
        assert cost > 0
    
    def test_estimate_compute_cost_large_vs_small(self):
        """Test that larger tier costs more."""
        estimator = WaveCostEstimator()
        cost_small = estimator.estimate_compute_cost(100.0, ResourceTier.SMALL)
        cost_large = estimator.estimate_compute_cost(100.0, ResourceTier.LARGE)
        
        assert cost_large > cost_small
    
    def test_estimate_network_cost(self):
        """Test network cost calculation."""
        estimator = WaveCostEstimator()
        cost = estimator.estimate_network_cost(100.0)
        
        # 100 GB * $0.02/GB
        assert cost == pytest.approx(2.0, rel=1e-5)
    
    def test_estimate_labor_cost(self):
        """Test labor cost calculation."""
        estimator = WaveCostEstimator()
        cost = estimator.estimate_labor_cost(10, hours_per_entity=4.0)
        
        # 10 entities * 4 hours * $85/hour
        assert cost == pytest.approx(3400.0, rel=1e-5)
    
    def test_estimate_licensing_cost_small(self):
        """Test licensing cost for small data volume."""
        estimator = WaveCostEstimator()
        cost = estimator.estimate_licensing_cost(50.0, tool_licenses=1)
        
        # Base license only (under 100GB)
        assert cost == pytest.approx(5000.0, rel=1e-5)
    
    def test_estimate_licensing_cost_large(self):
        """Test licensing cost scales with volume."""
        estimator = WaveCostEstimator()
        cost_small = estimator.estimate_licensing_cost(100.0, tool_licenses=1)
        cost_large = estimator.estimate_licensing_cost(500.0, tool_licenses=1)
        
        assert cost_large > cost_small
    
    def test_create_estimate_basic(self):
        """Test creating basic estimate."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0,
            estimated_days=30
        )
        
        assert estimate.wave_id == "wave-001"
        assert estimate.project_name == "test-project"
        assert estimate.total_entities == 20
        assert estimate.data_volume_gb == 100.0
        assert estimate.total_cost > 0
        assert estimate.final_cost_with_contingency > estimate.total_cost
    
    def test_create_estimate_contains_all_categories(self):
        """Test estimate includes all cost categories."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0
        )
        
        categories = {item.category for item in estimate.cost_items}
        assert CostCategory.DATA_STORAGE in categories
        assert CostCategory.COMPUTE in categories
        assert CostCategory.NETWORK in categories
        assert CostCategory.LABOR in categories
        assert CostCategory.LICENSING in categories
        assert CostCategory.CONTINGENCY in categories
    
    def test_create_estimate_breakdown(self):
        """Test cost breakdown is calculated."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0
        )
        
        assert len(estimate.breakdown) > 0
        assert sum(estimate.breakdown.values()) == pytest.approx(estimate.final_cost_with_contingency, rel=1e-5)
    
    def test_cost_per_gb(self):
        """Test cost per GB calculation."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0
        )
        
        expected_per_gb = estimate.total_cost / 100.0
        assert estimate.cost_per_gb == pytest.approx(expected_per_gb, rel=1e-5)
    
    def test_contingency_percentage(self):
        """Test contingency calculation."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0,
            estimated_days=30
        )
        
        contingency_cost = estimate.final_cost_with_contingency - estimate.total_cost
        expected_contingency = estimate.total_cost * 0.15
        assert contingency_cost == pytest.approx(expected_contingency, rel=1e-5)
    
    def test_get_cost_summary(self):
        """Test summary generation."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-001",
            project_name="test-project",
            total_entities=20,
            data_volume_gb=100.0
        )
        
        summary = estimator.get_cost_summary("wave-001")
        assert "Migration Cost Estimate" in summary
        assert "wave-001" in summary
        assert "test-project" in summary
        assert "$" in summary
    
    def test_get_cost_summary_nonexistent(self):
        """Test summary for nonexistent estimate."""
        estimator = WaveCostEstimator()
        summary = estimator.get_cost_summary("nonexistent")
        
        assert "No estimate found" in summary
    
    def test_compare_estimates_single(self):
        """Test comparing single estimate."""
        estimator = WaveCostEstimator()
        estimator.create_estimate(
            wave_id="wave-001",
            project_name="test",
            total_entities=20,
            data_volume_gb=100.0
        )
        
        comparison = estimator.compare_estimates(["wave-001"])
        assert "wave-001" in comparison
        assert "total_cost" in comparison["wave-001"]
        assert "cost_per_gb" in comparison["wave-001"]
    
    def test_compare_estimates_multiple(self):
        """Test comparing multiple estimates."""
        estimator = WaveCostEstimator()
        estimator.create_estimate("wave-001", "test", 20, 100.0)
        estimator.create_estimate("wave-002", "test", 50, 200.0)
        
        comparison = estimator.compare_estimates(["wave-001", "wave-002"])
        
        assert len(comparison) == 2
        assert comparison["wave-002"]["final_cost"] > comparison["wave-001"]["final_cost"]
    
    def test_large_data_volume(self):
        """Test estimate for large data volume."""
        estimator = WaveCostEstimator()
        estimate = estimator.create_estimate(
            wave_id="wave-large",
            project_name="test",
            total_entities=1000,
            data_volume_gb=10000.0,
            resource_tier=ResourceTier.XLARGE
        )
        
        assert estimate.total_entities == 1000
        assert estimate.data_volume_gb == 10000.0
        assert estimate.final_cost_with_contingency > 100000  # Should be expensive
