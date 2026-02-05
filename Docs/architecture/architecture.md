# 🏗️ Architecture Document

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 2.0  
> **Data:** 2026-02-05  
> **Autor:** 🏗️ Winston (DataArchitect)  
> **Referências:** [problem-statement.md](../strategy/problem-statement.md) | [sttm.md](../requirements/sttm.md) | [decisions.md](decisions.md)

---

## 1. Sumário Executivo

Este documento define a arquitetura técnica completa para o projeto **NYC Green Taxi Analytics**, implementando um **Data Lakehouse** com padrão **Medallion Architecture** (Bronze/Silver/Gold) utilizando **Azure Databricks** como plataforma principal de processamento.

### 1.1 Objetivo do Documento

Este documento serve como **blueprint técnico** para toda a equipe de desenvolvimento, definindo:
- Arquitetura de referência e padrões adotados
- Componentes de infraestrutura e suas interações
- Fluxos de dados end-to-end
- Políticas de segurança e governança
- Estratégias de escalabilidade e disaster recovery
- Estimativas de custo e roadmap de implementação

### 1.2 Decisões Arquiteturais Chave

| Decisão | Escolha | Justificativa | ADR |
|---------|---------|---------------|-----|
| **Padrão Arquitetural** | Lakehouse | Combina flexibilidade de Data Lake com ACID de DW | ADR-001 |
| **Plataforma de Compute** | Azure Databricks | Spark otimizado, Unity Catalog, ML-ready | ADR-002 |
| **Camadas de Dados** | Medallion (3 layers) | Separação clara de responsabilidades | ADR-005 |
| **Storage** | Azure Data Lake Gen2 | Escalabilidade, integração Azure, custo | - |
| **Formato de Arquivo** | Delta Lake | ACID, time travel, schema evolution | ADR-003 |
| **Modelo Dimensional** | Star Schema (Kimball) | Performance BI, simplicidade | ADR-004 |
| **Orquestração ETL** | Databricks Workflows | Native, integrado, observability | - |
| **Governança** | Unity Catalog | Centralizado, lineage, RBAC | - |
| **BI / Visualização** | Power BI | Integração nativa, DirectQuery | - |

### 1.3 Visão Geral da Solução

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           NYC GREEN TAXI ANALYTICS - SOLUTION OVERVIEW                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   FONTES              INGESTÃO            PROCESSAMENTO           CONSUMO              │
│   ──────              ────────            ─────────────           ───────              │
│                                                                                         │
│   ┌─────────┐        ┌─────────┐         ┌─────────────┐        ┌─────────────┐       │
│   │  CSV    │───────▶│Databricks│────────▶│ Bronze      │───────▶│ Power BI    │       │
│   │  JSON   │        │ Auto     │         │ Silver      │        │ Dashboards  │       │
│   │  TSV    │        │ Loader   │         │ Gold        │        │ Reports     │       │
│   └─────────┘        └─────────┘         └─────────────┘        └─────────────┘       │
│                            │                   │                       │               │
│                            │                   │                       │               │
│   ┌─────────────────────────────────────────────────────────────────────────────┐     │
│   │                         AZURE DATABRICKS WORKSPACE                           │     │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │     │
│   │  │ Unity    │  │ Workflows│  │ Delta    │  │ SQL      │  │ ML       │      │     │
│   │  │ Catalog  │  │ Jobs     │  │ Live     │  │ Warehouse│  │ Runtime  │      │     │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │     │
│   └─────────────────────────────────────────────────────────────────────────────┘     │
│                                         │                                             │
│   ┌─────────────────────────────────────────────────────────────────────────────┐     │
│   │                          AZURE DATA LAKE STORAGE GEN2                        │     │
│   │            ┌────────────┐  ┌────────────┐  ┌────────────┐                   │     │
│   │            │  Bronze    │  │   Silver   │  │    Gold    │                   │     │
│   │            │  Container │  │  Container │  │  Container │                   │     │
│   │            └────────────┘  └────────────┘  └────────────┘                   │     │
│   └─────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Arquitetura de Alto Nível

### 2.1 Diagrama de Arquitetura Detalhado

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    NYC GREEN TAXI ANALYTICS                                          │
│                              Data Lakehouse Architecture on Databricks                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        DATA SOURCES                                                  │
├───────────────────────┬───────────────────────┬───────────────────────┬─────────────────────────────┤
│       CSV FILES       │      JSON FILES       │       TSV FILES       │       ERROR LOGS            │
├───────────────────────┼───────────────────────┼───────────────────────┼─────────────────────────────┤
│ green_tripdata_*.csv  │ payment_type_array.json│ trip_type.tsv        │ errors_*.txt                │
│ ~500K rows/month      │ 6 records             │ 2 records             │ ~1K rows/month              │
│ 20 columns            │ Nested structure      │ Tab-separated         │ Error tracking              │
└───────────┬───────────┴───────────┬───────────┴───────────┬───────────┴─────────────┬───────────────┘
            │                       │                       │                         │
            └───────────────────────┴───────────────────────┴─────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    INGESTION LAYER                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│    ┌─────────────────────────────────────────────────────────────────────────────────────────┐     │
│    │                        DATABRICKS AUTO LOADER / COPY INTO                                │     │
│    ├─────────────────────────────────────────────────────────────────────────────────────────┤     │
│    │  • Incremental file ingestion with checkpoint                                           │     │
│    │  • Schema inference and evolution                                                        │     │
│    │  • File notification (Event Grid) or Directory listing                                  │     │
│    │  • Exactly-once semantics with idempotent writes                                        │     │
│    │  • Automatic handling of new files in landing zone                                      │     │
│    └─────────────────────────────────────────────────────────────────────────────────────────┘     │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              STORAGE LAYER - AZURE DATA LAKE GEN2                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  Storage Account: stnyctaxianalytics                                                                │
│  Hierarchical Namespace: Enabled                                                                    │
│  Redundancy: LRS (dev) / GRS (prod)                                                                 │
│                                                                                                     │
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐   ┌───────────────┐   │
│  │ Container: landing  │   │ Container: bronze   │   │ Container: silver   │   │Container: gold│   │
│  ├─────────────────────┤   ├─────────────────────┤   ├─────────────────────┤   ├───────────────┤   │
│  │ /raw/tripdata/      │   │ /lnd_green_tripdata/│   │ /slv_trips/         │   │ /fact_trips/  │   │
│  │ /raw/payment/       │   │ /lnd_payment_type/  │   │ /slv_payment_type/  │   │ /dim_date/    │   │
│  │ /raw/rate/          │   │ /lnd_rate_code/     │   │ /slv_rate_code/     │   │ /dim_payment/ │   │
│  │ /raw/trip_type/     │   │ /lnd_trip_type/     │   │ /slv_trip_type/     │   │ /dim_rate/    │   │
│  │ /raw/errors/        │   │ _checkpoints/       │   │ _checkpoints/       │   │ /dim_trip_type│   │
│  └─────────────────────┘   └─────────────────────┘   └─────────────────────┘   └───────────────┘   │
│                                                                                                     │
│  Format: Delta Lake with Parquet underlying                                                         │
│  Compression: Snappy (default)                                                                      │
│  File Size Target: 128MB - 1GB                                                                      │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PROCESSING LAYER - MEDALLION ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐   │
│  │      🥉 BRONZE LAYER       │    │      🥈 SILVER LAYER       │    │      🥇 GOLD LAYER         │   │
│  │      (Raw / Landing)      │    │      (Curated)            │    │      (Business)           │   │
│  ├───────────────────────────┤    ├───────────────────────────┤    ├───────────────────────────┤   │
│  │                           │    │                           │    │                           │   │
│  │ PURPOSE:                  │    │ PURPOSE:                  │    │ PURPOSE:                  │   │
│  │ • Preserve raw data       │    │ • Clean & validate        │    │ • Business aggregations   │   │
│  │ • Source of truth         │    │ • Apply DQ rules          │    │ • Star schema model       │   │
│  │ • Reprocessing source     │    │ • Type enforcement        │    │ • KPI calculations        │   │
│  │                           │    │ • Deduplication           │    │ • Pre-computed metrics    │   │
│  │ SCHEMA: Schema-on-read    │    │ SCHEMA: Schema-on-write   │    │ SCHEMA: Star Schema       │   │
│  │ FORMAT: Delta Lake        │    │ FORMAT: Delta Lake        │    │ FORMAT: Delta Lake        │   │
│  │ UPDATES: Append-only      │    │ UPDATES: Merge/Upsert     │    │ UPDATES: Full refresh     │   │
│  │ RETENTION: Unlimited      │    │ RETENTION: 3 years        │    │ RETENTION: 7 years        │   │
│  │                           │────▶│                           │────▶│                           │   │
│  │ TABLES:                   │DLT │ TABLES:                   │DLT │ TABLES:                   │   │
│  │ • lnd_green_tripdata      │    │ • slv_trips               │    │ • fact_trips              │   │
│  │ • lnd_payment_type        │    │ • slv_payment_type        │    │ • dim_date                │   │
│  │ • lnd_rate_code           │    │ • slv_rate_code           │    │ • dim_payment             │   │
│  │ • lnd_trip_type           │    │ • slv_trip_type           │    │ • dim_rate                │   │
│  │                           │    │                           │    │ • dim_trip_type           │   │
│  │ VOLUME: ~1.5M rows/Q      │    │ VOLUME: ~1.4M rows/Q      │    │ • dim_location            │   │
│  │ SIZE: ~300 MB             │    │ SIZE: ~280 MB             │    │ VOLUME: ~1.4M rows/Q      │   │
│  │                           │    │                           │    │ SIZE: ~400 MB             │   │
│  └───────────────────────────┘    └───────────────────────────┘    └───────────────────────────┘   │
│              │                                │                                │                   │
│              │                                │                                │                   │
│              ▼                                ▼                                ▼                   │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              AUDIT & QUARANTINE LAYER                                      │   │
│  ├───────────────────────────────────────────────────────────────────────────────────────────┤   │
│  │  audit.dq_results          │  audit.quarantine_records      │  audit.pipeline_runs        │   │
│  │  • Rule execution results  │  • Rejected records            │  • Job execution logs       │   │
│  │  • Pass/fail metrics       │  • Rule violations             │  • Duration, status         │   │
│  │  • Trend analysis          │  • Reprocessing queue          │  • Row counts               │   │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    SERVING LAYER                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────┐    ┌─────────────────────────────────┐                        │
│  │   DATABRICKS SQL WAREHOUSE      │    │         POWER BI                 │                        │
│  ├─────────────────────────────────┤    ├─────────────────────────────────┤                        │
│  │  • Serverless SQL endpoint      │    │  • DirectQuery to Databricks    │                        │
│  │  • Auto-scaling (2-8 clusters)  │───▶│  • Import mode for aggregates   │                        │
│  │  • Query caching                │    │  • Row-level security           │                        │
│  │  • Cost: $0.55/DBU              │    │  • Scheduled refresh            │                        │
│  │  • T-SQL compatible             │    │  • 5 Pro licenses               │                        │
│  └─────────────────────────────────┘    └─────────────────────────────────┘                        │
│                                                                                                     │
│  VIEWS EXPOSED:                                                                                     │
│  • vw_trip_summary         - Daily aggregations                                                    │
│  • vw_revenue_by_zone      - Revenue by pickup/dropoff zone                                        │
│  • vw_payment_analysis     - Payment type breakdown                                                │
│  • vw_hourly_demand        - Hourly patterns for heatmaps                                          │
│  • vw_kpi_dashboard        - Pre-calculated KPIs                                                   │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              MONITORING & OBSERVABILITY                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌────────────────┐  │
│  │  DATABRICKS MONITOR  │  │   AZURE MONITOR      │  │  LOG ANALYTICS       │  │  ALERTING      │  │
│  ├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤  ├────────────────┤  │
│  │ • Job run metrics    │  │ • Platform metrics   │  │ • Query logs         │  │ • PagerDuty    │  │
│  │ • Cluster metrics    │  │ • Storage metrics    │  │ • Audit logs         │  │ • Slack        │  │
│  │ • SQL warehouse      │  │ • Cost tracking      │  │ • DQ results         │  │ • Email        │  │
│  │ • Data quality       │  │ • Health dashboard   │  │ • Custom queries     │  │ • Teams        │  │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └────────────────┘  │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Componentes da Arquitetura

