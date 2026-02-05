# 🛡️ Data Quality Rules

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🛡️ Gaia (DataSteward)  
> **Referências:** [dq-initial.md](../requirements/dq-initial.md) | [data-model.md](../architecture/data-model.md) | [governance.md](governance.md)

---

## 1. Sumário Executivo

Este documento define regras abrangentes de Data Quality (DQ) para todas as camadas do Data Lakehouse, expandindo os requisitos iniciais com implementação técnica detalhada usando **Databricks Delta Live Tables (DLT) Expectations**.

### 1.1 Visão Geral das Regras

| Camada | Total Regras | CRITICAL | HIGH | MEDIUM | LOW |
|--------|--------------|----------|------|--------|-----|
| **Bronze** | 12 | 6 | 4 | 2 | 0 |
| **Silver** | 38 | 12 | 15 | 9 | 2 |
| **Gold** | 15 | 3 | 6 | 5 | 1 |
| **Cross-Layer** | 8 | 2 | 4 | 2 | 0 |
| **Total** | **73** | **23** | **29** | **18** | **3** |

### 1.2 Categorias de Regras

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA QUALITY RULE CATEGORIES                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  CATEGORIA              PROPÓSITO                           REGRAS       EXEMPLO        │
│  ─────────              ─────────                           ──────       ───────        │
│                                                                                         │
│  Completeness           Missing data detection                15       NOT NULL        │
│  Validity               Format and range validation           22       Range check     │
│  Uniqueness             Duplicate detection                    5       PK unique       │
│  Consistency            Cross-field validation                12       Date order      │
│  Referential Integrity  FK validation                          8       Exists in dim   │
│  Timeliness             Data freshness                         4       Max age         │
│  Accuracy               Business rule validation               7       Sum validation  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Severity Levels & Actions

| Severity | Action | Method | Reprocessable | Target Pass Rate |
|----------|--------|--------|---------------|------------------|
| 🔴 **CRITICAL** | REJECT (drop) | `expect_or_drop()` | No | 100% |
| 🟡 **HIGH** | QUARANTINE | `expect_or_quarantine()` | Yes | ≥99% |
| 🟢 **MEDIUM** | FLAG | `expect()` | N/A | ≥95% |
| ℹ️ **LOW** | LOG | `expect()` | N/A | ≥90% |

---

## 2. Bronze Layer Rules

### 2.1 Metadata Quality (All Tables)

| Rule ID | Rule | Severity | Category | DLT Implementation |
|---------|------|----------|----------|--------------------|
| **BRZ-001** | _source_file NOT NULL | 🔴 CRITICAL | Completeness | `expect_or_drop("valid_source_file", "_source_file IS NOT NULL")` |
| **BRZ-002** | _ingestion_timestamp NOT NULL | 🔴 CRITICAL | Completeness | `expect_or_drop("valid_ingestion_ts", "_ingestion_timestamp IS NOT NULL")` |
| **BRZ-003** | _batch_id NOT NULL | 🔴 CRITICAL | Completeness | `expect_or_drop("valid_batch_id", "_batch_id IS NOT NULL")` |
| **BRZ-004** | _ingestion_timestamp ≤ current_timestamp | 🟡 HIGH | Validity | `expect("valid_ingestion_time", "_ingestion_timestamp <= current_timestamp()")` |

### 2.2 lnd_green_tripdata

| Rule ID | Rule | Severity | Category | Field | DLT Implementation |
|---------|------|----------|----------|-------|--------------------|
| **BRZ-010** | pickup_datetime NOT NULL | 🔴 CRITICAL | Completeness | pickup_datetime | `expect_or_drop("not_null_pickup", "lpep_pickup_datetime IS NOT NULL")` |
| **BRZ-011** | dropoff_datetime NOT NULL | 🔴 CRITICAL | Completeness | dropoff_datetime | `expect_or_drop("not_null_dropoff", "lpep_dropoff_datetime IS NOT NULL")` |
| **BRZ-012** | total_amount parseable as DECIMAL | 🟡 HIGH | Validity | total_amount | `expect("parseable_total", "CAST(total_amount AS DECIMAL(10,2)) IS NOT NULL")` |
| **BRZ-013** | trip_distance parseable as DECIMAL | 🟡 HIGH | Validity | trip_distance | `expect("parseable_distance", "CAST(trip_distance AS DECIMAL(10,2)) IS NOT NULL")` |
| **BRZ-014** | passenger_count parseable as INT | 🟢 MEDIUM | Validity | passenger_count | `expect("parseable_passengers", "CAST(passenger_count AS INT) IS NOT NULL")` |
| **BRZ-015** | vendor_id IN (1, 2) | 🟢 MEDIUM | Validity | vendor_id | `expect("valid_vendor", "VendorID IN (1, 2)")` |

### 2.3 lnd_payment_type, lnd_rate_code, lnd_trip_type

| Rule ID | Rule | Severity | Category | DLT Implementation |
|---------|------|----------|----------|--------------------|
| **BRZ-020** | Primary key NOT NULL | 🔴 CRITICAL | Completeness | `expect_or_drop("not_null_pk", "{pk_field} IS NOT NULL")` |
| **BRZ-021** | Primary key UNIQUE | 🔴 CRITICAL | Uniqueness | Handled by constraint |
| **BRZ-022** | Description NOT NULL | 🟡 HIGH | Completeness | `expect("not_null_desc", "{desc_field} IS NOT NULL")` |

