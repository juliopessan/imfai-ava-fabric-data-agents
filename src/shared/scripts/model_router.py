#!/usr/bin/env python3
"""
Model Router — routes DMF agent tasks to the appropriate Azure OpenAI deployment
based on task complexity, optimising cost while preserving quality.

Routing tiers (Azure OpenAI only — Microsoft-only constraint):
  SIMPLE   → gpt-4o-mini     (validation, schema checks, format verification)
  MEDIUM   → gpt-4o          (STTM generation, DDL review, data quality rules)
  COMPLEX  → gpt-4o / o1     (architecture decisions, ADRs, risk mapping)

Usage
-----
>>> router = ModelRouter()
>>> model = router.route("validate_gate_score", context={})
>>> model
'gpt-4o-mini'

>>> model = router.route("generate_adr", context={"entity_count": 50})
>>> model
'gpt-4o'
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Complexity tiers
# ---------------------------------------------------------------------------

class TaskComplexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ModelConfig:
    deployment: str
    max_tokens: int
    cost_per_1k_input: float   # USD
    cost_per_1k_output: float  # USD
    suitable_for: List[str] = field(default_factory=list)

    @property
    def cost_rank(self) -> float:
        return self.cost_per_1k_input + self.cost_per_1k_output


# Default Azure OpenAI deployments — override via ModelRouter(model_map=…)
DEFAULT_MODEL_MAP: Dict[TaskComplexity, ModelConfig] = {
    TaskComplexity.SIMPLE: ModelConfig(
        deployment="gpt-4o-mini",
        max_tokens=4096,
        cost_per_1k_input=0.000150,
        cost_per_1k_output=0.000600,
        suitable_for=[
            "validate_gate_score",
            "validate_schema",
            "check_wave_config",
            "format_check",
            "count_entities",
            "gate_score_report",
            "quality_thresholds",
            "reconciliation_check",
        ],
    ),
    TaskComplexity.MEDIUM: ModelConfig(
        deployment="gpt-4o",
        max_tokens=16384,
        cost_per_1k_input=0.002500,
        cost_per_1k_output=0.010000,
        suitable_for=[
            "generate_sttm",
            "review_ddl",
            "generate_data_quality_rules",
            "build_dependency_graph",
            "classify_entities",
            "risk_rollup",
            "kpi_dashboard",
            "wave_status",
            "cost_estimate",
        ],
    ),
    TaskComplexity.COMPLEX: ModelConfig(
        deployment="gpt-4o",
        max_tokens=32768,
        cost_per_1k_input=0.002500,
        cost_per_1k_output=0.010000,
        suitable_for=[
            "generate_adr",
            "architecture_design",
            "risk_mapping",
            "logic_extraction",
            "generate_data_model",
            "security_compliance_review",
            "bi_semantic_layer",
            "iteration_improvement",
        ],
    ),
}

# Context signals that escalate complexity
_ESCALATION_RULES: List[tuple] = [
    # (context_key, operator, threshold, escalate_to)
    ("entity_count", ">", 100, TaskComplexity.COMPLEX),
    ("entity_count", ">", 30, TaskComplexity.MEDIUM),
    ("schema_size_kb", ">", 500, TaskComplexity.COMPLEX),
    ("schema_size_kb", ">", 100, TaskComplexity.MEDIUM),
    ("adr_required", "==", True, TaskComplexity.COMPLEX),
    ("cross_domain", "==", True, TaskComplexity.COMPLEX),
]


# ---------------------------------------------------------------------------
# Main router
# ---------------------------------------------------------------------------

class ModelRouter:
    """
    Route DMF agent tasks to the right Azure OpenAI deployment.

    Design principles
    -----------------
    1. Default to cheapest model that can handle the task.
    2. Escalate only when context signals demand it.
    3. Never downgrade a task that was already classified as COMPLEX.
    4. All deployments are Azure OpenAI (Microsoft-only).
    """

    def __init__(
        self,
        model_map: Optional[Dict[TaskComplexity, ModelConfig]] = None,
        default_complexity: TaskComplexity = TaskComplexity.MEDIUM,
    ) -> None:
        self.model_map = model_map or DEFAULT_MODEL_MAP
        self.default_complexity = default_complexity
        self._task_index: Dict[str, TaskComplexity] = self._build_task_index()
        self._routing_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(
        self,
        task_name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Return the Azure OpenAI deployment name for *task_name*.

        Parameters
        ----------
        task_name : str
            Logical task identifier (e.g. "validate_gate_score", "generate_adr").
        context : dict, optional
            Runtime context signals for escalation (e.g. {"entity_count": 120}).

        Returns
        -------
        str
            Azure OpenAI deployment name (e.g. "gpt-4o-mini").
        """
        context = context or {}
        base_complexity = self._classify_task(task_name)
        final_complexity = self._apply_escalation_rules(base_complexity, context)
        config = self.model_map[final_complexity]

        entry = {
            "task": task_name,
            "base_complexity": base_complexity.value,
            "final_complexity": final_complexity.value,
            "deployment": config.deployment,
            "escalated": final_complexity != base_complexity,
        }
        self._routing_log.append(entry)
        logger.debug("Route: %s → %s (%s)", task_name, config.deployment, final_complexity.value)

        return config.deployment

    def get_config(
        self,
        task_name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ModelConfig:
        """Return full ModelConfig (deployment + cost info) for *task_name*."""
        context = context or {}
        base_complexity = self._classify_task(task_name)
        final_complexity = self._apply_escalation_rules(base_complexity, context)
        return self.model_map[final_complexity]

    def classify(self, task_name: str) -> TaskComplexity:
        """Return complexity tier for *task_name* without context escalation."""
        return self._classify_task(task_name)

    def routing_summary(self) -> Dict[str, Any]:
        """Return a cost-awareness summary of all routing decisions made so far."""
        if not self._routing_log:
            return {"total_decisions": 0, "escalations": 0, "by_complexity": {}}

        by_complexity: Dict[str, int] = {}
        escalations = 0
        for entry in self._routing_log:
            tier = entry["final_complexity"]
            by_complexity[tier] = by_complexity.get(tier, 0) + 1
            if entry["escalated"]:
                escalations += 1

        return {
            "total_decisions": len(self._routing_log),
            "escalations": escalations,
            "escalation_rate_pct": round(escalations / len(self._routing_log) * 100, 1),
            "by_complexity": by_complexity,
            "log": self._routing_log[-20:],  # Last 20 decisions
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_task_index(self) -> Dict[str, TaskComplexity]:
        """Build a flat lookup: task_name → complexity tier."""
        index: Dict[str, TaskComplexity] = {}
        for complexity, config in self.model_map.items():
            for task in config.suitable_for:
                index[task] = complexity
        return index

    def _classify_task(self, task_name: str) -> TaskComplexity:
        """Map *task_name* to a base complexity tier."""
        exact = self._task_index.get(task_name)
        if exact:
            return exact

        # Fuzzy keyword escalation as fallback
        name_lower = task_name.lower()
        if any(kw in name_lower for kw in ("adr", "architect", "risk", "model", "logic", "design")):
            return TaskComplexity.COMPLEX
        if any(kw in name_lower for kw in ("generate", "build", "review", "extract", "classify")):
            return TaskComplexity.MEDIUM
        if any(kw in name_lower for kw in ("validate", "check", "count", "format", "report")):
            return TaskComplexity.SIMPLE

        logger.debug("Unknown task '%s' — using default complexity: %s", task_name, self.default_complexity.value)
        return self.default_complexity

    def _apply_escalation_rules(
        self, base: TaskComplexity, context: Dict[str, Any]
    ) -> TaskComplexity:
        """Escalate complexity based on runtime context signals."""
        # Complexity ordinal: SIMPLE < MEDIUM < COMPLEX
        _order = [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM, TaskComplexity.COMPLEX]
        current_rank = _order.index(base)
        max_rank = current_rank

        for ctx_key, operator, threshold, target in _ESCALATION_RULES:
            value = context.get(ctx_key)
            if value is None:
                continue
            triggered = False
            if operator == ">" and value > threshold:
                triggered = True
            elif operator == ">=" and value >= threshold:
                triggered = True
            elif operator == "==" and value == threshold:
                triggered = True
            elif operator == "<" and value < threshold:
                triggered = True

            if triggered:
                target_rank = _order.index(target)
                max_rank = max(max_rank, target_rank)

        return _order[max_rank]


# ---------------------------------------------------------------------------
# Module-level singleton — import and use directly in agent scripts
# ---------------------------------------------------------------------------

_default_router: Optional[ModelRouter] = None


def get_router() -> ModelRouter:
    """Return (or lazily create) the module-level default router."""
    global _default_router
    if _default_router is None:
        _default_router = ModelRouter()
    return _default_router


def route_task(task_name: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Convenience wrapper: route a task via the default router."""
    return get_router().route(task_name, context)