| Componente | Tecnologia | Versão | Propósito | Configuração |
|------------|------------|--------|-----------|--------------|
| **Storage** | Azure Data Lake Gen2 | - | Armazenamento centralizado | HNS enabled, LRS/GRS |
| **Format** | Delta Lake | 2.4+ | ACID, versioning, time travel | 30 days retention |
| **Compute** | Azure Databricks | 14.x LTS | ETL, Analytics, ML | Premium tier |
| **ETL Engine** | Delta Live Tables | - | Declarative ETL pipelines | Development mode |
| **Orchestration** | Databricks Workflows | - | Job scheduling, dependencies | Cron triggers |
| **Governance** | Unity Catalog | - | Data governance, lineage, RBAC | Workspace-level |
| **SQL** | Databricks SQL Warehouse | Serverless | Ad-hoc queries, BI | 2X-Small |
| **BI** | Power BI | Pro | Dashboards, reports | DirectQuery |
| **Monitoring** | Azure Monitor + Databricks | - | Observability | 30 days retention |
| **Alerting** | Azure Alerts | - | Notifications | Email + Teams |

### 2.3 Integrações Externas

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              INTEGRATION ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────────┐
                                    │  AZURE ACTIVE   │
                                    │   DIRECTORY     │
                                    │  (Identity)     │
                                    └────────┬────────┘
                                             │ OAuth 2.0 / SCIM
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
          ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
          │   DATABRICKS    │      │   POWER BI      │      │   AZURE         │
          │   WORKSPACE     │◀────▶│   SERVICE       │      │   KEY VAULT     │
          │                 │      │                 │      │   (Secrets)     │
          └────────┬────────┘      └─────────────────┘      └────────┬────────┘
                   │                                                  │
                   │ ABFSS://                                         │ Secret Scope
                   ▼                                                  ▼
          ┌─────────────────┐                                ┌─────────────────┐
          │   ADLS GEN2     │                                │   CONNECTION    │
          │   STORAGE       │                                │   STRINGS       │
          └─────────────────┘                                └─────────────────┘
```

---

## 3. Data Layers (Medallion Architecture) - Detalhado

### 3.1 Bronze Layer (Landing/Raw)

**Propósito:** Armazenamento de dados brutos, exatamente como recebidos da fonte. Esta camada serve como **single source of truth** e permite reprocessamento completo.

#### 3.1.1 Características Técnicas

| Característica | Valor | Detalhes |
|----------------|-------|----------|
| **Schema** | Schema-on-read | Infere schema durante leitura, permite evolução |
| **Transformação** | Nenhuma (raw) | Dados exatamente como recebidos |
| **Formato** | Delta Lake | ACID garantido, time travel habilitado |
| **Partição** | Por data de ingestão | `year=YYYY/month=MM` |
| **Retenção** | Ilimitada | Archive tier após 1 ano |
| **Acesso** | ETL processes only | Service Principal ou Managed Identity |
| **Compressão** | Snappy (default) | ~70% compression ratio |
| **File Size** | Target 128MB | Optimize automático |

#### 3.1.2 Tabelas Bronze - Especificação

**bronze.lnd_green_tripdata**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        lnd_green_tripdata                                │
├─────────────────────────────────────────────────────────────────────────┤
│ Storage Path: abfss://bronze@stnyctaxi.dfs.core.windows.net/            │
│               lnd_green_tripdata/year=2021/month=04/                    │
├─────────────────────────────────────────────────────────────────────────┤
│ Partitioning: year (INT), month (INT)                                   │
│ Format: Delta Lake                                                       │
│ Clustering: None (raw data)                                              │
├─────────────────────────────────────────────────────────────────────────┤
│ COLUMNS:                                                                 │
│ ─────────────────────────────────────────────────────────────────────── │
│ vendor_id               INT         Provider code (1, 2)                │
│ pickup_datetime         STRING      Raw datetime string                 │
│ dropoff_datetime        STRING      Raw datetime string                 │
│ store_and_fwd_flag      STRING      Y/N flag                            │
│ ratecode_id             INT         Rate code (1-6)                     │
│ pu_location_id          INT         Pickup zone ID (1-265)              │
│ do_location_id          INT         Dropoff zone ID (1-265)             │
│ passenger_count         INT         Number of passengers                │
│ trip_distance           DOUBLE      Distance in miles                   │
│ fare_amount             DOUBLE      Base fare                           │
│ extra                   DOUBLE      Rush hour/overnight extras          │
│ mta_tax                 DOUBLE      MTA tax ($0.50)                     │
│ tip_amount              DOUBLE      Tip (card only)                     │
│ tolls_amount            DOUBLE      Tolls                               │
│ ehail_fee               DOUBLE      E-hail fee (deprecated)             │
│ improvement_surcharge   DOUBLE      Improvement surcharge ($0.30)       │
│ total_amount            DOUBLE      Total trip amount                   │
│ payment_type            INT         Payment method (1-6)                │
│ trip_type               INT         Street-hail vs dispatch (1-2)       │
│ congestion_surcharge    DOUBLE      Congestion fee ($2.75)              │
│ ─────────────────────────────────────────────────────────────────────── │
│ METADATA COLUMNS (added during ingestion):                              │
│ _source_file            STRING      Source filename                     │
│ _ingestion_timestamp    TIMESTAMP   When data was loaded                │
│ _batch_id               STRING      Batch identifier                    │
└─────────────────────────────────────────────────────────────────────────┘
```

**bronze.lnd_payment_type** / **bronze.lnd_rate_code** / **bronze.lnd_trip_type**
```
┌─────────────────────────────────────────────────────────────────────────┐
│                      REFERENCE TABLES (BRONZE)                           │
├──────────────────────┬──────────────────────┬───────────────────────────┤
│  lnd_payment_type    │   lnd_rate_code      │    lnd_trip_type          │
├──────────────────────┼──────────────────────┼───────────────────────────┤
│ payment_type_id  INT │ rate_code_id     INT │ trip_type_id          INT │
│ payment_desc  STRING │ rate_code_desc STRING│ trip_type_desc     STRING │
│ _raw_json    STRING  │ _ingestion_ts    TS  │ _ingestion_ts          TS │
│ _ingestion_ts    TS  │                      │                           │
├──────────────────────┼──────────────────────┼───────────────────────────┤
│ Records: 6           │ Records: 6           │ Records: 2                │
│ Source: JSON         │ Source: JSON         │ Source: TSV               │
└──────────────────────┴──────────────────────┴───────────────────────────┘
```

#### 3.1.3 Ingestion Pattern - Auto Loader

```python
# Databricks Auto Loader Configuration for Bronze
spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "csv") \
    .option("cloudFiles.schemaLocation", checkpoint_path) \
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
    .option("cloudFiles.inferColumnTypes", "true") \
    .option("header", "true") \
    .load(landing_path) \
    .withColumn("_source_file", input_file_name()) \
    .withColumn("_ingestion_timestamp", current_timestamp()) \
    .withColumn("_batch_id", lit(batch_id)) \
    .writeStream \
    .format("delta") \
    .option("checkpointLocation", checkpoint_path) \
    .option("mergeSchema", "true") \
    .partitionBy("year", "month") \
    .trigger(availableNow=True) \
    .toTable("bronze.lnd_green_tripdata")
```

### 3.2 Silver Layer (Curated/Cleansed)

**Propósito:** Dados limpos, tipados, validados e deduplicados. Esta camada aplica regras de qualidade e prepara dados para consumo analítico.

#### 3.2.1 Características Técnicas

| Característica | Valor | Detalhes |
|----------------|-------|----------|
| **Schema** | Schema-on-write (enforced) | Schema definido, evolução controlada |
| **Transformação** | Cleanse, type, validate, dedupe | 38 regras DQ aplicadas |
| **Formato** | Delta Lake | ACID, schema enforcement |
| **Partição** | Por data do evento | `pickup_date` (daily) |
| **Retenção** | 3 anos | Purge após 3 anos |
| **Acesso** | Analytics, Data Science | Read para analistas |
| **Z-Order** | `pickup_datetime, pu_location_id` | Query optimization |
| **File Size** | Target 256MB | Compacted files |

