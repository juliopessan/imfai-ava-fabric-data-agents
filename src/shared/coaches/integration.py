"""
DMF Coach Integration — Integrates telemetry and anti-pattern detection
with existing migration-coordinator and quality-gate workflows.

This module provides:
1. Hook for telemetry capture (called after agent execution)
2. Anti-pattern detection wrapper for GateScore adjustment
3. Wave-level analysis and skill discovery
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from src.shared.coaches import telemetry_collector, anti_pattern_detector

logger = logging.getLogger(__name__)


# ============================================================================
# DECISION 1: Telemetry Hook (Migration-Coordinator Integration)
# ============================================================================

class TelemetryHook:
    """
    Hook to capture agent execution telemetry.
    
    Called by: migration-coordinator.spawn_agent()
    Location: AFTER agent execution, before returning result
    
    Usage:
        hook = TelemetryHook()
        hook.log_agent_execution(
            agent_id='data-architect',
            wave='bradesco_wave_2',
            gate=1,
            result=agent_result
        )
    """
    
    def __init__(self):
        self.collector = telemetry_collector
    
    def log_agent_execution(
        self,
        agent_id: str,
        wave: str,
        gate: int,
        result: Dict[str, Any],
        agent_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Log agent execution to telemetry.
        
        Expected result format:
        {
            'model': 'claude-opus-4-1',
            'tokens_input': 12500,
            'tokens_output': 8300,
            'artifact_content': '...',
            'artifact_filename': 'architecture.md',
            'execution_time_sec': 130,
            'status': 'success',
            'artifact_lines': 432,
            'artifact_sections': 12,
            'references_entities': 87,
            'validation_passed': True
        }
        """
        try:
            artifact_size = len(result.get('artifact_content', ''))
            
            event = self.collector.log_execution(
                agent_id=agent_id,
                wave=wave,
                gate=gate,
                model=result.get('model', 'unknown'),
                tokens_in=result.get('tokens_input', 0),
                tokens_out=result.get('tokens_output', 0),
                artifact_filename=result.get('artifact_filename', 'output'),
                artifact_size=artifact_size,
                execution_time_sec=result.get('execution_time_sec', 0),
                status=result.get('status', 'unknown'),
                artifact_lines=result.get('artifact_lines'),
                artifact_sections=result.get('artifact_sections'),
                artifact_entities=result.get('references_entities'),
                validation_passed=result.get('validation_passed', True),
                agent_role=agent_role,
            )
            
            logger.info(f"✅ Telemetry logged for {agent_id} in {wave} Gate {gate}")
            return event
        
        except Exception as e:
            logger.error(f"❌ Failed to log telemetry for {agent_id}: {e}")
            return {}


# ============================================================================
# DECISION 2: GateScore Adjustment (Quality-Gate Integration)
# ============================================================================

