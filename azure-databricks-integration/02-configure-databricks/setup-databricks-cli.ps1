<#
.SYNOPSIS
    Configura o Databricks CLI com autenticação via token

.DESCRIPTION
    Este script:
    - Instala Databricks CLI (se necessário)
    - Configura perfil de autenticação
    - Testa conectividade

.NOTES
    Pré-requisitos:
    - Python 3.9+ instalado
    - Workspace Databricks já provisionado
    - Personal Access Token gerado

.EXAMPLE
    .\setup-databricks-cli.ps1
    Configuração interativa

.EXAMPLE
    .\setup-databricks-cli.ps1 -WorkspaceUrl "https://adb-123.azuredatabricks.net" -Token "dapi..."
    Configuração automatizada
#>

param(
    [string]$WorkspaceUrl,
    [string]$Token,
    [string]$ProfileName = "DEFAULT"
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

# ══════════════════════════════════════════════════════════════════════════════
# VALIDAÇÕES INICIAIS
# ══════════════════════════════════════════════════════════════════════════════

Write-Header "Databricks CLI - Configuração de Autenticação"

# Verifica Python
Write-Step "Verificando Python..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python detectado: $pythonVersion"
} catch {
    Write-Error "Python não encontrado!"
    Write-Host "Instale com: winget install Python.Python.3.11" -ForegroundColor Yellow
    exit 1
}

# ══════════════════════════════════════════════════════════════════════════════
# INSTALA DATABRICKS CLI
# ══════════════════════════════════════════════════════════════════════════════

Write-Step "Verificando Databricks CLI..."
try {
    $databricksVersion = databricks --version 2>&1
    Write-Success "Databricks CLI já instalado: $databricksVersion"
} catch {
    Write-Step "Instalando Databricks CLI..."
    pip install databricks-cli
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Databricks CLI instalado com sucesso!"
    } else {
        Write-Error "Falha na instalação!"
        exit 1
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# OBTER WORKSPACE URL
# ══════════════════════════════════════════════════════════════════════════════

if (-not $WorkspaceUrl) {
    # Tentar ler do arquivo de informações do workspace
    $infoFile = "..\01-provision-azure\databricks-workspace-info.json"
    if (Test-Path $infoFile) {
        $workspaceInfo = Get-Content $infoFile | ConvertFrom-Json
        $WorkspaceUrl = $workspaceInfo.workspaceUrl
        Write-Host "► URL do workspace detectada: $WorkspaceUrl" -ForegroundColor Gray
    } else {
        Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
        Write-Host "║  COMO OBTER A URL DO WORKSPACE                                     ║" -ForegroundColor Yellow
        Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
        Write-Host @"
1. Acesse o portal Azure: https://portal.azure.com
2. Navegue até seu Databricks workspace
3. Copie a 'Workspace URL' (formato: https://adb-123456789.azuredatabricks.net)

Ou execute:
az databricks workspace show --name <workspace-name> --resource-group <rg-name> --query workspaceUrl -o tsv
"@ -ForegroundColor Gray
        
        $WorkspaceUrl = Read-Host "`nDigite a URL do workspace"
    }
}

# Normaliza URL
if (-not $WorkspaceUrl.StartsWith("https://")) {
    $WorkspaceUrl = "https://$WorkspaceUrl"
}

# ══════════════════════════════════════════════════════════════════════════════
# OBTER TOKEN
# ══════════════════════════════════════════════════════════════════════════════

if (-not $Token) {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║  COMO GERAR UM PERSONAL ACCESS TOKEN                               ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host @"
1. Acesse: $WorkspaceUrl
2. Clique no ícone do usuário (canto superior direito)
3. User Settings → Developer
4. Access Tokens → Generate New Token
5. Defina:
   - Comment: "Databricks CLI - Data Migration"
   - Lifetime: 90 dias (recomendado)
6. Clique em 'Generate'
7. IMPORTANTE: Copie o token (ele aparece apenas UMA vez!)

"@ -ForegroundColor Gray
    
    $Token = Read-Host "Digite o Personal Access Token" -AsSecureString
    $Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Token)
    )
}

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURA DATABRICKS CLI
# ══════════════════════════════════════════════════════════════════════════════