#### 3.2.2 Tabela Principal - slv_trips

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    slv_trips                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Storage Path: abfss://silver@stnyctaxi.dfs.core.windows.net/slv_trips/              │
│ Partitioning: pickup_date (DATE)                                                     │
│ Z-Order: pickup_datetime, pu_location_id                                             │
│ Format: Delta Lake with schema enforcement                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ COLUMN                    TYPE              NULLABLE   DQ RULES                      │
│ ─────────────────────────────────────────────────────────────────────────────────── │
│ trip_id                   BIGINT            NO         PK, UNIQUE                    │
│ vendor_id                 INT               YES        IN(1,2)                       │
│ pickup_datetime           TIMESTAMP         NO         NOT NULL, VALID_DATE          │
│ dropoff_datetime          TIMESTAMP         NO         NOT NULL, > pickup            │
│ pickup_date               DATE              NO         DERIVED, partition key        │
│ store_and_fwd_flag        BOOLEAN           YES        Converted Y/N → true/false    │
│ ratecode_id               INT               YES        IN(1-6), FK                   │
│ pu_location_id            INT               YES        BETWEEN 1-265                 │
│ do_location_id            INT               YES        BETWEEN 1-265                 │
│ passenger_count           INT               YES        BETWEEN 0-9, DEFAULT 1        │
│ trip_distance             DECIMAL(10,2)     YES        >= 0, < 100                   │
│ fare_amount               DECIMAL(10,2)     YES        >= 0                          │
│ extra                     DECIMAL(10,2)     YES        >= 0                          │
│ mta_tax                   DECIMAL(10,2)     YES        IN(0, 0.5)                    │
│ tip_amount                DECIMAL(10,2)     YES        >= 0, <= fare*100%            │
│ tolls_amount              DECIMAL(10,2)     YES        >= 0                          │
│ ehail_fee                 DECIMAL(10,2)     YES        COALESCE(0)                   │
│ improvement_surcharge     DECIMAL(10,2)     YES        IN(0, 0.3)                    │
│ total_amount              DECIMAL(10,2)     YES        >= 0, CONSISTENCY CHECK       │
│ payment_type_id           INT               YES        IN(1-6), FK                   │
│ trip_type_id              INT               YES        IN(1,2), FK                   │
│ congestion_surcharge      DECIMAL(10,2)     YES        COALESCE(0)                   │
│ ─────────────────────────────────────────────────────────────────────────────────── │
│ DERIVED/CALCULATED COLUMNS:                                                          │
│ trip_duration_min         INT               YES        DATEDIFF(dropoff, pickup)     │
│ trip_duration_sec         INT               YES        DATEDIFF seconds              │
│ avg_speed_mph             DECIMAL(5,2)      YES        distance / (duration/60)      │
│ ─────────────────────────────────────────────────────────────────────────────────── │
│ AUDIT COLUMNS:                                                                       │
│ dq_status                 STRING            NO         'VALID'|'FLAGGED'|'QUARANTINE'│
│ dq_rules_failed           STRING            YES        Comma-separated rule IDs      │
│ dq_score                  DECIMAL(5,2)      YES        Quality score 0-100           │
│ _source_bronze_id         BIGINT            YES        Reference to bronze record    │
│ _process_timestamp        TIMESTAMP         NO         When processed to silver      │
│ _pipeline_run_id          STRING            NO         DLT pipeline run ID           │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2.3 Delta Live Tables Pipeline (Silver)

```python
# DLT Pipeline Definition for Silver Layer
import dlt
from pyspark.sql.functions import *

@dlt.table(
    name="slv_trips",
    comment="Cleansed and validated taxi trip data",
    table_properties={
        "quality": "silver",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    },
    partition_cols=["pickup_date"]
)
@dlt.expect_or_drop("valid_pickup_datetime", "pickup_datetime IS NOT NULL")
@dlt.expect_or_drop("valid_dropoff_datetime", "dropoff_datetime IS NOT NULL")
@dlt.expect_or_drop("valid_total_amount", "total_amount >= 0")
@dlt.expect_or_quarantine("valid_trip_duration", "trip_duration_min > 0 AND trip_duration_min < 1440")
@dlt.expect_or_quarantine("valid_trip_distance", "trip_distance >= 0 AND trip_distance < 100")
@dlt.expect("valid_payment_type", "payment_type_id IN (1,2,3,4,5,6)")
def slv_trips():
    return (
        dlt.read("bronze.lnd_green_tripdata")
        .withColumn("pickup_datetime", to_timestamp("pickup_datetime"))
        .withColumn("dropoff_datetime", to_timestamp("dropoff_datetime"))
        .withColumn("pickup_date", to_date("pickup_datetime"))
        .withColumn("trip_duration_min", 
            (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime")) / 60)
        .withColumn("trip_id", monotonically_increasing_id())
        .withColumn("dq_status", lit("VALID"))
        .withColumn("_process_timestamp", current_timestamp())
    )
```

### 3.3 Gold Layer (Aggregated/Business)

**Propósito:** Modelo dimensional otimizado para análise e BI. Star Schema para performance máxima em queries analíticas.

#### 3.3.1 Características Técnicas

| Característica | Valor | Detalhes |
|----------------|-------|----------|
| **Schema** | Star Schema (Kimball) | Fact + Dimensions |
| **Transformação** | Aggregate, enrich, model | Business rules applied |
| **Formato** | Delta Lake | Optimized for BI |
| **Partição** | Por data (facts) | `date_sk` (monthly buckets) |
| **Retenção** | 7 anos | Regulatory compliance |
| **Acesso** | BI, Reports, Dashboards | Power BI DirectQuery |
| **Z-Order** | `date_sk, payment_type_sk` | BI query patterns |
| **Clustering** | `date_sk` | Time-series queries |

#### 3.3.2 Modelo Dimensional - Star Schema Detalhado

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    GOLD LAYER - STAR SCHEMA                                          │
│                                   Grain: 1 row per taxi trip                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                          ┌────────────────────────────────┐
                                          │          dim_date              │
                                          │         (Type 0 SCD)           │
                                          ├────────────────────────────────┤
                                          │ 🔑 date_sk          INT     PK │
                                          │    full_date        DATE    NK │
                                          │    day_of_week      INT        │
                                          │    day_name         STRING     │
                                          │    day_of_month     INT        │
                                          │    day_of_year      INT        │
                                          │    week_of_year     INT        │
                                          │    month_num        INT        │
                                          │    month_name       STRING     │
                                          │    quarter          INT        │
                                          │    quarter_name     STRING     │
                                          │    year             INT        │
                                          │    year_month       STRING     │
                                          │    is_weekend       BOOLEAN    │
                                          │    is_holiday       BOOLEAN    │
                                          │    holiday_name     STRING     │
                                          │    fiscal_year      INT        │
                                          │    fiscal_quarter   INT        │
                                          ├────────────────────────────────┤
                                          │ Records: 365/year              │
                                          │ Range: 2021-01-01 to 2021-12-31│
                                          └───────────────┬────────────────┘
                                                          │
                                                          │ 1:N
                                                          │
┌────────────────────────────────┐                        │                        ┌────────────────────────────────┐
│        dim_payment             │                        │                        │         dim_rate               │
│       (Type 1 SCD)             │                        │                        │        (Type 1 SCD)            │
├────────────────────────────────┤                        │                        ├────────────────────────────────┤
│ 🔑 payment_type_sk    INT   PK │                        │                        │ 🔑 rate_code_sk       INT   PK │
│    payment_type_id    INT   NK │                        │                        │    rate_code_id       INT   NK │
│    payment_type_desc  STRING   │                        │                        │    rate_code_desc     STRING   │
│    is_electronic      BOOLEAN  │                        │                        │    is_airport         BOOLEAN  │
│    is_tip_tracked     BOOLEAN  │                        │                        │    is_flat_rate       BOOLEAN  │
│    payment_category   STRING   │                        │                        │    rate_category      STRING   │
├────────────────────────────────┤                        │                        ├────────────────────────────────┤
│ Records: 6                     │                        │                        │ Records: 6                     │
│ 1=Credit, 2=Cash, 3=No charge  │                        │                        │ 1=Standard, 2=JFK, 3=Newark    │
│ 4=Dispute, 5=Unknown, 6=Voided │                        │                        │ 4=Nassau, 5=Negotiated, 6=Group│
└─────────────┬──────────────────┘                        │                        └──────────────┬─────────────────┘
              │                                           │                                       │
              │ 1:N                                       │                                       │ 1:N
              │        ┌──────────────────────────────────┴───────────────────────────────────┐   │
              │        │                                                                      │   │
              └───────▶│                          fact_trips                                  │◀──┘
                       │                    (Transaction Fact Table)                          │
                       ├──────────────────────────────────────────────────────────────────────┤
                       │ 🔑 trip_sk                  BIGINT              PK (Surrogate)       │
                       │    trip_id                  BIGINT              NK (Natural)         │
                       │ ─────────────────────────────────────────────────────────────────────│
                       │ DIMENSION KEYS (Foreign Keys):                                       │
                       │    date_sk                  INT                 FK → dim_date        │
                       │    pickup_time_sk           INT                 Degenerate (HHMM)    │
                       │    dropoff_time_sk          INT                 Degenerate (HHMM)    │
                       │    pickup_location_sk       INT                 FK → dim_location    │
                       │    dropoff_location_sk      INT                 FK → dim_location    │
                       │    payment_type_sk          INT                 FK → dim_payment     │
                       │    rate_code_sk             INT                 FK → dim_rate        │
                       │    trip_type_sk             INT                 FK → dim_trip_type   │
                       │ ─────────────────────────────────────────────────────────────────────│
                       │ DEGENERATE DIMENSIONS:                                               │
                       │    vendor_id                INT                 1 or 2               │
                       │    pickup_hour              INT                 0-23                 │
                       │    dropoff_hour             INT                 0-23                 │
                       │ ─────────────────────────────────────────────────────────────────────│
                       │ MEASURES (Additive):                                                 │
                       │    passenger_count          INT                 Discrete             │
                       │    trip_distance            DECIMAL(10,2)       Miles                │
                       │    trip_duration_min        INT                 Minutes              │
                       │    fare_amount              DECIMAL(10,2)       Base fare $          │
                       │    extra_amount             DECIMAL(10,2)       Extras $             │
                       │    mta_tax                  DECIMAL(10,2)       MTA tax $            │
                       │    tip_amount               DECIMAL(10,2)       Tip $                │
                       │    tolls_amount             DECIMAL(10,2)       Tolls $              │
                       │    improvement_surcharge    DECIMAL(10,2)       Surcharge $          │
                       │    congestion_surcharge     DECIMAL(10,2)       Congestion $         │
                       │    total_amount             DECIMAL(10,2)       Total $              │
                       │ ─────────────────────────────────────────────────────────────────────│
                       │ DERIVED MEASURES (Calculated):                                       │
                       │    revenue_per_mile         DECIMAL(10,4)       total/distance       │
                       │    revenue_per_minute       DECIMAL(10,4)       total/duration       │
                       │    tip_percentage           DECIMAL(5,2)        tip/fare * 100       │
                       │    avg_speed_mph            DECIMAL(5,2)        distance/(dur/60)    │
                       │ ─────────────────────────────────────────────────────────────────────│
                       │ Grain: 1 row per taxi trip                                           │
                       │ Volume: ~1.5M rows/quarter, ~6M rows/year                            │
                       │ Partitioning: date_sk (monthly)                                      │
                       │ Z-Order: date_sk, payment_type_sk, pickup_location_sk                │
                       └─────────────────────────────────────────┬────────────────────────────┘
                                                                 │
              ┌──────────────────────────────────────────────────┴───────────────────────────────────┐
              │                                                                                      │
              │ 1:N                                                                            1:N   │
              ▼                                                                                      ▼
┌────────────────────────────────┐                                              ┌────────────────────────────────┐
│       dim_trip_type            │                                              │        dim_location            │
│       (Type 1 SCD)             │                                              │        (Type 1 SCD)            │
├────────────────────────────────┤                                              ├────────────────────────────────┤
│ 🔑 trip_type_sk       INT   PK │                                              │ 🔑 location_sk        INT   PK │
│    trip_type_id       INT   NK │                                              │    location_id        INT   NK │
│    trip_type_desc     STRING   │                                              │    borough            STRING   │
│    is_dispatch        BOOLEAN  │                                              │    zone_name          STRING   │
│    channel_category   STRING   │                                              │    service_zone       STRING   │
├────────────────────────────────┤                                              │    latitude           DECIMAL  │
│ Records: 2                     │                                              │    longitude          DECIMAL  │
│ 1 = Street-hail                │                                              ├────────────────────────────────┤
│ 2 = Dispatch (app/phone)       │                                              │ Records: 265 (TLC zones)       │
└────────────────────────────────┘                                              │ Source: NYC TLC Shapefile      │
                                                                                │ Status: External data required │
                                                                                └────────────────────────────────┘
