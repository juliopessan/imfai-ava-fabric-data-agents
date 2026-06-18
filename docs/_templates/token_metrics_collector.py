#!/usr/bin/env python3
"""
Token Metrics Collector
Extracts token usage metrics from migration logs and agent outputs.
Aggregates by agent, phase, and wave for reporting.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class TokenMetricsCollector:
    """Collect and aggregate token usage metrics from DMF execution."""

    def __init__(self, project_root: str | None = None):
        """Initialize collector with optional project root."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.metrics: Dict[str, Any] = {
            "by_agent": {},
            "by_phase": {},
            "by_wave": {},
            "by_section": {},
            "total": 0,
            "timestamp": datetime.now().isoformat(),
        }

    def collect_from_artifacts(self, wave_dir: str) -> Dict[str, Any]:
        """Collect token metrics from wave artifact outputs."""
        wave_path = Path(wave_dir)
        if not wave_path.exists():
            return self.metrics

        # Scan for token_usage.json files in outputs
        for token_file in wave_path.glob("**/token_usage.json"):
            self._parse_token_file(token_file)

        # Estimate from artifact sizes (fallback)
        self._estimate_from_artifacts(wave_path)

        return self.metrics

    def _parse_token_file(self, file_path: Path):
        """Parse token_usage.json from agent output."""
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))

            # Update agent metrics
            agent = data.get("agent", "unknown")
            tokens = data.get("tokens_used", 0)
            phase = data.get("phase", "unknown")

            if agent not in self.metrics["by_agent"]:
                self.metrics["by_agent"][agent] = {"tokens": 0, "calls": 0, "phase": phase}

            self.metrics["by_agent"][agent]["tokens"] += tokens
            self.metrics["by_agent"][agent]["calls"] += 1
            self.metrics["total"] += tokens

            # Update phase metrics
            if phase not in self.metrics["by_phase"]:
                self.metrics["by_phase"][phase] = 0
            self.metrics["by_phase"][phase] += tokens

        except Exception as e:
            print(f"⚠️  Failed to parse {file_path}: {e}")

    def _estimate_from_artifacts(self, wave_path: Path):
        """Estimate tokens from artifact file sizes (rough heuristic)."""
        # Heuristic: ~1 token ≈ 4 chars (token estimation)
        phase_map = {
            "upstream": ["discovery", "strategy", "sttm"],
            "midstream": ["architecture", "model", "governance", "code"],
            "downstream": ["execution", "reconciliation", "healing"],
        }

        for artifact in wave_path.glob("**/*.md"):
            if artifact.name.startswith("token_"):
                continue

            size_bytes = artifact.stat().st_size
            estimated_tokens = int(size_bytes / 4)  # Rough heuristic

            # Infer phase from path
            phase = "unknown"
            for p, keywords in phase_map.items():
                if any(k in artifact.parts[-1].lower() for k in keywords):
                    phase = p
                    break

            # Add to section metrics
            section = artifact.stem
            if section not in self.metrics["by_section"]:
                self.metrics["by_section"][section] = {"tokens": 0, "phase": phase}

            self.metrics["by_section"][section]["tokens"] += estimated_tokens
            self.metrics["total"] += estimated_tokens

            if phase not in self.metrics["by_phase"]:
                self.metrics["by_phase"][phase] = 0
            self.metrics["by_phase"][phase] += estimated_tokens

    @staticmethod
    def generate_sample_metrics() -> Dict[str, Any]:
        """Generate sample token metrics for testing."""
        return {
            "by_agent": {
                "discovery-scout": {"tokens": 45_000, "calls": 8, "phase": "upstream"},
                "business-analyst": {"tokens": 32_000, "calls": 6, "phase": "upstream"},
                "data-architect": {"tokens": 56_000, "calls": 10, "phase": "midstream"},
                "data-modeler": {"tokens": 48_000, "calls": 9, "phase": "midstream"},
                "code-generator": {"tokens": 72_000, "calls": 12, "phase": "midstream"},
                "quality-gate": {"tokens": 28_000, "calls": 5, "phase": "midstream"},
                "downstream-executor": {"tokens": 41_000, "calls": 7, "phase": "downstream"},
                "reconciliation": {"tokens": 22_000, "calls": 4, "phase": "downstream"},
            },
            "by_phase": {
                "upstream": 77_000,
                "midstream": 204_000,
                "downstream": 63_000,
            },
            "by_wave": {
                "WAVE-001": 344_000,
            },
            "by_section": {
                "discovery_report": {"tokens": 18_000, "phase": "upstream"},
                "sttm_mapping": {"tokens": 22_000, "phase": "upstream"},
                "architecture_design": {"tokens": 52_000, "phase": "midstream"},
                "data_model": {"tokens": 48_000, "phase": "midstream"},
                "code_package": {"tokens": 104_000, "phase": "midstream"},
                "execution_plan": {"tokens": 32_000, "phase": "downstream"},
                "reconciliation_report": {"tokens": 25_000, "phase": "downstream"},
            },
            "total": 344_000,
            "timestamp": datetime.now().isoformat(),
        }

    def get_top_agents(self, limit: int = 5) -> List[tuple]:
        """Get top N agents by token consumption."""
        sorted_agents = sorted(
            self.metrics["by_agent"].items(),
            key=lambda x: x[1]["tokens"],
            reverse=True,
        )
        return sorted_agents[:limit]

    def get_phase_breakdown(self) -> Dict[str, int]:
        """Get token breakdown by phase."""
        return self.metrics["by_phase"]

    def get_cost_estimate(self, cost_per_mtokens: float = 0.0015) -> Dict[str, float]:
        """Estimate cost in USD based on token count."""
        # Typical OpenAI GPT pricing (adjust as needed)
        total_mtokens = self.metrics["total"] / 1_000_000
        total_cost = total_mtokens * cost_per_mtokens

        return {
            "total_tokens": self.metrics["total"],
            "total_mtokens": round(total_mtokens, 2),
            "cost_usd": round(total_cost, 2),
            "rate_per_mtokens": cost_per_mtokens,
        }


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Collect token metrics from migration artifacts")
    parser.add_argument("--wave-dir", help="Path to wave outputs directory")
    parser.add_argument("--output", help="Output JSON file for metrics")
    parser.add_argument("--sample", action="store_true", help="Generate sample metrics")
    args = parser.parse_args()

    if args.sample:
        metrics = TokenMetricsCollector.generate_sample_metrics()
    else:
        collector = TokenMetricsCollector()
        if args.wave_dir:
            metrics = collector.collect_from_artifacts(args.wave_dir)
        else:
            metrics = collector.metrics

    # Print summary
    print(f"\n📊 Token Usage Metrics")
    print(f"{'='*50}")
    print(f"Total Tokens: {metrics['total']:,}")
    print(f"\nBy Phase:")
    for phase, tokens in metrics["by_phase"].items():
        pct = (tokens / metrics["total"] * 100) if metrics["total"] > 0 else 0
        print(f"  {phase:20s}: {tokens:>10,} ({pct:>5.1f}%)")

    print(f"\nTop Agents:")
    collector = TokenMetricsCollector()
    collector.metrics = metrics
    for agent, data in collector.get_top_agents(5):
        print(f"  {agent:30s}: {data['tokens']:>10,} tokens")

    # Cost estimate
    costs = collector.get_cost_estimate()
    print(f"\nEstimated Cost (GPT pricing):")
    print(f"  Total: ${costs['cost_usd']:.2f} USD ({costs['total_mtokens']} M tokens)")

    # Save to file
    if args.output:
        Path(args.output).write_text(json.dumps(metrics, indent=2), encoding='utf-8')
        print(f"\n✅ Metrics saved to: {args.output}")

    return metrics


if __name__ == "__main__":
    main()
