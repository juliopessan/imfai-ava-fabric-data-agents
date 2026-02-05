# 🧩 Data Model Document

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🧩 Sofia (DataModeler) & 🏗️ Winston (DataArchitect)  
> **Referências:** [architecture.md](architecture.md) | [sttm.md](../requirements/sttm.md)

---

## 1. Sumário Executivo

Este documento define o modelo de dados completo para o projeto NYC Green Taxi Analytics, incluindo todas as entidades das camadas Bronze, Silver e Gold, seguindo o padrão **Medallion Architecture** com modelo dimensional **Star Schema (Kimball)**.

### 1.1 Resumo do Modelo

| Camada | Entidades | Propósito |
|--------|-----------|-----------|
| **Bronze** | 4 tabelas | Raw data, schema-on-read |
| **Silver** | 4 tabelas | Cleansed, typed, validated |
| **Gold** | 6 tabelas | Star schema dimensional |
| **Audit** | 2 tabelas | DQ, lineage tracking |

---

## 2. Convenções de Nomenclatura

### 2.1 Naming Standards

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| **Schema Bronze** | `bronze` | `bronze.lnd_green_tripdata` |
| **Schema Silver** | `silver` | `silver.slv_trips` |
| **Schema Gold** | `gold` | `gold.fact_trips` |
| **Schema Audit** | `audit` | `audit.dq_results` |
| **Landing Table** | `lnd_{source}_{entity}` | `lnd_green_tripdata` |
| **Silver Table** | `slv_{entity}` | `slv_trips` |
| **Fact Table** | `fact_{subject}` | `fact_trips` |
| **Dimension** | `dim_{entity}` | `dim_payment` |
| **Surrogate Key** | `{entity}_sk` | `trip_sk` |
| **Natural Key** | `{entity}_id` | `payment_type_id` |
| **Foreign Key** | `{related_entity}_sk` | `payment_type_sk` |
| **Date** | `*_date` ou `*_datetime` | `pickup_datetime` |
| **Flag** | `is_*` ou `has_*` | `is_weekend` |
| **Amount** | `*_amount` | `fare_amount` |
| **Count** | `*_count` | `passenger_count` |

### 2.2 Data Types Standards

| Tipo Lógico | SQL Server | Delta Lake | Uso |
|-------------|------------|------------|-----|
| Identificador | BIGINT | LONG | PKs, FKs |
| Código | INT | INT | Códigos de referência |
| Texto Curto | VARCHAR(50) | STRING | Descrições curtas |
| Texto Longo | VARCHAR(255) | STRING | Descrições longas |
| Monetário | DECIMAL(10,2) | DECIMAL(10,2) | Valores financeiros |
| Distância | DECIMAL(10,2) | DECIMAL(10,2) | Milhas, km |
| Percentual | DECIMAL(5,2) | DECIMAL(5,2) | Taxas, % |
| Data/Hora | DATETIME2 | TIMESTAMP | Timestamps |
| Data | DATE | DATE | Datas sem hora |
| Flag | BIT | BOOLEAN | True/False |
| JSON | NVARCHAR(MAX) | STRING | Dados semi-estruturados |

---

## 3. Bronze Layer (Landing)

