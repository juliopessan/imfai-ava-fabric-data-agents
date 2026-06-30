#!/usr/bin/env python3
"""
Specification Repository — Persistent storage for reusable data governance specs.

Stores data contracts, schemas, SLAs, and governance rules as versioned,
referenceable code artifacts. Enables spec-as-code and pattern reuse.

Usage:
  repo = SpecRepository()
  
  # Define and store a contract
  contract = DataContract(
      table_name="customers",
      sla_availability_pct=99.5,
      sla_rto_minutes=30,
      owner="data-platform",
      retention_days=2555  # 7 years
  )
  repo.save_contract(contract, version=1)
  
  # Later, reference it:
  spec = repo.get_contract("customers", version=1)
  # → Use for validation, documentation, compliance
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timezone
import json
from pathlib import Path


class SeverityLevel(str, Enum):
    """Severity for governance rules."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


@dataclass
class DataContract:
    """Reusable data contract specification."""
    table_name: str
    description: str = ""
    owner: str = ""
    domain: str = ""
    
    # SLA specifications
    sla_availability_pct: float = 99.5  # 99.5%
    sla_rto_minutes: int = 60           # 1 hour
    sla_rpo_minutes: int = 15           # 15 min recovery point
    
    # Data governance
    retention_days: int = 365
    pii_columns: List[str] = field(default_factory=list)
    requires_encryption: bool = False
    audit_required: bool = False
    
    # Version
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = ""
    
    def to_dict(self) -> Dict:
        """Export to dictionary."""
        return asdict(self)


@dataclass
class GovernanceRule:
    """Reusable governance/quality rule."""
    rule_id: str
    rule_name: str
    description: str
    severity: SeverityLevel
    
    # Rule logic
    validation_logic: str  # SQL or Python expression
    remediation: str      # How to fix if violated
    
    applicable_to: List[str] = field(default_factory=list)  # Entity types
    
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = ""


@dataclass
class SchemaBlueprint:
    """Reusable schema template."""
    blueprint_id: str
    schema_name: str
    description: str
    
    # Column definitions
    columns: List[Dict[str, Any]] = field(default_factory=list)
    # [{"name": "id", "type": "BIGINT", "nullable": False, "description": "..."}]
    
    # Index definitions
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    # [{"name": "idx_customer", "columns": ["customer_id"], "unique": True}]
    
    # Constraints
    constraints: List[Dict[str, Any]] = field(default_factory=list)
    
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    created_by: str = ""


