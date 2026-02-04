-- ============================================================================
-- 05-TRANSFORM-TO-SILVER-PARQUET.SQL - Transformação Landing → Silver (Parquet)
-- ============================================================================
-- Propósito: Transformar dados Parquet de VARCHAR para tipos apropriados
-- Requisito: 2b (LANDING.TRIP_DATA_PARQUET → SILVER.TRIP_DATA_PARQUET)
-- Autor: DataFlow Agent
-- Data: 17 de Novembro de 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
SET NOCOUNT ON;
GO

PRINT '============================================================================';
PRINT 'TRANSFORMAÇÃO LANDING → SILVER (PARQUET) - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @RecordsProcessed INT = 0;
DECLARE @RecordsValid INT = 0;
DECLARE @RecordsInvalid INT = 0;
DECLARE @RecordsWarning INT = 0;

-- ============================================================================
-- VERIFICAR DADOS DISPONÍVEIS
-- ============================================================================
PRINT '--- Verificando Dados em Landing ---';
PRINT '';

DECLARE @LandingCount INT;
SELECT @LandingCount = COUNT(*) FROM LANDING.TRIP_DATA_PARQUET;

PRINT 'Registros disponíveis em LANDING.TRIP_DATA_PARQUET: ' + CAST(@LandingCount AS VARCHAR);
PRINT '';

IF @LandingCount = 0
BEGIN
    PRINT '⚠️  AVISO: Nenhum dado encontrado em LANDING.TRIP_DATA_PARQUET';
    PRINT '   Execute: python load_parquet_to_sql.py';
    PRINT '   Depois: 03-load-landing-parquet.sql';
    PRINT '';
    PRINT '   Pipeline continuará (script não-bloqueante)';
    PRINT '';
    RETURN;
END

-- ============================================================================
-- REQUISITO 2b: TRANSFORMAR PARQUET PARA SILVER
-- ============================================================================
PRINT '--- REQUISITO 2b: Transformando Landing → Silver (Parquet) ---';
PRINT '    • Convertendo VARCHAR → Tipos apropriados';
PRINT '    • Aplicando validações de qualidade';
PRINT '    • Mantendo metadados de partição';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- Limpar tabelas Silver Parquet
    TRUNCATE TABLE SILVER.TRIP_DATA_PARQUET;
    TRUNCATE TABLE SILVER.TRIP_DATA_PARQUET_REJECTS;
    
    PRINT '🗑️  Tabelas Silver Parquet limpas';
    PRINT '';
    
    -- Inserir registros transformados
    INSERT INTO SILVER.TRIP_DATA_PARQUET (
        VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
        store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
        passenger_count, trip_distance, fare_amount, extra, mta_tax,
        tip_amount, tolls_amount, improvement_surcharge, total_amount,
        payment_type, trip_type, congestion_surcharge,
        partition_month, quality_flag, validation_errors, source_system
    )
    SELECT 
        -- Conversões de tipo
        TRY_CAST(VendorID AS INT) as VendorID,
        TRY_CAST(lpep_pickup_datetime AS DATETIME2) as lpep_pickup_datetime,
        TRY_CAST(lpep_dropoff_datetime AS DATETIME2) as lpep_dropoff_datetime,
        LEFT(store_and_fwd_flag, 1) as store_and_fwd_flag,
        TRY_CAST(RatecodeID AS INT) as RatecodeID,
        TRY_CAST(PULocationID AS INT) as PULocationID,
        TRY_CAST(DOLocationID AS INT) as DOLocationID,
        TRY_CAST(passenger_count AS INT) as passenger_count,
        TRY_CAST(trip_distance AS DECIMAL(8,2)) as trip_distance,
        TRY_CAST(fare_amount AS DECIMAL(10,2)) as fare_amount,
        TRY_CAST(extra AS DECIMAL(10,2)) as extra,
        TRY_CAST(mta_tax AS DECIMAL(10,2)) as mta_tax,
        TRY_CAST(tip_amount AS DECIMAL(10,2)) as tip_amount,
        TRY_CAST(tolls_amount AS DECIMAL(10,2)) as tolls_amount,
        TRY_CAST(improvement_surcharge AS DECIMAL(10,2)) as improvement_surcharge,
        TRY_CAST(total_amount AS DECIMAL(10,2)) as total_amount,
        TRY_CAST(payment_type AS INT) as payment_type,
        TRY_CAST(trip_type AS INT) as trip_type,
        TRY_CAST(congestion_surcharge AS DECIMAL(10,2)) as congestion_surcharge,
        
        -- Extrair mês da partição (month=04 → 04)
        RIGHT(partition_key, 2) as partition_month,
        
        -- Quality flag (mesmas regras do CSV)
        CASE 
            WHEN TRY_CAST(VendorID AS INT) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(VendorID AS INT) NOT IN (1, 2) THEN 'INVALID'
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) < TRY_CAST(lpep_pickup_datetime AS DATETIME2) THEN 'INVALID'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) < 0 THEN 'INVALID'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) > 500 THEN 'INVALID'
            WHEN TRY_CAST(passenger_count AS INT) IS NULL THEN 'WARNING'
            WHEN TRY_CAST(passenger_count AS INT) < 0 THEN 'WARNING'
            WHEN TRY_CAST(passenger_count AS INT) > 8 THEN 'WARNING'
            ELSE 'VALID'
        END as quality_flag,
        
        -- Mensagens de erro
        CASE WHEN TRY_CAST(VendorID AS INT) IS NULL THEN 'VendorID inválido; ' ELSE '' END +
        CASE WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL THEN 'Pickup inválido; ' ELSE '' END +
        CASE WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) IS NULL THEN 'Dropoff inválido; ' ELSE '' END +
        CASE WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) < TRY_CAST(lpep_pickup_datetime AS DATETIME2) THEN 'Dropoff antes pickup; ' ELSE '' END as validation_errors,
        
        'PARQUET_LANDING' as source_system
        
    FROM LANDING.TRIP_DATA_PARQUET;
    
    SET @RecordsProcessed = @@ROWCOUNT;
    
    -- Contadores por qualidade
    SELECT @RecordsValid = COUNT(*) FROM SILVER.TRIP_DATA_PARQUET WHERE quality_flag = 'VALID';
    SELECT @RecordsWarning = COUNT(*) FROM SILVER.TRIP_DATA_PARQUET WHERE quality_flag = 'WARNING';
    SELECT @RecordsInvalid = COUNT(*) FROM SILVER.TRIP_DATA_PARQUET WHERE quality_flag = 'INVALID';
    
    PRINT '✅ Transformação Parquet → Silver concluída';
    PRINT '   • Registros processados: ' + CAST(@RecordsProcessed AS VARCHAR);
    PRINT '   • VALID: ' + CAST(@RecordsValid AS VARCHAR) + 
          ' (' + CAST((@RecordsValid * 100.0 / @RecordsProcessed) AS DECIMAL(5,2)) + '%)';
    PRINT '   • WARNING: ' + CAST(@RecordsWarning AS VARCHAR);
    PRINT '   • INVALID: ' + CAST(@RecordsInvalid AS VARCHAR);
    PRINT '';
    
    COMMIT TRANSACTION;
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    PRINT '❌ ERRO: ' + ERROR_MESSAGE();
    THROW;