**Bronze DLT Pipeline Example:**

```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    name="lnd_green_tripdata",
    comment="Bronze layer - raw trip data from CSV files",
    table_properties={"quality": "bronze", "layer": "landing"}
)
@dlt.expect_or_drop("BRZ-001", "_source_file IS NOT NULL")
@dlt.expect_or_drop("BRZ-002", "_ingestion_timestamp IS NOT NULL")
@dlt.expect_or_drop("BRZ-010", "lpep_pickup_datetime IS NOT NULL")
@dlt.expect_or_drop("BRZ-011", "lpep_dropoff_datetime IS NOT NULL")
@dlt.expect("BRZ-012", "CAST(total_amount AS DECIMAL(10,2)) IS NOT NULL")
@dlt.expect("BRZ-013", "CAST(trip_distance AS DECIMAL(10,2)) IS NOT NULL")
def bronze_green_tripdata():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", "/mnt/schemas/green_tripdata")
        .option("header", "true")
        .load("/mnt/landing/green_tripdata/*.csv")
        .withColumn("_source_file", input_file_name())
        .withColumn("_ingestion_timestamp", current_timestamp())
        .withColumn("_batch_id", lit(spark.conf.get("pipeline.batch_id")))
    )
```

---

## 3. Silver Layer Rules

### 3.1 slv_trips - Completeness Rules

| Rule ID | Rule | Severity | Field | Action | DLT Implementation |
|---------|------|----------|-------|--------|--------------------|
| **SLV-001** | pickup_datetime NOT NULL | 🔴 CRITICAL | pickup_datetime | DROP | `expect_or_drop("DQ-001", "pickup_datetime IS NOT NULL")` |
| **SLV-005** | dropoff_datetime NOT NULL | 🔴 CRITICAL | dropoff_datetime | DROP | `expect_or_drop("DQ-005", "dropoff_datetime IS NOT NULL")` |
| **SLV-009** | total_amount NOT NULL | 🔴 CRITICAL | total_amount | DROP | `expect_or_drop("DQ-009", "total_amount IS NOT NULL")` |
| **SLV-013** | fare_amount NOT NULL | 🟡 HIGH | fare_amount | QUARANTINE | `expect_or_quarantine("DQ-013", "fare_amount IS NOT NULL")` |
| **SLV-019** | trip_distance NOT NULL | 🟡 HIGH | trip_distance | QUARANTINE | `expect_or_quarantine("DQ-019", "trip_distance IS NOT NULL")` |

### 3.2 slv_trips - Validity Rules

| Rule ID | Rule | Severity | Field | Condition | Action | DLT Implementation |
|---------|------|----------|-------|-----------|--------|--------------------|
| **SLV-002** | pickup_datetime parseable | 🔴 CRITICAL | pickup_datetime | Valid date format | DROP | Handled by schema |
| **SLV-003** | pickup_datetime in range | 🟡 HIGH | pickup_datetime | BETWEEN '2021-01-01' AND '2021-12-31' | QUARANTINE | `expect_or_quarantine("DQ-003", "pickup_datetime BETWEEN '2021-01-01' AND '2021-12-31'")` |
| **SLV-004** | pickup_datetime ≤ current | 🟡 HIGH | pickup_datetime | ≤ current_timestamp | QUARANTINE | `expect_or_quarantine("DQ-004", "pickup_datetime <= current_timestamp()")` |
| **SLV-006** | dropoff_datetime parseable | 🔴 CRITICAL | dropoff_datetime | Valid date format | DROP | Handled by schema |
| **SLV-010** | total_amount ≥ 0 | 🔴 CRITICAL | total_amount | >= 0 | QUARANTINE | `expect_or_quarantine("DQ-010", "total_amount >= 0")` |
| **SLV-011** | total_amount ≤ 1000 | 🟡 HIGH | total_amount | <= 1000 | FLAG | `expect("DQ-011", "total_amount <= 1000")` |
| **SLV-014** | fare_amount ≥ 0 | 🔴 CRITICAL | fare_amount | >= 0 | QUARANTINE | `expect_or_quarantine("DQ-014", "fare_amount >= 0")` |
| **SLV-015** | fare_amount ≥ 2.50 or 0 | 🟢 MEDIUM | fare_amount | >= 2.50 OR = 0 | FLAG | `expect("DQ-015", "fare_amount >= 2.50 OR fare_amount = 0")` |
| **SLV-016** | tip_amount ≥ 0 | 🔴 CRITICAL | tip_amount | >= 0 | QUARANTINE | `expect_or_quarantine("DQ-016", "tip_amount >= 0")` |
| **SLV-018** | tip_amount ≤ fare * 1.0 | 🟡 HIGH | tip_amount | <= fare_amount | FLAG | `expect("DQ-018", "tip_amount <= fare_amount * 1.0")` |
| **SLV-020** | trip_distance ≥ 0 | 🔴 CRITICAL | trip_distance | >= 0 | QUARANTINE | `expect_or_quarantine("DQ-020", "trip_distance >= 0")` |
| **SLV-021** | trip_distance ≤ 100 | 🟡 HIGH | trip_distance | <= 100 miles | FLAG | `expect("DQ-021", "trip_distance <= 100")` |
| **SLV-027** | payment_type valid | 🔴 CRITICAL | payment_type | IN (1,2,3,4,5,6) | QUARANTINE | `expect_or_quarantine("DQ-027", "payment_type IN (1,2,3,4,5,6)")` |
| **SLV-028** | ratecode_id valid | 🔴 CRITICAL | ratecode_id | IN (1,2,3,4,5,6) | DEFAULT(1) | `expect("DQ-028", "RatecodeID IN (1,2,3,4,5,6) OR RatecodeID IS NULL")` |
| **SLV-030** | trip_type valid | 🔴 CRITICAL | trip_type | IN (1,2) | DEFAULT(1) | `expect("DQ-030", "trip_type IN (1,2) OR trip_type IS NULL")` |
| **SLV-032** | location_id range | 🔴 CRITICAL | pu/do_location_id | BETWEEN 1 AND 265 | QUARANTINE | `expect_or_quarantine("DQ-032", "PULocationID BETWEEN 1 AND 265 AND DOLocationID BETWEEN 1 AND 265")` |
| **SLV-033** | passenger_count range | 🟢 MEDIUM | passenger_count | BETWEEN 0 AND 9 | COALESCE(1) | `expect("DQ-033", "passenger_count BETWEEN 0 AND 9 OR passenger_count IS NULL")` |

