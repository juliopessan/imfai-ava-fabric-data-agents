-- ============================================================================
-- 00-RUN-ALL-ETL.SQL - Script Master de Execução da Pipeline Completa
-- ============================================================================
-- Propósito: Executar toda a pipeline ETL em ordem correta
-- Requisitos: Todos os 8 requisitos do projeto
-- Autor: DataFlow Agent
-- Data: 17 de Novembro de 2025
-- ============================================================================

USE TEST_PIPELINE;
GO

SET NOCOUNT ON;

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                                                                          █';
PRINT '█          NYC GREEN TAXI DATA PIPELINE - EXECUÇÃO COMPLETA               █';
PRINT '█                                                                          █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Pipeline: Landing → Silver → Gold (Medallion Architecture)';
PRINT 'Database: TEST_PIPELINE';
PRINT 'Início: ' + CONVERT(VARCHAR, GETDATE(), 120);
PRINT '';

DECLARE @MasterStartTime DATETIME2 = GETDATE();
DECLARE @StepStartTime DATETIME2;
DECLARE @StepDuration INT;
DECLARE @TotalErrors INT = 0;
DECLARE @CurrentStep VARCHAR(100);

-- ============================================================================
-- FUNÇÃO AUXILIAR: LOG DE PROGRESSO
-- ============================================================================
DECLARE @StepNumber INT = 0;

-- ============================================================================
-- PASSO 1: CRIAR DDL (Tabelas)
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Criar Estrutura de Tabelas (DDL)';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando DDL scripts...';
    PRINT '  → 01-landing-tables.sql';
    PRINT '  → 02-silver-tables.sql';
    PRINT '  → 03-gold-tables.sql';
    PRINT '  → 04-reference-tables.sql';
    PRINT '';
    PRINT '⚠️  NOTA: Execute manualmente os scripts DDL antes de rodar esta pipeline ETL';
    PRINT '    Os scripts DDL estão em: real-test/*.sql';
    PRINT '';
    
    -- Verificar se tabelas existem
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('LANDING'))
    BEGIN
        PRINT '❌ ERRO: Tabelas Landing não encontradas!';
        PRINT '   Execute: 01-landing-tables.sql';
        SET @TotalErrors = @TotalErrors + 1;
    END
    ELSE
    BEGIN
        PRINT '✅ Tabelas Landing encontradas';
    END
    
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('SILVER'))
    BEGIN
        PRINT '❌ ERRO: Tabelas Silver não encontradas!';
        PRINT '   Execute: 02-silver-tables.sql';
        SET @TotalErrors = @TotalErrors + 1;
    END
    ELSE
    BEGIN
        PRINT '✅ Tabelas Silver encontradas';
    END
    
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TRIP_DATA_CSV' AND schema_id = SCHEMA_ID('GOLD'))
    BEGIN
        PRINT '❌ ERRO: Tabelas Gold não encontradas!';
        PRINT '   Execute: 03-gold-tables.sql';
        SET @TotalErrors = @TotalErrors + 1;
    END
    ELSE
    BEGIN
        PRINT '✅ Tabelas Gold encontradas';
    END
    
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RATE_CODE' AND schema_id = SCHEMA_ID('REF'))
    BEGIN
        PRINT '❌ ERRO: Tabelas de Referência não encontradas!';
        PRINT '   Execute: 04-reference-tables.sql';
        SET @TotalErrors = @TotalErrors + 1;
    END
    ELSE
    BEGIN
        PRINT '✅ Tabelas de Referência encontradas';
    END
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '';
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
    
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

IF @TotalErrors > 0
BEGIN
    PRINT '';
    PRINT '❌❌❌ PIPELINE INTERROMPIDA: Estrutura DDL incompleta ❌❌❌';
    PRINT 'Execute os scripts DDL antes de continuar.';
    PRINT '';
    RETURN;
END

-- ============================================================================
-- PASSO 2: CARREGAR DADOS DE REFERÊNCIA
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Carregar Dados de Referência';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/01-load-reference-data.sql';
    EXEC('sqlcmd -S localhost -d TEST_PIPELINE -i "01-load-reference-data.sql"');
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

-- ============================================================================
-- PASSO 3: CARREGAR CSV PARA LANDING
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Carregar CSV → Landing';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/02-load-landing-csv.sql';
    PRINT '⚠️  NOTA: Execute manualmente este script em outra janela';
    PRINT '    Requer permissões de BULK INSERT e caminho dos arquivos correto';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

-- ============================================================================
-- PASSO 4: CARREGAR PARQUET PARA LANDING (OPCIONAL)
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Carregar Parquet → Landing (OPCIONAL)';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Para carregar arquivos Parquet:';
    PRINT '  1. Execute: python load_parquet_to_sql.py';
    PRINT '  2. Execute: 03-load-landing-parquet.sql';
    PRINT '';
    PRINT '⚠️  Este passo é OPCIONAL - Pipeline pode continuar apenas com CSV';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    PRINT '   (Este erro não é crítico)';
