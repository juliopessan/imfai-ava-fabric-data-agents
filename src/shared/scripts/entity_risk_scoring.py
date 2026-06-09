"""
Entity Risk Scoring — Calculates composite risk scores per entity.
Combines probability, impact, and mitigation factors into single score.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import json


class RiskDimension(Enum):
    """Risk dimensions."""
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    SCHEDULE = "schedule"
    RESOURCE = "resource"
    DATA_QUALITY = "data_quality"
    SECURITY = "security"


class RiskLevel(Enum):
    """Risk level classification."""
    MINIMAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


@dataclass
class DimensionScore:
    """Score for single risk dimension."""
    dimension: RiskDimension
    probability: float  # 0.0-1.0
    impact: float  # 0.0-1.0
    mitigation_effectiveness: float  # 0.0-1.0
    residual_score: float = 0.0
    
    def __post_init__(self):
        """Calculate residual score."""
        base_score = self.probability * self.impact * 100
        self.residual_score = base_score * (1.0 - self.mitigation_effectiveness)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "dimension": self.dimension.value,
            "probability": round(self.probability, 4),
            "impact": round(self.impact, 4),
            "mitigation_effectiveness": round(self.mitigation_effectiveness, 4),
            "residual_score": round(self.residual_score, 2)
        }


@dataclass
class EntityRiskScore:
    """Composite risk score for entity."""
    entity_name: str
    dimension_scores: List[DimensionScore] = field(default_factory=list)
    overall_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.MINIMAL
    primary_risks: List[str] = field(default_factory=list)
    mitigation_recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "entity_name": self.entity_name,
            "dimension_scores": [d.to_dict() for d in self.dimension_scores],
            "overall_score": round(self.overall_score, 2),
            "risk_level": self.risk_level.name,
            "primary_risks": self.primary_risks,
            "mitigation_recommendations": self.mitigation_recommendations,
            "timestamp": self.timestamp
        }


class EntityRiskScoringEngine:
    """Calculates entity risk scores."""
    
    def __init__(self):
        """Initialize engine."""
        self.entity_scores: Dict[str, EntityRiskScore] = {}
    
    def add_dimension_score(
        self,
        entity_name: str,
        dimension: RiskDimension,
        probability: float,
        impact: float,
        mitigation_effectiveness: float = 0.0
    ) -> None:
        """Add dimension score for entity."""
        if entity_name not in self.entity_scores:
            self.entity_scores[entity_name] = EntityRiskScore(entity_name=entity_name)
        
        dim_score = DimensionScore(
            dimension=dimension,
            probability=probability,
            impact=impact,
            mitigation_effectiveness=mitigation_effectiveness
        )
        
        self.entity_scores[entity_name].dimension_scores.append(dim_score)
    
    def calculate_entity_risk(
        self,
        entity_name: str
    ) -> EntityRiskScore:
        """
        Calculate composite risk score for entity.
        
        Args:
            entity_name: Entity name
        
        Returns:
            Entity risk score with classifications
        """
        if entity_name not in self.entity_scores:
            return EntityRiskScore(entity_name=entity_name)
        
        score = self.entity_scores[entity_name]
        
        if not score.dimension_scores:
            score.overall_score = 0.0
            score.risk_level = RiskLevel.MINIMAL
            return score
        
        # Calculate weighted average of residual scores
        total_residual = sum(d.residual_score for d in score.dimension_scores)
        avg_residual = total_residual / len(score.dimension_scores)
        
        # Normalize to 0-100
        score.overall_score = min(100.0, avg_residual)
        
        # Classify risk level
        if score.overall_score < 10:
            score.risk_level = RiskLevel.MINIMAL
        elif score.overall_score < 25:
            score.risk_level = RiskLevel.LOW
        elif score.overall_score < 50:
            score.risk_level = RiskLevel.MEDIUM
        elif score.overall_score < 75:
            score.risk_level = RiskLevel.HIGH
        else:
            score.risk_level = RiskLevel.CRITICAL
        
        # Identify primary risks (highest scoring dimensions)
        sorted_dims = sorted(score.dimension_scores, key=lambda d: d.residual_score, reverse=True)
        score.primary_risks = [
            f"{d.dimension.value} ({d.residual_score:.1f})"
            for d in sorted_dims[:3]  # Top 3
        ]
        
        # Generate recommendations
        score.mitigation_recommendations = self._generate_recommendations(score)
        
        return score
    
    def _generate_recommendations(self, score: EntityRiskScore) -> List[str]:
        """Generate mitigation recommendations."""
        recommendations = []
        
        for dim_score in score.dimension_scores:
            if dim_score.residual_score > 40:
                if dim_score.dimension == RiskDimension.TECHNICAL:
                    recommendations.append(f"Increase technical validation for {score.entity_name}")
                elif dim_score.dimension == RiskDimension.SECURITY:
                    recommendations.append(f"Enhance security controls for {score.entity_name}")
                elif dim_score.dimension == RiskDimension.DATA_QUALITY:
                    recommendations.append(f"Implement data quality checks for {score.entity_name}")
                elif dim_score.dimension == RiskDimension.SCHEDULE:
                    recommendations.append(f"Add buffer time for {score.entity_name} migration")
        
        if not recommendations:
            recommendations.append(f"Standard risk mitigation for {score.entity_name}")
        
        return recommendations
    
    def get_high_risk_entities(self, threshold: float = 50.0) -> List[EntityRiskScore]:
        """Get entities above risk threshold."""
        high_risk = []
        
        for entity_name, score in self.entity_scores.items():
            calculated = self.calculate_entity_risk(entity_name)
            if calculated.overall_score >= threshold:
                high_risk.append(calculated)
        
        return sorted(high_risk, key=lambda s: s.overall_score, reverse=True)
    
    def get_risk_summary(self) -> Dict[str, int]:
        """Get count of entities by risk level."""
        summary = {
            "minimal": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }
        
        for entity_name in self.entity_scores.keys():
            score = self.calculate_entity_risk(entity_name)
            level_key = score.risk_level.name.lower()
            summary[level_key] += 1
        
        return summary
    
    def get_average_risk_score(self) -> float:
        """Get average risk score across all entities."""
        if not self.entity_scores:
            return 0.0
        
        total = sum(
            self.calculate_entity_risk(e).overall_score
            for e in self.entity_scores.keys()
        )
        
        return total / len(self.entity_scores)
    
    def generate_risk_report(self) -> str:
        """Generate human-readable risk report."""
        report = "Entity Risk Scoring Report\n"
        report += f"Total Entities: {len(self.entity_scores)}\n\n"
        
        summary = self.get_risk_summary()
        report += "Risk Distribution:\n"
        for level, count in summary.items():
            report += f"  {level.upper()}: {count}\n"
        
        report += f"\nAverage Risk Score: {self.get_average_risk_score():.1f}\n\n"
        
        high_risk = self.get_high_risk_entities(threshold=60.0)
        if high_risk:
            report += "High-Risk Entities:\n"
            for score in high_risk[:5]:
                report += f"  {score.entity_name}: {score.overall_score:.1f} ({score.risk_level.name})\n"
        
        return report
    
    def save_scores(self, file_path: str) -> None:
        """Save scores to file."""
        scores_dict = {
            entity_name: self.calculate_entity_risk(entity_name).to_dict()
            for entity_name in self.entity_scores.keys()
        }
        
        with open(file_path, "w") as f:
            json.dump(scores_dict, f, indent=2)
