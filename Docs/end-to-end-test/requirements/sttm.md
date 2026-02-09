# 📋 STTM - Source-to-Target Mapping

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 📊 Mary (BusinessAnalyst)  
> **Referências:** [problem-statement.md](../strategy/problem-statement.md) | [kpis.md](../strategy/kpis.md)

---

## 1. Visão Geral

Este documento define o mapeamento completo entre as fontes de dados e as tabelas de destino nas camadas Landing, Silver e Gold do Data Lakehouse.

### 1.1 Resumo de Fontes

| Fonte | Tipo | Formato | Volume | Frequência |
|-------|------|---------|--------|------------|
| Green Tripdata | Transacional | CSV | ~500K rows/mês | Mensal |
| Payment Types | Referência | JSON (nested) | 6 registros | Estático |
| Rate Codes | Referência | JSON (array) | 6 registros | Estático |
| Trip Types | Referência | TSV | 2 registros | Estático |
| Error Logs | Operacional | TXT | ~1K rows/mês | Mensal |

### 1.2 Resumo de Destinos

| Camada | Tabelas | Propósito |
|--------|---------|-----------|
| **Landing** | 4 tabelas | Dados brutos, sem transformação |
| **Silver** | 4 tabelas | Dados limpos, tipados, validados |
| **Gold** | 5 tabelas | Modelo dimensional para análise |

---

## 2. Arquitetura de Camadas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                    │
├────────────────┬────────────────┬────────────────┬──────────────────────────┤
│  CSV Files     │  JSON Files    │  TSV Files     │  TXT Files               │
│  (Tripdata)    │  (Reference)   │  (Reference)   │  (Error Logs)            │
└───────┬────────┴───────┬────────┴───────┬────────┴────────┬─────────────────┘
        │                │                │                 │
        ▼                ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LANDING LAYER (lnd_)                               │
│   lnd_green_tripdata  │  lnd_payment_type  │  lnd_rate_code  │ lnd_trip_type│
└───────────────────────────────────────────┬─────────────────────────────────┘
                                            │ Cleanse + Type + Validate
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SILVER LAYER (slv_)                                │
│   slv_trips  │  slv_payment_type  │  slv_rate_code  │  slv_trip_type        │
└───────────────────────────────────────────┬─────────────────────────────────┘
                                            │ Aggregate + Enrich + Model
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GOLD LAYER (gld_)                                 │
│   fact_trips  │  dim_payment  │  dim_rate  │  dim_trip_type  │  dim_date    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Fontes de Dados - Detalhamento

### 3.1 Green Tripdata (CSV)

**Localização:** `data-engineer-exec-agent/Files/green_tripdata_2021-{MM}.csv`

| # | Campo Fonte | Tipo Fonte | Exemplo | Descrição |
|---|-------------|------------|---------|-----------|
| 1 | VendorID | INT | 2 | Código do provedor LPEP |
| 2 | lpep_pickup_datetime | STRING | 2021-04-01 00:38:16 | Data/hora início corrida |
| 3 | lpep_dropoff_datetime | STRING | 2021-04-01 00:43:14 | Data/hora fim corrida |
| 4 | store_and_fwd_flag | STRING | N | Flag de store-and-forward |
| 5 | RatecodeID | INT | 1 | Código da tarifa |
| 6 | PULocationID | INT | 134 | ID zona de pickup |
| 7 | DOLocationID | INT | 197 | ID zona de dropoff |
| 8 | passenger_count | INT | 2 | Número de passageiros |
| 9 | trip_distance | FLOAT | 1.11 | Distância em milhas |
| 10 | fare_amount | FLOAT | 6.0 | Valor da tarifa base |
| 11 | extra | FLOAT | 0.5 | Extras (rush hour, overnight) |
| 12 | mta_tax | FLOAT | 0.5 | Taxa MTA |
| 13 | tip_amount | FLOAT | 0.0 | Gorjeta |
| 14 | tolls_amount | FLOAT | 0.0 | Pedágios |
| 15 | ehail_fee | FLOAT | NULL | Taxa e-hail |
| 16 | improvement_surcharge | FLOAT | 0.3 | Sobretaxa de melhoria |
| 17 | total_amount | FLOAT | 7.3 | Valor total |
| 18 | payment_type | INT | 2 | Tipo de pagamento |
| 19 | trip_type | INT | 1 | Tipo de corrida |
| 20 | congestion_surcharge | FLOAT | 0.0 | Taxa de congestionamento |

