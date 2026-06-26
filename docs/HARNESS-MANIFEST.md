# Harness Manifest — DMF v3 Agentic Engineering

**Version:** 1.0  
**Date:** 2026-06-16  
**Author:** AI Architecture  
**Status:** Active

---

## Purpose

Formalizar o **Harness** como artefato de primeira-classe na Data Migration Factory. O Harness é o sistema de constraints, verificação e orquestração que rodeia cada modelo de agente e garante comportamento determinístico, auditável e seguro.

**Equação do Paper (Google, 2026):**
```
Agent = Model (reasoning engine) + Harness (everything else)
Comportamento observado ≈ 70% Harness + 30% Model
```

---

## Componentes do Harness DMF

### 1. **Instructions & Rule Files** (Camada Estática)

| Artefato | Proprietário | Localização | Escopo |
|----------|---|---|---|
| `AGENTS.md` | master-agent | `.github/` | Rol global de agents, modos, restrições |
| `.claude.md` / `.copilot-instructions.md` | orchestrator | `.github/` | Regras de sistema (Microsoft-only, 8k char limit, PT-BR conventions) |
| Skill files | skill author | `.github/skills/ava-dmf-*` | Conhecimento procedural por módulo |
| Wave rules | wave-architect | `projects/<project>/wave-config.yaml` | Políticas específicas da wave |

**Princípio:** Static context é carregado em TODA interação. Mínimo sinal + máxima performance.

### 2. **Tools & MCP Servers** (Camada de Execução)

```
Tools Categories:
├─ File Operations (read, write, search)
├─ Execution Environments (sandbox, terminal, Python REPL)
├─ Governance Scripts (validate_gate*.py, gate_score_report.py)
├─ External APIs (Azure, GitHub, Dataverse)
└─ Sub-Agent Invocation (delegation via master-agent)
```

**Cada tool tem:**
- Assinatura precisa (inputs/outputs tipados)
- Guardrails (o que PODE fazer, o que NÃO PODE)
- Audit logging (quem, quando, para quê)

### 3. **Sandboxes & Execution Boundaries**

| Sandbox | Acesso | Restrições | Monitoramento |
|---------|--------|-----------|---|
| **Local Dev** | Filesystem + Python environment | Nenhuma restrição (dev) | Logs locais |
| **CI/CD Pipeline** | Controlled file set + approved scripts | No access to secrets (use Azure Key Vault) | GitHub Actions logs + Azure Monitor |
| **Cloud Agent Runtime** (Foundry) | Network-scoped; MCP-mediated tools | RBAC via Entra ID; data residency rules | Distributed traces; cost tracking |

### 4. **Orchestration Logic** (Multi-Agent Choreography)

```
Entry: master-agent (*route command)
  ├─ Fingerprint document (BRD vs FDD vs Architecture)
  ├─ Recommend playbook sequence
  ├─ Load skill by context
  └─ Invoke specialized agent (01-11 or 12-16)
      ├─ Agent perceives goal
      ├─ Calls tools (with audit logging)
      ├─ Observes results
      ├─ Iterates OR escalates (see: Human-Agent Checkpoints)
      └─ Return to orchestrator for next phase
```

**Routing rules in orchestrator:**
- Task ∉ wave scope → warn user
- AI-scope = no + agent (13 or 16) → escalate to human
- Agent error rate > threshold → fall back to simpler model

### 5. **Guardrails & Hooks** (Deterministic Safeguards)

**Hooks** execute at lifecycle events:

```python
# Before tool call
@hook.before_tool_call
def validate_tool_permissions(agent_id, tool_name, args):
    """Ensure agent has permission; block secrets"""
    if "password" in str(args):
        raise SecurityError("No hardcoded secrets allowed")

# After file edit
@hook.after_file_write
def enforce_code_style(file_path, new_content):
    """Run formatters, linters, validate syntax"""
    fmt = format_bicep(file_path, new_content) if file_path.endswith('.bicep')
    return fmt

# Before commit
@hook.before_commit
def verify_gate_readiness(commit_msg, files_changed):
    """Ensure all gate validators pass before commit"""
    if "gate1" in commit_msg:
        result = validate_gate1_artifacts(files_changed)
        return result.score >= 0.85
```

**Built-in Guardrails:**
- ✅ No hardcoded credentials (block patterns: `password=`, `key=`, AWS secret formats)
- ✅ No `rm -rf` or destructive commands without human approval
- ✅ No commits to `main` branch without gate approval
- ✅ All file writes logged with before/after diff
- ✅ Tool execution timeout (default: 5min; configurable per tool)

### 6. **Observability: Logs, Traces, Metrics** (HITL Feedback Loop)

```
┌─ Trace ID (unique per agent invocation)
│  ├─ Agent: data-modeler
│  ├─ Wave: Financeiro-g1
│  ├─ Gate: 2
│  ├─ Session: 2026-06-16T14:30:42Z
│  │
│  ├─ Span: perceive (LLM called, context tokens: 12,450)
│  ├─ Span: plan (tool sequence decided)
│  ├─ Span: tool_call (name: validate_data_contracts, duration: 2.3s)
│  ├─ Span: observe (result: 3 errors, 45 warnings)
│  ├─ Span: iterate (LLM re-plan based on errors)
│  │
│  └─ Metrics:
│      ├─ tokens_input: 12,450
│      ├─ tokens_output: 3,200
│      ├─ cost_usd: $0.48
│      ├─ duration_sec: 18.5
│      ├─ success: false (escalated to human)
│      └─ drift_score: 0.12 (within 1σ of baseline)
```

