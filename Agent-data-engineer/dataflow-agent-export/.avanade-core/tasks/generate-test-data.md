---
task: generate-test-data
version: 1.0
elicit: true
description: Generate synthetic/mock data for testing data pipelines
---

# Generate Test Data

## Purpose
Create realistic synthetic data for testing data pipelines, including edge cases, boundary conditions, and various data quality scenarios without using production data.

## Process

### Step 1: Gather Test Data Requirements
ASK the user:

1. **Target Schema**: What table schema to generate data for?
2. **Volume**: How many rows needed? (10, 100, 1000, 10000+)
3. **Scenarios**: Normal data, edge cases, invalid data, stress test?
4. **Format**: SQL INSERT, CSV, JSON, Parquet?
5. **Constraints**: Any referential integrity to maintain?
6. **Sensitive Data**: Need to mask/anonymize any fields?

### Step 2: Analyze Schema for Generation

**Extract Schema Information:**
```sql
-- Get table structure for test data generation
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    numeric_precision,
    numeric_scale,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = '{SCHEMA}' AND table_name = '{TABLE}'
ORDER BY ordinal_position;
```

### Step 3: Define Data Generation Rules

**Column Generation Strategies:**
```markdown
## Generation Strategy: {TABLE_NAME}

| Column | Type | Strategy | Parameters | Example Values |
|--------|------|----------|------------|----------------|
| trip_id | BIGINT | SEQUENCE | start=1, increment=1 | 1, 2, 3, ... |
| vendor_id | INT | RANDOM_CHOICE | values=[1,2] | 1, 2 |
| pickup_datetime | TIMESTAMP | RANDOM_DATE | start='2021-04-01', end='2021-06-30' | 2021-05-15 14:30:00 |
| dropoff_datetime | TIMESTAMP | DERIVED | pickup + RANDOM(5,120) minutes | 2021-05-15 15:15:00 |
| passenger_count | INT | WEIGHTED_RANDOM | {1:50%, 2:25%, 3:15%, 4:5%, 5:3%, 6:2%} | 1, 2, 1, 3, ... |
| trip_distance | DECIMAL | RANDOM_RANGE | min=0.5, max=30.0, precision=2 | 5.75, 12.30 |
| rate_code_id | INT | WEIGHTED_RANDOM | {1:85%, 2:5%, 3:3%, 4:2%, 5:5%} | 1, 1, 2, 1, 5 |
| fare_amount | DECIMAL | FORMULA | base_fare + (distance * rate) | 15.50 |
| tip_amount | DECIMAL | CONDITIONAL | IF payment_type=1 THEN RANDOM(0, fare*0.3) ELSE 0 | 4.65, 0.00 |
| payment_type | INT | WEIGHTED_RANDOM | {1:60%, 2:35%, 3:3%, 4:2%} | 1, 2, 1, 1 |
| email | VARCHAR | PATTERN | {firstname}.{lastname}@{domain} | john.doe@email.com |
| phone | VARCHAR | PATTERN | +1-{3digits}-{3digits}-{4digits} | +1-555-123-4567 |
```

### Step 4: Generate SQL INSERT Statements