### 3.2 Payment Types (JSON)

**Localização:** `data-engineer-exec-agent/Files/payment_type_array.json`

| Campo Fonte | Tipo | Exemplo | Descrição |
|-------------|------|---------|-----------|
| payment_type | INT | 1 | Código do pagamento |
| payment_type_desc | ARRAY | [{sub_type, value}] | Descrições aninhadas |
| payment_type_desc.sub_type | INT | 1 | Subtipo |
| payment_type_desc.value | STRING | "Credit card" | Descrição |

**Valores de Referência:**
| Code | Description |
|------|-------------|
| 1 | Credit card |
| 2 | Cash |
| 3 | No charge |
| 4 | Dispute |
| 5 | Unknown / Unavailable |
| 6 | Voided trip |

### 3.3 Rate Codes (JSON)

**Localização:** `data-engineer-exec-agent/Files/rate_code.json`

| Campo Fonte | Tipo | Exemplo | Descrição |
|-------------|------|---------|-----------|
| rate_code_id | INT | 1 | Código da tarifa |
| rate_code | STRING | "Standard rate" | Descrição |

**Valores de Referência:**
| Code | Description |
|------|-------------|
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau or Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |

### 3.4 Trip Types (TSV)

**Localização:** `data-engineer-exec-agent/Files/trip_type.tsv`

| Campo Fonte | Tipo | Exemplo | Descrição |
|-------------|------|---------|-----------|
| trip_type | INT | 1 | Código do tipo |
| trip_type_desc | STRING | "Street-hail" | Descrição |

**Valores de Referência:**
| Code | Description |
|------|-------------|
| 1 | Street-hail |
| 2 | Dispatch |

---

## 4. Landing Layer - Mapeamento

### 4.1 lnd_green_tripdata

| # | Campo Destino | Tipo Destino | Campo Fonte | Transformação |
|---|---------------|--------------|-------------|---------------|
| 1 | vendor_id | INT | VendorID | CAST AS INT |
| 2 | pickup_datetime | VARCHAR(50) | lpep_pickup_datetime | AS-IS |
| 3 | dropoff_datetime | VARCHAR(50) | lpep_dropoff_datetime | AS-IS |
| 4 | store_and_fwd_flag | VARCHAR(1) | store_and_fwd_flag | AS-IS |
| 5 | ratecode_id | INT | RatecodeID | CAST AS INT |
| 6 | pu_location_id | INT | PULocationID | CAST AS INT |
| 7 | do_location_id | INT | DOLocationID | CAST AS INT |
| 8 | passenger_count | INT | passenger_count | CAST AS INT |
| 9 | trip_distance | DECIMAL(10,2) | trip_distance | CAST AS DECIMAL |
| 10 | fare_amount | DECIMAL(10,2) | fare_amount | CAST AS DECIMAL |
| 11 | extra | DECIMAL(10,2) | extra | CAST AS DECIMAL |
| 12 | mta_tax | DECIMAL(10,2) | mta_tax | CAST AS DECIMAL |
| 13 | tip_amount | DECIMAL(10,2) | tip_amount | CAST AS DECIMAL |
| 14 | tolls_amount | DECIMAL(10,2) | tolls_amount | CAST AS DECIMAL |
| 15 | ehail_fee | DECIMAL(10,2) | ehail_fee | COALESCE(0) |
| 16 | improvement_surcharge | DECIMAL(10,2) | improvement_surcharge | CAST AS DECIMAL |
| 17 | total_amount | DECIMAL(10,2) | total_amount | CAST AS DECIMAL |
| 18 | payment_type | INT | payment_type | CAST AS INT |
| 19 | trip_type | INT | trip_type | CAST AS INT |
| 20 | congestion_surcharge | DECIMAL(10,2) | congestion_surcharge | CAST AS DECIMAL |
| 21 | source_file | VARCHAR(100) | - | METADATA: filename |
| 22 | load_timestamp | DATETIME | - | METADATA: GETDATE() |

