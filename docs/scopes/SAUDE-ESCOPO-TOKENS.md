# 📊 MAPEAMENTO DE ESCOPO — PROJETO REFERENCE SAÚDE

**Data:** 2026-06-26  
**Escopo:** Análise completa para cálculo de tokens e planejamento de migração  
**Status:** ✅ Finalizado

---

## 1️⃣ RESUMO EXECUTIVO

| Métrica | Valor |
|---------|-------|
| **Total de arquivos** | 166 |
| **Tamanho total** | 153.38 MB |
| **Estimativa de tokens** | ~40.2M (bruto) / ~52.3M (com overhead) |
| **Schemas SQL** | 27 (9 BI + 11 DW + 2 CRM + 5 outros) |
| **DAGs Airflow** | 5 (com ~11 tasks) |
| **Complexidade** | 🟠 **MÉDIA-ALTA** |
| **Stack** | SQL Server DW + Airflow + EMR (Spark) |

---

## 2️⃣ DISTRIBUIÇÃO DE ARQUIVOS

### Por Tipo de Arquivo

| Extensão | Quantidade | Tamanho | % do Total | Categoria |
|----------|-----------|--------|-----------|-----------|
| `.zip` | 113 | 120.02 MB | 78.3% | 📦 Archives/Backups |
| `.sql` | 27 | 33.31 MB | 21.7% | 🗄️ SQL Schemas |
| `.sh` | 11 | 13.84 KB | 0.0% | 🔧 Shell/Airflow Tasks |
| `.py` | 5 | 7.90 KB | 0.0% | 🐍 DAG Definitions |
| `.yml` | 4 | 5.96 KB | 0.0% | ⚙️ Config |
| `.txt` | 2 | 19.11 KB | 0.0% | 📄 Docs |
| **(no-ext)** | 3 | 2.56 KB | 0.0% | 📁 Scripts |

### Distribuição por Diretório

| Diretório | Quantidade | Tamanho |
|-----------|-----------|--------|
| `emr-scripts-extracted/` | 139 | 145+ MB |
| `dw-scripts-extracted/` | 27 | 33.31 MB |

---

## 3️⃣ OBJETOS DE BANCO DE DADOS (SQL)

### BI Schemas (9 total)
- `bi_adhoc` — Ad hoc queries (446 linhas)
- `bi_cco` — Centro de Custos Operacional (61 linhas)
- `bi_dw` — Data Warehouse BI base (599 linhas)
- `bi_dw_iirs` — Sistema IIRS (20,796 linhas) 🔴 Grande
- `bi_laboratorio` — Laboratório (19 linhas)
- `bi_ods` — ODS (Operational Data Store)
- `bi_real_time` — Real Time analytics
- `bi_salesforce` — Salesforce integration
- `bi_stage` — Staging area

### DW Schemas (11 total)
- `dwanalytics` — Analytics Data Warehouse (292 linhas)
- `dwdash` — Dashboard data (6,216 linhas)
- `dwhiae` — HIAE DW (128,991 linhas) 🔴 MAIOR
- `DWMKT02` — Marketing DW 02
- `DWMKT03` — Marketing DW 03
- `dwpacs` — PACS (medical imaging) DW
- `dwrentabilidade` — Rentabilidade
- `dwsaudepopulacional` — Saúde Populacional
- `dwstage` — DW Staging
- `Monitorizacao BI` — Monitoração

### CRM Schemas (2 total)
- `CRMANALTC_MD` — CRM Analytics (1,697 linhas)
- `CRMANLTC` — CRM (13,086 linhas)

### Outros Schemas (5 total)
- `app_microbiologia` — Aplicação Microbiologia (3,751 linhas)
- `dba` — DBA utilities (1,749 linhas)
- `db_intermediario` — Database intermediária (33,322 linhas) 🟠 Grande
- `ensino_bi` — Ensino (educação) (44,138 linhas) 🟠 Grande
- `jobs` — Jobs/Procedures (41,712 linhas) 🟠 Grande

### Estatísticas SQL
```
Total de linhas SQL:     367,513
Média por schema:        13,612 linhas
Schemas grandes (>30k):  3 (ensino_bi, jobs, db_intermediario)
Schemas super-grandes:   2 (dwhiae=128k, bi_dw_iirs=20k)
```

---

## 4️⃣ ORQUESTRAÇÃO E PIPELINES (Airflow)

