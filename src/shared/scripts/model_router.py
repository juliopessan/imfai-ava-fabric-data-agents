#!/usr/bin/env python3
"""
Model Router — routes DMF agent tasks to the appropriate Claude model
based on task complexity, optimising cost while preserving quality.

Routing tiers (Claude, via the Anthropic API — see anthropic_client.py):
  SIMPLE   -> claude-haiku-4-5   (validation, schema checks, format verification)
  MEDIUM   -> claude-sonnet-4-6  (STTM generation, DDL review, data quality rules)
  COMPLEX  -> claude-opus-4-8    (architecture decisions, ADRs, risk mapping)

Previously targeted Azure OpenAI deployments (gpt-4o-mini/gpt-4o). Switched
to Claude because that's what every agent in this repo (.github/agents/*) and
the rest of the cost-instrumentation chain (model_pricing.py,
enhanced_token_metrics.py, execution_telemetry.py) actually assumes — the
Azure OpenAI version was a parallel design nothing in this repo ever called.

Usage
-----
>>> router = ModelRouter()
>>> model = router.route("validate_gate_score", context={})
>>> model
'claude-haiku-4-5'

>>> model = router.route("generate_adr", context={"entity_count": 50})
>>> model
'claude-opus-4-8'
"""
from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import model_pricing

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
    deployment: str  # Claude model ID, e.g. "claude-haiku-4-5"
    max_tokens: int
    cost_per_1k_input: float   # USD — derived from model_pricing.py, not hand-picked
    cost_per_1k_output: float  # USD
    suitable_for: List[str] = field(default_factory=list)

    @property
    def cost_rank(self) -> float:
        return self.cost_per_1k_input + self.cost_per_1k_output


def _config_for(model: str, max_tokens: int, suitable_for: List[str]) -> ModelConfig:
    """Build a ModelConfig with cost fields sourced from model_pricing.py."""
    price = model_pricing.get_price(model)
    return ModelConfig(
        deployment=model,
        max_tokens=max_tokens,
        cost_per_1k_input=price.input_per_mtok / 1000,
        cost_per_1k_output=price.output_per_mtok / 1000,
        suitable_for=suitable_for,
    )


# Default Claude models per tier — override via ModelRouter(model_map=…)
DEFAULT_MODEL_MAP: Dict[TaskComplexity, ModelConfig] = {
    TaskComplexity.SIMPLE: _config_for(
        "claude-haiku-4-5",
        max_tokens=4096,
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
    TaskComplexity.MEDIUM: _config_for(
        "claude-sonnet-4-6",
        max_tokens=16384,
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
    TaskComplexity.COMPLEX: _config_for(
        "claude-opus-4-8",
        max_tokens=32768,
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
    Route DMF agent tasks to the right Claude model.

    Design principles
    -----------------
    1. Default to the cheapest model that can handle the task.
    2. Escalate only when context signals demand it.
    3. Never downgrade a task that was already classified as COMPLEX.
    4. Cost fields come from model_pricing.py — one source of truth.
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
        Return the Claude model ID for *task_name*.

        Parameters
        ----------
        task_name : str
            Logical task identifier (e.g. "validate_gate_score", "generate_adr").
        context : dict, optional
            Runtime context signals for escalation (e.g. {"entity_count": 120}).

        Returns
        -------
        str
            Claude model ID (e.g. "claude-haiku-4-5").
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
        logger.debug("Route: %s -> %s (%s)", task_name, config.deployment, final_complexity.value)

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
        """Build a flat lookup: task_name -> complexity tier."""
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