**SQL Generation Template:**
```sql
-- ============================================
-- Test Data Generation Script
-- Table: {SCHEMA}.{TABLE_NAME}
-- Generated: {timestamp}
-- Records: {count}
-- ============================================

-- Clear existing test data (optional)
-- DELETE FROM {SCHEMA}.{TABLE_NAME} WHERE source_file = 'TEST_DATA';

-- Insert test records
INSERT INTO {SCHEMA}.{TABLE_NAME} (
    trip_id,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code_id,
    payment_type,
    fare_amount,
    tip_amount,
    total_amount,
    source_file,
    load_timestamp
) VALUES
-- Normal Records (80%)
(1, 1, '2021-04-01 08:15:00', '2021-04-01 08:35:00', 1, 5.2, 1, 1, 18.50, 3.70, 25.30, 'TEST_DATA', CURRENT_TIMESTAMP),
(2, 2, '2021-04-01 09:00:00', '2021-04-01 09:45:00', 2, 12.8, 1, 1, 42.00, 8.40, 55.90, 'TEST_DATA', CURRENT_TIMESTAMP),
(3, 1, '2021-04-01 10:30:00', '2021-04-01 10:50:00', 1, 3.5, 1, 2, 12.50, 0.00, 15.80, 'TEST_DATA', CURRENT_TIMESTAMP),

-- Edge Cases (10%)
-- Minimum values
(100, 1, '2021-04-01 00:00:00', '2021-04-01 00:05:00', 1, 0.1, 1, 1, 2.50, 0.50, 6.30, 'TEST_DATA', CURRENT_TIMESTAMP),
-- Maximum values
(101, 2, '2021-04-01 23:59:59', '2021-04-02 01:30:00', 6, 50.0, 2, 1, 150.00, 30.00, 195.80, 'TEST_DATA', CURRENT_TIMESTAMP),
-- Boundary values
(102, 1, '2021-06-30 23:59:59', '2021-07-01 00:30:00', 1, 10.0, 1, 1, 35.00, 7.00, 47.30, 'TEST_DATA', CURRENT_TIMESTAMP),

-- Null Handling (5%)
(200, 1, '2021-04-02 12:00:00', '2021-04-02 12:30:00', NULL, 5.0, 1, 2, 18.00, NULL, 21.30, 'TEST_DATA', CURRENT_TIMESTAMP),
(201, 2, '2021-04-02 14:00:00', '2021-04-02 14:20:00', 2, NULL, 1, 1, 15.00, 3.00, 21.30, 'TEST_DATA', CURRENT_TIMESTAMP),

-- Invalid Records for Quality Testing (5%)
-- Negative fare (should fail validation)
(300, 1, '2021-04-03 10:00:00', '2021-04-03 10:30:00', 1, 5.0, 1, 1, -10.00, 0.00, -6.70, 'TEST_DATA_INVALID', CURRENT_TIMESTAMP),
-- Future date (should fail validation)
(301, 2, '2099-12-31 23:59:59', '2099-12-31 23:59:59', 1, 5.0, 1, 1, 15.00, 3.00, 21.30, 'TEST_DATA_INVALID', CURRENT_TIMESTAMP),
-- Invalid passenger count (should fail validation)
(302, 1, '2021-04-03 11:00:00', '2021-04-03 11:30:00', 99, 5.0, 1, 1, 15.00, 3.00, 21.30, 'TEST_DATA_INVALID', CURRENT_TIMESTAMP),
-- Dropoff before pickup (should fail validation)
(303, 2, '2021-04-03 12:00:00', '2021-04-03 11:00:00', 1, 5.0, 1, 1, 15.00, 3.00, 21.30, 'TEST_DATA_INVALID', CURRENT_TIMESTAMP);

-- Verify inserted records
SELECT 
    source_file,
    COUNT(*) as record_count,
    COUNT(CASE WHEN fare_amount < 0 THEN 1 END) as negative_fares,
    COUNT(CASE WHEN passenger_count IS NULL THEN 1 END) as null_passengers
FROM {SCHEMA}.{TABLE_NAME}
WHERE source_file LIKE 'TEST_DATA%'
GROUP BY source_file;
```

### Step 5: Generate PySpark/Python Test Data

