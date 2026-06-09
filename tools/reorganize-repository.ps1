# Reorganizacao Automatica do Repositorio
# Purpose: Move arquivos soltos para estrutura organizada
# Usage: .\tools\reorganize-repository.ps1

param(
    [switch]$DryRun,
    [switch]$UseGitMv = $true
)

$ErrorActionPreference = "Continue"

# Define as mapeações de movimento
$moves = @(
    # Relatórios → /docs/reports/
    @{ source = 'TIER1-COMPLETION-REPORT.md'; destination = 'docs/reports' }
    @{ source = 'TIER1-FINAL-SUMMARY.md'; destination = 'docs/reports' }
    @{ source = 'TIER2-IMPLEMENTATION-SUMMARY.md'; destination = 'docs/reports' }
    @{ source = 'TIER2-PHASE2-SUMMARY.md'; destination = 'docs/reports' }
    @{ source = 'FINAL-INTEGRATION-REPORT.md'; destination = 'docs/reports' }
    @{ source = 'CLEANUP-REPORT.md'; destination = 'docs/reports' }
    @{ source = 'EXEC-SUMMARY.txt'; destination = 'docs/reports' }
    @{ source = 'INTEGRATION-COMPLETE.md'; destination = 'docs/reports' }
    @{ source = 'WORKFLOW-INTEGRATION-STATUS.md'; destination = 'docs/reports' }
    @{ source = 'WORKFLOW-INTEGRATION-REPORT.json'; destination = 'docs/reports' }
    @{ source = 'WORKFLOW-INTEGRATION-FINAL-STATUS.txt'; destination = 'docs/reports' }
    
    # Planos & Checklists → /docs/project-plans/
    @{ source = 'PHASE-5-COMPLETION-SUMMARY.md'; destination = 'docs/project-plans' }
    @{ source = 'PROJECT-COMPLETION-SUMMARY.md'; destination = 'docs/project-plans' }
    @{ source = 'REPOSITORY-STRUCTURE.md'; destination = 'docs/project-plans' }
    @{ source = 'INTEGRATION-CHECKLIST.md'; destination = 'docs/project-plans' }
    @{ source = 'BRADESCO-TIER1-EXECUTION-PLAN.md'; destination = 'docs/project-plans' }
    @{ source = 'BRADESCO-TIER1-VALIDATION-REPORT.md'; destination = 'docs/project-plans' }
    @{ source = 'GAP-ANALYSIS-REPORT.md'; destination = 'docs/project-plans' }
    
    # Scripts de Validação → /tools/validation/
    @{ source = 'WORKFLOW-INTEGRATION-CHECK.py'; destination = 'tools/validation' }
    @{ source = 'WORKFLOW-INTEGRATION-CHECK-v2.py'; destination = 'tools/validation' }
    @{ source = 'run_bradesco_tier1_validation.py'; destination = 'tools/validation' }
    
    # Scripts de Utilidade → /tools/utilities/
    @{ source = 'test_telemetry_system.py'; destination = 'tools/utilities' }
    
    # Configuração → /config/
    @{ source = 'requirements-dev.txt'; destination = 'config' }
    @{ source = 'azure-pipelines.yml'; destination = 'config' }
)

# Funcao para verificar se esta em um repositorio git
function Test-GitRepository {
    if (Test-Path .git) {
        return $true
    }
    return $false
}

# Função para mover arquivo
function Move-RepositoryFile {
    param(
        [string]$Source,
        [string]$Destination,
        [bool]$UseGitMv,
        [bool]$DryRun
    )
    
    if (-not (Test-Path $Source)) {
        Write-Host "WARNING: File not found: $Source" -ForegroundColor Yellow
        return $false
    }
    
    # Garantir que o diretorio de destino existe
    if (-not (Test-Path $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }
    
    $targetPath = Join-Path $Destination (Split-Path $Source -Leaf)
    
    if ($DryRun) {
        Write-Host "[DRY RUN] $Source -> $targetPath" -ForegroundColor Cyan
        return $true
    }
    
    if ($UseGitMv -and (Test-GitRepository)) {
        try {
            git mv $Source $targetPath 2>&1 | Out-Null
            Write-Host "OK: $Source -> $targetPath (via git mv)" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "WARNING: Git mv failed, using Move-Item: $_" -ForegroundColor Yellow
            Move-Item -Path $Source -Destination $targetPath -Force
            Write-Host "OK: $Source -> $targetPath (via Move-Item)" -ForegroundColor Green
            return $true
        }
    }
    else {
        Move-Item -Path $Source -Destination $targetPath -Force
        Write-Host "OK: $Source -> $targetPath" -ForegroundColor Green
        return $true
    }
}

# Main
function Invoke-RepositoryReorganization {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Repository Reorganization Script" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "[INFO] Mode: DRY RUN (no changes made)" -ForegroundColor Yellow
        Write-Host ""
    }
    
    # Verificar se estamos no diretorio correto
    if (-not (Test-Path 'src/shared')) {
        Write-Host "ERROR: Please run this script from the repository root" -ForegroundColor Red
        exit 1
    }
    
    $successCount = 0
    $failureCount = 0
    
    # Processar cada movimento
    foreach ($move in $moves) {
        $source = $move.source
        $destination = $move.destination
        
        if (Move-RepositoryFile -Source $source -Destination $destination -UseGitMv $UseGitMv -DryRun $DryRun) {
            $successCount++
        }
        else {
            $failureCount++
        }
    }
    
    # Resumo
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "Summary" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Successful: $successCount" -ForegroundColor Green
    if ($failureCount -gt 0) {
        Write-Host "Failed: $failureCount" -ForegroundColor Red
    }
    
    if ($DryRun) {
        Write-Host ""
        Write-Host "To execute for real, run without -DryRun parameter:" -ForegroundColor Yellow
        Write-Host "  .\tools\reorganize-repository.ps1" -ForegroundColor Yellow
    }
    else {
        Write-Host ""
        Write-Host "Repository reorganized successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Green
        Write-Host "  1. Review changes: git status" -ForegroundColor Cyan
        Write-Host "  2. Commit: git commit -m 'refactor: organize repository structure'" -ForegroundColor Cyan
        Write-Host "  3. Push: git push origin main" -ForegroundColor Cyan
        Write-Host ""
    }
}

# Executar
Invoke-RepositoryReorganization
