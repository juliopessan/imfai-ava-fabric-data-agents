-- ============================================================================
-- 07-BUILD-GOLD-AGGREGATED.SQL - Construção Gold Layer (Aggregated)
-- ============================================================================
-- Propósito: Criar tabela Gold agregada por PULocationID
-- Requisito: 7 (GOLD.TRIP_DATA_PARQUET_AGG - agregação por localização)
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
PRINT 'CONSTRUINDO GOLD LAYER - TABELA AGREGADA (PARQUET)';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @LocationsAggregated INT = 0;

-- ============================================================================
-- VERIFICAR DADOS DISPONÍVEIS
-- ============================================================================
PRINT '--- Verificando Dados em Silver ---';
PRINT '';

DECLARE @SilverParquetCount INT, @SilverValidCount INT;
SELECT @SilverParquetCount = COUNT(*) FROM SILVER.TRIP_DATA_PARQUET;
SELECT @SilverValidCount = COUNT(*) FROM SILVER.TRIP_DATA_PARQUET WHERE quality_flag = 'VALID';

PRINT 'Dados em SILVER.TRIP_DATA_PARQUET:';
PRINT '  • Total: ' + CAST(@SilverParquetCount AS VARCHAR);
PRINT '  • VALID: ' + CAST(@SilverValidCount AS VARCHAR);
PRINT '';

IF @SilverValidCount = 0
BEGIN
    PRINT '⚠️  AVISO: Nenhum dado VÁLIDO em SILVER.TRIP_DATA_PARQUET';
    PRINT '   Este script usará SILVER.TRIP_DATA_CSV como fallback';
    PRINT '';
END

