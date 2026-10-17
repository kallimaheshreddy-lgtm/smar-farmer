@echo off
setlocal
title Smart Farmer AI - Database Terminal
color 0E
cls
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

".venv\Scripts\python.exe" "query_db.py"

endlocal