### 3.1 Diagrama ER - Bronze

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            BRONZE LAYER (Landing)                            │
│                        Schema-on-Read, Append-Only                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐    ┌─────────────────────────────┐
│   lnd_green_tripdata        │    │   lnd_payment_type          │
├─────────────────────────────┤    ├─────────────────────────────┤
│ vendor_id          INT      │    │ payment_type_id    INT  PK  │
│ pickup_datetime    VARCHAR  │    │ payment_type_desc  NVARCHAR │
│ dropoff_datetime   VARCHAR  │    │ load_timestamp     DATETIME │
│ store_and_fwd_flag VARCHAR  │    └─────────────────────────────┘
│ ratecode_id        INT      │
│ pu_location_id     INT      │    ┌─────────────────────────────┐
│ do_location_id     INT      │    │   lnd_rate_code             │
│ passenger_count    INT      │    ├─────────────────────────────┤
│ trip_distance      DECIMAL  │    │ rate_code_id       INT  PK  │
│ fare_amount        DECIMAL  │    │ rate_code_desc     VARCHAR  │
│ extra              DECIMAL  │    │ load_timestamp     DATETIME │
│ mta_tax            DECIMAL  │    └─────────────────────────────┘
│ tip_amount         DECIMAL  │
│ tolls_amount       DECIMAL  │    ┌─────────────────────────────┐
│ ehail_fee          DECIMAL  │    │   lnd_trip_type             │
│ improvement_surcharge DECIMAL│   ├─────────────────────────────┤
│ total_amount       DECIMAL  │    │ trip_type_id       INT  PK  │
│ payment_type       INT      │    │ trip_type_desc     VARCHAR  │
│ trip_type          INT      │    │ load_timestamp     DATETIME │
│ congestion_surcharge DECIMAL│    └─────────────────────────────┘
│ source_file        VARCHAR  │
│ load_timestamp     DATETIME │
└─────────────────────────────┘
```

### 3.2 bronze.lnd_green_tripdata

**Descrição:** Dados brutos de corridas de táxi verde, exatamente como recebidos do arquivo CSV.

| # | Coluna | Tipo | Nullable | Default | Descrição |
|---|--------|------|----------|---------|-----------|
| 1 | vendor_id | INT | YES | NULL | Código do provedor LPEP (1=Creative Mobile, 2=VeriFone) |
| 2 | pickup_datetime | VARCHAR(50) | YES | NULL | Data/hora início corrida (string raw) |
| 3 | dropoff_datetime | VARCHAR(50) | YES | NULL | Data/hora fim corrida (string raw) |
| 4 | store_and_fwd_flag | VARCHAR(1) | YES | NULL | Flag store-and-forward (Y/N) |
| 5 | ratecode_id | INT | YES | NULL | Código da tarifa aplicada |
| 6 | pu_location_id | INT | YES | NULL | Código da zona de pickup (TLC zone) |
| 7 | do_location_id | INT | YES | NULL | Código da zona de dropoff (TLC zone) |
| 8 | passenger_count | INT | YES | NULL | Número de passageiros |
| 9 | trip_distance | DECIMAL(10,2) | YES | NULL | Distância da corrida em milhas |
| 10 | fare_amount | DECIMAL(10,2) | YES | NULL | Valor base da tarifa |
| 11 | extra | DECIMAL(10,2) | YES | NULL | Extras (rush hour $0.50, overnight $1.00) |
| 12 | mta_tax | DECIMAL(10,2) | YES | NULL | Taxa MTA ($0.50) |
| 13 | tip_amount | DECIMAL(10,2) | YES | NULL | Gorjeta (apenas cartão) |
| 14 | tolls_amount | DECIMAL(10,2) | YES | NULL | Pedágios |
| 15 | ehail_fee | DECIMAL(10,2) | YES | NULL | Taxa e-hail (deprecated) |
| 16 | improvement_surcharge | DECIMAL(10,2) | YES | NULL | Sobretaxa de melhoria ($0.30) |
| 17 | total_amount | DECIMAL(10,2) | YES | NULL | Valor total da corrida |
| 18 | payment_type | INT | YES | NULL | Código do tipo de pagamento |
| 19 | trip_type | INT | YES | NULL | Código do tipo de corrida |
| 20 | congestion_surcharge | DECIMAL(10,2) | YES | NULL | Taxa de congestionamento ($2.75) |
| 21 | source_file | VARCHAR(100) | NO | - | Nome do arquivo de origem |
| 22 | load_timestamp | DATETIME | NO | GETDATE() | Timestamp de carga |

**Particionamento:** `year` (INT), `month` (INT)

**Índices:** Nenhum (append-only)

```sql
-- DDL Preview
CREATE TABLE bronze.lnd_green_tripdata (
    vendor_id               INT,
    pickup_datetime         VARCHAR(50),
    dropoff_datetime        VARCHAR(50),
    store_and_fwd_flag      VARCHAR(1),
    ratecode_id             INT,
    pu_location_id          INT,
    do_location_id          INT,
    passenger_count         INT,
    trip_distance           DECIMAL(10,2),
    fare_amount             DECIMAL(10,2),
    extra                   DECIMAL(10,2),
    mta_tax                 DECIMAL(10,2),
    tip_amount              DECIMAL(10,2),
    tolls_amount            DECIMAL(10,2),
    ehail_fee               DECIMAL(10,2),
    improvement_surcharge   DECIMAL(10,2),
    total_amount            DECIMAL(10,2),
    payment_type            INT,
    trip_type               INT,
    congestion_surcharge    DECIMAL(10,2),
    source_file             VARCHAR(100) NOT NULL,
    load_timestamp          DATETIME NOT NULL DEFAULT GETDATE()
);
```

### 3.3 bronze.lnd_payment_type

**Descrição:** Dados de referência de tipos de pagamento do arquivo JSON.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | payment_type_id | INT | NO | PK | Código do tipo de pagamento |
| 2 | payment_type_desc_raw | NVARCHAR(MAX) | YES | | JSON bruto da descrição |
| 3 | load_timestamp | DATETIME | NO | | Timestamp de carga |

### 3.4 bronze.lnd_rate_code

**Descrição:** Dados de referência de códigos de tarifa do arquivo JSON.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | rate_code_id | INT | NO | PK | Código da tarifa |
| 2 | rate_code_desc | VARCHAR(50) | YES | | Descrição da tarifa |
| 3 | load_timestamp | DATETIME | NO | | Timestamp de carga |

### 3.5 bronze.lnd_trip_type

**Descrição:** Dados de referência de tipos de corrida do arquivo TSV.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | trip_type_id | INT | NO | PK | Código do tipo de corrida |
| 2 | trip_type_desc | VARCHAR(50) | YES | | Descrição do tipo |
| 3 | load_timestamp | DATETIME | NO | | Timestamp de carga |

---

## 4. Silver Layer (Curated)

### 4.1 Diagrama ER - Silver

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SILVER LAYER (Curated)                            │
│                      Cleansed, Typed, Validated, DQ Applied                  │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌─────────────────────────────┐
                           │   slv_payment_type          │
                           ├─────────────────────────────┤
                           │ payment_type_id    INT  PK  │◄────┐
                           │ payment_type_desc  VARCHAR  │     │
                           │ is_active          BIT      │     │
                           │ process_timestamp  DATETIME │     │
                           └─────────────────────────────┘     │
                                                               │ FK
┌─────────────────────────────────────────────────────────────┴───────────────┐
│   slv_trips                                                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ trip_id              BIGINT       PK    (Generated)                          │
│ vendor_id            INT                                                     │
│ pickup_datetime      DATETIME           NOT NULL                             │
│ dropoff_datetime     DATETIME           NOT NULL                             │
│ store_and_fwd_flag   BIT                                                     │
│ ratecode_id          INT          FK → slv_rate_code                         │
│ pu_location_id       INT                BETWEEN 1-265                        │
│ do_location_id       INT                BETWEEN 1-265                        │
│ passenger_count      INT                DEFAULT 1                            │
│ trip_distance        DECIMAL(10,2)      >= 0                                 │
│ fare_amount          DECIMAL(10,2)      >= 0                                 │
│ extra                DECIMAL(10,2)      >= 0                                 │
│ mta_tax              DECIMAL(10,2)      >= 0                                 │
│ tip_amount           DECIMAL(10,2)      >= 0                                 │
│ tolls_amount         DECIMAL(10,2)      >= 0                                 │
│ ehail_fee            DECIMAL(10,2)      DEFAULT 0                            │
│ improvement_surcharge DECIMAL(10,2)     >= 0                                 │
│ total_amount         DECIMAL(10,2)      >= 0                                 │
│ payment_type_id      INT          FK → slv_payment_type                      │
│ trip_type_id         INT          FK → slv_trip_type                         │
│ congestion_surcharge DECIMAL(10,2)      DEFAULT 0                            │
│ trip_duration_min    INT                DERIVED: dropoff - pickup            │
│ dq_status            VARCHAR(20)        'VALID' | 'QUARANTINE' | 'FLAGGED'   │
│ dq_rules_failed      VARCHAR(200)       Comma-separated rule IDs             │
│ process_timestamp    DATETIME                                                │
└─────────────────────────────────────────────────────────────────────────────┬┘
                                                               │ FK
                           ┌─────────────────────────────┐     │
                           │   slv_rate_code             │◄────┘
                           ├─────────────────────────────┤
                           │ rate_code_id       INT  PK  │◄────┐
                           │ rate_code_desc     VARCHAR  │     │
                           │ is_active          BIT      │     │
                           │ process_timestamp  DATETIME │     │
                           └─────────────────────────────┘     │

                           ┌─────────────────────────────┐     │
                           │   slv_trip_type             │◄────┘
                           ├─────────────────────────────┤
                           │ trip_type_id       INT  PK  │
                           │ trip_type_desc     VARCHAR  │
                           │ is_active          BIT      │
                           │ process_timestamp  DATETIME │
                           └─────────────────────────────┘
```

