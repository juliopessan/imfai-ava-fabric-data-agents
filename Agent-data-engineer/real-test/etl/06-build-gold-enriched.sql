-- ============================================================================
-- 06-BUILD-GOLD-ENRICHED.SQL - Construção Gold Layer (Enriched)
-- ============================================================================
-- Propósito: Criar tabela Gold enriquecida com JOINs de referência
-- Requisito: 6 (GOLD.TRIP_DATA_CSV com JOINs para rate_code, payment_type, trip_type)
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
PRINT 'CONSTRUINDO GOLD LAYER - TABELA ENRIQUECIDA (CSV)';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @RecordsCreated INT = 0;

-- ============================================================================
-- VERIFICAR DADOS DISPONÍVEIS
-- ============================================================================
PRINT '--- Verificando Dados em Silver ---';
PRINT '';

DECLARE @SilverCSVCount INT, @SilverValidCount INT;
SELECT @SilverCSVCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV;
SELECT @SilverValidCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID';

PRINT 'Dados em SILVER.TRIP_DATA_CSV:';
PRINT '  • Total: ' + CAST(@SilverCSVCount AS VARCHAR);
PRINT '  • VALID: ' + CAST(@SilverValidCount AS VARCHAR);
PRINT '';

IF @SilverValidCount = 0
BEGIN
    PRINT '❌ ERRO: Nenhum dado VÁLIDO em SILVER.TRIP_DATA_CSV';
    PRINT '   Execute primeiro: 04-transform-to-silver-csv.sql';
    RETURN;
END

-- ============================================================================
-- VERIFICAR DADOS DE REFERÊNCIA
-- ============================================================================
PRINT '--- Verificando Dados de Referência ---';
PRINT '';

DECLARE @RateCodeCount INT, @PaymentTypeCount INT, @TripTypeCount INT;
SELECT @RateCodeCount = COUNT(*) FROM REF.RATE_CODE;
SELECT @PaymentTypeCount = COUNT(*) FROM REF.VW_PAYMENT_TYPE_SIMPLE;
SELECT @TripTypeCount = COUNT(*) FROM REF.TRIP_TYPE;

PRINT 'Dados de Referência:';
PRINT '  • Rate Codes: ' + CAST(@RateCodeCount AS VARCHAR);
PRINT '  • Payment Types: ' + CAST(@PaymentTypeCount AS VARCHAR);
PRINT '  • Trip Types: ' + CAST(@TripTypeCount AS VARCHAR);
PRINT '';

IF @RateCodeCount = 0 OR @PaymentTypeCount = 0 OR @TripTypeCount = 0
BEGIN
    PRINT '❌ ERRO: Dados de referência ausentes';
    PRINT '   Execute primeiro: 01-load-reference-data.sql';
    RETURN;
END