Write-Step "Configurando perfil '$ProfileName'..."

# Cria diretório de configuração se não existir
$configDir = "$env:USERPROFILE\.databrickscfg"
if (-not (Test-Path $configDir)) {
    Write-Step "Criando arquivo de configuração..."
}

# Configura via comando
$env:DATABRICKS_HOST = $WorkspaceUrl
$env:DATABRICKS_TOKEN = $Token

# Escreve arquivo de configuração
$configContent = @"
[DEFAULT]
host = $WorkspaceUrl
token = $Token

# Para usar este perfil:
# databricks workspace list --profile DEFAULT
# 
# Para criar perfis adicionais (dev, staging, prod):
# databricks configure --token --profile dev
"@

$configContent | Out-File -FilePath "$env:USERPROFILE\.databrickscfg" -Encoding UTF8 -Force

Write-Success "Configuração salva em: $env:USERPROFILE\.databrickscfg"

# ══════════════════════════════════════════════════════════════════════════════
# TESTA CONECTIVIDADE
# ══════════════════════════════════════════════════════════════════════════════

Write-Step "Testando conectividade..."

try {
    $workspaces = databricks workspace list / 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Conexão estabelecida com sucesso!"
        Write-Host "  Workspace URL: $WorkspaceUrl" -ForegroundColor Gray
        Write-Host "  Autenticação: Token válido" -ForegroundColor Gray
    } else {
        Write-Error "Falha na conexão!"
        Write-Host $workspaces -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Error "Erro ao testar conectividade: $_"
    exit 1
}

# ══════════════════════════════════════════════════════════════════════════════
# SALVA VARIÁVEIS DE AMBIENTE (OPCIONAL)
# ══════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  CONFIGURAR VARIÁVEIS DE AMBIENTE (OPCIONAL)                       ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

$saveEnv = Read-Host "Deseja criar arquivo .env para uso em scripts Python? (s/N)"

if ($saveEnv -eq "s" -or $saveEnv -eq "S") {
    $envContent = @"
# Databricks Configuration
# IMPORTANTE: Não commitar este arquivo no Git!
# Adicione '.env' ao .gitignore

DATABRICKS_HOST=$WorkspaceUrl
DATABRICKS_TOKEN=$Token

# Para usar em Python:
# from dotenv import load_dotenv
# load_dotenv()
# 
# import os
# host = os.getenv('DATABRICKS_HOST')
# token = os.getenv('DATABRICKS_TOKEN')
"@
    
    $envFile = "..\..\.env"
    $envContent | Out-File -FilePath $envFile -Encoding UTF8 -Force
    Write-Success "Arquivo .env criado: $envFile"
    Write-Host "  IMPORTANTE: Adicione '.env' ao .gitignore!" -ForegroundColor Red
    
    # Cria .gitignore se não existir
    $gitignoreFile = "..\..\..\.gitignore"
    if (-not (Test-Path $gitignoreFile)) {
        @"
# Databricks Credentials
.env
.databrickscfg
databricks-workspace-info.json
*.token

# Python
__pycache__/
*.pyc
venv/
.venv/

# Logs
*.log
"@ | Out-File -FilePath $gitignoreFile -Encoding UTF8
        Write-Success "Arquivo .gitignore criado"
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# PRÓXIMOS PASSOS
# ══════════════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  PRÓXIMOS PASSOS                                                   ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host @"

✓ Databricks CLI configurado com sucesso!

Comandos úteis:
  databricks workspace list /               # Listar workspace
  databricks clusters list                  # Listar clusters
  databricks fs ls dbfs:/                   # Listar arquivos DBFS

Próximas etapas:
  1. Criar schemas e tabelas:
     cd ..\03-database-setup
     .\execute-ddl.ps1

  2. Ingerir dados:
     cd ..\04-data-ingestion
     python ingest-from-csv.py

  3. Ou execute tudo:
     cd ..\05-orchestration
     .\run-all.ps1

"@ -ForegroundColor Yellow

Write-Header "Configuração concluída!"