---

## Harness per Phase

### Gate 1: Requirements & Planning (Configuring)

| Component | Role | Check |
|-----------|------|-------|
| Wave config | Define guardrails, tools available, skill versions | ✅ validate_wave_config.py |
| Agent instructions | Load skills for discovery agents | ✅ Syntax check + skill manifest validation |
| Data contracts stub | Prepare schemas that agents will populate | ✅ Schema valid per Purview rules |

### Gate 2: Design & Architecture (Running)

| Component | Role | Check |
|-----------|------|-------|
| Execution sandbox | Code runs in isolated environment | ✅ No network access except MCP |
| Tools + guardrails | Agent can call validate_data_contracts, etc. | ✅ Tool permission matrix (RBAC) |
| Hooks (post-file-write) | Format + validate each change | ✅ Hook output recorded in trace |
| Observability | Continuous logging | ✅ Traces routed to Application Insights |

### Gate 3: Testing & Deployment (Feedback Loop)

| Component | Role | Check |
|-----------|------|-------|
| Evals (trajectory + output) | Did agent take the right steps? Did output meet spec? | ✅ Eval scores in wave_status_tracker |
| Rollback hooks | If post-deployment, revert bad changes | ✅ Git reset + artifact restore tested |
| Monitoring | Production behavior differs from dev? | ✅ Anomaly detection on metrics |

---

## Governance Policies in the Harness

### Policy: "No Human in the Loop = No Production"

**Rule:** Agents operating in **Orchestrator mode** (async, autonomous) MUST have:
- ✅ 100% test coverage of their outputs (unit + integration + property-based)
- ✅ Eval suite with ≥2 human-labeled reference examples per task type
- ✅ Checkpoint rule: if eval score < 0.75, escalate to human (see: Human-Agent Checkpoints)
- ✅ Rollback plan documented in `deployment-decision.md`

**Violation:** If any missing, agent downgrades to **Conductor mode** (human-supervised, real-time).

### Policy: "Skills are Versioned; No Breaking Changes"

**Rule:** Once a skill is released (added to `.github/skills/ava-dmf-*`):
- ✅ Bug fixes go to same version (v1.2.3 → v1.2.4)
- ✅ New capabilities go to minor bump (v1.2.3 → v1.3.0)
- ✅ Breaking changes go to major bump (v1.2.3 → v2.0.0) + deprecation notice
- ✅ Wave config pins skill version: `skill: ava-dmf-data-quality@v1.2.3`
- ✅ Fallback: if pinned version unavailable, auto-downgrade to last stable

### Policy: "Context Rot Detection"

**Rule:** Monthly audit of harness components:
- ✅ Static context size: Alert if > 25KB (wasted tokens)
- ✅ Skill count: Alert if > 20 active in one agent (progressive disclosure failing)
- ✅ Tool permissions: Alert if agent has access to tools not used in last 30 days
- ✅ Hook execution time: Alert if pre-commit hooks > 30 sec (slows developer)

**Action:** Harness rebalancing (move static → dynamic, deprecate unused tools).

---

## Harness Change Control

**Every harness change requires:**
1. **Rationale** — why this change?
2. **Impact assessment** — which agents, which waves affected?
3. **Regression testing** — evals pass on baseline?
4. **Approval** — architect sign-off required (via PR review)
5. **Changelog entry** — recorded in `HARNESS-CHANGELOG.md`

**Harness changes that DON'T require regression testing:**
- Adding new (unused) tools
- Updating error messages
- Adding observability metrics (non-blocking)

**Harness changes that ALWAYS require testing:**
- Modifying guardrails (e.g., blocking a tool)
- Changing skill loading logic
- Updating validation rules

---

## Harness as Code

```yaml
# harness-spec.yaml (new, version-controlled)
harness:
  version: "1.0.0"  # Harness schema version
  updated: "2026-06-16"
  
  static_context:
    - file: ".github/copilot-instructions.md"
      size_bytes: 8500
      role: "global rules"
    - file: ".github/AGENTS.md"
      size_bytes: 12300
      role: "agent registry"
    
  tools:
    - name: "validate_gate1_artifacts"
      category: "governance"
      available_to: ["discovery-scout", "inventory-scout"]
      timeout_sec: 300
      cost_estimate_usd: 0.05
      
  sandboxes:
    - name: "dev-local"
      restrictions: "none"
      audit_logging: "local"
    - name: "ci-pipeline"
      restrictions: "no-secrets; approved-scripts-only"
      audit_logging: "github-actions + application-insights"
      
  hooks:
    - event: "before_tool_call"
      handler: "validate_tool_permissions"
      critical: true
    - event: "after_file_write"
      handler: "enforce_code_style"
      critical: false
      
  policies:
    - name: "no-vibe-coding-in-production"
      severity: "CRITICAL"
      check: "eval_score >= 0.75 OR human_approved"
    - name: "skill-versioning"
      severity: "HIGH"
      check: "all_skills_pinned_to_version"
```

---

## Adoption Checklist

- [ ] Create `harness-spec.yaml` template
- [ ] Document all 23 governance scripts in harness context
- [ ] Implement trace ID propagation (correlation across agents)
- [ ] Set up cost attribution per agent/gate/wave
- [ ] Build drift detection baseline (compare agent behavior month-over-month)
- [ ] Train engineers: "Harness failures, not model failures"
- [ ] Migrate `validate_*.py` scripts to return trajectory scores (not just pass/fail)

---

**Next:** See `HARNESS-CHANGELOG.md` for version history and change rationale.
