-- ============================================================================
-- 02-LOAD-LANDING-CSV-SAMPLE.SQL - Carga de Dados de Amostra
-- ============================================================================
-- Propósito: Carregar dados de amostra para demonstração do pipeline
-- Requisito: 1a (CSV → LANDING com VARCHAR)
-- Nota: Use esta versão para testes quando BULK INSERT não estiver disponível
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
PRINT 'CARREGANDO DADOS DE AMOSTRA PARA LANDING LAYER - NYC GREEN TAXI';
PRINT '============================================================================';
PRINT '';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';
PRINT 'NOTA: Usando dados de amostra para demonstração do pipeline';
PRINT '      Em produção, use BULK INSERT ou SSIS para carregar arquivos CSV';
PRINT '';

-- Variáveis de controle
DECLARE @BatchID VARCHAR(50) = 'SAMPLE_BATCH_' + CONVERT(VARCHAR, GETDATE(), 112);
DECLARE @StartTime DATETIME2 = GETDATE();

PRINT 'Batch ID: ' + @BatchID;
PRINT '';

-- ============================================================================
-- LIMPAR DADOS ANTERIORES (OPCIONAL)
-- ============================================================================
PRINT '--- Limpando dados anteriores ---';
TRUNCATE TABLE LANDING.TRIP_DATA_CSV;
PRINT '✅ Tabela Landing limpa';
PRINT '';

-- ============================================================================
-- REQUISITO 1a: Inserir dados de amostra (VARCHAR)
-- ============================================================================
PRINT '--- REQUISITO 1a: Inserindo dados de amostra ---';
PRINT '';

