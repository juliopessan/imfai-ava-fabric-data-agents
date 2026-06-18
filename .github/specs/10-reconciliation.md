# SDD: reconciliation (Validate Data)

**Role:** Compare legacy data vs migrated data. 100% accuracy validation.

---

## Input Contract

```
Required:
  ├─ legacy_connection: Dict — {server, db, user, password}
  ├─ target_connection: Dict — {server, db, user, password}
  ├─ reconciliation_rules: File — projects/[project]/outputs/reconciliation_rules.json
  ├─ table_list: List — tables to validate
  └─ sample_size: Int — rows to check (or 'all')

Reject If:
  ├─ Connections invalid
  ├─ Reconciliation rules missing
  └─ Table list empty
```

---

## Task Definition

1. **Query** legacy system (row count, checksum, first/last rows)
2. **Query** target system (same queries)
3. **Compare** results:
   - Row count match
   - Checksum match
   - Sample row match
4. **Flag** any discrepancies with root cause
5. **Generate** reconciliation report

---

## Success Criteria

- ✅ Row counts match (100%)
- ✅ Checksums match (for sampled data)
- ✅ No data loss
- ✅ Reconciliation score >= 0.98

---

## Output

```
Produces:
  ├─ reconciliation-report.md: Detailed comparison
  ├─ discrepancies.json: Any mismatches found
  ├─ reconciliation-score.json: {table, score, status}
  └─ sign-off.txt: APPROVED|FAILED

Location: projects/[project]/outputs/reconciliation/
Passes To: migration-coordinator (for go-live decision)
```

---

## Constraints

🔴 100% accuracy (no approximations)  
🔴 All discrepancies must be explained  
🔴 Score < 0.98 requires investigation  
🔴 No go-live without approval

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16