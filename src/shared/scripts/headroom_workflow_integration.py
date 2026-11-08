#!/usr/bin/env python3
"""
Headroom Workflow Integration Module
Demonstrates and manages Headroom integration into DMF Phase 1 workflow.

**Integration Points:**
1. migration-coordinator.py - calls compress_handoff before agent transitions
2. token_metrics_collector.py - captures compression metrics  
3. dashboard_server.py - displays Headroom widget with live metrics
4. validate_gate{N}_artifacts.py - validates compression ratios meet thresholds

**Timeline:** Phase 1 starts 2026-06-22 (8 weeks, 32 hours)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

try:
    from .headroom_context_manager import HeadroomContextManager
except ImportError:  # executed as a plain script
    from headroom_context_manager import HeadroomContextManager


class HeadroomWorkflowIntegration:
    """
    Bridge between Headroom and DMF agents.
    Manages compression checkpoints at each gate.
    """
    
    def __init__(self, project_root: str | None = None):
        """Initialize workflow integration."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.headroom = HeadroomContextManager(project_root, use_mock=False)
        
        # Track compression by phase
        self.phase_compression = {
            "upstream": {"compressed": False, "ratio": 0},
            "midstream": {"compressed": False, "ratio": 0},
            "downstream": {"compressed": False, "ratio": 0},
        }

    def compress_upstream_handoff(
        self, artifact_data: dict | str, source_agent: str
    ) -> tuple[str, Dict[str, Any]]:
        """
        Compress artifact at end of Upstream phase.
        
        Handoff: discovery-scout → data-architect
        """
        compressed, stats = self.headroom.compress_handoff(
            data=artifact_data,
            source_agent=source_agent,
            target_agent="data-architect",  # Entry to midstream
        )
        
        self.phase_compression["upstream"]["compressed"] = True
        self.phase_compression["upstream"]["ratio"] = stats.compression_ratio
        
        return compressed, stats.to_dict()

    def compress_midstream_handoff(
        self, artifact_data: dict | str, source_agent: str
    ) -> tuple[str, Dict[str, Any]]:
        """
        Compress artifact at end of Midstream phase.
        
        Handoff: code-generator → downstream-executor
        """
        compressed, stats = self.headroom.compress_handoff(
            data=artifact_data,
            source_agent=source_agent,
            target_agent="downstream-executor",  # Entry to downstream
        )
        
        self.phase_compression["midstream"]["compressed"] = True
        self.phase_compression["midstream"]["ratio"] = stats.compression_ratio
        
        return compressed, stats.to_dict()

    def compress_downstream_handoff(
        self, artifact_data: dict | str, source_agent: str
    ) -> tuple[str, Dict[str, Any]]:
        """
        Compress artifact at end of Downstream phase.
        
        Handoff: reconciliation → documentation
        """
        compressed, stats = self.headroom.compress_handoff(
            data=artifact_data,
            source_agent=source_agent,
            target_agent="documentation",  # Final reporting
        )
        
        self.phase_compression["downstream"]["compressed"] = True
        self.phase_compression["downstream"]["ratio"] = stats.compression_ratio
        
        return compressed, stats.to_dict()

    def validate_compression_ratios(self, phase: str) -> Dict[str, Any]:
        """
        Validate that compression meets phase requirements.
        
        Thresholds (from HEADROOM-POC-DECISION.md):
        - upstream/midstream: >= 30% (30-70% acceptable)
        - downstream: >= 20% (more I/O intensive)
        """
        thresholds = {
            "upstream": 0.30,
            "midstream": 0.30,
            "downstream": 0.20,
        }
        
        actual_ratio = self.phase_compression[phase]["ratio"]
        threshold = thresholds[phase]
        
        passed = actual_ratio >= threshold
        
        return {
            "phase": phase,
            "compression_ratio": actual_ratio,
            "threshold": threshold,
            "passed": passed,
            "status": "🟢 PASS" if passed else "🔴 FAIL",
            "recommendation": (
                f"✅ Exceeds {phase} threshold of {threshold*100:.0f}%"
                if passed
                else f"⚠️  Below {phase} threshold of {threshold*100:.0f}%. "
                     f"Consider optimizing artifacts."
            ),
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get comprehensive workflow integration status."""
        headroom_stats = self.headroom.get_stats()
        
        return {
            "integration_status": "🟢 Active" if self.headroom.headroom_available else "🟡 Mock Mode",
            "method": "headroom" if self.headroom.headroom_available else "mock-estimator",
            "phase_compression": self.phase_compression,
            "phase_validations": {
                phase: self.validate_compression_ratios(phase)
                for phase in ["upstream", "midstream", "downstream"]
            },
            "cumulative_stats": headroom_stats,
            "timestamp": datetime.now().isoformat(),
        }

    def save_workflow_metrics(self, output_file: str | Path):
        """Save complete workflow metrics for dashboard."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        metrics = self.get_workflow_status()
        output_path.write_text(json.dumps(metrics, indent=2))
        
        print(f"📊 Workflow metrics saved to {output_path}")
        return metrics


# Integration patterns for migration-coordinator

MIGRATION_COORDINATOR_PATTERN = """
# Example: integration in migration-coordinator.py

from headroom_context_manager import HeadroomContextManager

class MigrationCoordinator:
    def __init__(self):
        self.headroom = HeadroomContextManager()
    
    def start_midstream(self, wave_id: str):
        '''Start midstream phase with compression checkpoints.'''
        
        # After discovery-scout completes, compress handoff
        discovery_artifacts = self.load_upstream_outputs(wave_id)
        compressed, stats = self.headroom.compress_handoff(
            data=discovery_artifacts,
            source_agent="discovery-scout",
            target_agent="data-architect",
        )
        
        # Log to token metrics
        self.token_metrics.add_compression(wave_id, stats)
        
        # Validate compression
        if stats.compression_ratio < 0.30:
            logger.warning(f"⚠️  Low compression ratio: {stats.compression_ratio*100:.1f}%")
        
        # Save compressed artifact
        self.save_artifact(wave_id, "compressed-discovery", compressed)
        
        # Proceed to midstream
        return self.start_data_architect(wave_id, compressed)
"""

DASHBOARD_WIDGET_PATTERN = """
<!-- Headroom Metrics Widget (for dashboard_server.py) -->

<div class="headroom-widget">
    <h3>🎯 Token Optimization (Headroom)</h3>
    
    <div class="metrics-grid">
        <div class="metric">
            <label>Avg Compression</label>
            <value class="headroom-compression">87.5%</value>
        </div>
        <div class="metric">
            <label>Tokens Saved (Wave)</label>
            <value class="headroom-tokens-saved">114,457</value>
        </div>
        <div class="metric">
            <label>Cost Avoided (USD)</label>
            <value class="headroom-cost">$0.34</value>
        </div>
        <div class="metric">
            <label>Status</label>
            <value class="headroom-status">🟢 Active</value>
        </div>
    </div>
    
    <div class="phase-breakdown">
        <h4>By Phase</h4>
        <ul>
            <li>Upstream: <strong>50%</strong> compression</li>
            <li>Midstream: <strong>60%</strong> compression</li>
            <li>Downstream: <strong>40%</strong> compression</li>
        </ul>
    </div>
</div>

<style>
.headroom-widget {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 8px;
    color: white;
}
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 15px 0;
}
.metric {
    background: rgba(255,255,255,0.1);
    padding: 12px;
    border-radius: 6px;
}
.metric value {
    font-size: 1.8em;
    font-weight: bold;
    display: block;
}
</style>
"""

if __name__ == "__main__":
    # Example usage
    integration = HeadroomWorkflowIntegration()
    
    # Simulate upstream completion and handoff
    upstream_data = {"entities": 45, "metrics": 1200}
    compressed, stats = integration.compress_upstream_handoff(upstream_data, "discovery-scout")
    
    print(f"✅ Upstream compression: {stats['compression_ratio']*100:.1f}%")
    print(f"✅ Tokens saved: {stats['tokens_saved']:,}")
    
    # Get full workflow status
    status = integration.get_workflow_status()
    print(f"\n📊 Workflow Status:\n{json.dumps(status, indent=2)}")
    
    # Save to file for dashboard
    integration.save_workflow_metrics("projects/bradesco/outputs/headroom-metrics.json")
