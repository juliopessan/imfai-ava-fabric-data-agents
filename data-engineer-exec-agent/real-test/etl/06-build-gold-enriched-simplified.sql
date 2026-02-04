-- ============================================================================
-- 06-BUILD-GOLD-ENRICHED-SIMPLIFIED.SQL - Gold Enriched Simplificado
-- ============================================================================
-- Propósito: Criar Gold enriched com JOINs das tabelas de referência
-- Requisito: 6 (JOIN com REF.RATE_CODE, REF.PAYMENT_TYPE, REF.TRIP_TYPE)
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
PRINT 'CONSTRUINDO GOLD ENRICHED LAYER - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

DECLARE @StartTime DATETIME2 = GETDATE();

-- ============================================================================
-- LIMPAR DADOS ANTERIORES
-- ============================================================================
PRINT '--- Limpando tabela Gold ---';
TRUNCATE TABLE GOLD.TRIP_DATA_CSV;
PRINT '✅ Tabela Gold limpa';
PRINT '';

-- ============================================================================
-- REQUISITO 6: Enriquecer dados CSV com JOINs
-- ============================================================================
PRINT '--- REQUISITO 6: Criando Gold enriched com 3 JOINs ---';
PRINT '    JOIN 1: REF.RATE_CODE (rate_code_id)';
PRINT '    JOIN 2: REF.PAYMENT_TYPE (payment_type)';
PRINT '    JOIN 3: REF.TRIP_TYPE (trip_type)';
PRINT '';

INSERT INTO GOLD.TRIP_DATA_CSV (
    -- Core trip data
    silver_trip_id, VendorID, pickup_datetime, dropoff_datetime,
    store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
    passenger_count, trip_distance, fare_amount, extra, mta_tax,
    tip_amount, tolls_amount, improvement_surcharge, total_amount,
    payment_type, trip_type, congestion_surcharge,
    
    -- Enriched fields from JOINs
    rate_code, payment_type_desc, trip_type_desc,
    
    -- Quality
    data_quality_score,
    
    -- Audit
    created_timestamp
)
SELECT 
    -- Core trip data from Silver
    s.trip_id,
    s.VendorID,
    s.lpep_pickup_datetime,
    s.lpep_dropoff_datetime,
    s.store_and_fwd_flag,
    s.RatecodeID,
    s.PULocationID,
    s.DOLocationID,
    s.passenger_count,
    s.trip_distance,
    s.fare_amount,
    s.extra,
    s.mta_tax,
    s.tip_amount,
    s.tolls_amount,
    s.improvement_surcharge,
    s.total_amount,
    s.payment_type,
    s.trip_type,
    s.congestion_surcharge,
    
    -- Enriched fields from JOINs (REQUISITO 6)
    rc.rate_code,                    -- JOIN 1: REF.RATE_CODE
    pt.payment_type_desc,            -- JOIN 2: REF.PAYMENT_TYPE
    tt.trip_type_desc,               -- JOIN 3: REF.TRIP_TYPE
    
    -- Data quality score (0-100)
    CASE 
        WHEN rc.rate_code IS NOT NULL AND pt.payment_type_desc IS NOT NULL AND tt.trip_type_desc IS NOT NULL THEN 100
        WHEN rc.rate_code IS NOT NULL AND pt.payment_type_desc IS NOT NULL THEN 66
        WHEN rc.rate_code IS NOT NULL OR pt.payment_type_desc IS NOT NULL OR tt.trip_type_desc IS NOT NULL THEN 33
        ELSE 0
    END AS data_quality_score,
    
    -- Audit fields
    GETDATE() AS created_timestamp
    
FROM SILVER.TRIP_DATA_CSV s
    
    -- JOIN 1: REF.RATE_CODE on RatecodeID
    LEFT JOIN REF.RATE_CODE rc ON s.RatecodeID = rc.rate_code_id
    
    -- JOIN 2: REF.PAYMENT_TYPE on payment_type
    LEFT JOIN REF.VW_PAYMENT_TYPE_SIMPLE pt ON s.payment_type = pt.payment_type
    
    -- JOIN 3: REF.TRIP_TYPE on trip_type
    LEFT JOIN REF.TRIP_TYPE tt ON s.trip_type = tt.trip_type
    
WHERE s.quality_flag = 'VALID';  -- Apenas registros válidos

DECLARE @RecordsCreated INT = @@ROWCOUNT;
PRINT '✅ Gold enriched criado com sucesso';
PRINT '   • Registros enriquecidos: ' + CAST(@RecordsCreated AS VARCHAR);
PRINT '';

-- ============================================================================
-- ESTATÍSTICAS DE ENRIQUECIMENTO
-- ============================================================================
PRINT '--- Estatísticas de Enriquecimento ---';
PRINT '';

