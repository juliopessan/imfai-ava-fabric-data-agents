"""
Agent Contract Validator — Validates DMF agent capability declarations.
Ensures agents declare capabilities they can fulfill and handle errors appropriately.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import json


class AgentCapabilityType(Enum):
    """Types of agent capabilities."""
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    LOADING = "loading"
    ORCHESTRATION = "orchestration"
    REPORTING = "reporting"
    QUALITY_CHECK = "quality_check"


class ContractStatus(Enum):
    """Status of contract validation."""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    UNKNOWN = "unknown"


@dataclass
class AgentCapability:
    """Declaration of agent capability."""
    name: str
    capability_type: AgentCapabilityType
    input_requirements: List[str] = field(default_factory=list)
    output_guarantees: List[str] = field(default_factory=list)
    error_handling: str = ""
    supports_rollback: bool = False
    sla_availability: float = 0.99
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "capability_type": self.capability_type.value,
            "input_requirements": self.input_requirements,
            "output_guarantees": self.output_guarantees,
            "error_handling": self.error_handling,
            "supports_rollback": self.supports_rollback,
            "sla_availability": self.sla_availability
        }


@dataclass
class AgentContract:
    """Agent contract definition."""
    agent_id: str
    agent_name: str
    version: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    max_retries: int = 3
    timeout_seconds: int = 3600
    requires_approval: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.version,
            "capabilities": [c.to_dict() for c in self.capabilities],
            "dependencies": self.dependencies,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "requires_approval": self.requires_approval,
            "timestamp": self.timestamp
        }


@dataclass
class ContractValidationResult:
    """Result of contract validation."""
    agent_id: str
    status: ContractStatus
    is_valid: bool
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "is_valid": self.is_valid,
            "violations": self.violations,
            "warnings": self.warnings,
            "missing_fields": self.missing_fields,
            "timestamp": self.timestamp
        }


class AgentContractValidator:
    """Validates DMF agent contracts."""
    
    def __init__(self):
        """Initialize validator."""
        self.contracts: Dict[str, AgentContract] = {}
        self.validation_results: Dict[str, ContractValidationResult] = {}
    
    def register_contract(self, contract: AgentContract) -> None:
        """Register agent contract."""
        self.contracts[contract.agent_id] = contract
    
    def validate_capability(
        self,
        capability: AgentCapability
    ) -> Tuple[bool, List[str]]:
        """
        Validate single capability declaration.
        
        Returns:
            (is_valid, list of violations)
        """
        violations = []
        
        if not capability.name:
            violations.append("Capability must have a name")
        
        if not capability.input_requirements:
            violations.append(f"Capability '{capability.name}' must declare input requirements")
        
        if not capability.output_guarantees:
            violations.append(f"Capability '{capability.name}' must declare output guarantees")
        
        if not capability.error_handling:
            violations.append(f"Capability '{capability.name}' must declare error handling strategy")
        
        if capability.sla_availability < 0.9 or capability.sla_availability > 1.0:
            violations.append(f"Capability '{capability.name}' has invalid SLA availability {capability.sla_availability}")
        
        return len(violations) == 0, violations
    
    def validate_contract(
        self,
        contract: AgentContract
    ) -> ContractValidationResult:
        """
        Validate complete agent contract.
        
        Args:
            contract: Agent contract to validate
        
        Returns:
            Validation result
        """
        result = ContractValidationResult(
            agent_id=contract.agent_id,
            status=ContractStatus.UNKNOWN,
            is_valid=True
        )
        
        # Check required fields
        if not contract.agent_id:
            result.missing_fields.append("agent_id")
        
        if not contract.agent_name:
            result.missing_fields.append("agent_name")
        
        if not contract.version:
            result.missing_fields.append("version")
        
        if result.missing_fields:
            result.violations.append(f"Missing required fields: {', '.join(result.missing_fields)}")
            result.is_valid = False
        
        # Check capabilities
        if not contract.capabilities:
            result.violations.append("Agent must declare at least one capability")
            result.is_valid = False
        
        for capability in contract.capabilities:
            valid, violations = self.validate_capability(capability)
            if not valid:
                result.violations.extend(violations)
                result.is_valid = False
        
        # Check configuration
        if contract.max_retries < 0 or contract.max_retries > 10:
            result.warnings.append(f"max_retries {contract.max_retries} is unusual (recommend 1-5)")
        
        if contract.timeout_seconds < 60:
            result.warnings.append(f"timeout_seconds {contract.timeout_seconds} is very short")
        
        if contract.timeout_seconds > 86400:  # 24 hours
            result.warnings.append(f"timeout_seconds {contract.timeout_seconds} is very long")
        
        # Determine status
        if not result.is_valid:
            result.status = ContractStatus.INVALID
        elif result.warnings:
            result.status = ContractStatus.WARNING
        else:
            result.status = ContractStatus.VALID
        
        self.validation_results[contract.agent_id] = result
        return result
    
    def validate_all_contracts(self) -> Dict[str, ContractValidationResult]:
        """Validate all registered contracts."""
        results = {}
        for agent_id, contract in self.contracts.items():
            results[agent_id] = self.validate_contract(contract)
        
        return results
    
    def get_invalid_contracts(self) -> List[str]:
        """Get list of agent IDs with invalid contracts."""
        return [
            agent_id for agent_id, result in self.validation_results.items()
            if not result.is_valid
        ]
    
    def get_contracts_with_warnings(self) -> List[str]:
        """Get list of agent IDs with warnings."""
        return [
            agent_id for agent_id, result in self.validation_results.items()
            if result.status == ContractStatus.WARNING
        ]
    
    def check_capability_availability(
        self,
        agent_id: str,
        capability_type: AgentCapabilityType
    ) -> bool:
        """Check if agent has capability."""
        if agent_id not in self.contracts:
            return False
        
        contract = self.contracts[agent_id]
        return any(c.capability_type == capability_type for c in contract.capabilities)
    
    def get_dependent_agents(
        self,
        agent_id: str
    ) -> List[str]:
        """Get agents that depend on given agent."""
        dependents = []
        for other_id, contract in self.contracts.items():
            if agent_id in contract.dependencies:
                dependents.append(other_id)
        
        return dependents
    
    def check_dependency_chain(
        self,
        agent_id: str,
        visited: Optional[Set[str]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Check for circular dependencies.
        
        Returns:
            (no_cycles, cycle_path)
        """
        if visited is None:
            visited = set()
        
        if agent_id in visited:
            return False, [agent_id]  # Cycle detected
        
        if agent_id not in self.contracts:
            return True, []  # Valid - external dependency
        
        visited.add(agent_id)
        contract = self.contracts[agent_id]
        
        for dep in contract.dependencies:
            valid, path = self.check_dependency_chain(dep, visited.copy())
            if not valid:
                return False, path + [agent_id]
        
        return True, []
    
    def generate_validation_report(self) -> str:
        """Generate validation report."""
        report = "Agent Contract Validation Report\n"
        report += f"Total Contracts: {len(self.contracts)}\n"
        
        valid_count = sum(1 for r in self.validation_results.values() if r.status == ContractStatus.VALID)
        warning_count = sum(1 for r in self.validation_results.values() if r.status == ContractStatus.WARNING)
        invalid_count = sum(1 for r in self.validation_results.values() if r.status == ContractStatus.INVALID)
        
        report += f"Valid: {valid_count}\n"
        report += f"Warnings: {warning_count}\n"
        report += f"Invalid: {invalid_count}\n\n"
        
        if self.get_invalid_contracts():
            report += "Invalid Contracts:\n"
            for agent_id in self.get_invalid_contracts():
                result = self.validation_results[agent_id]
                report += f"  {agent_id}:\n"
                for violation in result.violations:
                    report += f"    - {violation}\n"
        
        return report
    
    def save_contracts(self, file_path: str) -> None:
        """Save contracts to file."""
        contracts_dict = {
            agent_id: contract.to_dict()
            for agent_id, contract in self.contracts.items()
        }
        
        with open(file_path, "w") as f:
            json.dump(contracts_dict, f, indent=2)
    
    def save_validation_results(self, file_path: str) -> None:
        """Save validation results to file."""
        results_dict = {
            agent_id: result.to_dict()
            for agent_id, result in self.validation_results.items()
        }
        
        with open(file_path, "w") as f:
            json.dump(results_dict, f, indent=2)