### 3.3 slv_trips - Consistency Rules

| Rule ID | Rule | Severity | Fields | Condition | Action | DLT Implementation |
|---------|------|----------|--------|-----------|--------|--------------------|
| **SLV-007** | dropoff ≥ pickup | 🔴 CRITICAL | pickup/dropoff | dropoff ≥ pickup | QUARANTINE | `expect_or_quarantine("DQ-007", "dropoff_datetime >= pickup_datetime")` |
| **SLV-008** | trip ≤ 24 hours | 🟡 HIGH | pickup/dropoff | Duration ≤ 24h | FLAG | `expect("DQ-008", "(unix_timestamp(dropoff_datetime) - unix_timestamp(pickup_datetime)) / 3600 <= 24")` |
| **SLV-012** | total = sum components | 🟢 MEDIUM | financial fields | total = fare + extras (±$0.01) | FLAG | `expect("DQ-012", "ABS(total_amount - (fare_amount + extra + mta_tax + tip_amount + tolls_amount + improvement_surcharge)) <= 0.02")` |
| **SLV-017** | cash = no tip | 🟢 MEDIUM | payment/tip | IF cash THEN tip=0 | INFO | `expect("DQ-017", "payment_type != 2 OR tip_amount = 0")` |
| **SLV-022** | distance/duration | 🟢 MEDIUM | distance/duration | IF dist>0 THEN dur>0 | FLAG | `expect("DQ-022", "trip_distance = 0 OR trip_duration_min > 0")` |
| **SLV-023** | trip_duration > 0 | 🔴 CRITICAL | trip_duration_min | > 0 minutes | QUARANTINE | `expect_or_quarantine("DQ-023", "trip_duration_min > 0")` |
| **SLV-024** | trip_duration ≤ 24h | 🟡 HIGH | trip_duration_min | < 1440 minutes | FLAG | `expect("DQ-024", "trip_duration_min < 1440")` |
| **SLV-025** | avg_speed ≤ 100mph | 🟢 MEDIUM | distance/duration | Speed < 100 | FLAG | `expect("DQ-025", "trip_duration_min = 0 OR (trip_distance / (trip_duration_min / 60.0)) < 100")` |
| **SLV-029** | JFK rate check | 🟢 MEDIUM | ratecode/fare | IF JFK THEN fare≥$52 | FLAG | `expect("DQ-029", "RatecodeID != 2 OR fare_amount >= 52")` |

### 3.4 slv_trips - Referential Integrity

| Rule ID | Rule | Severity | FK Field | Referenced Table | Action | DLT Implementation |
|---------|------|----------|----------|------------------|--------|--------------------|
| **SLV-040** | payment_type FK | 🟡 HIGH | payment_type | slv_payment_type | DEFAULT(-1) | Enforced in Gold |
| **SLV-041** | ratecode_id FK | 🟡 HIGH | ratecode_id | slv_rate_code | DEFAULT(-1) | Enforced in Gold |
| **SLV-042** | trip_type FK | 🟡 HIGH | trip_type | slv_trip_type | DEFAULT(-1) | Enforced in Gold |

### 3.5 slv_trips - Derived Fields

| Rule ID | Rule | Severity | Derived Field | Formula | Action |
|---------|------|----------|---------------|---------|--------|
| **SLV-050** | trip_duration_min | 🔴 CRITICAL | trip_duration_min | (dropoff - pickup) / 60 | AUTO |
| **SLV-051** | avg_speed_mph | 🟢 MEDIUM | avg_speed_mph | distance / (duration / 60) | AUTO |
| **SLV-052** | pickup_date | 🔴 CRITICAL | pickup_date | DATE(pickup_datetime) | AUTO |
| **SLV-053** | pickup_hour | 🟢 MEDIUM | pickup_hour | HOUR(pickup_datetime) | AUTO |

**Silver DLT Pipeline Example:**

