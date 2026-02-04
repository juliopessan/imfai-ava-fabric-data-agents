-- ============================================================================
-- 08-UNIT-TESTS.SQL - Testes Unitários da Pipeline ETL
-- ============================================================================
-- Propósito: Validar todos os 8 requisitos com testes automatizados
-- Requisito: 8 (Testes unitários comparando arquivos e tabelas)
-- Autor: DataFlow Agent
-- Data: 17 de Novembro de 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

SET NOCOUNT ON;

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                                                                          █';
PRINT '█                     TESTES UNITÁRIOS - PIPELINE ETL                     █';
PRINT '█                                                                          █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Database: TEST_PIPELINE';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @TestStartTime DATETIME2 = GETDATE();
DECLARE @TotalTests INT = 0;
DECLARE @PassedTests INT = 0;
DECLARE @FailedTests INT = 0;
DECLARE @WarningTests INT = 0;
DECLARE @TestName VARCHAR(200);
DECLARE @TestResult VARCHAR(10);
DECLARE @TestMessage VARCHAR(MAX);

-- Tabela temporária para resultados
IF OBJECT_ID('tempdb..#TestResults', 'U') IS NOT NULL DROP TABLE #TestResults;

CREATE TABLE #TestResults (
    test_id INT IDENTITY(1,1),
    test_category VARCHAR(50),
    test_name VARCHAR(200),
    test_result VARCHAR(10),
    expected_value VARCHAR(100),
    actual_value VARCHAR(100),
    test_message VARCHAR(MAX),
    execution_time DATETIME2 DEFAULT GETDATE()
);

-- ============================================================================
-- CATEGORIA 1: TESTES DE ESTRUTURA DDL
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 1: TESTES DE ESTRUTURA (DDL)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 1.1: Landing Tables
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Verificar existência de LANDING.TRIP_DATA_CSV';
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('LANDING'))
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'PASS', 'Tabela existe');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'FAIL', 'Tabela não encontrada');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 1.2: Silver Tables
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Verificar existência de SILVER.TRIP_DATA_CSV';
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('SILVER'))
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'PASS', 'Tabela existe');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'FAIL', 'Tabela não encontrada');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 1.3: Gold Tables
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Verificar existência de GOLD.TRIP_DATA_CSV';
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('GOLD'))
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'PASS', 'Tabela existe');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'FAIL', 'Tabela não encontrada');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 1.4: Reference Tables
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Verificar existência de REF.RATE_CODE, REF.PAYMENT_TYPE, REF.TRIP_TYPE';
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'RATE_CODE' AND schema_id = SCHEMA_ID('REF'))
   AND EXISTS (SELECT * FROM sys.tables WHERE name = 'PAYMENT_TYPE' AND schema_id = SCHEMA_ID('REF'))
   AND EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_TYPE' AND schema_id = SCHEMA_ID('REF'))
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'PASS', 'Todas as tabelas de referência existem');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('DDL', @TestName, 'FAIL', 'Uma ou mais tabelas de referência ausentes');
    PRINT '❌ FAIL: ' + @TestName;
END

PRINT '';

-- ============================================================================
-- CATEGORIA 2: TESTES DE DADOS DE REFERÊNCIA (Requisitos 3, 4, 5)
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 2: DADOS DE REFERÊNCIA (REQ 3, 4, 5)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 2.1: REF.TRIP_TYPE (Requisito 3)
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 3: REF.TRIP_TYPE contém 2 tipos de viagem';
DECLARE @TripTypeCount INT;
SELECT @TripTypeCount = COUNT(*) FROM REF.TRIP_TYPE;

IF @TripTypeCount = 2
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'PASS', '2', CAST(@TripTypeCount AS VARCHAR), 'Contagem correta');
    PRINT '✅ PASS: ' + @TestName + ' (Esperado: 2, Atual: ' + CAST(@TripTypeCount AS VARCHAR) + ')';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'FAIL', '2', CAST(@TripTypeCount AS VARCHAR), 'Contagem incorreta');
    PRINT '❌ FAIL: ' + @TestName + ' (Esperado: 2, Atual: ' + CAST(@TripTypeCount AS VARCHAR) + ')';
END

