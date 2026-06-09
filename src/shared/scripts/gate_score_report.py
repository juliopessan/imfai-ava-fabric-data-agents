"""
Gate Score Report Generator.
Calculates GateScore for wave progression based on weighted metrics.

GateScore formula: 0.35 × Completude + 0.25 × Qualidade + 0.20 × RiscoResidual + 0.20 × Reconciliação
Approval threshold: >= 0.85 (approved)
Conditional threshold: 0.70-0.84 (approved with open items)
Blocked threshold: < 0.70 (blocked)
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from pathlib import Path
import json
from datetime import datetime, timezone


@dataclass
class GateScoreResult:
    """Result of GateScore calculation."""
    gate_number: int
    wave_id: str
    score: float
    completude: float
    quality: float
    residual_risk: float
    reconciliation: float
    status: str  # "approved", "conditional", "blocked"
    calculated_at: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_number": self.gate_number,
            "wave_id": self.wave_id,
            "score": round(self.score, 4),
            "completude": round(self.completude, 4),
            "quality": round(self.quality, 4),
            "residual_risk": round(self.residual_risk, 4),
            "reconciliation": round(self.reconciliation, 4),
            "status": self.status,
            "calculated_at": self.calculated_at,
            "recommendations": self.recommendations
        }


class GateScoreCalculator:
    """Calculates GateScore for DMF wave progression."""
    
    # Weighting formula
    COMPLETUDE_WEIGHT = 0.35
    QUALITY_WEIGHT = 0.25
    RESIDUAL_RISK_WEIGHT = 0.20
    RECONCILIATION_WEIGHT = 0.20
    
    # Approval thresholds
    APPROVAL_THRESHOLD = 0.85
    CONDITIONAL_THRESHOLD = 0.70
    
    def __init__(self, gate_number: int, wave_id: str):
        """Initialize calculator for a specific gate."""
        self.gate_number = gate_number
        self.wave_id = wave_id
    
    def calculate(
        self,
        completude: float,
        quality: float,
        residual_risk: float,
        reconciliation: float = 1.0
    ) -> GateScoreResult:
        """
        Calculate GateScore using weighted formula.
        
        Args:
            completude: Artifact completude (0.0-1.0)
            quality: Quality score (0.0-1.0)
            residual_risk: Residual risk score (0.0-1.0, where 1.0 = no risk)
            reconciliation: Reconciliation success rate (0.0-1.0, for Gate 3)
        
        Returns:
            GateScoreResult with score and status
        """
        # Calculate weighted score
        score = (
            (completude * self.COMPLETUDE_WEIGHT) +
            (quality * self.QUALITY_WEIGHT) +
            (residual_risk * self.RESIDUAL_RISK_WEIGHT) +
            (reconciliation * self.RECONCILIATION_WEIGHT)
        )
        
        # Determine status
        if score >= self.APPROVAL_THRESHOLD:
            status = "approved"
        elif score >= self.CONDITIONAL_THRESHOLD:
            status = "conditional"
        else:
            status = "blocked"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            completude, quality, residual_risk, reconciliation, status
        )
        
        return GateScoreResult(
            gate_number=self.gate_number,
            wave_id=self.wave_id,
            score=score,
            completude=completude,
            quality=quality,
            residual_risk=residual_risk,
            reconciliation=reconciliation,
            status=status,
            calculated_at=datetime.now(timezone.utc).isoformat(),
            recommendations=recommendations
        )
    
    def _generate_recommendations(
        self,
        completude: float,
        quality: float,
        residual_risk: float,
        reconciliation: float,
        status: str
    ) -> List[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        
        if completude < 0.9:
            recommendations.append(
                f"⚠️ Completude is low ({completude:.0%}). Ensure all required artifacts are generated."
            )
        
        if quality < 0.8:
            recommendations.append(
                f"⚠️ Quality score is low ({quality:.0%}). Review artifacts for content gaps and errors."
            )
        
        if residual_risk < 0.7:
            recommendations.append(
                f"🔴 High residual risk detected ({residual_risk:.0%}). Escalate to decision board."
            )
        
        if reconciliation < 0.95 and self.gate_number == 3:
            recommendations.append(
                f"🔴 Reconciliation incomplete ({reconciliation:.0%}). Validate row counts and schemas before go-live."
            )
        
        if status == "approved":
            recommendations.append("✅ Gate ready for approval. Proceed to next phase.")
        elif status == "conditional":
            recommendations.append(
                "⚡ Gate can proceed with conditions. Document open items in gate-decision.md."
            )
        else:
            recommendations.append(
                "🛑 Gate is blocked. Resolve critical issues before resubmission."
            )
        
        return recommendations
    
    @staticmethod
    def from_artifacts_dict(gate_number: int, wave_id: str, artifacts_dict: Dict[str, Any]) -> GateScoreResult:
        """
        Calculate GateScore directly from artifact validation results.
        
        Args:
            gate_number: Gate number (1, 2, or 3)
            wave_id: Wave identifier
            artifacts_dict: Result from validate_gate*_artifacts() function
        
        Returns:
            GateScoreResult
        """
        calculator = GateScoreCalculator(gate_number, wave_id)
        
        completude = artifacts_dict.get("completude", 0.0)
        quality = artifacts_dict.get("quality", 0.0)
        
        # Default risk score (will be overridden by risk assessment in Gate 1)
        residual_risk = 0.8  # Assume moderate risk if not specified
        
        # For Gate 3, use reconciliation score if available
        reconciliation = artifacts_dict.get("reconciliation", 1.0)
        
        return calculator.calculate(completude, quality, residual_risk, reconciliation)


def calculate_gate_score(
    gate_number: int,
    wave_id: str,
    completude: float,
    quality: float,
    residual_risk: float,
    reconciliation: float = 1.0
) -> Dict[str, Any]:
    """
    Calculate and return GateScore.
    
    Args:
        gate_number: Gate number (1, 2, or 3)
        wave_id: Wave identifier
        completude: Artifact completude (0.0-1.0)
        quality: Quality score (0.0-1.0)
        residual_risk: Residual risk score (0.0-1.0)
        reconciliation: Reconciliation rate (0.0-1.0, for Gate 3)
    
    Returns:
        Dict with GateScore results
    """
    calculator = GateScoreCalculator(gate_number, wave_id)
    result = calculator.calculate(completude, quality, residual_risk, reconciliation)
    return result.to_dict()


def calculate_gate_score_from_artifacts(
    gate_number: int,
    wave_id: str,
    artifacts_validation: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate GateScore from artifact validation results.
    
    Args:
        gate_number: Gate number (1, 2, or 3)
        wave_id: Wave identifier
        artifacts_validation: Result from validate_gate*_artifacts()
    
    Returns:
        Dict with GateScore results
    """
    result = GateScoreCalculator.from_artifacts_dict(gate_number, wave_id, artifacts_validation)
    return result.to_dict()
