# Star Schema Model Diagram

**Project:** NYC Green Taxi Analytics  
**Model:** Power BI Semantic Model  
**Created:** 2026-02-05  
**Author:** Bianca (BiSemantic)

---

## 📊 Star Schema Visualization

```mermaid
erDiagram
    fact_trips ||--o{ dim_date : "date_sk"
    fact_trips ||--o{ dim_payment : "payment_type_sk"
    fact_trips ||--o{ dim_rate : "rate_code_sk"
    fact_trips ||--o{ dim_trip_type : "trip_type_sk"
    fact_trips ||--o{ dim_location : "pickup_location_sk (active)"
    fact_trips ||--o{ dim_location : "dropoff_location_sk (inactive)"

    fact_trips {
        int64 trip_sk PK "Surrogate key"
        int64 date_sk FK "Date foreign key"
        int64 payment_type_sk FK "Payment type FK"
        int64 rate_code_sk FK "Rate code FK"
        int64 trip_type_sk FK "Trip type FK"
        int64 pickup_location_sk FK "Pickup zone FK"
        int64 dropoff_location_sk FK "Dropoff zone FK"
        decimal total_amount "Total revenue"
        decimal fare_amount "Base fare"
        decimal tip_amount "Tip amount"
        decimal trip_distance "Distance in miles"
        int trip_duration_min "Duration in minutes"
        int passenger_count "Number of passengers"
    }

    dim_date {
        int64 date_sk PK "Surrogate key (YYYYMMDD)"
        date full_date "Calendar date"
        string month_name "Month name"
        string quarter_name "Quarter name"
        int year "Year"
        boolean is_weekend "Weekend flag"
        boolean is_holiday "Holiday flag"
    }

    dim_payment {
        int64 payment_type_sk PK "Surrogate key"
        int payment_type_id NK "Natural key"
        string payment_type_desc "Description"
        boolean is_electronic "Electronic flag"
        boolean is_tracked "Tip tracked flag"
    }

    dim_rate {
        int64 rate_code_sk PK "Surrogate key"
        int rate_code_id NK "Natural key"
        string rate_code_desc "Description"
        boolean is_airport "Airport trip flag"
        boolean is_flat_rate "Flat rate flag"
    }

    dim_trip_type {
        int64 trip_type_sk PK "Surrogate key"
        int trip_type_id NK "Natural key"
        string trip_type_desc "Description"
        boolean is_dispatch "Dispatch flag"
    }

    dim_location {
        int64 location_sk PK "Surrogate key"
        int location_id NK "TLC zone ID"
        string borough "NYC borough"
        string zone_name "Zone name"
        string service_zone "Service zone type"
        decimal latitude "Latitude"
        decimal longitude "Longitude"
    }
```

---

## 🔗 Relationships Summary

| # | From Table | From Column | To Table | To Column | Cardinality | Active | Cross-Filter |
|---|------------|-------------|----------|-----------|-------------|--------|--------------|
| 1 | fact_trips | date_sk | dim_date | date_sk | Many:1 | ✅ Yes | Single → |
| 2 | fact_trips | payment_type_sk | dim_payment | payment_type_sk | Many:1 | ✅ Yes | Single → |
| 3 | fact_trips | rate_code_sk | dim_rate | rate_code_sk | Many:1 | ✅ Yes | Single → |
| 4 | fact_trips | trip_type_sk | dim_trip_type | trip_type_sk | Many:1 | ✅ Yes | Single → |
| 5 | fact_trips | pickup_location_sk | dim_location | location_sk | Many:1 | ✅ Yes | Single → |
| 6 | fact_trips | dropoff_location_sk | dim_location | location_sk | Many:1 | ❌ No | Single → |

**Notes:**
- Relationship #6 is **inactive** (role-playing dimension) - use `USERELATIONSHIP()` in DAX for dropoff analysis
- All relationships use **single-direction** cross-filtering for optimal performance
- All relationships rely on **referential integrity** (guaranteed by Gold layer ETL)

---

## 📐 Model Architecture

### Fact Table: fact_trips
- **Type:** Transaction Fact
- **Grain:** One row per taxi trip
- **Row Count:** ~238,000 (Q2-Q3 2021)
- **Partitioning:** Monthly by date_sk
- **Optimization:** Z-ORDER on date_sk, payment_type_sk, pickup_location_sk
- **Storage Mode:** DirectQuery (recommended) or Import

**Key Measures:**
- Additive: total_amount, fare_amount, tip_amount, tolls_amount, etc.
- Semi-Additive: passenger_count (sum), trip_distance (sum)
- Derived: revenue_per_mile, revenue_per_minute, tip_percentage

### Dimensions

#### dim_date (Type 0 - Static)
- **Grain:** One calendar day
- **Row Count:** 1,826 (2021-2025)
- **Key Feature:** Calendar Hierarchy (Year → Quarter → Month → Date)
- **Role:** Date table for time intelligence (TOTALYTD, SAMEPERIODLASTYEAR, etc.)

