# 📜 Architecture Decision Records (ADRs)

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 2.0  
> **Data:** 2026-02-05  
> **Autor:** 🏗️ Winston (DataArchitect)  
> **Referências:** [architecture.md](architecture.md) | [data-model.md](data-model.md)

---

## Sumário de ADRs

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| ADR-001 | Padrão Arquitectural: Lakehouse | ✅ Accepted | 2026-02-05 |
| ADR-002 | Plataforma: Azure Databricks | ✅ Accepted | 2026-02-05 |
| ADR-003 | Formato de Storage: Delta Lake | ✅ Accepted | 2026-02-05 |
| ADR-004 | Modelo Dimensional: Star Schema (Kimball) | ✅ Accepted | 2026-02-05 |
| ADR-005 | Estratégia de Camadas: Medallion (Bronze/Silver/Gold) | ✅ Accepted | 2026-02-05 |
| ADR-006 | Estratégia de SCD: Type 1 para Dimensões | ✅ Accepted | 2026-02-05 |
| ADR-007 | Linguagem ETL: Python/Spark + SQL | ✅ Accepted | 2026-02-05 |
| ADR-008 | Estratégia de Particionamento | ✅ Accepted | 2026-02-05 |
| ADR-009 | Estratégia de Data Quality | ✅ Accepted | 2026-02-05 |
| ADR-010 | Naming Conventions | ✅ Accepted | 2026-02-05 |

---

## ADR-001: Padrão Arquitectural - Lakehouse

### Status
✅ **Accepted** (2026-02-05)

### Context
O projeto NYC Green Taxi Analytics precisa de uma arquitetura que suporte:
- Ingestão de dados de múltiplos formatos (CSV, JSON, TSV)
- Processamento batch mensal
- Análise ad-hoc e dashboards Power BI
- Qualidade de dados e governança
- Custo otimizado para volume moderado (~1.5M rows/quarter)

### Decision
Adotar o padrão **Data Lakehouse** combinando as melhores características de Data Lake (flexibilidade, custo) com Data Warehouse (ACID, schema enforcement).

### Alternatives Considered

| Alternativa | Prós | Contras |
|-------------|------|---------|
| **Traditional DW** | ACID, performance, familiar | Custo alto, inflexível |
| **Data Lake** | Flexível, barato | Sem ACID, difícil governança |
| **Lakehouse** ✅ | ACID + flexibilidade + custo | Complexidade moderada |
| **Data Mesh** | Escalabilidade organizacional | Overhead para projeto pequeno |

### Consequences

**Positivas:**
- Unifica analytics e data science em uma única plataforma
- Delta Lake fornece ACID transactions
- Schema evolution sem downtime
- Custo otimizado (storage barato + compute on-demand)

**Negativas:**
- Requer conhecimento de Delta Lake/Parquet
- Complexidade moderada de setup inicial

**Riscos:**
- Lock-in parcial com formato Delta (mitigado: Delta é open source)

### Compliance
- ✅ Alinhado com Azure Well-Architected Framework
- ✅ Suporta requisitos de governance

---

## ADR-002: Plataforma - Azure Databricks

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos escolher a plataforma de compute/processing para o Lakehouse. O projeto tem:
- Volume moderado (~1.5M rows/quarter, com crescimento projetado)
- Requisito de governança centralizada
- Requisito de integração com Power BI
- Necessidade de Data Quality automatizado (DLT Expectations)
- Visão de longo prazo (ML/AI readiness)

### Decision
Adotar **Azure Databricks (Premium)** com Unity Catalog como plataforma principal, aproveitando Delta Live Tables para orquestração de pipelines e SQL Warehouse Serverless para consumo analítico.

### Alternatives Considered

