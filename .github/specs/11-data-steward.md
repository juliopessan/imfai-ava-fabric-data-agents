# SDD: data-steward (Govern Data Quality)

**Role:** Define data quality rules, ownership, and SLAs. Not execution.

---

## Input Contract

```
Required:
  ├─ data-contracts.json: File — from data-modeler
  ├─ business-rules.md: File — from business-analyst
  └─ governance_policy: Dict — quality thresholds, owners

Optional:
  └─ stakeholder_feedback: String — quality concerns
```

---

## Task Definition

1. **Define** data quality rules (null %, uniqueness, range, format)
2. **Assign** data owners per table
3. **Set** SLOs (Service Level Objectives) for freshness, accuracy, completeness
4. **Document** quality standards
5. **Create** monitoring plan

---

## Success Criteria

- ✅ Every table has an assigned owner
- ✅ Every quality rule is measurable (no vague language)
- ✅ SLOs defined for freshness, accuracy, completeness

---

## Output Contract

```
Produces:
  ├─ data-governance-policy.md: Rules + owners + SLOs
  ├─ quality-metrics-spec.json: Measurable thresholds
  └─ monitoring-dashboard-spec.json: KPI definitions

Location: projects/[project]/outputs/governance/
Passes To: code-generator (for test script generation)
```

---

## Constraints

🔴 All quality rules must be measurable
🔴 Must define owner per table
🔴 No vague SLOs ("reasonable" is forbidden)

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16
