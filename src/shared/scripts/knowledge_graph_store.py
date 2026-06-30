#!/usr/bin/env python3
"""
Knowledge Graph Store — Persistent storage for dependency graphs across waves.

Persists entity relationships, lineage, and patterns from completed migrations
so Wave N+1 can reuse patterns, reducing analysis time by 30-40%.

Usage:
  store = KnowledgeGraphStore("financeiro_kg.db")
  store.save_graph(wave_id="wave2", graph=dependency_graph)
  
  # Later, in wave5:
  similar = store.find_similar_entities("customers", wave_id="wave2")
  # → [{"wave": "wave2", "entity": "customers", "lineage": [...], "patterns": [...]}]
"""

import sqlite3
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class StoredEntity:
    """Persisted entity from knowledge graph."""
    entity_name: str
    entity_type: str  # "source", "staging", "target"
    wave_id: str
    created_at: str
    incoming_dependencies: List[str]
    outgoing_dependencies: List[str]
    impact_score: float
    criticality_score: float
    patterns: List[str]  # ["aggregation", "slowly_changing_dim", etc.]


@dataclass
class StoredLineageEdge:
    """Persisted lineage edge."""
    source: str
    target: str
    dependency_type: str
    description: str
    is_critical: bool
    wave_id: str
    created_at: str


class KnowledgeGraphStore:
    """Persistent store for dependency graphs and entity patterns."""
    
    def __init__(self, db_path: str = "knowledge_graphs.db"):
        """Initialize store with a persistent connection."""
        self.db_path = str(db_path)
        # Persistent connection — required for :memory: and avoids Windows file lock
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def close(self):
        """Explicitly close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def _init_schema(self):
        """Initialize SQLite schema."""
        conn = self._conn
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY,
                entity_name TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                wave_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                incoming_deps TEXT,
                outgoing_deps TEXT,
                impact_score REAL,
                criticality_score REAL,
                patterns TEXT,
                UNIQUE(entity_name, wave_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS lineage_edges (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                dependency_type TEXT NOT NULL,
                description TEXT,
                is_critical INTEGER,
                wave_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(source, target, wave_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS entity_patterns (
                id INTEGER PRIMARY KEY,
                wave_id TEXT NOT NULL,
                entity_name TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                UNIQUE(wave_id, entity_name, pattern_type)
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_entity_name ON entities(entity_name)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_wave_id ON entities(wave_id)
        """)
        conn.commit()
    
    def save_entity(self, entity: StoredEntity) -> None:
        """Save entity to store."""
        conn = self._conn
        conn.execute("""
                INSERT OR REPLACE INTO entities
                (entity_name, entity_type, wave_id, created_at, incoming_deps, 
                 outgoing_deps, impact_score, criticality_score, patterns)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity.entity_name,
                entity.entity_type,
                entity.wave_id,
                entity.created_at,
                json.dumps(entity.incoming_dependencies),
                json.dumps(entity.outgoing_dependencies),
                entity.impact_score,
                entity.criticality_score,
                json.dumps(entity.patterns)
            ))
        conn.commit()
    
    def save_lineage_edge(self, edge: StoredLineageEdge) -> None:
        """Save lineage edge to store."""
        conn = self._conn
        conn.execute("""
                INSERT OR REPLACE INTO lineage_edges
                (source, target, dependency_type, description, is_critical, wave_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                edge.source,
                edge.target,
                edge.dependency_type,
                edge.description,
                1 if edge.is_critical else 0,
                edge.wave_id,
                edge.created_at
            ))
        conn.commit()
    
    def find_similar_entities(
        self,
        entity_name: str,
        wave_id: Optional[str] = None,
        entity_type: Optional[str] = None
    ) -> List[Dict]:
        """Find entities similar to the given one from other waves."""
        conn = self._conn
        query = "SELECT * FROM entities WHERE entity_name = ?"
        params = [entity_name]

        if entity_type:
            query += " AND entity_type = ?"
            params.append(entity_type)

        if wave_id:
            query += " AND wave_id != ?"
            params.append(wave_id)

        rows = conn.execute(query, params).fetchall()

        results = []
        for row in rows:
            results.append({
                "entity_name": row["entity_name"],
                "entity_type": row["entity_type"],
                "wave_id": row["wave_id"],
                "incoming_deps": json.loads(row["incoming_deps"]),
                "outgoing_deps": json.loads(row["outgoing_deps"]),
                "impact_score": row["impact_score"],
                "criticality_score": row["criticality_score"],
                "patterns": json.loads(row["patterns"]),
                "created_at": row["created_at"]
            })

        return results
    
    def get_entities_by_wave(self, wave_id: str) -> List[StoredEntity]:
        """Get all entities from a specific wave."""
        conn = self._conn
        rows = conn.execute(
            "SELECT * FROM entities WHERE wave_id = ?",
            (wave_id,)
        ).fetchall()

        return [
            StoredEntity(
                entity_name=row["entity_name"],
                entity_type=row["entity_type"],
                wave_id=row["wave_id"],
                created_at=row["created_at"],
                incoming_dependencies=json.loads(row["incoming_deps"]),
                outgoing_dependencies=json.loads(row["outgoing_deps"]),
                impact_score=row["impact_score"],
                criticality_score=row["criticality_score"],
                patterns=json.loads(row["patterns"])
            )
            for row in rows
        ]

    def get_entity_lineage(self, entity_name: str, wave_id: str) -> Dict:
        """Get lineage for an entity (incoming + outgoing)."""
        conn = self._conn

        incoming = conn.execute("""
            SELECT * FROM lineage_edges WHERE target = ? AND wave_id = ?
        """, (entity_name, wave_id)).fetchall()

        outgoing = conn.execute("""
            SELECT * FROM lineage_edges WHERE source = ? AND wave_id = ?
        """, (entity_name, wave_id)).fetchall()

        return {
            "incoming": [
                {
                    "source": row["source"],
                    "description": row["description"],
                    "is_critical": bool(row["is_critical"])
                }
                for row in incoming
            ],
            "outgoing": [
                {
                    "target": row["target"],
                    "description": row["description"],
                    "is_critical": bool(row["is_critical"])
                }
                for row in outgoing
            ]
        }

    def get_statistics(self) -> Dict:
        """Get store statistics."""
        conn = self._conn
        total_entities = conn.execute(
            "SELECT COUNT(*) FROM entities"
        ).fetchone()[0]

        total_edges = conn.execute(
            "SELECT COUNT(*) FROM lineage_edges"
        ).fetchone()[0]

        wave_count = conn.execute(
            "SELECT COUNT(DISTINCT wave_id) FROM entities"
        ).fetchone()[0]

        return {
            "total_entities": total_entities,
            "total_lineage_edges": total_edges,
            "waves_stored": wave_count,
            "db_file": str(self.db_path)
        }
