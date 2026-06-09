"""
Data Contract Validator — Validates data SLA/contract definitions.
Ensures contracts have required SLA properties (availability, RTO, RPO, freshness).
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DataContract:
    """Data contract with SLA definitions."""
    entity_name: str
    sla_availability: float          # e.g., 99.9
    rto_hours: int                   # Recovery Time Objective
    rpo_minutes: int                 # Recovery Point Objective
    data_freshness_hours: int        # How fresh must data be
    owner: str
    description: str
    critical: bool = False           # Is this a critical entity


class DataContractValidator:
    """Validates data contracts against requirements."""
    
    # Minimum acceptable SLA values
    MINIMUM_SLA = {
        "critical": {"availability": 99.99, "rto_hours": 1, "rpo_minutes": 5},
        "high": {"availability": 99.9, "rto_hours": 4, "rpo_minutes": 15},
        "medium": {"availability": 99.5, "rto_hours": 8, "rpo_minutes": 60},
        "low": {"availability": 99.0, "rto_hours": 24, "rpo_minutes": 480}
    }
    
    def __init__(self):
        """Initialize validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_contract(self, contract_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a single contract.
        Returns: (is_valid, list_of_errors)
        """
        self.errors = []
        self.warnings = []
        
        # Check required fields
        required = ["entity_name", "sla_availability", "rto_hours", "rpo_minutes", "owner"]
        for field in required:
            if field not in contract_data or contract_data[field] is None:
                self.errors.append(f"Missing required field: {field}")
        
        if self.errors:
            return False, self.errors
        
        # Validate types
        if not isinstance(contract_data.get("sla_availability"), (int, float)):
            self.errors.append(f"sla_availability must be number, got {type(contract_data.get('sla_availability'))}")
        
        if not isinstance(contract_data.get("rto_hours"), int):
            self.errors.append(f"rto_hours must be integer, got {type(contract_data.get('rto_hours'))}")
        
        if not isinstance(contract_data.get("rpo_minutes"), int):
            self.errors.append(f"rpo_minutes must be integer, got {type(contract_data.get('rpo_minutes'))}")
        
        if self.errors:
            return False, self.errors
        
        # Validate value ranges
        availability = contract_data.get("sla_availability")
        if not (99.0 <= availability <= 99.99):
            self.errors.append(f"SLA availability {availability} outside range [99.0, 99.99]")
        
        if contract_data.get("rto_hours", 0) < 0:
            self.errors.append("RTO hours must be non-negative")
        
        if contract_data.get("rpo_minutes", 0) < 0:
            self.errors.append("RPO minutes must be non-negative")
        
        # Data freshness validation (if provided)
        if "data_freshness_hours" in contract_data:
            if not isinstance(contract_data["data_freshness_hours"], int):
                self.errors.append("data_freshness_hours must be integer")
            elif contract_data["data_freshness_hours"] < 0:
                self.errors.append("data_freshness_hours must be non-negative")
        
        return len(self.errors) == 0, self.errors
    
    def validate_contract_batch(self, contracts: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        """
        Validate multiple contracts.
        Returns: (valid_count, list_of_all_errors)
        """
        all_errors = []
        valid_count = 0
        
        for idx, contract in enumerate(contracts):
            is_valid, errors = self.validate_contract(contract)
            if is_valid:
                valid_count += 1
            else:
                entity_name = contract.get("entity_name", f"contract[{idx}]")
                for error in errors:
                    all_errors.append(f"{entity_name}: {error}")
        
        return valid_count, all_errors
    
    def check_sla_alignment(
        self,
        contract: Dict[str, Any],
        risk_level: str
    ) -> Tuple[bool, List[str]]:
        """
        Check if contract meets minimum SLA for risk level.
        Returns: (meets_minimum, list_of_gaps)
        """
        if risk_level not in self.MINIMUM_SLA:
            risk_level = "medium"  # Default
        
        minimum = self.MINIMUM_SLA[risk_level]
        gaps = []
        
        # Check availability
        availability = contract.get("sla_availability", 0)
        if availability < minimum["availability"]:
            gaps.append(
                f"SLA availability {availability}% below minimum {minimum['availability']}% "
                f"for {risk_level} risk"
            )
        
        # Check RTO
        rto = contract.get("rto_hours", float('inf'))
        if rto > minimum["rto_hours"]:
            gaps.append(
                f"RTO {rto}h exceeds maximum {minimum['rto_hours']}h for {risk_level} risk"
            )
        
        # Check RPO
        rpo = contract.get("rpo_minutes", float('inf'))
        if rpo > minimum["rpo_minutes"]:
            gaps.append(
                f"RPO {rpo}m exceeds maximum {minimum['rpo_minutes']}m for {risk_level} risk"
            )
        
        return len(gaps) == 0, gaps
    
    def generate_report(self, contracts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate validation report for contracts."""
        valid_count, errors = self.validate_contract_batch(contracts)
        
        return {
            "total_contracts": len(contracts),
            "valid_contracts": valid_count,
            "invalid_contracts": len(contracts) - valid_count,
            "validity_percentage": (valid_count / len(contracts) * 100) if contracts else 0,
            "errors": errors,
            "contracts_validated": [
                {
                    "entity_name": c.get("entity_name", "unknown"),
                    "sla_availability": c.get("sla_availability"),
                    "rto_hours": c.get("rto_hours"),
                    "rpo_minutes": c.get("rpo_minutes")
                }
                for c in contracts
            ]
        }
    
    def save_report(self, report: Dict[str, Any], output_path: Path) -> None:
        """Save validation report to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)


def validate_contracts_file(input_path: Path) -> Dict[str, Any]:
    """Helper: Load and validate contracts from JSON file."""
    if not input_path.exists():
        return {"error": f"File not found: {input_path}"}
    
    with open(input_path) as f:
        contracts = json.load(f)
    
    validator = DataContractValidator()
    report = validator.generate_report(contracts if isinstance(contracts, list) else [contracts])
    
    return report
