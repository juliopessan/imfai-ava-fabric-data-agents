-- =============================================================================
-- DDL Script: Reference Tables
-- Project: NYC Green Taxi Pipeline
-- Generated: 2026-01-26 16:00
-- Agent: DataFlow v2.0
-- =============================================================================
-- -----------------------------------------------------------------------------
-- REF.PAYMENT_TYPE
-- Purpose: Payment method lookup
-- Source: payment_type_array.json
-- -----------------------------------------------------------------------------
IF OBJECT_ID('REF.PAYMENT_TYPE', 'U') IS NOT NULL DROP TABLE REF.PAYMENT_TYPE;
GO CREATE TABLE REF.PAYMENT_TYPE (
        payment_type_id TINYINT PRIMARY KEY,
        payment_type_desc VARCHAR(50) NOT NULL,
        is_active BIT DEFAULT 1,
        created_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- Seed data from payment_type_array.json
INSERT INTO REF.PAYMENT_TYPE (payment_type_id, payment_type_desc)
VALUES (1, 'Credit card'),
    (2, 'Cash'),
    (3, 'No charge'),
    (4, 'Dispute'),
    (5, 'Unknown'),
    (6, 'Voided trip');
GO -- -----------------------------------------------------------------------------
    -- REF.RATE_CODE
    -- Purpose: Rate code lookup
    -- Source: rate_code.json
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('REF.RATE_CODE', 'U') IS NOT NULL DROP TABLE REF.RATE_CODE;
GO CREATE TABLE REF.RATE_CODE (
        rate_code_id TINYINT PRIMARY KEY,
        rate_code_desc VARCHAR(50) NOT NULL,
        is_active BIT DEFAULT 1,
        created_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- Seed data from rate_code.json
INSERT INTO REF.RATE_CODE (rate_code_id, rate_code_desc)
VALUES (1, 'Standard rate'),
    (2, 'JFK'),
    (3, 'Newark'),
    (4, 'Nassau/Westchester'),
    (5, 'Negotiated fare'),
    (6, 'Group ride');
GO -- -----------------------------------------------------------------------------
    -- REF.TRIP_TYPE
    -- Purpose: Trip type lookup
    -- Source: trip_type.tsv
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('REF.TRIP_TYPE', 'U') IS NOT NULL DROP TABLE REF.TRIP_TYPE;
GO CREATE TABLE REF.TRIP_TYPE (
        trip_type_id TINYINT PRIMARY KEY,
        trip_type_desc VARCHAR(50) NOT NULL,
        is_active BIT DEFAULT 1,
        created_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO -- Seed data from trip_type.tsv
INSERT INTO REF.TRIP_TYPE (trip_type_id, trip_type_desc)
VALUES (1, 'Street-hail'),
    (2, 'Dispatch');
GO -- -----------------------------------------------------------------------------
    -- REF.VENDOR
    -- Purpose: Vendor lookup
    -- Source: Derived from data analysis
    -- -----------------------------------------------------------------------------
    IF OBJECT_ID('REF.VENDOR', 'U') IS NOT NULL DROP TABLE REF.VENDOR;
GO CREATE TABLE REF.VENDOR (
        vendor_id TINYINT PRIMARY KEY,
        vendor_name VARCHAR(100) NOT NULL,
        vendor_code VARCHAR(10),
        is_active BIT DEFAULT 1,
        created_timestamp DATETIME2 DEFAULT GETDATE()
    );
GO
INSERT INTO REF.VENDOR (vendor_id, vendor_name, vendor_code)
VALUES (1, 'Creative Mobile Technologies', 'CMT'),
    (2, 'VeriFone Inc.', 'VFI');
GO -- =============================================================================
    -- Verification
    -- =============================================================================
SELECT TABLE_SCHEMA,
    TABLE_NAME,
    (
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS c
        WHERE c.TABLE_SCHEMA = t.TABLE_SCHEMA
            AND c.TABLE_NAME = t.TABLE_NAME
    ) AS column_count,
    (
        SELECT COUNT(*)
        FROM sys.tables t2
            JOIN sys.schemas s ON t2.schema_id = s.schema_id
        WHERE s.name = t.TABLE_SCHEMA
            AND t2.name = t.TABLE_NAME
    ) AS row_count
FROM INFORMATION_SCHEMA.TABLES t
WHERE TABLE_SCHEMA = 'REF'
ORDER BY TABLE_NAME;
GO -- Show reference data counts
SELECT 'PAYMENT_TYPE' AS table_name,
    COUNT(*) AS row_count
FROM REF.PAYMENT_TYPE
UNION ALL
SELECT 'RATE_CODE',
    COUNT(*)
FROM REF.RATE_CODE
UNION ALL
SELECT 'TRIP_TYPE',
    COUNT(*)
FROM REF.TRIP_TYPE
UNION ALL
SELECT 'VENDOR',
    COUNT(*)
FROM REF.VENDOR;
GO PRINT '✅ Reference tables created and populated successfully';
GO