**PySpark Data Generation:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_test_data(spark, num_records=1000, include_invalid=True):
    """Generate synthetic test data for trip table"""
    
    schema = StructType([
        StructField("trip_id", LongType(), False),
        StructField("vendor_id", IntegerType(), False),
        StructField("pickup_datetime", TimestampType(), False),
        StructField("dropoff_datetime", TimestampType(), False),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DecimalType(10, 2), True),
        StructField("rate_code_id", IntegerType(), True),
        StructField("payment_type", IntegerType(), False),
        StructField("fare_amount", DecimalType(10, 2), True),
        StructField("tip_amount", DecimalType(10, 2), True),
        StructField("total_amount", DecimalType(10, 2), True),
        StructField("source_file", StringType(), False),
        StructField("test_scenario", StringType(), False)
    ])
    
    data = []
    
    # Normal records (80%)
    normal_count = int(num_records * 0.80)
    for i in range(normal_count):
        pickup = fake.date_time_between(
            start_date=datetime(2021, 4, 1),
            end_date=datetime(2021, 6, 30)
        )
        duration = random.randint(5, 120)
        dropoff = pickup + timedelta(minutes=duration)
        distance = round(random.uniform(0.5, 30.0), 2)
        fare = round(2.50 + (distance * 2.50), 2)
        payment = random.choices([1, 2, 3, 4], weights=[60, 35, 3, 2])[0]
        tip = round(random.uniform(0, fare * 0.3), 2) if payment == 1 else 0.0
        
        data.append((
            i + 1,
            random.choice([1, 2]),
            pickup,
            dropoff,
            random.choices([1, 2, 3, 4, 5, 6], weights=[50, 25, 15, 5, 3, 2])[0],
            distance,
            random.choices([1, 2, 3, 4, 5], weights=[85, 5, 3, 2, 5])[0],
            payment,
            fare,
            tip,
            round(fare + tip + 3.30, 2),  # total with fees
            'TEST_DATA_NORMAL',
            'NORMAL'
        ))
    
    # Edge cases (10%)
    edge_count = int(num_records * 0.10)
    edge_start = normal_count + 1
    for i in range(edge_count):
        # Various edge case scenarios
        scenario = random.choice(['MIN_VALUES', 'MAX_VALUES', 'BOUNDARY', 'LONG_TRIP', 'SHORT_TRIP'])
        
        if scenario == 'MIN_VALUES':
            data.append((
                edge_start + i, 1,
                datetime(2021, 4, 1, 0, 0, 0),
                datetime(2021, 4, 1, 0, 5, 0),
                1, 0.1, 1, 1, 2.50, 0.50, 6.30,
                'TEST_DATA_EDGE', scenario
            ))
        elif scenario == 'MAX_VALUES':
            data.append((
                edge_start + i, 2,
                datetime(2021, 6, 30, 23, 0, 0),
                datetime(2021, 7, 1, 1, 0, 0),
                6, 99.99, 2, 1, 299.99, 59.99, 375.28,
                'TEST_DATA_EDGE', scenario
            ))
        # ... more scenarios
    
    if include_invalid:
        # Invalid records (10%)
        invalid_count = int(num_records * 0.10)
        invalid_start = edge_start + edge_count
        
        invalid_scenarios = [
            # Negative fare
            (invalid_start, 1, datetime(2021, 4, 1), datetime(2021, 4, 1, 0, 30), 
             1, 5.0, 1, 1, -15.00, 0.0, -11.70, 'TEST_DATA_INVALID', 'NEGATIVE_FARE'),
            # Future date
            (invalid_start + 1, 2, datetime(2099, 12, 31), datetime(2099, 12, 31, 0, 30),
             1, 5.0, 1, 1, 15.00, 3.0, 21.30, 'TEST_DATA_INVALID', 'FUTURE_DATE'),
            # Invalid passenger
            (invalid_start + 2, 1, datetime(2021, 4, 2), datetime(2021, 4, 2, 0, 30),
             99, 5.0, 1, 1, 15.00, 3.0, 21.30, 'TEST_DATA_INVALID', 'INVALID_PASSENGER'),
            # Dropoff before pickup
            (invalid_start + 3, 2, datetime(2021, 4, 3, 12, 0), datetime(2021, 4, 3, 11, 0),
             1, 5.0, 1, 1, 15.00, 3.0, 21.30, 'TEST_DATA_INVALID', 'TIME_TRAVEL'),
        ]
        data.extend(invalid_scenarios)
    
    return spark.createDataFrame(data, schema)