### 4.2 lnd_payment_type

| # | Campo Destino | Tipo Destino | Campo Fonte | Transformação |
|---|---------------|--------------|-------------|---------------|
| 1 | payment_type_id | INT | payment_type | AS-IS |
| 2 | payment_type_desc_raw | NVARCHAR(MAX) | payment_type_desc | JSON stringify |
| 3 | load_timestamp | DATETIME | - | METADATA: GETDATE() |

### 4.3 lnd_rate_code

| # | Campo Destino | Tipo Destino | Campo Fonte | Transformação |
|---|---------------|--------------|-------------|---------------|
| 1 | rate_code_id | INT | rate_code_id | AS-IS |
| 2 | rate_code_desc | VARCHAR(50) | rate_code | AS-IS |
| 3 | load_timestamp | DATETIME | - | METADATA: GETDATE() |

### 4.4 lnd_trip_type

| # | Campo Destino | Tipo Destino | Campo Fonte | Transformação |
|---|---------------|--------------|-------------|---------------|
| 1 | trip_type_id | INT | trip_type | CAST AS INT |
| 2 | trip_type_desc | VARCHAR(50) | trip_type_desc | TRIM |
| 3 | load_timestamp | DATETIME | - | METADATA: GETDATE() |

---

## 5. Silver Layer - Mapeamento

### 5.1 slv_trips

| # | Campo Destino | Tipo | PK/FK | Fonte | Transformação | DQ Rule |
|---|---------------|------|-------|-------|---------------|---------|
| 1 | trip_id | BIGINT | PK | - | ROW_NUMBER() | UNIQUE |
| 2 | vendor_id | INT | | lnd.vendor_id | AS-IS | IN (1,2) |
| 3 | pickup_datetime | DATETIME | | lnd.pickup_datetime | CONVERT(DATETIME) | NOT NULL, VALID_DATE |
| 4 | dropoff_datetime | DATETIME | | lnd.dropoff_datetime | CONVERT(DATETIME) | NOT NULL, > pickup |
| 5 | store_and_fwd_flag | BIT | | lnd.store_and_fwd_flag | CASE Y/N → 1/0 | IN (0,1) |
| 6 | ratecode_id | INT | FK→dim_rate | lnd.ratecode_id | AS-IS | IN (1-6) |
| 7 | pu_location_id | INT | FK→dim_location | lnd.pu_location_id | AS-IS | BETWEEN 1-265 |
| 8 | do_location_id | INT | FK→dim_location | lnd.do_location_id | AS-IS | BETWEEN 1-265 |
| 9 | passenger_count | INT | | lnd.passenger_count | COALESCE(1) | BETWEEN 0-9 |
| 10 | trip_distance | DECIMAL(10,2) | | lnd.trip_distance | AS-IS | >= 0 |
| 11 | fare_amount | DECIMAL(10,2) | | lnd.fare_amount | AS-IS | >= 0 |
| 12 | extra | DECIMAL(10,2) | | lnd.extra | AS-IS | >= 0 |
| 13 | mta_tax | DECIMAL(10,2) | | lnd.mta_tax | AS-IS | IN (0, 0.5) |
| 14 | tip_amount | DECIMAL(10,2) | | lnd.tip_amount | AS-IS | >= 0 |
| 15 | tolls_amount | DECIMAL(10,2) | | lnd.tolls_amount | AS-IS | >= 0 |
| 16 | ehail_fee | DECIMAL(10,2) | | lnd.ehail_fee | AS-IS | >= 0 |
| 17 | improvement_surcharge | DECIMAL(10,2) | | lnd.improvement_surcharge | AS-IS | IN (0, 0.3) |
| 18 | total_amount | DECIMAL(10,2) | | lnd.total_amount | AS-IS | >= 0none |
| 19 | payment_type_id | INT | FK→dim_payment | lnd.payment_type | AS-IS | IN (1-6) |
| 20 | trip_type_id | INT | FK→dim_trip_type | lnd.trip_type | AS-IS | IN (1,2) |
| 21 | congestion_surcharge | DECIMAL(10,2) | | lnd.congestion_surcharge | AS-IS | >= 0 |
| 22 | trip_duration_min | INT | | DERIVED | DATEDIFF(MIN, pickup, dropoff) | > 0, < 1440 |
| 23 | dq_status | VARCHAR(20) | | - | 'VALID' or 'QUARANTINE' | |
| 24 | process_timestamp | DATETIME | | - | GETDATE() | |

