#!/usr/bin/env python3
"""
Enhanced Token Metrics Collector with Headroom Integration
Tracks both raw tokens and compression metrics from Headroom.

**Phase 1 Integration (starting 2026-06-22):**
- Collect tokens BEFORE compression
- Track compression metrics FROM headroom_context_manager
- Calculate cost delta (before/after)
- Feed metrics to dashboards
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class EnhancedTokenMetrics:
    """Enhanced token metrics with Headroom compression tracking."""

    def __init__(self, project_root: str | None = None):
        """Initialize enhanced metrics collector."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.metrics: Dict[str, Any] = {
            "raw_tokens": {  # Tokens BEFORE compression
                "by_agent": {},
                "by_phase": {},
                "by_wave": {},
                "total": 0,
            },
            "compression": {  # Headroom compression stats
                "by_agent_pair": {},  # discovery-scout → data-architect
                "by_phase": {},  # Compression ratio per phase
                "total_saved": 0,
                "avg_ratio": 0.0,
                "method": "mock",  # or "headroom"
            },
            "cost_delta": {  # Cost before/after compression
                "raw_cost_usd": 0.0,
                "compressed_cost_usd": 0.0,
                "savings_usd": 0.0,
            },
            "timestamp": datetime.now().isoformat(),
        }

    def add_raw_tokens(
        self,
        agent: str,
        phase: str,
        wave_id: str,
        tokens: int,
    ):
        """Record raw token count (before compression)."""
        # By agent
        if agent not in self.metrics["raw_tokens"]["by_agent"]:
            self.metrics["raw_tokens"]["by_agent"][agent] = {"tokens": 0, "calls": 0, "phase": phase}

        self.metrics["raw_tokens"]["by_agent"][agent]["tokens"] += tokens
        self.metrics["raw_tokens"]["by_agent"][agent]["calls"] += 1

        # By phase
        if phase not in self.metrics["raw_tokens"]["by_phase"]:
            self.metrics["raw_tokens"]["by_phase"][phase] = 0
        self.metrics["raw_tokens"]["by_phase"][phase] += tokens

        # By wave
        if wave_id not in self.metrics["raw_tokens"]["by_wave"]:
            self.metrics["raw_tokens"]["by_wave"][wave_id] = 0
        self.metrics["raw_tokens"]["by_wave"][wave_id] += tokens

        # Total
        self.metrics["raw_tokens"]["total"] += tokens

    def add_compression_event(
        self,
        source_agent: str,
        target_agent: str,
        input_tokens: int,
        output_tokens: int,
        compression_ratio: float,
        phase: str,
        method: str = "mock",
    ):
        """Record compression event from Headroom."""
        agent_pair = f"{source_agent} → {target_agent}"
        tokens_saved = input_tokens - output_tokens

        # By agent pair
        if agent_pair not in self.metrics["compression"]["by_agent_pair"]:
            self.metrics["compression"]["by_agent_pair"][agent_pair] = {
                "count": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "tokens_saved": 0,
                "compression_ratio": 0.0,
                "phase": phase,
            }

        pair_data = self.metrics["compression"]["by_agent_pair"][agent_pair]
        pair_data["count"] += 1
        pair_data["input_tokens"] += input_tokens
        pair_data["output_tokens"] += output_tokens
        pair_data["tokens_saved"] += tokens_saved
        pair_data["compression_ratio"] = compression_ratio

        # By phase
        if phase not in self.metrics["compression"]["by_phase"]:
            self.metrics["compression"]["by_phase"][phase] = {
                "handoffs": 0,
                "total_input": 0,
                "total_output": 0,
                "total_saved": 0,
                "avg_ratio": 0.0,
            }

        phase_data = self.metrics["compression"]["by_phase"][phase]
        phase_data["handoffs"] += 1
        phase_data["total_input"] += input_tokens
        phase_data["total_output"] += output_tokens
        phase_data["total_saved"] += tokens_saved

        # Recalculate average ratio
        if phase_data["total_input"] > 0:
            phase_data["avg_ratio"] = (
                phase_data["total_saved"] / phase_data["total_input"]
            )

        # Update totals
        self.metrics["compression"]["total_saved"] += tokens_saved
        self.metrics["compression"]["method"] = method

        # Recalculate global average
        total_input = sum(
            d["input_tokens"]
            for d in self.metrics["compression"]["by_agent_pair"].values()
        )
        if total_input > 0:
            self.metrics["compression"]["avg_ratio"] = (
                self.metrics["compression"]["total_saved"] / total_input
            )

    def calculate_cost_delta(
        self,
        raw_cost_per_mtokens: float = 0.0015,
        compressed_cost_factor: float = 0.8,  # 20% cost increase for compression overhead
    ) -> Dict[str, float]:
        """
        Calculate cost difference before/after compression.
        
        Args:
            raw_cost_per_mtokens: Cost per M tokens without compression
            compressed_cost_factor: Additional cost factor for compression (0.8 = 80% of raw)
        """
        raw_tokens = self.metrics["raw_tokens"]["total"]
        tokens_saved = self.metrics["compression"]["total_saved"]
        compressed_tokens = raw_tokens - tokens_saved

        # Raw cost (no compression)
        raw_cost = (raw_tokens / 1_000_000) * raw_cost_per_mtokens

        # Compressed cost (input tokens have higher rate + output tokens)
        # Simplified: use compressed tokens with same rate but account for compression overhead
        compressed_cost = (
            (compressed_tokens / 1_000_000) * raw_cost_per_mtokens
            + (tokens_saved / 1_000_000) * raw_cost_per_mtokens * (1 - compressed_cost_factor)
        )

        savings = raw_cost - compressed_cost

        self.metrics["cost_delta"] = {
            "raw_cost_usd": round(raw_cost, 6),
            "compressed_cost_usd": round(compressed_cost, 6),
            "savings_usd": round(savings, 6),
            "savings_pct": round((savings / raw_cost * 100) if raw_cost > 0 else 0, 1),
        }

        return self.metrics["cost_delta"]

    def get_summary_for_dashboard(self) -> Dict[str, Any]:
        """Get concise summary for dashboard display."""
        cost = self.metrics["cost_delta"]
        total_input = sum(
            d["input_tokens"]
            for d in self.metrics["compression"]["by_agent_pair"].values()
        )

        return {
            "title": "📊 Token Optimization",
            "raw_tokens_total": self.metrics["raw_tokens"]["total"],
            "tokens_saved": self.metrics["compression"]["total_saved"],
            "compression_ratio": self.metrics["compression"]["avg_ratio"],
            "compression_pct": f"{self.metrics['compression']['avg_ratio']*100:.1f}%",
            "cost_raw_usd": cost["raw_cost_usd"],
            "cost_compressed_usd": cost["compressed_cost_usd"],
            "cost_savings_usd": cost["savings_usd"],
            "cost_savings_pct": cost.get("savings_pct", 0),
            "method": self.metrics["compression"]["method"],
            "by_phase": self.metrics["compression"]["by_phase"],
            "by_agent_pair": dict(
                list(self.metrics["compression"]["by_agent_pair"].items())[:5]  # Top 5
            ),
        }

    def get_detailed_report(self) -> Dict[str, Any]:
        """Get full detailed report for archival."""
        return {
            "timestamp": self.metrics["timestamp"],
            "raw_tokens": self.metrics["raw_tokens"],
            "compression": self.metrics["compression"],
            "cost_delta": self.metrics["cost_delta"],
            "summary": self.get_summary_for_dashboard(),
        }

    def save_to_file(self, output_file: str | Path):
        """Save metrics to JSON file."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        report = self.get_detailed_report()
        output_path.write_text(json.dumps(report, indent=2), encoding='utf-8')

        return output_path

    @staticmethod
    def example_with_headroom_integration() -> EnhancedTokenMetrics:
        """
        Example of metrics collection WITH Headroom integration.
        Demonstrates the expected data flow.
        """
        metrics = EnhancedTokenMetrics()

        # UPSTREAM phase
        metrics.add_raw_tokens(
            agent="discovery-scout",
            phase="upstream",
            wave_id="WAVE-001",
            tokens=130_808,
        )

        # After discovery completes, compress handoff
        metrics.add_compression_event(
            source_agent="discovery-scout",
            target_agent="data-architect",
            input_tokens=130_808,
            output_tokens=65_404,
            compression_ratio=0.50,
            phase="upstream",
            method="mock",
        )

        # MIDSTREAM phase
        metrics.add_raw_tokens(
            agent="data-architect",
            phase="midstream",
            wave_id="WAVE-001",
            tokens=65_404,
        )

        metrics.add_compression_event(
            source_agent="data-architect",
            target_agent="code-generator",
            input_tokens=65_404,
            output_tokens=32_702,
            compression_ratio=0.50,
            phase="midstream",
            method="mock",
        )

        # DOWNSTREAM phase
        metrics.add_raw_tokens(
            agent="downstream-executor",
            phase="downstream",
            wave_id="WAVE-001",
            tokens=32_702,
        )

        metrics.add_compression_event(
            source_agent="code-generator",
            target_agent="reconciliation",
            input_tokens=32_702,
            output_tokens=16_351,
            compression_ratio=0.50,
            phase="downstream",
            method="mock",
        )

        # Calculate cost impact
        metrics.calculate_cost_delta()

        return metrics


if __name__ == "__main__":
    # Example with realistic data
    metrics = EnhancedTokenMetrics.example_with_headroom_integration()

    # Print summary
    summary = metrics.get_summary_for_dashboard()
    print(f"\n📊 Token Optimization Summary")
    print(f"{'='*60}")
    print(f"Raw Tokens:          {summary['raw_tokens_total']:>12,}")
    print(f"Tokens Saved:        {summary['tokens_saved']:>12,}")
    print(f"Compression Ratio:   {summary['compression_pct']:>12s}")
    print(f"\nCost Impact (USD):")
    print(f"Before Compression:  ${summary['cost_raw_usd']:>11.6f}")
    print(f"After Compression:   ${summary['cost_compressed_usd']:>11.6f}")
    print(f"Savings:             ${summary['cost_savings_usd']:>11.6f} ({summary['cost_savings_pct']}%)")
    print(f"\nMethod:               {summary['method']}")

    # By phase
    print(f"\nCompression by Phase:")
    for phase, data in summary["by_phase"].items():
        print(
            f"  {phase:12s}: {data['avg_ratio']*100:>6.1f}% "
            f"({data['handoffs']} handoff, {data['total_saved']:>8,} tokens saved)"
        )

    # Save to file
    output_file = "headroom-metrics-example.json"
    metrics.save_to_file(output_file)
    print(f"\n✅ Full report saved to: {output_file}")
