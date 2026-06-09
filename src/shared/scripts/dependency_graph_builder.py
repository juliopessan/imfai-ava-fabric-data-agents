"""
Dependency Graph Builder — Builds entity dependency graph for impact analysis.
Tracks data lineage and dependency chains for impact assessment.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import json


@dataclass
class DependencyEdge:
    """Single dependency relationship."""
    source: str  # Source entity
    target: str  # Target entity (depends on source)
    dependency_type: str  # "data_flow", "transformation", "aggregation"
    description: str = ""
    is_critical: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "source": self.source,
            "target": self.target,
            "dependency_type": self.dependency_type,
            "description": self.description,
            "is_critical": self.is_critical
        }


@dataclass
class EntityNode:
    """Entity node in dependency graph."""
    entity_name: str
    entity_type: str  # "source", "staging", "target"
    incoming_dependencies: List[str] = field(default_factory=list)  # Entities this depends on
    outgoing_dependencies: List[str] = field(default_factory=list)  # Entities depending on this
    impact_score: float = 0.0
    criticality_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "entity_name": self.entity_name,
            "entity_type": self.entity_type,
            "incoming_dependencies": self.incoming_dependencies,
            "outgoing_dependencies": self.outgoing_dependencies,
            "impact_score": round(self.impact_score, 4),
            "criticality_score": round(self.criticality_score, 4)
        }


class DependencyGraphBuilder:
    """Builds and analyzes entity dependency graphs."""
    
    def __init__(self):
        """Initialize builder."""
        self.nodes: Dict[str, EntityNode] = {}
        self.edges: Dict[Tuple[str, str], DependencyEdge] = {}
    
    def add_entity(
        self,
        entity_name: str,
        entity_type: str = "staging"
    ) -> EntityNode:
        """Add entity node to graph."""
        node = EntityNode(
            entity_name=entity_name,
            entity_type=entity_type
        )
        self.nodes[entity_name] = node
        return node
    
    def add_dependency(
        self,
        source: str,
        target: str,
        dependency_type: str = "data_flow",
        description: str = "",
        is_critical: bool = False
    ) -> DependencyEdge:
        """
        Add dependency edge (target depends on source).
        
        Args:
            source: Source entity
            target: Target entity (depends on source)
            dependency_type: Type of dependency
            description: Description
            is_critical: Whether dependency is critical
        
        Returns:
            Dependency edge
        """
        # Ensure nodes exist
        if source not in self.nodes:
            self.add_entity(source, "staging")
        if target not in self.nodes:
            self.add_entity(target, "staging")
        
        edge = DependencyEdge(
            source=source,
            target=target,
            dependency_type=dependency_type,
            description=description,
            is_critical=is_critical
        )
        
        edge_key = (source, target)
        self.edges[edge_key] = edge
        
        # Update node relationships
        self.nodes[source].outgoing_dependencies.append(target)
        self.nodes[target].incoming_dependencies.append(source)
        
        return edge
    
    def get_upstream_entities(self, entity_name: str) -> Set[str]:
        """Get all entities this entity depends on."""
        if entity_name not in self.nodes:
            return set()
        
        upstream = set()
        visited = set()
        queue = [entity_name]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current in self.nodes:
                for dep in self.nodes[current].incoming_dependencies:
                    upstream.add(dep)
                    queue.append(dep)
        
        return upstream
    
    def get_downstream_entities(self, entity_name: str) -> Set[str]:
        """Get all entities depending on this entity."""
        if entity_name not in self.nodes:
            return set()
        
        downstream = set()
        visited = set()
        queue = [entity_name]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current in self.nodes:
                for dep in self.nodes[current].outgoing_dependencies:
                    downstream.add(dep)
                    queue.append(dep)
        
        return downstream
    
    def get_impact_scope(self, entity_name: str) -> Dict:
        """Get full impact scope of changes to entity."""
        downstream = self.get_downstream_entities(entity_name)
        
        return {
            "entity": entity_name,
            "directly_impacts": self.nodes[entity_name].outgoing_dependencies if entity_name in self.nodes else [],
            "cascade_impacts": list(downstream),
            "total_impact_count": len(downstream)
        }
    
    def calculate_impact_scores(self) -> None:
        """Calculate impact scores for all entities."""
        for entity_name in self.nodes.keys():
            downstream_count = len(self.get_downstream_entities(entity_name))
            critical_count = sum(
                1 for edge in self.edges.values()
                if edge.source == entity_name and edge.is_critical
            )
            
            self.nodes[entity_name].impact_score = min(1.0, downstream_count / 100.0)
            self.nodes[entity_name].criticality_score = critical_count / max(1, len(self.nodes[entity_name].outgoing_dependencies))
    
    def get_high_impact_entities(self, threshold: float = 0.5) -> List[EntityNode]:
        """Get entities with high impact scores."""
        self.calculate_impact_scores()
        
        high_impact = [
            node for node in self.nodes.values()
            if node.impact_score >= threshold
        ]
        
        return sorted(high_impact, key=lambda n: n.impact_score, reverse=True)
    
    def check_circular_dependencies(self) -> Tuple[bool, List[List[str]]]:
        """
        Check for circular dependencies.
        
        Returns:
            (has_cycles, list of cycle paths)
        """
        cycles = []
        
        for entity in self.nodes.keys():
            visited = set()
            path = []
            
            if self._dfs_cycle(entity, visited, path):
                cycles.append(path[:])
        
        return len(cycles) > 0, cycles
    
    def _dfs_cycle(
        self,
        entity: str,
        visited: Set[str],
        path: List[str]
    ) -> bool:
        """DFS for cycle detection."""
        if entity in visited:
            if entity in path:
                # Found cycle
                cycle_start = path.index(entity)
                path[:] = path[cycle_start:] + [entity]
                return True
            return False
        
        visited.add(entity)
        path.append(entity)
        
        if entity in self.nodes:
            for dep in self.nodes[entity].incoming_dependencies:
                if self._dfs_cycle(dep, visited.copy(), path[:]):
                    return True
        
        return False
    
    def get_root_entities(self) -> List[str]:
        """Get source entities (no incoming dependencies)."""
        return [
            name for name, node in self.nodes.items()
            if len(node.incoming_dependencies) == 0
        ]
    
    def get_leaf_entities(self) -> List[str]:
        """Get leaf entities (no outgoing dependencies)."""
        return [
            name for name, node in self.nodes.items()
            if len(node.outgoing_dependencies) == 0
        ]
    
    def generate_dependency_report(self) -> str:
        """Generate dependency analysis report."""
        self.calculate_impact_scores()
        
        has_cycles, cycles = self.check_circular_dependencies()
        
        report = "Dependency Graph Analysis Report\n"
        report += f"Total Entities: {len(self.nodes)}\n"
        report += f"Total Dependencies: {len(self.edges)}\n"
        report += f"Root Entities: {len(self.get_root_entities())}\n"
        report += f"Leaf Entities: {len(self.get_leaf_entities())}\n"
        report += f"Circular Dependencies: {'YES' if has_cycles else 'NO'}\n\n"
        
        high_impact = self.get_high_impact_entities(threshold=0.3)
        if high_impact:
            report += "High Impact Entities:\n"
            for entity in high_impact[:5]:
                report += f"  - {entity.entity_name} (Impact: {entity.impact_score:.2f})\n"
        
        if has_cycles:
            report += f"\nCycles Detected: {len(cycles)}\n"
        
        return report
    
    def save_graph(self, file_path: str) -> None:
        """Save graph to file."""
        graph_dict = {
            "nodes": {name: node.to_dict() for name, node in self.nodes.items()},
            "edges": [edge.to_dict() for edge in self.edges.values()]
        }
        
        with open(file_path, "w") as f:
            json.dump(graph_dict, f, indent=2)