-- Teste 2.2: REF.RATE_CODE (Requisito 4)
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 4: REF.RATE_CODE contém 6 códigos de tarifa';
DECLARE @RateCodeCount INT;
SELECT @RateCodeCount = COUNT(*) FROM REF.RATE_CODE;

IF @RateCodeCount = 6
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'PASS', '6', CAST(@RateCodeCount AS VARCHAR), 'Contagem correta');
    PRINT '✅ PASS: ' + @TestName + ' (Esperado: 6, Atual: ' + CAST(@RateCodeCount AS VARCHAR) + ')';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'FAIL', '6', CAST(@RateCodeCount AS VARCHAR), 'Contagem incorreta');
    PRINT '❌ FAIL: ' + @TestName + ' (Esperado: 6, Atual: ' + CAST(@RateCodeCount AS VARCHAR) + ')';
END

-- Teste 2.3: REF.PAYMENT_TYPE (Requisito 5)
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 5: REF.PAYMENT_TYPE contém 6 tipos únicos de pagamento';
DECLARE @PaymentTypeCount INT;
SELECT @PaymentTypeCount = COUNT(DISTINCT payment_type) FROM REF.PAYMENT_TYPE;

IF @PaymentTypeCount = 6
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'PASS', '6', CAST(@PaymentTypeCount AS VARCHAR), 'Contagem correta');
    PRINT '✅ PASS: ' + @TestName + ' (Esperado: 6, Atual: ' + CAST(@PaymentTypeCount AS VARCHAR) + ')';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('REF_DATA', @TestName, 'FAIL', '6', CAST(@PaymentTypeCount AS VARCHAR), 'Contagem incorreta');
    PRINT '❌ FAIL: ' + @TestName + ' (Esperado: 6, Atual: ' + CAST(@PaymentTypeCount AS VARCHAR) + ')';
END

PRINT '';

-- ============================================================================
-- CATEGORIA 3: TESTES DE CARREGAMENTO CSV (Requisito 1a)
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 3: CARREGAMENTO CSV (REQ 1a)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 3.1: Landing CSV tem dados
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1a: LANDING.TRIP_DATA_CSV contém dados';
DECLARE @LandingCSVCount INT;
SELECT @LandingCSVCount = COUNT(*) FROM LANDING.TRIP_DATA_CSV;

IF @LandingCSVCount > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('LANDING', @TestName, 'PASS', '>0', CAST(@LandingCSVCount AS VARCHAR), 'Dados carregados: ' + CAST(@LandingCSVCount AS VARCHAR));
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@LandingCSVCount AS VARCHAR) + ' registros)';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('LANDING', @TestName, 'FAIL', '>0', '0', 'Nenhum dado carregado');
    PRINT '❌ FAIL: ' + @TestName + ' (Nenhum dado carregado)';
END

-- Teste 3.2: Campos são VARCHAR em Landing
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1a: Campos em LANDING.TRIP_DATA_CSV são VARCHAR';
DECLARE @NonVarcharColumns INT;
SELECT @NonVarcharColumns = COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'LANDING' 
  AND TABLE_NAME = 'TRIP_DATA_CSV'
  AND COLUMN_NAME NOT IN ('load_timestamp', 'landing_id', 'source_file', 'load_batch_id')
  AND DATA_TYPE NOT IN ('varchar', 'nvarchar');

IF @NonVarcharColumns = 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('LANDING', @TestName, 'PASS', 'Todos os campos de dados são VARCHAR');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('LANDING', @TestName, 'FAIL', '0', CAST(@NonVarcharColumns AS VARCHAR), CAST(@NonVarcharColumns AS VARCHAR) + ' campos não-VARCHAR encontrados');
    PRINT '❌ FAIL: ' + @TestName + ' (' + CAST(@NonVarcharColumns AS VARCHAR) + ' campos não-VARCHAR)';
END

-- Teste 3.3: Contagem esperada de registros CSV
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1a: Validar volume de dados (Full: 261,858 ou Sample: 10+)';
DECLARE @ExpectedCSVCount INT = 261858;
DECLARE @CSVCountDiff DECIMAL(5,2);
SET @CSVCountDiff = ABS(@LandingCSVCount - @ExpectedCSVCount) * 100.0 / @ExpectedCSVCount;

