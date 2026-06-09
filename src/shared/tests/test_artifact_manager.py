"""
Tests for ArtifactManager — Artifact lifecycle and versioning management.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.shared.scripts.artifact_manager import (
    ArtifactManager, ArtifactMetadata, ArtifactVersion
)


class TestArtifactManager:
    """Test suite for ArtifactManager."""
    
    def test_initialization(self):
        """Test manager initialization."""
        manager = ArtifactManager()
        assert len(manager.artifacts) == 0
        assert len(manager.artifact_registry) == 0
    
    def test_create_artifact(self):
        """Test creating an artifact."""
        manager = ArtifactManager()
        metadata = manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        assert metadata.artifact_id == "inv-001"
        assert metadata.current_version == 1
        assert len(metadata.versions) == 1
        assert metadata.lifecycle_stage == "draft"
    
    def test_create_artifact_duplicate_id(self):
        """Test creating artifact with duplicate ID."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        with pytest.raises(ValueError, match="already exists"):
            manager.create_artifact(
                artifact_id="inv-001",
                name="other",
                artifact_type="inventory",
                owner="bob@company.com",
                content_hash="def456",
                size_bytes=2048
            )
    
    def test_add_version(self):
        """Test adding a new version."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        version = manager.add_version(
            artifact_id="inv-001",
            content_hash="def456",  # Changed
            size_bytes=2048,
            gate="gate_1",
            updated_by="alice@company.com"
        )
        
        assert version.version == 2
        assert version.status == "draft"
        metadata = manager.get_artifact("inv-001")
        assert metadata.current_version == 2
    
    def test_add_version_unchanged_content(self):
        """Test adding version with unchanged content."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        with pytest.raises(ValueError, match="Content unchanged"):
            manager.add_version(
                artifact_id="inv-001",
                content_hash="abc123",  # Same
                size_bytes=1024,
                gate="gate_1",
                updated_by="alice@company.com"
            )
    
    def test_approve_artifact(self):
        """Test approving an artifact."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        manager.approve_artifact("inv-001", "gate_1", "approver@company.com")
        
        metadata = manager.get_artifact("inv-001")
        assert metadata.lifecycle_stage == "approved"
        assert metadata.versions[-1].status == "approved"
        assert "gate_1" in manager.artifact_registry
        assert "inv-001" in manager.artifact_registry["gate_1"]
    
    def test_archive_artifact(self):
        """Test archiving an artifact."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        manager.archive_artifact("inv-001")
        
        metadata = manager.get_artifact("inv-001")
        assert metadata.lifecycle_stage == "archived"
        assert metadata.versions[-1].status == "archived"
    
    def test_add_tags(self):
        """Test adding tags to artifact."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        manager.add_tags("inv-001", ["gate1", "critical"])
        
        metadata = manager.get_artifact("inv-001")
        assert "gate1" in metadata.tags
        assert "critical" in metadata.tags
    
    def test_get_artifact(self):
        """Test retrieving artifact."""
        manager = ArtifactManager()
        manager.create_artifact(
            artifact_id="inv-001",
            name="discovery_inventory",
            artifact_type="inventory",
            owner="alice@company.com",
            content_hash="abc123",
            size_bytes=1024
        )
        
        metadata = manager.get_artifact("inv-001")
        assert metadata is not None
        assert metadata.name == "discovery_inventory"
    
    def test_get_artifact_nonexistent(self):
        """Test retrieving non-existent artifact."""
        manager = ArtifactManager()
        assert manager.get_artifact("nonexistent") is None
    
    def test_get_artifacts_by_type(self):
        """Test filtering artifacts by type."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory1", "inventory", "alice@company.com", "hash1", 1024)
        manager.create_artifact("inv-002", "inventory2", "inventory", "alice@company.com", "hash2", 1024)
        manager.create_artifact("arch-001", "architecture", "architecture", "bob@company.com", "hash3", 2048)
        
        inventories = manager.get_artifacts_by_type("inventory")
        assert len(inventories) == 2
        assert all(a.artifact_type == "inventory" for a in inventories)
    
    def test_get_artifacts_by_gate(self):
        """Test filtering artifacts by gate."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory1", "inventory", "alice@company.com", "hash1", 1024)
        manager.create_artifact("inv-002", "inventory2", "inventory", "alice@company.com", "hash2", 1024)
        
        manager.approve_artifact("inv-001", "gate_1", "approver@company.com")
        
        gate1_artifacts = manager.get_artifacts_by_gate("gate_1")
        assert len(gate1_artifacts) == 1
        assert gate1_artifacts[0].artifact_id == "inv-001"
    
    def test_get_artifact_history(self):
        """Test retrieving artifact version history."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory", "inventory", "alice@company.com", "hash1", 1024)
        manager.add_version("inv-001", "hash2", 2048, "gate_1", "alice@company.com")
        manager.add_version("inv-001", "hash3", 3072, "gate_2", "alice@company.com")
        
        history = manager.get_artifact_history("inv-001")
        assert len(history) == 3
        assert history[0]["version"] == 1
        assert history[2]["version"] == 3
    
    def test_detect_changes(self):
        """Test change detection."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory", "inventory", "alice@company.com", "hash1", 1024)
        
        assert manager.detect_changes("inv-001", "hash2") is True
        assert manager.detect_changes("inv-001", "hash1") is False
    
    def test_generate_audit_trail(self):
        """Test generating audit trail."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "discovery_inventory", "inventory", "alice@company.com", "hash1", 1024)
        manager.add_version("inv-001", "hash2", 2048, "gate_1", "alice@company.com")
        
        trail = manager.generate_audit_trail("inv-001")
        assert "discovery_inventory" in trail
        assert "v1" in trail
        assert "v2" in trail
    
    def test_save_registry(self):
        """Test saving registry to file."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory", "inventory", "alice@company.com", "hash1", 1024)
        manager.approve_artifact("inv-001", "gate_1", "approver@company.com")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "registry.json"
            manager.save_registry(output_path)
            
            assert output_path.exists()
            with open(output_path) as f:
                data = json.load(f)
            
            assert "inv-001" in data["artifacts"]
            assert "gate_1" in data["gate_registry"]
    
    def test_get_artifact_summary(self):
        """Test generating artifact summary."""
        manager = ArtifactManager()
        manager.create_artifact("inv-001", "inventory1", "inventory", "alice@company.com", "hash1", 1024)
        manager.create_artifact("inv-002", "inventory2", "inventory", "alice@company.com", "hash2", 1024)
        manager.create_artifact("arch-001", "architecture", "architecture", "bob@company.com", "hash3", 2048)
        manager.approve_artifact("inv-001", "gate_1", "approver@company.com")
        
        summary = manager.get_artifact_summary()
        assert summary["total_artifacts"] == 3
        assert summary["by_type"]["inventory"] == 2
        assert summary["by_type"]["architecture"] == 1
        assert summary["by_stage"]["draft"] == 2
        assert summary["by_stage"]["approved"] == 1
