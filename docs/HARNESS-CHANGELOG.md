# Harness Changelog — DMF v3

**Purpose:** Track all changes to harness components (rules, tools, guardrails, observability) with rationale, impact, and rollback plan.

Format: `YYYY-MM-DD | Component | Version | Impact | Approver | Notes`

---

## 2026-06-16 | Harness Formalization

**Change:** Introduced Harness Manifest as first-class governance artifact.

**Rationale:** 
- Paper analysis revealed harness accounts for ~70% of agent behavior; model only ~30%.
- Current setup is implicit (scattered across scripts, skills, instructions). Risk: "We don't know what we have."
- Formalization enables version control, impact tracking, regression testing.

**Component Versions Updated:**
- `static_context` → v1.0 (AGENTS.md + copilot-instructions.md)
- `tools` → v1.0 (23 governance scripts catalogued)
- `hooks` → v1.0 (pre-commit, post-file-write, before-tool-call)
- `observability` → v1.0 (traces + cost tracking initialized)

**Impact:** Medium
- No functional changes (yet)
- Adds audit trail for future changes
- Requires 1-2 hr onboarding per team member

**Approver:** architecture-board  
**Rollback:** N/A (documentation-only change)

**Related:** `docs/HARNESS-MANIFEST.md`

---

## 2026-06-16 | Skills Versioning Introduced

**Change:** Added versioning to `.github/skills/ava-dmf-*` with pinning in wave-config.

**Rationale:**
- Skills currently unversioned; wave-to-wave incompatibilities untracked.
- Error: agent uses v1.x skill, next wave loads v2.x (breaking), nobody notices until gate fails.
- Solution: pin versions + auto-fallback.

**Schema Changes:**
```yaml
# OLD
skills:
  - ava-dmf-data-quality
  
# NEW
skills:
  - name: ava-dmf-data-quality
    version: "2.1.3"
    fallback_to: "2.0.0"  # if 2.1.3 unavailable
```

**Impact:** Low
- Backward-compatible (unpinned = auto-resolve to latest)
- Requires wave-config updates for new waves
- Improves reproducibility

**Approver:** data-architect, code-owner  
**Rollback:** Remove version tags from skill files; revert wave-config.

**Related:** `src/shared/schemas/wave-config-extended.yaml`

---

## 2026-06-16 | Trajectory Evals Added to Gate Validation

**Change:** Gate validators now return multi-dimensional scores: `{output_quality, trajectory_quality, compliance}`.

**Rationale:**
- Current evals: binary (pass/fail). Can't distinguish: "Wrong output but good process" vs. "Right output, wrong process."
- Paper emphasizes: **trajectory evaluation** (did agent take right steps?) + **output evaluation** separately.
- Risk: agent hacks a solution (output correct, trajectory wrong); hard to detect until production.

**Schema:**
```python
# OLD
gate_result = {"passed": true, "score": 0.85}

# NEW
gate_result = {
    "passed": True,
    "gate_score": 0.85,  # composite (backward-compat)
    "output_quality": 0.90,  # did output meet spec?
    "trajectory_quality": 0.75,  # did agent take right steps?
    "compliance": 0.88,  # did agent follow guardrails?
    "audit_trail": [  # trajectory steps
        {"step": 1, "action": "call validate_data_contracts", "duration": 2.3},
        {"step": 2, "action": "parse result", "duration": 0.1},
        {"step": 3, "action": "escalate to human", "reason": "warnings > 10"}
    ]
}
```

**Impact:** Medium
- Changes `wave_status_tracker` reporting format
- Enables better root-cause analysis (trajectory vs. output failures)
- Requires updating eval rubrics (what counts as "good trajectory"?)

**Approver:** quality-gate-owner  
**Rollback:** Keep both formats; use `gate_score` field for backward-compat.

**Related:** `HUMAN-AGENT-CHECKPOINTS.md` (escalation rules now use trajectory score)

---

## 2026-06-16 | Observability: Distributed Traces Enabled

**Change:** All agent invocations now generate trace IDs; spans logged to Application Insights.

**Rationale:**
- Current: logs per agent, per wave. Hard to correlate: "Which agent call triggered this downstream cost?"
- Paper emphasizes: observability as part of harness. "Without it, no way to tell if agent drifting."
- Need: trace ID linking agent → tool calls → sub-agent invocations → gate validator.

