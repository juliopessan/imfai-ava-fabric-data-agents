"""
Gate Recommendation Engine — Generates advanced recommendations based on validation metrics.
Analyzes gate metrics and provides prioritized, actionable recommendations for progression.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class RecommendationPriority(Enum):
    """Priority levels for recommendations."""
    CRITICAL = 1  # Blocks progression
    HIGH = 2      # Should fix before progression
    MEDIUM = 3    # Nice to fix
    LOW = 4       # Optional


@dataclass
class Recommendation:
    """A single recommendation."""
    priority: RecommendationPriority
    category: str  # "completude", "quality", "risk", "performance", "compliance"
    title: str
    description: str
    impact: str  # "blocks_gate", "improves_score", "reduces_risk"
    effort: str  # "low", "medium", "high"
    suggested_action: str


class GateRecommendationEngine:
    """Generates gate-level recommendations."""
    
    def __init__(self):
        """Initialize engine."""
        self.gate_metrics = {}
    
    def analyze_gate(
        self,
        gate_number: int,
        completude: float,
        quality: float,
        error_count: int,
        total_entities: int,
        reconciliation: float,
        artifact_count: int,
        required_artifacts: int
    ) -> List[Recommendation]:
        """
        Analyze gate metrics and generate recommendations.
        Returns prioritized list of recommendations.
        """
        recommendations = []
        
        # Completude analysis
        if completude < 0.85:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.CRITICAL,
                category="completude",
                title="Low artifact completude",
                description=f"Only {completude:.1%} of required artifacts present",
                impact="blocks_gate",
                effort="high",
                suggested_action=f"Generate missing artifacts. Target: 100%, Current: {completude:.1%}"
            ))
        elif completude < 0.95:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.HIGH,
                category="completude",
                title="Completude below target",
                description=f"Completude is {completude:.1%}, target 95%+",
                impact="improves_score",
                effort="medium",
                suggested_action="Review and complete remaining artifacts"
            ))
        
        # Quality analysis
        if quality < 0.80:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.CRITICAL,
                category="quality",
                title="Poor data quality",
                description=f"Quality score {quality:.2f} below minimum 0.80",
                impact="blocks_gate",
                effort="high",
                suggested_action="Run data validation, fix quality issues"
            ))
        elif quality < 0.90:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.HIGH,
                category="quality",
                title="Quality score could improve",
                description=f"Current quality {quality:.2f}, target 0.90+",
                impact="improves_score",
                effort="medium",
                suggested_action="Review validation rules, test edge cases"
            ))
        
        # Error rate analysis
        error_rate = error_count / total_entities if total_entities > 0 else 0
        if error_rate > 0.1:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.CRITICAL,
                category="quality",
                title="High error rate",
                description=f"Error rate {error_rate:.1%} ({error_count}/{total_entities} entities)",
                impact="blocks_gate",
                effort="high",
                suggested_action="Debug failing validations, fix root causes"
            ))
        elif error_rate > 0.05:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.HIGH,
                category="quality",
                title="Moderate error rate",
                description=f"Error rate {error_rate:.1%}, should be <5%",
                impact="reduces_risk",
                effort="medium",
                suggested_action="Investigate and resolve error sources"
            ))
        
        # Reconciliation analysis (critical for Gate 3)
        if gate_number == 3 and reconciliation < 0.95:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.CRITICAL,
                category="compliance",
                title="Reconciliation below Gate 3 requirement",
                description=f"Reconciliation {reconciliation:.2f}, minimum 0.95 required for Gate 3",
                impact="blocks_gate",
                effort="high",
                suggested_action="Verify row counts, schema, and data quality validation"
            ))
        
        # Artifact count analysis
        if artifact_count < required_artifacts:
            recommendations.append(Recommendation(
                priority=RecommendationPriority.HIGH if gate_number < 3 else RecommendationPriority.CRITICAL,
                category="completude",
                title="Missing required artifacts",
                description=f"Only {artifact_count}/{required_artifacts} required artifacts present",
                impact="blocks_gate" if gate_number == 3 else "improves_score",
                effort="high",
                suggested_action=f"Generate {required_artifacts - artifact_count} missing artifacts"
            ))
        
        # Sort by priority
        recommendations.sort(key=lambda r: r.priority.value)
        
        return recommendations
    
    def get_blockers_only(self, recommendations: List[Recommendation]) -> List[Recommendation]:
        """Filter to only blocking recommendations."""
        return [
            r for r in recommendations
            if r.priority == RecommendationPriority.CRITICAL or r.impact == "blocks_gate"
        ]
    
    def get_recommendations_by_category(
        self,
        recommendations: List[Recommendation],
        category: str
    ) -> List[Recommendation]:
        """Filter recommendations by category."""
        return [r for r in recommendations if r.category == category]
    
    def generate_action_plan(self, recommendations: List[Recommendation]) -> str:
        """Generate actionable plan from recommendations."""
        if not recommendations:
            return "✓ No recommendations. Gate ready for progression."
        
        lines = ["# Action Plan for Gate Progression\n"]
        
        # Group by priority
        by_priority = {}
        for rec in recommendations:
            if rec.priority not in by_priority:
                by_priority[rec.priority] = []
            by_priority[rec.priority].append(rec)
        
        # Sort priorities
        for priority in sorted(by_priority.keys(), key=lambda p: p.value):
            recs = by_priority[priority]
            lines.append(f"## {priority.name} ({len(recs)} items)\n")
            
            for idx, rec in enumerate(recs, 1):
                lines.append(f"{idx}. **{rec.title}**")
                lines.append(f"   - Category: {rec.category}")
                lines.append(f"   - Effort: {rec.effort}")
                lines.append(f"   - Action: {rec.suggested_action}\n")
        
        return "\n".join(lines)
    
    def get_effort_summary(self, recommendations: List[Recommendation]) -> Dict[str, int]:
        """Summarize effort required."""
        return {
            "low": len([r for r in recommendations if r.effort == "low"]),
            "medium": len([r for r in recommendations if r.effort == "medium"]),
            "high": len([r for r in recommendations if r.effort == "high"])
        }
    
    def estimate_time_to_fix(self, recommendations: List[Recommendation]) -> str:
        """Estimate time needed to address all recommendations."""
        effort_summary = self.get_effort_summary(recommendations)
        
        # Estimate: low=1h, medium=4h, high=8h
        hours = (effort_summary["low"] * 1 +
                effort_summary["medium"] * 4 +
                effort_summary["high"] * 8)
        
        if hours == 0:
            return "No effort required"
        elif hours <= 1:
            return "< 1 hour"
        elif hours <= 4:
            return "1-4 hours"
        elif hours <= 8:
            return "4-8 hours"
        elif hours <= 16:
            return "1-2 days"
        else:
            return f"{hours // 8} days"
    
    def should_gate_proceed(self, recommendations: List[Recommendation]) -> bool:
        """Determine if gate should proceed despite recommendations."""
        blockers = self.get_blockers_only(recommendations)
        return len(blockers) == 0
    
    def generate_gate_readiness_report(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
        """Generate comprehensive gate readiness report."""
        blockers = self.get_blockers_only(recommendations)
        can_proceed = self.should_gate_proceed(recommendations)
        
        return {
            "can_proceed": can_proceed,
            "total_recommendations": len(recommendations),
            "blocking_recommendations": len(blockers),
            "effort_summary": self.get_effort_summary(recommendations),
            "estimated_time": self.estimate_time_to_fix(recommendations),
            "recommendations": [
                {
                    "priority": r.priority.name,
                    "category": r.category,
                    "title": r.title,
                    "action": r.suggested_action
                }
                for r in recommendations
            ]
        }
