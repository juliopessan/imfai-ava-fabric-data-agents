# Data Dictionary

**Project:** NYC Green Taxi Analytics  
**Model:** Power BI Semantic Model  
**Created:** 2026-02-05  
**Author:** Bianca (BiSemantic)

---

## Table of Contents

1. [fact_trips](#fact_trips)
2. [dim_date](#dim_date)
3. [dim_payment](#dim_payment)
4. [dim_rate](#dim_rate)
5. [dim_trip_type](#dim_trip_type)
6. [dim_location](#dim_location)

---

## fact_trips

**Table Type:** Fact (Transaction)  
**Grain:** One row per taxi trip  
**Row Count:** ~238,000  
**Source:** `gold.fact_trips`

### Columns

| Column | Data Type | Format | Nullable | Description | Business Rule |
|--------|-----------|--------|----------|-------------|---------------|
| **trip_sk** | INT64 | #,0 | No | Surrogate key (auto-generated) | Primary key, hidden in reports |
| **trip_id** | INT64 | #,0 | No | Natural key from source system | Unique identifier, hidden |
| **date_sk** | INT64 | #,0 | No | Foreign key to dim_date | Format: YYYYMMDD, hidden |
| **payment_type_sk** | INT64 | #,0 | Yes | Foreign key to dim_payment | Hidden, use dimension desc |
| **rate_code_sk** | INT64 | #,0 | Yes | Foreign key to dim_rate | Hidden, use dimension desc |
| **trip_type_sk** | INT64 | #,0 | Yes | Foreign key to dim_trip_type | Hidden, use dimension desc |
| **pickup_location_sk** | INT64 | #,0 | Yes | Foreign key to dim_location (pickup) | Active relationship |
| **dropoff_location_sk** | INT64 | #,0 | Yes | Foreign key to dim_location (dropoff) | Inactive relationship |
| **vendor_id** | INT64 | #,0 | Yes | Vendor providing service | 1=Creative Mobile, 2=VeriFone |
| **passenger_count** | INT64 | #,0 | Yes | Number of passengers in trip | Valid range: 1-6 |
| **trip_distance** | DECIMAL(10,2) | #,0.00 | Yes | Trip distance in miles | Must be ≥ 0 |
| **trip_duration_min** | INT64 | #,0 | Yes | Trip duration in minutes | Calculated: dropoff - pickup |
| **fare_amount** | DECIMAL(10,2) | $#,0.00 | Yes | Base fare charged | Must be ≥ 0 |
| **extra_amount** | DECIMAL(10,2) | $#,0.00 | Yes | Extra charges (rush hour, overnight) | $0.50 rush, $1.00 overnight |
| **mta_tax** | DECIMAL(10,2) | $#,0.00 | Yes | MTA tax | Fixed $0.50 per trip |
| **tip_amount** | DECIMAL(10,2) | $#,0.00 | Yes | Tip amount | Only tracked for credit card |
| **tolls_amount** | DECIMAL(10,2) | $#,0.00 | Yes | Toll charges | Actual tolls paid |
| **improvement_surcharge** | DECIMAL(10,2) | $#,0.00 | Yes | Improvement surcharge | Fixed $0.30 per trip |
| **congestion_surcharge** | DECIMAL(10,2) | $#,0.00 | Yes | Congestion surcharge | $2.75 for Manhattan pickups |
| **total_amount** | DECIMAL(10,2) | $#,0.00 | Yes | Total trip cost | Sum of all amounts |
| **revenue_per_mile** | DECIMAL(10,4) | $#,0.0000 | Yes | Revenue efficiency metric | total_amount / trip_distance |
| **revenue_per_minute** | DECIMAL(10,4) | $#,0.0000 | Yes | Revenue efficiency metric | total_amount / trip_duration_min |
| **tip_percentage** | DECIMAL(5,2) | 0.00% | Yes | Tip as % of fare | tip_amount / fare_amount * 100 |

### Key Measures (DAX)

| Measure Name | Formula | Format | Display Folder |
|--------------|---------|--------|----------------|
| **Total Trips** | `COUNTROWS(fact_trips)` | #,0 | Key Metrics |
| **Total Revenue** | `SUM(fact_trips[total_amount])` | $#,0.00 | Financial |
| **Avg Revenue Per Trip** | `DIVIDE([Total Revenue], [Total Trips])` | $#,0.00 | Financial |
| **Total Passengers** | `SUM(fact_trips[passenger_count])` | #,0 | Operational |
| **Total Distance (Miles)** | `SUM(fact_trips[trip_distance])` | #,0.00 | Operational |
| **Total Duration (Minutes)** | `SUM(fact_trips[trip_duration_min])` | #,0 | Operational |
| **Total Tips** | `SUM(fact_trips[tip_amount])` | $#,0.00 | Financial |
| **Avg Tip Percentage** | `DIVIDE(SUM([tip_amount]), SUM([fare_amount]), 0)` | 0.00% | Financial |
| **Revenue Per Mile** | `DIVIDE([Total Revenue], [Total Distance (Miles)], 0)` | $#,0.00 | Efficiency |
| **Revenue Per Minute** | `DIVIDE([Total Revenue], [Total Duration (Minutes)], 0)` | $#,0.00 | Efficiency |
| **Total Revenue YTD** | `TOTALYTD([Total Revenue], dim_date[full_date])` | $#,0.00 | Time Intelligence |
| **Revenue Growth YoY** | `DIVIDE([Total Revenue] - [Total Revenue PY], [Total Revenue PY], 0)` | 0.00% | Time Intelligence |

---

## dim_date

**Table Type:** Dimension (Type 0 - Static)  
**Grain:** One calendar day  
**Row Count:** 1,826 (2021-2025)  
**Source:** `gold.dim_date`

### Columns

| Column | Data Type | Format | Nullable | Description | Example |
|--------|-----------|--------|----------|-------------|---------|
| **date_sk** | INT64 | #,0 | No | Surrogate key in YYYYMMDD format | 20210415 |
| **full_date** | DATE | Short Date | No | Calendar date | 2021-04-15 |
| **day_of_week** | INT64 | #,0 | No | Day of week number | 1=Sunday, 7=Saturday |
| **day_name** | STRING | - | No | Day name | Monday, Tuesday, etc. |
| **day_of_month** | INT64 | #,0 | No | Day of month | 1-31 |
| **day_of_year** | INT64 | #,0 | No | Day of year | 1-366 |
| **week_of_year** | INT64 | #,0 | No | ISO week number | 1-53 |
| **month_num** | INT64 | #,0 | No | Month number | 1-12 |
| **month_name** | STRING | - | No | Month name | January, February, etc. |
| **month_short** | STRING | - | No | Month abbreviation | Jan, Feb, etc. |
| **quarter** | INT64 | #,0 | No | Quarter number | 1-4 |
| **quarter_name** | STRING | - | No | Quarter name | Q1, Q2, Q3, Q4 |
| **year** | INT64 | #,0 | No | Year | 2021, 2022, etc. |
| **year_month** | STRING | - | No | Year-Month format | 2021-04 |
| **is_weekend** | BOOLEAN | TRUE/FALSE | No | Weekend flag | TRUE if Sat/Sun |
| **is_holiday** | BOOLEAN | TRUE/FALSE | No | US holiday flag | TRUE if federal holiday |
| **holiday_name** | STRING | - | Yes | Holiday name | New Year's Day, etc. |

### Hierarchies

**Calendar Hierarchy:**
- Year → Quarter → Month → Date

**Fiscal Hierarchy:**
- Fiscal Year → Fiscal Quarter → Month

### Key Measures

| Measure Name | Formula | Display Folder |
|--------------|---------|----------------|
| **Days in Period** | `COUNTROWS(dim_date)` | Date Intelligence |
| **First Date in Selection** | `MIN(dim_date[full_date])` | Date Intelligence |
| **Last Date in Selection** | `MAX(dim_date[full_date])` | Date Intelligence |

---

## dim_payment

**Table Type:** Dimension (Type 1 - Overwrite)  
**Grain:** One payment type  
**Row Count:** 6  
**Source:** `gold.dim_payment`

### Columns

| Column | Data Type | Format | Nullable | Description | Values |
|--------|-----------|--------|----------|-------------|--------|
| **payment_type_sk** | INT64 | #,0 | No | Surrogate key | 1-6 |
| **payment_type_id** | INT64 | #,0 | No | Natural key from source | 1-6 |
| **payment_type_desc** | STRING | - | No | Payment method description | See reference data below |
| **is_electronic** | BOOLEAN | TRUE/FALSE | No | Electronic payment flag | TRUE for credit card |
| **is_tracked** | BOOLEAN | TRUE/FALSE | No | Tip tracking flag | TRUE if tips tracked |

### Reference Data

| SK | ID | Description | is_electronic | is_tracked |
|----|----|-------------|---------------|------------|
| 1 | 1 | Credit card | TRUE | TRUE |
| 2 | 2 | Cash | FALSE | FALSE |
| 3 | 3 | No charge | FALSE | FALSE |
| 4 | 4 | Dispute | FALSE | FALSE |
| 5 | 5 | Unknown | FALSE | FALSE |
| 6 | 6 | Voided trip | FALSE | FALSE |

---

## dim_rate

**Table Type:** Dimension (Type 1 - Overwrite)  
**Grain:** One rate code  
**Row Count:** 7  
**Source:** `gold.dim_rate`

### Columns

| Column | Data Type | Format | Nullable | Description | Business Rule |
|--------|-----------|--------|----------|-------------|---------------|
| **rate_code_sk** | INT64 | #,0 | No | Surrogate key | 1-7 |
| **rate_code_id** | INT64 | #,0 | No | Natural key from source | 1-7 |
| **rate_code_desc** | STRING | - | No | Rate type description | See reference data |
| **is_airport** | BOOLEAN | TRUE/FALSE | No | Airport trip flag | TRUE for JFK, Newark |
| **is_flat_rate** | BOOLEAN | TRUE/FALSE | No | Flat rate flag | TRUE for negotiated |

### Reference Data

| SK | ID | Description | is_airport | is_flat_rate |
|----|----|-------------|------------|--------------|
| 1 | 1 | Standard rate | FALSE | FALSE |
| 2 | 2 | JFK | TRUE | TRUE |
| 3 | 3 | Newark | TRUE | FALSE |
| 4 | 4 | Nassau or Westchester | FALSE | FALSE |
| 5 | 5 | Negotiated fare | FALSE | TRUE |
| 6 | 6 | Group ride | FALSE | FALSE |

---

## dim_trip_type

**Table Type:** Dimension (Type 1 - Overwrite)  
**Grain:** One trip type  
**Row Count:** 3  
**Source:** `gold.dim_trip_type`

### Columns

| Column | Data Type | Format | Nullable | Description | Values |
|--------|-----------|--------|----------|-------------|--------|
| **trip_type_sk** | INT64 | #,0 | No | Surrogate key | 1-3 |
| **trip_type_id** | INT64 | #,0 | No | Natural key from source | 1-2 |
| **trip_type_desc** | STRING | - | No | Trip type description | See reference data |
| **is_dispatch** | BOOLEAN | TRUE/FALSE | No | Dispatch flag | TRUE for app-based |

### Reference Data

| SK | ID | Description | is_dispatch |
|----|----|-------------|-------------|
| 1 | 1 | Street-hail | FALSE |
| 2 | 2 | Dispatch | TRUE |

---

## dim_location

**Table Type:** Dimension (Type 1 - Overwrite)  
**Grain:** One NYC taxi zone  
**Row Count:** 265  
**Source:** `gold.dim_location`

### Columns

| Column | Data Type | Format | Nullable | Description | Example |
|--------|-----------|--------|----------|-------------|---------|
| **location_sk** | INT64 | #,0 | No | Surrogate key | 1-265 |
| **location_id** | INT64 | #,0 | No | TLC zone ID (natural key) | 1-263 |
| **borough** | STRING | - | No | NYC borough | Manhattan, Brooklyn, Queens, Bronx, Staten Island |
| **zone_name** | STRING | - | No | Zone name | Upper East Side North, JFK Airport, etc. |
| **service_zone** | STRING | - | No | Service zone type | Yellow Zone, Boro Zone, Airports, EWR |
| **latitude** | DECIMAL(9,6) | #,0.000000 | Yes | Latitude coordinate | 40.767937 |
| **longitude** | DECIMAL(9,6) | #,0.000000 | Yes | Longitude coordinate | -73.982155 |

### Hierarchies

**Geographic Hierarchy:**
- Borough → Service Zone → Zone

### Reference Data (Sample)

| Zone ID | Borough | Zone Name | Service Zone |
|---------|---------|-----------|--------------|
| 4 | Manhattan | Alphabet City | Yellow Zone |
| 13 | Manhattan | Battery Park | Yellow Zone |
| 132 | JFK Airport | Jamaica Bay | Airports |
| 237 | Manhattan | Upper East Side North | Yellow Zone |
| 138 | Queens | LaGuardia Airport | Airports |

---

## Data Quality Notes

### Nullability
- All foreign keys (SK columns) are **nullable** to handle missing reference data
- All dimension natural keys (ID columns) are **NOT NULL**
- Financial columns are nullable but defaulted to 0.00 in ETL

### Data Types
- **INT64** used for all keys and counts for optimal performance
- **DECIMAL(10,2)** for financial amounts (exact precision, no floating point errors)
- **DECIMAL(10,4)** for calculated ratios (revenue per mile/minute)
- **BOOLEAN** for all flag columns
- **DATE** for dim_date.full_date (time intelligence compatibility)

### Formatting Standards
- Currency: `$#,0.00;($#,0.00);$#,0.00`
- Percentage: `0.00%;-0.00%;0.00%`
- Integer: `#,0`
- Decimal: `#,0.00`

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-05 | 1.0 | Initial data dictionary | Bianca (BiSemantic) |

---

**Last Updated:** 2026-02-05
