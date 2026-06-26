# Human-Agent Checkpoints & Escalation Rules — DMF v3

**Version:** 1.0  
**Date:** 2026-06-16  
**Owner:** SRE / Process Lead  

---

## Purpose

Definir **checkpoints explícitos** onde agentes pausam e escalalam para humanos, baseado em confiança (scores de evals), regras de negócio, e impacto. O objetivo é:

- 🟢 **Permitir autonomia** quando agent está confiante (score > threshold)
- 🟡 **Pedir revisão humana** quando agent está incerto (score 0.70–0.75)
- 🔴 **Bloquear e alertar** quando agent está claramente quebrado (score < 0.50)

---

## Escalation Rule Framework

### Three-Tier Model

```
┌─ TIER 1: Auto-Approve (High Confidence)
│  Condition: output_quality > 0.85 AND trajectory_quality > 0.80
│  Action: Proceed to next gate; no human review needed
│  Example: "Data model validates perfectly, agent took expected steps"
│
├─ TIER 2: Human Review (Medium Confidence)
│  Condition: 0.70 ≤ output_quality ≤ 0.85 OR trajectory_quality in [0.70, 0.80]
│  Action: Escalate to human; allow retry OR manual fix
│  Example: "Model is correct but agent took inefficient path; let architect review"
│  SLA: 60 minutes (prioritized over new work)
│  Allow Retry: YES (agent can try again after hints)
│
└─ TIER 3: Critical Escalation (Low Confidence)
   Condition: output_quality < 0.70 OR trajectory_quality < 0.50
   Action: BLOCK; alert all engineers; require manual fix
   Example: "Agent produced invalid YAML; security violation detected"
   SLA: 15 minutes (interrupt on-call)
   Allow Retry: NO (human must understand issue first)
```

---

## Gate-Specific Rules

### Gate 1: Requirements & Planning

**Goal:** Ensure discovery is complete, STTM accurate, DQ rules captured.

```yaml
gate1_escalation_rules:
  - name: "incomplete_discovery"
    condition: "output_quality < 0.75"
    reason: "Missing entities or data lineage gaps"
    action: "escalate_to_discovery_owner"
    priority: "high"
    sla_min: 120  # 2 hours for re-discovery
    allow_retry: true
    retry_hint: "Re-run discovery-scout with expanded scope"
    
  - name: "sttm_ambiguity"
    condition: "trajectory_quality < 0.70 AND compliance > 0.80"
    reason: "STTM logic is unclear; agent took questionable assumptions"
    action: "escalate_for_manual_sttm_refinement"
    priority: "medium"
    sla_min: 60
    allow_retry: true
    reviewer: "business_analyst"
    
  - name: "dq_rules_incomplete"
    condition: "compliance < 0.80"
    reason: "DQ validator didn't capture all business rules"
    action: "block + alert_data_steward"
    priority: "critical"
    sla_min: 15
    allow_retry: false
```

### Gate 2: Design & Architecture

**Goal:** Ensure data model, architecture decisions, and code are sound.

```yaml
gate2_escalation_rules:
  - name: "normalization_issue"
    condition: "output_quality in [0.75, 0.85] AND compliance > 0.85"
    reason: "Schema design is sound but not optimally normalized"
    action: "escalate_for_optional_refinement"
    priority: "low"
    sla_min: 240  # 4 hours; can defer to next wave
    allow_retry: true
    reviewer: "data_architect"
    
  - name: "bad_code_generation"
    condition: "output_quality < 0.70 OR compliance < 0.75"
    reason: "Generated DDL/ETL has syntax errors or anti-patterns"
    action: "block + alert_code_owner"
    priority: "critical"
    sla_min: 30
    allow_retry: true
    retry_hint: "Fix guardrails; re-run code-generator with corrected tools"
    
  - name: "architecture_mismatch"
    condition: "trajectory_quality < 0.60"
    reason: "Agent ignored architectural constraints"
    action: "escalate_to_architect + block"
    priority: "critical"
    sla_min: 15
    allow_retry: false
    reason_codes: ["ignored_constraints", "violated_data_residency", "missed_security_requirement"]
```

### Gate 3: Testing & Deployment

**Goal:** Ensure reconciliation passes, no data loss, safe to go live.

