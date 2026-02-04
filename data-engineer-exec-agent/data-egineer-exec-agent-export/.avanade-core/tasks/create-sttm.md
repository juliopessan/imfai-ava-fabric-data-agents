---
task: create-sttm
version: 1.0
elicit: true
description: Create Source-to-Target Mapping documentation for data pipelines
---

# Create Source-to-Target Mapping (STTM)

## Purpose
Generate comprehensive Source-to-Target Mapping documentation that defines how data flows from source systems to target tables, including transformation rules, business logic, and data quality requirements.

## Process

### Step 1: Gather STTM Requirements
ASK the user:

1. **Source Systems**: What are the source systems/files?
2. **Target Tables**: What are the destination tables?
3. **Transformation Rules**: Any specific business rules?
4. **Data Types**: Source vs target type mappings?
5. **Lookup Tables**: Any reference data for enrichment?
6. **Aggregation Logic**: Any grouping/summarization?

### Step 2: Document Source Analysis

**Source System Profile:**
```markdown
## Source System: {SOURCE_NAME}

### System Information
| Attribute | Value |
|-----------|-------|
| **System Name** | {source_system_name} |
| **System Type** | File / Database / API / Stream |
| **Connection** | {connection_string_pattern} |
| **Format** | CSV / Parquet / JSON / Database Table |
| **Encoding** | UTF-8 / Latin1 / etc. |
| **Delimiter** | Comma / Tab / Pipe |
| **Header Row** | Yes / No |
| **Quote Character** | " / ' / None |

### Source Schema
| # | Column Name | Data Type | Sample Values | Notes |
|---|-------------|-----------|---------------|-------|
| 1 | vendor_id | STRING | "1", "2" | Vendor identifier |
| 2 | pickup_datetime | STRING | "2021-04-01 00:15:32" | ISO format |
| 3 | fare_amount | STRING | "15.50", "22.00" | Currency as string |
```

### Step 3: Create STTM Matrix

**STTM Document Template:**
```markdown
# Source-to-Target Mapping

## Document Information
| Attribute | Value |
|-----------|-------|
| **Project** | {project_name} |
| **Version** | 1.0 |
| **Author** | {author_name} |
| **Created** | {date} |
| **Last Updated** | {date} |
| **Status** | Draft / In Review / Approved |

---

## Mapping: {SOURCE} → {TARGET}

### Overview
| Attribute | Value |
|-----------|-------|
| **Source System** | {source_system} |
| **Source Object** | {source_table_or_file} |
| **Target Schema** | {target_schema} |
| **Target Table** | {target_table} |
| **Load Type** | Full / Incremental / CDC |
| **Load Frequency** | Daily / Hourly / Real-time |
| **Primary Key** | {pk_columns} |
| **Incremental Key** | {date_column} (for incremental loads) |

### Column Mappings

| # | Source Column | Source Type | Target Column | Target Type | Transformation Rule | Nullable | Default | Notes |
|---|---------------|-------------|---------------|-------------|---------------------|----------|---------|-------|
| 1 | vendor_id | VARCHAR | vendor_id | INT | CAST(vendor_id AS INT) | NO | - | Direct type conversion |
| 2 | lpep_pickup_datetime | VARCHAR | pickup_datetime | TIMESTAMP | TO_TIMESTAMP(lpep_pickup_datetime, 'YYYY-MM-DD HH24:MI:SS') | NO | - | Parse string to timestamp |
| 3 | lpep_dropoff_datetime | VARCHAR | dropoff_datetime | TIMESTAMP | TO_TIMESTAMP(lpep_dropoff_datetime, 'YYYY-MM-DD HH24:MI:SS') | NO | - | Parse string to timestamp |
| 4 | - | - | trip_duration_minutes | INT | DATEDIFF(minute, pickup_datetime, dropoff_datetime) | NO | - | **Derived**: Calculate from pickup/dropoff |
| 5 | passenger_count | VARCHAR | passenger_count | INT | CAST(passenger_count AS INT) | YES | NULL | Allow nulls |
| 6 | trip_distance | VARCHAR | trip_distance | DECIMAL(10,2) | CAST(trip_distance AS DECIMAL(10,2)) | YES | 0.00 | Default to 0 if null |
| 7 | rate_code_id | VARCHAR | rate_code_id | INT | CAST(rate_code_id AS INT) | YES | 1 | Default to standard rate |
| 8 | - | - | rate_code_desc | VARCHAR(100) | LOOKUP: REF.rate_code.description | YES | 'Unknown' | **Lookup** from reference table |
| 9 | payment_type | VARCHAR | payment_type_id | INT | CAST(payment_type AS INT) | NO | - | Direct type conversion |
| 10 | - | - | payment_type_desc | VARCHAR(100) | LOOKUP: REF.payment_type.description | YES | 'Unknown' | **Lookup** from reference table |
| 11 | fare_amount | VARCHAR | fare_amount | DECIMAL(10,2) | CAST(fare_amount AS DECIMAL(10,2)) | YES | 0.00 | - |
| 12 | - | - | total_amount | DECIMAL(10,2) | fare_amount + extra + mta_tax + tip_amount + tolls_amount + improvement_surcharge | NO | - | **Calculated**: Sum of all charges |
| 13 | - | - | quality_flag | VARCHAR(50) | CASE WHEN valid THEN 'VALID' ELSE 'INVALID' END | NO | 'INVALID' | **Derived**: Based on validation rules |
| 14 | - | - | load_timestamp | TIMESTAMP | CURRENT_TIMESTAMP | NO | CURRENT_TIMESTAMP | **System**: Auto-generated |
| 15 | - | - | source_file | VARCHAR(500) | INPUT_FILE_NAME() | NO | - | **System**: Source file tracking |
```

