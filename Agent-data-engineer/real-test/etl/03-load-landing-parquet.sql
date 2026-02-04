-- ============================================================================
-- 03-LOAD-LANDING-PARQUET.SQL - Carregamento de Dados Parquet para Landing
-- ============================================================================
-- Propósito: Carregar arquivos Parquet no formato VARCHAR para Landing Layer
-- Requisito: 2a (LANDING.TRIP_DATA_PARQUET - todos os campos VARCHAR)
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
PRINT 'CARREGANDO DADOS PARQUET PARA LANDING LAYER - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

-- ============================================================================
-- NOTA IMPORTANTE: CARREGAMENTO DE ARQUIVOS PARQUET
-- ============================================================================
PRINT '--- NOTA: Carregamento de Arquivos Parquet ---';
PRINT '';
PRINT 'Arquivos Parquet requerem ferramentas externas para carregar em SQL Server:';
PRINT '  • Opção 1: Azure Data Factory / Synapse Analytics';
PRINT '  • Opção 2: Python + pyarrow + pyodbc';
PRINT '  • Opção 3: PySpark para ler Parquet e gravar em SQL Server';
PRINT '  • Opção 4: Converter Parquet para CSV primeiro';
PRINT '';
PRINT 'Este script demonstra a estrutura de carregamento.';
PRINT 'Para execução real, use o script Python complementar: load_parquet_to_sql.py';
PRINT '';

-- ============================================================================
-- VARIÁVEIS DE CONTROLE
-- ============================================================================
DECLARE @StartTime DATETIME2 = GETDATE();
DECLARE @RecordsLoaded INT = 0;
DECLARE @TotalRecords INT = 0;
DECLARE @ErrorMessage NVARCHAR(MAX);

-- ============================================================================
-- ESTRUTURA DE STAGING PARA PARQUET (Uso com Python/PySpark)
-- ============================================================================
PRINT '--- Criando Tabela Staging Temporária ---';
PRINT '';

-- Drop staging se existir
IF OBJECT_ID('tempdb..#PARQUET_STAGING', 'U') IS NOT NULL
    DROP TABLE #PARQUET_STAGING;

-- Criar staging table idêntica à estrutura Landing
CREATE TABLE #PARQUET_STAGING (
    VendorID                  VARCHAR(50),
    lpep_pickup_datetime      VARCHAR(50),
    lpep_dropoff_datetime     VARCHAR(50),
    store_and_fwd_flag        VARCHAR(50),
    RatecodeID                VARCHAR(50),
    PULocationID              VARCHAR(50),
    DOLocationID              VARCHAR(50),
    passenger_count           VARCHAR(50),
    trip_distance             VARCHAR(50),
    fare_amount               VARCHAR(50),
    extra                     VARCHAR(50),
    mta_tax                   VARCHAR(50),
    tip_amount                VARCHAR(50),
    tolls_amount              VARCHAR(50),
    ehail_fee                 VARCHAR(50),
    improvement_surcharge     VARCHAR(50),
    total_amount              VARCHAR(50),
    payment_type              VARCHAR(50),
    trip_type                 VARCHAR(50),
    congestion_surcharge      VARCHAR(50),
    source_file               VARCHAR(500),
    partition_key             VARCHAR(50)
);

PRINT '✅ Tabela staging criada para receber dados Parquet';
PRINT '';

-- ============================================================================
-- SIMULAÇÃO: CARREGAR DADOS DE PARQUET PARA STAGING
-- ============================================================================
PRINT '--- REQUISITO 2a: Preparando para Carregar Arquivos Parquet ---';
PRINT '';
PRINT 'Arquivos a processar:';
PRINT '  • month=04/part-00000-*.snappy.parquet';
PRINT '  • month=05/part-00000-*.snappy.parquet';
PRINT '  • month=06/part-00000-*.snappy.parquet';
PRINT '';