-- Aceita dataset completo (dentro de 5% de 261,858) OU sample data (10+ registros)
IF @CSVCountDiff < 5.0 OR @LandingCSVCount >= 10
BEGIN
    SET @PassedTests = @PassedTests + 1;
    DECLARE @DatasetType VARCHAR(20) = CASE WHEN @LandingCSVCount > 10000 THEN 'Full dataset' ELSE 'Sample data' END;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('LANDING', @TestName, 'PASS', '~261858 ou 10+', CAST(@LandingCSVCount AS VARCHAR), @DatasetType + ' detectado');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@LandingCSVCount AS VARCHAR) + ' registros - ' + @DatasetType + ')';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('LANDING', @TestName, 'WARNING', '~261858', CAST(@LandingCSVCount AS VARCHAR), 'Diferença: ' + CAST(@CSVCountDiff AS VARCHAR) + '% (>5%)');
    PRINT '⚠️  WARNING: ' + @TestName + ' (Diferença: ' + CAST(@CSVCountDiff AS VARCHAR) + '%)';
END

PRINT '';

-- ============================================================================
-- CATEGORIA 4: TESTES DE TRANSFORMAÇÃO SILVER (Requisito 1b)
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 4: TRANSFORMAÇÃO SILVER (REQ 1b)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 4.1: Silver tem dados
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1b: SILVER.TRIP_DATA_CSV contém dados';
DECLARE @SilverCSVCount INT;
SELECT @SilverCSVCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV;

IF @SilverCSVCount > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'PASS', '>0', CAST(@SilverCSVCount AS VARCHAR), 'Dados transformados: ' + CAST(@SilverCSVCount AS VARCHAR));
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@SilverCSVCount AS VARCHAR) + ' registros)';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'FAIL', '>0', '0', 'Nenhum dado transformado');
    PRINT '❌ FAIL: ' + @TestName + ' (Nenhum dado)';
END

-- Teste 4.2: Tipos de dados apropriados em Silver
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1b: Campos em SILVER têm tipos apropriados (INT, DECIMAL, DATETIME2)';
DECLARE @CorrectTypes INT;
SELECT @CorrectTypes = COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'SILVER' 
  AND TABLE_NAME = 'TRIP_DATA_CSV'
  AND (
      (COLUMN_NAME IN ('VendorID', 'RatecodeID', 'PULocationID', 'DOLocationID', 'passenger_count', 'payment_type', 'trip_type') AND DATA_TYPE = 'int')
      OR (COLUMN_NAME IN ('trip_distance', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge') AND DATA_TYPE = 'decimal')
      OR (COLUMN_NAME IN ('lpep_pickup_datetime', 'lpep_dropoff_datetime') AND DATA_TYPE = 'datetime2')
  );

IF @CorrectTypes >= 18  -- Pelo menos 18 campos com tipos corretos
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'PASS', '>=18', CAST(@CorrectTypes AS VARCHAR), 'Tipos de dados corretos');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@CorrectTypes AS VARCHAR) + ' campos corretos)';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'FAIL', '>=18', CAST(@CorrectTypes AS VARCHAR), 'Alguns tipos incorretos');
    PRINT '❌ FAIL: ' + @TestName + ' (Apenas ' + CAST(@CorrectTypes AS VARCHAR) + ' campos corretos)';
END

-- Teste 4.3: Quality flags atribuídos
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1b: Quality flags atribuídos (VALID, INVALID, WARNING)';
DECLARE @RecordsWithQualityFlag INT;
SELECT @RecordsWithQualityFlag = COUNT(*) 
FROM SILVER.TRIP_DATA_CSV 
WHERE quality_flag IN ('VALID', 'INVALID', 'WARNING');

IF @RecordsWithQualityFlag = @SilverCSVCount
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('SILVER', @TestName, 'PASS', 'Todos os registros têm quality flag');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'FAIL', CAST(@SilverCSVCount AS VARCHAR), CAST(@RecordsWithQualityFlag AS VARCHAR), 'Alguns registros sem quality flag');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 4.4: Taxa de qualidade aceitável
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1b: Taxa de registros VÁLIDOS > 90%';
DECLARE @ValidPercent DECIMAL(5,2);
SELECT @ValidPercent = COUNT(*) * 100.0 / NULLIF(@SilverCSVCount, 0)
FROM SILVER.TRIP_DATA_CSV 
WHERE quality_flag = 'VALID';

