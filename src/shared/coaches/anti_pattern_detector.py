"""
DMF Coach — Anti-Pattern Detector

Detects DMF-specific anti-patterns in agent execution and wave artifacts.
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import yaml

logger = logging.getLogger(__name__)


@dataclass
class AntiPattern:
    """Represents a detected anti-pattern."""
    name: str
    category: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    action: str
    score_impact: int  # Deduction from GateScore (e.g., -15)
    evidence: Dict[str, Any]


class AntiPatternDetector:
    """Detects and scores anti-patterns in DMF workflows."""

    # Built-in rule definitions (can be overridden via YAML)
    RULES = {
        "wave-completion": {
            "name": "Wave Completion Anti-Pattern",
            "category": "business-logic",
            "severity": "high",
            "entity_coverage_threshold": 0.90,
            "score_impact": -15,
        },
        "sttm-stability": {
            "name": "STTM Stability Anti-Pattern",
            "category": "stability",
            "severity": "medium",
            "regeneration_threshold": 2,  # Flag if > 2 regenerations
            "time_window_minutes": 120,
            "score_impact": -10,
        },
        "model-overreliance": {
            "name": "Model Overreliance Anti-Pattern",
            "category": "cost-optimization",
            "severity": "low",
            "expensive_models": ["gpt-4", "claude-opus-4-1"],
            "parametric_tasks": ["discovery-scout", "inventory-scout"],
            "score_impact": -5,
        },
        "context-bloat": {
            "name": "Context Bloat Anti-Pattern",
            "category": "efficiency",
            "severity": "medium",
            "context_window_threshold_pct": 70,
            "artifact_size_threshold_bytes": 40000,
            "score_impact": -10,
        },
        "silent-executor-failure": {
            "name": "Silent Executor Failure",
            "category": "critical",
            "severity": "critical",
            "output_token_threshold": 1000,
            "min_artifact_size_bytes": 10000,
            "score_impact": -30,
        },
        "gate-score-regression": {
            "name": "Gate Score Regression",
            "category": "quality-trend",
            "severity": "high",
            "regression_threshold_pct": 5,
            "score_impact": -20,
        },
    }

    def __init__(self, rules_dir: str = ".coach/rules"):
        self.rules_dir = Path(rules_dir)
        self.rules = self.RULES.copy()
        self._load_custom_rules()

    def _load_custom_rules(self) -> None:
        """Load custom rules from YAML files."""
        if not self.rules_dir.exists():
            return

        for rule_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    custom_rule = yaml.safe_load(f)
                    if custom_rule and "name" in custom_rule:
                        rule_id = rule_file.stem
                        self.rules[rule_id] = custom_rule
                        logger.info(f"Loaded custom rule: {rule_id}")
            except Exception as e:
                logger.warning(f"Failed to load rule {rule_file}: {e}")

    def detect_wave_completion_issue(
        self,
        gate_1_entity_count: int,
        gate_2_sttm_mapped_count: int,
        discovered_entities: List[str],
        mapped_entities: List[str],
    ) -> Optional[AntiPattern]:
        """Detect if discovered entities are missing from Gate 2 STTM."""
        rule = self.rules.get("wave-completion")
        threshold = rule["entity_coverage_threshold"]
        coverage = gate_2_sttm_mapped_count / gate_1_entity_count if gate_1_entity_count > 0 else 0

        if coverage < threshold:
            missing_entities = set(discovered_entities) - set(mapped_entities)
            gap_pct = (1 - coverage) * 100

            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"Entity coverage is {coverage:.1%}, below threshold of {threshold:.1%}",
                action=f"Review STTM with business-analyst. Missing {len(missing_entities)} entities: {missing_entities}",
                score_impact=rule["score_impact"],
                evidence={
                    "gate_1_entities": gate_1_entity_count,
                    "gate_2_mapped": gate_2_sttm_mapped_count,
                    "coverage_pct": coverage * 100,
                    "gap_pct": gap_pct,
                    "missing_count": len(missing_entities),
                },
            )
        return None

    def detect_sttm_instability(
        self,
        sttm_regenerations: int,
        regeneration_timestamps: List[str],
    ) -> Optional[AntiPattern]:
        """Detect STTM being regenerated multiple times."""
        rule = self.rules.get("sttm-stability")
        threshold = rule["regeneration_threshold"]

        if sttm_regenerations > threshold:
            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"STTM was regenerated {sttm_regenerations} times in {rule['time_window_minutes']} minutes",
                action="Clarify requirements with stakeholders before Gate 2 sign-off",
                score_impact=rule["score_impact"],
                evidence={
                    "regeneration_count": sttm_regenerations,
                    "timestamps": regeneration_timestamps,
                    "threshold": threshold,
                },
            )
        return None

    def detect_model_overreliance(
        self,
        agent_executions: List[Dict[str, Any]],
    ) -> Optional[AntiPattern]:
        """Detect overuse of expensive models for simple tasks."""
        rule = self.rules.get("model-overreliance")
        expensive_models = rule.get("expensive_models", [])
        parametric_tasks = rule.get("parametric_tasks", [])

        issues = []
        total_cost = 0

        for exec_event in agent_executions:
            model = exec_event.get("model", {}).get("name", "").lower()
            agent_id = exec_event.get("agent_id", "").lower()
            cost = exec_event.get("tokens", {}).get("cost_usd", 0)

            if any(em in model for em in expensive_models):
                if any(pt in agent_id for pt in parametric_tasks):
                    issues.append((agent_id, model, cost))
                    total_cost += cost

        if issues:
            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"Expensive models used for {len(issues)} parametric task(s), costing ${total_cost:.2f}",
                action=f"Downgrade {', '.join(t[0] for t in issues)} to Claude Haiku",
                score_impact=rule["score_impact"],
                evidence={
                    "overuse_count": len(issues),
                    "tasks_affected": [t[0] for t in issues],
                    "total_cost_usd": total_cost,
                },
            )
        return None

    def detect_context_bloat(
        self,
        artifacts: Dict[str, int],  # {filename: size_bytes}
        context_window_used_pct: float,
    ) -> Optional[AntiPattern]:
        """Detect artifacts consuming too much context."""
        rule = self.rules.get("context-bloat")
        threshold_pct = rule["context_window_threshold_pct"]
        threshold_bytes = rule["artifact_size_threshold_bytes"]

        bloated_artifacts = {
            name: size for name, size in artifacts.items() if size > threshold_bytes
        }
        total_size = sum(artifacts.values())

        if context_window_used_pct > threshold_pct or bloated_artifacts:
            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"Context window {context_window_used_pct:.0f}% used; {len(bloated_artifacts)} artifacts exceed {threshold_bytes} bytes",
                action=f"Split inventories into Wave A (core) and Wave B (audit columns). Monitor for auto-compaction.",
                score_impact=rule["score_impact"],
                evidence={
                    "context_window_used_pct": context_window_used_pct,
                    "total_artifact_size_bytes": total_size,
                    "bloated_artifacts": bloated_artifacts,
                },
            )
        return None

    def detect_silent_executor_failure(
        self,
        executor_output_tokens: int,
        executor_artifact_size: int,
        executor_output_text: str,
    ) -> Optional[AntiPattern]:
        """Detect downstream executor not actually writing files."""
        rule = self.rules.get("silent-executor-failure")
        token_threshold = rule["output_token_threshold"]
        size_threshold = rule["min_artifact_size_bytes"]

        is_suspicious = (
            executor_output_tokens < token_threshold
            and executor_artifact_size < size_threshold
        )

        if is_suspicious:
            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"Executor output suspiciously small: {executor_output_tokens} tokens, {executor_artifact_size} bytes",
                action="Auto-trigger self-healing agent to diagnose and re-execute",
                score_impact=rule["score_impact"],
                evidence={
                    "output_tokens": executor_output_tokens,
                    "artifact_size_bytes": executor_artifact_size,
                    "threshold_tokens": token_threshold,
                    "threshold_bytes": size_threshold,
                },
            )
        return None

    def detect_gate_score_regression(
        self,
        previous_gate_scores: List[float],  # [Wave 1, Wave 2, Wave 3, ...]
        current_wave_index: int,
    ) -> Optional[AntiPattern]:
        """Detect declining GateScore trend."""
        if current_wave_index < 1:
            return None

        rule = self.rules.get("gate-score-regression")
        threshold_pct = rule["regression_threshold_pct"] / 100

        prev_score = previous_gate_scores[current_wave_index - 1]
        current_score = previous_gate_scores[current_wave_index] if current_wave_index < len(
            previous_gate_scores
        ) else prev_score

        regression = (prev_score - current_score) / prev_score if prev_score > 0 else 0

        if regression > threshold_pct:
            return AntiPattern(
                name=rule["name"],
                category=rule["category"],
                severity=rule["severity"],
                description=f"GateScore dropped from {prev_score:.2f} to {current_score:.2f} ({regression*100:.1f}% regression)",
                action="Trigger iteration-improvement agent. Review: (a) discovery rush, (b) STTM instability, (c) context bloat",
                score_impact=rule["score_impact"],
                evidence={
                    "previous_score": prev_score,
                    "current_score": current_score,
                    "regression_pct": regression * 100,
                },
            )
        return None


# Global instance
detector = AntiPatternDetector()
