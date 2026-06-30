#!/usr/bin/env python3
"""
Confidence Escalation System — scores decision confidence and triggers escalation.

Gate decisions with low confidence (<0.8) are escalated for human review.
High-confidence decisions (>0.95) auto-promote without review.
Medium-confidence (0.8-0.95) proceed with documentation.

Integration Points:
  - validate_gate1_artifacts.py: entity_discovery_confidence, risk_coverage
  - validate_gate2_artifacts.py: lineage_completeness, contract_confidence
  - validate_gate3_artifacts.py: reconciliation_confidence, deployment_readiness
"""

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
import json


class EscalationLevel(str, Enum):
    """Escalation decision levels."""
    AUTO_PROMOTE = "auto_promote"      # >= 0.95: proceed without review
    AUTO_PROCEED = "auto_proceed"       # 0.80-0.94: proceed with documentation
    HUMAN_REVIEW = "human_review"       # < 0.80: escalate to human
    BLOCKED = "blocked"                 # < 0.70: rejected


@dataclass
class ConfidenceScore:
    """Confidence scores for a gate decision."""
    gate: int  # 1, 2, 3
    wave_id: str
    
    # Core confidence dimensions
    entity_discovery_completeness: float = 0.0  # 0.0-1.0 (% entities found)
    lineage_traceability: float = 0.0           # 0.0-1.0 (% of lineage mapped)
    risk_assessment_coverage: float = 0.0       # 0.0-1.0 (% of risks identified)
    contract_quality: float = 0.0               # 0.0-1.0 (data contracts complete)
    reconciliation_confidence: float = 0.0      # 0.0-1.0 (row count match, schema ok)
    deployment_readiness: float = 0.0           # 0.0-1.0 (DDL/ETL validated)
    
    # Aggregates
    overall_confidence: float = field(init=False)
    escalation_level: EscalationLevel = field(init=False)
    escalation_reason: str = ""
    escalation_owner: Optional[str] = None
    
    def __post_init__(self):
        """Calculate aggregate scores."""
        # Weights by gate (higher weights on most critical components)
        weights = {
            1: {"discovery": 0.50, "lineage": 0.30, "risk": 0.20},
            2: {"lineage": 0.40, "contract": 0.35, "risk": 0.25},
            3: {"contract": 0.25, "reconciliation": 0.50, "deployment": 0.25}
        }
        
        w = weights.get(self.gate, {})
        self.overall_confidence = (
            (self.entity_discovery_completeness * w.get("discovery", 0.0)) +
            (self.lineage_traceability * w.get("lineage", 0.0)) +
            (self.risk_assessment_coverage * w.get("risk", 0.0)) +
            (self.contract_quality * w.get("contract", 0.0)) +
            (self.reconciliation_confidence * w.get("reconciliation", 0.0)) +
            (self.deployment_readiness * w.get("deployment", 0.0))
        )
        
        # Determine escalation level
        if self.overall_confidence >= 0.95:
            self.escalation_level = EscalationLevel.AUTO_PROMOTE
        elif self.overall_confidence >= 0.80:
            self.escalation_level = EscalationLevel.AUTO_PROCEED
        elif self.overall_confidence >= 0.70:
            self.escalation_level = EscalationLevel.HUMAN_REVIEW
            self.escalation_reason = f"Low confidence: {self.overall_confidence:.2%}"
        else:
            self.escalation_level = EscalationLevel.BLOCKED
            self.escalation_reason = f"Critical: confidence below 70% threshold ({self.overall_confidence:.2%})"


@dataclass
class EscalationDecision:
    """Human escalation decision record."""
    confidence_score: ConfidenceScore
    escalation_timestamp: str
    escalated_to: str  # Team lead, architect, etc.
    decision: str  # "approved", "rejected", "needs_rework"
    feedback: str = ""
    rework_items: List[str] = field(default_factory=list)