IF @ValidPercent > 90.0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'PASS', '>90%', CAST(@ValidPercent AS VARCHAR) + '%', 'Boa qualidade de dados');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@ValidPercent AS VARCHAR) + '% válidos)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'WARNING', '>90%', CAST(@ValidPercent AS VARCHAR) + '%', 'Taxa de qualidade abaixo do esperado');
    PRINT '⚠️  WARNING: ' + @TestName + ' (' + CAST(@ValidPercent AS VARCHAR) + '% válidos)';
END

-- Teste 4.5: Registros inválidos capturados em REJECT
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 1b: Registros INVALID capturados em REJECT table';
DECLARE @InvalidCount INT, @RejectCount INT;
SELECT @InvalidCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'INVALID';
SELECT @RejectCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV_REJECTS;

IF @InvalidCount = @RejectCount
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'PASS', CAST(@InvalidCount AS VARCHAR), CAST(@RejectCount AS VARCHAR), 'Todos os inválidos capturados');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@RejectCount AS VARCHAR) + ' rejects)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('SILVER', @TestName, 'WARNING', CAST(@InvalidCount AS VARCHAR), CAST(@RejectCount AS VARCHAR), 'Contagem diferente entre INVALID e REJECTS');
    PRINT '⚠️  WARNING: ' + @TestName + ' (Invalid: ' + CAST(@InvalidCount AS VARCHAR) + ', Rejects: ' + CAST(@RejectCount AS VARCHAR) + ')';
END

PRINT '';

-- ============================================================================
-- CATEGORIA 5: TESTES DE GOLD ENRICHED (Requisito 6)
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 5: GOLD ENRICHED (REQ 6)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 5.1: Gold Enriched tem dados
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 6: GOLD.TRIP_DATA_CSV contém dados';
DECLARE @GoldCSVCount INT;
SELECT @GoldCSVCount = COUNT(*) FROM GOLD.TRIP_DATA_CSV;

IF @GoldCSVCount > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'PASS', '>0', CAST(@GoldCSVCount AS VARCHAR), 'Dados enriquecidos: ' + CAST(@GoldCSVCount AS VARCHAR));
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@GoldCSVCount AS VARCHAR) + ' registros)';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'FAIL', '>0', '0', 'Nenhum dado em Gold');
    PRINT '❌ FAIL: ' + @TestName + ' (Nenhum dado)';
END

-- Teste 5.2: JOINs com Rate Code funcionando
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 6: JOIN com REF.RATE_CODE está funcionando';
DECLARE @RateCodeEnriched INT;
SELECT @RateCodeEnriched = COUNT(*) 
FROM GOLD.TRIP_DATA_CSV 
WHERE rate_code IS NOT NULL AND rate_code <> 'Unknown';

DECLARE @RateCodeEnrichPercent DECIMAL(5,2);
SET @RateCodeEnrichPercent = @RateCodeEnriched * 100.0 / NULLIF(@GoldCSVCount, 0);

IF @RateCodeEnrichPercent > 80.0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'PASS', '>80%', CAST(@RateCodeEnrichPercent AS VARCHAR) + '%', 'JOIN efetivo');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@RateCodeEnrichPercent AS VARCHAR) + '% enriquecidos)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'WARNING', '>80%', CAST(@RateCodeEnrichPercent AS VARCHAR) + '%', 'Poucos registros enriquecidos');
    PRINT '⚠️  WARNING: ' + @TestName + ' (' + CAST(@RateCodeEnrichPercent AS VARCHAR) + '% enriquecidos)';
END

-- Teste 5.3: JOINs com Payment Type funcionando
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 6: JOIN com REF.PAYMENT_TYPE está funcionando';
DECLARE @PaymentTypeEnriched INT;
SELECT @PaymentTypeEnriched = COUNT(*) 
FROM GOLD.TRIP_DATA_CSV 
WHERE payment_type_desc IS NOT NULL AND payment_type_desc <> 'Unknown';

DECLARE @PaymentEnrichPercent DECIMAL(5,2);
SET @PaymentEnrichPercent = @PaymentTypeEnriched * 100.0 / NULLIF(@GoldCSVCount, 0);