```

#### 3.3.3 Aggregation Tables (Pre-computed)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              PRE-AGGREGATED TABLES (GOLD)                                            │
│                            For Dashboard Performance Optimization                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌───────────────────────────────────────┐    ┌───────────────────────────────────────┐            │
│  │       agg_daily_summary               │    │       agg_hourly_demand               │            │
│  ├───────────────────────────────────────┤    ├───────────────────────────────────────┤            │
│  │ date_sk                INT         PK │    │ date_sk                INT            │            │
│  │ total_trips            BIGINT         │    │ hour                   INT            │            │
│  │ total_revenue          DECIMAL        │    │ pu_location_id         INT            │            │
│  │ total_distance         DECIMAL        │    │ trip_count             INT            │            │
│  │ avg_revenue_per_trip   DECIMAL        │    │ avg_wait_time_proxy    DECIMAL        │            │
│  │ avg_trip_distance      DECIMAL        │    │ PK: (date_sk, hour, pu_location_id)   │            │
│  │ avg_trip_duration      DECIMAL        │    ├───────────────────────────────────────┤            │
│  │ total_tips             DECIMAL        │    │ Use: Hourly heatmaps, demand analysis │            │
│  │ pct_electronic_payment DECIMAL        │    │ Refresh: Daily                        │            │
│  ├───────────────────────────────────────┤    └───────────────────────────────────────┘            │
│  │ Use: KPI cards, trend lines           │                                                         │
│  │ Refresh: Daily at 06:00               │    ┌───────────────────────────────────────┐            │
│  └───────────────────────────────────────┘    │       agg_zone_revenue                │            │
│                                               ├───────────────────────────────────────┤            │
│  ┌───────────────────────────────────────┐    │ date_sk                INT            │            │
│  │       agg_monthly_kpis                │    │ pu_location_id         INT            │            │
│  ├───────────────────────────────────────┤    │ do_location_id         INT            │            │
│  │ year_month            STRING       PK │    │ trip_count             INT            │            │
│  │ kpi_avg_revenue       DECIMAL         │    │ total_revenue          DECIMAL        │            │
│  │ kpi_fleet_utilization DECIMAL         │    │ avg_revenue            DECIMAL        │            │
│  │ kpi_dq_rate           DECIMAL         │    │ avg_distance           DECIMAL        │            │
│  │ kpi_trips_count       BIGINT          │    │ PK: (date_sk, pu_loc, do_loc)         │            │
│  │ mom_growth_pct        DECIMAL         │    ├───────────────────────────────────────┤            │
│  │ yoy_growth_pct        DECIMAL         │    │ Use: Route analysis, geographic view  │            │
│  ├───────────────────────────────────────┤    │ Refresh: Daily                        │            │
│  │ Use: Executive dashboard, trends      │    └───────────────────────────────────────┘            │
│  │ Refresh: Monthly after close          │                                                         │
│  └───────────────────────────────────────┘                                                         │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Naming Convention:** `gold.fact_{subject}`, `gold.dim_{entity}`, `gold.agg_{grain}_{subject}`

---

## 4. Technology Stack - Azure Databricks (Detalhado)

### 4.1 Arquitetura Databricks

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  AZURE DATABRICKS ARCHITECTURE                                       │
│                                       Premium Tier Workspace                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      CONTROL PLANE (Managed by Databricks)                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐            │
│  │   Web UI         │  │   REST API       │  │   Workflow       │  │   Unity Catalog  │            │
│  │   (Notebooks)    │  │   (Automation)   │  │   Orchestrator   │  │   (Governance)   │            │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                │ Secure Connection
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      DATA PLANE (In Customer Subscription)                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │                                COMPUTE RESOURCES                                         │       │
│  ├─────────────────────────────────────────────────────────────────────────────────────────┤       │
│  │                                                                                         │       │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐     │       │
│  │  │                        JOB CLUSTERS (ETL Workloads)                            │     │       │
│  │  ├───────────────────────────────────────────────────────────────────────────────┤     │       │
│  │  │  Cluster: etl-bronze-cluster                                                  │     │       │
│  │  │  • Runtime: 14.3 LTS (Spark 3.5.0, Scala 2.12)                               │     │       │
│  │  │  • Node Type: Standard_DS3_v2 (4 cores, 14GB)                                │     │       │
│  │  │  • Workers: 2-8 (autoscale)                                                   │     │       │
│  │  │  • Spot instances: 70% (cost savings)                                         │     │       │
│  │  │  • Use: Bronze layer ingestion                                                │     │       │
│  │  ├───────────────────────────────────────────────────────────────────────────────┤     │       │
│  │  │  Cluster: etl-silver-gold-cluster                                             │     │       │
│  │  │  • Runtime: 14.3 LTS                                                          │     │       │
│  │  │  • Node Type: Standard_DS4_v2 (8 cores, 28GB)                                │     │       │
│  │  │  • Workers: 2-4 (autoscale)                                                   │     │       │
│  │  │  • Photon: Enabled (faster queries)                                           │     │       │
│  │  │  • Use: Silver/Gold transformations                                           │     │       │
│  │  └───────────────────────────────────────────────────────────────────────────────┘     │       │
│  │                                                                                         │       │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐     │       │
│  │  │                     SQL WAREHOUSE (BI & Ad-hoc Queries)                        │     │       │
│  │  ├───────────────────────────────────────────────────────────────────────────────┤     │       │
│  │  │  Warehouse: nyctaxi-sql-warehouse                                             │     │       │
│  │  │  • Type: Serverless                                                           │     │       │
│  │  │  • Size: 2X-Small (8 DBU)                                                     │     │       │
│  │  │  • Auto-stop: 10 minutes                                                      │     │       │
│  │  │  • Scaling: 1-2 clusters                                                      │     │       │
│  │  │  • Use: Power BI DirectQuery, ad-hoc analysis                                │     │       │
│  │  │  • Cost: $0.55/DBU (serverless)                                              │     │       │
│  │  └───────────────────────────────────────────────────────────────────────────────┘     │       │
│  │                                                                                         │       │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐     │       │
│  │  │                     DELTA LIVE TABLES (DLT) Pipeline                           │     │       │
│  │  ├───────────────────────────────────────────────────────────────────────────────┤     │       │
│  │  │  Pipeline: nyctaxi-etl-pipeline                                               │     │       │
│  │  │  • Mode: Triggered (not continuous)                                           │     │       │
│  │  │  • Development: Enabled (for testing)                                         │     │       │
│  │  │  • Product Edition: Advanced (DQ expectations)                                │     │       │
│  │  │  • Target Schema: bronze, silver, gold                                        │     │       │
│  │  │  • Use: Declarative ETL with built-in lineage                                │     │       │
│  │  └───────────────────────────────────────────────────────────────────────────────┘     │       │
│  │                                                                                         │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │                                   STORAGE (DBFS + External)                              │       │
│  ├─────────────────────────────────────────────────────────────────────────────────────────┤       │
│  │                                                                                         │       │
│  │  EXTERNAL LOCATIONS (Unity Catalog managed):                                            │       │
│  │  • abfss://landing@stnyctaxi.dfs.core.windows.net/   → Raw files                       │       │
│  │  • abfss://bronze@stnyctaxi.dfs.core.windows.net/    → Bronze Delta tables             │       │
│  │  • abfss://silver@stnyctaxi.dfs.core.windows.net/    → Silver Delta tables             │       │
│  │  • abfss://gold@stnyctaxi.dfs.core.windows.net/      → Gold Delta tables               │       │
│  │                                                                                         │       │
│  │  MANAGED TABLES (Unity Catalog):                                                        │       │
│  │  • Catalog: nyctaxi_catalog                                                            │       │
│  │  • Schemas: bronze, silver, gold, audit                                                │       │
│  │                                                                                         │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Unity Catalog - Governança

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    UNITY CATALOG HIERARCHY                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌────────────────────────────────┐
                              │         METASTORE              │
                              │    (nyctaxi-metastore)         │
                              │    Region: East US 2           │
                              └───────────────┬────────────────┘
                                              │
                              ┌───────────────┴────────────────┐
                              │                                │
                              ▼                                ▼
                ┌─────────────────────────┐      ┌─────────────────────────┐
                │     CATALOG (DEV)       │      │     CATALOG (PROD)      │
                │   nyctaxi_dev           │      │   nyctaxi_prod          │
                └───────────┬─────────────┘      └───────────┬─────────────┘
                            │                                │
          ┌─────────────────┼─────────────────┐              │ (same structure)
          │                 │                 │              │
          ▼                 ▼                 ▼              ▼
    ┌───────────┐     ┌───────────┐     ┌───────────┐
    │  SCHEMA   │     │  SCHEMA   │     │  SCHEMA   │
    │  bronze   │     │  silver   │     │   gold    │
    ├───────────┤     ├───────────┤     ├───────────┤
    │ • lnd_*   │     │ • slv_*   │     │ • fact_*  │
    │  tables   │     │  tables   │     │ • dim_*   │
    │           │     │           │     │ • agg_*   │
    │           │     │           │     │ • vw_*    │
    └───────────┘     └───────────┘     └───────────┘
          │                 │                 │
          │                 │                 │
          ▼                 ▼                 ▼
    ┌──────────────────────────────────────────────────────────────┐
    │                    TABLE-LEVEL PERMISSIONS                    │
    ├──────────────────────────────────────────────────────────────┤
    │  ROLE: data_engineer                                         │
    │  • bronze.*  → ALL PRIVILEGES                                │
    │  • silver.*  → ALL PRIVILEGES                                │
    │  • gold.*    → ALL PRIVILEGES                                │
    ├──────────────────────────────────────────────────────────────┤
    │  ROLE: data_analyst                                          │
    │  • bronze.*  → (none)                                        │
    │  • silver.*  → SELECT                                        │
    │  • gold.*    → SELECT                                        │
    ├──────────────────────────────────────────────────────────────┤
    │  ROLE: bi_developer                                          │
    │  • bronze.*  → (none)                                        │
    │  • silver.*  → (none)                                        │
    │  • gold.*    → SELECT (views only)                           │
    ├──────────────────────────────────────────────────────────────┤
    │  ROLE: data_scientist                                        │
    │  • bronze.*  → (none)                                        │
    │  • silver.*  → SELECT                                        │
    │  • gold.*    → SELECT                                        │
    └──────────────────────────────────────────────────────────────┘
```

