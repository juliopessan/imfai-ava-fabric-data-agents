#!/usr/bin/env python3
"""Gera relatório visual em ASCII para análise de tokens."""

def print_token_summary():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  FINANCEIRO — TOKEN COST ANALYSIS                          ║
║                          2026-06-26                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─ ESCOPO ─────────────────────────────────────────────────────────────────┐
│                                                                           │
│  Total de arquivos:      795  files                                      │
│  Tamanho:                43.67 MB                                        │
│  Entidades:              103 (tabelas + procedures + views + Hive)       │
│  Scripts:                98 (reproc + transformations + utilities)       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ TOKENS (ESTIMADO) ───────────────────────────────────────────────────────┐
│                                                                           │
│  Bruto:                  ~11.4M tokens  (45.7MB ÷ 4 chars/token)        │
│  Com overhead (30%):     ~15M tokens    (análise, context, iterações)   │
│  Migração completa:      ~700k tokens   (descoberta → design → exec)    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ ARQUIVOS POR TIPO (TOP 10) ──────────────────────────────────────────────┐
│                                                                           │
│  .pkl          8 files  ████████████████████████░░  54.4%  23.77 MB    │
│  .dtsx        75 files  ███████████░░░░░░░░░░░░░░  19.0%   8.29 MB    │
│  .zip          3 files  █████░░░░░░░░░░░░░░░░░░░░  11.2%   4.91 MB    │
│  .dtproj       2 files  ██░░░░░░░░░░░░░░░░░░░░░░░   3.0%   1.33 MB    │
│  .py         104 files  ██░░░░░░░░░░░░░░░░░░░░░░░   2.8%   1.24 MB    │
│  .json        45 files  ██░░░░░░░░░░░░░░░░░░░░░░░   2.7%   1.19 MB    │
│  .md         108 files  ██░░░░░░░░░░░░░░░░░░░░░░░   2.4%   1.06 MB    │
│  .html        33 files  ░░░░░░░░░░░░░░░░░░░░░░░░░   1.7%    772 KB    │
│  .hql         92 files  ░░░░░░░░░░░░░░░░░░░░░░░░░   0.7%    333 KB    │
│  .sql         43 files  ░░░░░░░░░░░░░░░░░░░░░░░░░   0.7%    294 KB    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ ENTIDADES DE BANCO DE DADOS ─────────────────────────────────────────────┐
│                                                                           │
│  SQL Objects:                                                            │
│    └─ Tabelas criadas         8  (sacl_stg, rentabilidade, etc)         │
│    └─ Stored Procedures       1  (dbo.*)                                │
│    └─ Views                   2  (sacl_acc, IF)                         │
│                                                                           │
│  Legacy Big Data (Hive/HDFS):                                           │
│    └─ Arquivos HQL           92  (partições + tabelas + índices)       │
│       ├─ sql_partitions/      (criar partições)                        │
│       ├─ sql_tables/          (definição de tabelas)                   │
│       ├─ sql_temp_tables/     (temporárias)                            │
│       └─ indices_econm/       (índices econômicos)                     │
│                                                                           │
│  TOTAL:                       103 entidades                              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ SCRIPTS DE LÓGICA ───────────────────────────────────────────────────────┐
│                                                                           │
│  Python Scripts (104 total):                                             │
│    ├─ reproc_*.py             22  (reprocessamento encadeado)          │
│    │   └─ reproc_carteira, reproc_producto, reproc_portfolio, etc      │
│    └─ outros scripts           76  (consolidação, utilitários)         │
│                                                                           │
│  Shell Scripts (234 total):                                              │
│    ├─ HDFS operations          ~50                                      │
│    ├─ Hive execution           ~50                                      │
│    ├─ PowerCenter workflows    ~40                                      │
│    └─ Monitoração/utils       ~94                                      │
│                                                                           │
│  SSIS/ETL (77 total):                                                    │
│    ├─ .dtsx packages           75  (SSIS packages)                      │
│    └─ .dtproj                   2  (SSIS projects)                      │
│                                                                           │
│  TOTAL:                        211 arquivos de lógica                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ ESTRUTURA HIERÁRQUICA ───────────────────────────────────────────────────┐
│                                                                           │
│  projects/financeiro/                                                    │
│  ├─ legacy/extracted/                  (legacy migration source)        │
│  │  ├─ aaar-srv-calc-rentabilidade-script/  (MAIN - rentabilidade)    │
│  │  │  ├─ hive/               ▓▓▓ 92 arquivos SQL + partições          │
│  │  │  ├─ python/             ▓▓▓ 22+ reproc scripts                  │
│  │  │  ├─ powercenter/        ▓▓▓ workflows completos                 │
│  │  │  ├─ ssis/               ▓▓▓ 75 packages (SSIS)                  │
│  │  │  ├─ spark/              ▓   config Spark                         │
│  │  │  ├─ sqlserver/          ▓   procedures SQL Server               │
│  │  │  ├─ teradata/           ▓   tabelas Teradata                    │
│  │  │  └─ utils/              ▓   utilitários                          │
│  │  │                                                                   │
│  │  └─ aadg-srv-d4960-algoritmo-procedencia/  (algoritmo)            │
│  │     ├─ ddl/                ▓                                        │
│  │     ├─ dml/                ▓   procedencia logic                   │
│  │     ├─ python/             ▓                                        │
│  │     └─ shell/              ▓                                        │
│  │                                                                      │
│  ├─ outputs/                    151 files (resultados de processamento) │
│  ├─ state/                       41 files (estado/checkpoints)          │
│  ├─ scripts/                     40 files (utilitários gerais)          │
│  ├─ docs/                         7 files (documentação)                │
│  └─ context/                      2 files (configuração)                │
│                                                                           │
│  Total: 795 files | 43.67 MB                                            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ TOKEN BURN POR FASE ─────────────────────────────────────────────────────┐
│                                                                           │
│  Discovery (Upstream)                                     ████░░░░░░░  20%│
│    └─ Inventário + mapping                  50-200k tokens             │
│                                                                           │
│  Design (Midstream)                         ██████████░░░░░░░░░░░░░░  45%│
│    └─ Arquitetura + código + validação    250-350k tokens             │
│                                                                           │
│  Execution (Downstream)                     ███████░░░░░░░░░░░░░░░░░  35%│
│    └─ Implementação + testes + deploy      150-250k tokens             │
│                                            ─────────────                 │
│  TOTAL ESTIMADO:                           ~700k tokens                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ COMPLEXIDADE & RISCO ────────────────────────────────────────────────────┐
│                                                                           │
│  🔴 CRÍTICO (blockers)                                                  │
│     └─ Hive → Spark: 92 scripts HQL                                     │
│     └─ SSIS → Data Factory: 75 packages                                 │
│     └─ PowerCenter: custom workflows                                     │
│                                                                           │
│  🟠 ALTO (dependencies)                                                 │
│     └─ Reproc encadeado: 22 scripts interdependentes                    │
│     └─ Teradata + TDCH: conectores custom                               │
│     └─ Pickles binárias: conversão de formato                           │
│                                                                           │
│  🟡 MÉDIO (investigation needed)                                        │
│     └─ Shell scripts: 234 automações                                    │
│     └─ Procedures SQL: lógica complexa                                  │
│     └─ Índices econômicos: time-sensitive                               │
│                                                                           │
│  OVERALL: 🔴 COMPLEXIDADE ALTA                                          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌─ RECOMENDAÇÕES ───────────────────────────────────────────────────────────┐
│                                                                           │
│  1. Executar Inventário Rápido (discovery-scout)           [50k tokens] │
│  2. Analisar Dependências (Python AST parse)              [100k tokens] │
│  3. Mapear Stack Legado (Hive→Spark, SSIS→DF)            [200k tokens] │
│  4. Design Data Model (Fabric + Semantic Kernel)          [250k tokens] │
│  5. Gate 2 Validation + Reconciliation                    [100k tokens] │
│                                                                           │
│  Total Phase 1-2: ~700k tokens                                           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

Generated: 2026-06-26
File: FINANCEIRO-ESCOPO-TOKENS.md + analyze_financeiro*.py
    """)

if __name__ == '__main__':
    print_token_summary()
