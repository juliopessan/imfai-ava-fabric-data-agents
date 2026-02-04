-- ══════════════════════════════════════════════════════════════════════════════
-- DATABRICKS - CRIAÇÃO DE SCHEMAS (MEDALLION ARCHITECTURE)
-- ══════════════════════════════════════════════════════════════════════════════
-- Descrição: Cria schemas para arquitetura Medallion (Bronze, Silver, Gold)
-- Autor: Avanade Core - Data Engineering Agents
-- Data: 2026-02-04
-- ══════════════════════════════════════════════════════════════════════════════

-- Bronze Layer: Dados brutos (raw data)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS bronze
COMMENT 'Bronze Layer - Raw data ingested from source systems. No transformations applied.'
LOCATION 'dbfs:/mnt/data/bronze';

-- Silver Layer: Dados limpos e validados
-- ─────────────────────────────────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS silver
COMMENT 'Silver Layer - Cleansed and validated data. Business rules applied.'
LOCATION 'dbfs:/mnt/data/silver';

-- Gold Layer: Dados agregados e prontos para consumo
-- ─────────────────────────────────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS gold
COMMENT 'Gold Layer - Business-level aggregations and analytics. Ready for BI tools.'
LOCATION 'dbfs:/mnt/data/gold';

-- Reference Layer: Dados de referência (lookup tables)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS reference
COMMENT 'Reference data - Lookup tables, dimensions, and master data'
LOCATION 'dbfs:/mnt/data/reference';

-- ══════════════════════════════════════════════════════════════════════════════
-- VERIFICAÇÃO
-- ══════════════════════════════════════════════════════════════════════════════
SHOW SCHEMAS;
