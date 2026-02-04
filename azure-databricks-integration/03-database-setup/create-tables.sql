-- ══════════════════════════════════════════════════════════════════════════════
-- DATABRICKS - CRIAÇÃO DE TABELAS (BASEADO EM GREEN TAXI TRIPS)
-- ══════════════════════════════════════════════════════════════════════════════
-- Descrição: Cria tabelas para pipeline de dados de táxis NYC
-- Autor: Avanade Core - Data Engineering Agents
-- Data: 2026-02-04
-- ══════════════════════════════════════════════════════════════════════════════

-- ══════════════════════════════════════════════════════════════════════════════
-- BRONZE LAYER - Tabelas de ingestão (raw data)
-- ══════════════════════════════════════════════════════════════════════════════

-- Bronze: Trips brutos vindos de CSV
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS bronze.taxi_trips_raw;

CREATE TABLE bronze.taxi_trips_raw (
    -- Identificadores
    vendorid BIGINT COMMENT 'Vendor ID (1=Creative Mobile, 2=VeriFone)',
    
    -- Timestamps
    lpep_pickup_datetime TIMESTAMP COMMENT 'Pickup date and time',
    lpep_dropoff_datetime TIMESTAMP COMMENT 'Dropoff date and time',
    
    -- Localização
    pulocationid BIGINT COMMENT 'Pickup location ID (TLC Taxi Zone)',
    dolocationid BIGINT COMMENT 'Dropoff location ID (TLC Taxi Zone)',
    
    -- Detalhes da viagem
    passenger_count DOUBLE COMMENT 'Number of passengers',
    trip_distance DOUBLE COMMENT 'Trip distance in miles',
    
    -- Taxas e valores
    fare_amount DOUBLE COMMENT 'Base fare amount',
    extra DOUBLE COMMENT 'Extra charges',
    mta_tax DOUBLE COMMENT 'MTA tax ($0.50)',
    tip_amount DOUBLE COMMENT 'Tip amount (credit card only)',
    tolls_amount DOUBLE COMMENT 'Tolls amount',
    improvement_surcharge DOUBLE COMMENT 'Improvement surcharge ($0.30)',
    total_amount DOUBLE COMMENT 'Total amount charged',
    congestion_surcharge DOUBLE COMMENT 'Congestion surcharge',
    
    -- Códigos de referência
    ratecodeid DOUBLE COMMENT 'Rate code (1=Standard, 2=JFK, 3=Newark, etc)',
    store_and_fwd_flag STRING COMMENT 'Store and forward flag (Y/N)',
    payment_type DOUBLE COMMENT 'Payment type (1=Credit, 2=Cash, etc)',
    trip_type DOUBLE COMMENT 'Trip type (1=Street-hail, 2=Dispatch)',
    ehail_fee DOUBLE COMMENT 'E-hail fee',
    
    -- Metadados de ingestão
    _ingestion_timestamp TIMESTAMP COMMENT 'Timestamp when record was ingested',
    _source_file STRING COMMENT 'Source CSV filename'
)
USING delta
COMMENT 'Bronze layer - Raw taxi trip data ingested from CSV files'
LOCATION 'dbfs:/mnt/data/bronze/taxi_trips_raw';

-- ══════════════════════════════════════════════════════════════════════════════
-- SILVER LAYER - Tabelas limpas e validadas
-- ══════════════════════════════════════════════════════════════════════════════

-- Silver: Trips validados e limpos
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS silver.taxi_trips;

CREATE TABLE silver.taxi_trips (
    -- Surrogate key
    trip_id STRING COMMENT 'Unique trip identifier (hash)',
    
    -- Identificadores
    vendor_id INT COMMENT 'Vendor ID',
    
    -- Timestamps
    pickup_datetime TIMESTAMP COMMENT 'Pickup date and time',
    dropoff_datetime TIMESTAMP COMMENT 'Dropoff date and time',
    trip_duration_minutes DOUBLE COMMENT 'Trip duration in minutes (calculated)',
    
    -- Localização
    pickup_location_id INT COMMENT 'Pickup location ID',
    dropoff_location_id INT COMMENT 'Dropoff location ID',
    
    -- Detalhes da viagem
    passenger_count INT COMMENT 'Number of passengers',
    trip_distance DOUBLE COMMENT 'Trip distance in miles',
    
    -- Valores financeiros
    fare_amount DECIMAL(10,2) COMMENT 'Base fare amount',
    extra DECIMAL(10,2) COMMENT 'Extra charges',
    mta_tax DECIMAL(10,2) COMMENT 'MTA tax',
    tip_amount DECIMAL(10,2) COMMENT 'Tip amount',
    tolls_amount DECIMAL(10,2) COMMENT 'Tolls amount',
    improvement_surcharge DECIMAL(10,2) COMMENT 'Improvement surcharge',
    total_amount DECIMAL(10,2) COMMENT 'Total amount charged',
    congestion_surcharge DECIMAL(10,2) COMMENT 'Congestion surcharge',
    
    -- Códigos de referência
    rate_code_id INT COMMENT 'Rate code',
    store_and_fwd_flag STRING COMMENT 'Store and forward flag',
    payment_type_id INT COMMENT 'Payment type',
    trip_type_id INT COMMENT 'Trip type',
    
    -- Flags de qualidade
    is_valid_trip BOOLEAN COMMENT 'Trip passed all DQ validations',
    dq_validation_errors STRING COMMENT 'List of DQ errors (if any)',
    
    -- Metadados
    _processed_timestamp TIMESTAMP COMMENT 'Timestamp when record was processed',
    _source_file STRING COMMENT 'Source CSV filename'
)
USING delta
COMMENT 'Silver layer - Cleansed and validated taxi trip data'
LOCATION 'dbfs:/mnt/data/silver/taxi_trips';