| Alternativa | Custo/Mês | Prós | Contras | Fit |
|-------------|-----------|------|---------|-----|
| **Synapse Serverless** | ~$52 | Pay-per-query, SQL nativo | Sem governance centralizada, DQ limitado | ⚠️ MVP only |
| **Synapse Dedicated** | ~$500+ | Alta performance | Custo alto, sempre on | ❌ Over-budget |
| **Databricks** ✅ | ~$215 | Unity Catalog, DLT, ML-ready, Photon | Custo médio | ✅ Escolhido |
| **Fabric** | ~$300+ | Unified Microsoft | Imaturidade, custo | ⚠️ Futuro |

### Decision Rationale

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WHY DATABRICKS OVER SYNAPSE SERVERLESS?                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  GOVERNANCE:                                                                    │
│  • Unity Catalog = Governança centralizada GRÁTIS no Databricks                 │
│  • Synapse precisaria de Microsoft Purview (~$200/mês adicional)                │
│                                                                                 │
│  DATA QUALITY:                                                                  │
│  • DLT Expectations = DQ nativo integrado ao pipeline                           │
│  • Synapse precisaria de Great Expectations ou solução custom                   │
│                                                                                 │
│  SCALABILITY:                                                                   │
│  • Databricks escala automaticamente (auto-scale clusters)                      │
│  • Synapse Serverless tem limitações em queries complexas                       │
│                                                                                 │
│  PERFORMANCE:                                                                   │
│  • Photon engine = 2-8x mais rápido que Spark tradicional                       │
│  • Z-ordering e liquid clustering otimizados                                    │
│                                                                                 │
│  FUTURE-READY:                                                                  │
│  • ML/AI nativamente suportado (MLflow integrado)                               │
│  • Databricks Assistant para desenvolvimento                                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Consequences

**Positivas:**
- Unity Catalog fornece governance centralizada (lineage, RBAC, data discovery)
- DLT Expectations integra DQ nativamente aos pipelines
- Photon runtime acelera queries 2-8x
- Auto Loader simplifica ingestão incremental
- ML-ready (MLflow, Feature Store)
- Serverless SQL Warehouse elimina gestão de clusters para BI
- Integração nativa Power BI via Partner Connect

**Negativas:**
- Custo ~$160/mês maior que Synapse Serverless
- Curva de aprendizado para time SQL-only (Python/Spark)
- Requer Premium SKU para Unity Catalog

**Riscos:**
- Databricks pricing pode mudar → Mitigação: Reserved capacity
- Vendor lock-in → Mitigação: Delta Lake é open source, portável

### Cost Estimate

| Componente | Uso Mensal | Custo |
|------------|------------|-------|
| ADLS Gen2 Storage | 50 GB | $1.50 |
| Databricks Job Clusters | ~25 hrs | $56.00 |
| Databricks SQL Warehouse | ~100 hrs | $44.00 |
| Databricks Interactive | ~20 hrs | $8.00 |
| Private Endpoints | 3 endpoints | $21.90 |
| Log Analytics | ~10 GB | $28.10 |
| Power BI Pro | 5 usuários | $50.00 |
| **Total** | | **~$215/mês** |

### Component Choices

| Databricks Feature | Usage | Justification |
|--------------------|-------|---------------|
| **Unity Catalog** | Metastore central | Governance, lineage, RBAC |
| **Delta Live Tables** | Bronze → Silver | DQ expectations, retry logic |
| **Databricks Workflows** | Orchestration | Native, includes DLT |
| **SQL Warehouse (Serverless)** | BI queries | Auto-scale, cost-efficient |
| **Photon** | All clusters | Performance boost |
| **Auto Loader** | File ingestion | Schema evolution, checkpoints |

---

## ADR-003: Formato de Storage - Delta Lake

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir o formato de armazenamento para o Data Lakehouse. Requisitos:
- ACID transactions
- Schema evolution
- Time travel (audit, rollback)
- Compatibilidade com ferramentas de BI
- Performance de leitura

### Decision
Adotar **Delta Lake** como formato padrão para todas as camadas (Bronze, Silver, Gold).

### Alternatives Considered