### 4.2 silver.slv_trips

**Descrição:** Corridas de táxi verde limpas, tipadas e validadas. Dados prontos para consumo analítico.

| # | Coluna | Tipo | Nullable | PK/FK | DQ Rule | Descrição |
|---|--------|------|----------|-------|---------|-----------|
| 1 | trip_id | BIGINT | NO | PK | UNIQUE | ID único gerado (ROW_NUMBER) |
| 2 | vendor_id | INT | YES | | IN(1,2) | Código do provedor |
| 3 | pickup_datetime | DATETIME | NO | | DQ-001,002,003,004 | Data/hora início corrida |
| 4 | dropoff_datetime | DATETIME | NO | | DQ-005,006,007,008 | Data/hora fim corrida |
| 5 | store_and_fwd_flag | BIT | YES | | DQ-035 | Flag store-and-forward (0/1) |
| 6 | ratecode_id | INT | YES | FK→slv_rate_code | DQ-028,029 | Código da tarifa |
| 7 | pu_location_id | INT | YES | | DQ-031,032 | Zona de pickup |
| 8 | do_location_id | INT | YES | | DQ-031,032 | Zona de dropoff |
| 9 | passenger_count | INT | YES | | DQ-033 | Número de passageiros |
| 10 | trip_distance | DECIMAL(10,2) | YES | | DQ-019,020,021,022 | Distância em milhas |
| 11 | fare_amount | DECIMAL(10,2) | YES | | DQ-013,014,15 | Valor base tarifav |
| 12 | extra | DECIMAL(10,2) | YES | | ≥0 | Extras |
| 13 | mta_tax | DECIMAL(10,2) | YES | | IN(0,0.5) | Taxa MTA |
| 14 | tip_amount | DECIMAL(10,2) | YES | | DQ-016,17,18 | Gorjeta |
| 15 | tolls_amount | DECIMAL(10,2) | YES | | ≥0 | Pedágios |
| 16 | ehail_fee | DECIMAL(10,2) | YES | | ≥0 | Taxa e-hail |
| 17 | improvement_surcharge | DECIMAL(10,2) | YES | | IN(0,0.3) | Sobretaxa |
| 18 | total_amount | DECIMAL(10,2) | YES | | DQ-009,10,11,12 | Valor total |
| 19 | payment_type_id | INT | YES | FK→slv_payment | DQ-026,27 | Tipo de pagamento |
| 20 | trip_type_id | INT | YES | FK→slv_trip_type | DQ-030 | Tipo de corrida |
| 21 | congestion_surcharge | DECIMAL(10,2) | YES | | ≥0 | Taxa congestionamento |
| 22 | trip_duration_min | INT | YES | | DQ-023,24,25 | Duração calculada (min) |
| 23 | dq_status | VARCHAR(20) | NO | | - | Status DQ do registro |
| 24 | dq_rules_failed | VARCHAR(200) | YES | | - | Regras violadas |
| 25 | process_timestamp | DATETIME | NO | | - | Timestamp processamento |

**Particionamento:** `pickup_date` (DATE)