class SpecRepository:
    """Manages specification storage and retrieval."""
    
    def __init__(self, repo_dir: str = "spec_repository"):
        """Initialize repository."""
        self.repo_dir = Path(repo_dir)
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize subdirectories
        (self.repo_dir / "contracts").mkdir(exist_ok=True)
        (self.repo_dir / "rules").mkdir(exist_ok=True)
        (self.repo_dir / "schemas").mkdir(exist_ok=True)
        (self.repo_dir / "index.json").touch(exist_ok=True)
        
        self._index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load specification index."""
        index_path = self.repo_dir / "index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {"contracts": {}, "rules": {}, "schemas": {}}
        return {"contracts": {}, "rules": {}, "schemas": {}}
    
    def _save_index(self):
        """Save specification index."""
        index_path = self.repo_dir / "index.json"
        with open(index_path, 'w') as f:
            json.dump(self._index, f, indent=2)
    
    def save_contract(self, contract: DataContract) -> str:
        """Save data contract."""
        contract_id = f"{contract.table_name}_v{contract.version}"
        contract_path = self.repo_dir / "contracts" / f"{contract_id}.json"
        
        with open(contract_path, 'w') as f:
            json.dump(contract.to_dict(), f, indent=2)
        
        # Index it
        if contract.table_name not in self._index["contracts"]:
            self._index["contracts"][contract.table_name] = []
        
        self._index["contracts"][contract.table_name].append({
            "version": contract.version,
            "path": str(contract_path),
            "created_at": contract.created_at,
            "created_by": contract.created_by
        })
        self._save_index()
        
        return contract_id
    
    def get_contract(
        self,
        table_name: str,
        version: Optional[int] = None
    ) -> Optional[DataContract]:
        """Retrieve data contract."""
        if table_name not in self._index["contracts"]:
            return None
        
        versions = self._index["contracts"][table_name]
        if not versions:
            return None
        
        # Get specific version or latest
        target = versions[-1] if version is None else next(
            (v for v in versions if v["version"] == version), None
        )
        
        if not target:
            return None
        
        with open(target["path"], 'r') as f:
            data = json.load(f)
            return DataContract(**data)
    
    def save_rule(self, rule: GovernanceRule) -> str:
        """Save governance rule."""
        rule_id = f"{rule.rule_id}_v{rule.version}"
        rule_path = self.repo_dir / "rules" / f"{rule_id}.json"
        
        with open(rule_path, 'w') as f:
            json.dump(asdict(rule), f, indent=2)
        
        # Index it
        if rule.rule_id not in self._index["rules"]:
            self._index["rules"][rule.rule_id] = []
        
        self._index["rules"][rule.rule_id].append({
            "version": rule.version,
            "path": str(rule_path),
            "created_at": rule.created_at,
            "severity": rule.severity
        })
        self._save_index()
        
        return rule_id
    
    def get_rules_by_severity(
        self,
        severity: SeverityLevel
    ) -> List[GovernanceRule]:
        """Get all rules of given severity."""
        rules = []
        for rule_list in self._index["rules"].values():
            for rule_ref in rule_list:
                with open(rule_ref["path"], 'r') as f:
                    data = json.load(f)
                    if data["severity"] == severity:
                        rules.append(GovernanceRule(**data))
        return rules
    
    def save_schema_blueprint(self, blueprint: SchemaBlueprint) -> str:
        """Save schema blueprint."""
        schema_id = f"{blueprint.blueprint_id}_v{blueprint.version}"
        schema_path = self.repo_dir / "schemas" / f"{schema_id}.json"
        
        with open(schema_path, 'w') as f:
            json.dump(asdict(blueprint), f, indent=2)
        
        # Index it
        if blueprint.blueprint_id not in self._index["schemas"]:
            self._index["schemas"][blueprint.blueprint_id] = []
        
        self._index["schemas"][blueprint.blueprint_id].append({
            "version": blueprint.version,
            "path": str(schema_path),
            "created_at": blueprint.created_at
        })
        self._save_index()
        
        return schema_id
    
    def get_schema_blueprint(
        self,
        blueprint_id: str,
        version: Optional[int] = None
    ) -> Optional[SchemaBlueprint]:
        """Retrieve schema blueprint."""
        if blueprint_id not in self._index["schemas"]:
            return None
        
        versions = self._index["schemas"][blueprint_id]
        if not versions:
            return None
        
        target = versions[-1] if version is None else next(
            (v for v in versions if v["version"] == version), None
        )
        
        if not target:
            return None
        
        with open(target["path"], 'r') as f:
            data = json.load(f)
            return SchemaBlueprint(**data)
    
    def get_statistics(self) -> Dict:
        """Get repository statistics."""
        contract_count = sum(len(v) for v in self._index["contracts"].values())
        rule_count = sum(len(v) for v in self._index["rules"].values())
        schema_count = sum(len(v) for v in self._index["schemas"].values())
        
        return {
            "total_contracts": contract_count,
            "total_rules": rule_count,
            "total_schemas": schema_count,
            "unique_contracts": len(self._index["contracts"]),
            "unique_rules": len(self._index["rules"]),
            "unique_schemas": len(self._index["schemas"])
        }
    
    def export_index(self) -> Dict:
        """Export full specification index."""
        return self._index