### 4.3 Databricks Workflows - Orquestração

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    WORKFLOW: nyctaxi-daily-etl                                       │
│                                    Schedule: Daily at 02:00 UTC                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   START     │────▶│  Task 1:    │────▶│  Task 2:    │────▶│  Task 3:    │────▶│  Task 4:    │
│  (Trigger)  │     │ Load Bronze │     │  DQ Check   │     │ Transform   │     │ Build Gold  │
│             │     │             │     │             │     │  Silver     │     │             │
└─────────────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
                           │                   │                   │                   │
                           │                   │                   │                   │
                    ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
                    │ Cluster:    │     │ Python      │     │ DLT         │     │ SQL         │
                    │ etl-bronze  │     │ Notebook    │     │ Pipeline    │     │ Notebook    │
                    │ Auto Loader │     │ Validation  │     │ Bronze→Slv  │     │ Slv→Gold    │
                    │ 5-10 min    │     │ 2 min       │     │ 10-15 min   │     │ 5-10 min    │
                    └─────────────┘     └──────┬──────┘     └─────────────┘     └──────┬──────┘
                                               │                                       │
                                        ┌──────▼──────┐                         ┌──────▼──────┐
                                        │  On Fail:   │                         │  On Success:│
                                        │ Quarantine  │                         │ Notify      │
                                        │ Alert       │                         │ Refresh BI  │
                                        └─────────────┘                         └─────────────┘

DEPENDENCIES:
Task 1 → Task 2 → Task 3 → Task 4 (sequential)

RETRY POLICY:
• Max retries: 2
• Retry delay: 5 minutes

ALERTING:
• On failure: Email + Slack #data-alerts
• On success: Slack #data-updates (silent)

TIMEOUT:
• Task timeout: 30 minutes
• Job timeout: 2 hours
```

### 4.4 Comparativo Final: Por que Databricks?

| Aspecto | Azure Synapse Serverless | Azure Databricks | Decisão |
|---------|--------------------------|------------------|---------|
| **Custo Inicial** | ~$52/mês | ~$120/mês | Synapse ✓ |
| **Escalabilidade** | Limitada | Excelente (autoscale) | Databricks ✓ |
| **Performance ETL** | Boa | Excelente (Photon) | Databricks ✓ |
| **Governança** | Básica | Unity Catalog (completa) | Databricks ✓ |
| **Data Quality** | Manual | DLT Expectations (nativo) | Databricks ✓ |
| **ML/AI Ready** | Não | MLflow integrado | Databricks ✓ |
| **Lineage** | Purview (separado) | Unity Catalog (built-in) | Databricks ✓ |
| **DevOps/CI-CD** | ADF Git | Repos, APIs, Terraform | Databricks ✓ |
| **Expertise Time** | SQL | Spark + SQL | Empate |
| **Futuro-proof** | Estável | Inovação constante | Databricks ✓ |

**Decisão Final:** **Azure Databricks** - trade-off de custo maior (~$70/mês a mais) justificado por:
- Governança centralizada (Unity Catalog)
- Data Quality nativo (DLT Expectations)
- Escalabilidade para crescimento futuro
- ML-ready para análises avançadas
- Melhor observabilidade e lineage

---

## 5. Data Flow (Detalhado)

### 5.1 Pipeline de Ingestão End-to-End

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              END-TO-END DATA FLOW ARCHITECTURE                                       │
│                                   Daily Batch Processing                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

 STAGE 1: LANDING              STAGE 2: BRONZE              STAGE 3: SILVER              STAGE 4: GOLD
 ──────────────────            ───────────────              ────────────────             ─────────────

 ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
 │   SOURCE FILES  │          │   AUTO LOADER   │          │  DLT PIPELINE   │          │   SQL NOTEBOOK  │
 │   (Landing Zone)│          │   (Streaming)   │          │  (Expectations) │          │   (Transforms)  │
 ├─────────────────┤          ├─────────────────┤          ├─────────────────┤          ├─────────────────┤
 │                 │          │                 │          │                 │          │                 │
 │  CSV Files      │─────────▶│  Read Stream    │─────────▶│  Apply DQ       │─────────▶│  Build Facts    │
 │  *.csv          │  Detect  │  + Schema       │  Write   │  38 Rules       │  MERGE   │  + Dimensions   │
 │  ~500K rows/mo  │  New     │  Inference      │  Delta   │  Quarantine     │  Enrich  │  Star Schema    │
 │                 │  Files   │                 │          │                 │          │                 │
 │  JSON Files     │          │  Add Metadata   │          │  Type Cast      │          │  Aggregations   │
 │  payment, rate  │          │  _source_file   │          │  Cleanse        │          │  Pre-compute    │
 │                 │          │  _ingestion_ts  │          │  Deduplicate    │          │  KPIs           │
 │  TSV Files      │          │  _batch_id      │          │                 │          │                 │
 │  trip_type      │          │                 │          │  Derive Fields  │          │  Views for BI   │
 │                 │          │                 │          │  duration, speed│          │                 │
 └─────────────────┘          └─────────────────┘          └─────────────────┘          └─────────────────┘
         │                            │                            │                            │
         │                            │                            │                            │
         ▼                            ▼                            ▼                            ▼
 ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
 │  ADLS Container │          │  ADLS Container │          │  ADLS Container │          │  ADLS Container │
 │  landing/       │          │  bronze/        │          │  silver/        │          │  gold/          │
 │                 │          │                 │          │                 │          │                 │
 │  /raw/tripdata/ │          │  /lnd_green_    │          │  /slv_trips/    │          │  /fact_trips/   │
 │     YYYY-MM.csv │          │   tripdata/     │          │    pickup_date= │          │    date_sk=     │
 │  /raw/payment/  │          │     year=YYYY/  │          │     2021-04-01/ │          │     202104/     │
 │  /raw/rate/     │          │     month=MM/   │          │     ...         │          │  /dim_date/     │
 │  /raw/trip_type/│          │  /lnd_payment/  │          │  /slv_payment/  │          │  /dim_payment/  │
 │                 │          │  /lnd_rate/     │          │  /slv_rate/     │          │  /dim_rate/     │
 │                 │          │  /lnd_trip_type/│          │  /slv_trip_type/│          │  /dim_trip_type/│
 │                 │          │                 │          │                 │          │  /agg_daily/    │
 └─────────────────┘          └─────────────────┘          └─────────────────┘          └─────────────────┘
                                                                   │
                                                                   │ DQ FAIL
                                                                   ▼
                                                           ┌─────────────────┐
                                                           │   QUARANTINE    │
                                                           │    (audit/)     │
                                                           ├─────────────────┤
                                                           │  quarantine_    │
                                                           │   records/      │
                                                           │                 │
                                                           │  • rule_id      │
                                                           │  • record_json  │
                                                           │  • timestamp    │
                                                           └─────────────────┘

 ─────────────────────────────────────────────────────────────────────────────────────────────────────────
 TIMING:    02:00-02:15           02:15-02:30            02:30-03:00              03:00-03:30
 DURATION:     ~15 min               ~15 min                ~30 min                  ~30 min
 ─────────────────────────────────────────────────────────────────────────────────────────────────────────
```

### 5.2 Schedule de Execução Detalhado

| Job | Trigger | Start | SLA | Dependencies | Cluster | Retry |
|-----|---------|-------|-----|--------------|---------|-------|
| **01-Ingest-Landing** | File arrival | 02:00 | 02:15 | Source files | Auto Loader | 2x, 5min |
| **02-Load-Bronze** | After 01 | 02:15 | 02:30 | 01 complete | etl-bronze | 2x, 5min |
| **03-DQ-Validate** | After 02 | 02:30 | 02:45 | 02 complete | etl-silver | 1x |
| **04-Transform-Silver** | After 03 | 02:45 | 03:15 | 03 pass >95% | DLT Pipeline | 2x |
| **05-Build-Gold** | After 04 | 03:15 | 03:45 | 04 complete | etl-gold | 2x |
| **06-Optimize-Tables** | After 05 | 03:45 | 04:00 | 05 complete | maintenance | 1x |
| **07-Refresh-BI** | Daily 06:00 | 06:00 | 06:30 | 05 complete | n/a (Power BI) | 3x |

### 5.3 Data Quality Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DATA QUALITY GATE (Between Bronze → Silver)                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                 ┌─────────────────────────────────┐
                                 │        BRONZE TABLE             │
                                 │     lnd_green_tripdata          │
                                 │        ~500K rows               │
                                 └───────────────┬─────────────────┘
                                                 │
                                                 ▼
                        ┌────────────────────────────────────────────────┐
                        │              DLT EXPECTATIONS                   │
                        │         38 Rules Applied in Parallel            │
                        ├────────────────────────────────────────────────┤
                        │                                                │
                        │  CRITICAL (expect_or_drop):                    │
                        │  • DQ-001: pickup_datetime NOT NULL            │
                        │  • DQ-005: dropoff_datetime NOT NULL           │
                        │  • DQ-009: total_amount NOT NULL               │
                        │  • DQ-010: total_amount >= 0                   │
                        │                                                │
                        │  HIGH (expect_or_quarantine):                  │
                        │  • DQ-003: date in valid range                 │
                        │  • DQ-007: dropoff > pickup                    │
                        │  • DQ-019: trip_distance >= 0                  │
                        │  • DQ-021: trip_distance < 100                 │
                        │                                                │
                        │  MEDIUM (expect with warn):                    │
                        │  • DQ-012: total = sum of components           │
                        │  • DQ-025: speed < 100 mph                     │
                        │  • DQ-033: passenger_count 0-9                 │
                        │                                                │
                        └────────────────────┬───────────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
          ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
          │     DROP        │      │   QUARANTINE    │      │    SILVER       │
          │  (Critical)     │      │   (Review)      │      │   (Valid)       │
          ├─────────────────┤      ├─────────────────┤      ├─────────────────┤
          │ Records with    │      │ Records with    │      │ Clean records   │
          │ NULL required   │      │ HIGH violations │      │ passed all      │
          │ fields or       │      │ for manual      │      │ critical +      │
          │ impossible data │      │ review          │      │ high checks     │
          │                 │      │                 │      │                 │
          │ ~0.2% (~1K)     │      │ ~1.5% (~7.5K)   │      │ ~98.3% (~491K)  │
          │                 │      │                 │      │                 │
          │ → Logged only   │      │ → quarantine/   │      │ → slv_trips     │
          └─────────────────┘      └─────────────────┘      └─────────────────┘

          GATE THRESHOLD: Pipeline continues if SILVER >= 95%
          ALERT: If quarantine > 5%, notify data team
