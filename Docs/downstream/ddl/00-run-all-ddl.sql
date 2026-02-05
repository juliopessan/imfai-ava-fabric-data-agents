-- ========================================
-- MASTER DDL EXECUTION SCRIPT
-- ========================================
-- Project: NYC Green Taxi Analytics
-- Purpose: Execute all DDL scripts in correct order
-- Platform: Azure Databricks
-- Version: 1.0
-- Created: 2026-02-05
-- Author: Diego (DataEngineerExec)
-- ========================================

-- EXECUTION ORDER:
-- Step 1: Create catalog and schemas
-- Step 2: Create Bronze layer tables
-- Step 3: Create Silver layer tables
-- Step 4: Create Gold layer tables
-- Step 5: Validate installation

-- ========================================
-- STEP 0: PREREQUISITES
-- ========================================

-- Ensure Unity Catalog is enabled
-- Ensure user has CREATE CATALOG permission
-- Ensure storage locations are configured

-- ========================================
-- STEP 1: CREATE CATALOG & SCHEMAS
-- ========================================

CREATE CATALOG IF NOT EXISTS nyc_taxi
  COMMENT 'NYC Green Taxi Analytics Data Lakehouse';

USE CATALOG nyc_taxi;

-- Set catalog-level properties
ALTER CATALOG nyc_taxi SET OWNER TO `data-engineering-team`;

-- ========================================
-- STEP 2: EXECUTE BRONZE LAYER DDL
-- ========================================

-- Run: 01-bronze-tables.sql
-- Creates: bronze.trips_raw, bronze.payment_types_raw, 
--          bronze.rate_codes_raw, bronze.trip_types_raw

-- Verification
SELECT 'Bronze layer created successfully' as status,
       COUNT(*) as table_count 
FROM system.information_schema.tables 
WHERE table_schema = 'bronze';

-- ========================================
-- STEP 3: EXECUTE SILVER LAYER DDL
-- ========================================

-- Run: 02-silver-tables.sql
-- Creates: silver.trips_cleaned, silver.payment_types,
--          silver.rate_codes, silver.trip_types, silver.dq_quarantine

-- Verification
SELECT 'Silver layer created successfully' as status,
       COUNT(*) as table_count 
FROM system.information_schema.tables 
WHERE table_schema = 'silver';

-- ========================================
-- STEP 4: EXECUTE GOLD LAYER DDL
-- ========================================

-- Run: 03-gold-tables.sql
-- Creates: gold.fact_trips, gold.dim_date, gold.dim_location,
--          gold.dim_payment, gold.dim_rate, gold.dim_trip_type

-- Verification
SELECT 'Gold layer created successfully' as status,
       COUNT(*) as table_count 
FROM system.information_schema.tables 
WHERE table_schema = 'gold';

-- ========================================
-- STEP 5: COMPLETE VALIDATION
-- ========================================

-- Show all tables created
SELECT 
    table_schema as layer,
    table_name,
    table_type,
    CAST(table_owner AS STRING) as owner
FROM system.information_schema.tables
WHERE table_catalog = 'nyc_taxi'
ORDER BY table_schema, table_name;

-- Count tables by layer
SELECT 
    table_schema as layer,
    COUNT(*) as table_count
FROM system.information_schema.tables
WHERE table_catalog = 'nyc_taxi'
GROUP BY table_schema
ORDER BY table_schema;

-- Expected counts:
-- bronze: 4 tables
-- silver: 5 tables (including dq_quarantine)
-- gold: 7 tables (6 star schema + 1 aggregate)

-- ========================================
-- STEP 6: GRANT PERMISSIONS
-- ========================================

-- Bronze layer
GRANT USE CATALOG ON CATALOG nyc_taxi TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA bronze TO `data-engineers`;
GRANT SELECT ON SCHEMA bronze TO `data-engineers`;
GRANT MODIFY ON SCHEMA bronze TO `data-pipeline-service-principal`;

-- Silver layer
GRANT USE SCHEMA ON SCHEMA silver TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA silver TO `data-analysts`;
GRANT SELECT ON SCHEMA silver TO `data-engineers`;
GRANT SELECT ON SCHEMA silver TO `data-analysts`;
GRANT MODIFY ON SCHEMA silver TO `data-pipeline-service-principal`;

-- Gold layer
GRANT USE SCHEMA ON SCHEMA gold TO `data-engineers`;
GRANT USE SCHEMA ON SCHEMA gold TO `data-analysts`;
GRANT USE SCHEMA ON SCHEMA gold TO `bi-developers`;
GRANT SELECT ON SCHEMA gold TO `data-engineers`;
GRANT SELECT ON SCHEMA gold TO `data-analysts`;
GRANT SELECT ON SCHEMA gold TO `bi-developers`;
GRANT MODIFY ON SCHEMA gold TO `data-pipeline-service-principal`;

-- ========================================
-- STEP 7: INSTALLATION REPORT
-- ========================================

SELECT '=== NYC TAXI ANALYTICS - DDL INSTALLATION COMPLETE ===' as report;

SELECT 
    'Catalog' as component,
    'nyc_taxi' as name,
    'ACTIVE' as status;

SELECT 
    'Schema' as component,
    table_schema as name,
    CASE 
        WHEN COUNT(*) > 0 THEN 'TABLES CREATED'
        ELSE 'EMPTY'
    END as status
FROM system.information_schema.tables
WHERE table_catalog = 'nyc_taxi'
GROUP BY table_schema
ORDER BY table_schema;

SELECT 
    '=== NEXT STEPS ===' as action,
    'Run ETL scripts to populate tables' as description
UNION ALL
SELECT 
    '1. Ingest Bronze',
    'Execute DLT pipeline for bronze layer'
UNION ALL
SELECT 
    '2. Transform Silver',
    'Execute DLT pipeline with DQ expectations'
UNION ALL
SELECT 
    '3. Build Gold',
    'Execute Spark SQL jobs for dimensional model'
UNION ALL
SELECT 
    '4. Connect BI',
    'Configure Power BI dataset connection';

-- ========================================
-- END OF MASTER DDL SCRIPT
-- ========================================