### DAGs Mapeadas (5 total)

#### 1. **checkup_ingestao** (Produção)
```
dag_checkup_ingestao.py
├─ task_checkup_ingestao_1.sh
└─ task_checkup_ingestao_2.sh
```
- Purpose: Ingestão de dados de verificação/checkup

#### 2. **dev_checkup_ingestao** (Desenvolvimento)
```
dag_dev_checkup_ingestao.py
├─ task_dev_checkup_ingestao_1.sh
└─ task_dev_checkup_ingestao_2.sh
```
- Purpose: Dev version with incremental test

#### 3. **dev_fluxo_predicao** (Desenvolvimento)
```
dag_dev_fluxo_predicao.py
└─ task_dev_fluxo_predicao_0.sh
```
- Purpose: Prediction flow (Clinical Deterioration?)

#### 4. **info_pacientes_semi** 
```
dag_info_pacientes_semi.py
```
- Purpose: Patient information semi-aggregation

#### 5. **checkup_v2_questionario**
```
dag_questionario.py
```
- Purpose: Questionnaire processing

#### 6. **checkup_v2_checkup_povoar_tabela_history**
- Purpose: Populate history tables

### Airflow Infrastructure
- **Docker Compose** configs (local + sequential + resetdb)
- **Bootstrap scripts** para ambiente local
- **Constraints.txt** para pip dependencies
- **WebServer config** para UI customization
- **MWAA base providers** (Amazon MWAA compatible)

---

## 5️⃣ ESTRUTURA EMR/SPARK

### Diretórios EMR Detectados
```
emr-scripts-extracted/
├─ _full_extract/
│  └─ AIRFLOW/                  (Airflow + DAGs)
│     └─ edge-airflow-cloud9-development/
│        ├─ docker/             (Docker config)
│        ├─ migracao-dags/      (DAG migrations)
│        ├─ script/             (startup scripts)
│        └─ dags/               (DAG definitions)
├─ CDM/                         (Common Data Model)
├─ CURATEDS/                    (Curated datasets)
├─ GOLD/                        (Gold layer)
├─ INGESTION/                   (Ingestion pipelines)
├─ PUBLICO/                     (Public data)
├─ RDT/                         (Raw Data Table?)
└─ WORKS/                       (Workspaces/experimental)
```

### Arquitetura de Camadas (Medallion)
```
INGESTION (raw) → RDT (raw data table) → GOLD (facts/dimensions)
                                      ↓
                        CURATEDS (aggregations)
                                      ↓
                        PUBLICO (external-ready)
```

---

## 6️⃣ STACK TECNOLÓGICO

### Bancos de Dados
- **SQL Server** (principal)
  - Multiple schemas para OLAP/DW
  - Views complexas (BI)
  - Stored Procedures (jobs)

### Orquestração
- **Airflow** (Apache Airflow 2.x)
  - MWAA-compatible (Amazon Managed Workflows)
  - DAGs em Python
  - Tasks em Shell (bash)

### Compute
- **EMR** (Elastic MapReduce — AWS!)
  - Spark clusters
  - Hadoop HDFS
  - Medallion architecture

### Documentação & Config
- Docker Compose (local dev)
- Constraints (Python dependencies)
- WebServer config (UI customization)

---

## 7️⃣ ESTIMATIVA DE TOKENS

### Cálculo Base
```
Total em bytes:        160,833,387
Estimativa bruta:      ~40,208,346 tokens
  (1 token ≈ 4 caracteres)

Com overhead (30%):    ~52,270,850 tokens
  (para análise, contexto, iterações)
```

### Breakdown por Fase de Migração

| Fase | Estimativa | Notas |
|------|-----------|-------|
| **Inventário** | 30k | Scan + mapping de 27 schemas |
| **SQL Analysis** | 100k | Parse de 367k linhas SQL |
| **Airflow DAGs** | 80k | 5 DAGs + 11 tasks + config |
| **Design Target** | 150k | Arquitetura Fabric + ADF |
| **Validação** | 50k | Gate 2, reconciliação |
| **────────────** | **────────** | **────────** |
| **TOTAL** | **~410k** | **Estimado para execução completa** |

### Token Burn por Atividade

```
🔍 Descoberta (Upstream):     80-100k tokens
   └─ Scan, inventário, schema mapping

🏗️ Design (Midstream):        150-200k tokens
   └─ Target architecture, Fabric design

🚀 Execução (Downstream):     100-150k tokens
   └─ Implementação, testes, deploy
```

