# ⚖️ Task: Reconcile Wave

> **Agent:** Balance (Reconciliation Agent)
> **Phase:** DOWNSTREAM | **Gate:** 3
> **Command:** `*reconcile-wave`

---

## Objective

Execute a full reconciliation suite for a migration wave. Run all checks (row count, checksum, schema diff, data profiling), aggregate results, generate `reconciliation-report.json`, and flag critical discrepancies that block wave sign-off.

---

## Prerequisites

- [ ] All tables in the wave have been migrated to target
- [ ] Source and target connections verified
- [ ] Row count, checksum, schema-diff, and profile-data tasks are available
- [ ] Wave definition (table list, scope) confirmed

---

## Steps

### Step 1 — Initialize Reconciliation

```text
1. Load wave definition (table list, expected counts)
2. Verify source connectivity
3. Verify target connectivity
4. Initialize result containers for all check types
5. Log reconciliation start time
```

### Step 2 — Execute Row Count Comparison

```text
1. Run compare-row-counts task for all tables in wave
2. Collect results: passed, failed, delta per table
3. Store in reconciliation_results["row_count"]
4. Log: "Phase 1/4: Row Counts .............. ✅ 449/450 PASS"
```

### Step 3 — Execute Checksum Validation

```text
1. Run validate-checksums task for all tables in wave
2. Use appropriate strategy (full table vs per-partition)
3. Collect results: passed, failed, checksum mismatches
4. Store in reconciliation_results["checksum"]
5. Log: "Phase 2/4: Checksums ............... ✅ 450/450 PASS"
```

### Step 4 — Execute Schema Diff

```text
1. Run diff-schemas task for all tables in wave
2. Collect results: identical, diffs, severity classification
3. Store in reconciliation_results["schema_diff"]
4. Log: "Phase 3/4: Schema Diffs ............ ✅ 450/450 PASS"
```

### Step 5 — Execute Data Profiling

```text
1. Run profile-data task for all tables in wave
2. Compare statistical profiles between source and target
3. Collect results: no drift, warnings, critical drifts
4. Store in reconciliation_results["data_profile"]
5. Log: "Phase 4/4: Data Profiling .......... ⚠️ 448/450 PASS (2 warnings)"
```

### Step 6 — Aggregate Results

```text
1. Calculate overall parity percentage
2. Count total CRITICAL, WARNING, INFO issues
3. Determine wave sign-off eligibility:
   - IF critical_count == 0 AND parity >= 99.9%: ELIGIBLE
   - ELSE: BLOCKED
4. Generate summary statistics
```

### Step 7 — Generate Reconciliation Report

```json
{
  "report_type": "wave_reconciliation",
  "wave": 1,
  "timestamp": "2026-02-13T12:00:00Z",
  "duration_minutes": 45,
  "summary": {
    "total_tables": 450,
    "overall_parity_pct": 99.97,
    "sign_off_eligible": false,
    "critical_issues": 1,
    "warnings": 2,
    "info": 3
  },
  "checks": {
    "row_count": {
      "tables_passed": 449,
      "tables_failed": 1,
      "status": "FAIL"
    },
    "checksum": {
      "tables_passed": 450,
      "tables_failed": 0,
      "status": "PASS"
    },
    "schema_diff": {
      "tables_identical": 450,
      "tables_with_diffs": 0,
      "status": "PASS"
    },
    "data_profile": {
      "tables_no_drift": 448,
      "tables_with_drift": 2,
      "status": "WARNING"
    }
  },
  "critical_issues": [
    {
      "table": "MARD",
      "check": "row_count",
      "detail": "Source: 456789, Target: 456786, Delta: -3",
      "action_required": "Investigate missing 3 rows in MARD"
    }
  ],
  "warnings": [
    {
      "table": "EKPO",
      "check": "data_profile",
      "detail": "avg(NETWR) drift 1.66%",
      "action_required": "Review rounding logic for NETWR"
    }
  ]
}
```

### Step 8 — Flag Critical Discrepancies

```text
For each critical issue:
  1. Create discrepancy detail record
  2. Assign to responsible team member
  3. Block wave sign-off until resolved
  4. Notify downstream agents (Scribe)
```

---

## Output Files

| File                                | Location                                            |
| ----------------------------------- | --------------------------------------------------- |
| `wave-{N}-reconciliation-report.json` | `./reconciliation-outputs/reconciliation-reports/` |
| `wave-{N}-discrepancies.json`       | `./reconciliation-outputs/discrepancy-details/`     |
| `wave-{N}-profiles.json`            | `./reconciliation-outputs/data-profiles/`           |
| `wave-{N}-schema-diffs.json`        | `./reconciliation-outputs/schema-diffs/`            |

---

## Success Criteria

- [ ] All four check types executed successfully
- [ ] Aggregate parity percentage calculated
- [ ] Wave sign-off eligibility determined
- [ ] `reconciliation-report.json` generated and saved
- [ ] Critical discrepancies documented in `discrepancy-details.json`
- [ ] Results communicated to downstream agents
- [ ] Execution time logged for performance baseline
