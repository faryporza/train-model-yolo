@echo off
chcp 65001 >nul
echo ============================================================
echo        YOLO Training Pipeline
echo ============================================================
echo.

REM Check if venv exists
if not exist venv (
    echo ❌ Virtual environment not found!
    echo    Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run main script
python main.py

REM Keep window open after script ends
echo.
pause
