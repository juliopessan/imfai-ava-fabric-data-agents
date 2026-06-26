# Financeiro — Shared Context

## Projeto
Migração de serviços legados de processamento de dados do Financeiro para plataforma moderna (Databricks).

## Escopo Inicial (Wave 1)
Dois repositórios de microserviços:
1. **aaar-srv-calc-rentabilidade-script** — Serviço de cálculo de rentabilidade de produtos financeiros
2. **aadg-srv-d4960-algoritmo-procedencia** — Algoritmo de procedência (lineage) de dados

## Tecnologias Esperadas
- Java / Scala / Python
- SQL (procedures, queries)
- Shell scripts (orquestração)
- Configurações Maven/Gradle/SBT
- Possíveis integrações com Kafka, bancos Oracle/DB2, APIs REST

## Target Platform
- Microsoft Azure Databricks
- Delta Lake (Lakehouse)
- Unity Catalog

## Convenções
- Output path: `projects/Financeiro/outputs/upstream/`
- Legacy path: `projects/Financeiro/legacy/`
- Scripts: `projects/Financeiro/scripts/`