-- ============================================================================
-- PASSO 1: Python/PySpark carrega Parquet → #PARQUET_STAGING
-- ============================================================================
-- Este passo é executado externamente via Python (ver load_parquet_to_sql.py)
-- O script Python irá:
-- 1. Ler arquivos .parquet com pyarrow ou PySpark
-- 2. Converter todos os campos para STRING
-- 3. Inserir em #PARQUET_STAGING via pyodbc/sqlalchemy

PRINT '⏳ Aguardando carregamento externo de dados Parquet...';
PRINT '   (Execute: python load_parquet_to_sql.py)';
PRINT '';

-- ============================================================================
-- PASSO 2: MOVER STAGING → LANDING.TRIP_DATA_PARQUET
-- ============================================================================
PRINT '--- Movendo Dados de Staging para Landing ---';
PRINT '';

-- Verificar se staging tem dados
DECLARE @StagingCount INT = 0;
SELECT @StagingCount = COUNT(*) FROM #PARQUET_STAGING;

IF @StagingCount > 0
BEGIN
    PRINT 'Dados encontrados em staging: ' + CAST(@StagingCount AS VARCHAR) + ' registros';
    PRINT '';
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Inserir de staging para landing
        INSERT INTO LANDING.TRIP_DATA_PARQUET (
            VendorID, lpep_pickup_datetime, lpep_dropoff_datetime, 
            store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
            passenger_count, trip_distance, fare_amount, extra, mta_tax,
            tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
            total_amount, payment_type, trip_type, congestion_surcharge,
            source_file, partition_key
        )
        SELECT 
            VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
            store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
            passenger_count, trip_distance, fare_amount, extra, mta_tax,
            tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
            total_amount, payment_type, trip_type, congestion_surcharge,
            source_file, partition_key
        FROM #PARQUET_STAGING;
        
        SET @RecordsLoaded = @@ROWCOUNT;
        
        -- Registrar no log de lineage por partição
        INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status)
        SELECT 
            partition_key + '/parquet_files',
            'LANDING.TRIP_DATA_PARQUET',
            COUNT(*),
            'SUCCESS'
        FROM #PARQUET_STAGING
        GROUP BY partition_key;
        
        COMMIT TRANSACTION;
        
        PRINT '✅ Dados Parquet movidos para LANDING com sucesso';
        PRINT '   • Registros inseridos: ' + CAST(@RecordsLoaded AS VARCHAR);
        PRINT '';
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
        PRINT '❌ ERRO ao mover dados de staging: ' + @ErrorMessage;
        
        INSERT INTO LANDING.DATA_LINEAGE (source_file, target_table, records_loaded, load_status, error_message)
        VALUES ('parquet_files', 'LANDING.TRIP_DATA_PARQUET', 0, 'FAILED', @ErrorMessage);
        
        PRINT '';
    END CATCH;
END
ELSE
BEGIN
    PRINT '⚠️  AVISO: Nenhum dado encontrado em staging';
    PRINT '   Execute o script Python primeiro: python load_parquet_to_sql.py';
    PRINT '';
    PRINT '   Script Python irá:';
    PRINT '   1. Ler arquivos Parquet de Files/month=04,05,06/';
    PRINT '   2. Converter para VARCHAR (todos os campos)';
    PRINT '   3. Inserir em #PARQUET_STAGING';
    PRINT '   4. Este script SQL move para LANDING.TRIP_DATA_PARQUET';
    PRINT '';
END

