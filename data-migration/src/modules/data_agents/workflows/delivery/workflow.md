---
name: delivery
description: Geração de DDL/SQL/PySpark para o pipeline
web_bundle: true
---

# Workflow: delivery

Workflow DOWNSTREAM para gerar estrutura de entrega (SQL/PySpark) e empacotar outputs em `implementation-artifacts/`.

## Saídas

- `{artifacts_root}/{project_code}/implementation-artifacts/sql/`
- `{artifacts_root}/{project_code}/implementation-artifacts/pyspark/`
- `{artifacts_root}/{project_code}/implementation-artifacts/README.md`

## Execução (create-only)

Siga as etapas em `steps-c/`.