```python
import dlt
from pyspark.sql.functions import *

@dlt.table(
    name="slv_trips",
    comment="Silver layer - validated and enriched trip data",
    table_properties={
        "quality": "silver",
        "layer": "cleansed",
        "delta.autoOptimize.optimizeWrite": "true"
    },
    partition_cols=["pickup_date"]
)
# CRITICAL: Must have (REJECT/DROP)
@dlt.expect_or_drop("SLV-001", "pickup_datetime IS NOT NULL")
@dlt.expect_or_drop("SLV-005", "dropoff_datetime IS NOT NULL")
@dlt.expect_or_drop("SLV-009", "total_amount IS NOT NULL")

# HIGH: Quarantine for review
@dlt.expect_or_quarantine("SLV-003", "pickup_datetime BETWEEN '2021-01-01' AND '2021-12-31'")
@dlt.expect_or_quarantine("SLV-007", "dropoff_datetime >= pickup_datetime")
@dlt.expect_or_quarantine("SLV-010", "total_amount >= 0")
@dlt.expect_or_quarantine("SLV-014", "fare_amount >= 0")
@dlt.expect_or_quarantine("SLV-016", "tip_amount >= 0")
@dlt.expect_or_quarantine("SLV-020", "trip_distance >= 0")
@dlt.expect_or_quarantine("SLV-023", "trip_duration_min > 0")
@dlt.expect_or_quarantine("SLV-027", "payment_type IN (1,2,3,4,5,6)")
@dlt.expect_or_quarantine("SLV-032", "PULocationID BETWEEN 1 AND 265 AND DOLocationID BETWEEN 1 AND 265")

# MEDIUM/LOW: Flag but allow through
@dlt.expect("SLV-011", "total_amount <= 1000")
@dlt.expect("SLV-021", "trip_distance <= 100")
@dlt.expect("SLV-024", "trip_duration_min < 1440")
@dlt.expect("SLV-025", "trip_duration_min = 0 OR (trip_distance / (trip_duration_min / 60.0)) < 100")
@dlt.expect("SLV-012", "ABS(total_amount - (fare_amount + extra + mta_tax + tip_amount + tolls_amount + improvement_surcharge)) <= 0.02")

def slv_trips():
    return (
        dlt.read("lnd_green_tripdata")
        .select(
            # Cast to proper types
            col("VendorID").cast("int").alias("vendor_id"),
            to_timestamp("lpep_pickup_datetime").alias("pickup_datetime"),
            to_timestamp("lpep_dropoff_datetime").alias("dropoff_datetime"),
            col("store_and_fwd_flag"),
            col("RatecodeID").cast("int").alias("ratecode_id"),
            col("PULocationID").cast("int"),
            col("DOLocationID").cast("int"),
            col("passenger_count").cast("int"),
            col("trip_distance").cast("decimal(10,2)"),
            col("fare_amount").cast("decimal(10,2)"),
            col("extra").cast("decimal(10,2)"),
            col("mta_tax").cast("decimal(10,2)"),
            col("tip_amount").cast("decimal(10,2)"),
            col("tolls_amount").cast("decimal(10,2)"),
            col("ehail_fee").cast("decimal(10,2)"),
            col("improvement_surcharge").cast("decimal(10,2)"),
            col("total_amount").cast("decimal(10,2)"),
            col("payment_type").cast("int"),
            col("trip_type").cast("int"),
            col("congestion_surcharge").cast("decimal(10,2)")
        )
        # Derive fields
        .withColumn("trip_duration_min", 
            (unix_timestamp("dropoff_datetime") - unix_timestamp("pickup_datetime")) / 60)
        .withColumn("avg_speed_mph",
            when(col("trip_duration_min") > 0, 
                col("trip_distance") / (col("trip_duration_min") / 60.0))
            .otherwise(0))
        .withColumn("pickup_date", to_date("pickup_datetime"))
        .withColumn("pickup_hour", hour("pickup_datetime"))
        .withColumn("is_weekend", dayofweek("pickup_datetime").isin([1, 7]))
        .withColumn("created_at", current_timestamp())
    )
```

---

## 4. Gold Layer Rules

### 4.1 fact_trips - Integrity Rules

| Rule ID | Rule | Severity | Field | Condition | Action | Implementation |
|---------|------|----------|-------|-----------|--------|----------------|
| **GLD-001** | date_sk NOT NULL | 🔴 CRITICAL | date_sk | NOT NULL | DROP | `WHERE date_sk IS NOT NULL` |
| **GLD-002** | payment_type_sk valid | 🟡 HIGH | payment_type_sk | >= -1 | DEFAULT(-1) | `COALESCE(payment_type_sk, -1)` |
| **GLD-003** | rate_code_sk valid | 🟡 HIGH | rate_code_sk | >= -1 | DEFAULT(-1) | `COALESCE(rate_code_sk, -1)` |
| **GLD-004** | trip_type_sk valid | 🟡 HIGH | trip_type_sk | >= -1 | DEFAULT(-1) | `COALESCE(trip_type_sk, -1)` |

### 4.2 fact_trips - Business Rules

| Rule ID | Rule | Severity | Condition | Purpose | Action |
|---------|------|----------|-----------|---------|--------|
| **GLD-010** | Revenue ≥ 0 | 🔴 CRITICAL | total_amount >= 0 | KPI accuracy | DROP |
| **GLD-011** | Trip count = 1 | 🟡 HIGH | Unique trip | No duplicates | FLAG |
| **GLD-012** | Date exists in dim_date | 🟡 HIGH | FK integrity | Calendar alignment | FLAG |
| **GLD-013** | Measures non-negative | 🟢 MEDIUM | All amounts >= 0 | Logical consistency | FLAG |

### 4.3 Dimension Tables - Integrity

