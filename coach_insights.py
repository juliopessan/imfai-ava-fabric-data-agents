#!/usr/bin/env python3
"""
DMF Coach Insights — Continuous Best-Practices Analysis

Analyzes trace data from each phase and provides:
  1. Token efficiency metrics
  2. Cost attribution analysis
  3. Anti-pattern detection
  4. Best-practice suggestions
  5. Phase health scoring

Usage:
  from coach_insights import CoachInsights
  coach = CoachInsights()
  insights = coach.analyze_execution(agent_trace, etl_traces, gate_trace)
  coach.print_insights(insights)
"""

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class HealthStatus(Enum):
    """Phase health status."""
    HEALTHY = "🟢"
    WARNING = "🟡"
    CRITICAL = "🔴"


@dataclass
class PhaseInsight:
    """Insight about a phase execution."""
    metric: str
    value: Any
    status: HealthStatus
    message: str
    suggestion: Optional[str] = None


class CoachInsights:
    """DMF Coach — Best-practices analyzer for Data Migration Factory."""

    # Anti-pattern thresholds
    TOKEN_RATIO_WARNING = 0.5  # tokens_out / tokens_in < 50% = warning
    TOKEN_RATIO_CRITICAL = 0.3  # tokens_out / tokens_in < 30% = critical
    DURATION_WARNING_SEC = 300  # 5+ minutes = warning
    DURATION_CRITICAL_SEC = 600  # 10+ minutes = critical
    COST_PER_ARTIFACT_WARNING = 0.10  # $0.10+ per artifact = warning

    def __init__(self):
        self.insights_history: List[Dict[str, Any]] = []

    def analyze_execution(
        self,
        agent_trace: Dict[str, Any],
        etl_traces: Optional[List[Dict[str, Any]]] = None,
        gate_trace: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a phase execution from its traces.

        Returns:
          {
            'phase': 'phase_name',
            'status': HealthStatus,
            'insights': [PhaseInsight, ...],
            'metrics': { 'token_efficiency', 'cost_per_artifact', ... },
            'recommendations': [str, ...]
          }
        """
        insights = []
        metrics = {}
        recommendations = []

        # 1️⃣ Token Efficiency Analysis
        token_efficiency = self._analyze_token_efficiency(agent_trace)
        insights.append(token_efficiency["insight"])
        metrics["token_efficiency"] = token_efficiency["ratio"]
        if token_efficiency["suggestion"]:
            recommendations.append(token_efficiency["suggestion"])

        # 2️⃣ Duration Analysis
        duration_insight = self._analyze_duration(agent_trace)
        insights.append(duration_insight["insight"])
        metrics["duration_sec"] = agent_trace.get("duration_sec", 0)
        if duration_insight["suggestion"]:
            recommendations.append(duration_insight["suggestion"])

        # 3️⃣ Cost Analysis
        cost_insight = self._analyze_cost(agent_trace)
        insights.append(cost_insight["insight"])
        metrics["cost_usd"] = agent_trace.get("cost_usd", 0)
        if cost_insight["suggestion"]:
            recommendations.append(cost_insight["suggestion"])

        # 4️⃣ Artifact Productivity
        artifact_insight = self._analyze_artifact_productivity(agent_trace)
        insights.append(artifact_insight["insight"])
        metrics["artifacts_per_minute"] = artifact_insight["productivity"]
        if artifact_insight["suggestion"]:
            recommendations.append(artifact_insight["suggestion"])

        # 5️⃣ ETL Data Quality
        if etl_traces:
            etl_insight = self._analyze_etl_quality(etl_traces)
            insights.append(etl_insight["insight"])
            metrics["etl_error_rate"] = etl_insight["error_rate"]
            if etl_insight["suggestion"]:
                recommendations.append(etl_insight["suggestion"])

        # 6️⃣ Gate Scoring Health
        if gate_trace:
            gate_insight = self._analyze_gate_health(gate_trace)
            insights.append(gate_insight["insight"])
            metrics["gate_score"] = gate_trace.get("final_score", 0)
            if gate_insight["suggestion"]:
                recommendations.append(gate_insight["suggestion"])

        # Determine overall status
        statuses = [i.status for i in insights]
        if HealthStatus.CRITICAL in statuses:
            overall_status = HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.HEALTHY

        result = {
            "phase": agent_trace.get("operation_name", "unknown"),
            "wave": agent_trace.get("wave", "unknown"),
            "gate": agent_trace.get("gate", 0),
            "status": overall_status,
            "insights": insights,
            "metrics": metrics,
            "recommendations": recommendations,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.insights_history.append(result)
        return result

    def _analyze_token_efficiency(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input vs output token ratio."""
        tokens_in = trace.get("tokens_in", 1)  # avoid division by zero
        tokens_out = trace.get("tokens_out", 0)

        ratio = tokens_out / tokens_in if tokens_in > 0 else 0

        if ratio < self.TOKEN_RATIO_CRITICAL:
            status = HealthStatus.CRITICAL
            message = (
                f"⚠️  Very low token efficiency: {ratio:.1%} "
                f"({tokens_out}/{tokens_in})"
            )
            suggestion = (
                "Consider: (a) cached prompts, (b) few-shot examples, "
                "(c) prompt optimization"
            )
        elif ratio < self.TOKEN_RATIO_WARNING:
            status = HealthStatus.WARNING
            message = f"🟡 Low token efficiency: {ratio:.1%} ({tokens_out}/{tokens_in})"
            suggestion = "Opportunity for token optimization through better prompting"
        else:
            status = HealthStatus.HEALTHY
            message = f"✅ Good token efficiency: {ratio:.1%}"
            suggestion = None

        return {
            "insight": PhaseInsight(
                metric="token_efficiency",
                value=f"{ratio:.1%}",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "ratio": ratio,
            "suggestion": suggestion,
        }

    def _analyze_duration(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze phase execution duration."""
        duration = trace.get("duration_sec", 0)

        if duration > self.DURATION_CRITICAL_SEC:
            status = HealthStatus.CRITICAL
            message = f"⚠️  Very long execution: {duration:.1f}s (10+ min)"
            suggestion = (
                "Consider: (a) parallel sub-phases, (b) incremental processing, "
                "(c) resumable orchestration"
            )
        elif duration > self.DURATION_WARNING_SEC:
            status = HealthStatus.WARNING
            message = f"🟡 Long execution: {duration:.1f}s (5+ min)"
            suggestion = "Opportunity for parallelization or incremental execution"
        else:
            status = HealthStatus.HEALTHY
            message = f"✅ Good execution speed: {duration:.1f}s"
            suggestion = None

        return {
            "insight": PhaseInsight(
                metric="duration_sec",
                value=f"{duration:.1f}s",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "suggestion": suggestion,
        }

    def _analyze_cost(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cost per phase."""
        cost_usd = trace.get("cost_usd", 0)
        artifacts = trace.get("artifacts_generated", 1)
        cost_per_artifact = cost_usd / artifacts if artifacts > 0 else 0

        if cost_per_artifact > self.COST_PER_ARTIFACT_WARNING:
            status = HealthStatus.WARNING
            message = f"🟡 High cost per artifact: ${cost_per_artifact:.3f}"
            suggestion = "Review model selection, batch size, or prompt efficiency"
        else:
            status = HealthStatus.HEALTHY
            message = f"✅ Reasonable cost per artifact: ${cost_per_artifact:.3f}"
            suggestion = None

        return {
            "insight": PhaseInsight(
                metric="cost_usd",
                value=f"${cost_usd:.2f}",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "suggestion": suggestion,
        }

    def _analyze_artifact_productivity(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze artifacts generated per unit time."""
        duration = trace.get("duration_sec", 1)
        artifacts = trace.get("artifacts_generated", 0)
        productivity = artifacts / (duration / 60) if duration > 0 else 0

        status = HealthStatus.HEALTHY if artifacts > 0 else HealthStatus.WARNING
        message = f"📊 Generated {artifacts} artifacts at {productivity:.1f}/min"
        suggestion = None

        return {
            "insight": PhaseInsight(
                metric="productivity",
                value=f"{productivity:.1f} artifacts/min",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "productivity": productivity,
            "suggestion": suggestion,
        }

    def _analyze_etl_quality(self, etl_traces: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze ETL data quality."""
        total_rows = sum(t.get("rows_processed", 0) for t in etl_traces)
        failed_rows = sum(t.get("rows_failed", 0) for t in etl_traces)

        error_rate = (
            failed_rows / total_rows if total_rows > 0 else 0
        )

        if error_rate > 0.05:  # > 5%
            status = HealthStatus.CRITICAL
            message = f"⚠️  High ETL error rate: {error_rate:.2%} ({failed_rows}/{total_rows})"
            suggestion = "Review data validation, schema mapping, and error handling"
        elif error_rate > 0.01:  # > 1%
            status = HealthStatus.WARNING
            message = f"🟡 Elevated ETL error rate: {error_rate:.2%}"
            suggestion = "Monitor data quality; consider stricter validation"
        else:
            status = HealthStatus.HEALTHY
            message = f"✅ Good ETL quality: {error_rate:.2%} error rate"
            suggestion = None

        return {
            "insight": PhaseInsight(
                metric="etl_error_rate",
                value=f"{error_rate:.2%}",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "error_rate": error_rate,
            "suggestion": suggestion,
        }

    def _analyze_gate_health(self, gate_trace: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze gate validation score."""
        final_score = gate_trace.get("final_score", 0)
        anti_patterns = gate_trace.get("anti_patterns_detected", 0)

        if final_score < 0.70:
            status = HealthStatus.CRITICAL
            message = f"⚠️  Gate score too low: {final_score:.2f} (< 0.70)"
            suggestion = f"Address {anti_patterns} anti-patterns before proceeding"
        elif final_score < 0.85:
            status = HealthStatus.WARNING
            message = f"🟡 Gate score acceptable but low: {final_score:.2f}"
            suggestion = f"Review and address {anti_patterns} anti-patterns"
        else:
            status = HealthStatus.HEALTHY
            message = f"✅ Gate score strong: {final_score:.2f}"
            suggestion = None

        return {
            "insight": PhaseInsight(
                metric="gate_score",
                value=f"{final_score:.2f}",
                status=status,
                message=message,
                suggestion=suggestion,
            ),
            "suggestion": suggestion,
        }

    def print_insights(self, analysis: Dict[str, Any]) -> None:
        """Print formatted insights to console."""
        print(f"\n{'=' * 80}")
        print(
            f"  {analysis['status'].value} COACH INSIGHTS — {analysis['phase'].upper()}"
        )
        print(f"{'=' * 80}\n")

        # Print metrics table
        print("📊 METRICS:")
        for metric, value in analysis["metrics"].items():
            print(f"   {metric:.<30} {value}")

        # Print insights
        print("\n🔍 ANALYSIS:")
        for insight in analysis["insights"]:
            print(f"   {insight.status.value} {insight.message}")

        # Print recommendations
        if analysis["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(analysis["recommendations"], 1):
                print(f"   {i}. {rec}")

        print(f"\n{'=' * 80}\n")

    def get_wave_summary(self, wave: str) -> Dict[str, Any]:
        """Get aggregated insights for a complete wave."""
        wave_records = [r for r in self.insights_history if r["wave"] == wave]

        if not wave_records:
            return {"wave": wave, "phases": 0, "status": "no_data"}

        total_duration = sum(r["metrics"].get("duration_sec", 0) for r in wave_records)
        total_cost = sum(r["metrics"].get("cost_usd", 0) for r in wave_records)
        avg_gate_score = (
            sum(r["metrics"].get("gate_score", 0) for r in wave_records)
            / len(wave_records)
            if wave_records
            else 0
        )

        critical_count = sum(
            1 for r in wave_records if r["status"] == HealthStatus.CRITICAL
        )
        warning_count = sum(
            1 for r in wave_records if r["status"] == HealthStatus.WARNING
        )

        if critical_count > 0:
            overall = HealthStatus.CRITICAL
        elif warning_count > 0:
            overall = HealthStatus.WARNING
        else:
            overall = HealthStatus.HEALTHY

        return {
            "wave": wave,
            "phases": len(wave_records),
            "status": overall,
            "total_duration_sec": total_duration,
            "total_cost_usd": total_cost,
            "avg_gate_score": avg_gate_score,
            "critical_phases": critical_count,
            "warning_phases": warning_count,
            "phase_details": wave_records,
        }

    def print_wave_summary(self, wave: str) -> None:
        """Print formatted wave summary."""
        summary = self.get_wave_summary(wave)

        if summary["status"] == "no_data":
            print(f"⚠️  No insights found for wave: {wave}")
            return

        print(f"\n{'=' * 80}")
        print(f"  {summary['status'].value} WAVE SUMMARY — {wave.upper()}")
        print(f"{'=' * 80}\n")

        print("📊 AGGREGATED METRICS:")
        print(
            f"   Phases Completed ...... {summary['phases']}"
        )
        print(
            f"   Total Duration ....... {summary['total_duration_sec']:.1f}s "
            f"({summary['total_duration_sec']/60:.1f} min)"
        )
        print(f"   Total Cost ........... ${summary['total_cost_usd']:.2f}")
        print(f"   Average Gate Score ... {summary['avg_gate_score']:.2f}")

        print("\n⚠️  ISSUES FOUND:")
        print(f"   Critical Phases ...... {summary['critical_phases']}")
        print(f"   Warning Phases ....... {summary['warning_phases']}")

        print(f"\n{'=' * 80}\n")

    def validate_ponytail_ladder(self, trace: Dict[str, Any], gate: int) -> Dict[str, Any]:
        """
        Validate that artifacts were generated following Ponytail 'lazy senior dev' ladder.
        
        Returns validation result with status and suggestions.
        """
        artifacts = trace.get("artifacts_generated", 0)
        gate_limits = {
            1: {"min": 1, "target": 3, "max": 5},      # Upstream: inventory, STTM, pain points
            2: {"min": 2, "target": 5, "max": 8},      # Midstream: DDL, contracts, strategy
            3: {"min": 3, "target": 6, "max": 10},     # Downstream: ETL, validation, tests
            4: {"min": 2, "target": 11, "max": 20},    # Consolidation: dashboards, runbook
        }
        
        limits = gate_limits.get(gate, {"min": 1, "target": 5, "max": 10})
        
        violations = []
        suggestions = []
        
        # Check YAGNI (Does it need to exist?)
        if artifacts > limits["max"]:
            violations.append(
                f"Artifact count {artifacts} exceeds gate {gate} target {limits['target']}"
            )
            suggestions.append(
                "Apply YAGNI: Does every artifact need to exist NOW? "
                "Consider deferring to next wave."
            )
        
        # Check reuse opportunity
        if artifacts > limits["target"]:
            suggestions.append(
                "Review: Can any artifacts be consolidated or templated? "
                "(Reuse over rewrite)"
            )
        
        # Check token efficiency
        tokens_in = trace.get("tokens_in", 1)
        tokens_out = trace.get("tokens_out", 0)
        ratio = tokens_out / tokens_in if tokens_in > 0 else 0
        
        if ratio > 0.6:  # Efficiency < 40%
            violations.append(
                f"Tokens {tokens_in} → {tokens_out} (efficiency {ratio:.1%}) "
                "suggests over-analysis"
            )
            suggestions.append(
                "Ponytail ladder: Stop at first rung that holds. "
                "Are you re-analyzing problems already solved?"
            )
        
        # Check cost per artifact
        cost = trace.get("cost_usd", 0)
        cost_per_artifact = cost / artifacts if artifacts > 0 else 0
        
        if cost_per_artifact > 0.15:
            suggestions.append(
                "Cost per artifact ${:.3f} is high. "
                "Consider stdlib/native platform options (rungs 3-4)".format(cost_per_artifact)
            )
        
        # Status determination
        if violations:
            status = HealthStatus.WARNING
            message = f"Ponytail ladder check: {len(violations)} violation(s)"
        else:
            status = HealthStatus.HEALTHY
            message = f"Ponytail ladder check passed: {artifacts} artifacts (target {limits['target']})"
        
        return {
            "status": status,
            "message": message,
            "violations": violations,
            "suggestions": suggestions,
            "gate": gate,
            "artifacts": artifacts,
            "target_artifacts": limits["target"],
        }


def get_coach_insights() -> CoachInsights:
    """Singleton getter for CoachInsights instance."""
    global _coach_instance
    if "_coach_instance" not in globals():
        _coach_instance = CoachInsights()
    return _coach_instance
