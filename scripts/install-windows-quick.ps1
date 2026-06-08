param(
    [switch]$Force
)

# Windows Quick Install helper
# Usage: .\install-windows-quick.ps1 [-Force]

if ($env:OS -notlike '*Windows*' -and $PSVersionTable.Platform -ne 'Win32NT') {
    Write-Error "This script must be run on Windows."
    exit 1
}

$winget = Get-Command winget -ErrorAction SilentlyContinue
if (-not $winget) {
    Write-Error "winget not found. Install 'App Installer' from Microsoft Store or ensure winget is on PATH."
    exit 2
}

Write-Host "Installing package 'astral-sh.uv' via winget..." -ForegroundColor Cyan

$args = @('install','astral-sh.uv')
if (-not $Force) { $args += '--silent' }

try {
    $proc = Start-Process -FilePath $winget.Source -ArgumentList $args -Wait -NoNewWindow -PassThru -ErrorAction Stop
    if ($proc.ExitCode -eq 0) {
        Write-Host "astral-sh.uv installed successfully." -ForegroundColor Green
        exit 0
    }
    else {
        Write-Error "winget exited with code $($proc.ExitCode)"
        exit $proc.ExitCode
    }
}
catch {
    Write-Error "Installation failed: $_"
    exit 3
}
