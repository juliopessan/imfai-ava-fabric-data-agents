# Execution Runbook - Wave WAVE-001

## 1. Scope

- Wave: WAVE-001
- Domains: Taxi trips baseline pipeline
- Layers: Bronze, Silver, Gold

## 2. Preconditions

- Gate 2 approved
- Input artifacts available
- Rollback path defined
- Stakeholder window approved for pilot

## 3. Step-by-Step Plan

1. Validate environment and object permissions.
2. Execute DDL package in sequence.
3. Execute ETL package in sequence.
4. Run quality checks.
5. Trigger reconciliation checks.
6. Publish wave report and evidence bundle.

## 4. Validation Checkpoints

- Artifact completeness
- Quality smoke checks
- Reconciliation baseline checks
- Test summary publication

## 5. Rollback

- Stop write operations.
- Revert newly created objects for pilot scope.
- Re-run baseline validation.

## 6. Escalation Contacts

- Technical owner: Downstream Executor
- Validation owner: Quality Gate
- Reconciliation owner: Reconciliation Agent

## 7. Post-Run

- Publish wave-report.md
- Register lessons learned
- Route pending actions