**Data Model:**
```json
{
  "trace_id": "a7f3-92c1-4e8b-11d7-5fk2m9p0",
  "span_id": "parent-perceive-001",
  "agent": "data-modeler",
  "wave": "bradesco-g1",
  "gate": 2,
  "timestamp": "2026-06-16T14:30:42Z",
  "events": [
    {
      "span_name": "perceive",
      "duration_ms": 4200,
      "tokens_input": 12450,
      "tokens_output": 3200,
      "model": "claude-opus-4"
    },
    {
      "span_name": "tool_call_validate_data_contracts",
      "duration_ms": 2300,
      "cost_usd": 0.05,
      "result": "3_errors_45_warnings"
    }
  ],
  "metrics": {
    "total_cost_usd": 0.48,
    "total_duration_sec": 18.5,
    "success": false,
    "escalated_to_human": true
  }
}
```

**Impact:** Medium
- Requires new `trace_context` middleware in agent orchestration
- Application Insights cost: +~$5-10/month (acceptable)
- Enables cost attribution per agent/gate
- Privacy: traces do NOT include sensitive data (use obfuscation rules)

**Approver:** observability-lead, security-team  
**Rollback:** Disable trace logging in orchestrator config; keep schema for future.

**Related:** `OBSERVABILITY-AND-TRACES.md`

---

## 2026-06-16 | Human-Agent Checkpoints: Escalation Rules

**Change:** Added checkpoint rules; agents auto-escalate based on confidence thresholds.

**Rationale:**
- Paper: "Orchestrator mode requires explicit handoff protocols."
- Current: All agent failures go to human equally. Need priority routing.
- Example: trajectory_quality = 0.72 (barely below 0.75) → prioritize for human review. trajectory_quality = 0.15 (clearly broken) → immediate escalation + alert.

**Rule Engine:**
```yaml
checkpoints:
  - gate: 1
    escalation_rule:
      if: "output_quality < 0.75"
      then: "escalate_to_human"
      priority: "high"
      sla_min: 30
      
  - gate: 2
    escalation_rules:
      - if: "trajectory_quality < 0.70 AND compliance > 0.85"
        then: "escalate_for_review"
        priority: "medium"
        allow_auto_retry: true
      - if: "trajectory_quality < 0.50"
        then: "alert_all + escalate_to_architect"
        priority: "critical"
        allow_auto_retry: false
        
  - gate: 3
    escalation_rules:
      - if: "output_quality < 0.80"
        then: "block_deployment"
        reason: "post-deployment gate requires high confidence"
```

**Impact:** High
- Changes agent autonomy boundaries
- Requires on-call setup for escalations
- Better observability of where humans spend time

**Approver:** engineering-leadership  
**Rollback:** Set all escalation thresholds to 0 (no auto-escalation); fall back to manual triage.

**Related:** `HUMAN-AGENT-CHECKPOINTS.md`

---

## 2026-06-15 | Context Rot Audit — Initial Baseline

**Change:** Measured static context size and complexity; documented drift risk.

**Rationale:**
- `.github/copilot-instructions.md` is 8.5 KB (good). 
- Total skill files: 26 × average 3 KB = 78 KB. If all loaded at once = waste.
- Risk: If developer adds "just one more agent" without cleaning up, static context grows unbounded.

**Baseline Metrics:**
- Static context: 8.5 KB (copilot-instructions)
- Dynamic context (per-task): avg 12.5 KB (skills + tool definitions)
- Wasted context: 0 KB (well-managed so far)

**Action Items:**
- Set monthly audit to flag if static context > 25 KB
- Document skills usage (which agents load which skills)
- Schedule quarterly "context cleanup" sprint

**Impact:** Low (observational only)

**Approver:** tech-lead  
**Rollback:** N/A

**Related:** `HARNESS-MANIFEST.md` (Policy: Context Rot Detection)

---

## Template for Future Changes

```markdown
## YYYY-MM-DD | Component | Brief Title

**Change:** What changed?

**Rationale:** Why?

**Component Versions Updated:**
- `component_name` → version

**Impact:** Low / Medium / High

**Approver:** team-member  
**Rollback:** How to undo?

**Related:** Link to docs
```

---

## Summary

| Date | Change | Impact | Status |
|------|--------|--------|--------|
| 2026-06-16 | Harness Formalization | Medium | ✅ Active |
| 2026-06-16 | Skills Versioning | Low | ✅ Active |
| 2026-06-16 | Trajectory Evals | Medium | ✅ Active |
| 2026-06-16 | Distributed Traces | Medium | ✅ Active |
| 2026-06-16 | Human-Agent Checkpoints | High | ✅ Active |
| 2026-06-15 | Context Rot Audit | Low | ✅ Baseline |

---

**Last Updated:** 2026-06-16  
**Owner:** Architecture Board