-- ============================================================================
-- REQUISITO 6: CONSTRUIR GOLD.TRIP_DATA_CSV (Enriched com JOINs)
-- ============================================================================
PRINT '--- REQUISITO 6: Construindo GOLD.TRIP_DATA_CSV (Enriched) ---';
PRINT '    • JOIN com REF.RATE_CODE';
PRINT '    • JOIN com REF.PAYMENT_TYPE';
PRINT '    • JOIN com REF.TRIP_TYPE';
PRINT '    • Calculando métricas de negócio';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- Limpar Gold table
    TRUNCATE TABLE GOLD.TRIP_DATA_CSV;
    
    PRINT '🗑️  GOLD.TRIP_DATA_CSV limpa';
    PRINT '';
    
    -- Construir Gold enriquecida
    INSERT INTO GOLD.TRIP_DATA_CSV (
        -- Campos originais
        VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
        PULocationID, DOLocationID, passenger_count, trip_distance,
        fare_amount, extra, mta_tax, tip_amount, tolls_amount,
        improvement_surcharge, total_amount, congestion_surcharge,
        
        -- Campos enriquecidos (JOINs com referências)
        rate_code, rate_code_type, is_airport_trip,
        payment_type_desc, is_electronic_payment, is_cash_payment,
        trip_type_desc,
        
        -- Métricas de negócio calculadas
        trip_duration_minutes, trip_speed_mph, fare_per_mile,
        fare_per_minute, tip_percentage, total_surcharges,
        
        -- Dimensões temporais
        pickup_hour, pickup_day_of_week, pickup_month, pickup_quarter,
        is_weekend, is_rush_hour,
        
        -- Categorização de viagens
        trip_distance_category, fare_category, duration_category,
        
        -- Metadados
        data_quality_score, processed_timestamp
    )
    SELECT 
        -- ====================================================================
        -- CAMPOS ORIGINAIS DE SILVER
        -- ====================================================================
        s.VendorID,
        s.lpep_pickup_datetime,
        s.lpep_dropoff_datetime,
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
        s.congestion_surcharge,
        
        -- ====================================================================
        -- CAMPOS ENRIQUECIDOS (REQUISITO 6: JOINs com Tabelas de Referência)
        -- ====================================================================
        
        -- De REF.RATE_CODE
        ISNULL(rc.rate_code, 'Unknown') as rate_code,
        ISNULL(rc.rate_type, 'Unknown') as rate_code_type,
        ISNULL(rc.is_airport_rate, 0) as is_airport_trip,
        
        -- De REF.PAYMENT_TYPE
        ISNULL(pt.payment_type_desc, 'Unknown') as payment_type_desc,
        ISNULL(pt.is_electronic, 0) as is_electronic_payment,
        ISNULL(pt.is_cash, 0) as is_cash_payment,
        
        -- De REF.TRIP_TYPE
        ISNULL(tt.trip_type_desc, 'Unknown') as trip_type_desc,
        
        -- ====================================================================
        -- MÉTRICAS DE NEGÓCIO CALCULADAS
        -- ====================================================================
        
        -- Duração da viagem em minutos
        DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) as trip_duration_minutes,
        
        -- Velocidade média em mph
        CASE 
            WHEN DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) > 0
            THEN (s.trip_distance * 60.0) / DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime)
            ELSE 0
        END as trip_speed_mph,
        
        -- Tarifa por milha
        CASE 
            WHEN s.trip_distance > 0 THEN s.fare_amount / s.trip_distance
            ELSE 0
        END as fare_per_mile,
        
        -- Tarifa por minuto
        CASE 
            WHEN DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) > 0
            THEN s.fare_amount / DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime)
            ELSE 0
        END as fare_per_minute,
        
        -- Percentual de gorjeta
        CASE 
            WHEN s.fare_amount > 0 THEN (s.tip_amount * 100.0) / s.fare_amount
            ELSE 0
        END as tip_percentage,
        
        -- Total de sobretaxas
        ISNULL(s.extra, 0) + ISNULL(s.mta_tax, 0) + 
        ISNULL(s.improvement_surcharge, 0) + ISNULL(s.congestion_surcharge, 0) as total_surcharges,
        
        -- ====================================================================
        -- DIMENSÕES TEMPORAIS
        -- ====================================================================
        
        DATEPART(HOUR, s.lpep_pickup_datetime) as pickup_hour,
        DATEPART(WEEKDAY, s.lpep_pickup_datetime) as pickup_day_of_week,
        DATEPART(MONTH, s.lpep_pickup_datetime) as pickup_month,
        DATEPART(QUARTER, s.lpep_pickup_datetime) as pickup_quarter,
        
        -- É fim de semana?
        CASE 
            WHEN DATEPART(WEEKDAY, s.lpep_pickup_datetime) IN (1, 7) THEN 1
            ELSE 0
        END as is_weekend,
        
        -- É hora de pico? (7-10am, 4-7pm)
        CASE 
            WHEN DATEPART(HOUR, s.lpep_pickup_datetime) BETWEEN 7 AND 10 THEN 1
            WHEN DATEPART(HOUR, s.lpep_pickup_datetime) BETWEEN 16 AND 19 THEN 1
            ELSE 0
        END as is_rush_hour,
        
        -- ====================================================================
        -- CATEGORIZAÇÃO DE VIAGENS
        -- ====================================================================
        
        -- Categoria de distância
        CASE 
            WHEN s.trip_distance < 1 THEN 'Very Short (<1mi)'
            WHEN s.trip_distance < 3 THEN 'Short (1-3mi)'
            WHEN s.trip_distance < 10 THEN 'Medium (3-10mi)'
            WHEN s.trip_distance < 20 THEN 'Long (10-20mi)'
            ELSE 'Very Long (>20mi)'
        END as trip_distance_category,
        
        -- Categoria de tarifa
        CASE 
            WHEN s.total_amount < 10 THEN 'Budget (<$10)'
            WHEN s.total_amount < 20 THEN 'Standard ($10-20)'
            WHEN s.total_amount < 50 THEN 'Premium ($20-50)'
            ELSE 'Luxury (>$50)'
        END as fare_category,
        
        -- Categoria de duração
        CASE 
            WHEN DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) < 10 THEN 'Quick (<10min)'
            WHEN DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) < 30 THEN 'Normal (10-30min)'
            WHEN DATEDIFF(MINUTE, s.lpep_pickup_datetime, s.lpep_dropoff_datetime) < 60 THEN 'Long (30-60min)'
            ELSE 'Very Long (>60min)'
        END as duration_category,
        
        -- ====================================================================
        -- METADADOS
        -- ====================================================================
        
        -- Score de qualidade de dados (100 = perfeito)
        100 - 
        (CASE WHEN rc.rate_code_id IS NULL THEN 10 ELSE 0 END) -
        (CASE WHEN pt.payment_type IS NULL THEN 10 ELSE 0 END) -
        (CASE WHEN tt.trip_type IS NULL THEN 10 ELSE 0 END) -
        (CASE WHEN s.passenger_count IS NULL OR s.passenger_count = 0 THEN 5 ELSE 0 END) as data_quality_score,
        
        GETDATE() as processed_timestamp
        
    FROM SILVER.TRIP_DATA_CSV s
    
    -- REQUISITO 6: JOINs com Tabelas de Referência
    LEFT JOIN REF.RATE_CODE rc ON s.RatecodeID = rc.rate_code_id
    LEFT JOIN REF.VW_PAYMENT_TYPE_SIMPLE pt ON s.payment_type = pt.payment_type
    LEFT JOIN REF.TRIP_TYPE tt ON s.trip_type = tt.trip_type
    
    WHERE s.quality_flag = 'VALID';  -- Somente registros válidos no Gold
    
    SET @RecordsCreated = @@ROWCOUNT;
    
    COMMIT TRANSACTION;
    
    PRINT '✅ GOLD.TRIP_DATA_CSV criada com sucesso';
    PRINT '   • Registros inseridos: ' + CAST(@RecordsCreated AS VARCHAR);
    PRINT '   • JOINs realizados: Rate Code, Payment Type, Trip Type';
    PRINT '   • Métricas calculadas: 6 métricas de negócio';
    PRINT '   • Dimensões temporais: 6 dimensões';
    PRINT '   • Categorias: 3 categorizações';
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    PRINT '❌ ERRO: ' + ERROR_MESSAGE();
    THROW;