**Índices:**
- PK: `trip_id`
- IX_pickup_datetime: `pickup_datetime`
- IX_payment_type: `payment_type_id`
- IX_dq_status: `dq_status`

```sql
-- DDL Preview
CREATE TABLE silver.slv_trips (
    trip_id                 BIGINT NOT NULL PRIMARY KEY,
    vendor_id               INT,
    pickup_datetime         DATETIME NOT NULL,
    dropoff_datetime        DATETIME NOT NULL,
    store_and_fwd_flag      BIT,
    ratecode_id             INT,
    pu_location_id          INT,
    do_location_id          INT,
    passenger_count         INT,
    trip_distance           DECIMAL(10,2),
    fare_amount             DECIMAL(10,2),
    extra                   DECIMAL(10,2),
    mta_tax                 DECIMAL(10,2),
    tip_amount              DECIMAL(10,2),
    tolls_amount            DECIMAL(10,2),
    ehail_fee               DECIMAL(10,2),
    improvement_surcharge   DECIMAL(10,2),
    total_amount            DECIMAL(10,2),
    payment_type_id         INT,
    trip_type_id            INT,
    congestion_surcharge    DECIMAL(10,2),
    trip_duration_min       INT,
    dq_status               VARCHAR(20) NOT NULL DEFAULT 'VALID',
    dq_rules_failed         VARCHAR(200),
    process_timestamp       DATETIME NOT NULL DEFAULT GETDATE(),
    
    CONSTRAINT CHK_trip_distance CHECK (trip_distance >= 0),
    CONSTRAINT CHK_total_amount CHECK (total_amount >= 0),
    CONSTRAINT CHK_duration CHECK (trip_duration_min >= 0)
);
```

### 4.3 silver.slv_payment_type

**Descrição:** Tipos de pagamento cleansed e validados.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | payment_type_id | INT | NO | PK | Código do pagamento (1-6) |
| 2 | payment_type_desc | VARCHAR(50) | NO | | Descrição (Credit card, Cash, etc.) |
| 3 | is_active | BIT | NO | | Flag de registro ativo |
| 4 | process_timestamp | DATETIME | NO | | Timestamp processamento |

**Dados de Referência:**
| ID | Description |
|----|-------------|
| 1 | Credit card |
| 2 | Cash |
| 3 | No charge |
| 4 | Dispute |
| 5 | Unknown |
| 6 | Voided trip |

### 4.4 silver.slv_rate_code

**Descrição:** Códigos de tarifa cleansed e validados.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | rate_code_id | INT | NO | PK | Código da tarifa (1-6) |
| 2 | rate_code_desc | VARCHAR(50) | NO | | Descrição |
| 3 | is_active | BIT | NO | | Flag de registro ativo |
| 4 | process_timestamp | DATETIME | NO | | Timestamp processamento |

**Dados de Referência:**
| ID | Description |
|----|-------------|
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau or Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |

### 4.5 silver.slv_trip_type

**Descrição:** Tipos de corrida cleansed e validados.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | trip_type_id | INT | NO | PK | Código do tipo (1-2) |
| 2 | trip_type_desc | VARCHAR(50) | NO | | Descrição |
| 3 | is_active | BIT | NO | | Flag de registro ativo |
| 4 | process_timestamp | DATETIME | NO | | Timestamp processamento |

**Dados de Referência:**
| ID | Description |
|----|-------------|
| 1 | Street-hail |
| 2 | Dispatch |

---

## 5. Gold Layer (Dimensional)

