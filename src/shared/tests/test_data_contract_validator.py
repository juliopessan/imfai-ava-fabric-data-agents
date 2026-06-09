"""
Tests for DataContractValidator — Data contract and SLA validation.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.data_contract_validator import (
    DataContract, DataContractValidator, validate_contracts_file
)


class TestDataContractValidator:
    """Test suite for DataContractValidator."""
    
    def test_validate_contract_valid(self):
        """Test validating a valid contract."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 99.9,
            "rto_hours": 4,
            "rpo_minutes": 15,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_contract_missing_required_field(self):
        """Test validation fails on missing required field."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 99.9,
            "rto_hours": 4,
            # Missing rpo_minutes
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is False
        assert any("rpo_minutes" in e for e in errors)
    
    def test_validate_contract_invalid_type(self):
        """Test validation fails on invalid field type."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": "99.9",  # Should be number
            "rto_hours": 4,
            "rpo_minutes": 15,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is False
    
    def test_validate_contract_availability_out_of_range(self):
        """Test validation fails on availability outside range."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 98.5,  # Below minimum 99.0
            "rto_hours": 4,
            "rpo_minutes": 15,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is False
        assert any("availability" in e.lower() for e in errors)
    
    def test_validate_contract_availability_too_high(self):
        """Test validation fails on unrealistic availability."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 99.999,  # Above maximum 99.99
            "rto_hours": 4,
            "rpo_minutes": 15,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is False
    
    def test_validate_contract_negative_rto(self):
        """Test validation fails on negative RTO."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 99.9,
            "rto_hours": -1,
            "rpo_minutes": 15,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is False
    
    def test_validate_contract_with_freshness(self):
        """Test validation with data freshness."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "customers",
            "sla_availability": 99.9,
            "rto_hours": 4,
            "rpo_minutes": 15,
            "data_freshness_hours": 24,
            "owner": "team@company.com"
        }
        
        is_valid, errors = validator.validate_contract(contract)
        assert is_valid is True
    
    def test_validate_contract_batch_all_valid(self):
        """Test batch validation with all valid contracts."""
        validator = DataContractValidator()
        contracts = [
            {
                "entity_name": f"entity_{i}",
                "sla_availability": 99.9,
                "rto_hours": 4,
                "rpo_minutes": 15,
                "owner": "team@company.com"
            }
            for i in range(3)
        ]
        
        valid_count, errors = validator.validate_contract_batch(contracts)
        assert valid_count == 3
        assert len(errors) == 0
    
    def test_validate_contract_batch_mixed(self):
        """Test batch validation with mixed valid/invalid."""
        validator = DataContractValidator()
        contracts = [
            {
                "entity_name": "valid",
                "sla_availability": 99.9,
                "rto_hours": 4,
                "rpo_minutes": 15,
                "owner": "team@company.com"
            },
            {
                "entity_name": "invalid",
                "sla_availability": 98.0,  # Invalid
                "rto_hours": 4,
                "rpo_minutes": 15,
                "owner": "team@company.com"
            }
        ]
        
        valid_count, errors = validator.validate_contract_batch(contracts)
        assert valid_count == 1
        assert len(errors) > 0
        assert any("invalid" in e for e in errors)
    
    def test_check_sla_alignment_critical_meets(self):
        """Test SLA alignment check for critical risk meeting requirements."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "payments",
            "sla_availability": 99.99,
            "rto_hours": 1,
            "rpo_minutes": 5
        }
        
        meets, gaps = validator.check_sla_alignment(contract, "critical")
        assert meets is True
        assert len(gaps) == 0
    
    def test_check_sla_alignment_critical_fails(self):
        """Test SLA alignment check for critical risk failing."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "payments",
            "sla_availability": 99.9,  # Below critical minimum
            "rto_hours": 4,            # Above critical maximum
            "rpo_minutes": 15          # Above critical maximum
        }
        
        meets, gaps = validator.check_sla_alignment(contract, "critical")
        assert meets is False
        assert len(gaps) > 0
    
    def test_check_sla_alignment_high_risk(self):
        """Test SLA alignment for high risk."""
        validator = DataContractValidator()
        contract = {
            "entity_name": "orders",
            "sla_availability": 99.9,
            "rto_hours": 4,
            "rpo_minutes": 15
        }
        
        meets, gaps = validator.check_sla_alignment(contract, "high")
        assert meets is True
    
    def test_generate_report(self):
        """Test report generation."""
        validator = DataContractValidator()
        contracts = [
            {
                "entity_name": "customers",
                "sla_availability": 99.9,
                "rto_hours": 4,
                "rpo_minutes": 15,
                "owner": "team@company.com"
            }
        ]
        
        report = validator.generate_report(contracts)
        assert report["total_contracts"] == 1
        assert report["valid_contracts"] == 1
        assert report["invalid_contracts"] == 0
        assert report["validity_percentage"] == 100.0
    
    def test_save_report(self):
        """Test report persistence."""
        validator = DataContractValidator()
        contracts = [
            {
                "entity_name": "customers",
                "sla_availability": 99.9,
                "rto_hours": 4,
                "rpo_minutes": 15,
                "owner": "team@company.com"
            }
        ]
        
        report = validator.generate_report(contracts)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.json"
            validator.save_report(report, output_path)
            
            assert output_path.exists()
            with open(output_path) as f:
                saved = json.load(f)
            
            assert saved["total_contracts"] == 1
            assert saved["valid_contracts"] == 1


class TestValidateContractsFileHelper:
    """Test suite for validate_contracts_file helper."""
    
    def test_validate_contracts_file_valid(self):
        """Test loading and validating contracts file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "contracts.json"
            
            contracts = [
                {
                    "entity_name": "customers",
                    "sla_availability": 99.9,
                    "rto_hours": 4,
                    "rpo_minutes": 15,
                    "owner": "team@company.com"
                }
            ]
            
            with open(filepath, 'w') as f:
                json.dump(contracts, f)
            
            report = validate_contracts_file(filepath)
            assert report["valid_contracts"] == 1
            assert "error" not in report
    
    def test_validate_contracts_file_not_found(self):
        """Test error on file not found."""
        report = validate_contracts_file(Path("nonexistent.json"))
        assert "error" in report
        assert "not found" in report["error"]


class TestDataContractDataclass:
    """Test suite for DataContract dataclass."""
    
    def test_data_contract_creation(self):
        """Test creating a DataContract."""
        contract = DataContract(
            entity_name="customers",
            sla_availability=99.9,
            rto_hours=4,
            rpo_minutes=15,
            data_freshness_hours=24,
            owner="team@company.com",
            description="Customer master data",
            critical=False
        )
        
        assert contract.entity_name == "customers"
        assert contract.sla_availability == 99.9
        assert contract.critical is False
