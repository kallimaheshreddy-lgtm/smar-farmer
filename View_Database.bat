@echo off
setlocal
title Smart Farmer AI - SQLite Database Viewer
color 0B
cls
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: The project's Python environment was not found.
    echo Expected: "%~dp0.venv\Scripts\python.exe"
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" "inspect_db.py"
if errorlevel 1 (
    echo.
    echo Database viewer exited with an error. See the message above.
)
echo.
echo Press any key to close...
pause >nul
endlocal