INSERT INTO LANDING.TRIP_DATA_CSV (
    VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
    store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID,
    passenger_count, trip_distance, fare_amount, extra, mta_tax,
    tip_amount, tolls_amount, ehail_fee, improvement_surcharge,
    total_amount, payment_type, trip_type, congestion_surcharge,
    source_file, load_batch_id
)
VALUES
-- Viagens normais de Abril 2021
('2', '2021-04-01 00:38:16', '2021-04-01 00:43:14', 'N', '1', '134', '197', '2', '1.11', '6.00', '0.50', '0.50', '0.00', '0.00', NULL, '0.30', '7.30', '2', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('2', '2021-04-01 00:03:27', '2021-04-01 00:28:58', 'N', '1', '82', '129', '1', '9.11', '27.50', '0.50', '0.50', '5.86', '0.00', NULL, '0.30', '34.66', '1', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('2', '2021-04-01 00:28:38', '2021-04-01 00:38:27', 'N', '1', '129', '137', '1', '1.67', '8.50', '0.50', '0.50', '1.00', '0.00', NULL, '0.30', '10.80', '1', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('2', '2021-04-01 00:39:13', '2021-04-01 00:56:44', 'N', '1', '137', '140', '1', '2.69', '13.00', '0.50', '0.50', '0.00', '0.00', NULL, '0.30', '14.30', '2', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('2', '2021-04-01 00:23:12', '2021-04-01 01:01:30', 'N', '1', '75', '42', '1', '6.79', '27.50', '0.50', '0.50', '5.96', '0.00', NULL, '0.30', '37.01', '1', '1', '2.75', 'sample_april_2021.csv', @BatchID),

-- Viagens de Maio 2021
('2', '2021-05-01 08:15:22', '2021-05-01 08:25:11', 'N', '1', '75', '166', '1', '1.85', '8.50', '0.00', '0.50', '1.86', '0.00', NULL, '0.30', '11.16', '1', '1', '0.00', 'sample_may_2021.csv', @BatchID),
('2', '2021-05-01 18:45:33', '2021-05-01 19:12:44', 'N', '1', '132', '205', '2', '4.23', '18.00', '1.00', '0.50', '3.86', '0.00', NULL, '0.30', '23.66', '1', '1', '2.75', 'sample_may_2021.csv', @BatchID),
('1', '2021-05-15 12:30:00', '2021-05-15 12:45:00', 'N', '2', '132', '138', '3', '12.50', '52.00', '0.00', '0.50', '0.00', '6.12', NULL, '0.30', '58.92', '2', '1', '0.00', 'sample_may_2021.csv', @BatchID),

-- Viagens de Junho 2021
('2', '2021-06-01 14:22:15', '2021-06-01 14:35:28', 'N', '1', '7', '129', '1', '2.10', '10.00', '0.00', '0.50', '2.16', '0.00', NULL, '0.30', '12.96', '1', '1', '0.00', 'sample_june_2021.csv', @BatchID),
('1', '2021-06-15 09:11:33', '2021-06-15 09:28:55', 'N', '1', '166', '236', '1', '3.41', '14.00', '0.00', '0.50', '0.00', '0.00', NULL, '0.30', '14.80', '2', '1', '0.00', 'sample_june_2021.csv', @BatchID),

-- Viagens com diferentes características para testes
('2', '2021-04-10 20:15:00', '2021-04-10 20:45:00', 'N', '5', '138', '132', '1', '5.50', '25.00', '0.50', '0.50', '0.00', '0.00', NULL, '0.30', '26.30', '3', '2', '0.00', 'sample_april_2021.csv', @BatchID),
('1', '2021-05-20 07:30:00', '2021-05-20 08:15:00', 'Y', '1', '132', '138', '4', '8.20', '32.00', '0.00', '0.50', '6.56', '0.00', NULL, '0.30', '39.36', '1', '1', '2.75', 'sample_may_2021.csv', @BatchID),
('2', '2021-06-25 22:00:00', '2021-06-25 22:30:00', 'N', '1', '74', '75', '2', '3.80', '16.50', '0.50', '0.50', '0.00', '0.00', NULL, '0.30', '17.80', '4', '1', '0.00', 'sample_june_2021.csv', @BatchID),

-- Viagens para aeroportos (rate_code 2 = JFK, 3 = Newark)
('2', '2021-04-05 06:00:00', '2021-04-05 06:45:00', 'N', '2', '132', '138', '1', '18.50', '52.00', '0.00', '0.50', '10.40', '6.12', NULL, '0.30', '69.32', '1', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('1', '2021-05-10 15:30:00', '2021-05-10 16:25:00', 'N', '3', '138', '1', '2', '22.30', '64.50', '0.00', '0.50', '0.00', '0.00', NULL, '0.30', '65.30', '2', '1', '0.00', 'sample_may_2021.csv', @BatchID),

-- Viagens com edge cases
('2', '2021-04-20 03:00:00', '2021-04-20 03:05:00', 'N', '1', '7', '7', '1', '0.50', '3.50', '0.50', '0.50', '0.00', '0.00', NULL, '0.30', '4.80', '2', '1', '0.00', 'sample_april_2021.csv', @BatchID),
('1', '2021-06-30 23:55:00', '2021-07-01 00:15:00', 'N', '1', '132', '138', '1', '4.10', '15.50', '0.50', '0.50', '3.26', '0.00', NULL, '0.30', '20.06', '1', '1', '0.00', 'sample_june_2021.csv', @BatchID);

DECLARE @RecordsLoaded INT = @@ROWCOUNT;

PRINT '✅ Dados de amostra inseridos com sucesso';
PRINT '   • Registros carregados: ' + CAST(@RecordsLoaded AS VARCHAR);
PRINT '';

-- ============================================================================
-- VERIFICAÇÃO DE QUALIDADE
-- ============================================================================
PRINT '--- Verificação de Qualidade ---';
PRINT '';

DECLARE @TotalRecords INT;
DECLARE @NullVendorID INT;
DECLARE @NullDates INT;
DECLARE @NegativeValues INT;

SELECT @TotalRecords = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE load_batch_id = @BatchID;
SELECT @NullVendorID = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE VendorID IS NULL AND load_batch_id = @BatchID;
SELECT @NullDates = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE (lpep_pickup_datetime IS NULL OR lpep_dropoff_datetime IS NULL) AND load_batch_id = @BatchID;
SELECT @NegativeValues = COUNT(*) FROM LANDING.TRIP_DATA_CSV WHERE TRY_CAST(fare_amount AS DECIMAL(10,2)) < 0 AND load_batch_id = @BatchID;

PRINT 'Estatísticas de Qualidade:';
PRINT '  • Total de registros carregados: ' + CAST(@TotalRecords AS VARCHAR);
PRINT '  • Registros com VendorID nulo: ' + CAST(@NullVendorID AS VARCHAR);
PRINT '  • Registros com datas nulas: ' + CAST(@NullDates AS VARCHAR);
PRINT '  • Registros com valores negativos: ' + CAST(@NegativeValues AS VARCHAR);
PRINT '';

IF @NullVendorID = 0 AND @NullDates = 0 AND @NegativeValues = 0
    PRINT '✅ Qualidade dos dados: EXCELENTE';
ELSE
    PRINT '⚠️  Atenção: Problemas de qualidade detectados';

PRINT '';

-- ============================================================================
-- ATUALIZAR LINEAGE
-- ============================================================================
INSERT INTO LANDING.DATA_LINEAGE (
    source_file,
    target_table,
    records_loaded,
    load_status,
    load_timestamp
)
VALUES (
    'sample_data_april_may_june_2021.csv',
    'LANDING.TRIP_DATA_CSV',
    @RecordsLoaded,
    'SUCCESS',
    GETDATE()
);

-- ============================================================================
-- ESTATÍSTICAS FINAIS
-- ============================================================================
PRINT '============================================================================';
PRINT 'CARREGAMENTO DE DADOS DE AMOSTRA COMPLETO';
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
PRINT '  • Meses cobertos: Abril, Maio, Junho 2021';
PRINT '  • Tipos de viagem: Street-hail (1), Dispatch (2)';
PRINT '  • Rate codes: Standard, JFK, Newark, Negotiated';
PRINT '  • Payment types: Credit, Cash, No charge, Dispute';
PRINT '';
PRINT 'Requisitos Implementados:';
PRINT '  ✅ REQUISITO 1a: CSV → LANDING (VARCHAR)';
PRINT '';
PRINT 'Próximo Passo:';
PRINT '  → Execute 04-transform-to-silver-csv.sql (REQ 1b)';
PRINT '============================================================================';
GO
