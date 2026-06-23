# Headroom-Migration Coordinator Adapter

**Purpose:** Shows exact code changes needed in `migration-coordinator.py` to use Headroom.

**Modified File:** `src/modules/dmf-fabric-agents/core-coordination/agents/migration-coordinator/migration-coordinator.py`

---

## Changes Summary

1. **Add imports** (Line ~30)
2. **Initialize managers** (Line ~50)
3. **Update phase transition methods** (3 methods)
4. **Add metrics endpoints** (Gate reviews)

---

## 1️⃣ Add Imports (Around Line 30)

```python
# EXISTING IMPORTS
from pathlib import Path
import json
import logging

# NEW IMPORTS FOR HEADROOM
from headroom_context_manager import HeadroomContextManager
from headroom_workflow_integration import HeadroomWorkflowIntegration
from enhanced_token_metrics import EnhancedTokenMetrics

logger = logging.getLogger(__name__)
```

---

## 2️⃣ Initialize in `__init__` (Around Line 50)

```python
class MigrationCoordinator:
    """Orchestrates DMF migration waves with compression optimization."""
    
    def __init__(self, project_root: str | None = None):
        """Initialize coordinator with Headroom support."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
        # EXISTING INITIALIZATION
        self.wave_config = None
        self.gate_scores = {}
        
        # NEW: HEADROOM INITIALIZATION
        self.headroom = HeadroomContextManager(project_root, use_mock=False)
        self.headroom_workflow = HeadroomWorkflowIntegration(project_root)
        self.token_metrics = EnhancedTokenMetrics(project_root)
        
        logger.info("✅ Headroom integration initialized")
```

---

## 3️⃣ Modify Phase Transition Methods

### Phase 1→2: After Gate 1 Approval (Upstream → Midstream)

**Current method signature:**
```python
def start_midstream(self, wave_id: str) -> bool:
```

**Replace with:**
```python
def start_midstream(self, wave_id: str) -> bool:
    """
    Start Midstream phase with token compression checkpoint.
    
    Flow: discovery-scout output → compress → data-architect input
    """
    logger.info(f"🔄 Starting MIDSTREAM for {wave_id}...")
    
    try:
        # Load upstream artifacts
        upstream_dir = self.project_root / "projects" / "clientebanco" / "outputs" / "upstream"
        discovery_outputs = self._load_json_artifacts(upstream_dir)
        
        if not discovery_outputs:
            logger.warning("⚠️  No upstream artifacts found. Skipping compression.")
            return self._invoke_data_architect(wave_id)
        
        # 🆕 COMPRESS UPSTREAM HANDOFF
        logger.info(f"📦 Compressing discovery-scout output...")
        compressed_data, compression_stats = self.headroom_workflow.compress_upstream_handoff(
            artifact_data=discovery_outputs,
            source_agent="discovery-scout",
        )
        
        # 🆕 RECORD METRICS
        self.token_metrics.add_raw_tokens(
            agent="discovery-scout",
            phase="upstream",
            wave_id=wave_id,
            tokens=compression_stats["input_tokens"],
        )
        self.token_metrics.add_compression_event(
            source_agent="discovery-scout",
            target_agent="data-architect",
            input_tokens=compression_stats["input_tokens"],
            output_tokens=compression_stats["output_tokens"],
            compression_ratio=compression_stats["compression_ratio"],
            phase="upstream",
            method=compression_stats["method"],
        )
        
        # 🆕 VALIDATE COMPRESSION
        validation = self.headroom_workflow.validate_compression_ratios("upstream")
        logger.info(f"✅ {validation['status']} - {validation['recommendation']}")
        
        # Save compressed artifact
        compressed_file = upstream_dir / f"compressed_{wave_id}_discovery.json"
        compressed_file.write_text(
            json.dumps(compressed_data, indent=2),
            encoding='utf-8'
        )
        logger.info(f"💾 Compressed artifact: {compressed_file}")
        
        # Proceed to data-architect with compressed data
        return self._invoke_data_architect(wave_id, compressed_data)
        
    except Exception as e:
        logger.error(f"❌ Midstream start failed: {e}")
        return False
```

### Phase 2→3: After Gate 2 Approval (Midstream → Downstream)

**Current method signature:**
```python
def start_downstream(self, wave_id: str) -> bool:
```