# Generate and save test data
df_test = generate_test_data(spark, num_records=1000)
df_test.write.mode("overwrite").saveAsTable("TEST.trip_data")
```

### Step 6: Generate CSV Test Files

**CSV Generation Script:**
```python
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_csv_test_file(output_path, num_records=1000):
    """Generate a CSV test file with synthetic data"""
    
    headers = [
        'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
        'passenger_count', 'trip_distance', 'RatecodeID',
        'PULocationID', 'DOLocationID', 'payment_type',
        'fare_amount', 'extra', 'mta_tax', 'tip_amount',
        'tolls_amount', 'improvement_surcharge', 'total_amount'
    ]
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(num_records):
            pickup = fake.date_time_between(
                start_date=datetime(2021, 4, 1),
                end_date=datetime(2021, 6, 30)
            )
            duration = random.randint(5, 120)
            dropoff = pickup + timedelta(minutes=duration)
            distance = round(random.uniform(0.5, 30.0), 2)
            fare = round(2.50 + (distance * 2.50), 2)
            payment = random.choices([1, 2, 3, 4], weights=[60, 35, 3, 2])[0]
            tip = round(random.uniform(0, fare * 0.3), 2) if payment == 1 else 0.0
            
            row = [
                random.choice([1, 2]),  # VendorID
                pickup.strftime('%Y-%m-%d %H:%M:%S'),
                dropoff.strftime('%Y-%m-%d %H:%M:%S'),
                random.choices([1, 2, 3, 4, 5, 6], weights=[50, 25, 15, 5, 3, 2])[0],
                distance,
                random.choices([1, 2, 3, 4, 5], weights=[85, 5, 3, 2, 5])[0],
                random.randint(1, 265),  # PULocationID
                random.randint(1, 265),  # DOLocationID
                payment,
                fare,
                round(random.uniform(0, 2.5), 2),  # extra
                0.50,  # mta_tax
                tip,
                round(random.uniform(0, 10), 2),  # tolls
                0.30,  # improvement_surcharge
                round(fare + tip + 3.30, 2)  # total
            ]
            writer.writerow(row)
    
    print(f"Generated {num_records} records to {output_path}")

# Generate test files
generate_csv_test_file('test_data_normal.csv', 800)
generate_csv_test_file('test_data_edge_cases.csv', 100)
generate_csv_test_file('test_data_invalid.csv', 100)
```

### Step 7: Test Scenario Matrix

**Test Scenarios Coverage:**
```markdown
## Test Scenario Matrix

| Scenario ID | Category | Description | Expected Result | Record IDs |
|-------------|----------|-------------|-----------------|------------|
| TS-001 | Normal | Standard trip with all valid values | VALID | 1-800 |
| TS-002 | Edge | Minimum duration trip (5 min) | VALID | 1001 |
| TS-003 | Edge | Maximum distance trip (50 miles) | VALID | 1002 |
| TS-004 | Edge | Boundary date (month end) | VALID | 1003 |
| TS-005 | Edge | 6 passengers (max valid) | VALID | 1004 |
| TS-006 | Null | Null passenger count | VALID (nullable) | 1101 |
| TS-007 | Null | Null trip distance | VALID (nullable) | 1102 |
| TS-008 | Invalid | Negative fare amount | INVALID | 2001 |
| TS-009 | Invalid | Future pickup date | INVALID | 2002 |
| TS-010 | Invalid | Passenger count > 9 | INVALID | 2003 |
| TS-011 | Invalid | Dropoff before pickup | INVALID | 2004 |
| TS-012 | Invalid | Missing required field | INVALID | 2005 |
| TS-013 | Referential | Invalid rate_code_id | WARNING | 2101 |
| TS-014 | Referential | Invalid payment_type | WARNING | 2102 |
| TS-015 | Stress | Large batch (10K records) | VALID | 10001-20000 |
```

## Output

Generate the following artifacts:

1. **SQL Test Data** (SQL)
   - INSERT statements with test scenarios
   - Cleanup scripts
   - Verification queries

2. **CSV Test Files** (CSV)
   - Normal data file
   - Edge case file
   - Invalid data file

3. **Python Generator** (Python)
   - Reusable data generation functions
   - Configurable parameters
   - Faker integration for realistic data

4. **Test Scenario Documentation** (Markdown)
   - Scenario matrix
   - Expected results
   - Test coverage report

## Completion Criteria

Test data is complete when:
- ✅ Normal scenarios covered (80%)
- ✅ Edge cases included (10%)
- ✅ Invalid records for negative testing (10%)
- ✅ Null handling scenarios included
- ✅ Referential integrity scenarios covered
- ✅ Multiple output formats generated
- ✅ Repeatable generation scripts created
