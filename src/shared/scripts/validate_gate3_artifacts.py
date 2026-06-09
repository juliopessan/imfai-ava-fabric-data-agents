"""
Validator for Gate 3 (Downstream Execution) artifacts.
Ensures all deployment phase deliverables meet quality requirements.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class Gate3ValidationResult:
    """Result of Gate 3 validation."""
    valid: bool
    completude: float
    quality: float
    reconciliation: float  # Reconciliation score (critical for Gate 3)
    errors: List[str]
    warnings: List[str]
    artifacts_found: List[str]
    artifacts_missing: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "completude": self.completude,
            "quality": self.quality,
            "reconciliation": self.reconciliation,
            "errors": self.errors,
            "warnings": self.warnings,
            "artifacts_found": self.artifacts_found,
            "artifacts_missing": self.artifacts_missing
        }


class Gate3ArtifactsValidator:
    """Validates Gate 3 (Downstream Execution) phase artifacts."""
    
    REQUIRED_ARTIFACTS = [
        "DDL_DELTA_TABLES.sql",
        "ETL_CONSOLIDACAO_DATABRICKS_JOB.py",
        "deployment_execution.json",
        "validation_reconciliation.json",
        "ROW_COUNT_RECONCILIATION.md",
        "SCHEMA_DIFF_VALIDATION.md"
    ]
    
    OPTIONAL_ARTIFACTS = [
        "DBT_MODELS_TESTS.sql",
        "GREAT_EXPECTATIONS_VALIDATION.py",
        "DATABRICKS_ALERTS_RUNBOOK.md",
        "MD5_RECONCILIATION.md"
    ]
    
    def __init__(self, artifacts_dir: Path):
        """Initialize validator with downstream artifacts directory."""
        self.artifacts_dir = Path(artifacts_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.artifacts_found: List[str] = []
        self.artifacts_missing: List[str] = []
    
    def validate(self) -> Gate3ValidationResult:
        """Run complete Gate 3 validation."""
        self.errors = []
        self.warnings = []
        self.artifacts_found = []
        self.artifacts_missing = []
        
        # Step 1: Directory existence
        if not self._check_directory_exists():
            return Gate3ValidationResult(
                valid=False,
                completude=0.0,
                quality=0.0,
                reconciliation=0.0,
                errors=self.errors,
                warnings=self.warnings,
                artifacts_found=[],
                artifacts_missing=self.REQUIRED_ARTIFACTS
            )
        
        # Step 2: Check required artifacts
        self._check_required_artifacts()
        
        # Step 3: Check optional artifacts
        self._check_optional_artifacts()
        
        # Step 4: Validate deployment artifacts
        self._validate_deployment_artifacts()
        
        # Step 5: Validate reconciliation (CRITICAL for Gate 3)
        reconciliation = self._validate_reconciliation()
        
        # Step 6: Check gate decision file
        self._check_gate_decision()
        
        # Calculate metrics
        completude = self._calculate_completude()
        quality = self._calculate_quality()
        
        # Gate 3 is valid only if: all required present AND reconciliation passed
        is_valid = (len(self.errors) == 0 and completude >= 0.9 and reconciliation >= 0.95)
        
        return Gate3ValidationResult(
            valid=is_valid,
            completude=completude,
            quality=quality,
            reconciliation=reconciliation,
            errors=self.errors,
            warnings=self.warnings,
            artifacts_found=self.artifacts_found,
            artifacts_missing=self.artifacts_missing
        )
    
    def _check_directory_exists(self) -> bool:
        """Check if downstream artifacts directory exists."""
        if not self.artifacts_dir.exists():
            self.errors.append(f"Downstream artifacts directory not found: {self.artifacts_dir}")
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
    
    def _validate_deployment_artifacts(self) -> None:
        """Validate deployment execution artifacts."""
        # Check DDL file
        ddl_path = self.artifacts_dir / "DDL_DELTA_TABLES.sql"
        if ddl_path.exists():
            content = ddl_path.read_text()
            if "CREATE" not in content.upper():
                self.warnings.append("DDL_DELTA_TABLES.sql: Missing CREATE statements")
        
        # Check ETL file
        etl_path = self.artifacts_dir / "ETL_CONSOLIDACAO_DATABRICKS_JOB.py"
        if etl_path.exists():
            content = etl_path.read_text()
            if "def " not in content or "databricks" not in content.lower():
                self.warnings.append("ETL file: May be incomplete or missing Databricks references")
        
        # Check deployment_execution.json
        deploy_path = self.artifacts_dir / "deployment_execution.json"
        if deploy_path.exists():
            try:
                deploy_data = json.loads(deploy_path.read_text())
                if not isinstance(deploy_data, dict):
                    self.warnings.append("deployment_execution.json: Expected dict at root")
                if "status" not in deploy_data:
                    self.warnings.append("deployment_execution.json: Missing 'status' field")
            except json.JSONDecodeError as e:
                self.errors.append(f"deployment_execution.json: Invalid JSON - {str(e)}")
    
    def _validate_reconciliation(self) -> float:
        """
        Validate reconciliation results. This is critical for Gate 3.
        Returns: reconciliation score (0.0-1.0)
        """
        reconciliation_path = self.artifacts_dir / "validation_reconciliation.json"
        
        if not reconciliation_path.exists():
            self.errors.append("validation_reconciliation.json not found (CRITICAL)")
            return 0.0
        
        try:
            recon_data = json.loads(reconciliation_path.read_text())
            
            # Check required reconciliation fields
            passed_checks = 0
            total_checks = 3
            
            if recon_data.get("row_count_validation") == "PASSED":
                passed_checks += 1
            else:
                self.errors.append("Row count reconciliation FAILED")
            
            if recon_data.get("schema_validation") == "PASSED":
                passed_checks += 1
            else:
                self.errors.append("Schema validation FAILED")
            
            if recon_data.get("data_quality_validation") == "PASSED":
                passed_checks += 1
            else:
                self.warnings.append("Data quality validation needs attention")
            
            return passed_checks / total_checks if total_checks > 0 else 0.0
            
        except json.JSONDecodeError as e:
            self.errors.append(f"validation_reconciliation.json: Invalid JSON - {str(e)}")
            return 0.0
    
    def _check_gate_decision(self) -> None:
        """Check gate3-decision.md file exists."""
        decision_path = self.artifacts_dir / "gate3-decision.md"
        if not decision_path.exists():
            self.warnings.append("gate3-decision.md not yet created (expected after gate review)")
    
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


def validate_gate3_artifacts(artifacts_dir: str) -> Dict[str, Any]:
    """
    Validate Gate 3 (Downstream Execution) artifacts.
    
    Args:
        artifacts_dir: Path to downstream artifacts directory
    
    Returns:
        Dict with validation results (includes reconciliation score)
    """
    validator = Gate3ArtifactsValidator(Path(artifacts_dir))
    result = validator.validate()
    return result.to_dict()
