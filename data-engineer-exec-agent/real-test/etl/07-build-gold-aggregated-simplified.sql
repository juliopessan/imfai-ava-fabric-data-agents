-- ============================================================================
-- 07-BUILD-GOLD-AGGREGATED-SIMPLIFIED.SQL - Gold Aggregated Simplificado
-- ============================================================================
-- Propósito: Criar agregação por PULocationID com SUM e COUNT
-- Requisito: 7 (Agregar por PULocationID: SUM(trip_distance), SUM(fare_amount), COUNT(*))
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
PRINT 'CONSTRUINDO GOLD AGGREGATED LAYER - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

DECLARE @StartTime DATETIME2 = GETDATE();

-- ============================================================================
-- LIMPAR DADOS ANTERIORES
-- ============================================================================
PRINT '--- Limpando tabela Gold Aggregated ---';
TRUNCATE TABLE GOLD.TRIP_DATA_PARQUET_AGG;
PRINT '✅ Tabela Gold Aggregated limpa';
PRINT '';

-- ============================================================================
-- REQUISITO 7: Agregar dados por PULocationID
-- ============================================================================
PRINT '--- REQUISITO 7: Criando Gold agregado por PULocationID ---';
PRINT '    Métricas: SUM(trip_distance), SUM(fare_amount), COUNT(*)';
PRINT '';

INSERT INTO GOLD.TRIP_DATA_PARQUET_AGG (
    PULocationID,
    trip_count,
    total_trip_distance,
    total_fare_amount,
    avg_trip_distance,
    avg_fare_amount,
    created_timestamp
)
SELECT 
    PULocationID,
    COUNT(*) AS trip_count,                                -- REQUISITO 7: COUNT(*)
    SUM(trip_distance) AS total_trip_distance,             -- REQUISITO 7: SUM(trip_distance)
    SUM(fare_amount) AS total_fare_amount,                 -- REQUISITO 7: SUM(fare_amount)
    AVG(trip_distance) AS avg_trip_distance,
    AVG(fare_amount) AS avg_fare_amount,
    GETDATE() AS created_timestamp
FROM SILVER.TRIP_DATA_CSV
WHERE quality_flag = 'VALID'
GROUP BY PULocationID;

DECLARE @RecordsCreated INT = @@ROWCOUNT;
PRINT '✅ Gold agregado criado com sucesso';
PRINT '   • Localizações únicas: ' + CAST(@RecordsCreated AS VARCHAR);
PRINT '';

-- ============================================================================
-- ESTATÍSTICAS DE AGREGAÇÃO
-- ============================================================================
PRINT '--- Estatísticas de Agregação ---';
PRINT '';

DECLARE @TotalTrips INT;
DECLARE @TotalDistance DECIMAL(18,2);
DECLARE @TotalRevenue DECIMAL(18,2);

SELECT 
    @TotalTrips = SUM(trip_count),
    @TotalDistance = SUM(total_trip_distance),
    @TotalRevenue = SUM(total_fare_amount)
FROM GOLD.TRIP_DATA_PARQUET_AGG;

PRINT 'Totais Agregados:';
PRINT '  • Total de viagens: ' + CAST(@TotalTrips AS VARCHAR);
PRINT '  • Distância total: ' + CAST(@TotalDistance AS VARCHAR) + ' miles';
PRINT '  • Receita total: $' + CAST(@TotalRevenue AS VARCHAR);
PRINT '  • Distância média por localização: ' + CAST(@TotalDistance / @RecordsCreated AS VARCHAR) + ' miles';
PRINT '  • Receita média por localização: $' + CAST(@TotalRevenue / @RecordsCreated AS VARCHAR);
PRINT '';

-- ============================================================================
-- TOP 10 LOCALIZAÇÕES POR RECEITA
-- ============================================================================
PRINT '--- Top 10 Localizações por Receita ---';
PRINT '';

SELECT TOP 10
    PULocationID,
    trip_count,
    total_trip_distance,
    total_fare_amount,
    avg_fare_amount
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY total_fare_amount DESC;

-- ============================================================================
-- TOP 10 LOCALIZAÇÕES POR VOLUME
-- ============================================================================
PRINT '';
PRINT '--- Top 10 Localizações por Volume de Viagens ---';
PRINT '';

SELECT TOP 10
    PULocationID,
    trip_count,
    total_trip_distance,
    total_fare_amount
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY trip_count DESC;

-- ============================================================================
-- SUMÁRIO FINAL
-- ============================================================================
PRINT '';
PRINT '============================================================================';
PRINT 'GOLD AGGREGATED LAYER COMPLETO';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '  • Duração: ' + CAST(DATEDIFF(SECOND, @StartTime, GETDATE()) AS VARCHAR) + ' segundos';
PRINT '';
PRINT 'Agregação:';
PRINT '  • Silver → Gold Aggregated: ' + CAST(@RecordsCreated AS VARCHAR) + ' localizações';
PRINT '  • Total de viagens agregadas: ' + CAST(@TotalTrips AS VARCHAR);
PRINT '  • Distância total: ' + CAST(@TotalDistance AS VARCHAR) + ' miles';
PRINT '  • Receita total: $' + CAST(@TotalRevenue AS VARCHAR);
PRINT '';
PRINT 'Requisitos Implementados:';
PRINT '  ✅ REQUISITO 7: Gold agregado por PULocationID';
PRINT '  ✅ SUM(trip_distance) ✅';
PRINT '  ✅ SUM(fare_amount) ✅';
PRINT '  ✅ COUNT(*) ✅';
PRINT '  ✅ Métricas adicionais (AVG, TOP 10)';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 08-unit-tests.sql (REQ 8)';
PRINT '============================================================================';
GO