| Rule ID | Rule | Severity | Table | Condition | Action |
|---------|------|----------|-------|-----------|--------|
| **GLD-020** | PK NOT NULL | 🔴 CRITICAL | All dimensions | {table}_sk NOT NULL | REJECT |
| **GLD-021** | PK UNIQUE | 🔴 CRITICAL | All dimensions | Unique constraint | REJECT |
| **GLD-022** | Natural key NOT NULL | 🟡 HIGH | All dimensions | {table}_id NOT NULL | FLAG |
| **GLD-023** | Description populated | 🟢 MEDIUM | All dimensions | description NOT NULL | DEFAULT('Unknown') |

### 4.4 agg_daily_summary - Aggregation Rules

| Rule ID | Rule | Severity | Condition | Purpose | Action |
|---------|------|----------|-----------|---------|--------|
| **GLD-030** | trip_count > 0 | 🟡 HIGH | trip_count > 0 | Valid aggregation | FLAG |
| **GLD-031** | avg values logical | 🟢 MEDIUM | avg >= min, avg <= max | Math consistency | FLAG |
| **GLD-032** | total = sum(fact) | 🟢 MEDIUM | Reconciliation | Accuracy check | FLAG |

**Gold SQL Example:**

```sql
-- Build fact_trips with DQ checks
CREATE OR REPLACE TABLE gold.fact_trips AS
SELECT
    -- Surrogate keys (GLD-001: date_sk NOT NULL enforced)
    CAST(date_format(t.pickup_datetime, 'yyyyMMdd') AS INT) AS date_sk,
    COALESCE(p.payment_type_sk, -1) AS payment_type_sk,  -- GLD-002
    COALESCE(r.rate_code_sk, -1) AS rate_code_sk,        -- GLD-003
    COALESCE(tt.trip_type_sk, -1) AS trip_type_sk,       -- GLD-004
    
    -- Degenerate dimensions
    t.PULocationID AS pickup_location_sk,
    t.DOLocationID AS dropoff_location_sk,
    t.vendor_id,
    
    -- Measures (GLD-010: Revenue >= 0 enforced)
    t.trip_distance,
    t.trip_duration_min,
    t.passenger_count,
    t.fare_amount,
    t.extra,
    t.mta_tax,
    t.tip_amount,
    t.tolls_amount,
    t.improvement_surcharge,
    t.congestion_surcharge,
    t.total_amount,
    
    -- Audit
    current_timestamp() AS created_at
FROM silver.slv_trips t
LEFT JOIN gold.dim_payment_type p 
    ON t.payment_type = p.payment_type
LEFT JOIN gold.dim_rate_code r 
    ON t.ratecode_id = r.ratecode_id
LEFT JOIN gold.dim_trip_type tt 
    ON t.trip_type = tt.trip_type
WHERE 
    -- GLD-001: Enforce date_sk NOT NULL
    t.pickup_datetime IS NOT NULL
    -- GLD-010: Enforce revenue >= 0
    AND t.total_amount >= 0
    -- GLD-011: No duplicates (handled by upstream dedup)
;
```

---

## 5. Cross-Layer Rules

### 5.1 Data Lineage & Reconciliation

| Rule ID | Rule | Severity | Scope | Purpose | Threshold |
|---------|------|----------|-------|---------|-----------|
| **XLR-001** | Bronze → Silver row count | 🟡 HIGH | Pipeline | Data loss detection | ≥95% |
| **XLR-002** | Silver → Gold row count | 🟡 HIGH | Pipeline | Data loss detection | ≥98% |
| **XLR-003** | Source file completeness | 🔴 CRITICAL | Ingestion | Missing files | 100% |
| **XLR-004** | Quarantine rate | 🟡 HIGH | DQ | Quality threshold | ≤5% |
| **XLR-005** | Daily load variance | 🟢 MEDIUM | Volume | Anomaly detection | ±20% |
| **XLR-006** | Revenue reconciliation | 🟡 HIGH | Finance | Accuracy | ±0.1% |
| **XLR-007** | Duplicate detection | 🔴 CRITICAL | Uniqueness | No duplicates | 0 |
| **XLR-008** | Schema drift | 🟢 MEDIUM | Evolution | Breaking changes | Manual review |

### 5.2 Timeliness Rules

| Rule ID | Rule | Severity | SLA | Alert Threshold | Purpose |
|---------|------|----------|-----|-----------------|---------|
| **TML-001** | Bronze load completion | 🔴 CRITICAL | 02:30 | >03:00 | Pipeline health |
| **TML-002** | Silver transform completion | 🟡 HIGH | 03:15 | >04:00 | Pipeline health |
| **TML-003** | Gold build completion | 🟡 HIGH | 03:45 | >04:30 | Pipeline health |
| **TML-004** | Data freshness (age) | 🟢 MEDIUM | <24h | >48h | Relevance |

---

## 6. Quarantine Strategy

### 6.1 Quarantine Table Structure