END CATCH;

-- ============================================================================
-- COMPARAÇÃO CSV vs PARQUET (Validação Cruzada)
-- ============================================================================
PRINT '--- Comparação de Qualidade: CSV vs Parquet ---';
PRINT '';

DECLARE @CSVValidPercent DECIMAL(5,2), @ParquetValidPercent DECIMAL(5,2);

SELECT @CSVValidPercent = (COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM SILVER.TRIP_DATA_CSV), 0))
FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID';

SELECT @ParquetValidPercent = (COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM SILVER.TRIP_DATA_PARQUET), 0))
FROM SILVER.TRIP_DATA_PARQUET WHERE quality_flag = 'VALID';

PRINT 'Taxa de Qualidade:';
PRINT '  • CSV: ' + CAST(@CSVValidPercent AS VARCHAR) + '% válidos';
PRINT '  • Parquet: ' + CAST(@ParquetValidPercent AS VARCHAR) + '% válidos';
PRINT '';

IF ABS(@CSVValidPercent - @ParquetValidPercent) < 5.0
BEGIN
    PRINT '✅ CSV e Parquet têm qualidade consistente';
END
ELSE
BEGIN
    PRINT '⚠️  Diferença de qualidade entre CSV e Parquet > 5%';
END

PRINT '';

-- ============================================================================
-- SUMÁRIO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'TRANSFORMAÇÃO PARQUET → SILVER COMPLETA';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas:';
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '  • Registros: ' + CAST(@RecordsProcessed AS VARCHAR);
PRINT '  • Taxa de válidos: ' + CAST(@ParquetValidPercent AS VARCHAR) + '%';
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 2b: LANDING.TRIP_DATA_PARQUET → SILVER.TRIP_DATA_PARQUET';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 06-build-gold-enriched.sql (criar Gold enriched)';
PRINT '============================================================================';

SET NOCOUNT OFF;
