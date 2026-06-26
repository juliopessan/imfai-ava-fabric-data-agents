"""
DMF Coach Integration Examples

Shows how to integrate Coach telemetry and anti-pattern detection
into existing migration-coordinator and quality-gate workflows.

DECISION 1: Telemetry Hook in migration-coordinator.spawn_agent()
DECISION 2: GateScore Adjustment in quality-gate.calculate_gatescore()
DECISION 3: Skills Governance (TBD - placeholder)
"""

# ============================================================================
# EXAMPLE 1: Telemetry Hook in migration-coordinator
# ============================================================================
# File: src/shared/scripts/migration-coordinator.py (pseudocode)
#
# Location: After agent execution, before returning result
#
# def spawn_agent(self, agent_id: str, wave: str, gate: int, ...) -> Dict[str, Any]:
#     """Spawn an agent and execute it."""
#     
#     # ... existing agent execution logic ...
#     result = await agent_execution(agent_id, wave, ...)
#     
#     # NEW: Log telemetry (Decision 1: Hook in migration-coordinator)
#     from src.shared.coaches import telemetry_hook
#     telemetry_hook.log_agent_execution(
#         agent_id=agent_id,
#         wave=wave,
#         gate=gate,
#         result=result,
#         agent_role=f"Agent: {agent_id.replace('-', ' ').title()}"
#     )
#     
#     return result

EXAMPLE_1_MIGRATION_COORDINATOR = """
# File: src/shared/scripts/migration-coordinator.py
# Pseudocode for integration

from src.shared.coaches import telemetry_hook

async def spawn_agent(self, agent_id: str, wave: str, gate: int, ...) -> Dict[str, Any]:
    '''Spawn and execute an agent.'''
    
    # Existing logic to execute agent
    result = await agent_execution(agent_id, wave, ...)
    
    # NEW: Log to Coach telemetry
    try:
        telemetry_hook.log_agent_execution(
            agent_id=agent_id,
            wave=wave,
            gate=gate,
            result=result
        )
    except Exception as e:
        logger.warning(f"Coach telemetry logging failed: {e}")
    
    return result
"""

# ============================================================================
# EXAMPLE 2: GateScore Adjustment in quality-gate
# ============================================================================
# File: src/shared/scripts/gate_score_report.py (pseudocode)
#
# Location: In GateScoreCalculator.calculate(), AFTER base score, BEFORE status determination
#
# def calculate(self, completude, quality, residual_risk, reconciliation):
#     """Calculate GateScore with anti-pattern adjustments."""
#     
#     # ... existing base score calculation ...
#     base_score = (completude * 0.35) + (quality * 0.25) + ...
#     
#     # NEW: Adjust for anti-patterns (Decision 2: Automatic GateScore adjustment)
#     from src.shared.coaches import gate_scorer
#     adjusted_score, anti_patterns, adjustments = gate_scorer.adjust_score(
#         base_score=base_score,
#         wave=self.wave_id,
#         gate=self.gate_number,
#         artifacts={
#             'entities_discovered': [...],
#             'entities_mapped': [...],
#             'sttm_regenerations': 3,
#             'agent_executions': [...]
#         },
#         artifact_sizes={'architecture.md': 45600, ...},
#         context_window_used_pct=77
#     )
#     
#     # Use adjusted_score for final decision
#     if adjusted_score >= 0.85:
#         status = "approved"
#     elif adjusted_score >= 0.70:
#         status = "conditional"
#     else:
#         status = "blocked"