**Replace with:**
```python
def start_downstream(self, wave_id: str) -> bool:
    """
    Start Downstream phase with token compression checkpoint.
    
    Flow: code-generator output → compress → downstream-executor input
    """
    logger.info(f"🔄 Starting DOWNSTREAM for {wave_id}...")
    
    try:
        # Load midstream artifacts
        midstream_dir = self.project_root / "projects" / "clientebanco" / "outputs" / "midstream"
        codegen_outputs = self._load_json_artifacts(midstream_dir)
        
        if not codegen_outputs:
            logger.warning("⚠️  No midstream artifacts found. Skipping compression.")
            return self._invoke_downstream_executor(wave_id)
        
        # 🆕 COMPRESS MIDSTREAM HANDOFF
        logger.info(f"📦 Compressing code-generator output...")
        compressed_data, compression_stats = self.headroom_workflow.compress_midstream_handoff(
            artifact_data=codegen_outputs,
            source_agent="code-generator",
        )
        
        # 🆕 RECORD METRICS
        self.token_metrics.add_compression_event(
            source_agent="code-generator",
            target_agent="downstream-executor",
            input_tokens=compression_stats["input_tokens"],
            output_tokens=compression_stats["output_tokens"],
            compression_ratio=compression_stats["compression_ratio"],
            phase="midstream",
            method=compression_stats["method"],
        )
        
        # 🆕 VALIDATE COMPRESSION
        validation = self.headroom_workflow.validate_compression_ratios("midstream")
        logger.info(f"✅ {validation['status']} - {validation['recommendation']}")
        
        # Save compressed artifact
        compressed_file = midstream_dir / f"compressed_{wave_id}_codegen.json"
        compressed_file.write_text(json.dumps(compressed_data, indent=2))
        
        # Proceed to downstream-executor
        return self._invoke_downstream_executor(wave_id, compressed_data)
        
    except Exception as e:
        logger.error(f"❌ Downstream start failed: {e}")
        return False
```

### Phase 3→Report: After Gate 3 Approval (Downstream → Documentation)

**Current method signature:**
```python
def start_documentation(self, wave_id: str) -> bool:
```

**Replace with:**
```python
def start_documentation(self, wave_id: str) -> bool:
    """
    Start Documentation phase with final compression and metrics generation.
    
    Flow: reconciliation output → compress → documentation input
    Then generate final metrics report for dashboard.
    """
    logger.info(f"📝 Starting DOCUMENTATION for {wave_id}...")
    
    try:
        # Load downstream artifacts
        downstream_dir = self.project_root / "projects" / "clientebanco" / "outputs" / "downstream"
        recon_outputs = self._load_json_artifacts(downstream_dir)
        
        if recon_outputs:
            # 🆕 COMPRESS FINAL HANDOFF
            logger.info(f"📦 Compressing reconciliation output...")
            compressed_data, compression_stats = self.headroom_workflow.compress_downstream_handoff(
                artifact_data=recon_outputs,
                source_agent="reconciliation",
            )
            
            # 🆕 RECORD METRICS
            self.token_metrics.add_compression_event(
                source_agent="reconciliation",
                target_agent="documentation",
                input_tokens=compression_stats["input_tokens"],
                output_tokens=compression_stats["output_tokens"],
                compression_ratio=compression_stats["compression_ratio"],
                phase="downstream",
                method=compression_stats["method"],
            )
        
        # 🆕 CALCULATE FINAL COST IMPACT
        cost_analysis = self.token_metrics.calculate_cost_delta()
        logger.info(
            f"💰 Cost Analysis:\n"
            f"   Raw Cost: ${cost_analysis['raw_cost_usd']:.6f}\n"
            f"   Compressed Cost: ${cost_analysis['compressed_cost_usd']:.6f}\n"
            f"   Savings: ${cost_analysis['savings_usd']:.6f}"
        )
        
        # 🆕 SAVE HEADROOM METRICS FOR DASHBOARD
        metrics_file = downstream_dir / f"{wave_id}_headroom_metrics.json"
        self.token_metrics.save_to_file(metrics_file)
        logger.info(f"📊 Headroom metrics saved: {metrics_file}")
        
        # 🆕 SAVE WORKFLOW STATUS
        workflow_status = self.headroom_workflow.get_workflow_status()
        status_file = downstream_dir / f"{wave_id}_headroom_workflow.json"
        status_file.write_text(json.dumps(workflow_status, indent=2))
        logger.info(f"🔄 Workflow status saved: {status_file}")
        
        # Proceed to documentation
        return self._invoke_documentation_agent(wave_id)
        
    except Exception as e:
        logger.error(f"❌ Documentation start failed: {e}")
        return False
```

