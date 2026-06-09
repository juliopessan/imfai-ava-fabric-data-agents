"""
Artifact Manager — Manages artifact lifecycle (create, version, archive, purge).
Tracks artifact metadata, versions, and status across gates.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import json


@dataclass
class ArtifactVersion:
    """A single version of an artifact."""
    version: int
    timestamp: str
    created_by: str
    gate: str
    status: str  # "draft", "approved", "archived"
    hash: str    # Content hash for change detection
    size_bytes: int


@dataclass
class ArtifactMetadata:
    """Artifact metadata and version history."""
    artifact_id: str
    name: str
    artifact_type: str  # "inventory", "architecture", "contracts", etc.
    owner: str
    created_at: str
    current_version: int
    versions: List[ArtifactVersion]
    lifecycle_stage: str  # "draft", "in_review", "approved", "archived"
    tags: List[str]


class ArtifactManager:
    """Manages artifact lifecycle and versioning."""
    
    def __init__(self):
        """Initialize manager."""
        self.artifacts: Dict[str, ArtifactMetadata] = {}
        self.artifact_registry: Dict[str, List[str]] = {}  # gate -> artifact_ids
    
    def create_artifact(
        self,
        artifact_id: str,
        name: str,
        artifact_type: str,
        owner: str,
        content_hash: str,
        size_bytes: int
    ) -> ArtifactMetadata:
        """Create a new artifact."""
        if artifact_id in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} already exists")
        
        version = ArtifactVersion(
            version=1,
            timestamp=datetime.utcnow().isoformat(),
            created_by=owner,
            gate="draft",
            status="draft",
            hash=content_hash,
            size_bytes=size_bytes
        )
        
        metadata = ArtifactMetadata(
            artifact_id=artifact_id,
            name=name,
            artifact_type=artifact_type,
            owner=owner,
            created_at=datetime.utcnow().isoformat(),
            current_version=1,
            versions=[version],
            lifecycle_stage="draft",
            tags=[]
        )
        
        self.artifacts[artifact_id] = metadata
        return metadata
    
    def add_version(
        self,
        artifact_id: str,
        content_hash: str,
        size_bytes: int,
        gate: str,
        updated_by: str
    ) -> ArtifactVersion:
        """Add a new version of an artifact."""
        if artifact_id not in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        
        metadata = self.artifacts[artifact_id]
        
        # Check if content changed
        if metadata.versions[-1].hash == content_hash:
            raise ValueError("Content unchanged - version not created")
        
        next_version = metadata.current_version + 1
        version = ArtifactVersion(
            version=next_version,
            timestamp=datetime.utcnow().isoformat(),
            created_by=updated_by,
            gate=gate,
            status="draft",
            hash=content_hash,
            size_bytes=size_bytes
        )
        
        metadata.versions.append(version)
        metadata.current_version = next_version
        
        return version
    
    def approve_artifact(
        self,
        artifact_id: str,
        gate: str,
        approver: str
    ) -> None:
        """Approve artifact for a gate."""
        if artifact_id not in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        
        metadata = self.artifacts[artifact_id]
        metadata.lifecycle_stage = "approved"
        metadata.versions[-1].status = "approved"
        metadata.versions[-1].gate = gate
        
        # Register in gate registry
        if gate not in self.artifact_registry:
            self.artifact_registry[gate] = []
        if artifact_id not in self.artifact_registry[gate]:
            self.artifact_registry[gate].append(artifact_id)
    
    def archive_artifact(self, artifact_id: str) -> None:
        """Archive an artifact."""
        if artifact_id not in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        
        metadata = self.artifacts[artifact_id]
        metadata.lifecycle_stage = "archived"
        metadata.versions[-1].status = "archived"
    
    def add_tags(self, artifact_id: str, tags: List[str]) -> None:
        """Add tags to an artifact."""
        if artifact_id not in self.artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        
        metadata = self.artifacts[artifact_id]
        metadata.tags.extend([t for t in tags if t not in metadata.tags])
    
    def get_artifact(self, artifact_id: str) -> Optional[ArtifactMetadata]:
        """Get artifact metadata."""
        return self.artifacts.get(artifact_id)
    
    def get_artifacts_by_type(self, artifact_type: str) -> List[ArtifactMetadata]:
        """Get all artifacts of a type."""
        return [a for a in self.artifacts.values() if a.artifact_type == artifact_type]
    
    def get_artifacts_by_gate(self, gate: str) -> List[ArtifactMetadata]:
        """Get all artifacts approved for a gate."""
        artifact_ids = self.artifact_registry.get(gate, [])
        return [self.artifacts[aid] for aid in artifact_ids if aid in self.artifacts]
    
    def get_artifact_history(self, artifact_id: str) -> List[Dict[str, Any]]:
        """Get version history for an artifact."""
        if artifact_id not in self.artifacts:
            return []
        
        metadata = self.artifacts[artifact_id]
        return [asdict(v) for v in metadata.versions]
    
    def detect_changes(self, artifact_id: str, new_hash: str) -> bool:
        """Detect if artifact content changed."""
        if artifact_id not in self.artifacts:
            return False
        
        metadata = self.artifacts[artifact_id]
        return metadata.versions[-1].hash != new_hash
    
    def generate_audit_trail(self, artifact_id: str) -> str:
        """Generate audit trail for an artifact."""
        if artifact_id not in self.artifacts:
            return ""
        
        metadata = self.artifacts[artifact_id]
        lines = [
            f"Artifact: {metadata.name} ({metadata.artifact_id})",
            f"Type: {metadata.artifact_type}",
            f"Owner: {metadata.owner}",
            f"Current Stage: {metadata.lifecycle_stage}",
            f"Version History:"
        ]
        
        for version in metadata.versions:
            lines.append(
                f"  v{version.version} ({version.timestamp}): {version.status} "
                f"(by {version.created_by}, gate={version.gate})"
            )
        
        return "\n".join(lines)
    
    def save_registry(self, output_path: Path) -> None:
        """Save artifact registry to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "artifacts": {
                aid: {
                    **asdict(metadata),
                    "versions": [asdict(v) for v in metadata.versions]
                }
                for aid, metadata in self.artifacts.items()
            },
            "gate_registry": self.artifact_registry
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_artifact_summary(self) -> Dict[str, Any]:
        """Generate summary of artifact inventory."""
        by_type = {}
        by_stage = {}
        
        for metadata in self.artifacts.values():
            # By type
            if metadata.artifact_type not in by_type:
                by_type[metadata.artifact_type] = 0
            by_type[metadata.artifact_type] += 1
            
            # By stage
            if metadata.lifecycle_stage not in by_stage:
                by_stage[metadata.lifecycle_stage] = 0
            by_stage[metadata.lifecycle_stage] += 1
        
        return {
            "total_artifacts": len(self.artifacts),
            "by_type": by_type,
            "by_stage": by_stage,
            "total_versions": sum(len(m.versions) for m in self.artifacts.values())
        }
