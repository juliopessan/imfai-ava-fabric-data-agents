"""
Entity Classification Engine — Auto-classifies entities by data sensitivity.
Assigns sensitivity labels based on data patterns and metadata.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
from datetime import datetime
import json
import re


class SensitivityLevel(Enum):
    """Data sensitivity levels."""
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4


class ClassificationReason(Enum):
    """Reasons for classification."""
    PII_DETECTED = "pii_detected"
    FINANCIAL_DATA = "financial_data"
    HEALTH_DATA = "health_data"
    ENCRYPTION_REQUIRED = "encryption_required"
    AUDIT_TRAIL_REQUIRED = "audit_trail_required"
    INTERNAL_USE_ONLY = "internal_use_only"
    PUBLIC_DATA = "public_data"


@dataclass
class ClassificationRule:
    """Classification rule definition."""
    rule_id: str
    name: str
    pattern: str  # Column name pattern or regex
    sensitivity: SensitivityLevel
    reason: ClassificationReason
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "pattern": self.pattern,
            "sensitivity": self.sensitivity.name,
            "reason": self.reason.value
        }


@dataclass
class EntityClassification:
    """Classification for single entity."""
    entity_name: str
    sensitivity_level: SensitivityLevel
    column_classifications: Dict[str, SensitivityLevel] = field(default_factory=dict)
    detected_reasons: List[ClassificationReason] = field(default_factory=list)
    requires_encryption: bool = False
    requires_audit: bool = False
    requires_masking: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "entity_name": self.entity_name,
            "sensitivity_level": self.sensitivity_level.name,
            "column_classifications": {k: v.name for k, v in self.column_classifications.items()},
            "detected_reasons": [r.value for r in self.detected_reasons],
            "requires_encryption": self.requires_encryption,
            "requires_audit": self.requires_audit,
            "requires_masking": self.requires_masking,
            "timestamp": self.timestamp
        }


class EntityClassificationEngine:
    """Classifies entities by sensitivity."""
    
    def __init__(self):
        """Initialize engine."""
        self.rules: Dict[str, ClassificationRule] = {}
        self.classifications: Dict[str, EntityClassification] = {}
        self._init_default_rules()
    
    def _init_default_rules(self) -> None:
        """Initialize default classification rules."""
        default_rules = [
            ClassificationRule("pii_1", "SSN Pattern", r".*ssn.*", SensitivityLevel.RESTRICTED, ClassificationReason.PII_DETECTED),
            ClassificationRule("pii_2", "Email Pattern", r".*email.*", SensitivityLevel.CONFIDENTIAL, ClassificationReason.PII_DETECTED),
            ClassificationRule("pii_3", "Phone Pattern", r".*phone.*", SensitivityLevel.CONFIDENTIAL, ClassificationReason.PII_DETECTED),
            ClassificationRule("pii_4", "DOB Pattern", r".*date_of_birth.*", SensitivityLevel.RESTRICTED, ClassificationReason.PII_DETECTED),
            ClassificationRule("fin_1", "Credit Card", r".*credit_card.*", SensitivityLevel.RESTRICTED, ClassificationReason.FINANCIAL_DATA),
            ClassificationRule("fin_2", "Bank Account", r".*account.*", SensitivityLevel.CONFIDENTIAL, ClassificationReason.FINANCIAL_DATA),
            ClassificationRule("fin_3", "Salary", r".*salary.*", SensitivityLevel.CONFIDENTIAL, ClassificationReason.FINANCIAL_DATA),
            ClassificationRule("health_1", "Patient ID", r".*patient.*", SensitivityLevel.RESTRICTED, ClassificationReason.HEALTH_DATA),
            ClassificationRule("health_2", "Medical Record", r".*medical.*", SensitivityLevel.RESTRICTED, ClassificationReason.HEALTH_DATA),
        ]
        
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
    
    def add_rule(self, rule: ClassificationRule) -> None:
        """Add classification rule."""
        self.rules[rule.rule_id] = rule
    
    def classify_entity(
        self,
        entity_name: str,
        column_names: List[str]
    ) -> EntityClassification:
        """
        Classify entity based on columns.
        
        Args:
            entity_name: Name of entity
            column_names: List of column names
        
        Returns:
            Entity classification
        """
        classification = EntityClassification(
            entity_name=entity_name,
            sensitivity_level=SensitivityLevel.PUBLIC
        )
        max_sensitivity = SensitivityLevel.PUBLIC
        
        # Check each column against rules
        for column in column_names:
            column_sensitivity = SensitivityLevel.PUBLIC
            
            for rule in self.rules.values():
                # Use regex matching for patterns
                try:
                    if re.search(rule.pattern, column, re.IGNORECASE):
                        column_sensitivity = rule.sensitivity
                        classification.detected_reasons.append(rule.reason)
                        
                        # Track requirements
                        if rule.sensitivity == SensitivityLevel.RESTRICTED:
                            classification.requires_encryption = True
                            classification.requires_audit = True
                            classification.requires_masking = True
                        elif rule.sensitivity == SensitivityLevel.CONFIDENTIAL:
                            classification.requires_encryption = True
                            classification.requires_audit = True
                        
                        max_sensitivity = max(max_sensitivity, column_sensitivity, key=lambda x: x.value)
                        break
                except re.error:
                    # If regex is invalid, fall back to simple substring matching
                    if rule.pattern.lower() in column.lower():
                        column_sensitivity = rule.sensitivity
                        classification.detected_reasons.append(rule.reason)
                        
                        # Track requirements
                        if rule.sensitivity == SensitivityLevel.RESTRICTED:
                            classification.requires_encryption = True
                            classification.requires_audit = True
                            classification.requires_masking = True
                        elif rule.sensitivity == SensitivityLevel.CONFIDENTIAL:
                            classification.requires_encryption = True
                            classification.requires_audit = True
                        
                        max_sensitivity = max(max_sensitivity, column_sensitivity, key=lambda x: x.value)
                        break
            
            classification.column_classifications[column] = column_sensitivity
        
        classification.sensitivity_level = max_sensitivity
        self.classifications[entity_name] = classification
        
        return classification
    
    def get_restricted_entities(self) -> List[EntityClassification]:
        """Get all restricted entities."""
        return [
            c for c in self.classifications.values()
            if c.sensitivity_level == SensitivityLevel.RESTRICTED
        ]
    
    def get_entities_requiring_encryption(self) -> List[EntityClassification]:
        """Get entities requiring encryption."""
        return [
            c for c in self.classifications.values()
            if c.requires_encryption
        ]
    
    def get_entities_requiring_audit(self) -> List[EntityClassification]:
        """Get entities requiring audit trails."""
        return [
            c for c in self.classifications.values()
            if c.requires_audit
        ]
    
    def get_sensitivity_distribution(self) -> Dict[str, int]:
        """Get count of entities by sensitivity."""
        distribution = {
            "public": 0,
            "internal": 0,
            "confidential": 0,
            "restricted": 0
        }
        
        for classification in self.classifications.values():
            level_key = classification.sensitivity_level.name.lower()
            distribution[level_key] += 1
        
        return distribution
    
    def generate_classification_report(self) -> str:
        """Generate classification report."""
        report = "Entity Classification Report\n"
        report += f"Total Entities: {len(self.classifications)}\n\n"
        
        distribution = self.get_sensitivity_distribution()
        report += "Sensitivity Distribution:\n"
        for level, count in sorted(distribution.items(), reverse=True):
            report += f"  {level.upper()}: {count}\n"
        
        restricted = self.get_restricted_entities()
        if restricted:
            report += f"\nRestricted Entities ({len(restricted)}):\n"
            for classification in restricted[:5]:
                report += f"  - {classification.entity_name}\n"
        
        encryption_needed = self.get_entities_requiring_encryption()
        if encryption_needed:
            report += f"\nRequire Encryption ({len(encryption_needed)}):\n"
            for classification in encryption_needed[:5]:
                report += f"  - {classification.entity_name}\n"
        
        return report
    
    def save_classifications(self, file_path: str) -> None:
        """Save classifications to file."""
        classifications_dict = {
            entity_name: classification.to_dict()
            for entity_name, classification in self.classifications.items()
        }
        
        with open(file_path, "w") as f:
            json.dump(classifications_dict, f, indent=2)