### 5.1 Diagrama Star Schema

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            GOLD LAYER (Star Schema)                                      │
│                               Kimball Dimensional Model                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────────────────┐
                                    │      dim_date           │
                                    │      (Type 0 SCD)       │
                                    ├─────────────────────────┤
                                    │ date_sk         INT PK  │
                                    │ full_date       DATE    │
                                    │ day_of_week     INT     │
                                    │ day_name        VARCHAR │
                                    │ day_of_month    INT     │
                                    │ week_of_year    INT     │
                                    │ month_num       INT     │
                                    │ month_name      VARCHAR │
                                    │ quarter         INT     │
                                    │ year            INT     │
                                    │ is_weekend      BIT     │
                                    │ is_holiday      BIT     │
                                    └───────────┬─────────────┘
                                                │
                                                │ 1:N
         ┌────────────────────┐                 │                 ┌────────────────────┐
         │    dim_payment     │                 │                 │    dim_rate        │
         │    (Type 1 SCD)    │                 │                 │    (Type 1 SCD)    │
         ├────────────────────┤                 │                 ├────────────────────┤
         │payment_type_sk  PK │                 │                 │ rate_code_sk    PK │
         │payment_type_id  NK │                 │                 │ rate_code_id    NK │
         │payment_type_desc   │                 │                 │ rate_code_desc     │
         │is_electronic       │                 │                 │ is_airport         │
         └─────────┬──────────┘                 │                 └─────────┬──────────┘
                   │                            │                           │
                   │ 1:N                        │                           │ 1:N
                   │     ┌──────────────────────┴──────────────────────┐    │
                   │     │                                             │    │
                   │     │              fact_trips                     │    │
                   │     │           (Transaction Fact)                │    │
                   │     ├─────────────────────────────────────────────┤    │
                   └─────┤ trip_sk               BIGINT          PK    ├────┘
                         │ trip_id               BIGINT          NK    │
                         │ date_sk               INT             FK ───┼──────┐
                         │ pickup_time_sk        INT                   │      │
                         │ dropoff_time_sk       INT                   │      │
                         │ pickup_location_sk    INT             FK ───┼──────┼──┐
                         │ dropoff_location_sk   INT             FK ───┼──────┼──┤
                    ┌────┤ payment_type_sk       INT             FK    │      │  │
                    │    │ rate_code_sk          INT             FK ───┼──────┘  │
                    │    │ trip_type_sk          INT             FK ───┼─────────┼──┐
                    │    │─────────────────────────────────────────────│         │  │
                    │    │ vendor_id             INT                   │         │  │
                    │    │ passenger_count       INT                   │         │  │
                    │    │ trip_distance         DECIMAL(10,2)         │         │  │
                    │    │ trip_duration_min     INT                   │         │  │
                    │    │─────────────────────────────────────────────│         │  │
                    │    │ fare_amount           DECIMAL(10,2)  MEASURE│         │  │
                    │    │ extra_amount          DECIMAL(10,2)  MEASURE│         │  │
                    │    │ mta_tax               DECIMAL(10,2)  MEASURE│         │  │
                    │    │ tip_amount            DECIMAL(10,2)  MEASURE│         │  │
                    │    │ tolls_amount          DECIMAL(10,2)  MEASURE│         │  │
                    │    │ improvement_surcharge DECIMAL(10,2)  MEASURE│         │  │
                    │    │ congestion_surcharge  DECIMAL(10,2)  MEASURE│         │  │
                    │    │ total_amount          DECIMAL(10,2)  MEASURE│         │  │
                    │    │─────────────────────────────────────────────│         │  │
                    │    │ revenue_per_mile      DECIMAL(10,4)  DERIVED│         │  │
                    │    │ revenue_per_minute    DECIMAL(10,4)  DERIVED│         │  │
                    │    │ tip_percentage        DECIMAL(5,2)   DERIVED│         │  │
                    │    └─────────────────────────────────────────────┘         │  │
                    │                                                            │  │
                    │                                                            │  │
         ┌──────────┴──────────┐                               ┌─────────────────┴──┴──┐
         │   dim_trip_type     │                               │     dim_location      │
         │   (Type 1 SCD)      │                               │     (Type 1 SCD)      │
         ├─────────────────────┤                               ├───────────────────────┤
         │ trip_type_sk     PK │                               │ location_sk       PK  │
         │ trip_type_id     NK │                               │ location_id       NK  │
         │ trip_type_desc      │                               │ borough              │
         └─────────────────────┘                               │ zone_name            │
                                                               │ service_zone         │
                                                               └───────────────────────┘
