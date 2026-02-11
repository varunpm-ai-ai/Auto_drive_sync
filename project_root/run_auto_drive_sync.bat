@echo off
title Auto Drive Sync v1.0.0

echo ==========================================
echo   Starting Auto Drive Sync v1.0.0
echo ==========================================
echo.

REM --- Activate virtual environment (ABSOLUTE PATH) ---
call "C:\Machine Learning\Auto_drive_sync\.venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM --- Move to actual project root ---
cd /d "C:\Machine Learning\Auto_drive_sync\project_root"

REM --- Sanity check (this proves success) ---
echo Using Python:
where python
python --version
echo.

REM --- Run application ---
python main.py

echo.
echo ==========================================
echo   Auto Drive Sync stopped
echo ==========================================
pause