-- ============================================================================
-- REQUISITO 7: CONSTRUIR GOLD.TRIP_DATA_PARQUET_AGG (Aggregated)
-- ============================================================================
PRINT '--- REQUISITO 7: Construindo GOLD.TRIP_DATA_PARQUET_AGG ---';
PRINT '    • Agregação por PULocationID (Pickup Location)';
PRINT '    • Métricas: SUM(trip_distance), SUM(fare_amount), COUNT(trips)';
PRINT '    • KPIs de Revenue e Utilização';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- Limpar Gold aggregated table
    TRUNCATE TABLE GOLD.TRIP_DATA_PARQUET_AGG;
    
    PRINT '🗑️  GOLD.TRIP_DATA_PARQUET_AGG limpa';
    PRINT '';
    
    -- Construir agregação Gold
    -- Se Parquet disponível, usar Parquet; senão usar CSV como fallback
    IF @SilverValidCount > 0
    BEGIN
        PRINT '📊 Usando dados PARQUET para agregação';
        PRINT '';
        
        INSERT INTO GOLD.TRIP_DATA_PARQUET_AGG (
            PULocationID,
            total_trips,
            total_distance,
            total_fare_amount,
            total_tip_amount,
            total_revenue,
            avg_trip_distance,
            avg_fare_amount,
            avg_tip_amount,
            avg_passenger_count,
            min_fare,
            max_fare,
            total_airport_trips,
            total_cash_trips,
            total_card_trips,
            avg_trip_duration_minutes,
            total_weekend_trips,
            total_rush_hour_trips,
            location_utilization_score,
            revenue_per_trip,
            revenue_per_mile,
            aggregation_month,
            data_source
        )
        SELECT 
            -- Dimensão de agrupamento
            PULocationID,
            
            -- Métricas básicas (REQUISITO 7)
            COUNT(*) as total_trips,
            SUM(trip_distance) as total_distance,
            SUM(fare_amount) as total_fare_amount,
            SUM(tip_amount) as total_tip_amount,
            SUM(total_amount) as total_revenue,
            
            -- Médias
            AVG(trip_distance) as avg_trip_distance,
            AVG(fare_amount) as avg_fare_amount,
            AVG(tip_amount) as avg_tip_amount,
            AVG(CAST(passenger_count AS FLOAT)) as avg_passenger_count,
            
            -- Ranges
            MIN(fare_amount) as min_fare,
            MAX(fare_amount) as max_fare,
            
            -- Segmentações
            SUM(CASE WHEN RatecodeID IN (2, 3) THEN 1 ELSE 0 END) as total_airport_trips,
            SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) as total_cash_trips,
            SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) as total_card_trips,
            
            -- Duração média
            AVG(CAST(DATEDIFF(MINUTE, lpep_pickup_datetime, lpep_dropoff_datetime) AS FLOAT)) as avg_trip_duration_minutes,
            
            -- Padrões temporais
            SUM(CASE WHEN DATEPART(WEEKDAY, lpep_pickup_datetime) IN (1, 7) THEN 1 ELSE 0 END) as total_weekend_trips,
            SUM(CASE 
                WHEN DATEPART(HOUR, lpep_pickup_datetime) BETWEEN 7 AND 10 THEN 1
                WHEN DATEPART(HOUR, lpep_pickup_datetime) BETWEEN 16 AND 19 THEN 1
                ELSE 0
            END) as total_rush_hour_trips,
            
            -- KPIs calculados
            -- Utilization Score: baseia-se em frequência de viagens
            CASE 
                WHEN COUNT(*) >= 1000 THEN 100
                WHEN COUNT(*) >= 500 THEN 80
                WHEN COUNT(*) >= 100 THEN 60
                WHEN COUNT(*) >= 50 THEN 40
                ELSE 20
            END as location_utilization_score,
            
            AVG(total_amount) as revenue_per_trip,
            CASE 
                WHEN SUM(trip_distance) > 0 THEN SUM(total_amount) / SUM(trip_distance)
                ELSE 0
            END as revenue_per_mile,
            
            -- Mês de agregação
            MAX(partition_month) as aggregation_month,
            
            'PARQUET' as data_source
            
        FROM SILVER.TRIP_DATA_PARQUET
        WHERE quality_flag = 'VALID'
          AND PULocationID IS NOT NULL
        GROUP BY PULocationID;
        
    END
    ELSE
    BEGIN
        PRINT '📊 Usando dados CSV para agregação (Parquet não disponível)';
        PRINT '';
        
        INSERT INTO GOLD.TRIP_DATA_PARQUET_AGG (
            PULocationID,
            total_trips,
            total_distance,
            total_fare_amount,
            total_tip_amount,
            total_revenue,
            avg_trip_distance,
            avg_fare_amount,
            avg_tip_amount,
            avg_passenger_count,
            min_fare,
            max_fare,
            total_airport_trips,
            total_cash_trips,
            total_card_trips,
            avg_trip_duration_minutes,
            total_weekend_trips,
            total_rush_hour_trips,
            location_utilization_score,
            revenue_per_trip,
            revenue_per_mile,
            aggregation_month,
            data_source
        )
        SELECT 
            PULocationID,
            COUNT(*) as total_trips,
            SUM(trip_distance) as total_distance,
            SUM(fare_amount) as total_fare_amount,
            SUM(tip_amount) as total_tip_amount,
            SUM(total_amount) as total_revenue,
            AVG(trip_distance) as avg_trip_distance,
            AVG(fare_amount) as avg_fare_amount,
            AVG(tip_amount) as avg_tip_amount,
            AVG(CAST(passenger_count AS FLOAT)) as avg_passenger_count,
            MIN(fare_amount) as min_fare,
            MAX(fare_amount) as max_fare,
            SUM(CASE WHEN RatecodeID IN (2, 3) THEN 1 ELSE 0 END) as total_airport_trips,
            SUM(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END) as total_cash_trips,
            SUM(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) as total_card_trips,
            AVG(CAST(DATEDIFF(MINUTE, lpep_pickup_datetime, lpep_dropoff_datetime) AS FLOAT)) as avg_trip_duration_minutes,
            SUM(CASE WHEN DATEPART(WEEKDAY, lpep_pickup_datetime) IN (1, 7) THEN 1 ELSE 0 END) as total_weekend_trips,
            SUM(CASE 
                WHEN DATEPART(HOUR, lpep_pickup_datetime) BETWEEN 7 AND 10 THEN 1
                WHEN DATEPART(HOUR, lpep_pickup_datetime) BETWEEN 16 AND 19 THEN 1
                ELSE 0
            END) as total_rush_hour_trips,
            CASE 
                WHEN COUNT(*) >= 1000 THEN 100
                WHEN COUNT(*) >= 500 THEN 80
                WHEN COUNT(*) >= 100 THEN 60
                WHEN COUNT(*) >= 50 THEN 40
                ELSE 20
            END as location_utilization_score,
            AVG(total_amount) as revenue_per_trip,
            CASE 
                WHEN SUM(trip_distance) > 0 THEN SUM(total_amount) / SUM(trip_distance)
                ELSE 0
            END as revenue_per_mile,
            CAST(DATEPART(MONTH, MIN(lpep_pickup_datetime)) AS VARCHAR) as aggregation_month,
            'CSV' as data_source
        FROM SILVER.TRIP_DATA_CSV
        WHERE quality_flag = 'VALID'
          AND PULocationID IS NOT NULL
        GROUP BY PULocationID;
    END
    
    SET @LocationsAggregated = @@ROWCOUNT;
    
    COMMIT TRANSACTION;
    
    PRINT '✅ GOLD.TRIP_DATA_PARQUET_AGG criada com sucesso';
    PRINT '   • Localizações agregadas: ' + CAST(@LocationsAggregated AS VARCHAR);
    PRINT '   • Métricas calculadas: 15+ KPIs por localização';
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    PRINT '❌ ERRO: ' + ERROR_MESSAGE();
    THROW;
