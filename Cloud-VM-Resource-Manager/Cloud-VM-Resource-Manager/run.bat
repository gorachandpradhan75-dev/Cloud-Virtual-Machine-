@echo off
title Cloud VM Resource Manager
cd /d "%~dp0"
echo ==========================================
echo    CLOUD VM RESOURCE MANAGER
echo ==========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.9+ and enable Add Python to PATH.
  pause
  exit /b 1
)
start "" http://127.0.0.1:8000
python app.py
pause