### Step 4: Document Transformation Rules

**Transformation Rules Detail:**
```markdown
### Transformation Rules

#### TR-001: Date/Time Parsing
- **Rule ID**: TR-001
- **Source**: lpep_pickup_datetime (VARCHAR)
- **Target**: pickup_datetime (TIMESTAMP)
- **Logic**: 
  ```sql
  TO_TIMESTAMP(lpep_pickup_datetime, 'YYYY-MM-DD HH24:MI:SS')
  ```
- **Handling**: If parse fails, set quality_flag = 'INVALID'
- **Example**: "2021-04-01 00:15:32" → 2021-04-01 00:15:32.000

#### TR-002: Trip Duration Calculation
- **Rule ID**: TR-002
- **Source**: pickup_datetime, dropoff_datetime
- **Target**: trip_duration_minutes (INT)
- **Logic**:
  ```sql
  DATEDIFF(minute, pickup_datetime, dropoff_datetime)
  ```
- **Validation**: Must be >= 0 and <= 1440 (24 hours)
- **Example**: pickup=10:00, dropoff=10:30 → 30 minutes

#### TR-003: Lookup Enrichment - Rate Code
- **Rule ID**: TR-003
- **Source**: rate_code_id (INT)
- **Target**: rate_code_desc (VARCHAR)
- **Logic**:
  ```sql
  LEFT JOIN REF.rate_code rc ON s.rate_code_id = rc.rate_code_id
  COALESCE(rc.description, 'Unknown')
  ```
- **Lookup Table**: REF.rate_code
- **Default**: 'Unknown' if not found

#### TR-004: Total Amount Calculation
- **Rule ID**: TR-004
- **Source**: Multiple amount columns
- **Target**: total_amount (DECIMAL)
- **Logic**:
  ```sql
  COALESCE(fare_amount, 0) + 
  COALESCE(extra, 0) + 
  COALESCE(mta_tax, 0) + 
  COALESCE(tip_amount, 0) + 
  COALESCE(tolls_amount, 0) + 
  COALESCE(improvement_surcharge, 0)
  ```
- **Validation**: Result must be >= 0

#### TR-005: Quality Flag Assignment
- **Rule ID**: TR-005
- **Source**: All validation rules
- **Target**: quality_flag (VARCHAR)
- **Logic**:
  ```sql
  CASE 
    WHEN trip_id IS NOT NULL
     AND pickup_datetime IS NOT NULL
     AND dropoff_datetime IS NOT NULL
     AND pickup_datetime < dropoff_datetime
     AND fare_amount >= 0
     AND passenger_count BETWEEN 1 AND 9
    THEN 'VALID'
    ELSE 'INVALID'
  END
  ```
```

### Step 5: Document Filter and Join Conditions

**Filter Conditions:**
```markdown
### Filter Conditions

| Filter ID | Description | SQL Condition | Applied At |
|-----------|-------------|---------------|------------|
| F-001 | Exclude future dates | pickup_datetime <= CURRENT_TIMESTAMP | Silver layer |
| F-002 | Exclude test records | vendor_id NOT IN (99, 0) | Silver layer |
| F-003 | Valid records only | quality_flag = 'VALID' | Gold layer |
| F-004 | Date range filter | pickup_datetime >= '2021-04-01' | Incremental load |
```