class AntiPatternGateScoringAdjustment:
    """
    Integrates anti-pattern detection into GateScore calculation.
    
    Called by: quality-gate.calculate_gatescore()
    Location: AFTER base GateScore calculation, BEFORE final status determination
    
    Flow:
        1. quality-gate calculates base_score (0.70-0.89)
        2. Coach detects anti-patterns
        3. Anti-pattern impacts deducted from score
        4. Final score used for gate decision
    
    Usage:
        adjuster = AntiPatternGateScoringAdjustment()
        adjusted_score = adjuster.adjust_score(
            base_score=0.82,
            wave='bradesco_wave_2',
            gate=1,
            artifacts={...}
        )
    """
    
    def __init__(self):
        self.detector = anti_pattern_detector
    
    def adjust_score(
        self,
        base_score: float,
        wave: str,
        gate: int,
        artifacts: Dict[str, Any],
        artifact_sizes: Optional[Dict[str, int]] = None,
        context_window_used_pct: Optional[float] = None,
    ) -> tuple:
        """
        Adjust GateScore based on detected anti-patterns.
        
        Args:
            base_score: Original GateScore (0.0-1.0)
            wave: Wave identifier
            gate: Gate number (1, 2, or 3)
            artifacts: Dict of artifact content or summary
            artifact_sizes: Dict of artifact sizes in bytes
            context_window_used_pct: Context window usage percentage
        
        Returns:
            (adjusted_score, anti_patterns, score_adjustments)
        """
        detected_patterns = []
        total_adjustment = 0
        adjustments_log = []
        
        try:
            # Rule 1: Wave Completion (Gate 2 only)
            if gate == 2 and 'entities_discovered' in artifacts and 'entities_mapped' in artifacts:
                pattern = self.detector.detect_wave_completion_issue(
                    gate_1_entity_count=len(artifacts.get('entities_discovered', [])),
                    gate_2_sttm_mapped_count=len(artifacts.get('entities_mapped', [])),
                    discovered_entities=artifacts.get('entities_discovered', []),
                    mapped_entities=artifacts.get('entities_mapped', [])
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.warning(f"  🟡 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Rule 2: STTM Stability (Gate 1-2)
            if 'sttm_regenerations' in artifacts:
                pattern = self.detector.detect_sttm_instability(
                    sttm_regenerations=artifacts.get('sttm_regenerations', 0),
                    regeneration_timestamps=artifacts.get('sttm_timestamps', [])
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.warning(f"  🟡 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Rule 3: Model Overreliance (all gates)
            if 'agent_executions' in artifacts:
                pattern = self.detector.detect_model_overreliance(
                    agent_executions=artifacts.get('agent_executions', [])
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.warning(f"  🟡 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Rule 4: Context Bloat (all gates)
            if artifact_sizes and context_window_used_pct:
                pattern = self.detector.detect_context_bloat(
                    artifacts=artifact_sizes,
                    context_window_used_pct=context_window_used_pct
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.warning(f"  🟡 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Rule 5: Silent Executor Failure (Gate 3 only)
            if gate == 3 and 'executor_output_tokens' in artifacts:
                pattern = self.detector.detect_silent_executor_failure(
                    executor_output_tokens=artifacts.get('executor_output_tokens', 0),
                    executor_artifact_size=artifacts.get('executor_artifact_size', 0),
                    executor_output_text=artifacts.get('executor_output_text', '')
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.error(f"  🚨 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Rule 6: GateScore Regression (historical comparison)
            if 'previous_gate_scores' in artifacts:
                pattern = self.detector.detect_gate_score_regression(
                    previous_gate_scores=artifacts.get('previous_gate_scores', []),
                    current_wave_index=artifacts.get('current_wave_index', 0)
                )
                if pattern:
                    detected_patterns.append(pattern)
                    total_adjustment += pattern.score_impact
                    adjustments_log.append((pattern.name, pattern.score_impact))
                    logger.warning(f"  🟡 {pattern.name} ({pattern.score_impact:+d} pts)")
            
            # Calculate final score
            adjusted_score = max(0.0, min(1.0, base_score + total_adjustment))
            
            # Log summary
            if adjustments_log:
                logger.info(f"GateScore Adjustment for {wave} Gate {gate}:")
                logger.info(f"  Base score:      {base_score:.4f}")
                logger.info(f"  Anti-patterns:   {len(detected_patterns)}")
                for name, impact in adjustments_log:
                    logger.info(f"    {name:40s} {impact:+3d} pts")
                logger.info(f"  Adjusted score:  {adjusted_score:.4f} (change: {total_adjustment:+d} pts)")
            
            return adjusted_score, detected_patterns, adjustments_log
        
        except Exception as e:
            logger.error(f"Error during anti-pattern detection: {e}")
            return base_score, [], []


# ============================================================================
# DECISION 3: Skills Governance Workflow (TBD)
# ============================================================================

class SkillGovernanceWorkflow:
    """
    Placeholder for skill discovery and approval workflow.
    
    Decision: TBD (governance workflow)
    
    Planned flow:
    1. skill_finder discovers reusable patterns
    2. Proposes skill creation to SKILL registry
    3. Code review gate (GitHub PR)
    4. Approval + merge to .github/skills/
    5. Auto-register in agent configs
    """
    
    STATUS = "PENDING - Governance workflow TBD"
    
    def propose_skill(self, skill_name: str, skill_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Propose a new skill for approval.
        Returns: governance ticket / GitHub issue (implementation TBD)
        """
        logger.info(f"💡 Skill proposed: {skill_name} (governance workflow TBD)")
        return {
            "status": "proposed",
            "skill_name": skill_name,
            "proposed_at": datetime.now().isoformat(),
            "pending_approval": True,
        }


# ============================================================================
# Global Instances
# ============================================================================

telemetry_hook = TelemetryHook()
gate_scorer = AntiPatternGateScoringAdjustment()
skill_governance = SkillGovernanceWorkflow()
