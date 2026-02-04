-- ============================================================================
-- 02-LOAD-LANDING-CSV.SQL - Carregamento de Dados CSV para Landing
-- ============================================================================
-- Propósito: Carregar arquivos CSV no formato VARCHAR para Landing Layer
-- Requisito: 1a (LANDING.TRIP_DATA_CSV - todos os campos VARCHAR)
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
PRINT 'CARREGANDO DADOS CSV PARA LANDING LAYER - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @BatchID VARCHAR(50) = 'BATCH_' + CONVERT(VARCHAR, GETDATE(), 112) + '_' + REPLACE(CONVERT(VARCHAR, GETDATE(), 108), ':', '');
DECLARE @RecordsLoaded INT = 0;
DECLARE @TotalRecords INT = 0;
DECLARE @ErrorMessage NVARCHAR(MAX);
DECLARE @SourcePath VARCHAR(500) = 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\';

PRINT 'Batch ID: ' + @BatchID;
PRINT 'Caminho dos arquivos: ' + @SourcePath;
PRINT '';

-- ============================================================================
-- VERIFICAR SE ARQUIVOS JÁ FORAM CARREGADOS (EVITAR DUPLICATAS)
-- ============================================================================
PRINT '--- Verificando Carregamentos Anteriores ---';
PRINT '';

DECLARE @File1Loaded INT, @File2Loaded INT, @File3Loaded INT;

SELECT @File1Loaded = COUNT(*) FROM LANDING.DATA_LINEAGE 
WHERE source_file = 'green_tripdata_2021-04.csv' AND load_status = 'SUCCESS';

SELECT @File2Loaded = COUNT(*) FROM LANDING.DATA_LINEAGE 
WHERE source_file = 'green_tripdata_2021-05.csv' AND load_status = 'SUCCESS';

SELECT @File3Loaded = COUNT(*) FROM LANDING.DATA_LINEAGE 
WHERE source_file = 'green_tripdata_2021-06.csv' AND load_status = 'SUCCESS';

IF @File1Loaded > 0 OR @File2Loaded > 0 OR @File3Loaded > 0
BEGIN
    PRINT '⚠️  AVISO: Alguns arquivos já foram carregados anteriormente:';
    IF @File1Loaded > 0 PRINT '    • green_tripdata_2021-04.csv (' + CAST(@File1Loaded AS VARCHAR) + ' carregamentos)';
    IF @File2Loaded > 0 PRINT '    • green_tripdata_2021-05.csv (' + CAST(@File2Loaded AS VARCHAR) + ' carregamentos)';
    IF @File3Loaded > 0 PRINT '    • green_tripdata_2021-06.csv (' + CAST(@File3Loaded AS VARCHAR) + ' carregamentos)';
    PRINT '';
    PRINT '    Para recarregar, limpe LANDING.TRIP_DATA_CSV e LANDING.DATA_LINEAGE primeiro.';
    PRINT '';
END

-- ============================================================================
-- REQUISITO 1a: CARREGAR green_tripdata_2021-04.csv
-- ============================================================================
PRINT '--- REQUISITO 1a: Carregando green_tripdata_2021-04.csv ---';
PRINT '    Registros Esperados: 86,941';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- BULK INSERT para carregar CSV
    -- Nota: Ajuste o caminho conforme necessário
    BULK INSERT LANDING.TRIP_DATA_CSV
    FROM 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\green_tripdata_2021-04.csv'
    WITH (
        FIRSTROW = 2,               -- Pula cabeçalho
        FIELDTERMINATOR = ',',      -- Delimitador CSV
        ROWTERMINATOR = '\n',       -- Fim de linha
        TABLOCK,                    -- Otimização de performance
        ERRORFILE = 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\errors_2021-04.txt',
        MAXERRORS = 100             -- Permite até 100 erros
    );
    
    -- Atualizar metadados de carga
    UPDATE LANDING.TRIP_DATA_CSV
    SET source_file = 'green_tripdata_2021-04.csv',
        load_batch_id = @BatchID
    WHERE source_file IS NULL;
    
    SET @RecordsLoaded = @@ROWCOUNT;
    SET @TotalRecords = @TotalRecords + @RecordsLoaded;
    
    -- Registrar no log de lineage
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status)
    VALUES ('green_tripdata_2021-04.csv', 'LANDING.TRIP_DATA_CSV', @RecordsLoaded, 'SUCCESS');
    
    COMMIT TRANSACTION;
    
    PRINT '✅ green_tripdata_2021-04.csv carregado com sucesso';
    PRINT '   • Registros inseridos: ' + CAST(@RecordsLoaded AS VARCHAR);
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    
    SET @ErrorMessage = ERROR_MESSAGE();
    PRINT '❌ ERRO ao carregar green_tripdata_2021-04.csv: ' + @ErrorMessage;
    
    -- Registrar erro no log
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status, error_message)
    VALUES ('green_tripdata_2021-04.csv', 'LANDING.TRIP_DATA_CSV', 0, 'FAILED', @ErrorMessage);
    
    PRINT '';
    PRINT '⚠️  Continuando com próximo arquivo...';
    PRINT '';
END CATCH;

