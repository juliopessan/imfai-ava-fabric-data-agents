"""
Validator for Gate 1 (Upstream Discovery) artifacts.
Ensures all discovery phase deliverables meet quality requirements.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class Gate1ValidationResult:
    """Result of Gate 1 validation."""
    valid: bool
    completude: float  # 0.0-1.0: percentage of required artifacts found
    quality: float    # 0.0-1.0: quality score based on content checks
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


class Gate1ArtifactsValidator:
    """Validates Gate 1 (Upstream) phase artifacts."""
    
    REQUIRED_ARTIFACTS = [
        "discovery_inventory.md",
        "data_lineage_map.md",
        "STTM_BUSINESS_REQUIREMENTS.md",
        "as_is_architecture.md",
        "risk_assessment.json"
    ]
    
    OPTIONAL_ARTIFACTS = [
        "schemas_catalog.json",
        "orchestration_inventory.json",
        "cleanup_recommendations.json"
    ]
    
    def __init__(self, artifacts_dir: Path):
        """Initialize validator with upstream artifacts directory."""
        self.artifacts_dir = Path(artifacts_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.artifacts_found: List[str] = []
        self.artifacts_missing: List[str] = []
    
    def validate(self) -> Gate1ValidationResult:
        """Run complete Gate 1 validation."""
        self.errors = []
        self.warnings = []
        self.artifacts_found = []
        self.artifacts_missing = []
        
        # Step 1: Directory existence
        if not self._check_directory_exists():
            return Gate1ValidationResult(
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
        
        return Gate1ValidationResult(
            valid=is_valid,
            completude=completude,
            quality=quality,
            errors=self.errors,
            warnings=self.warnings,
            artifacts_found=self.artifacts_found,
            artifacts_missing=self.artifacts_missing
        )
    
    def _check_directory_exists(self) -> bool:
        """Check if upstream artifacts directory exists."""
        if not self.artifacts_dir.exists():
            self.errors.append(f"Upstream artifacts directory not found: {self.artifacts_dir}")
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
        """Validate content of discovered artifacts."""
        # Check discovery_inventory
        inv_path = self.artifacts_dir / "discovery_inventory.md"
        if inv_path.exists():
            content = inv_path.read_text()
            if len(content.strip()) < 100:
                self.warnings.append("discovery_inventory.md appears incomplete (< 100 chars)")
        
        # Check STTM
        sttm_path = self.artifacts_dir / "STTM_BUSINESS_REQUIREMENTS.md"
        if sttm_path.exists():
            content = sttm_path.read_text()
            if "STTM" not in content and "sttm" not in content.lower():
                self.warnings.append("STTM_BUSINESS_REQUIREMENTS.md: Missing STTM reference")
        
        # Check risk_assessment.json
        risk_path = self.artifacts_dir / "risk_assessment.json"
        if risk_path.exists():
            try:
                risk_data = json.loads(risk_path.read_text())
                if not isinstance(risk_data, dict):
                    self.warnings.append("risk_assessment.json: Expected dict at root")
            except json.JSONDecodeError as e:
                self.errors.append(f"risk_assessment.json: Invalid JSON - {str(e)}")
    
    def _check_gate_decision(self) -> None:
        """Check gate1-decision.md file exists."""
        decision_path = self.artifacts_dir / "gate1-decision.md"
        if not decision_path.exists():
            self.warnings.append("gate1-decision.md not yet created (expected after gate review)")
    
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


def validate_gate1_artifacts(artifacts_dir: str) -> Dict[str, Any]:
    """
    Validate Gate 1 (Upstream) artifacts.
    
    Args:
        artifacts_dir: Path to upstream artifacts directory
    
    Returns:
        Dict with validation results
    """
    validator = Gate1ArtifactsValidator(Path(artifacts_dir))
    result = validator.validate()
    return result.to_dict()