```

### 5.2 gold.fact_trips

**Descrição:** Tabela fato transacional contendo uma linha por corrida. Esta é a tabela central do star schema.

**Grain (Granularidade):** Uma corrida de táxi

**Tipo:** Transaction Fact Table

| # | Coluna | Tipo | Nullable | PK/FK | Tipo Campo | Descrição |
|---|--------|------|----------|-------|------------|-----------|
| 1 | trip_sk | BIGINT | NO | PK | Surrogate Key | Chave surrogate gerada |
| 2 | trip_id | BIGINT | NO | NK | Natural Key | ID original da corrida |
| 3 | date_sk | INT | NO | FK | Dimension Key | FK para dim_date (pickup) |
| 4 | pickup_time_sk | INT | NO | | Degenerate | Hora pickup (HHMM) |
| 5 | dropoff_time_sk | INT | NO | | Degenerate | Hora dropoff (HHMM) |
| 6 | pickup_location_sk | INT | YES | FK | Dimension Key | FK para dim_location (PU) |
| 7 | dropoff_location_sk | INT | YES | FK | Dimension Key | FK para dim_location (DO) |
| 8 | payment_type_sk | INT | YES | FK | Dimension Key | FK para dim_payment |
| 9 | rate_code_sk | INT | YES | FK | Dimension Key | FK para dim_rate |
| 10 | trip_type_sk | INT | YES | FK | Dimension Key | FK para dim_trip_type |
| 11 | vendor_id | INT | YES | | Degenerate | ID do provedor |
| 12 | passenger_count | INT | YES | | Measure (discrete) | Passageiros |
| 13 | trip_distance | DECIMAL(10,2) | YES | | Measure (continuous) | Distância (miles) |
| 14 | trip_duration_min | INT | YES | | Measure (continuous) | Duração (min) |
| 15 | fare_amount | DECIMAL(10,2) | YES | | Measure (additive) | Tarifa base |
| 16 | extra_amount | DECIMAL(10,2) | YES | | Measure (additive) | Extras |
| 17 | mta_tax | DECIMAL(10,2) | YES | | Measure (additive) | Taxa MTA |
| 18 | tip_amount | DECIMAL(10,2) | YES | | Measure (additive) | Gorjeta |
| 19 | tolls_amount | DECIMAL(10,2) | YES | | Measure (additive) | Pedágios |
| 20 | improvement_surcharge | DECIMAL(10,2) | YES | | Measure (additive) | Sobretaxa |
| 21 | congestion_surcharge | DECIMAL(10,2) | YES | | Measure (additive) | Congestionamento |
| 22 | total_amount | DECIMAL(10,2) | YES | | Measure (additive) | Total |
| 23 | revenue_per_mile | DECIMAL(10,4) | YES | | Measure (derived) | Total / distance |
| 24 | revenue_per_minute | DECIMAL(10,4) | YES | | Measure (derived) | Total / duration |
| 25 | tip_percentage | DECIMAL(5,2) | YES | | Measure (derived) | Tip / fare × 100 |

**Particionamento:** `date_sk` (mensal)

**Índices:**
- PK: `trip_sk` (clustered)
- IX_date_sk: `date_sk` (para time-series queries)
- IX_payment: `payment_type_sk`
- IX_location: `pickup_location_sk, dropoff_location_sk`

```sql
-- DDL Preview
CREATE TABLE gold.fact_trips (
    trip_sk                 BIGINT IDENTITY(1,1) PRIMARY KEY,
    trip_id                 BIGINT NOT NULL,
    date_sk                 INT NOT NULL,
    pickup_time_sk          INT NOT NULL,
    dropoff_time_sk         INT NOT NULL,
    pickup_location_sk      INT,
    dropoff_location_sk     INT,
    payment_type_sk         INT,
    rate_code_sk            INT,
    trip_type_sk            INT,
    vendor_id               INT,
    passenger_count         INT,
    trip_distance           DECIMAL(10,2),
    trip_duration_min       INT,
    fare_amount             DECIMAL(10,2),
    extra_amount            DECIMAL(10,2),
    mta_tax                 DECIMAL(10,2),
    tip_amount              DECIMAL(10,2),
    tolls_amount            DECIMAL(10,2),
    improvement_surcharge   DECIMAL(10,2),
    congestion_surcharge    DECIMAL(10,2),
    total_amount            DECIMAL(10,2),
    revenue_per_mile        DECIMAL(10,4),
    revenue_per_minute      DECIMAL(10,4),
    tip_percentage          DECIMAL(5,2),
    
    CONSTRAINT FK_fact_date FOREIGN KEY (date_sk) REFERENCES gold.dim_date(date_sk),
    CONSTRAINT FK_fact_payment FOREIGN KEY (payment_type_sk) REFERENCES gold.dim_payment(payment_type_sk),
    CONSTRAINT FK_fact_rate FOREIGN KEY (rate_code_sk) REFERENCES gold.dim_rate(rate_code_sk),
    CONSTRAINT FK_fact_trip_type FOREIGN KEY (trip_type_sk) REFERENCES gold.dim_trip_type(trip_type_sk)
);
```

### 5.3 gold.dim_date

**Descrição:** Dimensão de data role-playing. Uma única dimensão usada para múltiplas datas (pickup, dropoff).

**SCD Type:** Type 0 (não muda)

**Grain:** Um dia do calendário

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | date_sk | INT | NO | PK | Chave surrogate (YYYYMMDD) |
| 2 | full_date | DATE | NO | NK | Data completa |
| 3 | day_of_week | INT | NO | | Dia da semana (1=Dom, 7=Sáb) |
| 4 | day_name | VARCHAR(10) | NO | | Nome do dia |
| 5 | day_of_month | INT | NO | | Dia do mês (1-31) |
| 6 | day_of_year | INT | NO | | Dia do ano (1-366) |
| 7 | week_of_year | INT | NO | | Semana do ano (1-53) |
| 8 | month_num | INT | NO | | Mês (1-12) |
| 9 | month_name | VARCHAR(10) | NO | | Nome do mês |
| 10 | month_short | VARCHAR(3) | NO | | Mês abreviado (Jan, Feb...) |
| 11 | quarter | INT | NO | | Trimestre (1-4) |
| 12 | quarter_name | VARCHAR(10) | NO | | Nome do trimestre (Q1, Q2...) |
| 13 | year | INT | NO | | Ano (YYYY) |
| 14 | year_month | VARCHAR(7) | NO | | Ano-Mês (YYYY-MM) |
| 15 | is_weekend | BIT | NO | | Flag de fim de semana |
| 16 | is_holiday | BIT | NO | | Flag de feriado US |
| 17 | holiday_name | VARCHAR(50) | YES | | Nome do feriado |

**Dados:** 
- Range: 2021-01-01 a 2021-12-31
- Total: 365 registros

```sql
-- DDL Preview
CREATE TABLE gold.dim_date (
    date_sk         INT PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,
    day_of_week     INT NOT NULL,
    day_name        VARCHAR(10) NOT NULL,
    day_of_month    INT NOT NULL,
    day_of_year     INT NOT NULL,
    week_of_year    INT NOT NULL,
    month_num       INT NOT NULL,
    month_name      VARCHAR(10) NOT NULL,
    month_short     VARCHAR(3) NOT NULL,
    quarter         INT NOT NULL,
    quarter_name    VARCHAR(10) NOT NULL,
    year            INT NOT NULL,
    year_month      VARCHAR(7) NOT NULL,
    is_weekend      BIT NOT NULL,
    is_holiday      BIT NOT NULL,
    holiday_name    VARCHAR(50)
);
```

### 5.4 gold.dim_payment

**Descrição:** Dimensão de tipo de pagamento.

**SCD Type:** Type 1 (sobrescreve)

**Grain:** Um tipo de pagamento

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | payment_type_sk | INT | NO | PK | Chave surrogate |
| 2 | payment_type_id | INT | NO | NK | Código original |
| 3 | payment_type_desc | VARCHAR(50) | NO | | Descrição |
| 4 | is_electronic | BIT | NO | | Flag pagamento eletrônico |
| 5 | is_tracked | BIT | NO | | Flag gorjeta rastreada |

**Dados de Referência:**
| SK | ID | Description | is_electronic | is_tracked |
|----|-----|-------------|---------------|------------|
| 1 | 1 | Credit card | 1 | 1 |
| 2 | 2 | Cash | 0 | 0 |
| 3 | 3 | No charge | 0 | 0 |
| 4 | 4 | Dispute | 0 | 0 |
| 5 | 5 | Unknown | 0 | 0 |
| 6 | 6 | Voided trip | 0 | 0 |

### 5.5 gold.dim_rate

**Descrição:** Dimensão de código de tarifa.

**SCD Type:** Type 1 (sobrescreve)

**Grain:** Um código de tarifa

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | rate_code_sk | INT | NO | PK | Chave surrogate |
| 2 | rate_code_id | INT | NO | NK | Código original |
| 3 | rate_code_desc | VARCHAR(50) | NO | | Descrição |
| 4 | is_airport | BIT | NO | | Flag corrida aeroporto |
| 5 | is_flat_rate | BIT | NO | | Flag tarifa fixa |

**Dados de Referência:**
| SK | ID | Description | is_airport | is_flat_rate |
|----|-----|-------------|------------|--------------|
| 1 | 1 | Standard rate | 0 | 0 |
| 2 | 2 | JFK | 1 | 1 |
| 3 | 3 | Newark | 1 | 0 |
| 4 | 4 | Nassau or Westchester | 0 | 0 |
| 5 | 5 | Negotiated fare | 0 | 0 |
| 6 | 6 | Group ride | 0 | 0 |

### 5.6 gold.dim_trip_type

**Descrição:** Dimensão de tipo de corrida.

**SCD Type:** Type 1 (sobrescreve)

**Grain:** Um tipo de corrida

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | trip_type_sk | INT | NO | PK | Chave surrogate |
| 2 | trip_type_id | INT | NO | NK | Código original |
| 3 | trip_type_desc | VARCHAR(50) | NO | | Descrição |
| 4 | is_dispatch | BIT | NO | | Flag corrida dispatch (app) |

**Dados de Referência:**
| SK | ID | Description | is_dispatch |
|----|-----|-------------|-------------|
| 1 | 1 | Street-hail | 0 |
| 2 | 2 | Dispatch | 1 |

### 5.7 gold.dim_location (Futura)

**Descrição:** Dimensão de zonas de localização TLC. **Nota:** Esta dimensão requer dados externos (TLC Zone Shapefile).

**SCD Type:** Type 1 (sobrescreve)

**Grain:** Uma zona TLC

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | location_sk | INT | NO | PK | Chave surrogate |
| 2 | location_id | INT | NO | NK | ID da zona TLC (1-265) |
| 3 | borough | VARCHAR(50) | NO | | Borough (Manhattan, Brooklyn, etc.) |
| 4 | zone_name | VARCHAR(100) | NO | | Nome da zona |
| 5 | service_zone | VARCHAR(50) | NO | | Zona de serviço (Yellow, Boro, Airport) |
| 6 | latitude | DECIMAL(9,6) | YES | | Latitude centroide |
| 7 | longitude | DECIMAL(9,6) | YES | | Longitude centroide |

**Status:** Pendente - requer integração com dados TLC

---

## 6. Audit Layer

### 6.1 audit.dq_results

**Descrição:** Resultados de validação de qualidade de dados por batch.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | dq_result_id | BIGINT | NO | PK | ID do resultado |
| 2 | batch_id | VARCHAR(50) | NO | | ID do batch processado |
| 3 | table_name | VARCHAR(100) | NO | | Tabela validada |
| 4 | rule_id | VARCHAR(20) | NO | | ID da regra DQ |
| 5 | rule_description | VARCHAR(200) | NO | | Descrição da regra |
| 6 | total_records | INT | NO | | Total de registros validados |
| 7 | passed_records | INT | NO | | Registros que passaram |
| 8 | failed_records | INT | NO | | Registros que falharam |
| 9 | pass_rate | DECIMAL(5,2) | NO | | Taxa de aprovação (%) |
| 10 | execution_timestamp | DATETIME | NO | | Timestamp execução |

### 6.2 audit.quarantine_records

**Descrição:** Registros rejeitados ou em quarentena.

| # | Coluna | Tipo | Nullable | PK | Descrição |
|---|--------|------|----------|-----|-----------|
| 1 | quarantine_id | BIGINT | NO | PK | ID do registro |
| 2 | source_table | VARCHAR(100) | NO | | Tabela de origem |
| 3 | source_file | VARCHAR(100) | YES | | Arquivo de origem |
| 4 | rule_id | VARCHAR(20) | NO | | Regra violada |
| 5 | severity | VARCHAR(20) | NO | | Severidade |
| 6 | field_name | VARCHAR(50) | NO | | Campo com problema |
| 7 | field_value | NVARCHAR(MAX) | YES | | Valor problemático |
| 8 | record_json | NVARCHAR(MAX) | NO | | Registro completo em JSON |
| 9 | quarantine_timestamp | DATETIME | NO | | Timestamp |
| 10 | reprocess_status | VARCHAR(20) | NO | | Status reprocessamento |
| 11 | reprocess_timestamp | DATETIME | YES | | Timestamp reprocessamento |

---

## 7. Cardinalidades e Volumetria

### 7.1 Estimativas de Volume

| Tabela | Rows (Q2/2021) | Rows (Anual) | Crescimento |
|--------|----------------|--------------|-------------|
| fact_trips | 1.5M | 6M | +500K/mês |
| dim_date | 365 | 365 | Estático |
| dim_payment | 6 | 6 | Estático |
| dim_rate | 6 | 6 | Estático |
| dim_trip_type | 2 | 2 | Estático |
| dim_location | 265 | 265 | Estático |
| audit.dq_results | ~100 | ~1.2K | +100/batch |
| audit.quarantine | ~30K | ~120K | ~2% do total |

### 7.2 Cardinalidades de Relacionamento

| Fact → Dimension | Cardinalidade | Selectivity |
|------------------|---------------|-------------|
| fact_trips → dim_date | N:1 | ~4K trips/day |
| fact_trips → dim_payment | N:1 | ~250K trips/type |
| fact_trips → dim_rate | N:1 | Varies |
| fact_trips → dim_trip_type | N:1 | ~750K trips/type |
| fact_trips → dim_location (PU) | N:1 | Varies |
| fact_trips → dim_location (DO) | N:1 | Varies |

---

## 8. Transformações de Chave

### 8.1 Surrogate Key Generation

| Tabela | Estratégia | Exemplo |
|--------|------------|---------|
| fact_trips.trip_sk | IDENTITY(1,1) | 1, 2, 3... |
| dim_date.date_sk | YYYYMMDD | 20210401 |
| dim_*.sk | IDENTITY | 1, 2, 3... |

### 8.2 Time Keys

| Campo | Formato | Exemplo |
|-------|---------|---------|
| date_sk | YYYYMMDD | 20210415 |
| pickup_time_sk | HHMM | 0830, 1445 |
| dropoff_time_sk | HHMM | 0915, 1530 |

```sql
-- Cálculo de date_sk
CAST(FORMAT(pickup_datetime, 'yyyyMMdd') AS INT)

