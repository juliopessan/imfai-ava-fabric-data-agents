#!/usr/bin/env python3
"""
Tests for Tier B complementation components.
Validates confidence escalation, knowledge graph, deduplication, SQL AST, and spec repository.
"""

import pytest
from pathlib import Path
import tempfile
import os
from datetime import datetime, timezone

from src.shared.scripts.confidence_escalation import (
    ConfidenceEscalationEngine, ConfidenceScore, EscalationLevel
)
from src.shared.scripts.knowledge_graph_store import (
    KnowledgeGraphStore, StoredEntity, StoredLineageEdge
)
from src.shared.scripts.artifact_deduplication import (
    ArtifactDeduplicationService, ArtifactFingerprint
)
from src.shared.scripts.sql_ast_parser import (
    SQLASTParser, SQLEntity, SQLEntityType
)
from src.shared.scripts.spec_repository import (
    SpecRepository, DataContract, GovernanceRule, SeverityLevel
)


class TestConfidenceEscalation:
    """Test confidence escalation system."""
    
    def test_gate1_confidence_scoring(self):
        """Test Gate 1 confidence calculation."""
        engine = ConfidenceEscalationEngine()
        
        score = engine.score_gate1_upstream(
            wave_id="wave1",
            discovered_entities=80,
            total_expected_entities=100,
            lineage_entries=45,
            total_expected_lineage=50,
            identified_risks=9,
            total_risk_categories=10
        )
        
        assert score.gate == 1
        assert score.entity_discovery_completeness == 0.8
        assert score.overall_confidence >= 0.80  # Should be high-confidence
        assert score.escalation_level == EscalationLevel.AUTO_PROCEED
    
    def test_gate2_low_confidence_escalation(self):
        """Test Gate 2 low-confidence triggers BLOCKED escalation."""
        engine = ConfidenceEscalationEngine()

        score = engine.score_gate2_midstream(
            wave_id="wave_low_conf",
            lineage_completeness=0.40,
            contracts_defined=2,
            total_entities=10,
            identified_risks=3,
            total_risk_categories=10
        )
        # 0.40*0.40 + 0.20*0.35 + 0.30*0.25 = 0.16 + 0.07 + 0.075 = 0.305
        assert score.gate == 2
        assert score.overall_confidence < 0.70
        assert score.escalation_level == EscalationLevel.BLOCKED

        needs_escalation, reason = engine.should_escalate("wave_low_conf", 2)
        assert needs_escalation is True
    
    def test_escalation_decision_recording(self):
        """Test recording escalation decisions."""
        engine = ConfidenceEscalationEngine()
        
        score = engine.score_gate1_upstream(
            wave_id="wave1",
            discovered_entities=50,
            total_expected_entities=100,
            lineage_entries=20,
            total_expected_lineage=50,
            identified_risks=5,
            total_risk_categories=10
        )
        
        decision = engine.record_escalation_decision(
            wave_id="wave1",
            gate=1,
            escalated_to="data-architect",
            decision="approved",
            feedback="Acceptable - sampling validation passed",
            rework_items=["increase_entity_discovery_sample"]
        )
        
        assert decision.escalated_to == "data-architect"
        assert decision.decision == "approved"
        assert len(decision.rework_items) == 1


class TestKnowledgeGraphStore:
    """Test persistent knowledge graph store."""
    
    def test_save_and_retrieve_entity(self):
        """Test entity storage and retrieval."""
        with KnowledgeGraphStore(":memory:") as store:
            entity = StoredEntity(
                entity_name="customers",
                entity_type="source",
                wave_id="wave1",
                created_at=datetime.now(timezone.utc).isoformat(),
                incoming_dependencies=[],
                outgoing_dependencies=["orders"],
                impact_score=0.8,
                criticality_score=0.9,
                patterns=["scd"]
            )
            store.save_entity(entity)
            # find_similar_entities: wave_id param excludes that wave; :memory: has no wave99
            results = store.find_similar_entities("customers", wave_id="wave99")
            assert len(results) == 1
            assert results[0]["entity_name"] == "customers"

    def test_lineage_edge_storage(self):
        """Test lineage edge persistence."""
        with KnowledgeGraphStore(":memory:") as store:
            edge = StoredLineageEdge(
                source="raw_orders",
                target="processed_orders",
                dependency_type="data_flow",
                description="ETL transformation",
                is_critical=True,
                wave_id="wave1",
                created_at=datetime.now(timezone.utc).isoformat()
            )
            store.save_lineage_edge(edge)
            lineage = store.get_entity_lineage("processed_orders", "wave1")
            assert len(lineage["incoming"]) == 1
            assert lineage["incoming"][0]["source"] == "raw_orders"
            assert lineage["incoming"][0]["is_critical"] is True

    def test_statistics(self):
        """Test store statistics."""
        with KnowledgeGraphStore(":memory:") as store:
            entity = StoredEntity(
                entity_name="orders",
                entity_type="target",
                wave_id="wave2",
                created_at=datetime.now(timezone.utc).isoformat(),
                incoming_dependencies=["raw_orders"],
                outgoing_dependencies=[],
                impact_score=0.5,
                criticality_score=0.5,
                patterns=[]
            )
            store.save_entity(entity)
            stats = store.get_statistics()
            assert stats["total_entities"] == 1
            assert stats["waves_stored"] == 1
            assert stats["total_lineage_edges"] == 0


