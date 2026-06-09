"""
Risk Rollup Calculator — Aggregates entity-level risks to wave level.
Computes composite risk scores and identifies high-impact risk items.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json


class RiskCategory(Enum):
    """Risk categories."""
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    SCHEDULE = "schedule"
    RESOURCE = "resource"
    DATA_QUALITY = "data_quality"
    SECURITY = "security"


class RiskSeverity(Enum):
    """Risk severity levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


@dataclass
class EntityRisk:
    """Risk associated with an entity."""
    entity_name: str
    category: RiskCategory
    severity: RiskSeverity
    description: str
    probability: float  # 0.0-1.0
    impact: float       # 0.0-1.0
    mitigation: str
    residual_risk: float  # Post-mitigation


@dataclass
class WaveRiskProfile:
    """Aggregated risk profile for a wave."""
    wave_id: str
    total_risks: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    overall_risk_score: float  # 0.0-100.0
    risk_trend: str  # "increasing", "stable", "decreasing"
    top_risks: List[Dict[str, Any]]
    by_category: Dict[str, int]


class RiskRollupCalculator:
    """Calculates wave-level risk from entity risks."""
    
    def __init__(self):
        """Initialize calculator."""
        self.entity_risks: Dict[str, List[EntityRisk]] = {}
    
    def add_entity_risk(
        self,
        entity_name: str,
        category: RiskCategory,
        severity: RiskSeverity,
        description: str,
        probability: float,
        impact: float,
        mitigation: str
    ) -> EntityRisk:
        """Add a risk for an entity."""
        if entity_name not in self.entity_risks:
            self.entity_risks[entity_name] = []
        
        # Calculate residual risk (post-mitigation)
        # Assume mitigation reduces risk by 30%
        residual_risk = probability * impact * 0.7
        
        risk = EntityRisk(
            entity_name=entity_name,
            category=category,
            severity=severity,
            description=description,
            probability=probability,
            impact=impact,
            mitigation=mitigation,
            residual_risk=residual_risk
        )
        
        self.entity_risks[entity_name].append(risk)
        return risk
    
    def calculate_wave_risk_profile(self, wave_id: str) -> WaveRiskProfile:
        """Calculate aggregate risk profile for wave."""
        if not self.entity_risks:
            return WaveRiskProfile(
                wave_id=wave_id,
                total_risks=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                overall_risk_score=0.0,
                risk_trend="stable",
                top_risks=[],
                by_category={}
            )
        
        # Aggregate risks
        all_risks = []
        severity_counts = {s: 0 for s in RiskSeverity}
        category_counts = {c.value: 0 for c in RiskCategory}
        
        for entity_risks in self.entity_risks.values():
            all_risks.extend(entity_risks)
            for risk in entity_risks:
                severity_counts[risk.severity] += 1
                category_counts[risk.category.value] += 1
        
        # Calculate overall risk score (0-100)
        # Weight by severity and residual risk
        weighted_risks = [
            r.severity.value * r.residual_risk * 10
            for r in all_risks
        ]
        overall_score = sum(weighted_risks) / len(all_risks) if all_risks else 0
        overall_score = min(100.0, max(0.0, overall_score))
        
        # Identify top 5 risks
        top_risks = sorted(all_risks, key=lambda r: r.residual_risk, reverse=True)[:5]
        
        profile = WaveRiskProfile(
            wave_id=wave_id,
            total_risks=len(all_risks),
            critical_count=severity_counts[RiskSeverity.CRITICAL],
            high_count=severity_counts[RiskSeverity.HIGH],
            medium_count=severity_counts[RiskSeverity.MEDIUM],
            low_count=severity_counts[RiskSeverity.LOW],
            overall_risk_score=overall_score,
            risk_trend=self._determine_risk_trend(overall_score),
            top_risks=[
                {
                    "entity": r.entity_name,
                    "category": r.category.value,
                    "severity": r.severity.name,
                    "residual_risk": round(r.residual_risk, 3),
                    "description": r.description
                }
                for r in top_risks
            ],
            by_category={k: v for k, v in category_counts.items() if v > 0}
        )
        
        return profile
    
    def _determine_risk_trend(self, score: float) -> str:
        """Determine risk trend from score."""
        if score > 70:
            return "increasing"
        elif score < 30:
            return "decreasing"
        else:
            return "stable"
    
    def get_risks_by_category(self, category: RiskCategory) -> List[EntityRisk]:
        """Get all risks in a category."""
        risks = []
        for entity_risks in self.entity_risks.values():
            risks.extend([r for r in entity_risks if r.category == category])
        return risks
    
    def get_high_residual_risks(self, threshold: float = 0.5) -> List[EntityRisk]:
        """Get risks with high residual risk after mitigation."""
        risks = []
        for entity_risks in self.entity_risks.values():
            risks.extend([r for r in entity_risks if r.residual_risk >= threshold])
        return sorted(risks, key=lambda r: r.residual_risk, reverse=True)
    
    def generate_risk_mitigation_plan(self) -> str:
        """Generate mitigation plan for high-risk items."""
        high_risks = self.get_high_residual_risks(threshold=0.6)
        
        lines = ["# Risk Mitigation Plan\n"]
        
        for idx, risk in enumerate(high_risks, 1):
            lines.append(f"{idx}. **{risk.category.value.upper()}** - {risk.entity_name}")
            lines.append(f"   - Severity: {risk.severity.name}")
            lines.append(f"   - Description: {risk.description}")
            lines.append(f"   - Mitigation: {risk.mitigation}")
            lines.append(f"   - Residual Risk: {risk.residual_risk:.1%}\n")
        
        return "\n".join(lines)
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get summary of risks by severity."""
        all_risks = []
        for entity_risks in self.entity_risks.values():
            all_risks.extend(entity_risks)
        
        severity_counts = {s.name: 0 for s in RiskSeverity}
        for risk in all_risks:
            severity_counts[risk.severity.name] += 1
        
        return {
            "total_risks": len(all_risks),
            "by_severity": severity_counts,
            "by_category": {
                c.value: len(self.get_risks_by_category(c))
                for c in RiskCategory
            },
            "avg_residual_risk": sum(r.residual_risk for r in all_risks) / len(all_risks) if all_risks else 0
        }
    
    def save_risk_profile(self, profile: WaveRiskProfile, output_path) -> None:
        """Save risk profile to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = asdict(profile)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
