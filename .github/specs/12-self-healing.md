# SDD: self-healing (Diagnose & Fix)

**Role:** Detect divergences between legacy and target. Propose corrections.

---

## Input Contract

```
Required:
  ├─ reconciliation-report.json: File — discrepancies
  ├─ deployment-log.txt: File — execution history
  ├─ legacy_connection: Dict — for re-validation
  └─ target_connection: Dict — for re-validation
```

---

## Task Definition

1. **Analyze** discrepancies (root causes)
2. **Categorize** issues:
   - Data quality (nulls, type mismatch)
   - Logic (join/aggregation error)
   - Performance (missing index)
3. **Propose** remediation per category
4. **Validate** fix doesn't introduce new issues
5. **Document** applied fixes

---

## Output

```
Produces:
  ├─ discrepancy-analysis.md: Root causes identified
  ├─ remediation-plan.md: Steps to fix
  └─ revalidation-results.json: Post-fix validation

Passes To: downstream-executor (for re-deployment if needed)
```

---

## Constraints

🔴 Only diagnose (don't modify without approval)  
🔴 Propose remediation (don't execute)  
🔴 No guessing root cause  

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16