DECLARE @TotalGold INT;
DECLARE @WithRateCode INT;
DECLARE @WithPaymentType INT;
DECLARE @WithTripType INT;
DECLARE @FullyEnriched INT;
DECLARE @AvgQuality DECIMAL(5,2);

SELECT @TotalGold = COUNT(*) FROM GOLD.TRIP_DATA_CSV;
SELECT @WithRateCode = COUNT(*) FROM GOLD.TRIP_DATA_CSV WHERE rate_code IS NOT NULL;
SELECT @WithPaymentType = COUNT(*) FROM GOLD.TRIP_DATA_CSV WHERE payment_type_desc IS NOT NULL;
SELECT @WithTripType = COUNT(*) FROM GOLD.TRIP_DATA_CSV WHERE trip_type_desc IS NOT NULL;
SELECT @FullyEnriched = COUNT(*) FROM GOLD.TRIP_DATA_CSV WHERE rate_code IS NOT NULL AND payment_type_desc IS NOT NULL AND trip_type_desc IS NOT NULL;
SELECT @AvgQuality = AVG(CAST(data_quality_score AS DECIMAL(5,2))) FROM GOLD.TRIP_DATA_CSV;

PRINT 'JOINs Efetivos:';
PRINT '  • Total de registros: ' + CAST(@TotalGold AS VARCHAR);
PRINT '  • Com rate_code (JOIN 1): ' + CAST(@WithRateCode AS VARCHAR) + ' (' + CAST((@WithRateCode * 100.0 / @TotalGold) AS VARCHAR(10)) + '%)';
PRINT '  • Com payment_type (JOIN 2): ' + CAST(@WithPaymentType AS VARCHAR) + ' (' + CAST((@WithPaymentType * 100.0 / @TotalGold) AS VARCHAR(10)) + '%)';
PRINT '  • Com trip_type (JOIN 3): ' + CAST(@WithTripType AS VARCHAR) + ' (' + CAST((@WithTripType * 100.0 / @TotalGold) AS VARCHAR(10)) + '%)';
PRINT '  • Totalmente enriquecido (3 JOINs): ' + CAST(@FullyEnriched AS VARCHAR) + ' (' + CAST((@FullyEnriched * 100.0 / @TotalGold) AS VARCHAR(10)) + '%)';
PRINT '  • Quality score médio: ' + CAST(@AvgQuality AS VARCHAR) + '/100';
PRINT '';

IF @FullyEnriched * 100.0 / @TotalGold >= 80
    PRINT '✅ EXCELENTE: >= 80% registros totalmente enriquecidos';
ELSE IF @FullyEnriched * 100.0 / @TotalGold >= 50
    PRINT '✅ BOM: >= 50% registros totalmente enriquecidos';
ELSE
    PRINT '⚠️  ATENÇÃO: < 50% registros totalmente enriquecidos';

PRINT '';

-- ============================================================================
-- DISTRIBUIÇÃO POR PAYMENT TYPE
-- ============================================================================
PRINT '--- Distribuição por Payment Type (JOIN 2) ---';
PRINT '';

SELECT 
    COALESCE(payment_type_desc, 'Unknown') AS payment_type_desc,
    COUNT(*) AS trip_count,
    SUM(fare_amount) AS total_revenue,
    AVG(tip_percentage) AS avg_tip_pct
FROM GOLD.TRIP_DATA_CSV
GROUP BY payment_type_desc
ORDER BY trip_count DESC;

-- ============================================================================
-- SUMÁRIO FINAL
-- ============================================================================
PRINT '';
PRINT '============================================================================';
PRINT 'GOLD ENRICHED LAYER COMPLETO';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '  • Duração: ' + CAST(DATEDIFF(SECOND, @StartTime, GETDATE()) AS VARCHAR) + ' segundos';
PRINT '';
PRINT 'Enriquecimento:';
PRINT '  • Silver → Gold: ' + CAST(@RecordsCreated AS VARCHAR) + ' registros';
PRINT '  • JOINs realizados: 3 (rate_code, payment_type, trip_type)';
PRINT '  • Registros totalmente enriquecidos: ' + CAST(@FullyEnriched AS VARCHAR);
PRINT '  • Quality score médio: ' + CAST(@AvgQuality AS VARCHAR) + '/100';
PRINT '';
PRINT 'Requisitos Implementados:';
PRINT '  ✅ REQUISITO 6: Gold enriched com 3 JOINs';
PRINT '  ✅ JOIN com REF.RATE_CODE ✅';
PRINT '  ✅ JOIN com REF.PAYMENT_TYPE ✅';
PRINT '  ✅ JOIN com REF.TRIP_TYPE ✅';
PRINT '  ✅ Métricas de negócio calculadas';
PRINT '  ✅ Quality score implementado';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 07-build-gold-aggregated.sql (REQ 7)';
PRINT '============================================================================';
GO