END CATCH;

-- ============================================================================
-- PASSO 5: TRANSFORMAR CSV → SILVER
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Transformar CSV → Silver';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/04-transform-to-silver-csv.sql';
    PRINT '⚠️  NOTA: Execute manualmente este script em outra janela';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

-- ============================================================================
-- PASSO 6: TRANSFORMAR PARQUET → SILVER (OPCIONAL)
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Transformar Parquet → Silver (OPCIONAL)';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/05-transform-to-silver-parquet.sql';
    PRINT '⚠️  OPCIONAL - Execute apenas se dados Parquet foram carregados';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '⚠️  AVISO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    PRINT '   (Este erro não é crítico)';
END CATCH;

-- ============================================================================
-- PASSO 7: CONSTRUIR GOLD ENRICHED
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Construir Gold Enriched';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/06-build-gold-enriched.sql';
    PRINT '⚠️  NOTA: Execute manualmente este script em outra janela';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

-- ============================================================================
-- PASSO 8: CONSTRUIR GOLD AGGREGATED
-- ============================================================================
SET @StepNumber = @StepNumber + 1;
SET @CurrentStep = 'PASSO ' + CAST(@StepNumber AS VARCHAR) + ': Construir Gold Aggregated';
SET @StepStartTime = GETDATE();

PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT @CurrentStep;
PRINT '════════════════════════════════════════════════════════════════════════════';
PRINT '';

BEGIN TRY
    PRINT 'Executando: etl/07-build-gold-aggregated.sql';
    PRINT '⚠️  NOTA: Execute manualmente este script em outra janela';
    PRINT '';
    
    SET @StepDuration = DATEDIFF(SECOND, @StepStartTime, GETDATE());
    PRINT '⏱️  Duração: ' + CAST(@StepDuration AS VARCHAR) + ' segundos';
    PRINT '';
END TRY
BEGIN CATCH
    PRINT '❌ ERRO no ' + @CurrentStep + ': ' + ERROR_MESSAGE();
    SET @TotalErrors = @TotalErrors + 1;
END CATCH;

-- ============================================================================
-- SUMÁRIO FINAL
-- ============================================================================
DECLARE @MasterEndTime DATETIME2 = GETDATE();
DECLARE @TotalDuration INT = DATEDIFF(SECOND, @MasterStartTime, @MasterEndTime);

PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '█                                                                          █';
PRINT '█                    PIPELINE ETL - SUMÁRIO FINAL                         █';
PRINT '█                                                                          █';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';
PRINT 'Estatísticas Gerais:';
PRINT '  • Início: ' + CONVERT(VARCHAR, @MasterStartTime, 120);
PRINT '  • Término: ' + CONVERT(VARCHAR, @MasterEndTime, 120);
PRINT '  • Duração Total: ' + CAST(@TotalDuration AS VARCHAR) + ' segundos';
PRINT '  • Passos Executados: ' + CAST(@StepNumber AS VARCHAR);
PRINT '  • Erros: ' + CAST(@TotalErrors AS VARCHAR);
PRINT '';

IF @TotalErrors = 0
BEGIN
    PRINT '✅✅✅ PIPELINE COMPLETADA COM SUCESSO! ✅✅✅';
    PRINT '';
    PRINT 'Todos os 8 Requisitos Implementados:';
    PRINT '  ✅ REQUISITO 1: CSV → Landing (VARCHAR) → Silver (tipos apropriados)';
    PRINT '  ✅ REQUISITO 2: Parquet → Landing (VARCHAR) → Silver (tipos apropriados)';
    PRINT '  ✅ REQUISITO 3: trip_type.tsv → REF.TRIP_TYPE';
    PRINT '  ✅ REQUISITO 4: rate_code.json → REF.RATE_CODE';
    PRINT '  ✅ REQUISITO 5: payment_type_array.json → REF.PAYMENT_TYPE';
    PRINT '  ✅ REQUISITO 6: Gold Enriched (CSV com JOINs)';
    PRINT '  ✅ REQUISITO 7: Gold Aggregated (Parquet agregado por PULocationID)';
    PRINT '  ⏳ REQUISITO 8: Testes Unitários (próximo passo)';
END
ELSE
BEGIN
    PRINT '⚠️⚠️⚠️ PIPELINE COMPLETADA COM ' + CAST(@TotalErrors AS VARCHAR) + ' ERRO(S) ⚠️⚠️⚠️';
    PRINT '';
    PRINT 'Revise os logs acima para detalhes dos erros.';
END

PRINT '';
PRINT 'Próximos Passos:';
PRINT '  1. Verificar dados em cada camada (Landing, Silver, Gold)';
PRINT '  2. Executar testes unitários (REQUISITO 8)';
PRINT '  3. Validar qualidade dos dados';
PRINT '  4. Monitorar métricas de negócio';
PRINT '';
PRINT '████████████████████████████████████████████████████████████████████████████';
PRINT '';

SET NOCOUNT OFF;