| Formato | ACID | Schema Evolution | Time Travel | Compatibilidade |
|---------|------|------------------|-------------|-----------------|
| **CSV** | ❌ | ❌ | ❌ | ✅ Alta |
| **Parquet** | ❌ | ⚠️ Parcial | ❌ | ✅ Alta |
| **Delta Lake** ✅ | ✅ | ✅ | ✅ | ✅ Alta |
| **Apache Iceberg** | ✅ | ✅ | ✅ | ⚠️ Crescendo |
| **Apache Hudi** | ✅ | ✅ | ✅ | ⚠️ Menor |

### Consequences

**Positivas:**
- ACID transactions garantem consistência
- Time travel permite audit e rollback (30 dias default)
- Schema evolution sem downtime
- Suporte nativo em Synapse e Databricks
- Z-ordering para otimização de queries
- Open source (Linux Foundation)

**Negativas:**
- Overhead de metadata vs Parquet puro
- Requer vacuum periódico para cleanup

**Configuration:**
```sql
-- Time travel retention
ALTER TABLE gold.fact_trips 
SET TBLPROPERTIES ('delta.logRetentionDuration' = '30 days');

-- Auto-optimize
ALTER TABLE gold.fact_trips 
SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true');
```

---

## ADR-004: Modelo Dimensional - Star Schema (Kimball)

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir a abordagem de modelagem para a camada Gold (analytics). O projeto requer:
- Dashboards Power BI performáticos
- Queries ad-hoc por analistas
- Respostas às 20 perguntas analíticas definidas
- Facilidade de uso para não-técnicos

### Decision
Adotar **Star Schema** seguindo metodologia **Kimball** para a camada Gold.

### Alternatives Considered

| Abordagem | Prós | Contras |
|-----------|------|---------|
| **Star Schema (Kimball)** ✅ | Performance, simplicidade, BI-friendly | Menos flexível para mudanças |
| **Snowflake Schema** | Normalização, menos redundância | Queries mais complexas |
| **Data Vault 2.0** | Flexibilidade, historização | Complexidade alta, overhead |
| **One Big Table (OBT)** | Simplicidade máxima | Redundância, manutenção |
| **Wide Tables** | Performance scans | Difícil evolução |

### Consequences

**Positivas:**
- Queries simples com JOINs diretos (fact → dim)
- Performance excelente em Power BI
- Fácil entendimento por analistas de negócio
- Padrão de mercado bem documentado
- Suporta todas as 20 perguntas analíticas

**Negativas:**
- Redundância em dimensões desnormalizadas
- Mudanças em dimensões requerem reprocessamento

**Model Summary:**
```
FACT TABLE:          fact_trips (1.5M rows)
DIMENSIONS:          dim_date (365), dim_payment (6), dim_rate (6), 
                     dim_trip_type (2), dim_location (265)
GRAIN:               1 row per taxi trip
MEASURES:            8 additive, 3 derived
```

---

## ADR-005: Estratégia de Camadas - Medallion Architecture

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir como organizar os dados desde a ingestão até o consumo. Requisitos:
- Rastreabilidade (lineage)
- Reprocessamento possível
- Separação de responsabilidades
- Governança por camada

### Decision
Adotar **Medallion Architecture** com 3 camadas: Bronze (raw), Silver (curated), Gold (aggregated).

### Alternatives Considered

| Abordagem | Camadas | Prós | Contras |
|-----------|---------|------|---------|
| **Single Layer** | 1 | Simples | Sem rastreabilidade |
| **Staging + DW** | 2 | Tradicional | Limitado para lakehouse |
| **Medallion (3)** ✅ | 3 | Balanced, standard | Moderada complexidade |
| **Multi-hop (4+)** | 4+ | Granular | Over-engineering |

### Consequences

**Layer Definitions:**

| Layer | Propósito | Schema | Transformação |
|-------|-----------|--------|---------------|
| **Bronze** | Raw data preservation | Schema-on-read | None (AS-IS) |
| **Silver** | Business-ready data | Schema-on-write | Cleanse, type, validate |
| **Gold** | Analytics-optimized | Star Schema | Aggregate, enrich |

