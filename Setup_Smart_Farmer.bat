@echo off
setlocal
title Smart Farmer AI - Initial Setup
color 0E
cls
echo ========================================================
echo        SMART FARMER AI - ONE-CLICK SYSTEM SETUP
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python installation...
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ and re-run this setup.
    pause
    exit /b 1
)

echo [2/4] Setting up Virtual Environment (.venv)...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
)

echo [3/4] Installing dependencies from requirements.txt...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies might have failed to install.
)

echo [4/4] Configuring Environment and Database...
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo Created .env from template.
)

if not exist "faemer.db" (
    echo Initializing database with seed data...
    ".venv\Scripts\python.exe" seed_data.py
)

echo.
echo ========================================================
echo                SETUP COMPLETED SUCCESSFULLY!
echo ========================================================
echo.
echo You can now run the app anytime using Start_Smart_Farmer.bat
echo or the "Smart Farmer AI" shortcut on your Desktop.
echo.
pause