```

### 5.4 Lineage Tracking (Unity Catalog)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DATA LINEAGE (Auto-captured by Unity Catalog)                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  SOURCE FILES                    BRONZE                      SILVER                       GOLD
  ────────────                    ──────                      ──────                       ────

  green_tripdata_               lnd_green_                  slv_trips                   fact_trips
  2021-04.csv     ─────────────▶  tripdata    ─────────────▶            ─────────────▶
  green_tripdata_                                                                       dim_date
  2021-05.csv                                                                           dim_payment ◀── slv_payment ◀── lnd_payment
  green_tripdata_                                                                       dim_rate    ◀── slv_rate    ◀── lnd_rate
  2021-06.csv                                                                           dim_trip    ◀── slv_trip    ◀── lnd_trip


  LINEAGE QUERIES (Unity Catalog):
  ─────────────────────────────────
  
  -- Show upstream dependencies of fact_trips
  SHOW LINEAGE FOR TABLE gold.fact_trips UPSTREAM;
  
  -- Show downstream consumers of slv_trips  
  SHOW LINEAGE FOR TABLE silver.slv_trips DOWNSTREAM;
  
  -- Track column-level lineage
  SELECT * FROM system.access.column_lineage 
  WHERE target_table = 'gold.fact_trips';
```

---

## 6. Security Architecture (Detalhado)

### 6.1 Camadas de Segurança

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  SECURITY ARCHITECTURE - DEFENSE IN DEPTH                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: NETWORK SECURITY                                                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │                              AZURE VIRTUAL NETWORK                                       │       │
│  │                                 (vnet-nyctaxi-prod)                                      │       │
│  │                                   10.0.0.0/16                                            │       │
│  │  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐  │       │
│  │  │   Subnet: databricks    │  │   Subnet: storage       │  │   Subnet: management    │  │       │
│  │  │   10.0.1.0/24           │  │   10.0.2.0/24           │  │   10.0.3.0/24           │  │       │
│  │  │   • Databricks clusters │  │   • Private Endpoints   │  │   • Bastion host        │  │       │
│  │  │   • Delegated to DBX    │  │   • ADLS Gen2           │  │   • Jump box            │  │       │
│  │  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘  │       │
│  │                                                                                         │       │
│  │  NSG Rules:                                                                             │       │
│  │  • Inbound: Deny all except Azure Databricks control plane                              │       │
│  │  • Outbound: Allow Databricks required services, storage                                │       │
│  │  • No public IPs on data plane                                                          │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
│  Private Endpoints:                                                                                 │
│  • pe-storage-blob    → stnyctaxi.blob.core.windows.net                                            │
│  • pe-storage-dfs     → stnyctaxi.dfs.core.windows.net                                             │
│  • pe-keyvault        → kv-nyctaxi.vault.azure.net                                                 │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: IDENTITY & ACCESS MANAGEMENT                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │                              AZURE ACTIVE DIRECTORY                                      │       │
│  ├─────────────────────────────────────────────────────────────────────────────────────────┤       │
│  │                                                                                         │       │
│  │  SERVICE PRINCIPALS:                           MANAGED IDENTITIES:                      │       │
│  │  ┌─────────────────────────────────┐          ┌─────────────────────────────────┐      │       │
│  │  │ sp-databricks-etl               │          │ mi-databricks-workspace         │      │       │
│  │  │ • Used by: Databricks jobs      │          │ • Used by: Databricks compute   │      │       │
│  │  │ • Permissions: Storage RW       │          │ • Permissions: Storage access   │      │       │
│  │  │ • Secret: Stored in Key Vault   │          │ • Auto-rotated                  │      │       │
│  │  └─────────────────────────────────┘          └─────────────────────────────────┘      │       │
│  │                                                                                         │       │
│  │  USERS & GROUPS (synced from AAD):                                                      │       │
│  │  • grp-nyctaxi-data-engineers     (3 members)                                          │       │
│  │  • grp-nyctaxi-data-analysts      (5 members)                                          │       │
│  │  • grp-nyctaxi-bi-developers      (2 members)                                          │       │
│  │  • grp-nyctaxi-admins             (2 members)                                          │       │
│  │                                                                                         │       │
│  │  CONDITIONAL ACCESS:                                                                    │       │
│  │  • MFA required for all users                                                          │       │
│  │  • Location-based: Only allowed regions                                                │       │
│  │  • Device compliance: Managed devices only                                             │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: DATA SECURITY (Unity Catalog)                                                              │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │                              UNITY CATALOG PERMISSIONS                                   │       │
│  ├─────────────────────────────────────────────────────────────────────────────────────────┤       │
│  │                                                                                         │       │
│  │  CATALOG LEVEL:                                                                         │       │
│  │  • grp-nyctaxi-admins: ALL PRIVILEGES                                                  │       │
│  │  • grp-nyctaxi-data-engineers: USE CATALOG                                             │       │
│  │  • grp-nyctaxi-data-analysts: USE CATALOG                                              │       │
│  │                                                                                         │       │
│  │  SCHEMA LEVEL:                                                                          │       │
│  │  ┌─────────────────┬─────────────────────────────────────────────────────────────────┐ │       │
│  │  │ Schema          │ data_engineers    │ data_analysts     │ bi_developers         │ │       │
│  │  ├─────────────────┼───────────────────┼───────────────────┼───────────────────────┤ │       │
│  │  │ bronze          │ ALL PRIVILEGES    │ (none)            │ (none)                │ │       │
│  │  │ silver          │ ALL PRIVILEGES    │ SELECT            │ (none)                │ │       │
│  │  │ gold            │ ALL PRIVILEGES    │ SELECT            │ SELECT (views)        │ │       │
│  │  │ audit           │ ALL PRIVILEGES    │ SELECT            │ (none)                │ │       │
│  │  └─────────────────┴───────────────────┴───────────────────┴───────────────────────┘ │       │
│  │                                                                                         │       │
│  │  ROW-LEVEL SECURITY (Future):                                                          │       │
│  │  -- Example: Restrict by borough                                                       │       │
│  │  CREATE FUNCTION gold.my_filter()                                                      │       │
│  │  RETURNS BOOLEAN                                                                       │       │
│  │  RETURN IS_ACCOUNT_GROUP_MEMBER('grp-manhattan-only')                                 │       │
│  │         AND borough = 'Manhattan';                                                     │       │
│  │                                                                                         │       │
│  │  COLUMN MASKING (Future):                                                              │       │
│  │  -- Example: Mask location details for non-analysts                                    │       │
│  │  ALTER TABLE gold.fact_trips ALTER COLUMN pu_location_id                              │       │
│  │    SET MASK mask_location USING COLUMNS (pu_location_id);                             │       │
│  │                                                                                         │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: ENCRYPTION                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  AT REST:                                         IN TRANSIT:                                       │
│  ┌─────────────────────────────────┐             ┌─────────────────────────────────┐               │
│  │ • ADLS Gen2: Microsoft-managed  │             │ • TLS 1.2+ enforced             │               │
│  │   keys (SSE with AES-256)       │             │ • Databricks workspace: HTTPS   │               │
│  │ • Option: Customer-managed keys │             │ • Private endpoints: encrypted  │               │
│  │   via Azure Key Vault           │             │ • Power BI: encrypted queries   │               │
│  │ • Delta Lake: inherits storage  │             │                                 │               │
│  │   encryption                    │             │                                 │               │
│  └─────────────────────────────────┘             └─────────────────────────────────┘               │
│                                                                                                     │
│  SECRETS MANAGEMENT:                                                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐       │
│  │ Azure Key Vault (kv-nyctaxi)                                                            │       │
│  │ • sp-databricks-etl-secret     → Service principal credentials                         │       │
│  │ • storage-account-key          → ADLS access key (backup)                              │       │
│  │ • powerbi-sp-secret            → Power BI service principal                            │       │
│  │                                                                                         │       │
│  │ Databricks Secret Scope (backed by Key Vault):                                         │       │
│  │ • Scope: nyctaxi-secrets                                                               │       │
│  │ • Access: dbutils.secrets.get("nyctaxi-secrets", "key-name")                          │       │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘       │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 RBAC Matrix Detalhado

| Role | Azure RBAC | Databricks Workspace | Unity Catalog | Storage | Power BI |
|------|------------|---------------------|---------------|---------|----------|
| **Platform Admin** | Owner | Admin | Metastore Admin | Owner | Admin |
| **Data Engineer** | Contributor | User + Cluster Create | bronze/silver/gold: ALL | RW | Viewer |
| **Data Analyst** | Reader | User | silver/gold: SELECT | R (silver, gold) | Viewer |
| **BI Developer** | Reader | SQL User | gold: SELECT (views) | R (gold) | Contributor |
| **Data Scientist** | Reader | User + ML Runtime | silver/gold: SELECT | R (silver, gold) | Viewer |
| **Business User** | - | - | - | - | Viewer |

### 6.3 Data Classification

| Classification | Examples | Storage | Access | Encryption | Retention |
|----------------|----------|---------|--------|------------|-----------|
| **Public** | Rate codes, trip types | Gold | All authenticated | Standard | Indefinite |
| **Internal** | Aggregated metrics, KPIs | Gold | Analysts + BI | Standard | 7 years |
| **Confidential** | Individual trip records | Silver | Engineers + Analysts | Standard | 3 years |
| **PII** | Location details (granular) | Silver (masked) | Engineers only | Enhanced | 1 year |

---

## 7. Scalability & Performance

### 7.1 Current vs Future Sizing

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    SCALABILITY PROJECTIONS                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                         CURRENT (Q2 2021)           1 YEAR              3 YEARS             5 YEARS
                         ─────────────────           ──────              ───────             ───────

  TRIP DATA VOLUME:
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                  │
  │    500K/month ────▶ 600K/month ────▶ 750K/month ────▶ 1M/month                                  │
  │    1.5M/quarter     7.2M/year       9M/year         12M/year                                    │
  │                                                                                                  │
  │    Storage Growth:                                                                               │
  │    1 GB ──────────▶ 12 GB ─────────▶ 35 GB ─────────▶ 60 GB                                     │
  │                                                                                                  │
  └──────────────────────────────────────────────────────────────────────────────────────────────────┘

  COMPUTE SCALING:
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                  │
  │  ETL Cluster:       2-4 nodes ────▶ 2-8 nodes ────▶ 4-12 nodes ────▶ 8-16 nodes                │
  │  SQL Warehouse:     2X-Small ────▶ X-Small ───────▶ Small ─────────▶ Medium                     │
  │  Job Duration:      30 min ───────▶ 45 min ───────▶ 60 min ────────▶ 90 min                    │
  │                                                                                                  │
  └──────────────────────────────────────────────────────────────────────────────────────────────────┘

  COST PROJECTION:
  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                  │
  │  Monthly Cost:      $120 ─────────▶ $180 ─────────▶ $300 ──────────▶ $500                       │
  │                                                                                                  │
  │  Breakdown:                                                                                      │
  │  • Databricks:      $70 ──────────▶ $120 ─────────▶ $200 ──────────▶ $350                       │
  │  • Storage:         $1 ───────────▶ $5 ───────────▶ $15 ───────────▶ $25                        │
  │  • Power BI:        $50 ──────────▶ $50 ──────────▶ $75 ───────────▶ $100                       │
  │  • Networking:      $0 ───────────▶ $5 ───────────▶ $10 ───────────▶ $25                        │
  │                                                                                                  │
  └──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Performance Optimizations

