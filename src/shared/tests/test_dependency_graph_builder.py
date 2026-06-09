"""
Tests for DependencyGraphBuilder — Entity dependency analysis.
"""

import pytest
from src.shared.scripts.dependency_graph_builder import (
    DependencyGraphBuilder, EntityNode, DependencyEdge
)


class TestDependencyGraphBuilder:
    """Test suite for DependencyGraphBuilder."""
    
    def test_initialization(self):
        """Test builder initialization."""
        builder = DependencyGraphBuilder()
        assert len(builder.nodes) == 0
        assert len(builder.edges) == 0
    
    def test_add_entity(self):
        """Test adding entity to graph."""
        builder = DependencyGraphBuilder()
        
        node = builder.add_entity("customers", "source")
        
        assert node.entity_name == "customers"
        assert node.entity_type == "source"
        assert "customers" in builder.nodes
    
    def test_add_dependency(self):
        """Test adding dependency between entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_entity("customers", "source")
        builder.add_entity("customer_profile", "staging")
        
        edge = builder.add_dependency("customers", "customer_profile")
        
        assert edge.source == "customers"
        assert edge.target == "customer_profile"
        assert ("customers", "customer_profile") in builder.edges
    
    def test_add_dependency_auto_creates_nodes(self):
        """Test adding dependency creates missing nodes."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("source_a", "target_a")
        
        assert "source_a" in builder.nodes
        assert "target_a" in builder.nodes
    
    def test_dependency_relationships(self):
        """Test dependency relationships are bidirectional."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "customer_profile")
        
        source_node = builder.nodes["customers"]
        target_node = builder.nodes["customer_profile"]
        
        assert "customer_profile" in source_node.outgoing_dependencies
        assert "customers" in target_node.incoming_dependencies
    
    def test_get_upstream_entities_direct(self):
        """Test getting directly upstream entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "profile")
        builder.add_dependency("accounts", "profile")
        
        upstream = builder.get_upstream_entities("profile")
        
        assert "customers" in upstream
        assert "accounts" in upstream
    
    def test_get_upstream_entities_transitive(self):
        """Test getting transitive upstream entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("raw_customers", "customers")
        builder.add_dependency("customers", "profile")
        
        upstream = builder.get_upstream_entities("profile")
        
        assert "customers" in upstream
        assert "raw_customers" in upstream
    
    def test_get_downstream_entities_direct(self):
        """Test getting directly downstream entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "profile")
        builder.add_dependency("customers", "segment")
        
        downstream = builder.get_downstream_entities("customers")
        
        assert "profile" in downstream
        assert "segment" in downstream
    
    def test_get_downstream_entities_transitive(self):
        """Test getting transitive downstream entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "profile")
        builder.add_dependency("profile", "dashboard")
        
        downstream = builder.get_downstream_entities("customers")
        
        assert "profile" in downstream
        assert "dashboard" in downstream
    
    def test_impact_scope(self):
        """Test impact scope calculation."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "profile")
        builder.add_dependency("profile", "dashboard")
        builder.add_dependency("profile", "analytics")
        
        impact = builder.get_impact_scope("customers")
        
        assert impact["entity"] == "customers"
        assert "profile" in impact["directly_impacts"]
        assert len(impact["cascade_impacts"]) >= 2
    
    def test_calculate_impact_scores(self):
        """Test impact score calculation."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("source", "middle")
        builder.add_dependency("middle", "target_1")
        builder.add_dependency("middle", "target_2")
        builder.add_dependency("middle", "target_3")
        
        builder.calculate_impact_scores()
        
        middle_node = builder.nodes["middle"]
        assert middle_node.impact_score > 0
    
    def test_get_high_impact_entities(self):
        """Test filtering high impact entities."""
        builder = DependencyGraphBuilder()
        
        # Create entity with many dependencies (need 10+ for 0.1 threshold)
        # impact_score = min(1.0, downstream_count / 100.0)
        # So with 10 dependencies: 10/100 = 0.1
        for i in range(10):
            builder.add_dependency("hub", f"spoke_{i}")
        
        high_impact = builder.get_high_impact_entities(threshold=0.1)
        
        assert any(node.entity_name == "hub" for node in high_impact)
    
    def test_critical_dependencies(self):
        """Test marking critical dependencies."""
        builder = DependencyGraphBuilder()
        
        edge = builder.add_dependency(
            "critical_source",
            "mission_critical",
            is_critical=True
        )
        
        assert edge.is_critical is True
    
    def test_dependency_types(self):
        """Test different dependency types."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("a", "b", dependency_type="data_flow")
        builder.add_dependency("b", "c", dependency_type="transformation")
        builder.add_dependency("c", "d", dependency_type="aggregation")
        
        assert builder.edges[("a", "b")].dependency_type == "data_flow"
        assert builder.edges[("b", "c")].dependency_type == "transformation"
        assert builder.edges[("c", "d")].dependency_type == "aggregation"
    
    def test_no_circular_dependencies(self):
        """Test detecting no circular dependencies."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("a", "b")
        builder.add_dependency("b", "c")
        builder.add_dependency("c", "d")
        
        has_cycles, cycles = builder.check_circular_dependencies()
        
        assert has_cycles is False
    
    def test_get_root_entities(self):
        """Test identifying root entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("source_1", "middle")
        builder.add_dependency("source_2", "middle")
        builder.add_dependency("middle", "target")
        
        roots = builder.get_root_entities()
        
        assert "source_1" in roots
        assert "source_2" in roots
        assert "target" not in roots
    
    def test_get_leaf_entities(self):
        """Test identifying leaf entities."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("source", "middle")
        builder.add_dependency("middle", "leaf_1")
        builder.add_dependency("middle", "leaf_2")
        
        leaves = builder.get_leaf_entities()
        
        assert "leaf_1" in leaves
        assert "leaf_2" in leaves
        assert "source" not in leaves
    
    def test_generate_dependency_report(self):
        """Test report generation."""
        builder = DependencyGraphBuilder()
        
        builder.add_dependency("customers", "profile")
        builder.add_dependency("profile", "dashboard")
        
        report = builder.generate_dependency_report()
        
        assert "Dependency Graph Analysis Report" in report
        assert "Total Entities" in report
        assert "Total Dependencies" in report
    
    def test_complex_dependency_chain(self):
        """Test complex dependency chain."""
        builder = DependencyGraphBuilder()
        
        # Create a multi-level chain
        for i in range(4):
            builder.add_dependency(f"level_{i}", f"level_{i+1}")
        
        upstream = builder.get_upstream_entities("level_4")
        assert len(upstream) == 4
        
        downstream = builder.get_downstream_entities("level_0")
        assert len(downstream) == 4
    
    def test_diamond_dependency(self):
        """Test diamond dependency pattern."""
        builder = DependencyGraphBuilder()
        
        # Create diamond: A -> B,C -> D
        builder.add_dependency("a", "b")
        builder.add_dependency("a", "c")
        builder.add_dependency("b", "d")
        builder.add_dependency("c", "d")
        
        upstream_d = builder.get_upstream_entities("d")
        assert "a" in upstream_d
        assert "b" in upstream_d
        assert "c" in upstream_d