```yaml
gate3_escalation_rules:
  - name: "reconciliation_warnings"
    condition: "output_quality in [0.80, 0.90] AND compliance >= 0.90"
    reason: "Reconciliation passed but with warnings (e.g., 5% variance)"
    action: "escalate_for_review + allow_conditional_approval"
    priority: "high"
    sla_min: 45
    allow_retry: false
    requires_approval: "ops_lead"
    can_override: true
    override_reason_required: true
    
  - name: "reconciliation_failure"
    condition: "output_quality < 0.80"
    reason: "Data mismatch or schema inconsistency detected"
    action: "block_deployment"
    priority: "critical"
    sla_min: 15
    allow_retry: true
    retry_hint: "Validate source data; check ETL logic; re-run reconciliation"
    escalated_to: ["data_engineer", "ops_lead"]
    
  - name: "performance_risk"
    condition: "trajectory_quality < 0.65 AND output_quality in [0.75, 0.85]"
    reason: "Query might be inefficient; could cause production slowdown"
    action: "escalate_for_performance_review + allow_deployment_with_monitoring"
    priority: "medium"
    sla_min: 60
    allow_retry: true
    condition_for_approval: "agrees_to_monitor_and_optimize_within_48h"
```

---

## Escalation Workflow

### Step 1: Checkpoint Evaluation

```python
class EscalationEngine:
    def evaluate_checkpoint(self, gate: int, eval_result: Dict) -> EscalationDecision:
        """Determine if agent can proceed or must escalate."""
        
        output_quality = eval_result["output_quality"]
        trajectory_quality = eval_result["trajectory_quality"]
        compliance = eval_result["compliance"]
        
        # Determine tier
        if output_quality > 0.85 and trajectory_quality > 0.80:
            return EscalationDecision(
                tier="auto_approve",
                action="proceed",
                reason="High confidence on all metrics"
            )
        
        elif 0.70 <= output_quality <= 0.85 or 0.70 <= trajectory_quality <= 0.80:
            # Look up gate-specific rules
            rule = self.get_escalation_rule(gate, output_quality, trajectory_quality, compliance)
            return EscalationDecision(
                tier="human_review",
                action=rule["action"],
                priority=rule["priority"],
                sla_min=rule["sla_min"],
                reviewer=rule["reviewer"],
                allow_retry=rule["allow_retry"]
            )
        
        else:  # Tier 3
            return EscalationDecision(
                tier="critical",
                action="block_and_alert",
                priority="critical",
                sla_min=15,
                escalated_to=["oncall_engineer", "architect"],
                allow_retry=False,
                reason_code=self.diagnose_failure(eval_result)
            )
```

### Step 2: Human Routing

```yaml
# Escalation routing matrix
routing:
  gate_1_discovery_owner: "team:data-discovery"  # Slack channel
  gate_1_business_analyst: "team:business-analysis"
  gate_2_data_architect: "team:data-platform-arch"
  gate_2_code_owner: "team:data-engineering"
  gate_3_ops_lead: "team:operations"
  gate_3_data_engineer: "team:data-engineering"
  
escalation_template:
    priority: "high|medium|low"
    sla_minutes: 60
    message: |
      🔴 Escalation: Gate {{ gate }} {{ checkpoint_name }}
      Wave: {{ wave_id }}
      Issue: {{ reason }}
      
      Eval Scores:
      - Output Quality: {{ output_quality }}
      - Trajectory Quality: {{ trajectory_quality }}
      - Compliance: {{ compliance }}
      
      Action Taken: {{ action }}
      Allow Retry: {{ allow_retry }}
      {% if allow_retry %}
        Retry Hint: {{ retry_hint }}
      {% endif %}
      
      Artifacts: {{ artifact_links }}
```

### Step 3: Human Decision

```
┌─ Human Receives Alert (Slack/Teams)
│  
├─ Option 1: APPROVE
│  └─ Update gate decision record
│     └─ Mark for next phase
│  
├─ Option 2: REQUEST CHANGES
│  └─ Leave comment in PR
│  └─ Agent can RETRY (if allowed)
│  
└─ Option 3: OVERRIDE (Rare)
   └─ Document override reason
   └─ Add to audit trail
   └─ Alert compliance team
```

### Step 4: Retry Loop (if allowed)

```
Retry triggered by human feedback
  ↓
Agent re-runs with updated context
  ↓
New evals generated
  ↓
Score improved?
  ├─ YES → Proceed to gate approval
  └─ NO → Back to human (escalate to architect)
```

---

## Audit Trail

Every escalation decision is logged:

```json
{
  "escalation_id": "esc-a7f3-92c1-4e8b",
  "trace_id": "a7f3-92c1-4e8b-11d7-5fk2m9p0",
  "gate": 2,
  "wave": "Financeiro-g1",
  "checkpoint_name": "bad_code_generation",
  "tier": "critical",
  "eval_scores": {
    "output_quality": 0.65,
    "trajectory_quality": 0.72,
    "compliance": 0.68
  },
  "action": "block_and_alert",
  "escalated_to": ["code_owner", "architect"],
  "priority": "critical",
  "sla_minutes": 30,
  "created_at": "2026-06-16T14:32:15Z",
  "human_response": {
    "reviewer": "carlos.silva",
    "decision": "request_changes",
    "comment": "Generated DDL uses wrong data types; please retry with updated tool definitions",
    "responded_at": "2026-06-16T14:45:00Z"
  },
  "retry_triggered": true,
  "retry_result": {
    "new_eval_scores": {
      "output_quality": 0.88,
      "trajectory_quality": 0.85,
      "compliance": 0.90
    },
    "status": "approved"
  }
}
```

---

## SLA Management

### Per-Tier SLAs

| Tier | SLA | Metric | Alert if Missed |
|------|-----|--------|---|
| Auto-Approve | Immediate | n/a | n/a |
| Human Review | 60 min | % reviews closed within SLA | Dashboard + Slack |
| Critical | 15 min | % escalations acknowledged | PagerDuty |

### SLA Breaches

```yaml
sla_breach_policy:
  - tier: "human_review"
    breach_after_min: 90  # 50% over SLA
    action: "escalate_up_chain"
    alert: "escalation_queue@company.com"
    
  - tier: "critical"
    breach_after_min: 20  # 30% over SLA
    action: "page_oncall"
    alert: "pagerduty_incident"
```

---

## Metrics & Reporting

### Weekly Escalation Report

```
Period: 2026-06-09 to 2026-06-16

Total Checkpoints Evaluated: 342
  ├─ Auto-Approved (Tier 1): 258 (75%)
  ├─ Human Reviewed (Tier 2): 72 (21%)
  │  ├─ Approved as-is: 45
  │  ├─ Approved with changes: 18
  │  └─ Rejected (awaiting redesign): 9
  └─ Critical (Tier 3): 12 (4%)
     ├─ Resolved: 8
     ├─ Pending: 4
     └─ Escalated to architects: 3

Human Review SLAs:
  ├─ Met: 68/72 (94%)
  ├─ Missed: 4/72 (6%)
  └─ Avg Response Time: 32 min (SLA: 60 min)

Critical SLAs:
  ├─ Met: 11/12 (92%)
  ├─ Missed: 1/12 (8%)
  └─ Avg Response Time: 18 min (SLA: 15 min)

Top Escalation Reasons:
  1. "normalization_issue" (28%)
  2. "trajectory_quality_low" (18%)
  3. "compliance_violation" (16%)
  4. "incomplete_discovery" (12%)
  5. Other (26%)

Agent Performance (Tier 1 Auto-Approve Rate):
  ├─ data-modeler: 82%
  ├─ logic-extractor: 65%
  ├─ code-generator: 78%
  ├─ quality-gate: 91%
  └─ reconciliation: 88%
```

---

## Exception Handling

### Timeout: Agent Never Completes

```yaml
timeout_rule:
  max_duration_sec: 600  # 10 minutes
  action_on_timeout: "escalate_to_human + suggest_fallback"
  fallback: "manual_implementation"
  notify: ["architect", "oncall"]
```

### Deadlock: Human Keeps Requesting Changes (> 3 iterations)

```yaml
deadlock_rule:
  max_retries: 3
  action_on_deadlock: "escalate_to_architect + auto_approve_with_caveat"
  caveat: |
    ⚠️ CAVEAT: This gate was auto-approved after 3 human rejections.
    Recommended post-wave review: re-examine agent instructions or guardrails.
  notify: ["process_owner"]
```

---

## Implementation Checklist

- [ ] Define eval score thresholds per gate (with SME input)
- [ ] Implement `EscalationEngine` class + routing logic
- [ ] Set up Slack/Teams integration for alerts
- [ ] Create audit trail table (SQL or CosmosDB)
- [ ] Build SLA dashboard (PowerBI)
- [ ] Test retry loop with sandbox agents
- [ ] Document runbook for "SLA breach escalation"
- [ ] Train on-call team on checkpoint decisions
- [ ] Run dry-run on Financeiro wave; collect feedback

---

**Related Docs:**
- `HARNESS-MANIFEST.md` (Guardrails & Orchestration)
- `OBSERVABILITY-AND-TRACES.md` (Use traces to diagnose failures)
- `HARNESS-CHANGELOG.md` (Change: "Trajectory Evals Added")
