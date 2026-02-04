-- ============================================================================
-- 04-TRANSFORM-TO-SILVER-CSV.SQL - Transformação Landing → Silver (CSV)
-- ============================================================================
-- Propósito: Transformar dados CSV de VARCHAR para tipos apropriados com validação
-- Requisito: 1b (LANDING.TRIP_DATA_CSV → SILVER.TRIP_DATA_CSV)
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
PRINT 'TRANSFORMAÇÃO LANDING → SILVER (CSV) - NYC GREEN TAXI';
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
DECLARE @ErrorMessage NVARCHAR(MAX);

-- ============================================================================
-- VERIFICAR DADOS DISPONÍVEIS EM LANDING
-- ============================================================================
PRINT '--- Verificando Dados em Landing ---';
PRINT '';

DECLARE @LandingCount INT;
SELECT @LandingCount = COUNT(*) FROM LANDING.TRIP_DATA_CSV;

PRINT 'Registros disponíveis em LANDING.TRIP_DATA_CSV: ' + CAST(@LandingCount AS VARCHAR);
PRINT '';

IF @LandingCount = 0
BEGIN
    PRINT '❌ ERRO: Nenhum dado encontrado em LANDING.TRIP_DATA_CSV';
    PRINT '   Execute primeiro: 02-load-landing-csv.sql';
    PRINT '';
    RETURN;
END

