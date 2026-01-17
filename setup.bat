@echo off
setlocal EnableExtensions
set "LOG=%~dp0setup.log"
if exist "%LOG%" del /q "%LOG%" >nul 2>&1
echo ============================================================
echo        YOLO Training Setup - Windows
echo ============================================================
echo.
echo 📝 Log file: %LOG%
echo.
echo [START] %date% %time%> "%LOG%"
chcp 65001 >nul
>> "%LOG%" echo [INFO] Code page set to UTF-8

REM Check if Python is installed
call :run python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found!
call :run python --version
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist venv (
    echo    Virtual environment already exists.
    set /p RECREATE="   Recreate? (y/N): "
    if /i "%RECREATE%"=="y" (
        rmdir /s /q venv
        call :run python -m venv venv
        if errorlevel 1 goto :fail
    )
) else (
    call :run python -m venv venv
    if errorlevel 1 goto :fail
)

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call :run call venv\Scripts\activate.bat
if errorlevel 1 goto :fail

REM Upgrade pip
echo.
echo 📥 Upgrading pip...
call :run python -m pip install --upgrade pip
if errorlevel 1 goto :fail

REM Install PyTorch with CUDA
echo.
echo ============================================================
echo    Installing PyTorch with CUDA support
echo ============================================================
echo.
echo    This will install PyTorch with CUDA 12.1 support.
echo    If you have a different CUDA version, please modify this script.
echo.

call :run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 goto :fail

REM Install Ultralytics (YOLOv11)
echo.
echo 📥 Installing Ultralytics (YOLO)...
call :run pip install ultralytics
if errorlevel 1 goto :fail

REM Install Roboflow
echo.
echo 📥 Installing Roboflow...
call :run pip install roboflow
if errorlevel 1 goto :fail

REM Install additional dependencies
echo.
echo 📥 Installing additional dependencies...
call :run pip install opencv-python
if errorlevel 1 goto :fail
call :run pip install matplotlib
if errorlevel 1 goto :fail
call :run pip install pandas
if errorlevel 1 goto :fail
call :run pip install tqdm
if errorlevel 1 goto :fail

REM Verify installation
echo.
echo ============================================================
echo    Verifying Installation
echo ============================================================
echo.

echo 🔍 Checking PyTorch...
call :run python -c "import torch; print(f'   PyTorch: {torch.__version__}')"
if errorlevel 1 goto :fail
call :run python -c "import torch; print(f'   CUDA Available: {torch.cuda.is_available()}')"
if errorlevel 1 goto :fail
call :run python -c "import torch; print(f'   CUDA Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
if errorlevel 1 goto :fail

echo.
echo 🔍 Checking Ultralytics...
call :run python -c "import ultralytics; print(f'   Ultralytics: {ultralytics.__version__}')"
if errorlevel 1 goto :fail

echo.
echo 🔍 Checking Roboflow...
call :run python -c "import roboflow; print(f'   Roboflow: {roboflow.__version__}')"
if errorlevel 1 goto :fail

echo.
echo ============================================================
echo    ✅ Setup Complete!
echo ============================================================
echo.
echo    To start training, run: run.bat
echo    Or manually:
echo      1. Activate venv: venv\Scripts\activate.bat
echo      2. Run: python main.py
echo.
pause
exit /b 0

:run
echo.>> "%LOG%"
echo [RUN] %*>> "%LOG%"
%*>> "%LOG%" 2>&1
set "ERR=%errorlevel%"
echo [EXIT] %ERR%>> "%LOG%"
exit /b %ERR%

:fail
echo.
echo ❌ Setup failed. Please review the error above.
echo 📝 Log saved at: %LOG%
echo.
pause
exit /b 1