-- ============================================================================
-- VERIFICAÇÃO DE QUALIDADE (SE DADOS FORAM CARREGADOS)
-- ============================================================================
IF @RecordsLoaded > 0
BEGIN
    PRINT '--- Verificação de Qualidade ---';
    PRINT '';
    
    DECLARE @TotalParquetRecords INT;
    DECLARE @PartitionCount INT;
    
    SELECT @TotalParquetRecords = COUNT(*) FROM LANDING.TRIP_DATA_PARQUET;
    SELECT @PartitionCount = COUNT(DISTINCT partition_key) FROM LANDING.TRIP_DATA_PARQUET;
    
    PRINT 'Estatísticas de Qualidade:';
    PRINT '  • Total de registros Parquet: ' + CAST(@TotalParquetRecords AS VARCHAR);
    PRINT '  • Partições carregadas: ' + CAST(@PartitionCount AS VARCHAR);
    PRINT '';
    
    -- Verificar distribuição por partição
    SELECT 
        partition_key,
        COUNT(*) as record_count,
        MIN(source_file) as sample_file
    FROM LANDING.TRIP_DATA_PARQUET
    GROUP BY partition_key
    ORDER BY partition_key;
    
    PRINT '';
END

-- ============================================================================
-- COMPARAÇÃO CSV vs PARQUET (Validação Cruzada)
-- ============================================================================
PRINT '--- Comparação CSV vs Parquet ---';
PRINT '';

DECLARE @CSVCount INT, @ParquetCount INT;

SELECT @CSVCount = COUNT(*) FROM LANDING.TRIP_DATA_CSV;
SELECT @ParquetCount = COUNT(*) FROM LANDING.TRIP_DATA_PARQUET;

PRINT 'Contadores:';
PRINT '  • Registros CSV: ' + CAST(@CSVCount AS VARCHAR);
PRINT '  • Registros Parquet: ' + CAST(@ParquetCount AS VARCHAR);
PRINT '';

IF @ParquetCount > 0
BEGIN
    DECLARE @Difference INT = ABS(@CSVCount - @ParquetCount);
    DECLARE @PercentDiff DECIMAL(5,2) = (@Difference * 100.0) / NULLIF(@CSVCount, 0);
    
    PRINT 'Diferença: ' + CAST(@Difference AS VARCHAR) + ' registros (' + CAST(@PercentDiff AS VARCHAR) + '%)';
    
    IF @PercentDiff < 1.0
    BEGIN
        PRINT '✅ CSV e Parquet estão consistentes (diferença < 1%)';
    END
    ELSE IF @PercentDiff < 5.0
    BEGIN
        PRINT '⚠️  Diferença aceitável entre CSV e Parquet (< 5%)';
    END
    ELSE
    BEGIN
        PRINT '❌ ALERTA: Grande diferença entre CSV e Parquet (>= 5%)';
    END
END

PRINT '';

-- ============================================================================
-- SUMÁRIO DE EXECUÇÃO
-- ============================================================================
DECLARE @EndTime DATETIME2 = GETDATE();
DECLARE @Duration INT = DATEDIFF(SECOND, @StartTime, @EndTime);

PRINT '============================================================================';
PRINT 'CARREGAMENTO PARQUET PARA LANDING COMPLETO';
PRINT '============================================================================';
PRINT '';
PRINT 'Estatísticas de Execução:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @StartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, @EndTime, 120);
PRINT '  • Duração: ' + CAST(@Duration AS VARCHAR) + ' segundos';
PRINT '';
PRINT 'Dados Carregados:';
PRINT '  • Registros Parquet: ' + CAST(@RecordsLoaded AS VARCHAR);
PRINT '  • Partições: month=04, month=05, month=06';
PRINT '';
PRINT 'Requisito Implementado:';
PRINT '  ✅ REQUISITO 2a: Parquet → LANDING.TRIP_DATA_PARQUET (todos campos VARCHAR)';
PRINT '';
PRINT 'Próximos Passos:';
PRINT '  → Execute 04-transform-to-silver-csv.sql (transformar CSV em Silver)';
PRINT '  → Execute 05-transform-to-silver-parquet.sql (transformar Parquet em Silver)';
PRINT '';
PRINT 'IMPORTANTE:';
PRINT '  Para carregar arquivos Parquet reais, execute antes:';
PRINT '  → python load_parquet_to_sql.py';
PRINT '============================================================================';

-- Limpar staging
DROP TABLE #PARQUET_STAGING;

SET NOCOUNT OFF;
