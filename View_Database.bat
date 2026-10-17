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
".venv\Scripts\python.exe" "export_data.py" >nul 2>&1

if errorlevel 1 (
    echo.
    echo Database viewer exited with an error. See the message above.
) else (
    echo.
    echo [INFO] Exported text report saved to:
    echo        1. database_report.txt (in this folder)
    echo        2. Smart_Farmer_Database_Report.txt (on your Desktop)
    echo        3. database_data/ (CSV table files)
)
echo.
echo Press any key to close...
pause >nul
endlocal