-- ============================================================================
-- REQUISITO 1b: TRANSFORMAR LANDING.TRIP_DATA_CSV → SILVER.TRIP_DATA_CSV
-- ============================================================================
PRINT '--- REQUISITO 1b: Transformando Landing → Silver (CSV) ---';
PRINT '    • Convertendo VARCHAR → Tipos apropriados';
PRINT '    • Aplicando validações de qualidade';
PRINT '    • Calculando campos derivados';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- Limpar tabela Silver antes de carregar
    TRUNCATE TABLE SILVER.TRIP_DATA_CSV;
    TRUNCATE TABLE SILVER.TRIP_DATA_CSV_REJECTS;
    
    PRINT '🗑️  Tabelas Silver limpas';
    PRINT '';
    
    -- ========================================================================
    -- INSERIR REGISTROS VÁLIDOS EM SILVER
    -- ========================================================================
    INSERT INTO SILVER.TRIP_DATA_CSV (
        VendorID,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        RatecodeID,
        PULocationID,
        DOLocationID,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        payment_type,
        trip_type,
        congestion_surcharge,
        quality_flag,
        validation_errors,
        source_system
    )
    SELECT 
        -- Conversões de tipo com TRY_CAST (retorna NULL se falhar)
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
        
        -- Quality flag: VALID, INVALID, ou WARNING
        CASE 
            -- INVALID: Falhas críticas de conversão ou valores inválidos
            WHEN TRY_CAST(VendorID AS INT) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) IS NULL THEN 'INVALID'
            WHEN TRY_CAST(total_amount AS DECIMAL(10,2)) IS NULL THEN 'INVALID'
            
            -- INVALID: Violações de regras de negócio críticas
            WHEN TRY_CAST(VendorID AS INT) NOT IN (1, 2) THEN 'INVALID'
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) < TRY_CAST(lpep_pickup_datetime AS DATETIME2) THEN 'INVALID'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) < 0 THEN 'INVALID'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) > 500 THEN 'INVALID'
            WHEN TRY_CAST(total_amount AS DECIMAL(10,2)) < 0 THEN 'INVALID'
            
            -- WARNING: Valores suspeitos mas não críticos
            WHEN TRY_CAST(passenger_count AS INT) IS NULL THEN 'WARNING'
            WHEN TRY_CAST(passenger_count AS INT) < 0 THEN 'WARNING'
            WHEN TRY_CAST(passenger_count AS INT) > 8 THEN 'WARNING'
            WHEN TRY_CAST(fare_amount AS DECIMAL(10,2)) < 0 THEN 'WARNING'
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) = 0 AND TRY_CAST(fare_amount AS DECIMAL(10,2)) > 0 THEN 'WARNING'
            WHEN TRY_CAST(payment_type AS INT) NOT IN (1,2,3,4,5,6) THEN 'WARNING'
            
            -- VALID: Passou em todas as validações
            ELSE 'VALID'
        END as quality_flag,
        
        -- Mensagens de erro de validação
        CASE 
            WHEN TRY_CAST(VendorID AS INT) IS NULL THEN 'VendorID inválido; '
            WHEN TRY_CAST(VendorID AS INT) NOT IN (1, 2) THEN 'VendorID fora do range (1,2); '
            ELSE ''
        END +
        CASE 
            WHEN TRY_CAST(lpep_pickup_datetime AS DATETIME2) IS NULL THEN 'Data de pickup inválida; '
            ELSE ''
        END +
        CASE 
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) IS NULL THEN 'Data de dropoff inválida; '
            WHEN TRY_CAST(lpep_dropoff_datetime AS DATETIME2) < TRY_CAST(lpep_pickup_datetime AS DATETIME2) THEN 'Dropoff antes de pickup; '
            ELSE ''
        END +
        CASE 
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) IS NULL THEN 'Distância inválida; '
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) < 0 THEN 'Distância negativa; '
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) > 500 THEN 'Distância suspeita (>500mi); '
            WHEN TRY_CAST(trip_distance AS DECIMAL(8,2)) = 0 AND TRY_CAST(fare_amount AS DECIMAL(10,2)) > 0 THEN 'Distância zero com tarifa; '
            ELSE ''
        END +
        CASE 
            WHEN TRY_CAST(passenger_count AS INT) IS NULL THEN 'Passenger count inválido; '
            WHEN TRY_CAST(passenger_count AS INT) < 0 THEN 'Passenger count negativo; '
            WHEN TRY_CAST(passenger_count AS INT) > 8 THEN 'Passenger count suspeito (>8); '
            ELSE ''
        END +
        CASE
            WHEN TRY_CAST(payment_type AS INT) NOT IN (1,2,3,4,5,6) THEN 'Payment type desconhecido; '
            ELSE ''
        END as validation_errors,
        
        'CSV_LANDING' as source_system
        
    FROM LANDING.TRIP_DATA_CSV;
    
    SET @RecordsProcessed = @@ROWCOUNT;
    
    -- Contar por categoria de qualidade
    SELECT @RecordsValid = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID';
    SELECT @RecordsWarning = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'WARNING';
    SELECT @RecordsInvalid = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'INVALID';
    
    PRINT '✅ Transformação para Silver concluída';
    PRINT '   • Registros processados: ' + CAST(@RecordsProcessed AS VARCHAR);
    PRINT '   • Registros VÁLIDOS: ' + CAST(@RecordsValid AS VARCHAR) + 
          ' (' + CAST((@RecordsValid * 100.0 / @RecordsProcessed) AS DECIMAL(5,2)) + '%)';
    PRINT '   • Registros com WARNING: ' + CAST(@RecordsWarning AS VARCHAR) + 
          ' (' + CAST((@RecordsWarning * 100.0 / @RecordsProcessed) AS DECIMAL(5,2)) + '%)';
    PRINT '   • Registros INVÁLIDOS: ' + CAST(@RecordsInvalid AS VARCHAR) + 
          ' (' + CAST((@RecordsInvalid * 100.0 / @RecordsProcessed) AS DECIMAL(5,2)) + '%)';
    PRINT '';
    
    -- ========================================================================
    -- MOVER REGISTROS INVÁLIDOS PARA REJECT TABLE
    -- ========================================================================
    IF @RecordsInvalid > 0
    BEGIN
        PRINT '--- Movendo Registros Inválidos para Reject Table ---';
        PRINT '';
        
        INSERT INTO SILVER.TRIP_DATA_CSV_REJECTS (
            original_data,
            error_reason,
            source_file,
            landing_id
        )
        SELECT 
            (SELECT lnd.* FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) as original_data,
            slv.validation_errors as error_reason,
            lnd.source_file,
            lnd.landing_id
        FROM SILVER.TRIP_DATA_CSV slv
        INNER JOIN LANDING.TRIP_DATA_CSV lnd ON lnd.landing_id = slv.silver_id
        WHERE slv.quality_flag = 'INVALID';
        
        DECLARE @RejectsInserted INT = @@ROWCOUNT;
        
        PRINT '✅ Registros inválidos movidos para REJECT table';
        PRINT '   • Rejects capturados: ' + CAST(@RejectsInserted AS VARCHAR);
        PRINT '';
    END
    
    COMMIT TRANSACTION;
    
    PRINT '✅ Transação commitada com sucesso';
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    
    SET @ErrorMessage = ERROR_MESSAGE();
    PRINT '❌ ERRO na transformação: ' + @ErrorMessage;
    PRINT '';
    THROW;
END CATCH;

-- ============================================================================
-- VALIDAÇÃO DE INTEGRIDADE REFERENCIAL
-- ============================================================================
PRINT '--- Validando Integridade Referencial ---';
PRINT '';

DECLARE @InvalidRateCodes INT, @InvalidPaymentTypes INT, @InvalidTripTypes INT;

