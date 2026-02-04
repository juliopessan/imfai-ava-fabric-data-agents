# Validate Gate 3 Task

**Task ID:** validate-gate-3  
**Agent:** Orchestrator  
**Version:** 1.0  
**Gate:** DOWNSTREAM → DEPLOY/PRODUCTION

---

## Purpose

Validate that all DOWNSTREAM artifacts are complete, tested, and meet production-readiness criteria before allowing deployment to production.

---

## Gate 3 Criteria

### Required Artifacts

| # | Artifact | Description | Required |
|---|----------|-------------|----------|
| 1 | DDL Scripts | Database definition scripts | ✅ Yes |
| 2 | ETL Code | Extraction, Transformation, Load code | ✅ Yes |
| 3 | Unit Tests | Automated unit tests | ✅ Yes |
| 4 | Integration Tests | End-to-end tests | ✅ Yes |
| 5 | Documentation | Pipeline documentation | ✅ Yes |
| 6 | DQ Validation | Data quality validation results | ✅ Yes |
| 7 | Performance Tests | Load/performance test results | ⚠️ Recommended |

### Quality Criteria

**DDL Scripts:**
- [ ] Scripts execute without errors
- [ ] Naming conventions followed
- [ ] Indexes defined appropriately
- [ ] Constraints implemented
- [ ] Scripts are idempotent (can re-run)

**ETL Code:**
- [ ] All source-to-target mappings implemented
- [ ] Error handling implemented
- [ ] Logging implemented
- [ ] Incremental load logic (if applicable)
- [ ] Code follows standards

**Unit Tests:**
- [ ] Coverage > 80%
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Negative tests included
- [ ] Tests are maintainable

**Integration Tests:**
- [ ] End-to-end pipeline tested
- [ ] Data flow validated
- [ ] Error scenarios tested
- [ ] Recovery procedures tested

**Documentation:**
- [ ] Pipeline overview documented
- [ ] Data lineage documented
- [ ] Troubleshooting guide
- [ ] Runbook created
- [ ] SLA documented

**DQ Validation:**
- [ ] All DQ rules executed
- [ ] Pass rate > threshold
- [ ] Critical rules passing
- [ ] DQ report generated

**Performance Tests:**
- [ ] Load time within SLA
- [ ] Resource usage acceptable
- [ ] Scalability verified

---

## Execution Steps

### Step 1: Locate Artifacts

Search workspace for Gate 3 artifacts:

```
Search patterns:
- **/ddl/*.sql
- **/etl/*.sql OR **/etl/*.py
- **/tests/*.sql OR **/tests/*.py
- **/tests/unit/**
- **/tests/integration/**
- **/documentation/*.md
- **/docs/*.md
- **/quality/*.md
- **/dq-results*.md
```

### Step 2: Validate Artifact Presence

Check each artifact category exists and contains files.

### Step 3: Validate Quality

For each artifact category:
1. Check files are not empty
2. Check for error patterns
3. Verify naming conventions
4. Check completeness

### Step 4: Run Automated Checks

If possible, execute:
- SQL syntax validation
- Test execution summary
- DQ rule summary

### Step 5: Generate Gate Report

Use template `gate-report-tmpl.yaml` to generate:

**Output file:** `{output_folder}/gate-reports/gate-3-report_{date}.md`

---

## Output Format

```markdown
# 🚦 Gate 3 Validation Report

**Gate:** DOWNSTREAM → PRODUCTION  
**Date:** {date}  
**Validated by:** Orchestrator

---

## Overall Result

**Status:** {PASS | FAIL | PARTIAL}

---

## Deployment Readiness Summary

| Category | Items | Status | Notes |
|----------|-------|--------|-------|
| DDL Scripts | {count} | {✅/⚠️/❌} | {notes} |
| ETL Code | {count} | {✅/⚠️/❌} | {notes} |
| Unit Tests | {count} | {✅/⚠️/❌} | {notes} |
| Integration Tests | {count} | {✅/⚠️/❌} | {notes} |
| Documentation | {count} | {✅/⚠️/❌} | {notes} |
| DQ Validation | {count} | {✅/⚠️/❌} | {notes} |
| Performance Tests | {count} | {✅/⚠️/❌} | {notes} |

---

## Test Results Summary

### Unit Tests
- Total: {total}
- Passed: {passed}
- Failed: {failed}
- Coverage: {coverage}%

### Integration Tests
- Total: {total}
- Passed: {passed}
- Failed: {failed}

### DQ Validation
- Rules Executed: {total}
- Passed: {passed}
- Failed: {failed}
- Critical Failures: {critical}

---

## Detailed Findings

### DDL Scripts
{detailed assessment}

### ETL Code
{detailed assessment}

### Tests
{detailed assessment}

### Documentation
{detailed assessment}

### DQ Validation
{detailed assessment}

---

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] DQ validation passed
- [ ] Documentation complete
- [ ] Runbook available
- [ ] Rollback plan documented
- [ ] Stakeholder approval obtained
- [ ] Change request submitted

---

## Gaps Identified

{list of missing or incomplete items}

---

## Recommendations

{if PASS}
✅ Gate 3 PASSED. Project is ready for deployment.

**Deployment Checklist:**
1. Submit change request
2. Schedule deployment window
3. Execute deployment runbook
4. Validate post-deployment
5. Monitor initial runs

{if FAIL}
❌ Gate 3 FAILED. The following must be completed:
{list of required actions}

**Recommended Actions:**
{specific actions and responsible agents}

---

*Gate validation performed by Orchestrator Agent*
```

---

## Decision Rules

```
IF all 6 required categories present AND tests passing AND DQ >95%:
  → RESULT: PASS
  → ACTION: Approve for production deployment

IF 5+ categories present AND tests >80% AND DQ >90%:
  → RESULT: PARTIAL (with conditions)
  → ACTION: List conditions for production readiness

IF <5 categories OR tests <80% OR DQ <90% OR critical failures:
  → RESULT: FAIL
  → ACTION: List gaps and remediation steps
```

---

## Post-Validation Actions

**On PASS:**
1. Create gate-3-report.md in gate-reports folder
2. Update project status to "PRODUCTION-READY"
3. Log passage in audit trail
4. Generate deployment package summary
5. Notify stakeholders

**On FAIL:**
1. Create gate-3-report.md with gaps
2. Keep project status as "DOWNSTREAM"
3. Log attempt in audit trail
4. Suggest routing to:
   - DataFlow for ETL/DDL issues
   - InsightForge for reporting issues
   - DataSteward for DQ issues
