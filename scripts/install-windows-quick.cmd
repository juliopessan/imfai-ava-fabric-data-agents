@echo off
REM Windows quick installer wrapper for winget
where winget >nul 2>&1
if errorlevel 1 (
  echo winget not found. Install 'App Installer' from Microsoft Store or ensure winget is on PATH.
  exit /b 1
)

echo Installing astral-sh.uv via winget...
winget install astral-sh.uv
if errorlevel 1 (
  echo winget installation failed with exit code %ERRORLEVEL%.
  exit /b %ERRORLEVEL%
)
echo Installed successfully.
exit /b 0