**Data Flow:**
```
Source → BRONZE (raw) → SILVER (clean) → GOLD (model)
              ↓              ↓
         Audit/Lineage   Quarantine
```

**Retention Policy:**
| Layer | Retention | Rationale |
|-------|-----------|-----------|
| Bronze | Indefinite | Source of truth, regulatory |
| Silver | 3 years | Active analytics |
| Gold | 7 years | Business reporting |

---

## ADR-006: Estratégia de SCD - Type 1 para Dimensões

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir como tratar mudanças em dimensões (Slowly Changing Dimensions). Para este projeto:
- Dimensões são pequenas e estáticas (payment, rate, trip_type)
- Não há requisito de histórico dimensional
- Simplicidade é prioritária para MVP

### Decision
Adotar **SCD Type 1** (sobrescrever) para todas as dimensões, exceto dim_date que é **Type 0** (imutável).

### Alternatives Considered

| SCD Type | Comportamento | Prós | Contras |
|----------|--------------|------|---------|
| **Type 0** | Imutável | Simples | Sem mudanças |
| **Type 1** ✅ | Sobrescreve | Simples, sempre atual | Perde histórico |
| **Type 2** | Nova row + versão | Histórico completo | Complexidade |
| **Type 3** | Coluna anterior | Histórico limitado | Parcial |
| **Type 4** | Tabela histórico | Flexível | Complexidade |
| **Type 6** | Hybrid (1+2+3) | Completo | Alta complexidade |

### Consequences

**Application:**

| Dimensão | SCD Type | Rationale |
|----------|----------|-----------|
| dim_date | Type 0 | Calendário nunca muda |
| dim_payment | Type 1 | Descrições podem mudar |
| dim_rate | Type 1 | Descrições podem mudar |
| dim_trip_type | Type 1 | Estático |
| dim_location | Type 1 | Zonas podem ser renomeadas |

**Positivas:**
- Implementação simples (MERGE statement)
- Queries sempre retornam valor atual
- Sem explosão de rows

**Negativas:**
- Não é possível analisar "como era" uma dimensão
- Se precisar Type 2 no futuro, requer refactoring

**Mitigation:**
- Bronze layer preserva estado original
- Se histórico for necessário, migrar para Type 2

---

## ADR-007: Linguagem ETL - Python/Spark + SQL

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir a linguagem para transformações ETL. Considerações:
- Plataforma é Azure Databricks
- Transformações variam de simples a moderadas
- Data Quality via DLT Expectations (requer Python)
- Visão de longo prazo inclui ML/AI

### Decision
Usar **Python com PySpark** para pipelines DLT (Bronze/Silver) e **Spark SQL** para transformações Gold e views analíticas.

### Alternatives Considered

| Linguagem | Prós | Contras | Fit |
|-----------|------|---------|-----|
| **T-SQL puro** | Familiar SQL Server | Não nativo Databricks | ❌ |
| **Spark SQL only** | SQL-friendly | Limitado em DLT | ⚠️ Parcial |
| **Python + PySpark** ✅ | DLT native, flexível, ML-ready | Curva aprendizado | ✅ Bronze/Silver |
| **Spark SQL** ✅ | Performance, BI-friendly | Menos flexível | ✅ Gold |
| **dbt-databricks** | Modular, testável | Ferramenta adicional | ⚠️ Futuro |

### Language Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LANGUAGE STRATEGY BY LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER          LANGUAGE         REASON                                     │
│  ─────          ────────         ──────                                     │
│                                                                             │
│  Bronze         Python           Auto Loader (streaming API)                │
│                 (PySpark)        Schema handling, metadata                  │
│                                                                             │
│  Silver         Python           DLT Expectations (DQ rules)                │
│                 (DLT)            Complex transformations                    │
│                                                                             │
│  Gold           Spark SQL        Dimensional modeling                       │
│                 (Notebooks)      BI-friendly syntax                         │
│                                  Easy debugging                             │
│                                                                             │
│  Views          SQL              Power BI consumption                       │
│                                  DirectQuery compatible                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Consequences

