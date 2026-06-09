"""
Schema Tracker — Tracks schema changes and drift across gate transitions.
Monitors table/column additions, removals, type changes, and validates consistency.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class ChangeType(Enum):
    """Type of schema change."""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    RENAMED = "renamed"


@dataclass
class ColumnChange:
    """A column-level schema change."""
    change_type: ChangeType
    column_name: str
    previous_type: Optional[str] = None
    new_type: Optional[str] = None
    nullable_changed: bool = False
    previous_nullable: Optional[bool] = None
    new_nullable: Optional[bool] = None


@dataclass
class TableChange:
    """A table-level schema change."""
    table_name: str
    change_type: ChangeType
    column_changes: List[ColumnChange]
    breaking: bool = False  # Breaking change requires migration


class SchemaTracker:
    """Tracks and validates schema changes across gates."""
    
    def __init__(self):
        """Initialize tracker."""
        self.schemas: Dict[str, Dict[str, Any]] = {}  # gate -> schema
        self.changes: Dict[str, List[TableChange]] = {}  # gate_pair -> changes
        self.breaking_changes: List[TableChange] = []
    
    def register_schema(self, gate_name: str, schema: Dict[str, Any]) -> None:
        """Register schema for a gate."""
        self.schemas[gate_name] = schema
    
    def get_schema(self, gate_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for a gate."""
        return self.schemas.get(gate_name)
    
    def compare_schemas(
        self,
        from_gate: str,
        to_gate: str
    ) -> Tuple[bool, List[TableChange]]:
        """
        Compare schemas between two gates.
        Returns: (no_breaking_changes, list_of_changes)
        """
        schema_from = self.schemas.get(from_gate)
        schema_to = self.schemas.get(to_gate)
        
        if not schema_from or not schema_to:
            return False, []
        
        changes = self._compute_changes(schema_from, schema_to)
        self.changes[f"{from_gate}->{to_gate}"] = changes
        
        # Check for breaking changes
        breaking = [c for c in changes if c.breaking]
        self.breaking_changes.extend(breaking)
        
        return len(breaking) == 0, changes
    
    def _compute_changes(
        self,
        schema_from: Dict[str, Any],
        schema_to: Dict[str, Any]
    ) -> List[TableChange]:
        """Compute schema changes between two schemas."""
        changes = []
        
        tables_from = schema_from.get("tables", {})
        tables_to = schema_to.get("tables", {})
        
        # Detect table additions
        for table_name in tables_to:
            if table_name not in tables_from:
                changes.append(TableChange(
                    table_name=table_name,
                    change_type=ChangeType.ADDED,
                    column_changes=[]
                ))
        
        # Detect table removals (breaking)
        for table_name in tables_from:
            if table_name not in tables_to:
                changes.append(TableChange(
                    table_name=table_name,
                    change_type=ChangeType.REMOVED,
                    column_changes=[],
                    breaking=True
                ))
        
        # Detect column-level changes
        for table_name in tables_from:
            if table_name in tables_to:
                cols_from = tables_from[table_name].get("columns", {})
                cols_to = tables_to[table_name].get("columns", {})
                
                col_changes = self._compute_column_changes(cols_from, cols_to)
                
                if col_changes:
                    # Check if breaking (e.g., column removed)
                    breaking = any(c.change_type == ChangeType.REMOVED for c in col_changes)
                    changes.append(TableChange(
                        table_name=table_name,
                        change_type=ChangeType.MODIFIED,
                        column_changes=col_changes,
                        breaking=breaking
                    ))
        
        return changes
    
    def _compute_column_changes(
        self,
        cols_from: Dict[str, Any],
        cols_to: Dict[str, Any]
    ) -> List[ColumnChange]:
        """Compute column-level changes."""
        changes = []
        
        # Detect column removals (breaking)
        for col_name in cols_from:
            if col_name not in cols_to:
                changes.append(ColumnChange(
                    change_type=ChangeType.REMOVED,
                    column_name=col_name,
                    previous_type=cols_from[col_name].get("type")
                ))
        
        # Detect column additions
        for col_name in cols_to:
            if col_name not in cols_from:
                changes.append(ColumnChange(
                    change_type=ChangeType.ADDED,
                    column_name=col_name,
                    new_type=cols_to[col_name].get("type"),
                    new_nullable=cols_to[col_name].get("nullable", True)
                ))
        
        # Detect column type changes
        for col_name in cols_from:
            if col_name in cols_to:
                type_from = cols_from[col_name].get("type")
                type_to = cols_to[col_name].get("type")
                
                if type_from != type_to:
                    changes.append(ColumnChange(
                        change_type=ChangeType.MODIFIED,
                        column_name=col_name,
                        previous_type=type_from,
                        new_type=type_to
                    ))
                
                # Detect nullable changes
                nullable_from = cols_from[col_name].get("nullable", True)
                nullable_to = cols_to[col_name].get("nullable", True)
                
                if nullable_from != nullable_to:
                    changes.append(ColumnChange(
                        change_type=ChangeType.MODIFIED,
                        column_name=col_name,
                        nullable_changed=True,
                        previous_nullable=nullable_from,
                        new_nullable=nullable_to
                    ))
        
        return changes
    
    def get_breaking_changes(self) -> List[TableChange]:
        """Get all breaking changes detected."""
        return self.breaking_changes
    
    def validate_schema_consistency(self, gate_name: str) -> Tuple[bool, List[str]]:
        """Validate schema consistency for a gate."""
        schema = self.get_schema(gate_name)
        if not schema:
            return False, [f"No schema registered for gate {gate_name}"]
        
        errors = []
        
        # Validate table structure
        for table_name, table_def in schema.get("tables", {}).items():
            if not isinstance(table_def, dict):
                errors.append(f"Table {table_name} definition is not a dictionary")
            
            if "columns" not in table_def:
                errors.append(f"Table {table_name} missing columns definition")
        
        return len(errors) == 0, errors
    
    def generate_migration_guide(self, changes: List[TableChange]) -> str:
        """Generate migration guide for schema changes."""
        lines = ["# Schema Migration Guide\n"]
        
        breaking = [c for c in changes if c.breaking]
        if breaking:
            lines.append("## ⚠️ BREAKING CHANGES (Require Migration)\n")
            for change in breaking:
                lines.append(f"- Table `{change.table_name}`: {change.change_type.value}")
        
        non_breaking = [c for c in changes if not c.breaking]
        if non_breaking:
            lines.append("\n## ✅ NON-BREAKING CHANGES (Safe)\n")
            for change in non_breaking:
                lines.append(f"- Table `{change.table_name}`: {change.change_type.value}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tracker state to dict."""
        return {
            "schemas": self.schemas,
            "breaking_changes_count": len(self.breaking_changes),
            "changes_by_gate_pair": {
                gate_pair: [
                    {
                        "table": c.table_name,
                        "change_type": c.change_type.value,
                        "breaking": c.breaking
                    }
                    for c in changes
                ]
                for gate_pair, changes in self.changes.items()
            }
        }