-- Cálculo de time_sk
CAST(FORMAT(pickup_datetime, 'HHmm') AS INT)
```

---

## 9. Medidas Derivadas

### 9.1 Fórmulas

| Medida | Fórmula | Tipo |
|--------|---------|------|
| trip_duration_min | DATEDIFF(MINUTE, pickup_datetime, dropoff_datetime) | Calculated |
| revenue_per_mile | total_amount / NULLIF(trip_distance, 0) | Calculated |
| revenue_per_minute | total_amount / NULLIF(trip_duration_min, 0) | Calculated |
| tip_percentage | (tip_amount / NULLIF(fare_amount, 0)) * 100 | Calculated |

### 9.2 Agregações Pré-calculadas (Futuro)

| Tabela | Grain | Uso |
|--------|-------|-----|
| gold.agg_daily_revenue | 1 row/day/zone | Dashboard KPIs |
| gold.agg_hourly_demand | 1 row/hour/zone | Heatmaps |
| gold.agg_monthly_summary | 1 row/month | Executive reports |

---

## 10. Diagrama Completo

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    NYC GREEN TAXI - DATA MODEL                                   │
│                                    Medallion + Star Schema                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

  SOURCE FILES              BRONZE LAYER               SILVER LAYER                GOLD LAYER
  ────────────              ────────────               ────────────                ──────────
  
  ┌───────────┐            ┌─────────────────┐        ┌─────────────────┐         ┌─────────────┐
  │  CSV      │───────────▶│lnd_green_tripdata│───────▶│   slv_trips     │────────▶│ fact_trips  │
  │(tripdata) │   Copy     │   (raw)         │ Clean  │   (validated)   │  Model  │  (grain:1   │
  └───────────┘            └─────────────────┘ + DQ   └─────────────────┘         │   trip)     │
                                                                                   └──────┬──────┘
  ┌───────────┐            ┌─────────────────┐        ┌─────────────────┐                │
  │  JSON     │───────────▶│lnd_payment_type │───────▶│slv_payment_type │───────────────▶├──▶dim_payment
  │(payment)  │   Parse    │   (raw JSON)    │Extract │   (cleansed)    │   Lookup      │
  └───────────┘            └─────────────────┘        └─────────────────┘                │
                                                                                         │
  ┌───────────┐            ┌─────────────────┐        ┌─────────────────┐                │
  │  JSON     │───────────▶│ lnd_rate_code   │───────▶│ slv_rate_code   │───────────────▶├──▶dim_rate
  │(rate)     │   Parse    │   (raw JSON)    │Extract │   (cleansed)    │   Lookup      │
  └───────────┘            └─────────────────┘        └─────────────────┘                │
                                                                                         │
  ┌───────────┐            ┌─────────────────┐        ┌─────────────────┐                │
  │  TSV      │───────────▶│ lnd_trip_type   │───────▶│ slv_trip_type   │───────────────▶├──▶dim_trip_type
  │(trip_type)│   Parse    │   (raw TSV)     │ Trim   │   (cleansed)    │   Lookup      │
  └───────────┘            └─────────────────┘        └─────────────────┘                │
                                                                                         │
                                                       ┌─────────────────┐                │
                                                       │   (generated)   │───────────────▶├──▶dim_date
                                                       │  date calendar  │   Generate     │
                                                       └─────────────────┘                │
                                                                                         │
                                                       ┌─────────────────┐                │
                                                       │   (external)    │───────────────▶└──▶dim_location
                                                       │  TLC zones      │   External     (future)
                                                       └─────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                         AUDIT LAYER                                             │
  │                           dq_results  │  quarantine_records                                     │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Sofia & Winston | Versão inicial completa |

---

*Documento gerado pelo 🧩 DataModeler & 🏗️ DataArchitect Agents - Avanade™ Core*
