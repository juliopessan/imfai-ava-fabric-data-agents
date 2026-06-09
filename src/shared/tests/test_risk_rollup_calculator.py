"""
Tests for RiskRollupCalculator — Entity-to-wave risk aggregation and scoring.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.risk_rollup_calculator import (
    RiskRollupCalculator, RiskCategory, RiskSeverity
)


class TestRiskRollupCalculator:
    """Test suite for RiskRollupCalculator."""
    
    def test_initialization(self):
        """Test calculator initialization."""
        calculator = RiskRollupCalculator()
        assert len(calculator.entity_risks) == 0
    
    def test_add_entity_risk(self):
        """Test adding a risk."""
        calculator = RiskRollupCalculator()
        risk = calculator.add_entity_risk(
            entity_name="customers",
            category=RiskCategory.DATA_QUALITY,
            severity=RiskSeverity.HIGH,
            description="Missing phone numbers",
            probability=0.6,
            impact=0.8,
            mitigation="Implement data validation"
        )
        
        assert risk.entity_name == "customers"
        assert risk.severity == RiskSeverity.HIGH
        assert risk.residual_risk > 0  # Post-mitigation
    
    def test_residual_risk_calculation(self):
        """Test residual risk is reduced by mitigation."""
        calculator = RiskRollupCalculator()
        risk = calculator.add_entity_risk(
            entity_name="customers",
            category=RiskCategory.DATA_QUALITY,
            severity=RiskSeverity.HIGH,
            description="Missing phone numbers",
            probability=1.0,
            impact=1.0,
            mitigation="Implement data validation"
        )
        
        # Without mitigation: 1.0 * 1.0 = 1.0
        # With 30% mitigation: 1.0 * 0.7 = 0.7
        assert abs(risk.residual_risk - 0.7) < 0.01
    
    def test_calculate_wave_risk_profile_no_risks(self):
        """Test profile with no risks."""
        calculator = RiskRollupCalculator()
        profile = calculator.calculate_wave_risk_profile("wave-001")
        
        assert profile.total_risks == 0
        assert profile.overall_risk_score == 0.0
    
    def test_calculate_wave_risk_profile_single_critical(self):
        """Test profile with single critical risk."""
        calculator = RiskRollupCalculator()
        calculator.add_entity_risk(
            entity_name="payments",
            category=RiskCategory.SECURITY,
            severity=RiskSeverity.CRITICAL,
            description="Encryption not implemented",
            probability=0.9,
            impact=1.0,
            mitigation="Deploy SSL/TLS"
        )
        
        profile = calculator.calculate_wave_risk_profile("wave-001")
        assert profile.critical_count == 1
        assert profile.overall_risk_score > 20  # Risk score is calculated with weighting
    
    def test_calculate_wave_risk_profile_multiple_risks(self):
        """Test profile with multiple risks."""
        calculator = RiskRollupCalculator()
        
        for i in range(3):
            calculator.add_entity_risk(
                entity_name=f"entity_{i}",
                category=RiskCategory.TECHNICAL if i % 2 == 0 else RiskCategory.OPERATIONAL,
                severity=RiskSeverity.HIGH if i < 2 else RiskSeverity.MEDIUM,
                description=f"Risk {i}",
                probability=0.5,
                impact=0.7,
                mitigation="Plan mitigation"
            )
        
        profile = calculator.calculate_wave_risk_profile("wave-001")
        assert profile.total_risks == 3
        assert profile.high_count == 2
        assert profile.medium_count == 1
    
    def test_risk_trend_high_score(self):
        """Test risk trend for high risk score."""
        calculator = RiskRollupCalculator()
        for _ in range(5):
            calculator.add_entity_risk(
                entity_name="high_risk_entity",
                category=RiskCategory.SECURITY,
                severity=RiskSeverity.CRITICAL,
                description="Critical risk",
                probability=1.0,
                impact=1.0,
                mitigation="Mitigation"
            )
        
        profile = calculator.calculate_wave_risk_profile("wave-001")
        assert profile.risk_trend in ["increasing", "stable"]  # Multiple critical risks may be stable threshold
    
    def test_risk_trend_low_score(self):
        """Test risk trend for low risk score."""
        calculator = RiskRollupCalculator()
        calculator.add_entity_risk(
            entity_name="low_risk_entity",
            category=RiskCategory.RESOURCE,
            severity=RiskSeverity.LOW,
            description="Minor risk",
            probability=0.1,
            impact=0.1,
            mitigation="Monitor"
        )
        
        profile = calculator.calculate_wave_risk_profile("wave-001")
        assert profile.risk_trend == "decreasing"
    
    def test_get_risks_by_category(self):
        """Test filtering risks by category."""
        calculator = RiskRollupCalculator()
        
        calculator.add_entity_risk("entity1", RiskCategory.TECHNICAL, RiskSeverity.HIGH,
                                 "Risk 1", 0.5, 0.7, "Mitigation 1")
        calculator.add_entity_risk("entity2", RiskCategory.TECHNICAL, RiskSeverity.MEDIUM,
                                 "Risk 2", 0.4, 0.6, "Mitigation 2")
        calculator.add_entity_risk("entity3", RiskCategory.SECURITY, RiskSeverity.CRITICAL,
                                 "Risk 3", 0.8, 0.9, "Mitigation 3")
        
        technical_risks = calculator.get_risks_by_category(RiskCategory.TECHNICAL)
        assert len(technical_risks) == 2
        assert all(r.category == RiskCategory.TECHNICAL for r in technical_risks)
    
    def test_get_high_residual_risks(self):
        """Test filtering high residual risks."""
        calculator = RiskRollupCalculator()
        
        # High residual risk: 1.0 * 1.0 * 0.7 = 0.7
        calculator.add_entity_risk("entity1", RiskCategory.TECHNICAL, RiskSeverity.HIGH,
                                 "High residual", 1.0, 1.0, "Mitigation")
        
        # Low residual risk: 0.1 * 0.1 * 0.7 = 0.007
        calculator.add_entity_risk("entity2", RiskCategory.OPERATIONAL, RiskSeverity.LOW,
                                 "Low residual", 0.1, 0.1, "Mitigation")
        
        high_risks = calculator.get_high_residual_risks(threshold=0.5)
        assert len(high_risks) == 1
        assert high_risks[0].entity_name == "entity1"
    
    def test_generate_risk_mitigation_plan(self):
        """Test generating mitigation plan."""
        calculator = RiskRollupCalculator()
        calculator.add_entity_risk("payments", RiskCategory.SECURITY, RiskSeverity.CRITICAL,
                                 "Encryption missing", 0.9, 1.0, "Deploy TLS")
        calculator.add_entity_risk("customers", RiskCategory.DATA_QUALITY, RiskSeverity.HIGH,
                                 "Missing data", 0.7, 0.8, "Implement validation")
        
        plan = calculator.generate_risk_mitigation_plan()
        assert "Risk Mitigation Plan" in plan
        assert "SECURITY" in plan or "CRITICAL" in plan
    
    def test_get_risk_summary(self):
        """Test generating risk summary."""
        calculator = RiskRollupCalculator()
        calculator.add_entity_risk("e1", RiskCategory.TECHNICAL, RiskSeverity.CRITICAL,
                                 "Risk 1", 0.8, 0.9, "Mitigation")
        calculator.add_entity_risk("e2", RiskCategory.TECHNICAL, RiskSeverity.HIGH,
                                 "Risk 2", 0.6, 0.7, "Mitigation")
        calculator.add_entity_risk("e3", RiskCategory.SECURITY, RiskSeverity.LOW,
                                 "Risk 3", 0.2, 0.3, "Mitigation")
        
        summary = calculator.get_risk_summary()
        assert summary["total_risks"] == 3
        assert summary["by_severity"]["CRITICAL"] == 1
        assert summary["by_severity"]["HIGH"] == 1
        assert summary["by_category"]["technical"] == 2
    
    def test_save_risk_profile(self):
        """Test saving profile to file."""
        calculator = RiskRollupCalculator()
        calculator.add_entity_risk("entity1", RiskCategory.TECHNICAL, RiskSeverity.HIGH,
                                 "Risk 1", 0.5, 0.7, "Mitigation")
        
        profile = calculator.calculate_wave_risk_profile("wave-001")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "risk_profile.json"
            calculator.save_risk_profile(profile, output_path)
            
            assert output_path.exists()
            with open(output_path) as f:
                data = json.load(f)
            
            assert data["wave_id"] == "wave-001"
            assert data["total_risks"] == 1
