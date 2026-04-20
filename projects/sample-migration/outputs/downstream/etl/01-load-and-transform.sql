-- Wave pilot ETL package
-- Scope: Bronze -> Silver -> Gold

INSERT INTO bronze.taxi_trips_raw
SELECT
  current_timestamp() AS ingestion_ts,
  source_file,
  vendor_id,
  pickup_datetime,
  dropoff_datetime,
  trip_distance,
  fare_amount,
  total_amount
FROM source_staging.taxi_trips_batch;

INSERT INTO silver.taxi_trips_clean
SELECT
  sha2(concat_ws('|', cast(pickup_datetime AS STRING), cast(dropoff_datetime AS STRING), vendor_id), 256) AS trip_id,
  CAST(pickup_datetime AS DATE) AS pickup_date,
  vendor_id,
  trip_distance,
  fare_amount,
  total_amount,
  CASE
    WHEN trip_distance >= 0 AND total_amount >= 0 THEN 'valid'
    ELSE 'invalid'
  END AS quality_status,
  current_timestamp() AS processed_ts
FROM bronze.taxi_trips_raw
WHERE pickup_datetime IS NOT NULL
  AND dropoff_datetime IS NOT NULL;

INSERT INTO gold.daily_trip_metrics
SELECT
  pickup_date,
  COUNT(*) AS trips_count,
  SUM(trip_distance) AS distance_sum,
  SUM(fare_amount) AS fare_sum,
  SUM(total_amount) AS total_sum,
  current_timestamp() AS refreshed_ts
FROM silver.taxi_trips_clean
WHERE quality_status = 'valid'
GROUP BY pickup_date;
