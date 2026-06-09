"""
Tests for EntityRiskScoringEngine — Composite entity risk scoring.
"""

import pytest
from src.shared.scripts.entity_risk_scoring import (
    EntityRiskScoringEngine, RiskDimension, RiskLevel
)


class TestEntityRiskScoringEngine:
    """Test suite for EntityRiskScoringEngine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = EntityRiskScoringEngine()
        assert len(engine.entity_scores) == 0
    
    def test_add_dimension_score(self):
        """Test adding dimension score."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="orders",
            dimension=RiskDimension.TECHNICAL,
            probability=0.3,
            impact=0.8,
            mitigation_effectiveness=0.5
        )
        
        assert "orders" in engine.entity_scores
        assert len(engine.entity_scores["orders"].dimension_scores) == 1
    
    def test_dimension_score_residual_calculation(self):
        """Test residual score calculation."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="orders",
            dimension=RiskDimension.TECHNICAL,
            probability=0.5,
            impact=0.8,
            mitigation_effectiveness=0.3
        )
        
        score = engine.entity_scores["orders"]
        dim_score = score.dimension_scores[0]
        
        # residual = (0.5 * 0.8 * 100) * (1 - 0.3) = 40 * 0.7 = 28
        assert dim_score.residual_score == pytest.approx(28.0, rel=1e-5)
    
    def test_calculate_entity_risk_no_scores(self):
        """Test calculating risk with no scores."""
        engine = EntityRiskScoringEngine()
        score = engine.calculate_entity_risk("unknown")
        
        assert score.overall_score == 0.0
        assert score.risk_level == RiskLevel.MINIMAL
    
    def test_calculate_entity_risk_minimal(self):
        """Test minimal risk classification."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="safe_entity",
            dimension=RiskDimension.TECHNICAL,
            probability=0.05,
            impact=0.10,
            mitigation_effectiveness=0.9
        )
        
        score = engine.calculate_entity_risk("safe_entity")
        assert score.risk_level == RiskLevel.MINIMAL
    
    def test_calculate_entity_risk_critical(self):
        """Test critical risk classification."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="risky_entity",
            dimension=RiskDimension.SECURITY,
            probability=0.9,
            impact=0.95,
            mitigation_effectiveness=0.1
        )
        
        score = engine.calculate_entity_risk("risky_entity")
        assert score.risk_level == RiskLevel.CRITICAL
        assert score.overall_score > 75
    
    def test_calculate_entity_risk_multiple_dimensions(self):
        """Test risk calculation across multiple dimensions."""
        engine = EntityRiskScoringEngine()
        
        for i, dim in enumerate([RiskDimension.TECHNICAL, RiskDimension.OPERATIONAL]):
            engine.add_dimension_score(
                entity_name="multi_entity",
                dimension=dim,
                probability=0.3 + (i * 0.1),
                impact=0.7,
                mitigation_effectiveness=0.2
            )
        
        score = engine.calculate_entity_risk("multi_entity")
        assert len(score.dimension_scores) == 2
        assert score.overall_score > 0
        assert len(score.primary_risks) > 0
    
    def test_primary_risks_ranking(self):
        """Test primary risks are ranked by score."""
        engine = EntityRiskScoringEngine()
        
        # High risk dimension
        engine.add_dimension_score(
            entity_name="entity",
            dimension=RiskDimension.TECHNICAL,
            probability=0.9,
            impact=0.8,
            mitigation_effectiveness=0.0
        )
        
        # Lower risk dimension
        engine.add_dimension_score(
            entity_name="entity",
            dimension=RiskDimension.OPERATIONAL,
            probability=0.3,
            impact=0.2,
            mitigation_effectiveness=0.5
        )
        
        score = engine.calculate_entity_risk("entity")
        assert len(score.primary_risks) > 0
        assert "technical" in score.primary_risks[0].lower()
    
    def test_mitigation_recommendations(self):
        """Test mitigation recommendations are generated."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="entity",
            dimension=RiskDimension.SECURITY,
            probability=0.8,
            impact=0.9,
            mitigation_effectiveness=0.1
        )
        
        score = engine.calculate_entity_risk("entity")
        assert len(score.mitigation_recommendations) > 0
    
    def test_get_high_risk_entities(self):
        """Test filtering high-risk entities."""
        engine = EntityRiskScoringEngine()
        
        # Add low risk entity
        engine.add_dimension_score(
            entity_name="safe",
            dimension=RiskDimension.TECHNICAL,
            probability=0.1,
            impact=0.1,
            mitigation_effectiveness=0.9
        )
        
        # Add high risk entity
        engine.add_dimension_score(
            entity_name="risky",
            dimension=RiskDimension.SECURITY,
            probability=0.9,
            impact=0.9,
            mitigation_effectiveness=0.0
        )
        
        high_risk = engine.get_high_risk_entities(threshold=50.0)
        assert len(high_risk) == 1
        assert high_risk[0].entity_name == "risky"
    
    def test_get_risk_summary(self):
        """Test risk summary generation."""
        engine = EntityRiskScoringEngine()
        
        for i in range(5):
            engine.add_dimension_score(
                entity_name=f"entity_{i}",
                dimension=RiskDimension.TECHNICAL,
                probability=0.2 + (i * 0.1),
                impact=0.7,
                mitigation_effectiveness=0.3
            )
        
        summary = engine.get_risk_summary()
        
        assert sum(summary.values()) == 5
        assert all(k in summary for k in ["minimal", "low", "medium", "high", "critical"])
    
    def test_get_average_risk_score(self):
        """Test average risk score calculation."""
        engine = EntityRiskScoringEngine()
        
        for i in range(3):
            engine.add_dimension_score(
                entity_name=f"entity_{i}",
                dimension=RiskDimension.TECHNICAL,
                probability=0.3,
                impact=0.5,
                mitigation_effectiveness=0.2
            )
        
        avg_score = engine.get_average_risk_score()
        assert avg_score > 0
        assert avg_score < 100
    
    def test_risk_level_boundaries(self):
        """Test risk level classification boundaries."""
        engine = EntityRiskScoringEngine()
        
        test_cases = [
            (0.05, 0.05, 0.9, RiskLevel.MINIMAL),  # 0.05 * 0.05 * 0.1 = 0.000025 * 100 = 0.0025, < 10
            (0.4, 0.3, 0.0, RiskLevel.LOW),  # 0.4 * 0.3 * 1.0 * 100 = 12, in 10-24
            (0.5, 0.5, 0.0, RiskLevel.MEDIUM),  # 0.5 * 0.5 * 1.0 * 100 = 25, in 25-49
            (0.75, 0.75, 0.0, RiskLevel.HIGH),  # 0.75 * 0.75 * 1.0 * 100 = 56.25, in 50-74
            (0.9, 0.9, 0.0, RiskLevel.CRITICAL),  # 0.9 * 0.9 * 1.0 * 100 = 81, >= 75
        ]
        
        for i, (prob, impact, mit, expected_level) in enumerate(test_cases):
            entity = f"test_{i}"
            engine.add_dimension_score(
                entity_name=entity,
                dimension=RiskDimension.TECHNICAL,
                probability=prob,
                impact=impact,
                mitigation_effectiveness=mit
            )
            
            score = engine.calculate_entity_risk(entity)
            assert score.risk_level == expected_level, f"test_{i}: expected {expected_level}, got {score.risk_level}, overall_score={score.overall_score}"
    
    def test_generate_risk_report(self):
        """Test report generation."""
        engine = EntityRiskScoringEngine()
        
        engine.add_dimension_score(
            entity_name="entity_1",
            dimension=RiskDimension.TECHNICAL,
            probability=0.5,
            impact=0.8,
            mitigation_effectiveness=0.3
        )
        
        report = engine.generate_risk_report()
        assert "Entity Risk Scoring Report" in report
        assert "Total Entities: 1" in report
        assert "Risk Distribution" in report