```sql
CREATE TABLE audit.quarantine_records (
    quarantine_id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Source identification
    source_table            STRING NOT NULL,
    source_layer            STRING NOT NULL,     -- bronze, silver, gold
    source_file             STRING,
    source_batch_id         STRING,
    
    -- DQ rule information
    rule_id                 STRING NOT NULL,     -- SLV-001, SLV-010, etc.
    rule_category           STRING NOT NULL,     -- completeness, validity, etc.
    severity                STRING NOT NULL,     -- CRITICAL, HIGH, MEDIUM
    rule_description        STRING,
    
    -- Failed field details
    field_name              STRING,
    field_value             STRING,
    expected_condition      STRING,
    actual_violation        STRING,
    
    -- Full record
    record_json             STRING NOT NULL,     -- Full record for reprocessing
    record_hash             STRING,              -- SHA2 hash for dedup
    
    -- Timestamps
    quarantine_timestamp    TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    first_seen              TIMESTAMP NOT NULL,
    last_seen               TIMESTAMP NOT NULL,
    occurrence_count        INT DEFAULT 1,
    
    -- Remediation
    reprocess_status        STRING DEFAULT 'PENDING',  -- PENDING, APPROVED, REJECTED, REPROCESSED
    reprocess_action        STRING,              -- FIX_AND_RELOAD, IGNORE, MANUAL_REVIEW
    reviewed_by             STRING,
    review_timestamp        TIMESTAMP,
    review_notes            STRING,
    reprocess_timestamp     TIMESTAMP,
    
    -- Optional: Auto-fix rules
    auto_fix_attempted      BOOLEAN DEFAULT FALSE,
    auto_fix_result         STRING
)
PARTITIONED BY (source_layer, quarantine_timestamp);

-- Indexes for performance
CREATE INDEX idx_rule_id ON audit.quarantine_records(rule_id);
CREATE INDEX idx_status ON audit.quarantine_records(reprocess_status);
CREATE INDEX idx_severity ON audit.quarantine_records(severity);
```

### 6.2 Quarantine Workflow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              QUARANTINE WORKFLOW                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  INCOMING DATA          DQ VALIDATION         DECISION TREE              QUARANTINE
  ─────────────          ─────────────         ─────────────              ──────────

  ┌───────────┐          ┌───────────┐         ┌───────────┐            ┌────────────┐
  │           │          │           │  PASS   │           │            │            │
  │  Source   │────────▶ │    DLT    │────────▶│  Silver   │───────────▶│    Gold    │
  │  Records  │          │Expectations│         │  Table    │            │   Table    │
  │           │          │           │         │           │            │            │
  └───────────┘          └─────┬─────┘         └───────────┘            └────────────┘
                               │
                               │ FAIL
                               ▼
                         ┌───────────┐
                         │ Severity? │
                         └─────┬─────┘
                               │
                ┌──────────────┼──────────────┬──────────────┐
                │              │              │              │
                ▼              ▼              ▼              ▼
         ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
         │ CRITICAL │   │   HIGH   │   │  MEDIUM  │   │   LOW    │
         │  (DROP)  │   │(QUARANTINE)│ │  (FLAG)  │   │  (LOG)   │
         └────┬─────┘   └─────┬────┘   └─────┬────┘   └─────┬────┘
              │               │              │              │
              ▼               ▼              │              │
         ┌──────────┐   ┌──────────┐        │              │
         │  Logged  │   │Quarantine│        │              │
         │   Only   │   │  Table   │        └──────┬───────┘
         │          │   │          │               │
         └──────────┘   └─────┬────┘               ▼
                              │              ┌──────────┐
                              │              │  Silver  │
                              │              │   with   │
                              │              │  _dq_flag│
                              │              └──────────┘
                              ▼
                        ┌──────────┐
                        │  Daily   │
                        │  Review  │
                        └─────┬────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
              ┌─────────┬─────────┬─────────┐
              │  AUTO   │ MANUAL  │ REJECT  │
              │  FIX    │ REVIEW  │ IGNORE  │
              └────┬────┴────┬────┴────┬────┘
                   │         │         │
                   └────┬────┴────┬────┘
                        │         │
                        ▼         ▼
                  ┌──────────┬──────────┐
                  │REPROCESS │ ARCHIVE  │
                  │ & RELOAD │          │
                  └──────────┴──────────┘
```

### 6.3 Quarantine Actions by Severity

| Severity | Automatic Action | Review Required | Reprocessable | Retention |
|----------|------------------|-----------------|---------------|-----------|
| 🔴 CRITICAL | Drop record, log only | No | No | 90 days |
| 🟡 HIGH | Quarantine | Yes (daily) | Yes | 180 days |
| 🟢 MEDIUM | Flag, allow through | No (weekly report) | N/A | 30 days |
| ℹ️ LOW | Log only | No | N/A | 7 days |

### 6.4 Auto-Fix Rules

```sql
-- Example: Auto-fix common issues
CREATE OR REPLACE FUNCTION auto_fix_quarantine_record(record_json STRING)
RETURNS STRUCT<fixed: BOOLEAN, new_record: STRING, fix_applied: STRING>
LANGUAGE SQL
AS
$$
    CASE 
        -- Fix 1: NULL passenger_count → default to 1
        WHEN json_extract_path_text(record_json, 'passenger_count') IS NULL 
        THEN 
            STRUCT(
                TRUE AS fixed,
                json_set(record_json, '$.passenger_count', '1') AS new_record,
                'DEFAULT_PASSENGER_COUNT' AS fix_applied
            )
        
        -- Fix 2: NULL ratecode_id → default to 1 (Standard)
        WHEN json_extract_path_text(record_json, 'ratecode_id') IS NULL 
        THEN 
            STRUCT(
                TRUE AS fixed,
                json_set(record_json, '$.ratecode_id', '1') AS new_record,
                'DEFAULT_RATECODE' AS fix_applied
            )
        
        -- No fix available
        ELSE 
            STRUCT(FALSE AS fixed, record_json AS new_record, NULL AS fix_applied)
    END