**Positivas:**
- DLT Expectations nativamente suportadas (Python API)
- Auto Loader simplifica ingestão streaming
- Spark SQL é familiar para analistas
- MLflow integration para future ML
- Best of both worlds: Python flexibility + SQL readability

**Negativas:**
- Time SQL-only precisa aprender Python basics
- Debugging mais complexo que T-SQL puro
- Dois estilos de código para manter

**Template DLT Pipeline (Bronze → Silver):**
```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    comment="Silver layer - cleaned and validated trips",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_pickup", "pickup_datetime IS NOT NULL")
@dlt.expect_or_drop("valid_dropoff", "dropoff_datetime IS NOT NULL")
@dlt.expect_or_quarantine("valid_amount", "total_amount >= 0")
@dlt.expect("valid_distance", "trip_distance >= 0 AND trip_distance < 100")
def slv_trips():
    return (
        dlt.read("lnd_green_tripdata")
        .withColumn("trip_duration_min", 
            (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime")) / 60)
        .withColumn("pickup_date", to_date("pickup_datetime"))
        .filter("pickup_datetime IS NOT NULL")
    )
```

**Template Spark SQL (Gold):**
```sql
-- Build fact_trips from silver
CREATE OR REPLACE TABLE gold.fact_trips AS
SELECT
    -- Surrogate keys
    CAST(date_format(pickup_datetime, 'yyyyMMdd') AS INT) AS date_sk,
    COALESCE(p.payment_type_sk, -1) AS payment_type_sk,
    COALESCE(r.rate_code_sk, -1) AS rate_code_sk,
    
    -- Degenerate dimensions
    PULocationID AS pickup_location_sk,
    DOLocationID AS dropoff_location_sk,
    
    -- Measures
    trip_distance,
    trip_duration_min,
    passenger_count,
    fare_amount,
    tip_amount,
    total_amount,
    
    -- Audit
    current_timestamp() AS created_at
FROM silver.slv_trips t
LEFT JOIN gold.dim_payment_type p ON t.payment_type = p.payment_type
LEFT JOIN gold.dim_rate_code r ON t.RatecodeID = r.ratecode_id
```

---

## ADR-008: Estratégia de Particionamento

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos definir estratégia de particionamento para otimizar queries e gerenciar dados. Padrões de acesso esperados:
- Queries por período (mês, semana, dia)
- Filtros por zona (location_id)
- Agregações por payment_type

### Decision
Particionar por **data** (diferentes granularidades por camada).

### Partition Strategy

| Camada | Tabela | Partition Key | Granularidade |
|--------|--------|---------------|---------------|
| Bronze | lnd_green_tripdata | year/month | Mensal (como source) |
| Silver | slv_trips | pickup_date | Diária |
| Gold | fact_trips | date_sk | Mensal |

### Consequences

**Positivas:**
- Partition pruning em queries temporais
- Facilita reprocessamento de períodos específicos
- Alinhado com padrão de ingestão (mensal)

**Negativas:**
- Queries sem filtro de data escaneiam todas partições
- Partições muito pequenas podem criar overhead

**Query Optimization:**
```sql
-- BOM: Partitioned scan
SELECT * FROM gold.fact_trips WHERE date_sk BETWEEN 20210401 AND 20210430;

-- RUIM: Full scan
SELECT * FROM gold.fact_trips WHERE payment_type_sk = 1;

-- MITIGATION: Add secondary index on payment_type_sk
```

---

## ADR-009: Estratégia de Data Quality

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos garantir qualidade dos dados ao longo do pipeline. Requisitos:
- 38 regras de DQ definidas
- Target: 99% quality rate
- Rastreabilidade de problemas
- Não bloquear pipeline por erros menores

### Decision
Implementar **DQ em camadas** com **quarantine pattern** para registros inválidos.

### DQ Strategy

```
Source → Bronze → [DQ Check] → Silver (valid) + Quarantine (invalid)
                      ↓
                  DQ Results (audit)
```

### Severity Actions

