"""
Governance Policy — Programmatic enforcement of governance rules.
Defines and enforces policies on artifact naming, structure, ownership, and quality.
"""

import re
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class PolicySeverity(Enum):
    """Policy violation severity."""
    ERROR = "error"        # Must fix
    WARNING = "warning"    # Should fix
    INFO = "info"          # Nice to have


@dataclass
class PolicyViolation:
    """A single policy violation."""
    policy_name: str
    severity: PolicySeverity
    entity: str
    message: str


class GovernancePolicy:
    """Base class for governance policies."""
    
    def __init__(self, name: str, description: str, severity: PolicySeverity = PolicySeverity.ERROR):
        """Initialize policy."""
        self.name = name
        self.description = description
        self.severity = severity
        self.violations: List[PolicyViolation] = []
    
    def validate(self, artifact: Dict[str, Any]) -> bool:
        """Validate an artifact against this policy."""
        raise NotImplementedError()
    
    def add_violation(self, entity: str, message: str) -> None:
        """Record a violation."""
        self.violations.append(
            PolicyViolation(self.name, self.severity, entity, message)
        )
    
    def clear_violations(self) -> None:
        """Clear all recorded violations."""
        self.violations = []


class ArtifactNamingPolicy(GovernancePolicy):
    """Policy: Enforce artifact naming conventions."""
    
    def __init__(self):
        super().__init__(
            "ArtifactNaming",
            "Artifact file names must follow conventions (UPPERCASE_SNAKE_CASE.md)",
            PolicySeverity.ERROR
        )
        self.required_artifacts = [
            "discovery_inventory.md",
            "data_lineage_map.md",
            "risk_assessment.json"
        ]
    
    def validate(self, artifact: Dict[str, Any]) -> bool:
        """Validate artifact naming."""
        self.clear_violations()
        
        filename = artifact.get("filename", "")
        if not filename:
            self.add_violation("unknown", "Filename not provided")
            return False
        
        # Check format: UPPERCASE_SNAKE_CASE or lowercase_snake_case
        pattern = r"^[a-zA-Z0-9_]+\.(md|json|py|sql)$"
        if not re.match(pattern, filename):
            self.add_violation(
                filename,
                f"File name '{filename}' doesn't match convention (use lowercase_snake_case.ext)"
            )
            return False
        
        return True


class ArtifactOwnershipPolicy(GovernancePolicy):
    """Policy: Enforce artifact ownership requirements."""
    
    def __init__(self):
        super().__init__(
            "ArtifactOwnership",
            "All artifacts must have identified owner",
            PolicySeverity.ERROR
        )
    
    def validate(self, artifact: Dict[str, Any]) -> bool:
        """Validate ownership assigned."""
        self.clear_violations()
        
        owner = artifact.get("owner")
        if not owner:
            self.add_violation(
                artifact.get("name", "unknown"),
                "No owner assigned. Assign to team member."
            )
            return False
        
        if not isinstance(owner, str) or len(owner.strip()) == 0:
            self.add_violation(
                artifact.get("name", "unknown"),
                f"Invalid owner: '{owner}'. Must be non-empty string."
            )
            return False
        
        return True


class DataQualityPolicy(GovernancePolicy):
    """Policy: Enforce data quality standards."""
    
    def __init__(self, min_quality_score: float = 0.80):
        super().__init__(
            "DataQuality",
            f"Data quality score must be ≥ {min_quality_score:.2f}",
            PolicySeverity.WARNING
        )
        self.min_quality_score = min_quality_score
    
    def validate(self, artifact: Dict[str, Any]) -> bool:
        """Validate data quality."""
        self.clear_violations()
        
        quality = artifact.get("quality_score", 1.0)
        if quality < self.min_quality_score:
            self.add_violation(
                artifact.get("name", "unknown"),
                f"Quality score {quality:.2f} below threshold {self.min_quality_score:.2f}"
            )
            return False
        
        return True


class ReconciliationPolicy(GovernancePolicy):
    """Policy: Enforce reconciliation requirements (Gate 3 critical)."""
    
    def __init__(self):
        super().__init__(
            "Reconciliation",
            "Gate 3 requires reconciliation validation: row_count, schema, data_quality all PASSED",
            PolicySeverity.ERROR
        )
    
    def validate(self, artifact: Dict[str, Any]) -> bool:
        """Validate reconciliation status."""
        self.clear_violations()
        
        reconciliation = artifact.get("reconciliation", {})
        required_checks = ["row_count_validation", "schema_validation", "data_quality_validation"]
        
        for check in required_checks:
            status = reconciliation.get(check)
            if status != "PASSED":
                self.add_violation(
                    artifact.get("name", "unknown"),
                    f"Reconciliation check '{check}' is '{status}', must be 'PASSED'"
                )
                return False
        
        return True


class PolicyEngine:
    """Engine for managing and enforcing policies."""
    
    def __init__(self):
        """Initialize policy engine."""
        self.policies: Dict[str, GovernancePolicy] = {}
    
    def register_policy(self, policy: GovernancePolicy) -> None:
        """Register a policy."""
        self.policies[policy.name] = policy
    
    def enforce(self, artifact: Dict[str, Any]) -> tuple[bool, List[PolicyViolation]]:
        """
        Enforce all registered policies on an artifact.
        Returns: (all_pass, list_of_violations)
        """
        all_violations = []
        
        for policy in self.policies.values():
            policy_pass = policy.validate(artifact)
            all_violations.extend(policy.violations)
        
        # Separate by severity
        errors = [v for v in all_violations if v.severity == PolicySeverity.ERROR]
        
        # Fail if any errors
        all_pass = len(errors) == 0
        
        return all_pass, all_violations
    
    def get_violations_by_severity(self, violations: List[PolicyViolation]) -> Dict[PolicySeverity, List[PolicyViolation]]:
        """Group violations by severity."""
        result = {}
        for severity in PolicySeverity:
            result[severity] = [v for v in violations if v.severity == severity]
        return result
    
    def get_summary(self, violations: List[PolicyViolation]) -> str:
        """Get human-readable summary of violations."""
        by_severity = self.get_violations_by_severity(violations)
        
        summary = []
        for severity in [PolicySeverity.ERROR, PolicySeverity.WARNING, PolicySeverity.INFO]:
            viols = by_severity[severity]
            if viols:
                summary.append(f"{len(viols)} {severity.value.upper()}: {', '.join(v.policy_name for v in viols[:3])}")
        
        return " | ".join(summary) if summary else "All policies passed"


def create_default_policy_engine() -> PolicyEngine:
    """Helper: Create engine with standard policies."""
    engine = PolicyEngine()
    
    engine.register_policy(ArtifactNamingPolicy())
    engine.register_policy(ArtifactOwnershipPolicy())
    engine.register_policy(DataQualityPolicy(min_quality_score=0.80))
    engine.register_policy(ReconciliationPolicy())
    
    return engine
