# Gate 3 Checklist

**Gate:** DOWNSTREAM → PRODUCTION  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Pre-Validation Requirements

### Previous Gates Status
- [ ] Gate 1 PASSED
- [ ] Gate 2 PASSED
- [ ] Project status is DOWNSTREAM

### Environment Check
- [ ] Workspace accessible
- [ ] All agent outputs available
- [ ] Template files available
- [ ] Output folder exists

---

## Artifact Verification

### 1. DDL Scripts
- [ ] Folder exists: `**/ddl/`
- [ ] At least 1 SQL file present
- [ ] Scripts cover all layers:
  - [ ] Landing/Raw tables
  - [ ] Bronze tables
  - [ ] Silver tables
  - [ ] Gold tables
  - [ ] Reference tables (if applicable)
- [ ] Naming conventions followed
- [ ] Constraints defined
- [ ] Indexes defined
- [ ] Scripts are idempotent

### 2. ETL Code
- [ ] Folder exists: `**/etl/`
- [ ] At least 1 ETL file present
- [ ] All STTM mappings implemented
- [ ] Error handling present
- [ ] Logging implemented
- [ ] Incremental load logic (if required)
- [ ] Code follows standards
- [ ] Run-all script present

### 3. Unit Tests
- [ ] Test files exist: `**/tests/*.sql` or `**/tests/*.py`
- [ ] At least 3 test files
- [ ] Coverage > 80% of ETL logic
- [ ] Edge cases covered
- [ ] Negative tests included
- [ ] All tests documented

### 4. Integration Tests
- [ ] Integration test files exist
- [ ] End-to-end pipeline tested
- [ ] Data flow validated
- [ ] Error scenarios tested

### 5. Documentation
- [ ] Folder exists: `**/docs/` or `**/documentation/`
- [ ] Pipeline overview documented
- [ ] Data lineage documented
- [ ] Troubleshooting guide exists
- [ ] Runbook created
- [ ] SLA documented

### 6. DQ Validation
- [ ] DQ validation results exist
- [ ] All DQ rules executed
- [ ] Pass rate > 95%
- [ ] No critical rule failures
- [ ] DQ report generated

### 7. Performance Tests (Recommended)
- [ ] Performance test results exist
- [ ] Load time within SLA
- [ ] Resource usage acceptable
- [ ] Scalability verified

---

## Quality Validation

### Code Quality
- [ ] No syntax errors in DDL
- [ ] No syntax errors in ETL
- [ ] Consistent formatting
- [ ] Comments present
- [ ] No hardcoded values

### Test Quality
- [ ] Tests are automated
- [ ] Tests are repeatable
- [ ] Test data is managed
- [ ] Results are logged

### Documentation Quality
- [ ] Clear and complete
- [ ] Up to date
- [ ] Follows templates
- [ ] Accessible to team

---

## Pre-Deployment Checklist

### Approvals
- [ ] Technical review completed
- [ ] Business approval obtained
- [ ] DQ validation approved
- [ ] Security review (if required)

### Deployment Readiness
- [ ] Rollback plan documented
- [ ] Deployment runbook ready
- [ ] Target environment prepared
- [ ] Access permissions verified
- [ ] Change request submitted

### Monitoring Setup
- [ ] Alerting configured
- [ ] Dashboards ready
- [ ] Log aggregation setup
- [ ] SLA monitoring enabled

---

## Decision Criteria

### PASS Conditions (ALL required)
- [ ] All 6 required categories present
- [ ] Tests passing (> 95%)
- [ ] DQ validation passed (> 95%)
- [ ] No critical issues
- [ ] Documentation complete

### PARTIAL Conditions (ANY applies)
- [ ] 5 of 6 categories present
- [ ] Tests passing (> 80%)
- [ ] DQ validation (> 90%)
- [ ] Minor issues documented
- [ ] Clear path to completion

### FAIL Conditions (ANY applies)
- [ ] Fewer than 5 categories present
- [ ] Tests failing (< 80%)
- [ ] DQ critical failures
- [ ] Major documentation gaps
- [ ] Blocker issues present

---

## Post-Validation Actions

### On PASS
- [ ] Generate gate-3-report.md
- [ ] Update project status to PRODUCTION-READY
- [ ] Log in audit trail
- [ ] Generate deployment package summary
- [ ] Notify stakeholders
- [ ] Initiate change management process

### On PARTIAL
- [ ] Generate gate-3-report.md with conditions
- [ ] Document conditions for production
- [ ] Recommend remediation agent
- [ ] Schedule re-validation
- [ ] Communicate timeline

### On FAIL
- [ ] Generate gate-3-report.md with gaps
- [ ] Keep status as DOWNSTREAM
- [ ] Log failure in audit trail
- [ ] Recommend appropriate agent:
  - DataFlow for DDL/ETL issues
  - InsightForge for reporting issues
  - DataSteward for DQ issues
- [ ] Create remediation plan