| Optimization | Layer | Implementation | Benefit |
|--------------|-------|----------------|---------|
| **Partitioning** | All | `year/month` (bronze), `pickup_date` (silver), `date_sk` (gold) | Partition pruning, faster queries |
| **Z-Ordering** | Silver, Gold | `OPTIMIZE table ZORDER BY (pickup_datetime, pu_location_id)` | Co-locate related data |
| **Delta Caching** | Gold | `delta.autoOptimize.autoCompact` = true | Faster repeated queries |
| **Liquid Clustering** | Future | Replace Z-ordering with liquid clustering | Adaptive optimization |
| **Photon** | All | Enable Photon runtime on clusters | 2-8x faster queries |
| **Broadcast Joins** | Gold | Small dimension tables broadcasted | Faster joins |
| **File Compaction** | All | `OPTIMIZE` with target 256MB files | Fewer files, faster reads |
| **Statistics** | All | `ANALYZE TABLE` after major loads | Better query plans |

### 7.3 Partitioning Strategy Detail

```sql
-- Bronze: Partition by ingestion date (matches source organization)
CREATE TABLE bronze.lnd_green_tripdata (...)
PARTITIONED BY (year INT, month INT)
LOCATION 'abfss://bronze@stnyctaxi.dfs.core.windows.net/lnd_green_tripdata';

-- Silver: Partition by business date (query patterns)
CREATE TABLE silver.slv_trips (...)
PARTITIONED BY (pickup_date DATE)
LOCATION 'abfss://silver@stnyctaxi.dfs.core.windows.net/slv_trips';

-- Gold: Partition by surrogate date key (BI performance)
CREATE TABLE gold.fact_trips (...)
PARTITIONED BY (date_sk INT)
LOCATION 'abfss://gold@stnyctaxi.dfs.core.windows.net/fact_trips';

-- Optimize Gold table weekly
OPTIMIZE gold.fact_trips ZORDER BY (payment_type_sk, pickup_location_sk);
```

---

## 8. Monitoring & Observability

### 8.1 Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    OBSERVABILITY STACK                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  DATA PIPELINE                    METRICS                     ALERTING                    DASHBOARDS
  ─────────────                    ───────                     ────────                    ──────────

  ┌───────────────┐          ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
  │  Databricks   │─────────▶│   Databricks  │─────────▶│   Azure       │─────────▶│   Grafana /   │
  │  Jobs/DLT     │  Emit    │   System      │  Forward │   Monitor     │  Display │   Power BI    │
  │               │  Metrics │   Tables      │  Metrics │   Alerts      │  Metrics │   Dashboard   │
  └───────────────┘          └───────────────┘          └───────────────┘          └───────────────┘
         │                          │                          │                          │
         │                          │                          │                          │
         ▼                          ▼                          ▼                          ▼
  ┌───────────────┐          ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
  │  Custom       │          │  Log          │          │  Action       │          │  DQ           │
  │  Logging      │          │  Analytics    │          │  Groups       │          │  Dashboard    │
  │  (audit.*)    │          │  Workspace    │          │  (email,slack)│          │  (Power BI)   │
  └───────────────┘          └───────────────┘          └───────────────┘          └───────────────┘


  METRICS COLLECTED:
  ──────────────────
  
  Pipeline Metrics:
  • job_duration_seconds        • rows_processed_total       • rows_quarantined_total
  • job_status (success/fail)   • dq_pass_rate_pct          • etl_lag_hours
  
  Cluster Metrics:
  • cluster_utilization_pct     • memory_usage_bytes        • disk_io_bytes
  • cpu_utilization_pct         • node_count                • spot_interruptions
  
  Storage Metrics:
  • storage_size_bytes          • file_count                • delta_table_operations
  • partition_count             • small_file_count          • vacuum_operations
  
  SQL Warehouse Metrics:
  • query_count                 • query_duration_avg        • queue_time_avg
  • warehouse_utilization       • cache_hit_rate            • concurrent_queries
```

### 8.2 Alerting Rules

| Alert | Condition | Severity | Action | Recipients |
|-------|-----------|----------|--------|------------|
| **Pipeline Failed** | job_status = 'FAILED' | Critical | Page on-call | #data-alerts, PagerDuty |
| **DQ Below Threshold** | dq_pass_rate < 95% | High | Email + Slack | #data-alerts |
| **Pipeline Delayed** | start_time > SLA + 1hr | Medium | Slack | #data-alerts |
| **High Quarantine** | quarantine_rate > 5% | Medium | Email | Data Engineers |
| **Storage Growth** | daily_growth > 2GB | Low | Email (weekly) | Data Engineers |
| **Cluster Overload** | cpu_util > 90% for 30min | Medium | Auto-scale | Monitoring |
| **SQL Warehouse Slow** | avg_query_time > 30s | Low | Slack | BI Developers |

### 8.3 Audit Tables

```sql
-- audit.pipeline_runs: Track every ETL execution
CREATE TABLE audit.pipeline_runs (
    run_id              STRING,
    pipeline_name       STRING,
    start_timestamp     TIMESTAMP,
    end_timestamp       TIMESTAMP,
    status              STRING,        -- 'SUCCESS', 'FAILED', 'RUNNING'
    rows_read           BIGINT,
    rows_written        BIGINT,
    rows_quarantined    BIGINT,
    error_message       STRING,
    cluster_id          STRING,
    dbu_consumed        DOUBLE
);

-- audit.dq_results: Track every DQ rule execution
CREATE TABLE audit.dq_results (
    dq_result_id        BIGINT,
    batch_id            STRING,
    run_id              STRING,
    table_name          STRING,
    rule_id             STRING,
    rule_description    STRING,
    total_records       BIGINT,
    passed_records      BIGINT,
    failed_records      BIGINT,
    pass_rate           DECIMAL(5,2),
    execution_timestamp TIMESTAMP
);

-- audit.quarantine_records: Store rejected records for review
CREATE TABLE audit.quarantine_records (
    quarantine_id       BIGINT,
    source_table        STRING,
    source_file         STRING,
    rule_id             STRING,
    severity            STRING,
    field_name          STRING,
    field_value         STRING,
    record_json         STRING,
    quarantine_timestamp TIMESTAMP,
    reprocess_status    STRING,        -- 'PENDING', 'REPROCESSED', 'DISCARDED'
    reprocess_timestamp TIMESTAMP
);
```

---

## 9. Disaster Recovery

### 9.1 Backup Strategy

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DISASTER RECOVERY ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                              PRIMARY REGION                           SECONDARY REGION
                              (East US 2)                              (West US 2)
                              ──────────────                           ─────────────────

  ┌─────────────────────────────────────────┐        ┌─────────────────────────────────────────┐
  │           ADLS GEN2 (PRIMARY)           │        │           ADLS GEN2 (SECONDARY)         │
  │           stnyctaxi                     │        │           stnyctaxi-dr                  │
  ├─────────────────────────────────────────┤        ├─────────────────────────────────────────┤
  │                                         │  GRS   │                                         │
  │  • bronze/                              │───────▶│  • bronze/     (async replication)      │
  │  • silver/                              │ Async  │  • silver/                              │
  │  • gold/                                │ ~15min │  • gold/                                │
  │  • audit/                               │  RPO   │  • audit/                               │
  │                                         │        │                                         │
  └─────────────────────────────────────────┘        └─────────────────────────────────────────┘

  ┌─────────────────────────────────────────┐        ┌─────────────────────────────────────────┐
  │        DATABRICKS WORKSPACE             │        │        DATABRICKS WORKSPACE (DR)        │
  │        (dbw-nyctaxi-prod)               │        │        (dbw-nyctaxi-dr)                 │
  ├─────────────────────────────────────────┤        ├─────────────────────────────────────────┤
  │                                         │ Export │                                         │
  │  • Unity Catalog metadata               │───────▶│  • Unity Catalog (standby)              │
  │  • Notebooks (Git sync)                 │ Daily  │  • Notebooks (Git sync)                 │
  │  • Job definitions                      │        │  • Job definitions (disabled)           │
  │  • Cluster configs                      │        │  • Cluster configs                      │
  │                                         │        │                                         │
  └─────────────────────────────────────────┘        └─────────────────────────────────────────┘

  ┌─────────────────────────────────────────┐
  │             GIT REPOSITORY              │
  │           (Azure DevOps)                │
  ├─────────────────────────────────────────┤
  │                                         │
  │  • Notebooks/*                          │
  │  • pipelines/*                          │
  │  • config/*                             │
  │  • terraform/*                          │
  │                                         │
  │  Branching: main (prod) / dev / feature │
  │  Backup: Azure DevOps geo-redundant     │
  │                                         │
  └─────────────────────────────────────────┘


  RECOVERY PROCEDURES:
  ────────────────────
  
  Scenario 1: Data Corruption (point-in-time recovery)
  ─────────────────────────────────────────────────────
  • Use Delta Lake time travel: RESTORE TABLE gold.fact_trips TO VERSION AS OF 142;
  • Or by timestamp: RESTORE TABLE gold.fact_trips TO TIMESTAMP AS OF '2026-02-05 10:00:00';
  • RPO: Near-zero (30 days history)
  • RTO: ~30 minutes
  
  Scenario 2: Regional Outage (failover to DR)
  ────────────────────────────────────────────
  • Activate DR workspace (enable jobs)
  • Switch storage to DR account
  • Update Power BI connections
  • RPO: ~15 minutes (GRS lag)
  • RTO: ~4 hours
  
  Scenario 3: Accidental Deletion
  ────────────────────────────────
  • Unity Catalog: UNDROP TABLE (30 days)
  • Delta Lake: Time travel restore
  • Full workspace: Terraform re-deploy from Git
```

### 9.2 Recovery Objectives

| Scenario | RPO (Max Data Loss) | RTO (Recovery Time) | Method |
|----------|---------------------|---------------------|--------|
| Data corruption | Near-zero | 30 minutes | Delta time travel |
| Table drop | 30 days | 1 hour | UNDROP / time travel |
| Regional outage | 15 minutes | 4 hours | GRS failover |
| Workspace failure | 1 day | 8 hours | Git + Terraform redeploy |
| Complete disaster | 24 hours | 24 hours | Full rebuild from backup |

---

## 10. Cost Estimates (Databricks)

