# Data Migration Factory v3 — Copilot Instructions

## What This Project Is

A **multi-agent migration factory** for data platform migrations. The full lifecycle (UPSTREAM → MIDSTREAM → DOWNSTREAM) is orchestrated by specialized AI agents, validated by three mandatory quality gates with measurable scores.

```
UPSTREAM (Gate 1)  →  MIDSTREAM (Gate 2)  →  DOWNSTREAM (Gate 3)
Discovery               Architecture             Execution
STTM + DQ Rules         Data Model + Code        Reconciliation
```

GateScore formula: `0.35 × Completude + 0.25 × Qualidade + 0.20 × RiscoResidual + 0.20 × Reconciliação`  
Threshold: >= 0.85 approved | 0.70–0.84 approved with open items | < 0.70 blocked.

## Architecture

- **19 agents** in `.github/agents/` — one per specialization (e.g., `discovery-scout`, `data-architect`, `downstream-executor`). Note: `orchestrator` is deprecated — use `migration-coordinator` instead.
- **26 skills** in `.github/skills/` — domain knowledge loaded on demand
- **23 governance scripts** in `scripts/` — Python modules with 189 automated tests
- **Docs** in `docs/` — playbooks, operating model, agent guide, skills blueprint

See [README.md](../README.md) for project overview.

## Agent Entry Point

When unsure which agent to use, always start with `master-agent` and run `*route`. It will recommend the correct agent for the current context.

Agent map: [docs/COPILOT-AGENTS-GUIDE.md](docs/COPILOT-AGENTS-GUIDE.md)

## Build and Test

```powershell
# Setup (once per machine)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest pyyaml

# Run all governance tests
python -m pytest tests/ -q
# Expected: 189 passed
```

Always activate `.venv` before running any Python script. If `pyyaml` is missing, 8 tests fail — install it.

## Scripts Reference

Do not edit scripts without running tests after. All 23 modules in `scripts/` are covered by tests in `tests/`. See [scripts/README.md](../scripts/README.md) for module descriptions.

Key scripts:
- `scripts/validate_wave_config.py` — validates wave YAML config
- `scripts/validate_gate1_artifacts.py` — validates Gate 1 artifact package
- `scripts/validate_gate2_artifacts.py` — validates Gate 2 artifact package
- `scripts/validate_gate3_artifacts.py` — validates Gate 3 artifact package (also contains generic `validate_gate_requirements()`)
- `scripts/gate_score_report.py` — calculates GateScore
- `scripts/wave_status_tracker.py` — consolidated wave status across gates
- `scripts/kpi_dashboard_report.py` — wave KPI dashboard report
- `scripts/quality_thresholds.py` — entity-tier quality thresholds
- `scripts/validate_agent_contracts.py` — structural contract validator for chatmode agents
- `scripts/governance_policy.py` — programmatic governance policy engine
- `scripts/data_contract_validator.py` — declarative data contract validation

## Conventions

- **Wave config:** every migration wave requires a `wave-config.yaml` validated by `validate_wave_config.py` before Gate 1
- **Gate decisions:** record in `gate{N}-decision.md` with score, approvers, and open items
- **Agent outputs:** store in `<agent-name>-agent/<domain>-outputs/`
- **Discovery ownership:** each wave has exactly one `discovery_owner` in wave-config; `inventory-scout` is fallback only
- **Platform agnostic:** do not hardcode Databricks, Fabric, or Snowflake in agent instructions or scripts — use `(inform target platform)` or receive via prompt
- **Coordinator hierarchy:** `master-agent` = user triage + KB; `migration-coordinator` (Orion) = wave orchestration + gates. Do NOT use `orchestrator` (deprecated).
- **Artifact ownership:** Winston (DataArchitect) owns `architecture.md`, `decisions.md`, `monitoring-spec.md`. Sofia (DataModeler) owns `data-model.md`, `data-contracts.md`, `metrics-catalog.md`.

## Docs Index

| Document | Purpose |
|---|---|
| [docs/PLAYBOOK-ONBOARDING.md](docs/PLAYBOOK-ONBOARDING.md) | New team member setup guide |
| [docs/PLAYBOOK-MIGRATION-OPERATIONS.md](docs/PLAYBOOK-MIGRATION-OPERATIONS.md) | Step-by-step migration wave execution |
| [docs/COPILOT-AGENTS-GUIDE.md](docs/COPILOT-AGENTS-GUIDE.md) | Full command reference per agent |
| [docs/OPERATING-MODEL-CANVAS-v2.md](docs/OPERATING-MODEL-CANVAS-v2.md) | Agent roles, permissions, governance |
| [docs/SKILLS-BLUEPRINT-BY-GATE.md](docs/SKILLS-BLUEPRINT-BY-GATE.md) | Skills mapped to each gate |
| [docs/PRD-Agentic-Data-Migration-Factory.md](docs/PRD-Agentic-Data-Migration-Factory.md) | Requirements and acceptance criteria |