class TestArtifactDeduplication:
    """Test artifact deduplication service."""
    
    def test_hash_computation(self):
        """Test content hash computation."""
        content = "SELECT * FROM customers"
        hash1 = ArtifactDeduplicationService.compute_hash(content)
        hash2 = ArtifactDeduplicationService.compute_hash(content)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256
    
    def test_artifact_registration(self):
        """Test artifact registration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dedup = ArtifactDeduplicationService(
                os.path.join(tmpdir, "artifacts.json")
            )
            
            fp = dedup.register_artifact(
                wave_id="wave2",
                artifact_id="sttm_001",
                artifact_type="STTM",
                content="customers => processed_customers",
                estimated_token_usage=1000.0
            )
            
            assert fp.artifact_id == "sttm_001"
            assert fp.artifact_type == "STTM"
    
    def test_duplicate_detection(self):
        """Test duplicate artifact detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dedup = ArtifactDeduplicationService(
                os.path.join(tmpdir, "artifacts.json")
            )
            
            content = "STTM mapping"
            
            fp1 = dedup.register_artifact(
                wave_id="wave2",
                artifact_id="sttm_001",
                artifact_type="STTM",
                content=content,
                estimated_token_usage=500.0
            )
            
            content_hash = ArtifactDeduplicationService.compute_hash(content)
            duplicate = dedup.find_duplicate("STTM", content_hash, exclude_wave="wave2")
            
            assert duplicate is None  # Same wave, excluded
    
    def test_deduplication_report(self):
        """Test deduplication report generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            dedup = ArtifactDeduplicationService(
                os.path.join(tmpdir, "artifacts.json")
            )
            
            dedup.register_artifact(
                wave_id="wave2",
                artifact_id="sttm_001",
                artifact_type="STTM",
                content="test",
                estimated_token_usage=1000.0
            )
            
            report = dedup.get_deduplication_report()
            assert report["total_artifacts_registered"] > 0


class TestSQLASTParser:
    """Test SQL parsing for lineage extraction."""
    
    def test_extract_entities_from_select(self):
        """Test entity extraction from SELECT."""
        parser = SQLASTParser()
        query = """
            SELECT c.id, c.name, o.order_id, COUNT(*) as order_count
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            WHERE c.created_at > '2026-01-01'
            GROUP BY c.id, c.name, o.order_id
        """
        
        entities = parser.extract_entities(query)
        
        assert "customers" in entities["tables"]
        assert "orders" in entities["tables"]
        assert len(entities["aggregations"]) > 0  # COUNT
    
    def test_lineage_edge_extraction(self):
        """Test lineage edge extraction."""
        parser = SQLASTParser()
        query = """
            INSERT INTO processed_orders
            SELECT o.*, c.country
            FROM raw_orders o
            JOIN customer_dim c ON o.customer_id = c.id
        """
        
        edges = parser.extract_lineage_edges(query)
        
        assert len(edges) > 0
        sources = [e.source_table for e in edges]
        assert "raw_orders" in sources or "customer_dim" in sources
    
    def test_scd_detection(self):
        """Test SCD pattern detection."""
        parser = SQLASTParser()
        query = """
            MERGE INTO customer_dim tgt
            USING customer_stg src
            ON tgt.customer_id = src.customer_id
            WHEN MATCHED AND tgt.effective_date < src.effective_date
                THEN UPDATE SET tgt.is_current = 0, tgt.valid_to = CURRENT_DATE
            WHEN NOT MATCHED
                THEN INSERT (customer_id, valid_from, is_current)
                VALUES (src.customer_id, CURRENT_DATE, 1)
        """
        
        is_scd = parser.detect_slowly_changing_dimension(query)
        assert is_scd is True
    
    def test_incremental_load_detection(self):
        """Test incremental load detection."""
        parser = SQLASTParser()
        query = """
            SELECT *
            FROM raw_orders
            WHERE updated_at > (SELECT MAX(updated_at) FROM processed_orders)
        """
        
        is_incremental = parser.detect_incremental_load(query)
        assert is_incremental is True


class TestSpecRepository:
    """Test specification storage and retrieval."""
    
    def test_save_and_retrieve_contract(self):
        """Test data contract storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = SpecRepository(tmpdir)
            
            contract = DataContract(
                table_name="customers",
                description="Customer master data",
                owner="data-platform",
                sla_availability_pct=99.95,
                sla_rto_minutes=30,
                retention_days=2555,
                pii_columns=["email", "phone", "ssn"],
                requires_encryption=True,
                audit_required=True,
                version=1
            )
            
            contract_id = repo.save_contract(contract)
            assert contract_id == "customers_v1"
            
            retrieved = repo.get_contract("customers", version=1)
            assert retrieved is not None
            assert retrieved.table_name == "customers"
            assert retrieved.sla_availability_pct == 99.95
    
    def test_save_governance_rule(self):
        """Test governance rule storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = SpecRepository(tmpdir)
            
            rule = GovernanceRule(
                rule_id="customer_email_unique",
                rule_name="Customer Email Uniqueness",
                description="Customer email must be unique across the table",
                severity=SeverityLevel.CRITICAL,
                validation_logic="SELECT COUNT(*) FROM customers GROUP BY email HAVING COUNT(*) > 1",
                remediation="Remove or update duplicate emails"
            )
            
            rule_id = repo.save_rule(rule)
            assert rule_id == "customer_email_unique_v1"
    
    def test_repository_statistics(self):
        """Test repository statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = SpecRepository(tmpdir)
            
            contract = DataContract(table_name="test", version=1)
            repo.save_contract(contract)
            
            stats = repo.get_statistics()
            assert stats["total_contracts"] == 1
            assert stats["unique_contracts"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
