"""
Tests for SchemaTracker — Schema change detection and migration guidance.
"""

import pytest
from src.shared.scripts.schema_tracker import (
    SchemaTracker, TableChange, ColumnChange, ChangeType
)


class TestSchemaTracker:
    """Test suite for SchemaTracker."""
    
    def test_initialization(self):
        """Test tracker initialization."""
        tracker = SchemaTracker()
        assert len(tracker.schemas) == 0
        assert len(tracker.breaking_changes) == 0
    
    def test_register_schema(self):
        """Test registering a schema."""
        tracker = SchemaTracker()
        schema = {
            "tables": {
                "customers": {
                    "columns": {
                        "id": {"type": "int", "nullable": False},
                        "name": {"type": "string", "nullable": False}
                    }
                }
            }
        }
        
        tracker.register_schema("gate_1", schema)
        assert "gate_1" in tracker.schemas
    
    def test_get_schema(self):
        """Test retrieving a schema."""
        tracker = SchemaTracker()
        schema = {"tables": {}}
        
        tracker.register_schema("gate_1", schema)
        retrieved = tracker.get_schema("gate_1")
        
        assert retrieved is not None
        assert retrieved == schema
    
    def test_get_schema_nonexistent(self):
        """Test retrieving non-existent schema."""
        tracker = SchemaTracker()
        assert tracker.get_schema("nonexistent") is None
    
    def test_compare_schemas_no_changes(self):
        """Test comparing identical schemas."""
        tracker = SchemaTracker()
        schema = {
            "tables": {
                "customers": {
                    "columns": {
                        "id": {"type": "int", "nullable": False}
                    }
                }
            }
        }
        
        tracker.register_schema("gate_1", schema)
        tracker.register_schema("gate_2", schema)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is True
        assert len(changes) == 0
    
    def test_compare_schemas_table_added(self):
        """Test detecting new table."""
        tracker = SchemaTracker()
        schema_1 = {"tables": {}}
        schema_2 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is True
        assert len(changes) == 1
        assert changes[0].change_type == ChangeType.ADDED
    
    def test_compare_schemas_table_removed_breaking(self):
        """Test detecting table removal (breaking change)."""
        tracker = SchemaTracker()
        schema_1 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        schema_2 = {"tables": {}}
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is False
        assert len(changes) == 1
        assert changes[0].breaking is True
    
    def test_compare_schemas_column_added(self):
        """Test detecting column addition."""
        tracker = SchemaTracker()
        schema_1 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        schema_2 = {
            "tables": {
                "customers": {
                    "columns": {
                        "id": {"type": "int"},
                        "name": {"type": "string"}
                    }
                }
            }
        }
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is True
        assert len(changes) == 1
        assert changes[0].change_type == ChangeType.MODIFIED
    
    def test_compare_schemas_column_removed_breaking(self):
        """Test detecting column removal (breaking change)."""
        tracker = SchemaTracker()
        schema_1 = {
            "tables": {
                "customers": {
                    "columns": {
                        "id": {"type": "int"},
                        "name": {"type": "string"}
                    }
                }
            }
        }
        schema_2 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is False
        assert len(changes) == 1
        assert any(c.breaking for c in changes)
    
    def test_compare_schemas_column_type_changed(self):
        """Test detecting column type change."""
        tracker = SchemaTracker()
        schema_1 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        schema_2 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "bigint"}}
                }
            }
        }
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        no_breaking, changes = tracker.compare_schemas("gate_1", "gate_2")
        assert no_breaking is True  # Type change is not necessarily breaking
        assert len(changes) == 1
    
    def test_get_breaking_changes(self):
        """Test retrieving breaking changes."""
        tracker = SchemaTracker()
        schema_1 = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        schema_2 = {"tables": {}}
        
        tracker.register_schema("gate_1", schema_1)
        tracker.register_schema("gate_2", schema_2)
        
        tracker.compare_schemas("gate_1", "gate_2")
        breaking = tracker.get_breaking_changes()
        
        assert len(breaking) > 0
    
    def test_validate_schema_consistency_valid(self):
        """Test schema consistency validation."""
        tracker = SchemaTracker()
        schema = {
            "tables": {
                "customers": {
                    "columns": {"id": {"type": "int"}}
                }
            }
        }
        
        tracker.register_schema("gate_1", schema)
        valid, errors = tracker.validate_schema_consistency("gate_1")
        
        assert valid is True
        assert len(errors) == 0
    
    def test_validate_schema_consistency_missing_columns(self):
        """Test validation fails with missing columns."""
        tracker = SchemaTracker()
        schema = {
            "tables": {
                "customers": {}  # Missing columns
            }
        }
        
        tracker.register_schema("gate_1", schema)
        valid, errors = tracker.validate_schema_consistency("gate_1")
        
        assert valid is False
        assert any("columns" in e for e in errors)
    
    def test_generate_migration_guide(self):
        """Test migration guide generation."""
        tracker = SchemaTracker()
        
        changes = [
            TableChange(
                table_name="old_table",
                change_type=ChangeType.REMOVED,
                column_changes=[],
                breaking=True
            ),
            TableChange(
                table_name="new_table",
                change_type=ChangeType.ADDED,
                column_changes=[],
                breaking=False
            )
        ]
        
        guide = tracker.generate_migration_guide(changes)
        assert "BREAKING CHANGES" in guide
        assert "NON-BREAKING CHANGES" in guide
    
    def test_to_dict(self):
        """Test conversion to dict."""
        tracker = SchemaTracker()
        schema = {"tables": {}}
        
        tracker.register_schema("gate_1", schema)
        data = tracker.to_dict()
        
        assert "schemas" in data
        assert "breaking_changes_count" in data
        assert "changes_by_gate_pair" in data
