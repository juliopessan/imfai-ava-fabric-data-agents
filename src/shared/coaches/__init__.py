"""
DMF Coach — Continuous Best-Practices Mentoring for Data Migration Factory

This module integrates the AI Engineer Coach concept with the Data Migration Factory,
providing continuous monitoring, anti-pattern detection, and skill discovery across
agent execution waves.

Modules:
- telemetry_collector: Captures agent execution events
- anti_pattern_detector: Detects 6+ DMF-specific anti-patterns
- integration: Hooks for migration-coordinator and quality-gate integration
- context_health_scorer: Audits .agent.md and skill quality (TODO)
- skill_finder: Discovers reusable patterns in agent outputs (TODO)
"""

from .telemetry_collector import TelemetryCollector, collector as telemetry_collector
from .anti_pattern_detector import AntiPatternDetector, detector as anti_pattern_detector
from .integration import TelemetryHook, AntiPatternGateScoringAdjustment, SkillGovernanceWorkflow
from .integration import telemetry_hook, gate_scorer, skill_governance

__all__ = [
    # Collectors
    "TelemetryCollector",
    "telemetry_collector",
    # Detectors
    "AntiPatternDetector",
    "anti_pattern_detector",
    # Integration hooks
    "TelemetryHook",
    "telemetry_hook",
    "AntiPatternGateScoringAdjustment",
    "gate_scorer",
    "SkillGovernanceWorkflow",
    "skill_governance",
]

__version__ = "0.1.0"