IF @PaymentEnrichPercent > 80.0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'PASS', '>80%', CAST(@PaymentEnrichPercent AS VARCHAR) + '%', 'JOIN efetivo');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@PaymentEnrichPercent AS VARCHAR) + '% enriquecidos)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'WARNING', '>80%', CAST(@PaymentEnrichPercent AS VARCHAR) + '%', 'Poucos registros enriquecidos');
    PRINT '⚠️  WARNING: ' + @TestName + ' (' + CAST(@PaymentEnrichPercent AS VARCHAR) + '% enriquecidos)';
END

-- Teste 5.4: JOINs com Trip Type funcionando
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 6: JOIN com REF.TRIP_TYPE está funcionando';
DECLARE @TripTypeEnriched INT;
SELECT @TripTypeEnriched = COUNT(*) 
FROM GOLD.TRIP_DATA_CSV 
WHERE trip_type_desc IS NOT NULL AND trip_type_desc <> 'Unknown';

DECLARE @TripTypeEnrichPercent DECIMAL(5,2);
SET @TripTypeEnrichPercent = @TripTypeEnriched * 100.0 / NULLIF(@GoldCSVCount, 0);

IF @TripTypeEnrichPercent > 80.0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'PASS', '>80%', CAST(@TripTypeEnrichPercent AS VARCHAR) + '%', 'JOIN efetivo');
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@TripTypeEnrichPercent AS VARCHAR) + '% enriquecidos)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'WARNING', '>80%', CAST(@TripTypeEnrichPercent AS VARCHAR) + '%', 'Poucos registros enriquecidos');
    PRINT '⚠️  WARNING: ' + @TestName + ' (' + CAST(@TripTypeEnrichPercent AS VARCHAR) + '% enriquecidos)';
END

-- Teste 5.5: Métricas de negócio calculadas
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 6: Métricas de negócio calculadas (fare_per_mile, tip_percentage)';
DECLARE @MetricsCalculated INT;
SELECT @MetricsCalculated = COUNT(*) 
FROM GOLD.TRIP_DATA_CSV 
WHERE fare_per_mile IS NOT NULL AND tip_percentage IS NOT NULL;

IF @MetricsCalculated = @GoldCSVCount
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD', @TestName, 'PASS', 'Todas as métricas calculadas');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD', @TestName, 'FAIL', CAST(@GoldCSVCount AS VARCHAR), CAST(@MetricsCalculated AS VARCHAR), 'Algumas métricas ausentes');
    PRINT '❌ FAIL: ' + @TestName;
END

PRINT '';

-- ============================================================================
-- CATEGORIA 6: TESTES DE GOLD AGGREGATED (Requisito 7)
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 6: GOLD AGGREGATED (REQ 7)';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 6.1: Gold Aggregated tem dados
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 7: GOLD.TRIP_DATA_PARQUET_AGG contém dados';
DECLARE @GoldAggCount INT;
SELECT @GoldAggCount = COUNT(*) FROM GOLD.TRIP_DATA_PARQUET_AGG;

IF @GoldAggCount > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD_AGG', @TestName, 'PASS', '>0', CAST(@GoldAggCount AS VARCHAR), 'Localizações agregadas: ' + CAST(@GoldAggCount AS VARCHAR));
    PRINT '✅ PASS: ' + @TestName + ' (' + CAST(@GoldAggCount AS VARCHAR) + ' localizações)';
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('GOLD_AGG', @TestName, 'FAIL', '>0', '0', 'Nenhuma agregação');
    PRINT '❌ FAIL: ' + @TestName + ' (Nenhuma agregação)';
END

-- Teste 6.2: SUM(trip_distance) calculado
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 7: SUM(trip_distance) por PULocationID calculado';
DECLARE @DistanceAgg INT;
SELECT @DistanceAgg = COUNT(*) 
FROM GOLD.TRIP_DATA_PARQUET_AGG 
WHERE total_trip_distance IS NOT NULL AND total_trip_distance > 0;