END CATCH;

-- ============================================================================
-- ESTATÍSTICAS DA GOLD LAYER
-- ============================================================================
PRINT '--- Estatísticas da Gold Layer Enriched ---';
PRINT '';

-- Distribuição por tipo de pagamento
PRINT 'Distribuição por Tipo de Pagamento:';
SELECT 
    payment_type_desc,
    COUNT(*) as trip_count,
    CAST(AVG(total_amount) AS DECIMAL(10,2)) as avg_fare,
    CAST(AVG(tip_percentage) AS DECIMAL(5,2)) as avg_tip_pct
FROM GOLD.TRIP_DATA_CSV
GROUP BY payment_type_desc
ORDER BY trip_count DESC;

PRINT '';

-- Distribuição por categoria de distância
PRINT 'Distribuição por Categoria de Distância:';
SELECT 
    trip_distance_category,
    COUNT(*) as trip_count,
    CAST(AVG(fare_per_mile) AS DECIMAL(10,2)) as avg_fare_per_mile
FROM GOLD.TRIP_DATA_CSV
GROUP BY trip_distance_category
ORDER BY 
    CASE trip_distance_category
        WHEN 'Very Short (<1mi)' THEN 1
        WHEN 'Short (1-3mi)' THEN 2
        WHEN 'Medium (3-10mi)' THEN 3
        WHEN 'Long (10-20mi)' THEN 4
        WHEN 'Very Long (>20mi)' THEN 5
    END;

PRINT '';

-- Score médio de qualidade
DECLARE @AvgQualityScore DECIMAL(5,2);
SELECT @AvgQualityScore = AVG(data_quality_score) FROM GOLD.TRIP_DATA_CSV;

PRINT 'Score Médio de Qualidade: ' + CAST(@AvgQualityScore AS VARCHAR) + '/100';
PRINT '';

-- ============================================================================
-- SUMÁRIO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'GOLD LAYER ENRICHED COMPLETA';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas:';
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '  • Registros criados: ' + CAST(@RecordsCreated AS VARCHAR);
PRINT '  • Score médio de qualidade: ' + CAST(@AvgQualityScore AS VARCHAR) + '/100';
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 6: GOLD.TRIP_DATA_CSV (Enriched)';
PRINT '      • JOIN com REF.RATE_CODE';
PRINT '      • JOIN com REF.PAYMENT_TYPE';
PRINT '      • JOIN com REF.TRIP_TYPE';
PRINT '      • 15+ campos enriquecidos';
PRINT '      • 6 métricas de negócio';
PRINT '      • 6 dimensões temporais';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 07-build-gold-aggregated.sql (criar Gold aggregated)';
PRINT '============================================================================';

SET NOCOUNT OFF;