---

## 8️⃣ COMPLEXIDADE E RISCOS

### Fatores de Complexidade

| Fator | Nível | Descrição |
|-------|-------|-----------|
| **Schemas SQL (27)** | 🟠 Médio | Múltiplos domínios (BI, DW, CRM) |
| **Tamanho (367k linhas)** | 🟠 Médio | ~13.6k linhas/schema |
| **Airflow (5 DAGs)** | 🟠 Médio | Pipelines com múltiplas tasks |
| **EMR/Spark** | 🔴 Crítico | AWS → Fabric (cross-cloud) |
| **Multi-layer arch** | 🟠 Médio | Medallion (Raw→Curated→Gold→Public) |

### Riscos Principais

🔴 **CRÍTICO**
- **EMR (AWS) → Azure Fabric:** Cross-cloud migration
- **SQL Server DW → Fabric DW:** Schema translation + performance tuning
- **Airflow → Data Factory/Synapse:** DAG orchestration conversion

🟠 **ALTO**
- Schemas grandes (dwhiae=128k, ensino_bi=44k linhas)
- Complex relationships (9 BI + 11 DW schemas interconnected)
- Medical data sensitivity (HIAE, microbiologia, PACS)
- Real-time pipelines (bi_real_time)

🟡 **MÉDIO**
- Shell tasks em Airflow (bash → PowerShell)
- CRM integration (Salesforce)
- Multiple DW schemas (may need consolidation)

---

## 9️⃣ RECOMENDAÇÕES PARA ANÁLISE

### Sequência de Análise (Token-otimizada)

```
1️⃣ Inventário Rápido (30k tokens)
   └─ Lista schemas, DAGs, stack detectado

2️⃣ SQL Schema Cataloging (100k tokens)
   └─ Parse de 27 schemas, linhas de código

3️⃣ Airflow DAG Analysis (80k tokens)
   └─ Tasks, dependencies, execution patterns

4️⃣ EMR/Spark Assessment (60k tokens)
   └─ Medallion layer mapping, data models

5️⃣ Target Design (150k tokens)
   └─ Fabric + Data Factory architecture

6️⃣ Validation & Gate 2 (50k tokens)
   └─ Reconciliation, quality rules
```

### Ferramentas Recomendadas

| Tool | Para | Token Cost |
|------|------|-----------|
| **SQL Server Management Studio** | Schema analysis | Baixo (local) |
| **Airflow UI inspection** | DAG visualization | Baixo (local) |
| **Python AST** | Task parsing | Baixo (local) |
| **Fabric Synapse** | Target validation | Médio |
| **Azure Data Factory** | Pipeline mapping | Médio |
| **Copilot** (subagent) | Design + docs | 150-200k |

---

## 🔟 COMPARATIVO: FINANCEIRO vs. SAÚDE

| Aspecto | Financeiro | Saúde |
|--------|-----------|-------|
| **Arquivos** | 795 | 166 |
| **Tamanho** | 43.67 MB | 153.38 MB |
| **Tokens (bruto)** | ~11.4M | ~40.2M |
| **Entidades BD** | 103 (Hive+SQL) | 27 (SQL Server) |
| **Scripts** | 98 (Python+Shell) | 11 (Shell tasks) |
| **Orquestração** | Legacy (PowerCenter) | Airflow (cloud-native) |
| **Stack** | Hive+SSIS+PowerCenter | SQL Server+Airflow+EMR |
| **Complexidade** | 🔴 ALTA | 🟠 MÉDIA-ALTA |
| **Token estimate** | ~700k | ~410k |
| **Criticality** | Financeiro (core) | Medical (regulated) |

---

## 1️⃣1️⃣ NEXT STEPS

- [ ] **Phase 1:** Executar inventário detalhado via `discovery-scout`
- [ ] **Phase 2:** Analisar dependências entre schemas (dependency graph)
- [ ] **Phase 3:** Mapear EMR → Microsoft Fabric (cross-cloud)
- [ ] **Phase 4:** Design Airflow → Data Factory conversion
- [ ] **Phase 5:** Gate 2 validation + data quality checks

---

**Gerado:** 2026-06-26  
**Arquivo:** `/memories/repo/saude-escopo-tokens.md`  
**Próximo:** Consolidar Financeiro + Saúde → Roadmap unificado
