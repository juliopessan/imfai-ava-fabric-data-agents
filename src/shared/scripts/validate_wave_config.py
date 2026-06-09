"""
Validator for wave-config.yaml files.
Ensures DMF wave configuration meets minimum requirements.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of validation check."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "score": self.score
        }


class WaveConfigValidator:
    """Validates wave-config.yaml structure and content."""
    
    REQUIRED_FIELDS = [
        "wave_id",
        "project_name",
        "discovery_owner",
        "target_platform",
        "entities",
        "gates"
    ]
    
    VALID_PLATFORMS = ["databricks", "fabric", "snowflake", "synapse", "bigquery"]
    
    VALID_GATES = ["gate1_required", "gate2_required", "gate3_required"]
    
    def __init__(self, config_path: Path):
        """Initialize validator with config file path."""
        self.config_path = Path(config_path)
        self.config_data = None
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> ValidationResult:
        """Run complete validation."""
        self.errors = []
        self.warnings = []
        
        # Step 1: File existence
        if not self._check_file_exists():
            return ValidationResult(
                valid=False,
                errors=self.errors,
                warnings=self.warnings,
                score=0.0
            )
        
        # Step 2: YAML syntax
        if not self._check_yaml_syntax():
            return ValidationResult(
                valid=False,
                errors=self.errors,
                warnings=self.warnings,
                score=0.1
            )
        
        # Step 3: Required fields
        self._check_required_fields()
        
        # Step 4: Field types & values
        self._check_field_types()
        
        # Step 5: Platform validation
        self._check_platform()
        
        # Step 6: Entity structure
        self._check_entities()
        
        # Step 7: Gates configuration
        self._check_gates()
        
        # Calculate score
        score = self._calculate_score()
        
        is_valid = len(self.errors) == 0
        
        return ValidationResult(
            valid=is_valid,
            errors=self.errors,
            warnings=self.warnings,
            score=score
        )
    
    def _check_file_exists(self) -> bool:
        """Check if config file exists."""
        if not self.config_path.exists():
            self.errors.append(f"Wave config file not found: {self.config_path}")
            return False
        return True
    
    def _check_yaml_syntax(self) -> bool:
        """Check YAML syntax validity."""
        try:
            with open(self.config_path, 'r') as f:
                self.config_data = yaml.safe_load(f)
            
            if self.config_data is None:
                self.errors.append("Wave config is empty (no YAML content)")
                return False
            
            if not isinstance(self.config_data, dict):
                self.errors.append(f"Wave config must be a YAML dict, got {type(self.config_data).__name__}")
                return False
                
            return True
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading config file: {str(e)}")
            return False
    
    def _check_required_fields(self) -> None:
        """Check all required fields are present."""
        for field in self.REQUIRED_FIELDS:
            if field not in self.config_data:
                self.errors.append(f"Missing required field: {field}")
            elif self.config_data[field] is None or self.config_data[field] == "":
                self.errors.append(f"Required field is empty: {field}")
    
    def _check_field_types(self) -> None:
        """Check field types."""
        if "wave_id" in self.config_data:
            if not isinstance(self.config_data["wave_id"], str):
                self.errors.append("wave_id must be a string")
        
        if "project_name" in self.config_data:
            if not isinstance(self.config_data["project_name"], str):
                self.errors.append("project_name must be a string")
        
        if "discovery_owner" in self.config_data:
            if not isinstance(self.config_data["discovery_owner"], str):
                self.errors.append("discovery_owner must be a string (email format recommended)")
        
        if "entities" in self.config_data:
            if not isinstance(self.config_data["entities"], list):
                self.errors.append("entities must be a list")
            elif len(self.config_data["entities"]) == 0:
                self.warnings.append("entities list is empty (no tables/views to migrate)")
        
        if "gates" in self.config_data:
            if not isinstance(self.config_data["gates"], dict):
                self.errors.append("gates must be a dict")
    
    def _check_platform(self) -> None:
        """Check target_platform is valid."""
        if "target_platform" in self.config_data:
            platform = self.config_data["target_platform"]
            if platform not in self.VALID_PLATFORMS:
                self.errors.append(
                    f"Invalid target_platform: {platform}. "
                    f"Must be one of: {', '.join(self.VALID_PLATFORMS)}"
                )
    
    def _check_entities(self) -> None:
        """Check entities structure."""
        if "entities" not in self.config_data:
            return
        
        entities = self.config_data["entities"]
        if not isinstance(entities, list):
            return  # Already caught in _check_field_types
        
        for idx, entity in enumerate(entities):
            if not isinstance(entity, dict):
                self.errors.append(f"Entity {idx} is not a dict: {type(entity).__name__}")
                continue
            
            if "name" not in entity:
                self.errors.append(f"Entity {idx}: missing 'name' field")
            elif not isinstance(entity["name"], str):
                self.errors.append(f"Entity {idx}: 'name' must be a string")
    
    def _check_gates(self) -> None:
        """Check gates configuration."""
        if "gates" not in self.config_data:
            return
        
        gates = self.config_data["gates"]
        if not isinstance(gates, dict):
            return  # Already caught in _check_field_types
        
        # At least one gate must be required
        gate_flags = [gates.get(g, False) for g in self.VALID_GATES]
        if not any(gate_flags):
            self.warnings.append("No gates are required (all gates set to False)")
    
    def _calculate_score(self) -> float:
        """Calculate validation score."""
        base_score = 1.0
        error_penalty = 0.15  # Each error deducts 15%
        warning_penalty = 0.05  # Each warning deducts 5%
        
        score = base_score - (len(self.errors) * error_penalty) - (len(self.warnings) * warning_penalty)
        
        # Clamp between 0.0 and 1.0
        return max(0.0, min(1.0, score))


def validate_wave_config(config_path: str) -> Dict[str, Any]:
    """
    Validate a wave-config.yaml file.
    
    Args:
        config_path: Path to wave-config.yaml
    
    Returns:
        Dict with validation results
    """
    validator = WaveConfigValidator(Path(config_path))
    result = validator.validate()
    return result.to_dict()