---

## 4️⃣ Add Headroom Status Endpoint (For Gate Reviews)

**Add these methods to MigrationCoordinator:**

```python
def get_headroom_status(self, wave_id: str) -> dict:
    """Get current Headroom compression status for a wave."""
    return self.headroom_workflow.get_workflow_status()

def validate_compression_for_gate(self, phase: str) -> dict:
    """Validate compression meets gate requirements."""
    return self.headroom_workflow.validate_compression_ratios(phase)

def get_cost_savings_report(self) -> dict:
    """Get cost savings report for stakeholders."""
    summary = self.token_metrics.get_summary_for_dashboard()
    return {
        "tokens_raw": summary["raw_tokens_total"],
        "tokens_saved": summary["tokens_saved"],
        "compression_pct": summary["compression_pct"],
        "cost_raw_usd": summary["cost_raw_usd"],
        "cost_compressed_usd": summary["cost_compressed_usd"],
        "cost_savings_usd": summary["cost_savings_usd"],
        "cost_savings_pct": summary.get("cost_savings_pct", 0),
    }
```

---

## 5️⃣ Helper Methods (Add to MigrationCoordinator)

```python
def _load_json_artifacts(self, directory: Path) -> dict | None:
    """Load all JSON artifacts from a directory."""
    try:
        artifacts = {}
        for json_file in directory.glob("*.json"):
            key = json_file.stem
            artifacts[key] = json.loads(json_file.read_text(encoding='utf-8'))
        return artifacts if artifacts else None
    except Exception as e:
        logger.warning(f"Failed to load artifacts from {directory}: {e}")
        return None

def _invoke_data_architect(self, wave_id: str, compressed_data: str | None = None) -> bool:
    """Invoke data-architect agent for Midstream."""
    logger.info("🧭 Routing to data-architect...")
    # Existing implementation
    # If compressed_data provided, pass it as context
    pass

def _invoke_downstream_executor(self, wave_id: str, compressed_data: str | None = None) -> bool:
    """Invoke downstream-executor agent."""
    logger.info("🧭 Routing to downstream-executor...")
    # Existing implementation
    pass

def _invoke_documentation_agent(self, wave_id: str) -> bool:
    """Invoke documentation agent for final reporting."""
    logger.info("🧭 Routing to documentation...")
    # Existing implementation
    pass
```

---

## 📊 Dashboard Integration Point

**Add to `dashboard_server.py` (Line ~80):**

```python
from enhanced_token_metrics import EnhancedTokenMetrics

@app.route("/api/headroom/<wave_id>")
def get_headroom_metrics(wave_id: str):
    """Serve Headroom metrics for dashboard."""
    metrics_file = Path(f"projects/clientebanco/outputs/downstream/{wave_id}_headroom_metrics.json")
    
    if metrics_file.exists():
        data = json.loads(metrics_file.read_text())
        return json.jsonify(data)
    
    return json.jsonify({"error": "No metrics found"}), 404

@app.route("/dashboard/headroom")
def headroom_dashboard():
    """Display Headroom optimization dashboard."""
    return render_template("headroom-dashboard.html")
```

---

## ✅ Validation Checklist

- [ ] Imports added successfully
- [ ] HeadroomContextManager initializes without errors
- [ ] `start_midstream()` compresses and records metrics
- [ ] `start_downstream()` compresses and validates
- [ ] `start_documentation()` calculates cost delta
- [ ] Metrics JSON files generated
- [ ] Dashboard receives metrics via `/api/headroom/<wave_id>`
- [ ] Tests pass: `pytest src/shared/tests/test_headroom_integration.py`

---

## 🚀 Deployment Steps

1. **Backup current migration-coordinator.py**
   ```bash
   cp migration-coordinator.py migration-coordinator.py.bak
   ```

2. **Apply changes** (use the code snippets above)

3. **Test with PoC data**
   ```bash
   python -m src.shared.scripts.headroom_poc --input test-data/test-schema-large.json
   ```

4. **Run integration tests**
   ```bash
   pytest src/shared/tests/test_headroom_integration.py -v
   ```

5. **Deploy to ClienteBanco WAVE-001**
   ```bash
   # After successful testing
   python src/shared/scripts/validate_gate3_artifacts.py projects/clientebanco/outputs/downstream
   ```

---

**Status:** 🟢 **Ready for Implementation (2026-06-22)**
