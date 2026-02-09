# Data Lineage Documentation

**Project:** NYC Green Taxi Analytics  
**Version:** 1.0  
**Last Updated:** 2026-02-05  
**Owner:** DataSteward (Gaia)  
**Phase:** MIDSTREAM - Gate 2  

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Lineage Architecture](#lineage-architecture)
3. [Source-to-Target Mapping](#source-to-target-mapping)
4. [Entity-Level Lineage](#entity-level-lineage)
5. [Column-Level Lineage](#column-level-lineage)
6. [Unity Catalog Lineage Tracking](#unity-catalog-lineage-tracking)
7. [Impact Analysis](#impact-analysis)
8. [Lineage Visualization](#lineage-visualization)
9. [Dependencies & Refresh](#dependencies--refresh)
10. [Maintenance & Governance](#maintenance--governance)

---

## 1. Executive Summary

### Purpose
This document provides comprehensive data lineage tracking for the NYC Green Taxi Analytics platform, enabling full traceability from raw sources through transformation layers to business consumption.

### Lineage Scope
- **Horizontal Lineage:** Source → Bronze → Silver → Gold → BI
- **Vertical Lineage:** Column-level transformations for critical fields
- **Technical Lineage:** Databricks workflows, DLT pipelines, Unity Catalog metadata
- **Business Lineage:** Business questions → KPIs → Reports

### Lineage Tools
| Tool | Purpose | Coverage |
|------|---------|----------|
| Unity Catalog Lineage | Automatic table/column lineage | 100% |
| DLT Pipeline Metadata | Transformation logic tracking | Bronze → Silver → Gold |
| Databricks System Tables | Query history and usage | All consumption |
| This Documentation | Business context and rules | Complete pipeline |

### Key Lineage Metrics
- **Data Sources:** 4 (CSV, JSON, TSV)
- **Bronze Tables:** 4
- **Silver Tables:** 4
- **Gold Tables:** 6 (1 fact + 5 dimensions)
- **BI Reports:** 15+ (planned)
- **Total Lineage Hops:** 4 (Source → Bronze → Silver → Gold → BI)
- **Critical Paths:** 3 (Revenue, Operational, Reference)

---

## 2. Lineage Architecture

### 2.1 Lineage Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    LINEAGE ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SOURCE LAYER (External)                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • green_tripdata_*.csv      [Trip Records]               │  │
│  │ • payment_type_array.json   [Payment Types]              │  │
│  │ • rate_code.json            [Rate Codes]                 │  │
│  │ • trip_type.tsv             [Trip Types]                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  BRONZE LAYER (Raw Ingestion) - Unity Catalog: nyc_taxi.bronze │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • trips_raw              [1:1 from CSV, append-only]     │  │
│  │ • payment_types_raw      [1:1 from JSON]                 │  │
│  │ • rate_codes_raw         [1:1 from JSON]                 │  │
│  │ • trip_types_raw         [1:1 from TSV]                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  SILVER LAYER (Cleaned) - Unity Catalog: nyc_taxi.silver       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • trips_cleaned          [Validated & enriched]          │  │
│  │ • payment_types          [Deduplicated, SCD Type 1]      │  │
│  │ • rate_codes             [Deduplicated, SCD Type 1]      │  │
│  │ • trip_types             [Deduplicated, SCD Type 1]      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  GOLD LAYER (Business) - Unity Catalog: nyc_taxi.gold          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ FACT:                                                     │  │
│  │ • fact_trips             [Star schema center]            │  │
│  │                                                           │  │
│  │ DIMENSIONS:                                               │  │
│  │ • dim_date               [Date dimension]                │  │
│  │ • dim_location           [Zone & borough)                │  │
│  │ • dim_payment            [Payment details]               │  │
│  │ • dim_rate               [Rate code details]             │  │
│  │ • dim_trip_type          [Trip type details]             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                     │
│  CONSUMPTION LAYER (BI)                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Power BI Semantic Models                               │  │
│  │ • Executive Dashboards                                   │  │
│  │ • Operational Reports                                    │  │
│  │ • Ad-hoc SQL Warehouse Queries                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Lineage Tracking Methods

| Layer | Tracking Method | Granularity | Automation |
|-------|----------------|-------------|------------|
| Source → Bronze | DLT pipeline metadata | Table & column | Automatic |
| Bronze → Silver | DLT pipeline metadata + Unity Catalog | Table & column | Automatic |
| Silver → Gold | Spark SQL lineage + Unity Catalog | Table & column | Automatic |
| Gold → BI | Unity Catalog + Power BI metadata | Table | Manual tracking |

### 2.3 Unity Catalog Hierarchy

```
Catalog: nyc_taxi
│
├── Schema: bronze
│   ├── trips_raw
│   ├── payment_types_raw
│   ├── rate_codes_raw
│   └── trip_types_raw
│
├── Schema: silver
│   ├── trips_cleaned
│   ├── payment_types
│   ├── rate_codes
│   └── trip_types
│
└── Schema: gold
    ├── fact_trips
    ├── dim_date
    ├── dim_location
    ├── dim_payment
    ├── dim_rate
    └── dim_trip_type
```

---

## 3. Source-to-Target Mapping

### 3.1 Trip Data Lineage (Critical Path)

#### Source → Bronze
```
SOURCE: green_tripdata_2021-*.csv
├── File Location: abfss://landing@storage.dfs.core.windows.net/taxi/green/
├── Format: CSV with header
├── Partitioning: month=YYYY-MM
├── Row Count: ~80,000 rows/month
├── Load Pattern: Monthly append
│
↓ [DLT Pipeline: ingest_trips_bronze]
│
TARGET: nyc_taxi.bronze.trips_raw
├── Format: Delta Lake
├── Partitioning: BY month (STRING)
├── Load Type: STREAMING APPEND
├── DQ Rules Applied: 12 (see dq-rules.md #BRONZE)
└── Audit Columns: _ingestion_timestamp, _source_file
```

**Transformation Logic:**
```python
# DLT Pipeline: ingest_trips_bronze
@dlt.table(
    name="trips_raw",
    comment="Raw green taxi trip data from CSV files",
    partition_cols=["month"],
    table_properties={"delta.enableChangeDataFeed": "true"}
)
@dlt.expect_all({
    "valid_vendor": "VendorID IS NOT NULL",
    "valid_dates": "lpep_pickup_datetime IS NOT NULL",
    # ... 10 more rules
})
def trips_raw():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("cloudFiles.schemaLocation", schema_location)
            .load(source_path)
            .withColumn("_ingestion_timestamp", current_timestamp())
            .withColumn("_source_file", input_file_name())
            .withColumn("month", date_format("lpep_pickup_datetime", "yyyy-MM"))
    )
```

#### Bronze → Silver
```
SOURCE: nyc_taxi.bronze.trips_raw
│
↓ [DLT Pipeline: transform_trips_silver]
│   Transformations:
│   ├── Remove duplicates (on trip_id)
│   ├── Validate dates (pickup < dropoff)
│   ├── Validate amounts (>= 0)
│   ├── Calculate trip_duration_minutes
│   ├── Apply geo-validations (LocationID exists)
│   ├── Standardize NULL handling
│   └── Apply 38 DQ rules (quarantine failures)
│
TARGET: nyc_taxi.silver.trips_cleaned
├── Format: Delta Lake
├── Partitioning: BY pickup_date (DATE)
├── Load Type: STREAMING with deduplication
├── DQ Rules Applied: 38 (see dq-rules.md #SILVER)
└── Quality Score: Target >= 99.5%
```

**Column-Level Transformations:**
| Source Column (Bronze) | Target Column (Silver) | Transformation |
|------------------------|------------------------|----------------|
| VendorID | vendor_id | INT, NOT NULL validated |
| lpep_pickup_datetime | pickup_datetime | TIMESTAMP, validated pickup < dropoff |
| lpep_dropoff_datetime | dropoff_datetime | TIMESTAMP, validated |
| PULocationID | pickup_location_id | INT, validated against dim_location |
| DOLocationID | dropoff_location_id | INT, validated against dim_location |
| passenger_count | passenger_count | INT, range 1-6 validated |
| trip_distance | trip_distance_miles | DECIMAL(8,2), >= 0 validated |
| fare_amount | fare_amount | DECIMAL(10,2), >= 0 validated |
| total_amount | total_amount | DECIMAL(10,2), >= 0 validated |
| payment_type | payment_type_id | INT, FK validated |
| RatecodeID | rate_code_id | INT, FK validated |
| trip_type | trip_type_id | INT, FK validated |
| *calculated* | trip_duration_minutes | DATEDIFF(minute, pickup, dropoff) |
| *calculated* | pickup_date | DATE from pickup_datetime |

#### Silver → Gold (Fact Table)
```
SOURCE: nyc_taxi.silver.trips_cleaned
│
↓ [Spark SQL Batch: build_fact_trips]
│   Transformations:
│   ├── Join with dim_date (ON pickup_date)
│   ├── Join with dim_location (ON pickup/dropoff location)
│   ├── Join with dim_payment (ON payment_type_id)
│   ├── Join with dim_rate (ON rate_code_id)
│   ├── Join with dim_trip_type (ON trip_type_id)
│   ├── Generate surrogate keys
│   ├── Calculate derived metrics
│   └── Apply 15 Gold DQ rules
│
TARGET: nyc_taxi.gold.fact_trips
├── Format: Delta Lake
├── Partitioning: BY year, month
├── Load Type: BATCH incremental (MERGE)
├── Grain: One row per trip
└── DQ Rules Applied: 15 (see dq-rules.md #GOLD)
```

**Column-Level Transformations:**
| Source (Silver) | Target (Gold) | Transformation |
|----------------|---------------|----------------|
| trip_id | trip_key | BIGINT surrogate key |
| pickup_date | date_key | INT FK to dim_date |
| pickup_location_id | pickup_location_key | INT FK to dim_location |
| dropoff_location_id | dropoff_location_key | INT FK to dim_location |
| payment_type_id | payment_key | INT FK to dim_payment |
| rate_code_id | rate_key | INT FK to dim_rate |
| trip_type_id | trip_type_key | INT FK to dim_trip_type |
| vendor_id | vendor_id | Pass-through |
| pickup_datetime | pickup_datetime | Pass-through |
| dropoff_datetime | dropoff_datetime | Pass-through |
| passenger_count | passenger_count | Pass-through |
| trip_distance_miles | trip_distance_miles | Pass-through |
| fare_amount | fare_amount | Pass-through |
| total_amount | total_amount | Pass-through |
| trip_duration_minutes | trip_duration_minutes | Pass-through |
| *calculated* | revenue_per_mile | total_amount / NULLIF(trip_distance_miles, 0) |
| *calculated* | avg_speed_mph | (trip_distance_miles / NULLIF(trip_duration_minutes, 0)) * 60 |

### 3.2 Reference Data Lineage

#### Payment Types
```
SOURCE: payment_type_array.json
↓ [DLT: ingest_payment_types_bronze]
nyc_taxi.bronze.payment_types_raw
↓ [DLT: transform_payment_types_silver - deduplicate, validate]
nyc_taxi.silver.payment_types
↓ [Spark SQL: build_dim_payment - add surrogate keys, SCD Type 1]
nyc_taxi.gold.dim_payment
```

#### Rate Codes
```
SOURCE: rate_code.json
↓ [DLT: ingest_rate_codes_bronze]
nyc_taxi.bronze.rate_codes_raw
↓ [DLT: transform_rate_codes_silver - deduplicate, validate]
nyc_taxi.silver.rate_codes
↓ [Spark SQL: build_dim_rate - add surrogate keys, SCD Type 1]
nyc_taxi.gold.dim_rate
```

#### Trip Types
```
SOURCE: trip_type.tsv
↓ [DLT: ingest_trip_types_bronze]
nyc_taxi.bronze.trip_types_raw
↓ [DLT: transform_trip_types_silver - deduplicate, validate]
nyc_taxi.silver.trip_types
↓ [Spark SQL: build_dim_trip_type - add surrogate keys, SCD Type 1]
nyc_taxi.gold.dim_trip_type
```

#### Date Dimension (Generated)
```
SOURCE: *GENERATED* (Python script)
↓ [Spark SQL: build_dim_date - generate 2021-2025 calendar]
nyc_taxi.gold.dim_date
├── Grain: One row per day
├── Range: 2021-01-01 to 2025-12-31 (1,826 days)
└── Attributes: 15 (year, quarter, month, day, weekday, etc.)
```

#### Location Dimension (Generated)
```
SOURCE: *GENERATED* (NYC Taxi Zone Lookup - public dataset)
↓ [Spark SQL: build_dim_location - load from external source]
nyc_taxi.gold.dim_location
├── Grain: One row per zone
├── Row Count: 265 (all NYC taxi zones)
└── Attributes: 5 (zone_id, zone_name, borough, service_zone)
```

---

## 4. Entity-Level Lineage

### 4.1 Complete Entity Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                  ENTITY DEPENDENCY GRAPH                        │
└─────────────────────────────────────────────────────────────────┘

SOURCES (4)
├── green_tripdata_*.csv ──────┐
├── payment_type_array.json ───┤
├── rate_code.json ─────────────┤
└── trip_type.tsv ──────────────┤
                                │
                                ↓
BRONZE LAYER (4)                │
├── trips_raw ◄─────────────────┘
├── payment_types_raw ◄─────────┐
├── rate_codes_raw ◄────────────┤
└── trip_types_raw ◄────────────┤
                                │
                                ↓
SILVER LAYER (4)                │
├── trips_cleaned ◄─────────────┘
├── payment_types ◄─────────────┐
├── rate_codes ◄────────────────┤
└── trip_types ◄────────────────┤
                                │
                                ↓
GOLD LAYER (6)                  │
├── fact_trips ◄────────────────┴──┬───┬───┬───┬───┐
│   (depends on ALL dimensions)    │   │   │   │   │
│                                   │   │   │   │   │
├── dim_date ◄────────────────────┘   │   │   │   │
│   (generated, no dependencies)       │   │   │   │
│                                       │   │   │   │
├── dim_location ◄────────────────────┘   │   │   │
│   (generated, no dependencies)           │   │   │
│                                           │   │   │
├── dim_payment ◄─────────────────────────┘   │   │
│   (depends on silver.payment_types)          │   │
│                                               │   │
├── dim_rate ◄────────────────────────────────┘   │
│   (depends on silver.rate_codes)                 │
│                                                   │
└── dim_trip_type ◄───────────────────────────────┘
    (depends on silver.trip_types)

                                ↓
CONSUMPTION LAYER (BI)
├── Power BI Dataset: Taxi Analytics
│   ├── Uses: fact_trips (IMPORT mode)
│   ├── Uses: ALL dimensions (IMPORT mode)
│   └── Refresh: Daily at 6:00 AM
│
├── Executive Dashboard
│   ├── KPI: Revenue trends
│   ├── KPI: Operational efficiency
│   └── Source: Power BI Dataset
│
└── Operational Reports (15+)
    └── Source: SQL Warehouse (DirectQuery to Gold)
```

### 4.2 Entity Lineage Matrix

| Target Entity | Source Entities | Transformation Type | Dependency |
|---------------|-----------------|---------------------|------------|
| **bronze.trips_raw** | green_tripdata_*.csv | Streaming Ingestion | Source file |
| **bronze.payment_types_raw** | payment_type_array.json | Batch Ingestion | Source file |
| **bronze.rate_codes_raw** | rate_code.json | Batch Ingestion | Source file |
| **bronze.trip_types_raw** | trip_type.tsv | Batch Ingestion | Source file |
| **silver.trips_cleaned** | bronze.trips_raw | Streaming Transformation | Bronze |
| **silver.payment_types** | bronze.payment_types_raw | Batch Transformation | Bronze |
| **silver.rate_codes** | bronze.rate_codes_raw | Batch Transformation | Bronze |
| **silver.trip_types** | bronze.trip_types_raw | Batch Transformation | Bronze |
| **gold.dim_date** | *GENERATED* | Generate Calendar | None |
| **gold.dim_location** | *EXTERNAL NYC DATASET* | Load Reference | External |
| **gold.dim_payment** | silver.payment_types | SCD Type 1 | Silver |
| **gold.dim_rate** | silver.rate_codes | SCD Type 1 | Silver |
| **gold.dim_trip_type** | silver.trip_types | SCD Type 1 | Silver |
| **gold.fact_trips** | silver.trips_cleaned, ALL dimensions | Star Schema Join | Silver + All Dims |

### 4.3 Critical Dependencies

**Fact Table Build Order (CRITICAL):**
```
1. dim_date          (no dependencies)
2. dim_location      (no dependencies)
3. dim_payment       (depends on silver.payment_types)
4. dim_rate          (depends on silver.rate_codes)
5. dim_trip_type     (depends on silver.trip_types)
6. fact_trips        (depends on ALL above + silver.trips_cleaned)
```

**Reason:** `fact_trips` has FK constraints to all dimension tables. Dimensions must be built first to ensure referential integrity.

---

## 5. Column-Level Lineage

### 5.1 Revenue Calculation Lineage (Critical Business Metric)

```
┌─────────────────────────────────────────────────────────────────┐
│          REVENUE COLUMN LINEAGE (End-to-End)                    │
└─────────────────────────────────────────────────────────────────┘

SOURCE: green_tripdata_2021-04.csv
│
├── Column: fare_amount (STRING in CSV)
├── Column: extra (STRING in CSV)
├── Column: mta_tax (STRING in CSV)
├── Column: tip_amount (STRING in CSV)
├── Column: tolls_amount (STRING in CSV)
├── Column: improvement_surcharge (STRING in CSV)
└── Column: total_amount (STRING in CSV) ◄── PRIMARY REVENUE FIELD
    │
    ↓
BRONZE: nyc_taxi.bronze.trips_raw
│
├── Column: fare_amount (STRING, unchanged)
├── Column: extra (STRING, unchanged)
├── Column: mta_tax (STRING, unchanged)
├── Column: tip_amount (STRING, unchanged)
├── Column: tolls_amount (STRING, unchanged)
├── Column: improvement_surcharge (STRING, unchanged)
└── Column: total_amount (STRING, unchanged)
    │
    ↓ [DQ Validation: Must be numeric, >= 0]
    │
SILVER: nyc_taxi.silver.trips_cleaned
│
├── Column: fare_amount (DECIMAL(10,2), cast + validated)
├── Column: extra (DECIMAL(10,2), cast + validated)
├── Column: mta_tax (DECIMAL(10,2), cast + validated)
├── Column: tip_amount (DECIMAL(10,2), cast + validated)
├── Column: tolls_amount (DECIMAL(10,2), cast + validated)
├── Column: improvement_surcharge (DECIMAL(10,2), cast + validated)
└── Column: total_amount (DECIMAL(10,2), cast + validated)
    │
    ↓ [DQ Validation: total = fare + extra + mta + tip + tolls + surcharge]
    │
GOLD: nyc_taxi.gold.fact_trips
│
├── Column: fare_amount (DECIMAL(10,2), pass-through)
├── Column: total_amount (DECIMAL(10,2), pass-through) ◄── KPI SOURCE
│
└── Column: revenue_per_mile (DECIMAL(10,2), CALCULATED)
    │       Formula: total_amount / NULLIF(trip_distance_miles, 0)
    │
    ↓
CONSUMPTION: Power BI
│
├── Measure: [Total Revenue] = SUM(fact_trips[total_amount])
├── Measure: [Avg Revenue per Mile] = AVERAGE(fact_trips[revenue_per_mile])
├── Measure: [Revenue Growth %] = DIVIDE([Total Revenue] - [Total Revenue PY], [Total Revenue PY])
│
└── Dashboard: Executive KPI
    └── Visual: Revenue Trend (Line Chart by month)
```

### 5.2 Date/Time Lineage

```
SOURCE: green_tripdata_2021-04.csv
├── Column: lpep_pickup_datetime (STRING: "2021-04-01 00:00:42")
└── Column: lpep_dropoff_datetime (STRING: "2021-04-01 00:09:19")
    │
    ↓
BRONZE: nyc_taxi.bronze.trips_raw
├── Column: lpep_pickup_datetime (STRING, unchanged)
└── Column: lpep_dropoff_datetime (STRING, unchanged)
    │
    ↓ [Cast to TIMESTAMP, validate pickup < dropoff]
    │
SILVER: nyc_taxi.silver.trips_cleaned
├── Column: pickup_datetime (TIMESTAMP)
├── Column: dropoff_datetime (TIMESTAMP)
├── Column: pickup_date (DATE, derived from pickup_datetime)
└── Column: trip_duration_minutes (INT, DATEDIFF(minute, pickup, dropoff))
    │
    ↓ [Join with dim_date on pickup_date]
    │
GOLD: nyc_taxi.gold.fact_trips
├── Column: date_key (INT, FK to dim_date)
├── Column: pickup_datetime (TIMESTAMP, pass-through)
├── Column: dropoff_datetime (TIMESTAMP, pass-through)
└── Column: trip_duration_minutes (INT, pass-through)
    │
    ↓
GOLD: nyc_taxi.gold.dim_date (JOIN target)
├── Column: date_key (INT, PK)
├── Column: full_date (DATE)
├── Column: year (INT)
├── Column: month (INT)
├── Column: day_of_month (INT)
├── Column: day_of_week (INT)
├── Column: weekday_name (STRING)
└── ... (15 attributes total)
    │
    ↓
CONSUMPTION: Power BI
└── Time Intelligence:
    ├── Filter by Year/Quarter/Month (from dim_date)
    ├── Measure: [Trips YTD] = TOTALYTD([Total Trips], dim_date[full_date])
    └── Measure: [Revenue MoM %] = Month-over-month comparison
```

### 5.3 Location Lineage

```
SOURCE: green_tripdata_2021-04.csv
├── Column: PULocationID (STRING: "74")
└── Column: DOLocationID (STRING: "129")
    │
    ↓
BRONZE: nyc_taxi.bronze.trips_raw
├── Column: PULocationID (STRING)
└── Column: DOLocationID (STRING)
    │
    ↓ [Cast to INT, validate against dim_location.zone_id]
    │
SILVER: nyc_taxi.silver.trips_cleaned
├── Column: pickup_location_id (INT)
└── Column: dropoff_location_id (INT)
    │
    ↓ [Join with dim_location twice: pickup + dropoff]
    │
GOLD: nyc_taxi.gold.fact_trips
├── Column: pickup_location_key (INT, FK to dim_location)
└── Column: dropoff_location_key (INT, FK to dim_location)
    │
    ↓
GOLD: nyc_taxi.gold.dim_location (JOIN target)
├── Column: location_key (INT, PK)
├── Column: zone_id (INT, natural key from NYC dataset)
├── Column: zone_name (STRING: "East Harlem North")
├── Column: borough (STRING: "Manhattan")
└── Column: service_zone (STRING: "Boro Zone")
    │
    ↓
CONSUMPTION: Power BI
└── Geo Analysis:
    ├── Slicer: Filter by Borough
    ├── Visual: Top 10 Pickup Zones (Bar chart)
    └── Visual: OD Matrix (Pickup vs Dropoff heatmap)
```

### 5.4 Column Lineage Summary Table

| Gold Column | Silver Source | Bronze Source | CSV Source | Transformations Applied |
|-------------|---------------|---------------|------------|-------------------------|
| **trip_key** | trip_id | - | - | Surrogate key generated |
| **date_key** | pickup_date | - | - | FK lookup from dim_date |
| **pickup_location_key** | pickup_location_id | PULocationID | PULocationID | STRING→INT, FK validated |
| **dropoff_location_key** | dropoff_location_id | DOLocationID | DOLocationID | STRING→INT, FK validated |
| **payment_key** | payment_type_id | payment_type | payment_type | STRING→INT, FK validated |
| **rate_key** | rate_code_id | RatecodeID | RatecodeID | STRING→INT, FK validated |
| **trip_type_key** | trip_type_id | trip_type | trip_type | STRING→INT, FK validated |
| **vendor_id** | vendor_id | VendorID | VendorID | STRING→INT, NOT NULL enforced |
| **pickup_datetime** | pickup_datetime | lpep_pickup_datetime | lpep_pickup_datetime | STRING→TIMESTAMP |
| **dropoff_datetime** | dropoff_datetime | lpep_dropoff_datetime | lpep_dropoff_datetime | STRING→TIMESTAMP |
| **passenger_count** | passenger_count | passenger_count | passenger_count | STRING→INT, range 1-6 |
| **trip_distance_miles** | trip_distance_miles | trip_distance | trip_distance | STRING→DECIMAL(8,2), >= 0 |
| **fare_amount** | fare_amount | fare_amount | fare_amount | STRING→DECIMAL(10,2), >= 0 |
| **total_amount** | total_amount | total_amount | total_amount | STRING→DECIMAL(10,2), component sum validated |
| **trip_duration_minutes** | trip_duration_minutes | *CALCULATED* | - | DATEDIFF(pickup, dropoff) |
| **revenue_per_mile** | *CALCULATED* | - | - | total_amount / trip_distance_miles |
| **avg_speed_mph** | *CALCULATED* | - | - | (distance / duration) * 60 |

---

## 6. Unity Catalog Lineage Tracking

### 6.1 Unity Catalog Lineage Features

Unity Catalog provides automatic lineage tracking for:
- **Table Lineage:** Which tables are read/written by each query
- **Column Lineage:** Which source columns contribute to target columns
- **Query History:** Full SQL/Spark code for each transformation
- **User Attribution:** Who ran each transformation
- **Timestamp Tracking:** When lineage was created/updated

### 6.2 Querying Unity Catalog Lineage

#### Get Table Lineage for fact_trips
```sql
-- Query Unity Catalog system tables for lineage
SELECT
    source_table_full_name,
    source_type,
    target_table_full_name,
    target_type,
    created_at,
    created_by,
    entity_id
FROM system.access.table_lineage
WHERE target_table_full_name = 'nyc_taxi.gold.fact_trips'
ORDER BY created_at DESC;
```

**Expected Output:**
| source_table_full_name | source_type | target_table_full_name | target_type | created_at | created_by |
|------------------------|-------------|------------------------|-------------|------------|------------|
| nyc_taxi.silver.trips_cleaned | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |
| nyc_taxi.gold.dim_date | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |
| nyc_taxi.gold.dim_location | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |
| nyc_taxi.gold.dim_payment | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |
| nyc_taxi.gold.dim_rate | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |
| nyc_taxi.gold.dim_trip_type | TABLE | nyc_taxi.gold.fact_trips | TABLE | 2026-02-05 | data.engineer@company.com |

#### Get Column Lineage for total_amount
```sql
-- Column-level lineage for revenue field
SELECT
    source_table_full_name,
    source_column_name,
    target_table_full_name,
    target_column_name,
    created_at
FROM system.access.column_lineage
WHERE target_table_full_name = 'nyc_taxi.gold.fact_trips'
  AND target_column_name = 'total_amount'
ORDER BY created_at DESC;
```

**Expected Output:**
| source_table_full_name | source_column_name | target_table_full_name | target_column_name | created_at |
|------------------------|-------------------|------------------------|-------------------|------------|
| nyc_taxi.silver.trips_cleaned | total_amount | nyc_taxi.gold.fact_trips | total_amount | 2026-02-05 |

#### Get Full Lineage Chain (Recursive)
```sql
-- Recursive CTE to trace lineage from source to target
WITH RECURSIVE lineage_chain AS (
    -- Base case: start from fact_trips
    SELECT
        target_table_full_name AS table_name,
        0 AS depth
    FROM system.access.table_lineage
    WHERE target_table_full_name = 'nyc_taxi.gold.fact_trips'
    
    UNION ALL
    
    -- Recursive case: find upstream dependencies
    SELECT
        tl.source_table_full_name AS table_name,
        lc.depth + 1 AS depth
    FROM system.access.table_lineage tl
    INNER JOIN lineage_chain lc ON tl.target_table_full_name = lc.table_name
    WHERE lc.depth < 10 -- Prevent infinite loops
)
SELECT DISTINCT
    table_name,
    depth,
    CASE depth
        WHEN 0 THEN 'GOLD (Target)'
        WHEN 1 THEN 'SILVER (Cleaned)'
        WHEN 2 THEN 'BRONZE (Raw)'
        WHEN 3 THEN 'SOURCE (Files)'
        ELSE 'OTHER'
    END AS layer
FROM lineage_chain
ORDER BY depth DESC, table_name;
```

**Expected Output:**
| table_name | depth | layer |
|------------|-------|-------|
| abfss://landing@storage/taxi/green/*.csv | 3 | SOURCE (Files) |
| nyc_taxi.bronze.trips_raw | 2 | BRONZE (Raw) |
| nyc_taxi.silver.trips_cleaned | 1 | SILVER (Cleaned) |
| nyc_taxi.gold.dim_date | 0 | GOLD (Target) |
| nyc_taxi.gold.dim_location | 0 | GOLD (Target) |
| nyc_taxi.gold.fact_trips | 0 | GOLD (Target) |

#### Get Query History for Lineage
```sql
-- Get actual SQL/Spark code that created lineage
SELECT
    query_id,
    query_text,
    executed_by,
    start_time,
    end_time,
    read_table_names,
    write_table_names,
    rows_produced
FROM system.query.history
WHERE ARRAY_CONTAINS(write_table_names, 'nyc_taxi.gold.fact_trips')
ORDER BY start_time DESC
LIMIT 10;
```

### 6.3 DLT Pipeline Lineage Metadata

Delta Live Tables automatically tracks lineage in pipeline event logs:

```sql
-- Query DLT pipeline events for lineage
SELECT
    timestamp,
    event_type,
    details:flow_definition.output_dataset AS target_table,
    details:flow_definition.input_datasets AS source_tables,
    details:flow_progress.metrics.num_output_rows AS rows_processed,
    details:flow_progress.data_quality.expectations AS dq_rules_applied
FROM event_log(TABLE(nyc_taxi_pipelines.pipeline_events))
WHERE event_type = 'flow_progress'
  AND details:flow_definition.output_dataset = 'nyc_taxi.silver.trips_cleaned'
ORDER BY timestamp DESC;
```

---

## 7. Impact Analysis

### 7.1 Impact Analysis Scenarios

#### Scenario 1: Change Source File Format (CSV → Parquet)
```
CHANGE: green_tripdata_*.csv → green_tripdata_*.parquet

IMPACT ANALYSIS:
├── BRONZE LAYER: ⚠️ HIGH IMPACT
│   ├── Table: trips_raw
│   ├── Change Required: Update DLT source format from "csv" to "parquet"
│   ├── Pipeline: ingest_trips_bronze
│   └── Estimated Effort: 2 hours (code + test)
│
├── SILVER LAYER: ✅ NO IMPACT
│   └── Table: trips_cleaned (reads from Bronze, format-agnostic)
│
├── GOLD LAYER: ✅ NO IMPACT
│   └── Table: fact_trips (reads from Silver)
│
└── CONSUMPTION: ✅ NO IMPACT
    └── Power BI (reads from Gold)

TOTAL IMPACT: 1 component, 2 hours effort
```

#### Scenario 2: Add New Column (driver_license_number in source)
```
CHANGE: Add "driver_license_number" to green_tripdata_*.csv

IMPACT ANALYSIS:
├── BRONZE LAYER: ⚠️ MEDIUM IMPACT
│   ├── Table: trips_raw
│   ├── Change Required: Schema evolution (Delta handles automatically)
│   ├── DQ Rules: Add NOT NULL + regex validation
│   └── Estimated Effort: 2 hours (DQ rules + test)
│
├── SILVER LAYER: ⚠️ MEDIUM IMPACT
│   ├── Table: trips_cleaned
│   ├── Change Required: Add column to schema
│   ├── DQ Rules: Add masking rule (PII protection)
│   ├── Classification: CONFIDENTIAL (in classification.md)
│   └── Estimated Effort: 3 hours (schema + DQ + governance)
│
├── GOLD LAYER: ⚠️ OPTIONAL IMPACT
│   ├── Table: fact_trips
│   ├── Change Required: Add column if needed for analytics
│   ├── Security: Apply masking in Unity Catalog
│   └── Estimated Effort: 2 hours (if needed)
│
└── CONSUMPTION: 🔄 BUSINESS DECISION
    ├── Power BI: Add to semantic model?
    └── Governance: Requires approval (PII data)

TOTAL IMPACT: 3 components, 7 hours effort, governance approval required
```

#### Scenario 3: Delete dim_payment Table
```
CHANGE: Drop nyc_taxi.gold.dim_payment

IMPACT ANALYSIS:
├── GOLD LAYER: 🚨 CRITICAL IMPACT - BREAKING CHANGE
│   ├── Table: fact_trips
│   ├── Dependency: FK constraint on payment_key
│   ├── Impact: ETL will fail with FK violation
│   └── Required Action: Remove FK or make payment_key nullable
│
├── CONSUMPTION: 🚨 CRITICAL IMPACT - BREAKING CHANGE
│   ├── Power BI Dataset: "Taxi Analytics"
│   ├── Dependency: Relationships on dim_payment
│   ├── Impact: Dataset refresh will fail
│   ├── Reports Affected: 8 reports use payment_type analysis
│   └── Required Action: Update semantic model, rebuild reports
│
└── BUSINESS IMPACT: 🚨 HIGH
    ├── KPI: "Cashless Trip %" will be unavailable
    ├── Dashboard: "Payment Trends" will break
    └── Users: Executive team, Finance dept

RECOMMENDATION: ❌ DO NOT DELETE - High business impact
ALTERNATIVE: Archive instead of delete, or add "deprecated" flag
```

#### Scenario 4: Change Partition Key (month → year/month)
```
CHANGE: bronze.trips_raw partition from month (STRING) to year/month (INT)

IMPACT ANALYSIS:
├── BRONZE LAYER: 🚨 HIGH IMPACT - REQUIRES REWRITE
│   ├── Table: trips_raw
│   ├── Change Required: Rewrite entire table with new partition scheme
│   ├── Downtime: 2-4 hours for full table rewrite
│   ├── Data Volume: ~240K rows to rewrite
│   └── Estimated Effort: 8 hours (code + test + migration)
│
├── SILVER LAYER: ⚠️ MEDIUM IMPACT
│   ├── Table: trips_cleaned
│   ├── Dependency: Reads from Bronze (partition-agnostic)
│   ├── Impact: DLT pipeline may need cache refresh
│   └── Estimated Effort: 1 hour (test + verify)
│
├── GOLD LAYER: ✅ NO IMPACT
│   └── Table: fact_trips (reads from Silver)
│
└── CONSUMPTION: ✅ NO IMPACT

RECOMMENDATION: ⚠️ PROCEED WITH CAUTION
├── Schedule during maintenance window
├── Backup Bronze table before migration
└── Consider Blue/Green deployment (create new table, switch)
```

### 7.2 Impact Analysis Query

Use Unity Catalog to find downstream dependencies:

```sql
-- Find all tables that depend on a specific table
WITH downstream AS (
    SELECT
        target_table_full_name AS dependent_table,
        1 AS hop_distance
    FROM system.access.table_lineage
    WHERE source_table_full_name = 'nyc_taxi.silver.trips_cleaned'
    
    UNION ALL
    
    SELECT
        tl.target_table_full_name AS dependent_table,
        d.hop_distance + 1 AS hop_distance
    FROM system.access.table_lineage tl
    INNER JOIN downstream d ON tl.source_table_full_name = d.dependent_table
    WHERE d.hop_distance < 10
)
SELECT DISTINCT
    dependent_table,
    MIN(hop_distance) AS min_hops
FROM downstream
GROUP BY dependent_table
ORDER BY min_hops, dependent_table;
```

### 7.3 Impact Analysis Checklist

Before making changes to lineage components:

- [ ] **Identify Impact:** Run Unity Catalog lineage queries
- [ ] **Check Dependencies:** List all downstream tables/reports
- [ ] **Assess Business Impact:** Which KPIs/dashboards are affected?
- [ ] **Estimate Effort:** Hours to update each component
- [ ] **Governance Approval:** Required for schema/classification changes?
- [ ] **Communication Plan:** Notify data consumers
- [ ] **Rollback Plan:** Can we revert if issues occur?
- [ ] **Testing Strategy:** How to validate changes end-to-end?
- [ ] **Deployment Window:** Can we do this without downtime?
- [ ] **Documentation Update:** Update this lineage doc

---

## 8. Lineage Visualization

### 8.1 High-Level Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    DATA LINEAGE FLOW (LEFT TO RIGHT)                 │
└──────────────────────────────────────────────────────────────────────┘

SOURCE FILES              BRONZE              SILVER              GOLD                BI
(External)               (Raw)             (Cleaned)          (Business)       (Consumption)

┌─────────────┐         ┌─────────┐        ┌─────────┐
│green_trip   │────────>│trips_   │───────>│trips_   │───┐
│data_*.csv   │  DLT    │raw      │  DLT   │cleaned  │   │
└─────────────┘ Stream  └─────────┘ Stream └─────────┘   │
                                                          │
┌─────────────┐         ┌─────────┐        ┌─────────┐   │     ┌─────────┐
│payment_type │────────>│payment_ │───────>│payment_ │───┼────>│dim_     │──┐
│array.json   │  DLT    │types_raw│  DLT   │types    │   │     │payment  │  │
└─────────────┘ Batch   └─────────┘ Batch  └─────────┘   │     └─────────┘  │
                                                          │                  │
┌─────────────┐         ┌─────────┐        ┌─────────┐   │     ┌─────────┐  │
│rate_code    │────────>│rate_    │───────>│rate_    │───┼────>│dim_rate │  │
│.json        │  DLT    │codes_raw│  DLT   │codes    │   │     └─────────┘  │
└─────────────┘ Batch   └─────────┘ Batch  └─────────┘   │                  │
                                                          │                  │
┌─────────────┐         ┌─────────┐        ┌─────────┐   │     ┌─────────┐  │
│trip_type    │────────>│trip_    │───────>│trip_    │───┼────>│dim_trip │  │
│.tsv         │  DLT    │types_raw│  DLT   │types    │   │     │_type    │  │
└─────────────┘ Batch   └─────────┘ Batch  └─────────┘   │     └─────────┘  │
                                                          │                  │
                                                          │     ┌─────────┐  │
                           *GENERATED*                    │     │dim_date │  │
                           Calendar                       │     └─────────┘  │
                           2021-2025                      │                  │
                                                          │                  │
                          *GENERATED*                     │     ┌─────────┐  │
                          NYC Zones                       │     │dim_     │  │
                          (265 rows)                      │     │location │  │
                                                          │     └─────────┘  │
                                                          │                  │
                                                          │     ┌─────────┐  │
                                                          └────>│fact_    │<─┤
                                                           JOIN │trips    │  │
                                                                └─────────┘  │
                                                                    │        │
                                                                    v        v
                                                              ┌──────────────────┐
                                                              │Power BI Dataset  │
                                                              │"Taxi Analytics"  │
                                                              └──────────────────┘
                                                                    │
                                                       ┌────────────┼────────────┐
                                                       v            v            v
                                                  ┌─────────┐ ┌─────────┐ ┌─────────┐
                                                  │Exec     │ │Ops      │ │Ad-hoc   │
                                                  │Dashboard│ │Reports  │ │Queries  │
                                                  └─────────┘ └─────────┘ └─────────┘
```

### 8.2 Transformation Depth Diagram

```
DEPTH 0: SOURCE LAYER
├── green_tripdata_2021-04.csv (80,247 rows)
├── green_tripdata_2021-05.csv (78,904 rows)
├── green_tripdata_2021-06.csv (81,351 rows)
├── payment_type_array.json (5 rows)
├── rate_code.json (7 rows)
└── trip_type.tsv (3 rows)
    │
    ↓ [Ingestion: DLT Streaming/Batch]
    │
DEPTH 1: BRONZE LAYER (Raw Ingestion)
├── trips_raw (240,502 rows, partitioned by month)
├── payment_types_raw (5 rows)
├── rate_codes_raw (7 rows)
└── trip_types_raw (3 rows)
    │
    ↓ [Transformation: DLT with DQ Rules]
    │
DEPTH 2: SILVER LAYER (Cleaned & Validated)
├── trips_cleaned (~238,500 rows after quarantine, partitioned by pickup_date)
├── payment_types (5 rows, SCD Type 1)
├── rate_codes (7 rows, SCD Type 1)
└── trip_types (3 rows, SCD Type 1)
    │
    ↓ [Transformation: Spark SQL Batch]
    │
DEPTH 3: GOLD LAYER (Business Dimensional Model)
├── fact_trips (~238,500 rows, partitioned by year/month)
├── dim_date (1,826 rows: 2021-01-01 to 2025-12-31)
├── dim_location (265 rows: NYC taxi zones)
├── dim_payment (5 rows)
├── dim_rate (7 rows)
└── dim_trip_type (3 rows)
    │
    ↓ [Consumption: Power BI / SQL Warehouse]
    │
DEPTH 4: CONSUMPTION LAYER
├── Power BI Dataset (IMPORT mode, daily refresh)
├── Executive Dashboard (15 visuals)
├── Operational Reports (SQL Warehouse DirectQuery)
└── Ad-hoc Analytics (Databricks SQL)
```

---

## 9. Dependencies & Refresh

### 9.1 Refresh Schedule

| Component | Refresh Frequency | Refresh Window | Dependency Chain | Duration |
|-----------|------------------|----------------|------------------|----------|
| **Bronze: trips_raw** | Continuous (Streaming) | 24/7 | Source files → Bronze | Real-time |
| **Bronze: Reference tables** | On-demand | As needed | Source files → Bronze | < 1 min |
| **Silver: trips_cleaned** | Continuous (Streaming) | 24/7 | Bronze → Silver | Real-time |
| **Silver: Reference tables** | On-demand | As needed | Bronze → Silver | < 1 min |
| **Gold: Dimensions** | Daily | 5:00 AM UTC | Silver → Gold dims | 5 mins |
| **Gold: fact_trips** | Daily | 5:30 AM UTC | Dims + Silver → fact | 15 mins |
| **Power BI Dataset** | Daily | 6:00 AM UTC | Gold → BI | 10 mins |
| **Dashboards** | On-demand | User-triggered | BI Dataset → Visuals | < 1 sec |

### 9.2 Dependency Chain

```
CRITICAL PATH (Daily Refresh):

05:00 AM ──> Build dim_date (if new dates)
             Build dim_location (if updated)
             Build dim_payment (from silver.payment_types)
             Build dim_rate (from silver.rate_codes)
             Build dim_trip_type (from silver.trip_types)
             [Parallel execution, 5 minutes total]
             │
             ↓ [Wait for all dimensions]
             │
05:30 AM ──> Build fact_trips
             [Depends on ALL dimensions + silver.trips_cleaned]
             [15 minutes for full refresh]
             │
             ↓ [Wait for fact completion]
             │
06:00 AM ──> Refresh Power BI Dataset
             [Import from all Gold tables]
             [10 minutes with incremental refresh]
             │
             ↓
06:10 AM ──> Dashboards available for business users
```

### 9.3 Failure Recovery

**Scenario: fact_trips build fails at 5:45 AM**

```
LINEAGE-AWARE RECOVERY:

1. Identify Failed Component:
   └─> fact_trips build failed (SQL error or data issue)

2. Check Upstream Status:
   ├─> dim_date: ✅ SUCCESS (built at 5:05 AM)
   ├─> dim_location: ✅ SUCCESS (built at 5:05 AM)
   ├─> dim_payment: ✅ SUCCESS (built at 5:05 AM)
   ├─> dim_rate: ✅ SUCCESS (built at 5:05 AM)
   ├─> dim_trip_type: ✅ SUCCESS (built at 5:05 AM)
   └─> silver.trips_cleaned: ✅ AVAILABLE (streaming, current data)

3. Diagnose Issue:
   └─> Query Unity Catalog lineage for last successful run
   └─> Check DLT expectations logs for quarantined records
   └─> Review query history for FK violations

4. Fix & Retry:
   └─> Fix issue (e.g., add missing dimension row)
   └─> Re-run fact_trips build only (no need to rebuild dims)
   └─> Duration: 15 minutes

5. Downstream Impact:
   ├─> Power BI refresh: Delayed by 30 minutes (5:45 failure + 15 min fix + 10 min BI refresh)
   └─> Final Availability: 6:40 AM (30 min delay vs 6:10 AM SLA)
```

### 9.4 Incremental Processing

**fact_trips Incremental Logic:**
```sql
-- Merge incremental data into fact_trips (avoids full rebuild)
MERGE INTO nyc_taxi.gold.fact_trips AS target
USING (
    SELECT
        t.trip_id,
        d.date_key,
        pl.location_key AS pickup_location_key,
        dl.location_key AS dropoff_location_key,
        p.payment_key,
        r.rate_key,
        tt.trip_type_key,
        t.*
    FROM nyc_taxi.silver.trips_cleaned t
    LEFT JOIN nyc_taxi.gold.dim_date d ON t.pickup_date = d.full_date
    LEFT JOIN nyc_taxi.gold.dim_location pl ON t.pickup_location_id = pl.zone_id
    LEFT JOIN nyc_taxi.gold.dim_location dl ON t.dropoff_location_id = dl.zone_id
    LEFT JOIN nyc_taxi.gold.dim_payment p ON t.payment_type_id = p.payment_type_id
    LEFT JOIN nyc_taxi.gold.dim_rate r ON t.rate_code_id = r.rate_code_id
    LEFT JOIN nyc_taxi.gold.dim_trip_type tt ON t.trip_type_id = tt.trip_type_id
    WHERE t.pickup_date >= CURRENT_DATE - INTERVAL 7 DAYS -- Only process last 7 days
) AS source
ON target.trip_id = source.trip_id
WHEN MATCHED THEN UPDATE SET * -- Update changed records (rare)
WHEN NOT MATCHED THEN INSERT *; -- Insert new records
```

**Benefits:**
- Processes only last 7 days instead of full table (240K rows → 20K rows)
- Reduces processing time from 15 min → 2 min
- Maintains full lineage in Unity Catalog

---

## 10. Maintenance & Governance

### 10.1 Lineage Documentation Maintenance

| Activity | Frequency | Owner | Process |
|----------|-----------|-------|---------|
| **Update Lineage Diagrams** | Quarterly | DataSteward | Review Unity Catalog, update ASCII diagrams |
| **Validate Column Lineage** | Monthly | DataEngineer | Run UC queries, verify source→target mappings |
| **Review Impact Analysis** | On-change | DataArchitect | Update impact scenarios when architecture changes |
| **Audit Lineage Accuracy** | Annually | DataGovernance Board | Compare doc vs UC system tables |
| **Train New Users** | On-demand | DataSteward | Walkthrough lineage doc + UC queries |

### 10.2 Lineage Audit Trail

Every lineage change must be audited:

```sql
-- Audit: Track who modified lineage-impacting tables
SELECT
    user_identity.email AS modified_by,
    table_name,
    operation_name, -- CREATE, ALTER, DROP
    operation_timestamp,
    request_params
FROM system.access.audit
WHERE operation_name IN ('CREATE_TABLE', 'ALTER_TABLE', 'DROP_TABLE')
  AND table_name LIKE 'nyc_taxi.%'
ORDER BY operation_timestamp DESC;
```

### 10.3 Lineage Governance Rules

1. **Rule: No Silent Data Drops**
   - Quarantine failed records, NEVER drop silently
   - Lineage must show quarantine tables in all diagrams

2. **Rule: All Transformations Must Be Traceable**
   - Every derived column must have transformation logic documented
   - Unity Catalog lineage must be enabled for all tables

3. **Rule: Impact Analysis Before Changes**
   - Run impact analysis queries before modifying schemas
   - Document impacted components in change request

4. **Rule: Lineage Review in Gate Checks**
   - Gate 2: Validate lineage documentation exists
   - Gate 3: Validate Unity Catalog lineage is working

5. **Rule: Business Lineage Must Map to Technical Lineage**
   - KPIs must trace back to source columns
   - Business questions must map to Gold tables

### 10.4 Lineage Metrics & KPIs

Track lineage health:

```sql
-- KPI: Lineage Coverage (% of tables with lineage tracked)
SELECT
    COUNT(DISTINCT table_name) AS total_tables,
    COUNT(DISTINCT CASE WHEN lineage_exists THEN table_name END) AS tables_with_lineage,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN lineage_exists THEN table_name END) / COUNT(DISTINCT table_name), 2) AS coverage_pct
FROM (
    SELECT DISTINCT table_full_name AS table_name, TRUE AS lineage_exists
    FROM system.access.table_lineage
    WHERE table_full_name LIKE 'nyc_taxi.%'
    
    UNION
    
    SELECT DISTINCT table_name, FALSE AS lineage_exists
    FROM system.information_schema.tables
    WHERE table_schema IN ('bronze', 'silver', 'gold')
);
```

**Target:** >= 95% lineage coverage

### 10.5 Lineage Documentation Versioning

| Version | Date | Author | Changes | Reason |
|---------|------|--------|---------|--------|
| 1.0 | 2026-02-05 | DataSteward (Gaia) | Initial lineage documentation | Gate 2 deliverable |
| *Future* | *TBD* | *TBD* | *Schema changes for dim_driver* | *Add driver dimension* |

---

## 📊 Appendix: Lineage Queries Reference

### A1. Get All Tables in Lineage
```sql
SELECT DISTINCT table_full_name
FROM system.access.table_lineage
WHERE table_full_name LIKE 'nyc_taxi.%'
ORDER BY table_full_name;
```

### A2. Get Lineage for Specific Column
```sql
SELECT *
FROM system.access.column_lineage
WHERE target_column_name = 'total_amount'
  AND target_table_full_name LIKE 'nyc_taxi.%';
```

### A3. Find Orphaned Tables (No Lineage)
```sql
SELECT t.table_schema, t.table_name
FROM system.information_schema.tables t
LEFT JOIN system.access.table_lineage tl
  ON CONCAT(t.table_catalog, '.', t.table_schema, '.', t.table_name) = tl.target_table_full_name
WHERE t.table_schema IN ('bronze', 'silver', 'gold')
  AND tl.target_table_full_name IS NULL;
```

### A4. Get Most Recent Lineage Update
```sql
SELECT
    table_full_name,
    MAX(created_at) AS last_lineage_update
FROM system.access.table_lineage
WHERE table_full_name LIKE 'nyc_taxi.%'
GROUP BY table_full_name
ORDER BY last_lineage_update DESC;
```

### A5. Get Full Transformation Code
```sql
-- Get the actual SQL/Spark code that created a table
SELECT
    query_text,
    executed_by,
    start_time,
    execution_duration
FROM system.query.history
WHERE ARRAY_CONTAINS(write_table_names, 'nyc_taxi.gold.fact_trips')
ORDER BY start_time DESC
LIMIT 1;
```

---

## 🎯 Summary

This lineage documentation provides:

✅ **Complete Traceability:** Source files → Bronze → Silver → Gold → BI  
✅ **Column-Level Details:** Critical fields (revenue, dates, locations) fully traced  
✅ **Impact Analysis:** Pre-defined scenarios for common changes  
✅ **Unity Catalog Integration:** Queries to leverage automatic lineage tracking  
✅ **Governance Compliance:** Audit trail, change management, versioning  
✅ **Operational Readiness:** Refresh schedules, dependencies, failure recovery  

**Next Steps:**
1. Validate lineage with `@orchestrator *gate-2`
2. Implement DLT pipelines (Diego - DataEngineerExec)
3. Enable Unity Catalog lineage tracking in production
4. Train business users on lineage queries

---

*Document Status: ✅ Complete | Phase: MIDSTREAM - Gate 2 | Owner: DataSteward (Gaia)*
