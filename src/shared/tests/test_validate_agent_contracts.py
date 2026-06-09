"""
Tests for AgentContractValidator — DMF agent contract validation.
"""

import pytest
from src.shared.scripts.validate_agent_contracts import (
    AgentContractValidator, AgentContract, AgentCapability, AgentCapabilityType, ContractStatus
)


class TestAgentContractValidator:
    """Test suite for AgentContractValidator."""
    
    def test_initialization(self):
        """Test validator initialization."""
        validator = AgentContractValidator()
        assert len(validator.contracts) == 0
        assert len(validator.validation_results) == 0
    
    def test_register_contract(self):
        """Test registering contract."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[capability]
        )
        
        validator.register_contract(contract)
        assert "agent-001" in validator.contracts
    
    def test_validate_capability_valid(self):
        """Test validating complete capability."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry",
            sla_availability=0.99
        )
        
        valid, violations = validator.validate_capability(capability)
        assert valid is True
        assert len(violations) == 0
    
    def test_validate_capability_missing_name(self):
        """Test capability validation fails without name."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        valid, violations = validator.validate_capability(capability)
        assert valid is False
        assert any("name" in v.lower() for v in violations)
    
    def test_validate_capability_missing_inputs(self):
        """Test capability validation fails without inputs."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=[],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        valid, violations = validator.validate_capability(capability)
        assert valid is False
        assert any("input" in v.lower() for v in violations)
    
    def test_validate_capability_invalid_sla(self):
        """Test capability validation fails with invalid SLA."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry",
            sla_availability=0.5  # Too low
        )
        
        valid, violations = validator.validate_capability(capability)
        assert valid is False
        assert any("SLA" in v for v in violations)
    
    def test_validate_contract_valid(self):
        """Test validating complete contract."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[capability],
            max_retries=3,
            timeout_seconds=3600
        )
        
        result = validator.validate_contract(contract)
        assert result.is_valid is True
        assert result.status == ContractStatus.VALID
    
    def test_validate_contract_missing_fields(self):
        """Test contract validation detects missing fields."""
        validator = AgentContractValidator()
        
        contract = AgentContract(
            agent_id="",  # Missing
            agent_name="Validator",
            version="1.0",
            capabilities=[]
        )
        
        result = validator.validate_contract(contract)
        assert result.is_valid is False
        assert ContractStatus.INVALID == result.status
    
    def test_validate_contract_no_capabilities(self):
        """Test contract validation fails without capabilities."""
        validator = AgentContractValidator()
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[]
        )
        
        result = validator.validate_contract(contract)
        assert result.is_valid is False
        assert any("capability" in v.lower() for v in result.violations)
    
    def test_validate_contract_with_warnings(self):
        """Test contract with warnings."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[capability],
            timeout_seconds=86400 * 2  # Too long
        )
        
        result = validator.validate_contract(contract)
        assert result.is_valid is True
        assert result.status == ContractStatus.WARNING
        assert len(result.warnings) > 0
    
    def test_validate_all_contracts(self):
        """Test validating multiple contracts."""
        validator = AgentContractValidator()
        
        for i in range(3):
            capability = AgentCapability(
                name="process",
                capability_type=AgentCapabilityType.TRANSFORMATION,
                input_requirements=["data"],
                output_guarantees=["result"],
                error_handling="log"
            )
            
            contract = AgentContract(
                agent_id=f"agent-{i:03d}",
                agent_name=f"Agent {i}",
                version="1.0",
                capabilities=[capability]
            )
            
            validator.register_contract(contract)
        
        results = validator.validate_all_contracts()
        assert len(results) == 3
        assert all(r.is_valid for r in results.values())
    
    def test_get_invalid_contracts(self):
        """Test filtering invalid contracts."""
        validator = AgentContractValidator()
        
        # Valid contract
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        contract1 = AgentContract(
            agent_id="agent-001",
            agent_name="Valid",
            version="1.0",
            capabilities=[capability]
        )
        
        # Invalid contract
        contract2 = AgentContract(
            agent_id="agent-002",
            agent_name="Invalid",
            version="1.0",
            capabilities=[]
        )
        
        validator.register_contract(contract1)
        validator.register_contract(contract2)
        validator.validate_all_contracts()
        
        invalid = validator.get_invalid_contracts()
        assert len(invalid) == 1
        assert "agent-002" in invalid
    
    def test_check_capability_availability(self):
        """Test checking if agent has capability."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[capability]
        )
        
        validator.register_contract(contract)
        
        assert validator.check_capability_availability("agent-001", AgentCapabilityType.VALIDATION)
        assert not validator.check_capability_availability("agent-001", AgentCapabilityType.LOADING)
    
    def test_get_dependent_agents(self):
        """Test finding dependent agents."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="process",
            capability_type=AgentCapabilityType.TRANSFORMATION,
            input_requirements=["data"],
            output_guarantees=["result"],
            error_handling="log"
        )
        
        contract1 = AgentContract(
            agent_id="agent-001",
            agent_name="Provider",
            version="1.0",
            capabilities=[capability]
        )
        
        contract2 = AgentContract(
            agent_id="agent-002",
            agent_name="Dependent",
            version="1.0",
            capabilities=[capability],
            dependencies=["agent-001"]
        )
        
        validator.register_contract(contract1)
        validator.register_contract(contract2)
        
        dependents = validator.get_dependent_agents("agent-001")
        assert "agent-002" in dependents
    
    def test_check_dependency_chain_no_cycles(self):
        """Test dependency chain with no cycles."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="process",
            capability_type=AgentCapabilityType.TRANSFORMATION,
            input_requirements=["data"],
            output_guarantees=["result"],
            error_handling="log"
        )
        
        contract1 = AgentContract(
            agent_id="agent-001",
            agent_name="A",
            version="1.0",
            capabilities=[capability]
        )
        
        contract2 = AgentContract(
            agent_id="agent-002",
            agent_name="B",
            version="1.0",
            capabilities=[capability],
            dependencies=["agent-001"]
        )
        
        validator.register_contract(contract1)
        validator.register_contract(contract2)
        
        valid, path = validator.check_dependency_chain("agent-002")
        assert valid is True
    
    def test_generate_validation_report(self):
        """Test report generation."""
        validator = AgentContractValidator()
        
        capability = AgentCapability(
            name="validate",
            capability_type=AgentCapabilityType.VALIDATION,
            input_requirements=["artifact"],
            output_guarantees=["score"],
            error_handling="retry"
        )
        
        contract = AgentContract(
            agent_id="agent-001",
            agent_name="Validator",
            version="1.0",
            capabilities=[capability]
        )
        
        validator.register_contract(contract)
        validator.validate_all_contracts()
        
        report = validator.generate_validation_report()
        assert "Agent Contract Validation Report" in report
        assert "Total Contracts: 1" in report
        assert "Valid: 1" in report