### 5.2 slv_payment_type

| # | Campo Destino | Tipo | PK/FK | Fonte | Transformação |
|---|---------------|------|-------|-------|---------------|
| 1 | payment_type_id | INT | PK | lnd.payment_type_id | AS-IS |
| 2 | payment_type_desc | VARCHAR(50) | | lnd.payment_type_desc_raw | JSON_VALUE([0].value) |
| 3 | is_active | BIT | | - | DEFAULT 1 |
| 4 | process_timestamp | DATETIME | | - | GETDATE() |

### 5.3 slv_rate_code

| # | Campo Destino | Tipo | PK/FK | Fonte | Transformação |
|---|---------------|------|-------|-------|---------------|
| 1 | rate_code_id | INT | PK | lnd.rate_code_id | AS-IS |
| 2 | rate_code_desc | VARCHAR(50) | | lnd.rate_code_desc | TRIM |
| 3 | is_active | BIT | | - | DEFAULT 1 |
| 4 | process_timestamp | DATETIME | | - | GETDATE() |

### 5.4 slv_trip_type

| # | Campo Destino | Tipo | PK/FK | Fonte | Transformação |
|---|---------------|------|-------|-------|---------------|
| 1 | trip_type_id | INT | PK | lnd.trip_type_id | AS-IS |
| 2 | trip_type_desc | VARCHAR(50) | | lnd.trip_type_desc | TRIM |
| 3 | is_active | BIT | | - | DEFAULT 1 |
| 4 | process_timestamp | DATETIME | | - | GETDATE() |

---

## 6. Gold Layer - Mapeamento

### 6.1 fact_trips (Fact Table)

| # | Campo Destino | Tipo | PK/FK | Fonte | Transformação |
|---|---------------|------|-------|-------|---------------|
| 1 | trip_sk | BIGINT | PK | - | IDENTITY |
| 2 | trip_id | BIGINT | NK | slv.trip_id | AS-IS |
| 3 | date_sk | INT | FK→dim_date | slv.pickup_datetime | YYYYMMDD format |
| 4 | pickup_time_sk | INT | FK→dim_time | slv.pickup_datetime | HHMM format |
| 5 | dropoff_time_sk | INT | FK→dim_time | slv.dropoff_datetime | HHMM format |
| 6 | pickup_location_sk | INT | FK→dim_location | slv.pu_location_id | LOOKUP |
| 7 | dropoff_location_sk | INT | FK→dim_location | slv.do_location_id | LOOKUP |
| 8 | payment_type_sk | INT | FK→dim_payment | slv.payment_type_id | LOOKUP |
| 9 | rate_code_sk | INT | FK→dim_rate | slv.ratecode_id | LOOKUP |
| 10 | trip_type_sk | INT | FK→dim_trip_type | slv.trip_type_id | LOOKUP |
| 11 | vendor_id | INT | | slv.vendor_id | AS-IS |
| 12 | passenger_count | INT | | slv.passenger_count | AS-IS |
| 13 | trip_distance | DECIMAL(10,2) | | slv.trip_distance | AS-IS |
| 14 | trip_duration_min | INT | | slv.trip_duration_min | AS-IS |
| 15 | fare_amount | DECIMAL(10,2) | | slv.fare_amount | AS-IS |
| 16 | extra_amount | DECIMAL(10,2) | | slv.extra | AS-IS |
| 17 | mta_tax | DECIMAL(10,2) | | slv.mta_tax | AS-IS |
| 18 | tip_amount | DECIMAL(10,2) | | slv.tip_amount | AS-IS |
| 19 | tolls_amount | DECIMAL(10,2) | | slv.tolls_amount | AS-IS |
| 20 | improvement_surcharge | DECIMAL(10,2) | | slv.improvement_surcharge | AS-IS |
| 21 | congestion_surcharge | DECIMAL(10,2) | | slv.congestion_surcharge | AS-IS |
| 22 | total_amount | DECIMAL(10,2) | | slv.total_amount | AS-IS |
| 23 | revenue_per_mile | DECIMAL(10,4) | | DERIVED | total_amount / NULLIF(trip_distance,0) |
| 24 | revenue_per_minute | DECIMAL(10,4) | | DERIVED | total_amount / NULLIF(trip_duration_min,0) |
| 25 | tip_percentage | DECIMAL(5,2) | | DERIVED | tip_amount / NULLIF(fare_amount,0) * 100 |

