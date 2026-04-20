# Downstream Executor Agent

Avanade Core agent for DOWNSTREAM execution in data migration projects.

## Overview

The Downstream Executor is responsible for converting approved design artifacts into executable migration assets: DDL, ETL, tests, and operational runbooks.

This agent fills the delivery gap between Gate 2 (design approved) and Gate 3 (production readiness).

## Scope

- Build and organize DDL and ETL assets
- Prepare and execute migration waves
- Run quality checks and reconciliation handoffs
- Produce deployment and rollback runbooks

## Commands

- `*help`: Show available commands
- `*status`: Show progress by artifact category
- `*create-ddl-etl`: Build initial DDL and ETL package from design artifacts
- `*run-wave`: Execute migration wave checklist and produce wave report
- `*prepare-runbook`: Generate execution and rollback runbook
- `*exit`: End session

## Required Inputs

- `architecture.md`
- `data-model.md`
- `dq-rules.md`
- `sttm.md` (recommended)

## Expected Outputs

- `ddl/`
- `etl/`
- `tests/`
- `documentation/`
- `wave-report.md`

## Folder Structure

```text
downstream-executor-agent/
  README.md
  .avanade-core/
    core-config.yaml
    agents/
      downstream-executor.md
    tasks/
      create-ddl-etl.md
      run-wave.md
      prepare-runbook.md
    checklists/
      downstream-executor-checklist.md
    templates/
      execution-runbook-tmpl.md
```
