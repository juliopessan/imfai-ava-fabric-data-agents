# SDD: downstream-executor (Execute Deployment)

**Role:** Deploy DDL and ETL to target platform. Execution only, no design changes.

---

## Input Contract

```
Required:
  ├─ ddl-scripts: Path — projects/[project]/outputs/code/ddl-*.sql
  ├─ etl-scripts: Path — projects/[project]/outputs/code/etl-*.py
  ├─ target_credentials: Dict — connection strings (secure)
  ├─ environment: String — dev|stage|prod
  └─ deployment_order: List — ['bronze', 'silver', 'gold']

Reject If:
  ├─ Any DDL fails syntax validation
  ├─ Target credentials invalid
  └─ Deployment order incomplete
```

---

## Task Definition

1. **Validate** all DDL/ETL before deployment
2. **Deploy** Bronze layer (raw data)
3. **Deploy** Silver layer (cleansed)
4. **Deploy** Gold layer (aggregated)
5. **Load sample data** (for validation)
6. **Execute reconciliation**
7. **Generate** deployment report

---

## Success Criteria

- ✅ All DDL deployed successfully
- ✅ Sample data loaded
- ✅ Reconciliation score >= 0.98
- ✅ No data loss

---

## Output Contract

```
Produces:
  ├─ deployment-log.txt: Full execution log
  ├─ deployment-status.json: {stage, status, row_count, errors}
  └─ reconciliation-report.md: Data validation results

Location: projects/[project]/outputs/deployment/
Passes To: quality-gate
```

---

## Constraints

🔴 EXECUTE ONLY (no code changes)  
🔴 ROLLBACK if any step fails  
🔴 All deployments logged  
🔴 No partial deployments (all-or-nothing)

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16