EXAMPLE_2_QUALITY_GATE = """
# File: src/shared/scripts/gate_score_report.py
# Integration in GateScoreCalculator.calculate()

from src.shared.coaches import gate_scorer
import logging

logger = logging.getLogger(__name__)

def calculate(
    self,
    completude: float,
    quality: float,
    residual_risk: float,
    reconciliation: float = 1.0,
    artifacts: Dict[str, Any] = None,  # NEW: artifacts for anti-pattern detection
    artifact_sizes: Dict[str, int] = None,  # NEW: for context bloat detection
    context_window_used_pct: float = None,  # NEW: for context tracking
) -> GateScoreResult:
    '''Calculate GateScore with anti-pattern adjustments.'''
    
    # Existing base score calculation
    base_score = (
        (completude * self.COMPLETUDE_WEIGHT) +
        (quality * self.QUALITY_WEIGHT) +
        (residual_risk * self.RESIDUAL_RISK_WEIGHT) +
        (reconciliation * self.RECONCILIATION_WEIGHT)
    )
    
    # NEW: Anti-pattern detection and scoring adjustment (Decision 2)
    adjusted_score = base_score
    detected_patterns = []
    adjustments_log = []
    
    if artifacts:
        adjusted_score, detected_patterns, adjustments_log = gate_scorer.adjust_score(
            base_score=base_score,
            wave=self.wave_id,
            gate=self.gate_number,
            artifacts=artifacts,
            artifact_sizes=artifact_sizes,
            context_window_used_pct=context_window_used_pct
        )
    
    # Determine status based on adjusted score
    if adjusted_score >= self.APPROVAL_THRESHOLD:
        status = "approved"
    elif adjusted_score >= self.CONDITIONAL_THRESHOLD:
        status = "conditional"
    else:
        status = "blocked"
    
    # Build result with anti-pattern findings
    result = GateScoreResult(
        gate_number=self.gate_number,
        wave_id=self.wave_id,
        score=adjusted_score,  # Adjusted score used here
        completude=completude,
        quality=quality,
        residual_risk=residual_risk,
        reconciliation=reconciliation,
        status=status,
        calculated_at=datetime.now(timezone.utc).isoformat(),
        recommendations=self._generate_recommendations(
            adjusted_score, detected_patterns  # NEW: Use anti-patterns in recommendations
        )
    )
    
    return result
"""

# ============================================================================
# EXAMPLE 3: Wave-level Analysis and Skill Discovery
# ============================================================================
# File: src/shared/scripts/wave_status_tracker.py (pseudocode)
#
# Location: At end of wave, in mark_wave_complete()
#
# def mark_wave_complete(self, wave_id: str, results: Dict[str, Any]):
#     """Mark a wave as complete and run Coach analysis."""
#     
#     # ... existing completion logic ...
#     
#     # NEW: Run Coach analysis (generates report + skill proposals)
#     from src.shared.coaches import telemetry_collector, skill_governance
#     
#     # Summarize wave telemetry
#     wave_summary = telemetry_collector.collector.summarize_wave(wave_id)
#     logger.info(f"Wave {wave_id} Summary: {wave_summary}")
#     
#     # Propose skills (governance workflow TBD)
#     # skill_governance.propose_skill(...)

EXAMPLE_3_WAVE_ANALYSIS = """
# File: src/shared/scripts/wave_status_tracker.py
# Integration in mark_wave_complete()

from src.shared.coaches import telemetry_collector, skill_governance
import logging

logger = logging.getLogger(__name__)

def mark_wave_complete(self, wave_id: str, results: Dict[str, Any]) -> None:
    '''Mark wave as complete and run Coach analysis.'''
    
    # Existing completion logic
    self.status = "complete"
    self.completed_at = datetime.now()
    
    # NEW: Coach wave analysis
    try:
        # Summarize telemetry for the wave
        wave_summary = telemetry_collector.collector.summarize_wave(wave_id)
        
        logger.info(f"📊 Coach Report: {wave_id}")
        logger.info(f"   Events: {wave_summary.get('event_count', 0)}")
        logger.info(f"   Agents: {', '.join(wave_summary.get('agents_used', []))}")
        logger.info(f"   Cost: ${wave_summary.get('total_cost_usd', 0):.2f}")
        logger.info(f"   Time: {wave_summary.get('total_execution_time_sec', 0):.0f}s")
        
        # Save report to .coach/reports/
        report_path = Path(".coach/reports") / f"{wave_id}-summary.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(wave_summary, indent=2))
        
        logger.info(f"   Report saved: {report_path}")
        
    except Exception as e:
        logger.warning(f"Coach analysis failed: {e}")
"""

# ============================================================================
# TEST EXAMPLES
# ============================================================================

TEST_TELEMETRY_HOOK = """
# Test: Verify telemetry hook works
from src.shared.coaches import telemetry_hook

# Simulate an agent result
agent_result = {
    'model': 'claude-opus-4-1',
    'tokens_input': 12500,
    'tokens_output': 8300,
    'artifact_content': 'Architecture content...' * 1000,
    'artifact_filename': 'architecture.md',
    'execution_time_sec': 130,
    'status': 'success',
    'artifact_lines': 432,
    'artifact_sections': 12,
    'references_entities': 87,
    'validation_passed': True
}

# Log execution
event = telemetry_hook.log_agent_execution(
    agent_id='data-architect',
    wave='test_wave_1',
    gate=1,
    result=agent_result
)

print(f"✅ Event logged: {event['timestamp']}")
print(f"   File: .coach/telemetry/test_wave_1_2026-06-18.jsonl")
"""