| Severidade | Ação | Destino |
|------------|------|---------|
| 🔴 CRITICAL | REJECT | Quarantine only |
| 🟡 HIGH | QUARANTINE | Quarantine, flag |
| 🟢 MEDIUM | FLAG | Silver + flag column |
| ℹ️ INFO | LOG | Silver + audit log |

### Consequences

**Positivas:**
- Pipeline não para por erros individuais
- Registros inválidos preservados para análise
- Métricas de DQ para dashboards
- Processo de correção e reprocessamento

**Negativas:**
- Overhead de tabela de quarantine
- Processo manual de revisão de quarantine

**Implementation:**
```sql
-- DQ validation example
INSERT INTO silver.slv_trips (...)
SELECT *, 
    CASE 
        WHEN total_amount < 0 THEN 'DQ-010'
        WHEN pickup_datetime > dropoff_datetime THEN 'DQ-007'
        ELSE 'VALID'
    END as dq_status
FROM bronze.lnd_green_tripdata
WHERE dq_status = 'VALID';  -- Only valid to Silver

INSERT INTO audit.quarantine_records (...)
SELECT *
FROM bronze.lnd_green_tripdata
WHERE dq_status != 'VALID';  -- Invalid to Quarantine
```

---

## ADR-010: Naming Conventions

### Status
✅ **Accepted** (2026-02-05)

### Context
Precisamos padronizar nomenclatura para consistência e manutenibilidade.

### Decision
Adotar naming conventions baseadas em melhores práticas de Data Warehousing.

### Standards

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Schema Bronze | `bronze` | `bronze.lnd_*` |
| Schema Silver | `silver` | `silver.slv_*` |
| Schema Gold | `gold` | `gold.fact_*`, `gold.dim_*` |
| Landing Table | `lnd_{source}_{entity}` | `lnd_green_tripdata` |
| Silver Table | `slv_{entity}` | `slv_trips` |
| Fact Table | `fact_{subject}` | `fact_trips` |
| Dimension | `dim_{entity}` | `dim_payment` |
| Surrogate Key | `{entity}_sk` | `trip_sk` |
| Natural Key | `{entity}_id` | `payment_type_id` |
| Foreign Key | `{ref}_sk` | `payment_type_sk` |
| Date Column | `*_date` ou `*_datetime` | `pickup_datetime` |
| Boolean | `is_*` ou `has_*` | `is_weekend` |
| Amount | `*_amount` | `fare_amount` |
| Count | `*_count` | `passenger_count` |

### Consequences

**Positivas:**
- Código auto-documentado
- Facilita onboarding de novos membros
- Queries mais legíveis
- Consistência entre artefatos

**Negativas:**
- Nomes podem ficar longos
- Requer disciplina do time

---

## Glossário de Termos

| Termo | Definição |
|-------|-----------|
| **ADR** | Architecture Decision Record - documento formal de decisão |
| **SCD** | Slowly Changing Dimension - estratégia de versionamento |
| **Medallion** | Padrão de arquitetura Bronze/Silver/Gold |
| **Lakehouse** | Arquitetura que combina Data Lake + Data Warehouse |
| **Star Schema** | Modelo dimensional com fact table central e dimensions ao redor |
| **Surrogate Key** | Chave técnica gerada (vs natural key do negócio) |
| **DQ** | Data Quality - qualidade de dados |
| **ACID** | Atomicity, Consistency, Isolation, Durability |

---

## Template de Nova ADR

```markdown
## ADR-XXX: [Título]

### Status
🟡 **Proposed** / ✅ **Accepted** / ❌ **Rejected** / 🔄 **Superseded**

### Context
[Descreva o problema e contexto]

### Decision
[Descreva a decisão tomada]

### Alternatives Considered
[Liste alternativas avaliadas]

### Consequences
[Descreva consequências positivas, negativas e riscos]
```

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Winston (DataArchitect) | Versão inicial - 10 ADRs |

---

*Documento gerado pelo 🏗️ DataArchitect Agent - Avanade™ Core*