class ConfidenceEscalationEngine:
    """Manages confidence scoring and escalation workflow."""
    
    def __init__(self, escalation_threshold: float = 0.80):
        """Initialize engine."""
        self.escalation_threshold = escalation_threshold
        self.scores: Dict[str, ConfidenceScore] = {}
        self.decisions: Dict[str, EscalationDecision] = {}
    
    def score_gate1_upstream(
        self,
        wave_id: str,
        discovered_entities: int,
        total_expected_entities: int,
        lineage_entries: int,
        total_expected_lineage: int,
        identified_risks: int,
        total_risk_categories: int
    ) -> ConfidenceScore:
        """Score Gate 1 (Upstream discovery) confidence."""
        score = ConfidenceScore(
            gate=1,
            wave_id=wave_id,
            entity_discovery_completeness=discovered_entities / max(total_expected_entities, 1),
            lineage_traceability=lineage_entries / max(total_expected_lineage, 1),
            risk_assessment_coverage=identified_risks / max(total_risk_categories, 1)
        )
        
        key = f"{wave_id}_gate1"
        self.scores[key] = score
        return score
    
    def score_gate2_midstream(
        self,
        wave_id: str,
        lineage_completeness: float,
        contracts_defined: int,
        total_entities: int,
        identified_risks: int,
        total_risk_categories: int
    ) -> ConfidenceScore:
        """Score Gate 2 (Midstream design) confidence."""
        score = ConfidenceScore(
            gate=2,
            wave_id=wave_id,
            lineage_traceability=lineage_completeness,
            contract_quality=contracts_defined / max(total_entities, 1),
            risk_assessment_coverage=identified_risks / max(total_risk_categories, 1)
        )
        
        key = f"{wave_id}_gate2"
        self.scores[key] = score
        return score
    
    def score_gate3_downstream(
        self,
        wave_id: str,
        reconciliation_match_pct: float,  # 0.0-1.0
        schema_validation_passed: bool,
        ddl_validated: bool,
        etl_tested: bool
    ) -> ConfidenceScore:
        """Score Gate 3 (Downstream execution) confidence."""
        deployment_score = 1.0 if (ddl_validated and etl_tested) else 0.5
        
        score = ConfidenceScore(
            gate=3,
            wave_id=wave_id,
            reconciliation_confidence=reconciliation_match_pct,
            deployment_readiness=deployment_score if schema_validation_passed else 0.3,
            contract_quality=0.9 if schema_validation_passed else 0.5
        )
        
        key = f"{wave_id}_gate3"
        self.scores[key] = score
        return score
    
    def should_escalate(self, wave_id: str, gate: int) -> Tuple[bool, str]:
        """Determine if decision needs escalation."""
        key = f"{wave_id}_gate{gate}"
        if key not in self.scores:
            return True, "No confidence score found"
        
        score = self.scores[key]
        if score.escalation_level in [EscalationLevel.HUMAN_REVIEW, EscalationLevel.BLOCKED]:
            return True, score.escalation_reason
        return False, ""
    
    def record_escalation_decision(
        self,
        wave_id: str,
        gate: int,
        escalated_to: str,
        decision: str,
        feedback: str = "",
        rework_items: Optional[List[str]] = None
    ) -> EscalationDecision:
        """Record human escalation decision."""
        key = f"{wave_id}_gate{gate}"
        score = self.scores.get(key)
        if not score:
            raise ValueError(f"No confidence score for {key}")
        
        decision_record = EscalationDecision(
            confidence_score=score,
            escalation_timestamp=datetime.now(timezone.utc).isoformat(),
            escalated_to=escalated_to,
            decision=decision,
            feedback=feedback,
            rework_items=rework_items or []
        )
        
        self.decisions[key] = decision_record
        return decision_record
    
    def to_dict(self) -> Dict:
        """Export to dictionary."""
        return {
            "scores": {k: asdict(v) for k, v in self.scores.items()},
            "decisions": {
                k: {
                    "escalated_to": v.escalated_to,
                    "decision": v.decision,
                    "feedback": v.feedback,
                    "rework_items": v.rework_items,
                    "timestamp": v.escalation_timestamp
                }
                for k, v in self.decisions.items()
            }
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """Export to JSON."""
        return json.dumps(self.to_dict(), indent=2 if pretty else None)
