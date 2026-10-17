@echo off
title Smart Farmer AI Server
color 0A
cls
echo ========================================================
echo        STARTING SMART FARMER AI FOR INDIAN FARMERS
echo ========================================================
echo.
echo Local Server Address: http://127.0.0.1:5000
echo.

cd /d "%~dp0"

echo Opening browser at http://127.0.0.1:5000 ...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

echo.
echo Server is running! Keep this window open while using the app.
echo Press Ctrl + C to stop the server anytime.
echo.

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run.py
) else (
    python run.py
)

pause