**Granularidade:** Uma linha por corrida (trip)

### 6.2 dim_payment (Type 1 SCD)

| # | Campo Destino | Tipo | PK | Fonte | Transformação |
|---|---------------|------|----|----|---------------|
| 1 | payment_type_sk | INT | PK | - | IDENTITY |
| 2 | payment_type_id | INT | NK | slv.payment_type_id | AS-IS |
| 3 | payment_type_desc | VARCHAR(50) | | slv.payment_type_desc | AS-IS |
| 4 | is_electronic | BIT | | DERIVED | CASE payment_type_id IN (1) THEN 1 ELSE 0 |

### 6.3 dim_rate (Type 1 SCD)

| # | Campo Destino | Tipo | PK | Fonte | Transformação |
|---|---------------|------|----|----|---------------|
| 1 | rate_code_sk | INT | PK | - | IDENTITY |
| 2 | rate_code_id | INT | NK | slv.rate_code_id | AS-IS |
| 3 | rate_code_desc | VARCHAR(50) | | slv.rate_code_desc | AS-IS |
| 4 | is_airport | BIT | | DERIVED | CASE rate_code_id IN (2,3) THEN 1 ELSE 0 |

### 6.4 dim_trip_type (Type 1 SCD)

| # | Campo Destino | Tipo | PK | Fonte | Transformação |
|---|---------------|------|----|----|---------------|
| 1 | trip_type_sk | INT | PK | - | IDENTITY |
| 2 | trip_type_id | INT | NK | slv.trip_type_id | AS-IS |
| 3 | trip_type_desc | VARCHAR(50) | | slv.trip_type_desc | AS-IS |

### 6.5 dim_date (Role-Playing)

| # | Campo Destino | Tipo | PK | Fonte | Transformação |
|---|---------------|------|----|----|---------------|
| 1 | date_sk | INT | PK | - | YYYYMMDD |
| 2 | full_date | DATE | | - | AS-IS |
| 3 | day_of_week | INT | | - | DATEPART(WEEKDAY) |
| 4 | day_name | VARCHAR(10) | | - | DATENAME(WEEKDAY) |
| 5 | day_of_month | INT | | - | DAY() |
| 6 | month_num | INT | | - | MONTH() |
| 7 | month_name | VARCHAR(10) | | - | DATENAME(MONTH) |
| 8 | quarter | INT | | - | DATEPART(QUARTER) |
| 9 | year | INT | | - | YEAR() |
| 10 | is_weekend | BIT | | - | CASE day_of_week IN (1,7) |
| 11 | is_holiday | BIT | | - | LOOKUP holiday table |

---

## 7. Regras de Transformação

### 7.1 Transformações de Tipo

| Transformação | Descrição | Exemplo |
|---------------|-----------|---------|
| CONVERT_DATETIME | String → DateTime | '2021-04-01 00:38:16' → DATETIME |
| CAST_DECIMAL | Float → Decimal(10,2) | 6.0 → 6.00 |
| FLAG_TO_BIT | Y/N → 1/0 | 'Y' → 1, 'N' → 0 |
| JSON_EXTRACT | Extract from nested | JSON_VALUE(desc, '$[0].value') |

### 7.2 Transformações de Negócio