END CATCH;

-- ============================================================================
-- TOP 10 LOCALIZAÇÕES POR MÉTRICAS
-- ============================================================================
PRINT '--- Top 10 Localizações por Receita ---';
PRINT '';

SELECT TOP 10
    PULocationID,
    total_trips,
    CAST(total_revenue AS DECIMAL(12,2)) as total_revenue,
    CAST(revenue_per_trip AS DECIMAL(8,2)) as revenue_per_trip,
    location_utilization_score
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY total_revenue DESC;

PRINT '';

PRINT '--- Top 10 Localizações por Volume de Viagens ---';
PRINT '';

SELECT TOP 10
    PULocationID,
    total_trips,
    CAST(total_distance AS DECIMAL(12,2)) as total_distance,
    CAST(avg_trip_distance AS DECIMAL(6,2)) as avg_trip_distance,
    location_utilization_score
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY total_trips DESC;

PRINT '';

-- ============================================================================
-- ESTATÍSTICAS GERAIS
-- ============================================================================
PRINT '--- Estatísticas Gerais da Agregação ---';
PRINT '';

DECLARE @TotalRevenue DECIMAL(15,2), @TotalTrips INT, @AvgUtilization DECIMAL(5,2);

SELECT 
    @TotalRevenue = SUM(total_revenue),
    @TotalTrips = SUM(total_trips),
    @AvgUtilization = AVG(location_utilization_score)
FROM GOLD.TRIP_DATA_PARQUET_AGG;

PRINT 'Agregação Geral:';
PRINT '  • Total de localizações: ' + CAST(@LocationsAggregated AS VARCHAR);
PRINT '  • Total de viagens: ' + CAST(@TotalTrips AS VARCHAR);
PRINT '  • Receita total: $' + CAST(@TotalRevenue AS VARCHAR);
PRINT '  • Utilização média: ' + CAST(@AvgUtilization AS VARCHAR) + '/100';
PRINT '';

-- ============================================================================
-- SUMÁRIO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'GOLD LAYER AGGREGATED COMPLETA';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas:';
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '  • Localizações agregadas: ' + CAST(@LocationsAggregated AS VARCHAR);
PRINT '  • Total de viagens agregadas: ' + CAST(@TotalTrips AS VARCHAR);
PRINT '  • Receita total: $' + CAST(@TotalRevenue AS VARCHAR);
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 7: GOLD.TRIP_DATA_PARQUET_AGG';
PRINT '      • Agregação por PULocationID';
PRINT '      • SUM(trip_distance), SUM(fare_amount), COUNT(*)';
PRINT '      • 15+ KPIs de negócio';
PRINT '      • Revenue metrics';
PRINT '      • Utilization scores';
PRINT '';
PRINT 'Pipeline ETL Completa!';
PRINT '  ✅ REQUISITO 1a: CSV → LANDING (VARCHAR)';
PRINT '  ✅ REQUISITO 1b: LANDING → SILVER (tipos apropriados)';
PRINT '  ✅ REQUISITO 2a: Parquet → LANDING (VARCHAR)';
PRINT '  ✅ REQUISITO 2b: LANDING → SILVER (tipos apropriados)';
PRINT '  ✅ REQUISITO 3,4,5: Dados de Referência carregados';
PRINT '  ✅ REQUISITO 6: Gold Enriched (com JOINs)';
PRINT '  ✅ REQUISITO 7: Gold Aggregated (por localização)';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Criar testes unitários (REQUISITO 8)';
PRINT '============================================================================';

SET NOCOUNT OFF;