-- ══════════════════════════════════════════════════════════════════════════════
-- GOLD LAYER - Tabelas agregadas (analytics-ready)
-- ══════════════════════════════════════════════════════════════════════════════

-- Gold: Trips agregados por dia e localização
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS gold.daily_trips_summary;

CREATE TABLE gold.daily_trips_summary (
    -- Dimensões
    trip_date DATE COMMENT 'Trip date',
    pickup_location_id INT COMMENT 'Pickup location ID',
    payment_type_id INT COMMENT 'Payment type',
    
    -- Métricas
    total_trips INT COMMENT 'Total number of trips',
    total_passengers INT COMMENT 'Total number of passengers',
    total_distance DOUBLE COMMENT 'Total distance traveled (miles)',
    avg_distance DOUBLE COMMENT 'Average distance per trip',
    total_revenue DECIMAL(12,2) COMMENT 'Total revenue',
    avg_fare DECIMAL(10,2) COMMENT 'Average fare amount',
    avg_tip_percentage DECIMAL(5,2) COMMENT 'Average tip as % of fare',
    
    -- Metadados
    _last_updated TIMESTAMP COMMENT 'Last update timestamp'
)
USING delta
COMMENT 'Gold layer - Daily aggregated trip metrics'
LOCATION 'dbfs:/mnt/data/gold/daily_trips_summary';

-- ══════════════════════════════════════════════════════════════════════════════
-- REFERENCE LAYER - Tabelas de referência
-- ══════════════════════════════════════════════════════════════════════════════

-- Reference: Payment Types
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS reference.payment_types;

CREATE TABLE reference.payment_types (
    payment_type_id INT COMMENT 'Payment type ID',
    payment_type_name STRING COMMENT 'Payment type name',
    payment_type_description STRING COMMENT 'Payment type description',
    is_active BOOLEAN COMMENT 'Is this payment type currently active?'
)
USING delta
COMMENT 'Reference data - Payment type lookup'
LOCATION 'dbfs:/mnt/data/reference/payment_types';

-- Reference: Rate Codes
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS reference.rate_codes;

CREATE TABLE reference.rate_codes (
    rate_code_id INT COMMENT 'Rate code ID',
    rate_code_name STRING COMMENT 'Rate code name',
    rate_code_description STRING COMMENT 'Rate code description'
)
USING delta
COMMENT 'Reference data - Rate code lookup'
LOCATION 'dbfs:/mnt/data/reference/rate_codes';

-- Reference: Trip Types
-- ─────────────────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS reference.trip_types;

CREATE TABLE reference.trip_types (
    trip_type_id INT COMMENT 'Trip type ID',
    trip_type_name STRING COMMENT 'Trip type name',
    trip_type_description STRING COMMENT 'Trip type description'
)
USING delta
COMMENT 'Reference data - Trip type lookup'
LOCATION 'dbfs:/mnt/data/reference/trip_types';

-- ══════════════════════════════════════════════════════════════════════════════
-- VERIFICAÇÃO
-- ══════════════════════════════════════════════════════════════════════════════

-- Listar todas as tabelas criadas
SHOW TABLES IN bronze;
SHOW TABLES IN silver;
SHOW TABLES IN gold;
SHOW TABLES IN reference;

-- Descrever estrutura das principais tabelas
DESCRIBE TABLE EXTENDED bronze.taxi_trips_raw;
DESCRIBE TABLE EXTENDED silver.taxi_trips;
DESCRIBE TABLE EXTENDED gold.daily_trips_summary;