TEST_GATE_SCORER = """
# Test: Verify GateScore adjustment works
from src.shared.coaches import gate_scorer

# Simulate artifacts with anti-pattern triggers
artifacts = {
    'entities_discovered': [f'entity_{i}' for i in range(127)],
    'entities_mapped': [f'entity_{i}' for i in range(98)],  # 87% coverage (< 90%)
    'sttm_regenerations': 3,  # Regenerated 3 times (> 2)
    'sttm_timestamps': ['14:40', '14:50', '15:00'],
    'agent_executions': [
        {'agent_id': 'discovery-scout', 'model': 'gpt-4', 'tokens_output': 5000},  # Expensive model
        {'agent_id': 'data-architect', 'model': 'claude-opus-4-1', 'tokens_output': 8000},
    ]
}

# Adjust score
base_score = 0.82
adjusted_score, patterns, adjustments = gate_scorer.adjust_score(
    base_score=base_score,
    wave='test_wave_1',
    gate=2,
    artifacts=artifacts,
    artifact_sizes={'sttm.md': 18300, 'architecture.md': 45600},
    context_window_used_pct=77
)

print(f"Base Score:     {base_score:.4f}")
print(f"Adjusted Score: {adjusted_score:.4f}")
print(f"Adjustment:     {adjusted_score - base_score:+.4f}")
print(f"Anti-patterns:  {len(patterns)}")
for name, impact in adjustments:
    print(f"  - {name}: {impact:+d} pts")

# Expected: 0.82 - 15 (entity gap) - 10 (STTM instability) - 5 (model overreliance) = 0.52
"""

# ============================================================================
# INTEGRATION CHECKLIST
# ============================================================================

INTEGRATION_CHECKLIST = """
✅ Coach Implementation Status (Decision-Based)

DECISION 1: Telemetry Hook in migration-coordinator.spawn_agent()
────────────────────────────────────────────────────────────────
[ ] Read src/shared/scripts/migration-coordinator.py
[ ] Locate spawn_agent() method
[ ] Add telemetry_hook.log_agent_execution() call (AFTER agent execution, BEFORE return)
[ ] Test with example agent (data-architect)
[ ] Verify .coach/telemetry/wave_*.jsonl files created

DECISION 2: GateScore Adjustment in quality-gate.calculate_gatescore()
──────────────────────────────────────────────────────────────────────
[ ] Read src/shared/scripts/gate_score_report.py
[ ] Locate GateScoreCalculator.calculate() method
[ ] Add gate_scorer.adjust_score() call (AFTER base_score, BEFORE status)
[ ] Pass artifacts (entities, STTM regen, executions) as parameters
[ ] Test with example artifacts containing anti-pattern triggers
[ ] Verify adjusted_score used for final status determination
[ ] Validate: score >= 0.85 (approved), 0.70-0.84 (conditional), < 0.70 (blocked)

DECISION 3: Skills Governance (TBD)
────────────────────────────────────
[ ] Define approval workflow (GitHub PR? Jira ticket?)
[ ] Implement skill_finder.discover_patterns()
[ ] Implement skill proposal API
[ ] Create registry for discovered skills
[ ] Automate skill packaging to .github/skills/

TESTING & VALIDATION
────────────────────
[ ] Unit tests for telemetry_hook (test_integration_telemetry.py)
[ ] Unit tests for gate_scorer (test_integration_gatescore.py)
[ ] Integration test on Financeiro Wave 2 historical data
[ ] Verify anti-pattern detection accuracy
[ ] Validate scoring impact (< 0.30 total deduction)

DOCUMENTATION
──────────────
[ ] Update .coach/README.md with integration examples
[ ] Create .coach/INTEGRATION-GUIDE.md (setup instructions)
[ ] Document hook points and expected parameters
[ ] Add troubleshooting guide
"""

if __name__ == "__main__":
    print("DMF Coach Integration Examples")
    print("=" * 60)
    print("\n1. Migration-Coordinator Hook:")
    print(EXAMPLE_1_MIGRATION_COORDINATOR)
    print("\n2. Quality-Gate Adjustment:")
    print(EXAMPLE_2_QUALITY_GATE)
    print("\n3. Wave-Level Analysis:")
    print(EXAMPLE_3_WAVE_ANALYSIS)
    print("\n4. Integration Checklist:")
    print(INTEGRATION_CHECKLIST)