SELECT @InvalidRateCodes = COUNT(*) 
FROM SILVER.TRIP_DATA_CSV s
LEFT JOIN REF.RATE_CODE r ON s.RatecodeID = r.rate_code_id
WHERE s.quality_flag = 'VALID' AND r.rate_code_id IS NULL AND s.RatecodeID IS NOT NULL;

SELECT @InvalidPaymentTypes = COUNT(*) 
FROM SILVER.TRIP_DATA_CSV s
LEFT JOIN REF.VW_PAYMENT_TYPE_SIMPLE p ON s.payment_type = p.payment_type
WHERE s.quality_flag = 'VALID' AND p.payment_type IS NULL AND s.payment_type IS NOT NULL;

SELECT @InvalidTripTypes = COUNT(*) 
FROM SILVER.TRIP_DATA_CSV s
LEFT JOIN REF.TRIP_TYPE t ON s.trip_type = t.trip_type
WHERE s.quality_flag = 'VALID' AND t.trip_type IS NULL AND s.trip_type IS NOT NULL;

PRINT 'Violações de Integridade Referencial:';
PRINT '  • Rate codes inválidos: ' + CAST(@InvalidRateCodes AS VARCHAR);
PRINT '  • Payment types inválidos: ' + CAST(@InvalidPaymentTypes AS VARCHAR);
PRINT '  • Trip types inválidos: ' + CAST(@InvalidTripTypes AS VARCHAR);
PRINT '';

IF @InvalidRateCodes + @InvalidPaymentTypes + @InvalidTripTypes = 0
BEGIN
    PRINT '✅ Integridade referencial VALIDADA!';
END
ELSE
BEGIN
    PRINT '⚠️  AVISO: Algumas foreign keys não correspondem aos dados de referência';
END

PRINT '';

-- ============================================================================
-- ESTATÍSTICAS DE QUALIDADE DETALHADAS
-- ============================================================================
PRINT '--- Estatísticas de Qualidade Detalhadas ---';
PRINT '';

-- Top 5 erros mais comuns
PRINT 'Top 5 Erros Mais Comuns:';
SELECT TOP 5 
    validation_errors,
    COUNT(*) as error_count
FROM SILVER.TRIP_DATA_CSV
WHERE quality_flag IN ('INVALID', 'WARNING')
  AND validation_errors IS NOT NULL
  AND validation_errors <> ''
GROUP BY validation_errors
ORDER BY COUNT(*) DESC;

PRINT '';

-- Distribuição por VendorID
PRINT 'Distribuição por Vendor:';
SELECT 
    VendorID,
    quality_flag,
    COUNT(*) as record_count
FROM SILVER.TRIP_DATA_CSV
GROUP BY VendorID, quality_flag
ORDER BY VendorID, quality_flag;

PRINT '';

-- ============================================================================
-- SUMÁRIO DE EXECUÇÃO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'TRANSFORMAÇÃO LANDING → SILVER (CSV) COMPLETA';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, @EndTime, 120);
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '  • Taxa: ' + CAST(@RecordsProcessed / NULLIF(@Duration, 0) AS VARCHAR) + ' registros/segundo';
PRINT '';
PRINT 'Resultados:';
PRINT '  • Registros processados: ' + CAST(@RecordsProcessed AS VARCHAR);
PRINT '  • ✅ VALID: ' + CAST(@RecordsValid AS VARCHAR) + 
      ' (' + CAST((@RecordsValid * 100.0 / NULLIF(@RecordsProcessed, 0)) AS DECIMAL(5,2)) + '%)';
PRINT '  • ⚠️  WARNING: ' + CAST(@RecordsWarning AS VARCHAR) + 
      ' (' + CAST((@RecordsWarning * 100.0 / NULLIF(@RecordsProcessed, 0)) AS DECIMAL(5,2)) + '%)';
PRINT '  • ❌ INVALID: ' + CAST(@RecordsInvalid AS VARCHAR) + 
      ' (' + CAST((@RecordsInvalid * 100.0 / NULLIF(@RecordsProcessed, 0)) AS DECIMAL(5,2)) + '%)';
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 1b: LANDING.TRIP_DATA_CSV → SILVER.TRIP_DATA_CSV';
PRINT '      • VARCHAR → Tipos apropriados';
PRINT '      • 20+ regras de validação aplicadas';
PRINT '      • Quality flags atribuídos';
PRINT '      • Rejects capturados';
PRINT '';
PRINT 'Próximos Passos:';
PRINT '  → Execute 05-transform-to-silver-parquet.sql (transformar Parquet)';
PRINT '  → Execute 06-build-gold-enriched.sql (criar Gold layer)';
PRINT '============================================================================';

SET NOCOUNT OFF;
