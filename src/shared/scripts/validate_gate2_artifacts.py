"""
Validator for Gate 2 (Midstream Design) artifacts.
Ensures all design phase deliverables meet quality requirements.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class Gate2ValidationResult:
    """Result of Gate 2 validation."""
    valid: bool
    completude: float
    quality: float
    errors: List[str]
    warnings: List[str]
    artifacts_found: List[str]
    artifacts_missing: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "completude": self.completude,
            "quality": self.quality,
            "errors": self.errors,
            "warnings": self.warnings,
            "artifacts_found": self.artifacts_found,
            "artifacts_missing": self.artifacts_missing
        }


class Gate2ArtifactsValidator:
    """Validates Gate 2 (Midstream Design) phase artifacts."""
    
    REQUIRED_ARTIFACTS = [
        "logical_data_model.json",
        "target_architecture.json",
        "ARCHITECTURE.md",
        "ARCHITECTURE_DECISIONS.md",
        "MONITORING_SPEC.md",
        "DATA_CONTRACTS.md"
    ]
    
    OPTIONAL_ARTIFACTS = [
        "DATA_QUALITY_RULES.md",
        "GOVERNANCE_POLICY.md",
        "METRICS_CATALOG.md",
        "code_generation_metadata.json"
    ]
    
    def __init__(self, artifacts_dir: Path):
        """Initialize validator with midstream artifacts directory."""
        self.artifacts_dir = Path(artifacts_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.artifacts_found: List[str] = []
        self.artifacts_missing: List[str] = []
    
    def validate(self) -> Gate2ValidationResult:
        """Run complete Gate 2 validation."""
        self.errors = []
        self.warnings = []
        self.artifacts_found = []
        self.artifacts_missing = []
        
        # Step 1: Directory existence
        if not self._check_directory_exists():
            return Gate2ValidationResult(
                valid=False,
                completude=0.0,
                quality=0.0,
                errors=self.errors,
                warnings=self.warnings,
                artifacts_found=[],
                artifacts_missing=self.REQUIRED_ARTIFACTS
            )
        
        # Step 2: Check required artifacts
        self._check_required_artifacts()
        
        # Step 3: Check optional artifacts
        self._check_optional_artifacts()
        
        # Step 4: Validate artifact content
        self._validate_artifact_content()
        
        # Step 5: Check gate decision file
        self._check_gate_decision()
        
        # Calculate metrics
        completude = self._calculate_completude()
        quality = self._calculate_quality()
        
        is_valid = len(self.errors) == 0 and completude >= 0.9
        
        return Gate2ValidationResult(
            valid=is_valid,
            completude=completude,
            quality=quality,
            errors=self.errors,
            warnings=self.warnings,
            artifacts_found=self.artifacts_found,
            artifacts_missing=self.artifacts_missing
        )
    
    def _check_directory_exists(self) -> bool:
        """Check if midstream artifacts directory exists."""
        if not self.artifacts_dir.exists():
            self.errors.append(f"Midstream artifacts directory not found: {self.artifacts_dir}")
            return False
        return True
    
    def _check_required_artifacts(self) -> None:
        """Check all required artifacts are present."""
        for artifact in self.REQUIRED_ARTIFACTS:
            artifact_path = self.artifacts_dir / artifact
            if artifact_path.exists():
                self.artifacts_found.append(artifact)
            else:
                self.artifacts_missing.append(artifact)
                self.errors.append(f"Missing required artifact: {artifact}")
    
    def _check_optional_artifacts(self) -> None:
        """Check optional artifacts (warnings if missing)."""
        for artifact in self.OPTIONAL_ARTIFACTS:
            artifact_path = self.artifacts_dir / artifact
            if not artifact_path.exists():
                self.warnings.append(f"Optional artifact missing: {artifact}")
            else:
                self.artifacts_found.append(artifact)
    
    def _validate_artifact_content(self) -> None:
        """Validate content of design artifacts."""
        # Check logical_data_model.json
        model_path = self.artifacts_dir / "logical_data_model.json"
        if model_path.exists():
            try:
                model_data = json.loads(model_path.read_text())
                if not isinstance(model_data, dict):
                    self.warnings.append("logical_data_model.json: Expected dict at root")
                if "entities" not in model_data and "tables" not in model_data:
                    self.warnings.append("logical_data_model.json: Missing entity definitions")
            except json.JSONDecodeError as e:
                self.errors.append(f"logical_data_model.json: Invalid JSON - {str(e)}")
        
        # Check ARCHITECTURE.md
        arch_path = self.artifacts_dir / "ARCHITECTURE.md"
        if arch_path.exists():
            content = arch_path.read_text()
            if len(content.strip()) < 200:
                self.warnings.append("ARCHITECTURE.md appears incomplete (< 200 chars)")
        
        # Check DATA_CONTRACTS.md
        contracts_path = self.artifacts_dir / "DATA_CONTRACTS.md"
        if contracts_path.exists():
            content = contracts_path.read_text()
            if "SLA" not in content and "sla" not in content.lower():
                self.warnings.append("DATA_CONTRACTS.md: Consider adding SLA definitions")
    
    def _check_gate_decision(self) -> None:
        """Check gate2-decision.md file exists."""
        decision_path = self.artifacts_dir / "gate2-decision.md"
        if not decision_path.exists():
            self.warnings.append("gate2-decision.md not yet created (expected after gate review)")
    
    def _calculate_completude(self) -> float:
        """Calculate artifact completude (0.0-1.0)."""
        total_required = len(self.REQUIRED_ARTIFACTS)
        found_required = len([a for a in self.artifacts_found if a in self.REQUIRED_ARTIFACTS])
        
        if total_required == 0:
            return 0.0
        
        return found_required / total_required
    
    def _calculate_quality(self) -> float:
        """Calculate quality score based on validation checks."""
        base_score = 1.0
        error_penalty = 0.20
        warning_penalty = 0.05
        
        score = base_score - (len(self.errors) * error_penalty) - (len(self.warnings) * warning_penalty)
        
        return max(0.0, min(1.0, score))


def validate_gate2_artifacts(artifacts_dir: str) -> Dict[str, Any]:
    """
    Validate Gate 2 (Midstream Design) artifacts.
    
    Args:
        artifacts_dir: Path to midstream artifacts directory
    
    Returns:
        Dict with validation results
    """
    validator = Gate2ArtifactsValidator(Path(artifacts_dir))
    result = validator.validate()
    return result.to_dict()
