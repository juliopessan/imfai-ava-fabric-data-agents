# SDD: migration-coordinator (Orchestrate Wave)

**Role:** Orchestrate multi-agent workflow. Manage gates, dependencies, escalation.

---

## Input Contract

```
Required:
  ├─ wave_config.yaml: File — projects/[project]/wave-config.yaml
  ├─ project_name: String — Financeiro|Reference-Sa�de|multi-platform
  ├─ phase: String — discovery|architecture|deployment|consolidation
  └─ start_phase: String — where to begin

Optional:
  └─ skip_gates: Boolean — false (always validate)
```

---

## Task Definition

1. **Load** wave config
2. **Route** to discovery-scout → data-architect → business-analyst → ...
3. **Wait** for gate validation between phases
4. **Escalate** if gate score < 0.85
5. **Track** wave state (progress, blockers, risks)
6. **Generate** consolidated wave report

---

## Success Criteria

- ✅ All phases completed
- ✅ All gate scores >= 0.85
- ✅ No blockers
- ✅ Consolidated report generated

---

## Output

```
Produces:
  ├─ wave-status.json: {phase, status, gates, blockers}
  ├─ wave-summary.md: Executive overview
  └─ consolidated-report.html: All phase dashboards

Location: projects/[project]/outputs/
Passes To: downstream-executor (if go-live approved)
```

---

## Constraints

🔴 NEVER skip gate validation  
🔴 ESCALATE if score < 0.85 (human decision)  
🔴 Maintain wave state (resume capability)  
🔴 Track all decisions in wave-decision.md

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16