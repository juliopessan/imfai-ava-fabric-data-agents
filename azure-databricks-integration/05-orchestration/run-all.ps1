<#
.SYNOPSIS
    Orquestrador completo - Executa todo o pipeline Databricks

.DESCRIPTION
    Este script executa todas as etapas do pipeline:
    1. Provisionamento do Azure Databricks workspace
    2. Configuração do Databricks CLI
    3. Criação de schemas e tabelas
    4. Ingestão de dados de fontes externas

.NOTES
    Pré-requisitos:
    - Azure CLI instalado e configurado
    - Python 3.9+ instalado
    - Credenciais Azure disponíveis

.EXAMPLE
    .\run-all.ps1
    Executa todo o pipeline do início ao fim

.EXAMPLE
    .\run-all.ps1 -SkipProvisioning
    Pula o provisionamento (usa workspace existente)

.EXAMPLE
    .\run-all.ps1 -IngestOnly
    Executa apenas a ingestão de dados
#>

param(
    [switch]$SkipProvisioning,      # Pula o provisionamento do workspace
    [switch]$SkipConfig,            # Pula a configuração do CLI
    [switch]$SkipDDL,               # Pula a criação de tabelas
    [switch]$SkipIngestion,         # Pula a ingestão de dados
    [switch]$IngestOnly,            # Executa apenas ingestão
    [string]$ConfigFile = "..\01-provision-azure\config.template.json"
)

$ErrorActionPreference = "Stop"

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

$global:ExecutionLog = @()
$global:StartTime = Get-Date

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

function Log-Step {
    param(
        [string]$Step,
        [string]$Status,
        [string]$Details
    )
    
    $global:ExecutionLog += [PSCustomObject]@{
        Step = $Step
        Status = $Status
        Details = $Details
        Timestamp = Get-Date
    }
}

