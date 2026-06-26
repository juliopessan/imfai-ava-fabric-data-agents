"""
Tests for model_router.py — complexity-based Claude model routing.

Covers:
- Task classification (SIMPLE / MEDIUM / COMPLEX)
- Context escalation rules
- route() and get_config() APIs
- route_task() module-level convenience function
- routing_summary() cost reporting
- Unknown task fallback
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from model_router import (
    ModelRouter,
    ModelConfig,
    TaskComplexity,
    DEFAULT_MODEL_MAP,
    route_task,
    get_router,
)


# ---------------------------------------------------------------------------
# Classification — base tier without context
# ---------------------------------------------------------------------------

class TestTaskClassification:
    def setup_method(self):
        self.router = ModelRouter()

    def test_simple_task_classify(self):
        assert self.router.classify("validate_gate_score") == TaskComplexity.SIMPLE

    def test_medium_task_classify(self):
        assert self.router.classify("generate_sttm") == TaskComplexity.MEDIUM

    def test_complex_task_classify(self):
        assert self.router.classify("generate_adr") == TaskComplexity.COMPLEX

    def test_unknown_task_uses_default(self):
        complexity = self.router.classify("some_totally_new_task")
        assert complexity == TaskComplexity.MEDIUM  # default

    def test_keyword_fallback_validate(self):
        # "validate_something_new" should map to SIMPLE via keyword heuristic
        assert self.router.classify("validate_something_new") == TaskComplexity.SIMPLE

    def test_keyword_fallback_architect(self):
        assert self.router.classify("design_architect_plan") == TaskComplexity.COMPLEX

    def test_keyword_fallback_generate(self):
        assert self.router.classify("generate_report_custom") == TaskComplexity.MEDIUM


# ---------------------------------------------------------------------------
# route() — deployment name
# ---------------------------------------------------------------------------

class TestRoute:
    def setup_method(self):
        self.router = ModelRouter()

    def test_simple_task_routes_to_mini(self):
        deployment = self.router.route("validate_gate_score")
        assert deployment == "claude-haiku-4-5"

    def test_medium_task_routes_to_sonnet(self):
        deployment = self.router.route("generate_sttm")
        assert deployment == "claude-sonnet-4-6"

    def test_complex_task_routes_to_opus(self):
        deployment = self.router.route("generate_adr")
        assert deployment == "claude-opus-4-8"

    def test_route_returns_string(self):
        result = self.router.route("validate_schema")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_route_with_empty_context(self):
        # Should not raise
        result = self.router.route("validate_gate_score", context={})
        assert result == "claude-haiku-4-5"


# ---------------------------------------------------------------------------
# Context escalation
# ---------------------------------------------------------------------------

class TestEscalation:
    def setup_method(self):
        self.router = ModelRouter()

    def test_high_entity_count_escalates_simple_to_medium(self):
        # 50 entities > 30 threshold → MEDIUM
        deployment = self.router.route(
            "validate_gate_score", context={"entity_count": 50}
        )
        # validate_gate_score is SIMPLE base, escalated to MEDIUM by entity_count > 30
        assert deployment == "claude-sonnet-4-6"

    def test_very_high_entity_count_escalates_to_complex(self):
        deployment = self.router.route(
            "validate_gate_score", context={"entity_count": 150}
        )
        assert deployment == "claude-opus-4-8"  # entity_count > 100 -> COMPLEX

    def test_adr_required_flag_escalates_to_complex(self):
        deployment = self.router.route(
            "validate_schema", context={"adr_required": True}
        )
        assert deployment == "claude-opus-4-8"

    def test_cross_domain_flag_escalates_to_complex(self):
        deployment = self.router.route(
            "check_wave_config", context={"cross_domain": True}
        )
        assert deployment == "claude-opus-4-8"

    def test_no_escalation_below_thresholds(self):
        deployment = self.router.route(
            "validate_gate_score", context={"entity_count": 5}
        )
        # Below 30 threshold → stays SIMPLE
        assert deployment == "claude-haiku-4-5"

    def test_complex_task_not_downgraded_by_small_context(self):
        # COMPLEX task should never drop to SIMPLE even with trivial context
        deployment = self.router.route(
            "generate_adr", context={"entity_count": 1}
        )
        assert deployment == "claude-opus-4-8"

    def test_large_schema_escalates(self):
        # schema_size_kb > 500 → COMPLEX
        deployment = self.router.route(
            "validate_schema", context={"schema_size_kb": 600}
        )
        assert deployment == "claude-opus-4-8"


# ---------------------------------------------------------------------------
# get_config()
# ---------------------------------------------------------------------------

class TestGetConfig:
    def setup_method(self):
        self.router = ModelRouter()

    def test_returns_model_config_instance(self):
        config = self.router.get_config("validate_gate_score")
        assert isinstance(config, ModelConfig)

    def test_simple_config_has_lower_cost(self):
        simple_cfg = self.router.get_config("validate_gate_score")
        medium_cfg = self.router.get_config("generate_sttm")
        assert simple_cfg.cost_rank < medium_cfg.cost_rank

    def test_config_has_required_fields(self):
        config = self.router.get_config("generate_adr")
        assert config.deployment
        assert config.max_tokens > 0
        assert config.cost_per_1k_input >= 0
        assert config.cost_per_1k_output >= 0


# ---------------------------------------------------------------------------
# routing_summary()
# ---------------------------------------------------------------------------

class TestRoutingSummary:
    def test_empty_summary_when_no_routes(self):
        router = ModelRouter()
        summary = router.routing_summary()
        assert summary["total_decisions"] == 0

    def test_summary_counts_decisions(self):
        router = ModelRouter()
        router.route("validate_gate_score")
        router.route("generate_sttm")
        router.route("generate_adr")
        summary = router.routing_summary()
        assert summary["total_decisions"] == 3

    def test_summary_tracks_escalations(self):
        router = ModelRouter()
        router.route("validate_gate_score")  # no escalation
        router.route("validate_schema", context={"entity_count": 50})  # escalated
        summary = router.routing_summary()
        assert summary["escalations"] >= 1

    def test_summary_has_by_complexity(self):
        router = ModelRouter()
        router.route("validate_gate_score")
        summary = router.routing_summary()
        assert "by_complexity" in summary


# ---------------------------------------------------------------------------
# Module-level convenience helpers
# ---------------------------------------------------------------------------

class TestModuleLevelHelpers:
    def test_route_task_function(self):
        result = route_task("validate_gate_score")
        assert result == "claude-haiku-4-5"

    def test_get_router_returns_singleton(self):
        r1 = get_router()
        r2 = get_router()
        assert r1 is r2

    def test_route_task_with_context(self):
        result = route_task("validate_schema", {"entity_count": 200})
        assert result == "claude-opus-4-8"


# ---------------------------------------------------------------------------
# DEFAULT_MODEL_MAP coverage — all registered tasks are routable
# ---------------------------------------------------------------------------

class TestDefaultModelMapCoverage:
    def test_all_suitable_for_tasks_are_routable(self):
        router = ModelRouter()
        for complexity, config in DEFAULT_MODEL_MAP.items():
            for task in config.suitable_for:
                deployment = router.route(task)
                assert deployment == config.deployment, (
                    f"Task '{task}' (tier={complexity.value}) should route to "
                    f"'{config.deployment}', got '{deployment}'"
                )

    def test_no_duplicate_task_in_map(self):
        seen: set = set()
        for config in DEFAULT_MODEL_MAP.values():
            for task in config.suitable_for:
                assert task not in seen, f"Duplicate task '{task}' in DEFAULT_MODEL_MAP"
                seen.add(task)

    def test_cost_rank_order_simple_lt_medium(self):
        simple = DEFAULT_MODEL_MAP[TaskComplexity.SIMPLE].cost_rank
        medium = DEFAULT_MODEL_MAP[TaskComplexity.MEDIUM].cost_rank
        assert simple < medium, "SIMPLE tier should be cheaper than MEDIUM"


# ---------------------------------------------------------------------------
# Custom model map
# ---------------------------------------------------------------------------

class TestCustomModelMap:
    def test_custom_map_overrides_defaults(self):
        custom_map = {
            TaskComplexity.SIMPLE: ModelConfig(
                deployment="my-mini-deployment",
                max_tokens=2048,
                cost_per_1k_input=0.0001,
                cost_per_1k_output=0.0004,
                suitable_for=["validate_gate_score"],
            ),
            TaskComplexity.MEDIUM: ModelConfig(
                deployment="my-medium-deployment",
                max_tokens=8192,
                cost_per_1k_input=0.002,
                cost_per_1k_output=0.008,
                suitable_for=["generate_sttm"],
            ),
            TaskComplexity.COMPLEX: ModelConfig(
                deployment="my-complex-deployment",
                max_tokens=32768,
                cost_per_1k_input=0.005,
                cost_per_1k_output=0.015,
                suitable_for=["generate_adr"],
            ),
        }
        router = ModelRouter(model_map=custom_map)
        assert router.route("validate_gate_score") == "my-mini-deployment"
        assert router.route("generate_adr") == "my-complex-deployment"