**Join Conditions:**
```markdown
### Join Conditions

| Join ID | Left Table | Right Table | Join Type | Join Condition | Notes |
|---------|------------|-------------|-----------|----------------|-------|
| J-001 | SILVER.trip_data | REF.rate_code | LEFT | trip.rate_code_id = ref.rate_code_id | Rate code enrichment |
| J-002 | SILVER.trip_data | REF.payment_type | LEFT | trip.payment_type_id = ref.payment_type_id | Payment type enrichment |
| J-003 | SILVER.trip_data | REF.vendor | LEFT | trip.vendor_id = ref.vendor_id | Vendor name enrichment |
```

### Step 6: Document Aggregation Rules

**Aggregation Mappings (for Gold Aggregated Tables):**
```markdown
### Aggregation Rules: GOLD.daily_trip_summary

| # | Target Column | Aggregation Type | Source Expression | Group By |
|---|---------------|------------------|-------------------|----------|
| 1 | trip_date | GROUP KEY | DATE(pickup_datetime) | ✓ |
| 2 | vendor_id | GROUP KEY | vendor_id | ✓ |
| 3 | total_trips | COUNT | COUNT(*) | - |
| 4 | total_passengers | SUM | SUM(passenger_count) | - |
| 5 | total_distance | SUM | SUM(trip_distance) | - |
| 6 | total_fare | SUM | SUM(fare_amount) | - |
| 7 | total_revenue | SUM | SUM(total_amount) | - |
| 8 | avg_fare | AVG | AVG(fare_amount) | - |
| 9 | avg_trip_distance | AVG | AVG(trip_distance) | - |
| 10 | avg_trip_duration | AVG | AVG(trip_duration_minutes) | - |
| 11 | min_fare | MIN | MIN(fare_amount) | - |
| 12 | max_fare | MAX | MAX(fare_amount) | - |

**SQL Implementation:**
```sql
INSERT INTO GOLD.daily_trip_summary
SELECT 
    DATE(pickup_datetime) as trip_date,
    vendor_id,
    COUNT(*) as total_trips,
    SUM(passenger_count) as total_passengers,
    SUM(trip_distance) as total_distance,
    SUM(fare_amount) as total_fare,
    SUM(total_amount) as total_revenue,
    AVG(fare_amount) as avg_fare,
    AVG(trip_distance) as avg_trip_distance,
    AVG(trip_duration_minutes) as avg_trip_duration,
    MIN(fare_amount) as min_fare,
    MAX(fare_amount) as max_fare,
    CURRENT_TIMESTAMP as created_timestamp
FROM SILVER.trip_data
WHERE quality_flag = 'VALID'
GROUP BY DATE(pickup_datetime), vendor_id;
```
```

### Step 7: Generate STTM Artifacts

**Output Structure:**
```
sttm/
├── README.md                           # STTM overview and index
├── mappings/
│   ├── STTM_CSV_to_Landing.md         # CSV → LND mapping
│   ├── STTM_Parquet_to_Landing.md     # Parquet → LND mapping
│   ├── STTM_Landing_to_Silver.md      # LND → SILVER mapping
│   ├── STTM_Silver_to_Gold_Enriched.md    # SILVER → GOLD enriched
│   └── STTM_Silver_to_Gold_Aggregated.md  # SILVER → GOLD aggregated
├── transformation-rules/
│   ├── type-conversions.md            # All type conversion rules
│   ├── calculated-fields.md           # Derived field logic
│   ├── lookups.md                     # Lookup table references
│   └── aggregations.md                # Aggregation rules
├── validation-rules/
│   └── quality-rules.md               # Data quality rules
└── exports/
    ├── sttm-matrix.xlsx               # Excel export
    └── sttm-matrix.csv                # CSV export
```

## Output

Generate the following artifacts:

1. **STTM Documents** (Markdown)
   - One document per source-to-target flow
   - Complete column mappings
   - Transformation rules

2. **Transformation Catalog** (Markdown)
   - All transformation rules indexed
   - Reusable rule definitions

3. **Excel/CSV Export**
   - Machine-readable mapping matrix
   - Import-ready format

## Completion Criteria

STTM is complete when:
- ✅ All source columns mapped to targets
- ✅ All transformations documented with examples
- ✅ Lookup tables identified and documented
- ✅ Aggregation rules defined
- ✅ Filter conditions specified
- ✅ Join conditions documented
- ✅ Data types explicitly defined
- ✅ Nullable/default values specified
