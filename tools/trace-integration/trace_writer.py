#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Trace Writer — Integration Layer for Financeiro Pipeline
Writes real-time traces to .trace-logs in JSONL format
Connects pipeline execution to observability system
"""

import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
import threading
from typing import Any, Dict, Optional, List
import sys


class TraceWriter:
    """
    Write traces to .trace-logs directory structure
    Handles JSONL append, validation, auto-organization by type
    """
    
    def __init__(self, trace_logs_root: Path = None):
        """Initialize trace writer with .trace-logs directory"""
        if trace_logs_root is None:
            # Find .trace-logs from current directory
            current = Path.cwd()
            for parent in [current] + list(current.parents):
                trace_root = parent / '.trace-logs'
                if trace_root.exists():
                    trace_logs_root = trace_root
                    break
            
            if trace_logs_root is None:
                trace_logs_root = current / '.trace-logs'
                trace_logs_root.mkdir(parents=True, exist_ok=True)
        
        self.trace_logs_root = Path(trace_logs_root)
        self._lock = threading.Lock()
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create required subdirectories"""
        subdirs = ['agents', 'workflows', 'etl', 'gates', 'migrations', 'analytics']
        for subdir in subdirs:
            (self.trace_logs_root / subdir).mkdir(parents=True, exist_ok=True)
    
    def _get_trace_id(self) -> str:
        """Generate unique trace ID (UUID v4 with tr_ prefix)"""
        return f"tr_{uuid.uuid4()}"
    
    def _get_timestamp(self) -> str:
        """Get ISO 8601 timestamp with UTC timezone"""
        return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
    
    def _validate_trace(self, trace: Dict[str, Any]) -> List[str]:
        """Validate trace against schema"""
        errors = []
        
        # Required fields
        required = ['timestamp', 'trace_id', 'trace_type', 'context', 'operation']
        for field in required:
            if field not in trace:
                errors.append(f"Missing required field: {field}")
        
        # Validate trace_id format
        if 'trace_id' in trace:
            if not trace['trace_id'].startswith('tr_'):
                errors.append("trace_id must start with 'tr_'")
        
        # Validate trace_type
        valid_types = ['agent_execution', 'workflow_execution', 'etl_operation', 
                       'gate_scoring', 'migration_event', 'performance_metric', 
                       'error_event', 'custom']
        if 'trace_type' in trace:
            if trace['trace_type'] not in valid_types:
                errors.append(f"Invalid trace_type: {trace['trace_type']}")
        
        # Validate operation status
        if 'operation' in trace:
            valid_statuses = ['success', 'failure', 'partial', 'timeout', 'pending']
            if 'status' in trace['operation']:
                if trace['operation']['status'] not in valid_statuses:
                    errors.append(f"Invalid operation status: {trace['operation']['status']}")
        
        return errors
    
    def _get_file_path(self, category: str, trace_type: str, wave: str = None) -> Path:
        """Get output file path based on category and wave"""
        # Map trace_type to category and directory
        category_map = {
            'agent_execution': 'agents',
            'workflow_execution': 'workflows',
            'etl_operation': 'etl',
            'gate_scoring': 'gates',
            'migration_event': 'migrations',
            'performance_metric': 'analytics',
            'error_event': 'agents',
            'custom': 'analytics'
        }
        
        subdir = category_map.get(trace_type, 'analytics')
        trace_dir = self.trace_logs_root / subdir
        trace_dir.mkdir(parents=True, exist_ok=True)
        
        # Filename: {trace_type}_{context}_{date}_{sequence}.jsonl
        today = datetime.now().strftime('%Y-%m-%d')
        wave_str = f"{wave}" if wave else "generic"
        filename = f"{trace_type}_{wave_str}_{today}_001.jsonl"
        
        return trace_dir / filename
    
    def write_trace(self, 
                   trace_type: str,
                   context: Dict[str, Any],
                   operation: Dict[str, Any],
                   metrics: Optional[Dict[str, Any]] = None,
                   metadata: Optional[Dict[str, Any]] = None,
                   tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Write a trace event to JSONL file
        
        Args:
            trace_type: Type of trace (agent_execution, etl_operation, etc.)
            context: Context dict with category, agent_id, wave, gate, user, etc.
            operation: Operation dict with name, duration_sec, status, error
            metrics: Optional metrics dict (tokens, cost, rows, etc.)
            metadata: Optional metadata dict (source, version, environment)
            tags: Optional list of tags
        
        Returns:
            Complete trace dict that was written
        """
        
        # Build trace
        trace = {
            'timestamp': self._get_timestamp(),
            'trace_id': self._get_trace_id(),
            'trace_type': trace_type,
            'context': context,
            'operation': operation,
        }
        
        if metrics:
            trace['metrics'] = metrics
        
        if metadata:
            trace['metadata'] = metadata
        
        if tags:
            trace['tags'] = tags
        
        # Validate
        errors = self._validate_trace(trace)
        if errors:
            print(f"❌ Trace validation errors: {errors}", file=sys.stderr)
            return None
        
        # Get file path
        wave = context.get('wave', 'generic')
        file_path = self._get_file_path(context.get('category', 'agents'), trace_type, wave)
        
        # Write to file (thread-safe)
        with self._lock:
            try:
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(trace) + '\n')
            except Exception as e:
                print(f"❌ Error writing trace: {e}", file=sys.stderr)
                return None
        
        return trace
    
    def write_agent_execution(self, 
                             agent_id: str,
                             wave: str,
                             gate: int,
                             operation_name: str,
                             duration_sec: float,
                             status: str = 'success',
                             tokens_in: int = 0,
                             tokens_out: int = 0,
                             cost_usd: float = 0.0,
                             artifacts_generated: int = 0,
                             error: str = None,
                             user: str = 'system'):
        """Write agent_execution trace"""
        return self.write_trace(
            trace_type='agent_execution',
            context={
                'category': 'agents',
                'agent_id': agent_id,
                'wave': wave,
                'gate': gate,
                'user': user,
                'tags': ['critical', f'gate-{gate}-validation']
            },
            operation={
                'name': operation_name,
                'duration_sec': duration_sec,
                'status': status,
                'error': error
            },
            metrics={
                'tokens_in': tokens_in,
                'tokens_out': tokens_out,
                'cost_usd': cost_usd,
                'artifacts_generated': artifacts_generated
            },
            metadata={
                'source': f'{agent_id}.py',
                'version': '1.0.0',
                'environment': 'production'
            }
        )
    
    def write_etl_operation(self,
                           pipeline: str,
                           wave: str,
                           operation_name: str,
                           duration_sec: float,
                           rows_processed: int,
                           rows_failed: int = 0,
                           status: str = 'success',
                           error: str = None):
        """Write etl_operation trace"""
        error_rate = rows_failed / rows_processed if rows_processed > 0 else 0.0
        throughput = rows_processed / duration_sec if duration_sec > 0 else 0.0
        
        return self.write_trace(
            trace_type='etl_operation',
            context={
                'category': 'etl',
                'pipeline': pipeline,
                'wave': wave
            },
            operation={
                'name': operation_name,
                'duration_sec': duration_sec,
                'status': status,
                'error': error
            },
            metrics={
                'rows_processed': rows_processed,
                'rows_failed': rows_failed,
                'error_rate': error_rate,
                'throughput': throughput
            },
            metadata={
                'source': f'etl-runner.py',
                'version': '1.0.0'
            }
        )
    
    def write_gate_scoring(self,
                          gate: int,
                          wave: str,
                          duration_sec: float,
                          artifacts_evaluated: int,
                          base_score: float,
                          final_score: float,
                          anti_patterns_detected: int = 0,
                          score_adjustment: float = 0.0):
        """Write gate_scoring trace"""
        return self.write_trace(
            trace_type='gate_scoring',
            context={
                'category': 'gates',
                'gate': gate,
                'wave': wave,
                'tags': ['validation', 'auto-adjustment']
            },
            operation={
                'name': 'calculate_gatescore',
                'duration_sec': duration_sec,
                'status': 'success'
            },
            metrics={
                'artifacts_evaluated': artifacts_evaluated,
                'base_score': base_score,
                'score_adjustment': score_adjustment,
                'final_score': final_score,
                'anti_patterns_detected': anti_patterns_detected
            },
            metadata={
                'source': 'quality-gate.py',
                'version': '1.0.0'
            }
        )
    
    def write_migration_event(self,
                             wave: str,
                             gate: int,
                             entities_total: int,
                             entities_mapped: int,
                             duration_sec: float,
                             status: str = 'success'):
        """Write migration_event trace"""
        coverage_pct = (entities_mapped / entities_total * 100) if entities_total > 0 else 0.0
        
        return self.write_trace(
            trace_type='migration_event',
            context={
                'category': 'migrations',
                'wave': wave,
                'gate': gate,
                'tags': ['entity-coverage']
            },
            operation={
                'name': 'validate_entities',
                'duration_sec': duration_sec,
                'status': status
            },
            metrics={
                'entities_total': entities_total,
                'entities_mapped': entities_mapped,
                'coverage_pct': coverage_pct
            },
            metadata={
                'source': 'inventory-scout.py',
                'version': '1.0.0'
            }
        )
    
    def write_workflow_execution(self,
                                pipeline: str,
                                wave: str,
                                operation_name: str,
                                duration_sec: float,
                                decision: str,
                                artifacts_generated: int = 0):
        """Write workflow_execution trace"""
        return self.write_trace(
            trace_type='workflow_execution',
            context={
                'category': 'workflows',
                'pipeline': pipeline,
                'wave': wave
            },
            operation={
                'name': operation_name,
                'duration_sec': duration_sec,
                'status': 'success'
            },
            metrics={
                'decision': decision,
                'artifacts_generated': artifacts_generated
            },
            metadata={
                'source': 'workflow-orchestrator.py',
                'version': '1.0.0'
            }
        )


# Singleton instance
_trace_writer = None

def get_trace_writer() -> TraceWriter:
    """Get or create singleton trace writer"""
    global _trace_writer
    if _trace_writer is None:
        _trace_writer = TraceWriter()
    return _trace_writer


def write_trace(trace_type: str, context: Dict, operation: Dict, 
                metrics: Dict = None, metadata: Dict = None, tags: List = None):
    """Convenience function to write a trace using singleton"""
    writer = get_trace_writer()
    return writer.write_trace(trace_type, context, operation, metrics, metadata, tags)


def write_agent_execution_trace(agent_id: str, wave: str, gate: int, operation_name: str,
                                duration_sec: float, status: str = 'success',
                                tokens_in: int = 0, tokens_out: int = 0,
                                cost_usd: float = 0.0, artifacts_generated: int = 0,
                                error: str = None):
    """Convenience function for agent execution traces"""
    writer = get_trace_writer()
    return writer.write_agent_execution(
        agent_id, wave, gate, operation_name, duration_sec, status,
        tokens_in, tokens_out, cost_usd, artifacts_generated, error
    )


if __name__ == '__main__':
    # Test the trace writer
    print("🧪 Testing Trace Writer...")
    
    writer = TraceWriter()
    
    # Test agent execution trace
    trace1 = writer.write_agent_execution(
        agent_id='migration-coordinator',
        wave='financeiro-wave2',
        gate=1,
        operation_name='spawn_agent',
        duration_sec=45.23,
        tokens_in=2048,
        tokens_out=1024,
        cost_usd=0.15,
        artifacts_generated=3
    )
    print(f"✅ Agent execution trace: {trace1['trace_id']}")
    
    # Test ETL operation trace
    trace2 = writer.write_etl_operation(
        pipeline='staging-to-delta',
        wave='financeiro-wave2',
        operation_name='load_entities',
        duration_sec=30.2,
        rows_processed=15000
    )
    print(f"✅ ETL operation trace: {trace2['trace_id']}")
    
    # Test gate scoring trace
    trace3 = writer.write_gate_scoring(
        gate=1,
        wave='financeiro-wave2',
        duration_sec=12.5,
        artifacts_evaluated=5,
        base_score=0.88,
        final_score=0.83,
        anti_patterns_detected=2,
        score_adjustment=-0.05
    )
    print(f"✅ Gate scoring trace: {trace3['trace_id']}")
    
    print(f"\n✅ All traces written to: {writer.trace_logs_root}")
