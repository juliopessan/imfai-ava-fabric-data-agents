# SDD: quality-gate (Validate Artifacts)

**Role:** Validate each phase output against quality criteria. Gate keeper.

---

## Input Contract

```
Required:
  ├─ artifact_type: String — discovery|architecture|model|code|deployment
  ├─ artifact_path: Path — to validate
  ├─ quality_rules: Dict — from quality_thresholds.py
  └─ gate_number: Int — 0|1|2|3 (which gate)

Reject If:
  ├─ Artifact doesn't exist
  ├─ Artifact invalid format
  └─ Quality rules undefined for type
```

---

## Task Definition

1. **Load** artifact
2. **Validate** structure (schema, completeness, format)
3. **Check** quality criteria:
   - Completeness (no missing fields)
   - Accuracy (no obvious errors)
   - Traceability (lineage is complete)
   - Performance (no N+1 patterns, etc.)
4. **Calculate** GateScore = 0.35×Completeness + 0.25×Quality + 0.20×RiskResidual + 0.20×Reconciliation
5. **Approve/Reject**

---

## Success Criteria

- ✅ GateScore >= 0.85
- ✅ No critical issues
- ✅ All dependencies satisfied
- ✅ Artifact signed off

---

## Output Contract

```
Produces:
  ├─ gate-score-report.json: {phase, score, criteria, issues}
  └─ gate-decision.md: APPROVED|BLOCKED|APPROVED_WITH_ITEMS

Passes To: migration-coordinator (for next phase)
```

---

## Constraints

🔴 NEVER approve score < 0.85  
🔴 All issues must be documented  
🔴 No subjective scoring (use formula)  
🔴 If blocked, provide remediation path

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16