$$;
```

---

## 7. Monitoring & Alerting

### 7.1 DQ Metrics Dashboard

```sql
-- Daily DQ Metrics (to be visualized in Power BI)
CREATE OR REPLACE VIEW audit.vw_dq_daily_metrics AS
SELECT
    DATE(execution_timestamp) AS metric_date,
    pipeline_name,
    source_table,
    
    -- Volume metrics
    COUNT(*) AS total_records_processed,
    SUM(CASE WHEN status = 'PASSED' THEN 1 ELSE 0 END) AS records_passed,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS records_failed,
    SUM(CASE WHEN status = 'QUARANTINED' THEN 1 ELSE 0 END) AS records_quarantined,
    
    -- Pass rates
    ROUND(100.0 * SUM(CASE WHEN status = 'PASSED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN status = 'QUARANTINED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS quarantine_rate_pct,
    
    -- By severity
    SUM(CASE WHEN severity = 'CRITICAL' AND status = 'FAILED' THEN 1 ELSE 0 END) AS critical_failures,
    SUM(CASE WHEN severity = 'HIGH' AND status = 'FAILED' THEN 1 ELSE 0 END) AS high_failures,
    SUM(CASE WHEN severity = 'MEDIUM' AND status = 'FAILED' THEN 1 ELSE 0 END) AS medium_failures,
    
    -- By category
    COUNT(DISTINCT rule_id) AS rules_triggered,
    COLLECT_SET(rule_id) AS failed_rules
FROM audit.dq_results
GROUP BY DATE(execution_timestamp), pipeline_name, source_table;
```

### 7.2 Alert Thresholds

| Alert | Condition | Severity | Recipients | Frequency |
|-------|-----------|----------|------------|-----------|
| **Critical Failure Spike** | critical_failures > 0 | 🔴 CRITICAL | #data-alerts, PagerDuty | Immediate |
| **Pass Rate Below Threshold** | pass_rate < 95% | 🔴 CRITICAL | #data-alerts, Email | Immediate |
| **High Quarantine Rate** | quarantine_rate > 5% | 🟡 HIGH | #data-alerts | Daily digest |
| **New Rule Failure** | New rule_id not seen before | 🟡 HIGH | Data Engineers | Immediate |
| **Volume Anomaly** | records ±30% from 7-day avg | 🟢 MEDIUM | Data Team | Daily digest |
| **Schema Drift Detected** | New/missing columns | 🟢 MEDIUM | Data Engineers | Immediate |

### 7.3 Alert SQL Queries

```sql
-- Alert 1: Critical failures
SELECT 
    'CRITICAL_FAILURE_ALERT' AS alert_type,
    source_table,
    rule_id,
    COUNT(*) AS failure_count,
    current_timestamp() AS alert_timestamp
FROM audit.dq_results
WHERE 
    DATE(execution_timestamp) = current_date()
    AND severity = 'CRITICAL'
    AND status = 'FAILED'
GROUP BY source_table, rule_id
HAVING COUNT(*) > 0;

-- Alert 2: Pass rate below threshold
SELECT 
    'PASS_RATE_ALERT' AS alert_type,
    source_table,
    ROUND(100.0 * SUM(CASE WHEN status = 'PASSED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_rate_pct,
    COUNT(*) AS total_records,
    current_timestamp() AS alert_timestamp
FROM audit.dq_results
WHERE DATE(execution_timestamp) = current_date()
GROUP BY source_table
HAVING pass_rate_pct < 95.0;

-- Alert 3: High quarantine rate
SELECT 
    'QUARANTINE_RATE_ALERT' AS alert_type,
    source_table,
    ROUND(100.0 * SUM(CASE WHEN status = 'QUARANTINED' THEN 1 ELSE 0 END) / COUNT(*), 2) AS quarantine_rate_pct,
    SUM(CASE WHEN status = 'QUARANTINED' THEN 1 ELSE 0 END) AS quarantined_count,
    current_timestamp() AS alert_timestamp
FROM audit.dq_results
WHERE DATE(execution_timestamp) = current_date()
GROUP BY source_table
HAVING quarantine_rate_pct > 5.0;
```

---

## 8. DQ KPIs & Reporting

### 8.1 Executive KPIs

| KPI | Target | Formula | Report Frequency |
|-----|--------|---------|------------------|
| **Overall DQ Score** | ≥99% | (passed_records / total_records) × 100 | Daily |
| **Critical Failure Rate** | 0% | (critical_failures / total_records) × 100 | Daily |
| **Quarantine Rate** | ≤1% | (quarantined_records / total_records) × 100 | Daily |
| **Reprocess Success Rate** | ≥80% | (reprocessed_success / total_quarantined) × 100 | Weekly |
| **Time to Resolution** | <24h | AVG(review_timestamp - quarantine_timestamp) | Weekly |
| **Data Freshness** | <24h | MAX(ingestion_timestamp) - current_timestamp | Real-time |

### 8.2 Operational Metrics

```sql
-- Weekly DQ Report
CREATE OR REPLACE VIEW audit.vw_weekly_dq_report AS
WITH weekly_stats AS (
    SELECT
        DATE_TRUNC('week', execution_timestamp) AS week_start,
        source_table,
        COUNT(*) AS total_records,
        SUM(CASE WHEN status = 'PASSED' THEN 1 ELSE 0 END) AS passed,
        SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed,
        SUM(CASE WHEN status = 'QUARANTINED' THEN 1 ELSE 0 END) AS quarantined
    FROM audit.dq_results
    WHERE execution_timestamp >= current_date() - INTERVAL 7 DAYS
    GROUP BY DATE_TRUNC('week', execution_timestamp), source_table
)
SELECT
    week_start,
    source_table,
    total_records,
    passed,
    failed,
    quarantined,
    ROUND(100.0 * passed / total_records, 2) AS pass_rate_pct,
    ROUND(100.0 * quarantined / total_records, 2) AS quarantine_rate_pct,
    
    -- Week-over-week comparison
    LAG(total_records) OVER (PARTITION BY source_table ORDER BY week_start) AS prev_week_records,
    ROUND(100.0 * (total_records - LAG(total_records) OVER (PARTITION BY source_table ORDER BY week_start)) 
        / NULLIF(LAG(total_records) OVER (PARTITION BY source_table ORDER BY week_start), 0), 2) AS volume_change_pct
FROM weekly_stats
ORDER BY week_start DESC, source_table;
```

---

## 9. Troubleshooting Runbook

### 9.1 Common DQ Issues & Resolutions

| Issue | Symptoms | Root Cause | Resolution | Prevention |
|-------|----------|------------|------------|------------|
| **High Quarantine Rate** | >5% quarantine | Source data quality degradation | Contact data provider, apply auto-fix | Implement source monitoring |
| **Critical Failures** | Pipeline stops | Null required fields | Investigate source, manual fix | Add upstream validation |
| **Schema Drift** | Parse errors | Source schema changed | Update DLT schema evolution | Coordinate schema changes |
| **Volume Anomaly** | ±30% from avg | Missing/extra files | Verify source file count | File arrival monitoring |
| **Slow DQ Validation** | >30min Silver | DLT expectations too complex | Optimize rules, increase cluster | Simplify rule logic |

### 9.2 Investigation Checklist

When DQ issues occur, follow this checklist:

```markdown
□ 1. Check audit.dq_results for failed rules
    - Filter by DATE(execution_timestamp) = <issue_date>
    - Group by rule_id to find most common failures

□ 2. Review quarantine table
    - SELECT * FROM audit.quarantine_records WHERE quarantine_timestamp >= <issue_start>
    - Identify patterns in field_name, field_value

□ 3. Validate source data
    - Check source file count (XLR-003)
    - Inspect raw CSV for anomalies
    - Compare schema to expected

□ 4. Check upstream dependencies
    - Verify Bronze load completion time
    - Review _batch_id consistency

□ 5. Analyze trends
    - Compare to 7-day average (audit.vw_dq_daily_metrics)
    - Look for new rule IDs

□ 6. Review cluster logs (Databricks)
    - Check for OOM errors
    - Review DLT pipeline event logs

□ 7. Document findings
    - Update audit.quarantine_records.review_notes
    - Log incident in tracking system
```

---

## 10. Implementation Checklist

### 10.1 Phase 1: Bronze DQ (Week 3-4)

```markdown
□ Implement metadata rules (BRZ-001 to BRZ-004)
□ Configure Auto Loader with schema evolution
□ Add source file tracking (_source_file, _batch_id)
□ Create audit.load_log table
□ Test with sample CSV files
□ Validate Bronze DQ dashboard
```

### 10.2 Phase 2: Silver DQ (Week 5-6)

```markdown
□ Implement DLT pipeline with all 38 SLV rules
□ Configure expect_or_drop() for CRITICAL rules
□ Configure expect_or_quarantine() for HIGH rules
□ Create audit.quarantine_records table
□ Create audit.dq_results table
□ Build DQ monitoring views (vw_dq_daily_metrics)
□ Test quarantine workflow end-to-end
□ Configure alerting (Slack, email)
□ Train team on quarantine review process
```

### 10.3 Phase 3: Gold DQ (Week 7-8)

```markdown
□ Implement Gold integrity rules (GLD-001 to GLD-023)
□ Configure FK enforcement with COALESCE defaults
□ Create dimension -1 records (Unknown)
□ Implement aggregation validation (GLD-030 to GLD-032)
□ Configure reconciliation queries (XLR-001, XLR-002)
□ Test revenue reconciliation (XLR-006)
```

### 10.4 Phase 4: Operationalization (Week 9-10)

```markdown
□ Deploy DQ dashboard to Power BI
□ Configure daily alert jobs
□ Create runbook for on-call
□ Train data analysts on quarantine review
□ Document auto-fix procedures
□ Setup weekly DQ review meeting
□ Enable DQ metrics in executive dashboard
```

---

## 11. Próximos Artefatos

Este documento alimenta:

| Artefato | Agente | Propósito |
|----------|--------|-----------|
| `governance.md` | 🛡️ Gaia | Framework de governança RACI |
| `classification.md` | 🛡️ Gaia | Classificação de sensibilidade |
| `notebooks/dq_*.py` | 🛠️ Diego | Implementação DLT |
| `tests/test_dq_*.py` | 🛠️ Diego | Unit tests para regras DQ |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Gaia (DataSteward) | Versão inicial - 73 regras detalhadas |

---

*Documento gerado pelo 🛡️ DataSteward Agent - Avanade™ Core*
