"""
Quality Thresholds — Entity-tier quality rules and SLA definitions.
Defines acceptable quality ranges for entities based on risk level (critical, high, medium, low).
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Entity risk level classification."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class QualityThreshold:
    """Quality threshold for an entity."""
    entity_name: str
    risk_level: RiskLevel
    min_completude: float  # 0.0-1.0
    min_quality: float      # 0.0-1.0
    max_error_count: int
    sla_availability: float  # 99.9, 99.99, etc.
    sla_rto_hours: int       # Recovery Time Objective
    sla_rpo_minutes: int     # Recovery Point Objective


class QualityThresholdRegistry:
    """Registry of quality thresholds for entities."""
    
    # Default thresholds by risk level
    DEFAULT_THRESHOLDS = {
        RiskLevel.CRITICAL: {
            "min_completude": 1.0,      # Must be 100% complete
            "min_quality": 0.98,         # Very high quality
            "max_error_count": 0,        # Zero errors tolerated
            "sla_availability": 99.99,   # Four nines
            "sla_rto_hours": 1,
            "sla_rpo_minutes": 5
        },
        RiskLevel.HIGH: {
            "min_completude": 0.95,      # 95% complete
            "min_quality": 0.95,
            "max_error_count": 1,
            "sla_availability": 99.9,    # Three nines
            "sla_rto_hours": 4,
            "sla_rpo_minutes": 15
        },
        RiskLevel.MEDIUM: {
            "min_completude": 0.90,      # 90% complete
            "min_quality": 0.90,
            "max_error_count": 2,
            "sla_availability": 99.5,    # 99.5%
            "sla_rto_hours": 8,
            "sla_rpo_minutes": 60
        },
        RiskLevel.LOW: {
            "min_completude": 0.85,      # 85% complete
            "min_quality": 0.80,
            "max_error_count": 5,
            "sla_availability": 99.0,    # 99%
            "sla_rto_hours": 24,
            "sla_rpo_minutes": 480      # 8 hours
        }
    }
    
    def __init__(self):
        """Initialize registry."""
        self.thresholds: Dict[str, QualityThreshold] = {}
    
    def register_entity(
        self,
        entity_name: str,
        risk_level: RiskLevel,
        custom_thresholds: Optional[Dict[str, Any]] = None
    ) -> QualityThreshold:
        """Register an entity with quality thresholds."""
        defaults = self.DEFAULT_THRESHOLDS[risk_level].copy()
        
        # Override with custom thresholds if provided
        if custom_thresholds:
            defaults.update(custom_thresholds)
        
        threshold = QualityThreshold(
            entity_name=entity_name,
            risk_level=risk_level,
            **defaults
        )
        
        self.thresholds[entity_name] = threshold
        return threshold
    
    def get_threshold(self, entity_name: str) -> Optional[QualityThreshold]:
        """Get threshold for an entity."""
        return self.thresholds.get(entity_name)
    
    def validate_entity_quality(
        self,
        entity_name: str,
        completude: float,
        quality: float,
        error_count: int
    ) -> tuple[bool, List[str]]:
        """
        Validate entity quality against thresholds.
        Returns: (is_valid, list_of_violations)
        """
        threshold = self.get_threshold(entity_name)
        if not threshold:
            return False, [f"Entity '{entity_name}' not registered in quality registry"]
        
        violations = []
        
        if completude < threshold.min_completude:
            violations.append(
                f"Completude {completude:.1%} below threshold {threshold.min_completude:.1%} "
                f"(risk: {threshold.risk_level.value})"
            )
        
        if quality < threshold.min_quality:
            violations.append(
                f"Quality {quality:.2f} below threshold {threshold.min_quality:.2f} "
                f"(risk: {threshold.risk_level.value})"
            )
        
        if error_count > threshold.max_error_count:
            violations.append(
                f"Error count {error_count} exceeds maximum {threshold.max_error_count} "
                f"(risk: {threshold.risk_level.value})"
            )
        
        return len(violations) == 0, violations
    
    def get_sla_report(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """Get SLA details for an entity."""
        threshold = self.get_threshold(entity_name)
        if not threshold:
            return None
        
        return {
            "entity_name": entity_name,
            "risk_level": threshold.risk_level.value,
            "sla_availability_percentage": threshold.sla_availability,
            "rto_hours": threshold.sla_rto_hours,
            "rpo_minutes": threshold.sla_rpo_minutes,
            "min_completude": threshold.min_completude,
            "min_quality": threshold.min_quality,
            "max_errors": threshold.max_error_count
        }
    
    def save_to_file(self, output_path: Path) -> None:
        """Save registry to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "thresholds": {
                name: {
                    "entity_name": t.entity_name,
                    "risk_level": t.risk_level.value,
                    "min_completude": t.min_completude,
                    "min_quality": t.min_quality,
                    "max_error_count": t.max_error_count,
                    "sla_availability": t.sla_availability,
                    "sla_rto_hours": t.sla_rto_hours,
                    "sla_rpo_minutes": t.sla_rpo_minutes
                }
                for name, t in self.thresholds.items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, input_path: Path) -> "QualityThresholdRegistry":
        """Load registry from JSON file."""
        registry = cls()
        
        with open(input_path) as f:
            data = json.load(f)
        
        for entity_name, threshold_data in data.get("thresholds", {}).items():
            risk_level = RiskLevel(threshold_data["risk_level"])
            custom = {k: v for k, v in threshold_data.items() 
                     if k not in ["entity_name", "risk_level"]}
            registry.register_entity(entity_name, risk_level, custom)
        
        return registry


def create_default_registry(entities: List[str], risk_mapping: Dict[str, str]) -> QualityThresholdRegistry:
    """Helper: Create registry with default thresholds for entities."""
    registry = QualityThresholdRegistry()
    
    for entity in entities:
        risk = RiskLevel(risk_mapping.get(entity, "medium"))
        registry.register_entity(entity, risk)
    
    return registry