| Transformação | Fórmula | Campo Destino |
|---------------|---------|---------------|
| TRIP_DURATION | DATEDIFF(MINUTE, pickup, dropoff) | trip_duration_min |
| REVENUE_PER_MILE | total_amount / trip_distance | revenue_per_mile |
| REVENUE_PER_MINUTE | total_amount / trip_duration_min | revenue_per_minute |
| TIP_PERCENTAGE | (tip_amount / fare_amount) * 100 | tip_percentage |
| IS_AIRPORT | rate_code_id IN (2, 3) | is_airport |
| IS_ELECTRONIC | payment_type_id = 1 | is_electronic |

### 7.3 Tratamento de Nulos

| Campo | Regra | Default |
|-------|-------|---------|
| passenger_count | COALESCE | 1 |
| ehail_fee | COALESCE | 0.00 |
| congestion_surcharge | COALESCE | 0.00 |
| trip_distance | Se NULL → QUARANTINE | - |
| total_amount | Se NULL → QUARANTINE | - |

---

## 8. Volumetria Estimada

### 8.1 Por Fonte (Q2/2021)

| Fonte | Abr | Mai | Jun | Total Q2 |
|-------|-----|-----|-----|----------|
| green_tripdata | 500K | 520K | 510K | ~1.5M |
| payment_type | 6 | 6 | 6 | 6 |
| rate_code | 6 | 6 | 6 | 6 |
| trip_type | 2 | 2 | 2 | 2 |

### 8.2 Por Camada

| Camada | Tabela | Rows Estimadas | Size Estimado |
|--------|--------|----------------|---------------|
| Landing | lnd_green_tripdata | 1.5M | 300 MB |
| Silver | slv_trips | 1.4M | 280 MB |
| Gold | fact_trips | 1.4M | 350 MB |
| Gold | dim_payment | 6 | < 1 KB |
| Gold | dim_rate | 6 | < 1 KB |
| Gold | dim_trip_type | 2 | < 1 KB |
| Gold | dim_date | 365 | < 50 KB |

---

## 9. Relações entre Tabelas

### 9.1 Modelo Dimensional (Star Schema)

```
                    ┌────────────────┐
                    │   dim_date     │
                    │  (date_sk)     │
                    └───────┬────────┘
                            │
┌────────────────┐          │          ┌────────────────┐
│  dim_payment   │          │          │   dim_rate     │
│(payment_type_sk)├─────────┼──────────┤ (rate_code_sk) │
└────────────────┘          │          └────────────────┘
                            │
                    ┌───────┴────────┐
                    │   fact_trips   │
                    │   (trip_sk)    │
                    └───────┬────────┘
                            │
┌────────────────┐          │          ┌────────────────┐
│ dim_trip_type  │          │          │  dim_location  │
│(trip_type_sk)  ├──────────┴──────────┤(location_sk)   │
└────────────────┘                     └────────────────┘
```

### 9.2 Chaves e Relacionamentos

| Tabela Origem | Campo | Tabela Destino | Campo | Cardinalidade |
|---------------|-------|----------------|-------|---------------|
| fact_trips | date_sk | dim_date | date_sk | N:1 |
| fact_trips | payment_type_sk | dim_payment | payment_type_sk | N:1 |
| fact_trips | rate_code_sk | dim_rate | rate_code_sk | N:1 |
| fact_trips | trip_type_sk | dim_trip_type | trip_type_sk | N:1 |
| fact_trips | pickup_location_sk | dim_location | location_sk | N:1 |
| fact_trips | dropoff_location_sk | dim_location | location_sk | N:1 |

---

## 10. Próximos Artefatos

Este STTM alimenta:

| Artefato | Agente | Propósito |
|----------|--------|-----------|
| `analytical-questions.md` | 📊 Mary | Perguntas de negócio |
| `dq-initial.md` | 📊 Mary | Regras de qualidade |
| `architecture.md` | 🏗️ Winston | Design técnico |
| `data-model.md` | 🧩 Sofia | Modelo dimensional |
| `ddl/*.sql` | 🛠️ Diego | Scripts de criação |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Mary (BusinessAnalyst) | Versão inicial completa |

---

*Documento gerado pelo 📊 BusinessAnalyst Agent - Avanade™ Core*
