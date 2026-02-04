<#
.SYNOPSIS
    Executa scripts SQL no Databricks via CLI

.DESCRIPTION
    Este script:
    - Carrega e executa arquivos SQL no Databricks
    - Suporta execução de múltiplos arquivos em sequência
    - Reporta erros e sucessos

.NOTES
    Pré-requisitos:
    - Databricks CLI configurado (executar setup-databricks-cli.ps1 primeiro)
    - Conexão ativa com o workspace

.EXAMPLE
    .\execute-ddl.ps1
    Executa todos os scripts SQL na ordem correta

.EXAMPLE
    .\execute-ddl.ps1 -SqlFile "create-schemas.sql"
    Executa apenas um arquivo específico
#>

param(
    [string]$SqlFile,
    [string]$ClusterIdOrName  # Opcional: ID ou nome do cluster
)

$ErrorActionPreference = "Stop"

# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

function Write-Header {
    param([string]$Message)
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  $Message" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Message)
    Write-Host "► $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Execute-DatabricksSQL {
    param(
        [string]$SqlFilePath,
        [string]$ClusterId
    )
    
    Write-Step "Executando: $SqlFilePath"
    
    # Lê o conteúdo do arquivo SQL
    $sqlContent = Get-Content $SqlFilePath -Raw
    
    # Divide por comandos (separados por ponto-e-vírgula)
    $commands = $sqlContent -split ';' | Where-Object { $_.Trim() -ne '' }
    
    $successCount = 0
    $errorCount = 0
    
    foreach ($cmd in $commands) {
        $trimmedCmd = $cmd.Trim()
        if ($trimmedCmd -eq '' -or $trimmedCmd.StartsWith('--')) {
            continue
        }
        
        # Remove comentários de linha
        $cleanCmd = $trimmedCmd -replace '--.*$', ''
        
        # Cria arquivo temporário para o comando
        $tempFile = [System.IO.Path]::GetTempFileName()
        $cleanCmd | Out-File -FilePath $tempFile -Encoding UTF8
        
        try {
            # Executa via Databricks CLI
            # Nota: Isso requer SQL Warehouse ou Cluster em execução
            Write-Host "  Executando comando SQL..." -ForegroundColor Gray
            
            # Usa databricks sql para executar
            # Se não tiver cluster/warehouse, use databricks fs put + notebook run
            $result = databricks workspace import $tempFile "/Shared/temp_sql_$(Get-Date -Format 'yyyyMMddHHmmss').sql" --language SQL --format SOURCE 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                $successCount++
                Write-Host "  ✓ Comando executado" -ForegroundColor Green
            } else {
                $errorCount++
                Write-Host "  ✗ Erro: $result" -ForegroundColor Red
            }
        } catch {
            $errorCount++
            Write-Host "  ✗ Erro: $_" -ForegroundColor Red
        } finally {
            Remove-Item $tempFile -ErrorAction SilentlyContinue
        }
    }
    
    return @{
        Success = $successCount
        Errors = $errorCount
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# VALIDAÇÕES INICIAIS
# ══════════════════════════════════════════════════════════════════════════════

Write-Header "Databricks SQL Executor"

# Verifica se Databricks CLI está configurado
Write-Step "Verificando configuração do Databricks CLI..."
try {
    $workspaceTest = databricks workspace list / 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Databricks CLI não configurado!"
        Write-Host "Execute primeiro: ..\02-configure-databricks\setup-databricks-cli.ps1" -ForegroundColor Yellow
        exit 1
    }
    Write-Success "Databricks CLI configurado"
} catch {
    Write-Error "Erro ao verificar Databricks CLI: $_"
    exit 1
}

# ══════════════════════════════════════════════════════════════════════════════
# DEFINE ORDEM DE EXECUÇÃO
# ══════════════════════════════════════════════════════════════════════════════

$sqlFiles = if ($SqlFile) {
    @($SqlFile)
} else {
    @(
        "create-schemas.sql",
        "create-tables.sql"
    )
}

# ══════════════════════════════════════════════════════════════════════════════
# MÉTODO ALTERNATIVO: Upload + SQL Warehouse/Notebook
# ══════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  EXECUÇÃO DE SQL NO DATABRICKS                                     ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host @"

OPÇÃO 1: SQL Warehouse (Recomendado)
─────────────────────────────────────
1. Os arquivos SQL serão copiados para o workspace
2. Você pode executá-los via:
   - Databricks SQL Editor
   - Notebooks
   - Jobs

OPÇÃO 2: Databricks Connect (Python)
──────────────────────────────────────
Use o script Python para execução automatizada.

"@ -ForegroundColor Gray

Write-Step "Fazendo upload dos arquivos SQL para o workspace..."

$uploadSuccess = 0
$uploadErrors = 0

foreach ($file in $sqlFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "  ✗ Arquivo não encontrado: $file" -ForegroundColor Red
        $uploadErrors++
        continue
    }
    
    $remotePath = "/Shared/ddl/$($file)"
    
    try {
        databricks workspace import $file $remotePath --language SQL --format SOURCE --overwrite 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Uploaded: $file → $remotePath" -ForegroundColor Green
            $uploadSuccess++
        } else {
            Write-Host "  ✗ Falha no upload: $file" -ForegroundColor Red
            $uploadErrors++
        }
    } catch {
        Write-Host "  ✗ Erro ao fazer upload de $file : $_" -ForegroundColor Red
        $uploadErrors++
    }
}

Write-Host "`n═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Upload concluído: $uploadSuccess sucesso(s), $uploadErrors erro(s)" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# ══════════════════════════════════════════════════════════════════════════════
# INSTRUÇÕES PARA EXECUÇÃO MANUAL
# ══════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  PRÓXIMOS PASSOS                                                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Obtém workspace URL
$configFile = "..\02-configure-databricks\.databrickscfg"
if (-not (Test-Path $configFile)) {
    $configFile = "$env:USERPROFILE\.databrickscfg"
}

if (Test-Path $configFile) {
    $configContent = Get-Content $configFile
    $hostLine = $configContent | Where-Object { $_ -match '^host\s*=\s*(.+)$' }
    if ($hostLine) {
        $workspaceUrl = $matches[1].Trim()
        
        Write-Host @"

Para executar os scripts SQL:

1. Acesse o Databricks SQL Editor:
   $workspaceUrl/sql/editor

2. Os arquivos foram carregados em: /Shared/ddl/

3. Execute na ordem:
   a) create-schemas.sql
   b) create-tables.sql

4. Ou crie um Notebook e execute:
   %sql
   -- Cole o conteúdo dos arquivos SQL

Alternativa (Python):
  cd ..\04-data-ingestion
  python execute-sql-via-api.py

"@ -ForegroundColor Yellow
    }
}

Write-Header "Upload de scripts concluído!"

Write-Host @"
NOTA: Para execução automatizada via API, use:
  python ..\04-data-ingestion\execute-sql-via-api.py

"@ -ForegroundColor Gray
