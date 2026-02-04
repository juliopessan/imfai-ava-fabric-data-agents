-- ============================================================================
-- 02-LOAD-LANDING-CSV-OPENROWSET.SQL - Alternativa usando OPENROWSET
-- ============================================================================
-- Propósito: Carregar dados CSV usando OPENROWSET (alternativa ao BULK INSERT)
-- Requisito: 1a (CSV → LANDING com VARCHAR)
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
PRINT 'CARREGANDO DADOS CSV PARA LANDING LAYER - NYC GREEN TAXI (OPENROWSET)';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- Variáveis de controle
DECLARE @BatchID VARCHAR(50) = 'BATCH_' + CONVERT(VARCHAR, GETDATE(), 112) + '_' + REPLACE(CONVERT(VARCHAR, GETDATE(), 108), ':', '');
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @RecordsLoaded INT = 0;

PRINT 'Batch ID: ' + @BatchID;
PRINT '';

-- ============================================================================
-- HABILITAR Ad Hoc Distributed Queries (se necessário)
-- ============================================================================
PRINT '--- Habilitando Ad Hoc Distributed Queries ---';
PRINT '';

EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'Ad Hoc Distributed Queries', 1;
RECONFIGURE;

PRINT '✅ Ad Hoc Distributed Queries habilitado';
PRINT '';

-- ============================================================================
-- CARREGAR ABRIL 2021
-- ============================================================================
PRINT '--- REQUISITO 1a: Carregando green_tripdata_2021-04.csv ---';
PRINT '    Registros Esperados: 86,941';
PRINT '';

BEGIN TRY
    INSERT INTO LANDING.TRIP_DATA_CSV (
        VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
        store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
        passenger_count, trip_distance, fare_amount, extra, mta_tax,
        tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
        total_amount, payment_type, trip_type, congestion_surcharge,
        source_file, load_batch_id
    )
    SELECT 
        VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
        store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
        passenger_count, trip_distance, fare_amount, extra, mta_tax,
        tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
        total_amount, payment_type, trip_type, congestion_surcharge,
        'green_tripdata_2021-04.csv',
        @BatchID
    FROM OPENROWSET(
        BULK 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\Files\green_tripdata_2021-04.csv',
        FORMATFILE = 'C:\Users\e.a.de.albuquerque\Documents\BMAD_TESTE\bd-agent-avanade\real-test\etl\format-file.xml',
        FIRSTROW = 2
    ) AS DataFile;
    
    SET @RecordsLoaded = @RecordsLoaded + @@ROWCOUNT;
    PRINT '✅ green_tripdata_2021-04.csv carregado com sucesso';
    PRINT '   • Registros carregados: ' + CAST(@@ROWCOUNT AS VARCHAR);
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO ao carregar green_tripdata_2021-04.csv: ' + ERROR_MESSAGE();
    PRINT '⚠️  Continuando com próximo arquivo...';
    PRINT '';
END CATCH;

-- ============================================================================
-- ESTATÍSTICAS FINAIS
-- ============================================================================
PRINT '============================================================================';
PRINT 'CARREGAMENTO CSV PARA LANDING COMPLETO';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '  • Duração: ' + CAST(DATEDIFF(SECOND, @StartTime, GETDATE()) AS VARCHAR) + ' segundos';
PRINT '  • Batch ID: ' + @BatchID;
PRINT '';
PRINT 'Dados Carregados:';
PRINT '  • Total de registros: ' + CAST(@RecordsLoaded AS VARCHAR);
PRINT '';
PRINT 'OBSERVAÇÃO: Se o carregamento falhou, considere usar:';
PRINT '  1. Criar format file XML para OPENROWSET';
PRINT '  2. Usar Integration Services (SSIS)';
PRINT '  3. Carregar dados de teste manualmente para validação';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 04-transform-to-silver-csv.sql (REQ 1b)';
PRINT '============================================================================';
GO
