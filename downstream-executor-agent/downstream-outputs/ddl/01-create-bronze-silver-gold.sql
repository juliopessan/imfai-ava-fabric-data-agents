-- Wave pilot DDL package
-- Scope: Bronze, Silver, Gold starter tables

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS bronze.taxi_trips_raw (
  ingestion_ts TIMESTAMP,
  source_file STRING,
  vendor_id STRING,
  pickup_datetime TIMESTAMP,
  dropoff_datetime TIMESTAMP,
  trip_distance DOUBLE,
  fare_amount DOUBLE,
  total_amount DOUBLE
);

CREATE TABLE IF NOT EXISTS silver.taxi_trips_clean (
  trip_id STRING,
  pickup_date DATE,
  vendor_id STRING,
  trip_distance DOUBLE,
  fare_amount DOUBLE,
  total_amount DOUBLE,
  quality_status STRING,
  processed_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold.daily_trip_metrics (
  pickup_date DATE,
  trips_count BIGINT,
  distance_sum DOUBLE,
  fare_sum DOUBLE,
  total_sum DOUBLE,
  refreshed_ts TIMESTAMP
);
