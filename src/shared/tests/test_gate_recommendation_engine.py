"""
Tests for GateRecommendationEngine — Gate-level recommendation generation.
"""

import pytest
from src.shared.scripts.gate_recommendation_engine import (
    GateRecommendationEngine, RecommendationPriority
)


class TestGateRecommendationEngine:
    """Test suite for GateRecommendationEngine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = GateRecommendationEngine()
        assert len(engine.gate_metrics) == 0
    
    def test_analyze_gate_all_good(self):
        """Test analysis with good metrics."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.98,
            quality=0.95,
            error_count=1,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            required_artifacts=5
        )
        
        assert len(recs) == 0  # No recommendations needed
    
    def test_analyze_gate_low_completude(self):
        """Test detection of low completude."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.95,
            error_count=0,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=3,
            required_artifacts=5
        )
        
        assert len(recs) > 0
        assert any("completude" in r.title.lower() for r in recs)
        assert any(r.priority == RecommendationPriority.CRITICAL for r in recs)
    
    def test_analyze_gate_low_quality(self):
        """Test detection of low quality."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.98,
            quality=0.75,
            error_count=0,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            required_artifacts=5
        )
        
        assert len(recs) > 0
        assert any("quality" in r.title.lower() for r in recs)
    
    def test_analyze_gate_high_error_rate(self):
        """Test detection of high error rate."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.98,
            quality=0.90,
            error_count=5,  # 25% error rate
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            required_artifacts=5
        )
        
        assert len(recs) > 0
        assert any("error" in r.title.lower() for r in recs)
    
    def test_analyze_gate_gate3_reconciliation_low(self):
        """Test Gate 3 reconciliation requirement."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=3,
            completude=0.98,
            quality=0.95,
            error_count=0,
            total_entities=20,
            reconciliation=0.90,  # Below 0.95 for Gate 3
            artifact_count=5,
            required_artifacts=5
        )
        
        assert len(recs) > 0
        assert any("reconciliation" in r.title.lower() for r in recs)
        assert any(r.priority == RecommendationPriority.CRITICAL for r in recs)
    
    def test_get_blockers_only(self):
        """Test filtering blocking recommendations."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.75,
            error_count=3,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=3,
            required_artifacts=5
        )
        
        blockers = engine.get_blockers_only(recs)
        assert len(blockers) > 0
        assert all(b.priority == RecommendationPriority.CRITICAL or 
                  b.impact == "blocks_gate" for b in blockers)
    
    def test_get_recommendations_by_category(self):
        """Test filtering by category."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.75,
            error_count=3,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=3,
            required_artifacts=5
        )
        
        quality_recs = engine.get_recommendations_by_category(recs, "quality")
        assert all(r.category == "quality" for r in quality_recs)
    
    def test_generate_action_plan_no_recs(self):
        """Test action plan with no recommendations."""
        engine = GateRecommendationEngine()
        plan = engine.generate_action_plan([])
        
        assert "ready for progression" in plan.lower() or "no recommendations" in plan.lower()
    
    def test_generate_action_plan_with_recs(self):
        """Test action plan generation."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.75,
            error_count=0,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=3,
            required_artifacts=5
        )
        
        plan = engine.generate_action_plan(recs)
        assert "Action Plan" in plan
        assert "CRITICAL" in plan or "HIGH" in plan
    
    def test_get_effort_summary(self):
        """Test effort summary."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.75,
            error_count=5,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=2,
            required_artifacts=5
        )
        
        summary = engine.get_effort_summary(recs)
        assert "low" in summary
        assert "medium" in summary
        assert "high" in summary
    
    def test_estimate_time_to_fix(self):
        """Test time estimation."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.70,
            quality=0.75,
            error_count=5,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=2,
            required_artifacts=5
        )
        
        estimate = engine.estimate_time_to_fix(recs)
        assert estimate != "No effort required"
        assert len(estimate) > 0
    
    def test_should_gate_proceed_no_blockers(self):
        """Test gate can proceed with no blockers."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.98,
            quality=0.95,
            error_count=0,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            required_artifacts=5
        )
        
        assert engine.should_gate_proceed(recs) is True
    
    def test_should_gate_proceed_with_blockers(self):
        """Test gate cannot proceed with blockers."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=3,
            completude=0.98,
            quality=0.95,
            error_count=0,
            total_entities=20,
            reconciliation=0.80,  # Below threshold
            artifact_count=5,
            required_artifacts=5
        )
        
        assert engine.should_gate_proceed(recs) is False
    
    def test_generate_gate_readiness_report(self):
        """Test readiness report generation."""
        engine = GateRecommendationEngine()
        recs = engine.analyze_gate(
            gate_number=1,
            completude=0.90,
            quality=0.92,
            error_count=1,
            total_entities=20,
            reconciliation=1.0,
            artifact_count=5,
            required_artifacts=5
        )
        
        report = engine.generate_gate_readiness_report(recs)
        assert "can_proceed" in report
        assert "total_recommendations" in report
        assert "blocking_recommendations" in report
        assert "effort_summary" in report