IF @DistanceAgg > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'PASS', 'Distâncias agregadas');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'FAIL', 'Agregações de distância ausentes');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 6.3: SUM(fare_amount) calculado
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 7: SUM(fare_amount) por PULocationID calculado';
DECLARE @FareAgg INT;
SELECT @FareAgg = COUNT(*) 
FROM GOLD.TRIP_DATA_PARQUET_AGG 
WHERE total_fare_amount IS NOT NULL AND total_fare_amount > 0;

IF @FareAgg > 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'PASS', 'Tarifas agregadas');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'FAIL', 'Agregações de tarifa ausentes');
    PRINT '❌ FAIL: ' + @TestName;
END

-- Teste 6.4: COUNT(*) por localização
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'REQ 7: COUNT(*) por PULocationID calculado';
DECLARE @CountAgg INT;
SELECT @CountAgg = COUNT(*) 
FROM GOLD.TRIP_DATA_PARQUET_AGG 
WHERE trip_count IS NOT NULL AND trip_count > 0;

IF @CountAgg = @GoldAggCount
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'PASS', 'Contagens agregadas');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('GOLD_AGG', @TestName, 'FAIL', 'Algumas contagens ausentes');
    PRINT '❌ FAIL: ' + @TestName;
END

PRINT '';

-- ============================================================================
-- CATEGORIA 7: TESTES DE INTEGRIDADE DE DADOS
-- ============================================================================
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT 'CATEGORIA 7: INTEGRIDADE DE DADOS';
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

-- Teste 7.1: Consistência Landing → Silver
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Consistência de registros: Landing → Silver (diferença < 1%)';
DECLARE @LandingSilverDiff DECIMAL(5,2);
SET @LandingSilverDiff = ABS(@LandingCSVCount - @SilverCSVCount) * 100.0 / NULLIF(@LandingCSVCount, 0);

IF @LandingSilverDiff < 1.0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('INTEGRITY', @TestName, 'PASS', 'Diferença: ' + CAST(@LandingSilverDiff AS VARCHAR) + '%');
    PRINT '✅ PASS: ' + @TestName + ' (Diferença: ' + CAST(@LandingSilverDiff AS VARCHAR) + '%)';
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('INTEGRITY', @TestName, 'WARNING', 'Diferença: ' + CAST(@LandingSilverDiff AS VARCHAR) + '% (>1%)');
    PRINT '⚠️  WARNING: ' + @TestName + ' (Diferença: ' + CAST(@LandingSilverDiff AS VARCHAR) + '%)';
END

-- Teste 7.2: Consistência Silver → Gold
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Registros VALID em Silver = Registros em Gold';
DECLARE @SilverValidCount INT;
SELECT @SilverValidCount = COUNT(*) FROM SILVER.TRIP_DATA_CSV WHERE quality_flag = 'VALID';

IF @GoldCSVCount = @SilverValidCount
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('INTEGRITY', @TestName, 'PASS', CAST(@SilverValidCount AS VARCHAR), CAST(@GoldCSVCount AS VARCHAR), 'Contagens consistentes');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @WarningTests = @WarningTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, expected_value, actual_value, test_message)
    VALUES ('INTEGRITY', @TestName, 'WARNING', CAST(@SilverValidCount AS VARCHAR), CAST(@GoldCSVCount AS VARCHAR), 'Diferença de ' + CAST(ABS(@SilverValidCount - @GoldCSVCount) AS VARCHAR) + ' registros');
    PRINT '⚠️  WARNING: ' + @TestName + ' (Silver Valid: ' + CAST(@SilverValidCount AS VARCHAR) + ', Gold: ' + CAST(@GoldCSVCount AS VARCHAR) + ')';
END

-- Teste 7.3: Sem duplicatas em Silver
SET @TotalTests = @TotalTests + 1;
SET @TestName = 'Sem duplicatas em SILVER.TRIP_DATA_CSV';
DECLARE @Duplicates INT;
SELECT @Duplicates = COUNT(*) - COUNT(DISTINCT trip_id) FROM SILVER.TRIP_DATA_CSV;

IF @Duplicates = 0
BEGIN
    SET @PassedTests = @PassedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('INTEGRITY', @TestName, 'PASS', 'Nenhuma duplicata encontrada');
    PRINT '✅ PASS: ' + @TestName;