### 10.1 Monthly Costs Breakdown

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    MONTHLY COST ESTIMATE                                             │
│                                  Azure Databricks + Dependencies                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  SERVICE                           USAGE                    UNIT COST           MONTHLY COST
  ───────                           ─────                    ─────────           ────────────

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ DATABRICKS COMPUTE                                                                              │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                 │
  │  Job Clusters (ETL):                                                                            │
  │  • Bronze cluster         30 runs × 15 min = 7.5 hrs      $0.40/DBU ×4       $12.00            │
  │  • Silver DLT pipeline    30 runs × 20 min = 10 hrs       $0.40/DBU ×8       $32.00            │
  │  • Gold cluster           30 runs × 15 min = 7.5 hrs      $0.40/DBU ×4       $12.00            │
  │                                                                                                 │
  │  SQL Warehouse:                                                                                 │
  │  • 2X-Small serverless    ~100 hrs runtime                $0.55/DBU ×8       $44.00            │
  │    (auto-stop 10 min)                                                                          │
  │                                                                                                 │
  │  Interactive Clusters:                                                                          │
  │  • Dev/testing            ~20 hrs/month                   $0.40/DBU ×4       $8.00             │
  │                                                                                                 │
  │  DATABRICKS SUBTOTAL:                                                        $108.00           │
  │                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ AZURE INFRASTRUCTURE                                                                            │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                 │
  │  Storage (ADLS Gen2):                                                                           │
  │  • Hot tier              ~50 GB                           $0.02/GB           $1.00             │
  │  • Transactions          ~10M operations                  $0.05/10K          $0.50             │
  │                                                                                                 │
  │  Networking:                                                                                    │
  │  • VNet/Subnets          Included                         -                  $0.00             │
  │  • Private Endpoints     3 endpoints                      $7.30/endpoint     $21.90            │
  │  • Data transfer         ~100 GB                          $0.05/GB           $5.00             │
  │                                                                                                 │
  │  Key Vault:                                                                                     │
  │  • Standard tier         ~1000 operations                 $0.03/10K          $0.10             │
  │                                                                                                 │
  │  Azure Monitor:                                                                                 │
  │  • Log Analytics         ~10 GB ingestion                 $2.76/GB           $27.60            │
  │  • Alerts                5 rules                          $0.10/rule         $0.50             │
  │                                                                                                 │
  │  AZURE INFRA SUBTOTAL:                                                       $56.60            │
  │                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ BUSINESS INTELLIGENCE                                                                           │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                 │
  │  Power BI:                                                                                      │
  │  • Pro licenses          5 users                          $10.00/user        $50.00            │
  │  • Premium (optional)    Not required for MVP             -                  $0.00             │
  │                                                                                                 │
  │  POWER BI SUBTOTAL:                                                          $50.00            │
  │                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                                 │
  │  ═══════════════════════════════════════════════════════════════════════════════════════════   │
  │                                                                                                 │
  │                              TOTAL MONTHLY COST:  $214.60                                       │
  │                                                                                                 │
  │  ═══════════════════════════════════════════════════════════════════════════════════════════   │
  │                                                                                                 │
  │  Cost Optimization Options:                                                                     │
  │  • Spot instances for job clusters:      -$25         (save ~$25/month on ETL)                 │
  │  • Reserved capacity (1 year):           -$20         (save ~15% on Databricks)                │
  │  • Reduce Log Analytics retention:       -$10         (7 days vs 30 days)                      │
  │                                                                                                 │
  │  OPTIMIZED MONTHLY COST:  ~$160                                                                │
  │                                                                                                 │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 10.2 Cost Comparison

| Aspect | Synapse Serverless | Databricks (This Choice) | Difference |
|--------|-------------------|--------------------------|------------|
| Compute | $0.50 | $108.00 | +$107.50 |
| Storage | $1.00 | $1.50 | +$0.50 |
| Networking | $0.00 | $26.90 | +$26.90 |
| Monitoring | $0.00 | $28.10 | +$28.10 |
| Power BI | $50.00 | $50.00 | $0.00 |
| **TOTAL** | **~$52/mo** | **~$215/mo** | **+$163/mo** |

**Justification for +$163/mo:**
- Unity Catalog for centralized governance (otherwise need Purview: ~$200/mo)
- Built-in DQ with DLT Expectations (otherwise need Great Expectations: setup cost)
- ML-ready platform for future (otherwise need separate ML infrastructure)
- Better scalability (Synapse has limitations at scale)
- Faster ETL with Spark/Photon (time savings = cost savings)

---

## 11. Implementation Roadmap

### 11.1 Detailed Phases

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    IMPLEMENTATION ROADMAP                                            │
│                                   12 Weeks to Production                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  WEEK      1    2    3    4    5    6    7    8    9   10   11   12
           ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 1  │████████████│    │    │    │    │    │    │    │    │    │  FOUNDATION
  (1-2)    │    │    │    │    │    │    │    │    │    │    │    │    │
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 2  │    │    │████████████│    │    │    │    │    │    │    │  BRONZE
  (3-4)    │    │    │    │    │    │    │    │    │    │    │    │    │
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 3  │    │    │    │    │████████████│    │    │    │    │    │  SILVER + DQ
  (5-6)    │    │    │    │    │    │    │    │    │    │    │    │    │
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 4  │    │    │    │    │    │    │████████████│    │    │    │  GOLD
  (7-8)    │    │    │    │    │    │    │    │    │    │    │    │    │
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 5  │    │    │    │    │    │    │    │    │████████████│    │  SERVING
  (9-10)   │    │    │    │    │    │    │    │    │    │    │    │    │
           │    │    │    │    │    │    │    │    │    │    │    │    │
  Phase 6  │    │    │    │    │    │    │    │    │    │    │████████│  GO-LIVE
  (11-12)  │    │    │    │    │    │    │    │    │    │    │    │    │
           └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
                 │         │         │         │         │         │
                 ▼         ▼         ▼         ▼         ▼         ▼
              Gate 0    Gate 1    Gate 2    Gate 3    Gate 4    PROD


  DETAILED PHASE BREAKDOWN:
  ─────────────────────────

  PHASE 1: FOUNDATION (Weeks 1-2)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 1:                                                                              │
  │ • Provision Azure resources (Terraform)                                              │
  │ • Create ADLS Gen2 storage account with containers                                   │
  │ • Set up VNet, subnets, NSGs                                                        │
  │ • Create Key Vault and secrets                                                       │
  │                                                                                      │
  │ Week 2:                                                                              │
  │ • Create Databricks workspace (Premium)                                              │
  │ • Configure Unity Catalog and metastore                                              │
  │ • Set up external locations and storage credentials                                  │
  │ • Configure AAD groups and RBAC                                                      │
  │ • Create secret scopes                                                               │
  │                                                                                      │
  │ Deliverables: Infrastructure ready, Unity Catalog configured                         │
  │ Gate 0: Infrastructure review                                                        │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  PHASE 2: BRONZE LAYER (Weeks 3-4)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 3:                                                                              │
  │ • Create Bronze schema in Unity Catalog                                              │
  │ • Develop Auto Loader notebooks for CSV/JSON/TSV                                     │
  │ • Configure checkpoints and schema evolution                                         │
  │ • Create lnd_green_tripdata, lnd_payment_type, lnd_rate_code, lnd_trip_type         │
  │                                                                                      │
  │ Week 4:                                                                              │
  │ • Test ingestion with sample data                                                    │
  │ • Create scheduled job (Databricks Workflow)                                         │
  │ • Implement error handling and logging                                               │
  │ • Load historical data (Q2 2021)                                                     │
  │                                                                                      │
  │ Deliverables: Bronze layer operational, historical data loaded                       │
  │ Gate 1: Bronze layer review, data validation                                         │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  PHASE 3: SILVER LAYER + DQ (Weeks 5-6)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 5:                                                                              │
  │ • Create Silver schema in Unity Catalog                                              │
  │ • Develop DLT pipeline for Bronze → Silver                                           │
  │ • Implement 38 DQ rules as DLT expectations                                          │
  │ • Create slv_trips, slv_payment_type, slv_rate_code, slv_trip_type                  │
  │                                                                                      │
  │ Week 6:                                                                              │
  │ • Set up quarantine table and handling                                               │
  │ • Test DQ rules and thresholds                                                       │
  │ • Create DQ monitoring/alerting                                                      │
  │ • Process historical data through Silver                                             │
  │                                                                                      │
  │ Deliverables: Silver layer operational, DQ rules active                              │
  │ Gate 2: Silver layer review, DQ validation (>95% pass rate)                          │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  PHASE 4: GOLD LAYER (Weeks 7-8)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 7:                                                                              │
  │ • Create Gold schema in Unity Catalog                                                │
  │ • Generate dim_date dimension (full calendar)                                        │
  │ • Create dimension tables (dim_payment, dim_rate, dim_trip_type)                    │
  │ • Develop fact_trips transformation                                                  │
  │                                                                                      │
  │ Week 8:                                                                              │
  │ • Create aggregation tables (agg_daily_summary, etc.)                               │
  │ • Implement surrogate key generation                                                 │
  │ • Optimize Gold tables (Z-ordering, compaction)                                      │
  │ • Process historical data through Gold                                               │
  │                                                                                      │
  │ Deliverables: Gold layer operational, star schema complete                           │
  │ Gate 3: Gold layer review, model validation                                          │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  PHASE 5: SERVING LAYER (Weeks 9-10)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 9:                                                                              │
  │ • Create SQL Warehouse                                                               │
  │ • Create BI views (vw_trip_summary, vw_kpi_dashboard, etc.)                         │
  │ • Configure Power BI connection (DirectQuery)                                        │
  │ • Build initial Power BI dataset and reports                                         │
  │                                                                                      │
  │ Week 10:                                                                             │
  │ • Build executive dashboard (KPIs, trends)                                           │
  │ • Build operational dashboard (zones, heatmaps)                                      │
  │ • Configure scheduled refresh                                                        │
  │ • User acceptance testing (UAT)                                                      │
  │                                                                                      │
  │ Deliverables: Power BI dashboards, SQL views                                         │
  │ Gate 4: UAT sign-off, performance testing                                            │
  └──────────────────────────────────────────────────────────────────────────────────────┘

  PHASE 6: GO-LIVE (Weeks 11-12)
  ┌──────────────────────────────────────────────────────────────────────────────────────┐
  │ Week 11:                                                                             │
  │ • End-to-end testing (full pipeline)                                                 │
  │ • Performance tuning                                                                 │
  │ • Security review and penetration testing                                            │
  │ • Documentation completion                                                           │
  │                                                                                      │
  │ Week 12:                                                                             │
  │ • Production deployment                                                              │
  │ • Cutover from test to production                                                    │
  │ • Monitoring and alerting activation                                                 │
  │ • Knowledge transfer and training                                                    │
  │ • Hypercare period begins                                                            │
  │                                                                                      │
  │ Deliverables: Production system live, documentation, training                        │
  │ Gate PROD: Production sign-off                                                       │
  └──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Próximos Artefatos

Este documento alimenta:

| Artefato | Agente | Propósito |
|----------|--------|-----------|
| [data-model.md](data-model.md) | 🧩 Sofia | Modelo dimensional detalhado |
| [decisions.md](decisions.md) | 🏗️ Winston | ADRs formais |
| `dq-rules.md` | 🛡️ Gaia | Regras de DQ expandidas |
| `ddl/*.sql` | 🛠️ Diego | Scripts de criação |
| `notebooks/*.py` | 🛠️ Diego | Databricks notebooks |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Winston (DataArchitect) | Versão inicial |
| 2.0 | 2026-02-05 | Winston (DataArchitect) | Expansão completa, mudança para Databricks |

---

*Documento gerado pelo 🏗️ DataArchitect Agent - Avanade™ Core*
