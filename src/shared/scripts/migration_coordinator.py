#!/usr/bin/env python3
"""
Migration Coordinator — Python orchestration layer for DMF wave execution.

Manages the three-phase migration lifecycle (Upstream → Midstream → Downstream)
with Headroom token compression at each gate transition.

Gate transitions:
  Gate 1 (after Upstream)   → compress before Midstream
  Gate 2 (after Midstream)  → compress before Downstream
  Gate 3 (after Downstream) → compress before Documentation
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Path bootstrap so scripts can import sibling modules without install
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from headroom_context_manager import HeadroomContextManager  # noqa: E402
from headroom_workflow_integration import HeadroomWorkflowIntegration  # noqa: E402
from enhanced_token_metrics import EnhancedTokenMetrics  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


class MigrationCoordinator:
    """
    Orchestrate DMF migration waves with Headroom compression checkpoints.

    Usage
    -----
    >>> coordinator = MigrationCoordinator(project_root=".", project_name="Financeiro")
    >>> coordinator.start_midstream("wave-1")
    >>> coordinator.start_downstream("wave-1")
    >>> coordinator.start_documentation("wave-1")
    >>> report = coordinator.get_cost_savings_report()
    """

    def __init__(
        self,
        project_root: str | Path | None = None,
        project_name: str = "Financeiro",
        use_mock: bool = False,
    ) -> None:
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.project_name = project_name
        self.wave_config: dict | None = None
        self.gate_scores: Dict[str, float] = {}

        # Headroom initialisation
        self.headroom = HeadroomContextManager(
            str(self.project_root), use_mock=use_mock
        )
        self.headroom_workflow = HeadroomWorkflowIntegration(str(self.project_root))
        self.token_metrics = EnhancedTokenMetrics(str(self.project_root))

        logger.info("✅ MigrationCoordinator initialised (project=%s)", project_name)

    # ------------------------------------------------------------------
    # Gate 1 → Gate 2 transition: Upstream → Midstream
    # ------------------------------------------------------------------

    def start_midstream(self, wave_id: str) -> bool:
        """
        Transition to Midstream after Gate 1 approval.

        Flow: discovery-scout artifacts → [compress] → data-architect context
        """
        logger.info("🔄 Starting MIDSTREAM for %s …", wave_id)
        upstream_dir = self._outputs_dir("upstream")

        try:
            artifacts = self._load_json_artifacts(upstream_dir)

            if not artifacts:
                logger.warning("⚠️  No upstream artifacts found — skipping compression.")
                return True

            compressed, stats = self.headroom_workflow.compress_upstream_handoff(
                artifact_data=artifacts,
                source_agent="discovery-scout",
            )

            self.token_metrics.add_raw_tokens(
                agent="discovery-scout",
                phase="upstream",
                wave_id=wave_id,
                tokens=stats["input_tokens"],
            )
            self.token_metrics.add_compression_event(
                source_agent="discovery-scout",
                target_agent="data-architect",
                input_tokens=stats["input_tokens"],
                output_tokens=stats["output_tokens"],
                compression_ratio=stats["compression_ratio"],
                phase="upstream",
                method=stats["method"],
            )

            validation = self.headroom_workflow.validate_compression_ratios("upstream")
            logger.info("Compression: %s — %s", validation["status"], validation["recommendation"])

            compressed_file = upstream_dir / f"compressed_{wave_id}_discovery.json"
            compressed_file.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(compressed, dict):
                compressed_file.write_text(json.dumps(compressed, indent=2), encoding="utf-8")
            else:
                compressed_file.write_text(str(compressed), encoding="utf-8")
            logger.info("💾 Compressed artifact saved: %s", compressed_file)

            return True

        except Exception as exc:
            logger.error("❌ start_midstream failed: %s", exc)
            return False

    # ------------------------------------------------------------------
    # Gate 2 → Gate 3 transition: Midstream → Downstream
    # ------------------------------------------------------------------

    def start_downstream(self, wave_id: str) -> bool:
        """
        Transition to Downstream after Gate 2 approval.

        Flow: code-generator artifacts → [compress] → downstream-executor context
        """
        logger.info("🔄 Starting DOWNSTREAM for %s …", wave_id)
        midstream_dir = self._outputs_dir("midstream")

        try:
            artifacts = self._load_json_artifacts(midstream_dir)

            if not artifacts:
                logger.warning("⚠️  No midstream artifacts found — skipping compression.")
                return True

            compressed, stats = self.headroom_workflow.compress_midstream_handoff(
                artifact_data=artifacts,
                source_agent="code-generator",
            )

            self.token_metrics.add_raw_tokens(
                agent="code-generator",
                phase="midstream",
                wave_id=wave_id,
                tokens=stats["input_tokens"],
            )
            self.token_metrics.add_compression_event(
                source_agent="code-generator",
                target_agent="downstream-executor",
                input_tokens=stats["input_tokens"],
                output_tokens=stats["output_tokens"],
                compression_ratio=stats["compression_ratio"],
                phase="midstream",
                method=stats["method"],
            )

            validation = self.headroom_workflow.validate_compression_ratios("midstream")
            logger.info("Compression: %s — %s", validation["status"], validation["recommendation"])

            compressed_file = midstream_dir / f"compressed_{wave_id}_codegen.json"
            compressed_file.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(compressed, dict):
                compressed_file.write_text(json.dumps(compressed, indent=2), encoding="utf-8")
            else:
                compressed_file.write_text(str(compressed), encoding="utf-8")
            logger.info("💾 Compressed artifact saved: %s", compressed_file)

            return True

        except Exception as exc:
            logger.error("❌ start_downstream failed: %s", exc)
            return False

    # ------------------------------------------------------------------
    # Gate 3 → Documentation: Downstream → Documentation
    # ------------------------------------------------------------------

    def start_documentation(self, wave_id: str) -> bool:
        """
        Transition to Documentation after Gate 3 approval.

        Flow: reconciliation artifacts → [compress] → documentation agent context
              Then generate final Headroom metrics report.
        """
        logger.info("📝 Starting DOCUMENTATION for %s …", wave_id)
        downstream_dir = self._outputs_dir("downstream")

        try:
            artifacts = self._load_json_artifacts(downstream_dir)

            if artifacts:
                compressed, stats = self.headroom_workflow.compress_downstream_handoff(
                    artifact_data=artifacts,
                    source_agent="reconciliation",
                )
                self.token_metrics.add_compression_event(
                    source_agent="reconciliation",
                    target_agent="documentation",
                    input_tokens=stats["input_tokens"],
                    output_tokens=stats["output_tokens"],
                    compression_ratio=stats["compression_ratio"],
                    phase="downstream",
                    method=stats["method"],
                )

                validation = self.headroom_workflow.validate_compression_ratios("downstream")
                logger.info(
                    "Compression: %s — %s", validation["status"], validation["recommendation"]
                )

            # Final cost impact
            cost = self.token_metrics.calculate_cost_delta()
            logger.info(
                "💰 Cost Analysis → raw: $%.6f | compressed: $%.6f | saved: $%.6f",
                cost["raw_cost_usd"],
                cost["compressed_cost_usd"],
                cost["savings_usd"],
            )

            # Persist metrics
            metrics_file = downstream_dir / f"{wave_id}_headroom_metrics.json"
            metrics_file.parent.mkdir(parents=True, exist_ok=True)
            self.token_metrics.save_to_file(metrics_file)
            logger.info("📊 Headroom metrics saved: %s", metrics_file)

            workflow_status = self.headroom_workflow.get_workflow_status()
            status_file = downstream_dir / f"{wave_id}_headroom_workflow.json"
            status_file.write_text(json.dumps(workflow_status, indent=2), encoding="utf-8")
            logger.info("🔄 Workflow status saved: %s", status_file)

            return True

        except Exception as exc:
            logger.error("❌ start_documentation failed: %s", exc)
            return False

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    def get_headroom_status(self, wave_id: str) -> dict:
        """Return current Headroom compression status for a wave."""
        return self.headroom_workflow.get_workflow_status()

    def validate_compression_for_gate(self, phase: str) -> dict:
        """Validate compression meets the gate threshold."""
        return self.headroom_workflow.validate_compression_ratios(phase)

    def get_cost_savings_report(self) -> dict:
        """Return cost savings summary suitable for stakeholder reporting."""
        summary = self.token_metrics.get_summary_for_dashboard()
        return {
            "tokens_raw": summary.get("raw_tokens_total", 0),
            "tokens_saved": summary.get("tokens_saved", 0),
            "compression_pct": summary.get("compression_pct", 0.0),
            "cost_raw_usd": summary.get("cost_raw_usd", 0.0),
            "cost_compressed_usd": summary.get("cost_compressed_usd", 0.0),
            "cost_savings_usd": summary.get("cost_savings_usd", 0.0),
            "cost_savings_pct": summary.get("cost_savings_pct", 0.0),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _outputs_dir(self, phase: str) -> Path:
        return self.project_root / "projects" / self.project_name / "outputs" / phase

    def _load_json_artifacts(self, directory: Path) -> dict | None:
        """Load all *.json files from *directory* into a single dict keyed by stem."""
        if not directory.exists():
            logger.debug("Artifact directory not found: %s", directory)
            return None
        artifacts: dict = {}
        for json_file in sorted(directory.glob("*.json")):
            try:
                artifacts[json_file.stem] = json.loads(
                    json_file.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError as exc:
                logger.warning("Skipping malformed JSON %s: %s", json_file.name, exc)
        return artifacts or None


# ---------------------------------------------------------------------------
# CLI entry point — convenience for manual validation / CI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run Headroom compression checkpoints for a migration wave."
    )
    parser.add_argument("--project-root", default=".", help="Workspace root path")
    parser.add_argument("--project-name", default="Financeiro", help="Project folder name")
    parser.add_argument("--wave-id", required=True, help="Wave identifier (e.g. wave-1)")
    parser.add_argument(
        "--phase",
        choices=["midstream", "downstream", "documentation", "all"],
        default="all",
        help="Phase to run compression for",
    )
    parser.add_argument("--mock", action="store_true", help="Force mock compression mode")
    args = parser.parse_args(argv)

    coordinator = MigrationCoordinator(
        project_root=args.project_root,
        project_name=args.project_name,
        use_mock=args.mock,
    )

    results: Dict[str, bool] = {}
    if args.phase in ("midstream", "all"):
        results["midstream"] = coordinator.start_midstream(args.wave_id)
    if args.phase in ("downstream", "all"):
        results["downstream"] = coordinator.start_downstream(args.wave_id)
    if args.phase in ("documentation", "all"):
        results["documentation"] = coordinator.start_documentation(args.wave_id)

    report = coordinator.get_cost_savings_report()
    print(json.dumps({"phases": results, "cost_savings": report}, indent=2))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
