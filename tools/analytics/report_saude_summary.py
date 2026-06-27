#!/usr/bin/env python3
"""Gera relatório visual em ASCII para análise de tokens - Reference Saúde."""

def print_saude_summary():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║              REFERENCE SAÚDE — TOKEN COST ANALYSIS                         ║
║                          2026-06-26                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ ESCOPO ─────────────────────────────────────────────────────────────────┐
│                                                                           │
│  Total de arquivos:      166  files                                      │
│  Tamanho:                153.38 MB                                       │
│  Schemas SQL:            27 (BI + DW + CRM + Others)                    │
│  DAGs Airflow:           5 (with 11 tasks total)                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ TOKENS (ESTIMADO) ───────────────────────────────────────────────────────┐
│                                                                           │
│  Bruto:                  ~40.2M tokens  (160.8MB ÷ 4 chars/token)       │
│  Com overhead (30%):     ~52.3M tokens  (análise, context, iterações)   │
│  Migração completa:      ~410k tokens   (descoberta → design → exec)    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ ARQUIVOS POR TIPO ───────────────────────────────────────────────────────┐
│                                                                           │
│  .zip             113 files  ███████████████████████████░░░  78.3%     │
│  .sql              27 files  ██████░░░░░░░░░░░░░░░░░░░░░░░░░  21.7%     │
│  .sh               11 files  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%     │
│  .py                5 files  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%     │
│  .yml               4 files  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%     │
│  .txt               2 files  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%     │
│  (no-ext)           3 files  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0%     │
│                                                                           │
│  Total: 166 files | 153.38 MB                                            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ SQL SCHEMAS (27 total) ───────────────────────────────────────────────────┐
│                                                                           │
│  BI SCHEMAS (9)          │  DW SCHEMAS (11)         │  CRM (2) / Other(5)│
│  ───────────────────────  │  ────────────────────────  │  ───────────────│
│  • bi_adhoc         446  │  • dwanalytics       292   │  • CRMANALTC_MD  │
│  • bi_cco            61  │  • dwdash           6,216   │  • CRMANLTC      │
│  • bi_dw            599  │  • dwhiae         128,991 🔴│                  │
│  • bi_dw_iirs    20,796 🔴 • dwpacs             TBD   │  • app_microbio   │
│  • bi_laboratorio    19  │  • dwrentabilidade   TBD   │  • dba           │
│  • bi_ods            ?   │  • dwsaudepop        TBD   │  • db_intermed   │
│  • bi_real_time      ?   │  • dwstage           TBD   │  • ensino_bi 44k│
│  • bi_salesforce     ?   │  • DWMKT02/03        TBD   │  • jobs      41k│
│  • bi_stage          ?   │  • Monitoracao       TBD   │                  │
│                          │                            │                  │
│  Total: 9 schemas       │  Total: 11 schemas        │  Total: 7 schemas│
│                                                                           │
│  STATISTICS:                                                             │
│  • Total de linhas SQL:          367,513              │
│  • Média por schema:              13,612 linhas       │
│  • Maior schema:                  dwhiae (128,991)    │
│  • Segundo maior:                 ensino_bi (44,138)  │
│  • Schemas > 30k linhas:          3                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ AIRFLOW DAGs & ORCHESTRATION ─────────────────────────────────────────────┐
│                                                                           │
│  DAG: checkup_ingestao (PROD)                                            │
│    └─ dag_checkup_ingestao.py                                            │
│    └─ task_checkup_ingestao_1.sh                                         │
│    └─ task_checkup_ingestao_2.sh                                         │
│                                                                           │
│  DAG: dev_checkup_ingestao (DEV)                                         │
│    └─ dag_dev_checkup_ingestao.py                                        │
│    └─ task_dev_checkup_ingestao_1.sh                                     │
│    └─ task_dev_checkup_ingestao_2.sh                                     │
│                                                                           │
│  DAG: dev_fluxo_predicao (DEV - Clinical Deterioration)                  │
│    └─ dag_dev_fluxo_predicao.py                                          │
│    └─ task_dev_fluxo_predicao_0.sh                                       │
│                                                                           │
│  DAG: info_pacientes_semi                                                │
│    └─ dag_info_pacientes_semi.py                                         │
│                                                                           │
│  DAG: checkup_v2_questionario                                            │
│    └─ dag_questionario.py                                                │
│                                                                           │
│  Infrastructure:                                                         │
│    • Docker Compose (local + sequential + resetdb)                       │
│    • Constraints.txt (pip dependencies)                                  │
│    • WebServer config (UI customization)                                 │
│    • MWAA base providers (Amazon MWAA compatible)                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ STACK TECNOLÓGICO ───────────────────────────────────────────────────────┐
│                                                                           │
│  Databases:                                                              │
│    └─ SQL Server (primary)                                               │
│       └─ 27 schemas (BI, DW, CRM, app schemas)                          │
│       └─ 367,513 linhas de código                                        │
│                                                                           │
│  Orchestration:                                                          │
│    └─ Apache Airflow 2.x                                                 │
│       └─ MWAA-compatible (Amazon Managed Workflows)                      │
│       └─ 5 DAGs com 11+ tasks                                            │
│       └─ Tasks em Shell (bash)                                           │
│                                                                           │
│  Compute (Data Lake):                                                    │
│    └─ EMR (Elastic MapReduce - AWS)  🚨 CROSS-CLOUD                    │
│       └─ Spark clusters                                                  │
│       └─ Medallion architecture (Raw → Curated → Gold → Public)         │
│       └─ Directories: INGESTION, CDM, CURATEDS, GOLD, PUBLICO, etc     │
│                                                                           │
│  Supporting:                                                             │
│    └─ Docker (local development)                                         │
│    └─ Python 3.x                                                         │
│    └─ Bash scripting                                                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ ESTRUTURA EMR/SPARK (Medallion Layers) ──────────────────────────────────┐
│                                                                           │
│  emr-scripts-extracted/                                                  │
│  ├─ _full_extract/AIRFLOW/                (Airflow + DAG migrations)    │
│  │  └─ edge-airflow-cloud9-development/                                 │
│  │     ├─ docker/                    (Docker config + compose)          │
│  │     ├─ migracao-dags/             (DAG migrations)                   │
│  │     └─ script/                    (Bootstrap, entrypoint, etc)       │
│  │                                                                       │
│  ├─ INGESTION/                        (Raw data ingestion)              │
│  ├─ RDT/                              (Raw Data Table?)                 │
│  ├─ CDM/                              (Common Data Model)               │
│  ├─ CURATEDS/                         (Curated/bronze datasets)         │
│  ├─ GOLD/                             (Gold/analytics layer)            │
│  ├─ PUBLICO/                          (Public external-ready)           │
│  └─ WORKS/                            (Experimental/scratch)            │
│                                                                           │
│  Data Flow:                                                              │
│  SQL Server DW                                                           │
│       ↓                                                                   │
│  INGESTION (Airflow pulls)                                               │
│       ↓                                                                   │
│  RDT (Spark bronze)                                                      │
│       ↓                                                                   │
│  CDM → CURATEDS (intermediate layer)                                     │
│       ↓                                                                   │
│  GOLD (aggregations, facts, dimensions)                                  │
│       ↓                                                                   │
│  PUBLICO (external systems)                                              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ TOKEN BURN POR FASE ─────────────────────────────────────────────────────┐
│                                                                           │
│  Discovery (Upstream)                                     ██░░░░░░░░░  20%│
│    └─ Inventário + mapping 27 schemas        30-50k tokens              │
│                                                                           │
│  Analysis (SQL/Airflow)                      ██████░░░░░░░░░░░░░░░░░░  30%│
│    └─ SQL parse + DAG analysis              100-130k tokens             │
│                                                                           │
│  Design (Midstream)                         ██████████░░░░░░░░░░░░░░░  45%│
│    └─ Target architecture + EMR→Fabric      150-200k tokens             │
│                                                                           │
│  Execution (Downstream)                      ████░░░░░░░░░░░░░░░░░░░░   5%│
│    └─ Implementation + tests                  50-100k tokens            │
│                                            ─────────────                 │
│  TOTAL ESTIMADO:                           ~410k tokens                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ COMPLEXIDADE & RISCO ────────────────────────────────────────────────────┐
│                                                                           │
│  🔴 CRÍTICO (blockers)                                                  │
│     └─ EMR (AWS) → Fabric (Azure): Cross-cloud migration               │
│     └─ Airflow → Data Factory: DAG orchestration conversion             │
│     └─ SQL Server DW → Fabric: Schema translation + performance       │
│                                                                           │
│  🟠 ALTO (complexity)                                                   │
│     └─ 27 schemas com interdependências (BI + DW)                      │
│     └─ Grandes schemas (dwhiae=128k, ensino_bi=44k linhas)            │
│     └─ Medical data sensitivity (HIAE, PACS, microbiologia)           │
│     └─ Real-time pipelines (bi_real_time)                              │
│                                                                           │
│  🟡 MÉDIO (investigation)                                               │
│     └─ Salesforce integration                                           │
│     └─ Shell tasks → PowerShell conversion                              │
│     └─ Multiple DW consolidation strategy                               │
│                                                                           │
│  OVERALL: 🟠 COMPLEXIDADE MÉDIA-ALTA                                   │
│  REGULATION IMPACT: 🔴 HIGH (Healthcare data)                          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ COMPARATIVO: FINANCEIRO vs. SAÚDE ───────────────────────────────────────┐
│                                                                           │
│                 Financeiro          Saúde                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  Arquivos        795                 166            (Saúde = 21%)      │
│  Tamanho         43.67 MB            153.38 MB      (Saúde = 3.5x)     │
│  Tokens (bruto)  ~11.4M              ~40.2M         (Saúde = 3.5x)     │
│  Entidades BD    103 (Hive+SQL)      27 (SQL)       (Fin = 3.8x)       │
│  Scripts         98                  11 (tasks)     (Fin = 8.9x)       │
│  Orquestração    PowerCenter         Airflow        (modern)            │
│  Stack           Hive+SSIS+MS        SQL+Airflow    (cloud-native)     │
│  Complexidade    🔴 ALTA             🟠 MÉDIA-ALTA                      │
│  Token budget    ~700k               ~410k          (Saúde = 59%)      │
│  ────────────────────────────────────────────────────────────────────  │
│  Key difference: Fin = more files/scripts, Saúde = larger files/DBs   │
│  Fin = legacy, Saúde = cloud-native (but cross-cloud AWS)             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ RECOMENDAÇÕES ───────────────────────────────────────────────────────────┐
│                                                                           │
│  1. Executar Inventário Rápido (discovery-scout)          [30k tokens] │
│  2. Analisar SQL Schemas (27) + Dependências              [100k tokens]│
│  3. Mapear Airflow DAGs → Data Factory                    [80k tokens] │
│  4. Design EMR → Fabric Spark conversion                  [150k tokens]│
│  5. Gate 2 Validation + Data Quality Rules                [50k tokens] │
│                                                                           │
│  Total Phase 1-2: ~410k tokens                                           │
│                                                                           │
│  CRITICAL: Coordinate with Healthcare Compliance (LGPD/GDPR)           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Generated: 2026-06-26
Files: SAUDE-ESCOPO-TOKENS.md + analyze_saude*.py
    """)

if __name__ == '__main__':
    print_saude_summary()