-- ============================================================================
-- REQUISITO 1a: CARREGAR green_tripdata_2021-05.csv
-- ============================================================================
PRINT '--- REQUISITO 1a: Carregando green_tripdata_2021-05.csv ---';
PRINT '    Registros Esperados: 88,180';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    BULK INSERT LANDING.TRIP_DATA_CSV
    FROM 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\green_tripdata_2021-05.csv'
    WITH (
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        TABLOCK,
        ERRORFILE = 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\errors_2021-05.txt',
        MAXERRORS = 100
    );
    
    UPDATE LANDING.TRIP_DATA_CSV
    SET source_file = 'green_tripdata_2021-05.csv',
        load_batch_id = @BatchID
    WHERE source_file IS NULL;
    
    SET @RecordsLoaded = @@ROWCOUNT;
    SET @TotalRecords = @TotalRecords + @RecordsLoaded;
    
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status)
    VALUES ('green_tripdata_2021-05.csv', 'LANDING.TRIP_DATA_CSV', @RecordsLoaded, 'SUCCESS');
    
    COMMIT TRANSACTION;
    
    PRINT '✅ green_tripdata_2021-05.csv carregado com sucesso';
    PRINT '   • Registros inseridos: ' + CAST(@RecordsLoaded AS VARCHAR);
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    
    SET @ErrorMessage = ERROR_MESSAGE();
    PRINT '❌ ERRO ao carregar green_tripdata_2021-05.csv: ' + @ErrorMessage;
    
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status, error_message)
    VALUES ('green_tripdata_2021-05.csv', 'LANDING.TRIP_DATA_CSV', 0, 'FAILED', @ErrorMessage);
    
    PRINT '';
    PRINT '⚠️  Continuando com próximo arquivo...';
    PRINT '';
END CATCH;

-- ============================================================================
-- REQUISITO 1a: CARREGAR green_tripdata_2021-06.csv
-- ============================================================================
PRINT '--- REQUISITO 1a: Carregando green_tripdata_2021-06.csv ---';
PRINT '    Registros Esperados: 86,737';
PRINT '';

BEGIN TRY
    BEGIN TRANSACTION;
    
    BULK INSERT LANDING.TRIP_DATA_CSV
    FROM 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\green_tripdata_2021-06.csv'
    WITH (
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        TABLOCK,
        ERRORFILE = 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\errors_2021-06.txt',
        MAXERRORS = 100
    );
    
    UPDATE LANDING.TRIP_DATA_CSV
    SET source_file = 'green_tripdata_2021-06.csv',
        load_batch_id = @BatchID
    WHERE source_file IS NULL;
    
    SET @RecordsLoaded = @@ROWCOUNT;
    SET @TotalRecords = @TotalRecords + @RecordsLoaded;
    
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status)
    VALUES ('green_tripdata_2021-06.csv', 'LANDING.TRIP_DATA_CSV', @RecordsLoaded, 'SUCCESS');
    
    COMMIT TRANSACTION;
    
    PRINT '✅ green_tripdata_2021-06.csv carregado com sucesso';
    PRINT '   • Registros inseridos: ' + CAST(@RecordsLoaded AS VARCHAR);
    PRINT '';
    
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    
    SET @ErrorMessage = ERROR_MESSAGE();
    PRINT '❌ ERRO ao carregar green_tripdata_2021-06.csv: ' + @ErrorMessage;
    
    INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status, error_message)
    VALUES ('green_tripdata_2021-06.csv', 'LANDING.TRIP_DATA_CSV', 0, 'FAILED', @ErrorMessage);
    
    PRINT '';
END CATCH;

-- ============================================================================
-- VERIFICAÇÃO DE QUALIDADE DOS DADOS CARREGADOS
-- ============================================================================
PRINT '--- Verificação de Qualidade ---';
PRINT '';

DECLARE @TotalLoadedRecords INT;
DECLARE @NullVendorID INT;
DECLARE @NullDates INT;
DECLARE @NegativeAmounts INT;

SELECT @TotalLoadedRecords = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE load_batch_id = @BatchID;
SELECT @NullVendorID = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE VendorID IS NULL AND load_batch_id = @BatchID;
SELECT @NullDates = COUNT(*) FROM LANDING.TRIP_DATA_CSV 
WHERE (lpep_pickup_datetime IS NULL OR lpep_dropoff_datetime IS NULL) AND load_batch_id = @BatchID;
SELECT @NegativeAmounts = COUNT(*) FROM LANDING.TRIP_DATA_CSV 
WHERE TRY_CAST(total_amount AS DECIMAL(10,2)) < 0 AND load_batch_id = @BatchID;

PRINT 'Estatísticas de Qualidade:';
PRINT '  • Total de registros carregados: ' + CAST(@TotalLoadedRecords AS VARCHAR);
PRINT '  • Registros com VendorID nulo: ' + CAST(@NullVendorID AS VARCHAR);
PRINT '  • Registros com datas nulas: ' + CAST(@NullDates AS VARCHAR);
PRINT '  • Registros com valores negativos: ' + CAST(@NegativeAmounts AS VARCHAR);
PRINT '';

IF @NullVendorID = 0 AND @NullDates = 0 AND @NegativeAmounts = 0
BEGIN
    PRINT '✅ Qualidade dos dados: EXCELENTE';
END
ELSE
BEGIN
    PRINT '⚠️  Qualidade dos dados: REVISAR (problemas detectados)';
END

PRINT '';

-- ============================================================================
-- SUMÁRIO DE EXECUÇÃO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'CARREGAMENTO CSV PARA LANDING COMPLETO';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, @EndTime, 120);
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '  • Batch ID: ' + @BatchID;
PRINT '';
PRINT 'Dados Carregados:';
PRINT '  • Total de registros: ' + CAST(@TotalLoadedRecords AS VARCHAR);
PRINT '  • Arquivos processados: 3';
PRINT '  • Taxa de sucesso: ' + CAST((@TotalRecords * 100.0 / 261858) AS DECIMAL(5,2)) + '%';
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 1a: CSV → LANDING.TRIP_DATA_CSV (todos campos VARCHAR)';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 03-load-landing-parquet.sql para carregar Parquet';
PRINT '  → Execute 04-transform-to-silver-csv.sql para transformar em Silver';
PRINT '============================================================================';

SET NOCOUNT OFF;