function Execute-Module {
    param(
        [string]$ModuleName,
        [string]$ModulePath,
        [scriptblock]$ScriptBlock
    )
    
    Write-Header "MÓDULO: $ModuleName"
    
    $moduleStart = Get-Date
    
    try {
        & $ScriptBlock
        
        $duration = ((Get-Date) - $moduleStart).TotalSeconds
        Write-Success "$ModuleName concluído em $([math]::Round($duration, 2))s"
        Log-Step -Step $ModuleName -Status "SUCCESS" -Details "Duração: $([math]::Round($duration, 2))s"
        
        return $true
    }
    catch {
        $duration = ((Get-Date) - $moduleStart).TotalSeconds
        Write-Error "$ModuleName falhou: $_"
        Log-Step -Step $ModuleName -Status "FAILED" -Details $_.Exception.Message
        
        return $false
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════════════════════════════

Clear-Host

Write-Host @"

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   █████╗ ███████╗██╗   ██╗██████╗ ███████╗                                ║
║  ██╔══██╗╚══███╔╝██║   ██║██╔══██╗██╔════╝                                ║
║  ███████║  ███╔╝ ██║   ██║██████╔╝█████╗                                  ║
║  ██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔══╝                                  ║
║  ██║  ██║███████╗╚██████╔╝██║  ██║███████╗                                ║
║  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                                ║
║                                                                            ║
║           DATABRICKS INTEGRATION - FULL PIPELINE                          ║
║                 Avanade™ Core - Data Engineering                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

Write-Host "Início da execução: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Gray

# ══════════════════════════════════════════════════════════════════════════════
# VALIDAÇÕES INICIAIS
# ══════════════════════════════════════════════════════════════════════════════

if ($IngestOnly) {
    Write-Step "Modo: Ingestão apenas"
    $SkipProvisioning = $true
    $SkipConfig = $true
    $SkipDDL = $true
}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: PROVISIONAMENTO DO AZURE DATABRICKS
# ══════════════════════════════════════════════════════════════════════════════

if (-not $SkipProvisioning) {
    $success = Execute-Module -ModuleName "Provisionamento Azure Databricks" -ModulePath "..\01-provision-azure" -ScriptBlock {
        
        Push-Location "..\01-provision-azure"
        
        try {
            # Verifica se config file existe
            if (-not (Test-Path "config.template.json")) {
                throw "Arquivo config.template.json não encontrado!"
            }
            
            # Executa provisionamento
            .\provision-databricks.ps1
            
            if ($LASTEXITCODE -ne 0) {
                throw "Provisionamento falhou com código: $LASTEXITCODE"
            }
        }
        finally {
            Pop-Location
        }
    }
    
    if (-not $success) {
        Write-Error "Pipeline abortado: Provisionamento falhou"
        exit 1
    }
} else {
    Write-Step "Pulando provisionamento (workspace existente)"
    Log-Step -Step "Provisionamento" -Status "SKIPPED" -Details "Usar workspace existente"
}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: CONFIGURAÇÃO DO DATABRICKS CLI
# ══════════════════════════════════════════════════════════════════════════════

if (-not $SkipConfig) {
    $success = Execute-Module -ModuleName "Configuração Databricks CLI" -ModulePath "..\02-configure-databricks" -ScriptBlock {
        
        Push-Location "..\02-configure-databricks"
        
        try {
            # Verifica se já está configurado
            $alreadyConfigured = $false
            
            if (Test-Path "$env:USERPROFILE\.databrickscfg") {
                Write-Step "Databricks CLI já configurado"
                $alreadyConfigured = $true
            }
            
            if (-not $alreadyConfigured) {
                Write-Step "Iniciando configuração do Databricks CLI..."
                Write-Host @"

IMPORTANTE: Você precisará fornecer:
1. Workspace URL (pode ser detectada automaticamente)
2. Personal Access Token (gere no Databricks)

"@ -ForegroundColor Yellow
                
                .\setup-databricks-cli.ps1
                
                if ($LASTEXITCODE -ne 0) {
                    throw "Configuração falhou"
                }
            }
        }
        finally {
            Pop-Location
        }
    }
    
    if (-not $success) {
        Write-Error "Pipeline abortado: Configuração falhou"
        exit 1
    }
} else {
    Write-Step "Pulando configuração do CLI"
    Log-Step -Step "Configuração CLI" -Status "SKIPPED" -Details "CLI já configurado"
}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3: CRIAÇÃO DE SCHEMAS E TABELAS (DDL)
# ══════════════════════════════════════════════════════════════════════════════

if (-not $SkipDDL) {
    $success = Execute-Module -ModuleName "Criação de Schemas e Tabelas" -ModulePath "..\03-database-setup" -ScriptBlock {
        
        Push-Location "..\03-database-setup"
        
        try {
            Write-Step "Executando scripts DDL..."
            
            # Verifica se Python está disponível para execução automatizada
            $pythonAvailable = Get-Command python -ErrorAction SilentlyContinue
            
            if ($pythonAvailable) {
                Write-Step "Instalando dependências Python..."
                pip install -q -r ..\04-data-ingestion\requirements.txt
                
                # Verifica se variáveis de ambiente estão configuradas
                if ($env:DATABRICKS_HOST -and $env:DATABRICKS_TOKEN) {
                    Write-Step "Executando DDL via Python API..."
                    python ..\04-data-ingestion\execute-sql-via-api.py
                    
                    if ($LASTEXITCODE -ne 0) {
                        throw "Execução de DDL falhou"
                    }
                } else {
                    Write-Step "Fazendo upload dos scripts SQL para o workspace..."
                    .\execute-ddl.ps1
                    
                    Write-Host @"

ATENÇÃO: Scripts SQL foram carregados no workspace Databricks.
Você precisará executá-los manualmente via:
- SQL Editor no Databricks
- Ou configurar DATABRICKS_SQL_WAREHOUSE_ID e executar novamente

"@ -ForegroundColor Yellow
                }
            } else {
                Write-Step "Python não encontrado. Fazendo upload dos scripts..."
                .\execute-ddl.ps1
            }
        }
        finally {
            Pop-Location
        }
    }
    
    if (-not $success) {
        Write-Error "Pipeline abortado: Criação de tabelas falhou"
        exit 1
    }
} else {
    Write-Step "Pulando criação de tabelas"
    Log-Step -Step "DDL" -Status "SKIPPED" -Details "Tabelas já existem"
}

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4: INGESTÃO DE DADOS
# ══════════════════════════════════════════════════════════════════════════════

if (-not $SkipIngestion) {
    $success = Execute-Module -ModuleName "Ingestão de Dados" -ModulePath "..\04-data-ingestion" -ScriptBlock {
        
        Push-Location "..\04-data-ingestion"
        
        try {
            Write-Step "Instalando dependências Python..."
            pip install -q -r requirements.txt
            
            # Busca arquivos CSV no diretório Files
            $csvFiles = Get-ChildItem "..\..\Files\*.csv" -ErrorAction SilentlyContinue
            
            if ($csvFiles) {
                Write-Step "Encontrados $($csvFiles.Count) arquivo(s) CSV para ingestão"
                
                foreach ($csvFile in $csvFiles) {
                    Write-Step "Ingerindo: $($csvFile.Name)"
                    
                    python ingest-from-csv.py --file $csvFile.FullName --table "bronze.taxi_trips_raw" --mode append
                    
                    if ($LASTEXITCODE -eq 0) {
                        Write-Success "Arquivo ingerido: $($csvFile.Name)"
                    } else {
                        Write-Error "Falha ao ingerir: $($csvFile.Name)"
                    }
                }
            } else {
                Write-Step "Nenhum arquivo CSV encontrado em ..\..\Files\"
                Write-Host "Você pode ingerir dados manualmente:" -ForegroundColor Yellow
                Write-Host "  python ingest-from-csv.py --file <caminho> --table bronze.taxi_trips_raw" -ForegroundColor Gray
            }
            
            # Busca arquivos JSON
            $jsonFiles = Get-ChildItem "..\..\Files\*.json" -ErrorAction SilentlyContinue
            
            if ($jsonFiles) {
                Write-Step "Encontrados $($jsonFiles.Count) arquivo(s) JSON"
                
                # Exemplo: ingere payment_type_array.json para tabela de referência
                $paymentTypeFile = $jsonFiles | Where-Object { $_.Name -like "*payment_type*" }
                
                if ($paymentTypeFile) {
                    Write-Step "Ingerindo payment types..."
                    python ingest-from-json.py --file $paymentTypeFile.FullName --table "reference.payment_types" --mode overwrite
                }
            }
        }
        finally {
            Pop-Location
        }
    }
    
    if (-not $success) {
        Write-Error "Ingestão de dados falhou (não-fatal)"
        # Não aborta o pipeline - ingestão pode ser feita depois
    }
} else {
    Write-Step "Pulando ingestão de dados"
    Log-Step -Step "Ingestão" -Status "SKIPPED" -Details "Dados serão ingeridos manualmente"
}

# ══════════════════════════════════════════════════════════════════════════════
# RESUMO DA EXECUÇÃO
# ══════════════════════════════════════════════════════════════════════════════

$totalDuration = ((Get-Date) - $global:StartTime).TotalSeconds

Write-Host "`n`n"
Write-Host "╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                       PIPELINE CONCLUÍDO                                   ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`nRESUMO DA EXECUÇÃO:" -ForegroundColor Cyan
Write-Host "══════════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan

foreach ($logEntry in $global:ExecutionLog) {
    $statusColor = switch ($logEntry.Status) {
        "SUCCESS" { "Green" }
        "FAILED" { "Red" }
        "SKIPPED" { "Yellow" }
        default { "Gray" }
    }
    
    $statusIcon = switch ($logEntry.Status) {
        "SUCCESS" { "✓" }
        "FAILED" { "✗" }
        "SKIPPED" { "○" }
        default { "·" }
    }
    
    Write-Host "$statusIcon $($logEntry.Step): " -NoNewline
    Write-Host $logEntry.Status -ForegroundColor $statusColor -NoNewline
    Write-Host " - $($logEntry.Details)" -ForegroundColor Gray
}

Write-Host "`nTempo total de execução: $([math]::Round($totalDuration, 2))s" -ForegroundColor White
Write-Host "══════════════════════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

# ══════════════════════════════════════════════════════════════════════════════
# PRÓXIMOS PASSOS
# ══════════════════════════════════════════════════════════════════════════════

Write-Host "PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "────────────────────────────────────────────────────────────────────────────" -ForegroundColor Cyan

# Obtém workspace URL
$infoFile = "..\01-provision-azure\databricks-workspace-info.json"
if (Test-Path $infoFile) {
    $workspaceInfo = Get-Content $infoFile | ConvertFrom-Json
    
    Write-Host @"

1. Acesse seu Databricks workspace:
   $($workspaceInfo.workspaceUrl)

2. Verifique as tabelas criadas:
   - bronze.taxi_trips_raw
   - silver.taxi_trips
   - gold.daily_trips_summary

3. Execute transformações:
   - Crie notebooks para processar dados Bronze → Silver → Gold

4. Configure agendamento:
   - Databricks Jobs
   - Azure Data Factory
   - GitHub Actions

5. Monitore:
   - Query History no SQL Editor
   - Cluster Metrics
   - Job Runs

"@ -ForegroundColor Yellow
} else {
    Write-Host @"

1. Configure variáveis de ambiente (se ainda não fez):
   DATABRICKS_HOST=<workspace-url>
   DATABRICKS_TOKEN=<token>
   DATABRICKS_HTTP_PATH=<sql-warehouse-http-path>

2. Execute módulos individualmente conforme necessário:
   - Provisionamento: ..\01-provision-azure\provision-databricks.ps1
   - Configuração: ..\02-configure-databricks\setup-databricks-cli.ps1
   - DDL: ..\03-database-setup\execute-ddl.ps1
   - Ingestão: ..\04-data-ingestion\ingest-from-csv.py

"@ -ForegroundColor Yellow
}

Write-Header "Pipeline finalizado!"

# Retorna código de sucesso
exit 0