#### dim_payment (Type 1 - Overwrite)
- **Grain:** One payment type
- **Row Count:** 6 (Credit, Cash, No charge, Dispute, Unknown, Voided)
- **Key Feature:** is_electronic flag for tip tracking analysis

#### dim_rate (Type 1 - Overwrite)
- **Grain:** One rate code
- **Row Count:** 7 (Standard, JFK, Newark, Nassau, Negotiated, Group)
- **Key Feature:** is_airport flag for airport trip analysis

#### dim_trip_type (Type 1 - Overwrite)
- **Grain:** One trip type
- **Row Count:** 3 (Street-hail, Dispatch)
- **Key Feature:** is_dispatch flag for channel analysis

#### dim_location (Type 1 - Overwrite - Role-Playing)
- **Grain:** One NYC taxi zone
- **Row Count:** 265 (all TLC zones)
- **Key Feature:** Geographic Hierarchy (Borough → Service Zone → Zone)
- **Role-Playing:** Used twice (pickup and dropoff)

---

## 🎯 Hierarchies

### Calendar Hierarchy (dim_date)
```
Year (e.g., 2021)
└── Quarter (e.g., Q2)
    └── Month (e.g., April)
        └── Date (e.g., 2021-04-15)
```

### Geographic Hierarchy (dim_location)
```
Borough (e.g., Manhattan)
└── Service Zone (e.g., Yellow Zone)
    └── Zone (e.g., Upper East Side North)
```

---

## 📊 Usage Examples

### Analyze Revenue by Month and Payment Type
```
Rows: dim_date[month_name]
Columns: dim_payment[payment_type_desc]
Values: [Total Revenue]
Filters: dim_date[year] = 2021
```

### Top 10 Pickup Zones by Trip Count
```
Visual: Table
Columns: dim_location[zone_name], [Total Trips], [Total Revenue]
Filters: TOPN(10, dim_location[zone_name], [Total Trips])
Relationship: Active (pickup_location_sk)
```

### Airport vs Non-Airport Trip Revenue
```
Visual: Pie Chart
Legend: dim_rate[is_airport]
Values: [Total Revenue]
```

### Weekday vs Weekend Trip Patterns
```
Rows: dim_date[is_weekend]
Columns: dim_date[day_name]
Values: [Total Trips], [Avg Revenue Per Trip]
```

---

## 🔄 Role-Playing Dimension Pattern

**dim_location** is used twice in the model:

### Active Relationship (Pickup)
```dax
// Automatically uses pickup_location_sk relationship
Total Trips by Pickup Zone = 
CALCULATE([Total Trips])
```

### Inactive Relationship (Dropoff)
```dax
// Must use USERELATIONSHIP for dropoff analysis
Total Trips by Dropoff Zone = 
CALCULATE(
    [Total Trips],
    USERELATIONSHIP(fact_trips[dropoff_location_sk], dim_location[location_sk])
)
```

---

## ✅ Model Quality Checklist

- [x] **Star Schema Structure** - No snowflaking, clean 1 fact + 5 dimensions
- [x] **Single-Direction Relationships** - All relationships filter one way for performance
- [x] **Surrogate Keys** - All dimensions use integer surrogate keys
- [x] **Date Table Marked** - dim_date marked as date table for time intelligence
- [x] **Hierarchies Defined** - Calendar and Geographic hierarchies for drill-down
- [x] **No Circular Dependencies** - All relationships form a proper star
- [x] **Role-Playing Handled** - Inactive relationship for dropoff with USERELATIONSHIP
- [x] **Referential Integrity** - All FKs guaranteed by upstream Gold layer ETL

---

## 📏 Model Statistics

| Metric | Value |
|--------|-------|
| **Total Tables** | 6 (1 fact + 5 dimensions) |
| **Total Columns** | 54 |
| **Total Relationships** | 6 (5 active + 1 inactive) |
| **Total Hierarchies** | 3 |
| **Total Measures** | 25+ DAX measures |
| **Estimated Size (Import)** | ~50 MB compressed |
| **Query Performance Target** | <2 seconds (95th percentile) |

---

## 🔧 Performance Optimizations

1. **Relationship Optimization**
   - Single-direction cross-filtering reduces query complexity
   - Referential integrity enabled for query optimization

2. **Partitioning**
   - Fact table partitioned monthly for incremental refresh
   - Dimensions fully loaded (small size)

3. **Data Types**
   - Integer keys for optimal join performance
   - Decimal(10,2) for financial columns (exact precision)

4. **Aggregations**
   - Separate `fact_trips_daily_summary` table for dashboard performance (future)

5. **Calculated Columns**
   - Minimized - use DAX measures instead for better performance

---

**Last Updated:** 2026-02-05  
**Version:** 1.0