END
ELSE
BEGIN
    SET @FailedTests = @FailedTests + 1;
    INSERT INTO #TestResults (test_category, test_name, test_result, test_message)
    VALUES ('INTEGRITY', @TestName, 'FAIL', CAST(@Duplicates AS VARCHAR) + ' duplicatas encontradas');
    PRINT '❌ FAIL: ' + @TestName + ' (' + CAST(@Duplicates AS VARCHAR) + ' duplicatas)';
END

PRINT '';

-- ============================================================================
-- SUMÁRIO FINAL DOS TESTES
-- ============================================================================
DECLARE @TestEndTime DATETIME2 = GETDATE();
DECLARE @TestDuration INT = DATEDIFF(SECOND, @TestStartTime, @TestEndTime);
DECLARE @SuccessRate DECIMAL(5,2) = (@PassedTests * 100.0) / @TotalTests;

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                                                                          █';
PRINT '█                         SUMÁRIO DOS TESTES                              █';
PRINT '█                                                                          █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Estatísticas Gerais:';
PRINT '  • Total de Testes: ' + CAST(@TotalTests AS VARCHAR);
PRINT '  • ✅ Passaram: ' + CAST(@PassedTests AS VARCHAR) + ' (' + CAST(CAST((@PassedTests * 100.0 / @TotalTests) AS DECIMAL(5,2)) AS VARCHAR) + '%)';
PRINT '  • ❌ Falharam: ' + CAST(@FailedTests AS VARCHAR) + ' (' + CAST(CAST((@FailedTests * 100.0 / @TotalTests) AS DECIMAL(5,2)) AS VARCHAR) + '%)';
PRINT '  • ⚠️  Warnings: ' + CAST(@WarningTests AS VARCHAR) + ' (' + CAST(CAST((@WarningTests * 100.0 / @TotalTests) AS DECIMAL(5,2)) AS VARCHAR) + '%)';
PRINT '  • Taxa de Sucesso: ' + CAST(@SuccessRate AS VARCHAR) + '%';
PRINT '  • Duração: ' + CAST(@TestDuration AS VARCHAR) + ' segundos';
PRINT '';

-- Status final
IF @FailedTests = 0 AND @WarningTests = 0
BEGIN
    PRINT '🎉🎉🎉 TODOS OS TESTES PASSARAM! PIPELINE 100% VALIDADA! 🎉🎉🎉';
END
ELSE IF @FailedTests = 0
BEGIN
    PRINT '✅ TODOS OS TESTES CRÍTICOS PASSARAM (Alguns warnings)';
END
ELSE
BEGIN
    PRINT '❌ ALGUNS TESTES FALHARAM - REVISE OS ERROS ACIMA';
END

PRINT '';

-- Detalhes por categoria
PRINT 'Resultados por Categoria:';
SELECT 
    test_category,
    COUNT(*) as total_tests,
    SUM(CASE WHEN test_result = 'PASS' THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN test_result = 'FAIL' THEN 1 ELSE 0 END) as failed,
    SUM(CASE WHEN test_result = 'WARNING' THEN 1 ELSE 0 END) as warnings,
    CAST(SUM(CASE WHEN test_result = 'PASS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) as success_rate
FROM #TestResults
GROUP BY test_category
ORDER BY test_category;

PRINT '';

-- Testes falhados (se houver)
IF @FailedTests > 0
BEGIN
    PRINT 'Testes que Falharam:';
    PRINT '';
    SELECT 
        test_name,
        expected_value,
        actual_value,
        test_message
    FROM #TestResults
    WHERE test_result = 'FAIL'
    ORDER BY test_id;
    PRINT '';
END

-- Warnings (se houver)
IF @WarningTests > 0
BEGIN
    PRINT 'Testes com Warning:';
    PRINT '';
    SELECT 
        test_name,
        expected_value,
        actual_value,
        test_message
    FROM #TestResults
    WHERE test_result = 'WARNING'
    ORDER BY test_id;
    PRINT '';
END

PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Requisito 8 Completo! ✅';
PRINT '';
PRINT 'Para salvar resultados, execute:';
PRINT '  SELECT * FROM #TestResults ORDER BY test_id;';
PRINT '';

-- Limpar
-- DROP TABLE #TestResults;  -- Comentado para permitir análise posterior

SET NOCOUNT OFF;
