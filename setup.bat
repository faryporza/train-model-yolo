@echo off
setlocal EnableExtensions EnableDelayedExpansion

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

REM -------------------------
REM Check if Python is installed
REM -------------------------
call :run python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 📝 Log saved at: %LOG%
    pause
    exit /b 1
)

echo ✅ Python found!
call :run python --version
echo.

REM -------------------------
REM Create virtual environment
REM -------------------------
echo 📦 Creating virtual environment...
if exist venv (
    echo    Virtual environment already exists.
    set /p RECREATE="   Recreate? (y/N): "
    if /i "!RECREATE!"=="y" (
        rmdir /s /q venv
        call :run python -m venv venv
        if errorlevel 1 goto :fail
    )
) else (
    call :run python -m venv venv
    if errorlevel 1 goto :fail
)

REM -------------------------
REM Activate virtual environment (สำคัญ: ห้าม call ซ้อนผ่าน :run)
REM -------------------------
echo.
echo 🔄 Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ venv\Scripts\activate.bat not found
    >> "%LOG%" echo [ERROR] activate.bat not found
    goto :fail
)
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate venv
    >> "%LOG%" echo [ERROR] Failed to activate venv
    goto :fail
)

REM -------------------------
REM Upgrade pip
REM -------------------------
echo.
echo 📥 Upgrading pip...
call :run python -m pip install --upgrade pip
if errorlevel 1 goto :fail

REM -------------------------
REM Install PyTorch with CUDA 12.1
REM -------------------------
echo.
echo ============================================================
echo    Installing PyTorch with CUDA support
echo ============================================================
echo.
echo    This will install PyTorch with CUDA 12.1 support.
echo    If you do NOT have NVIDIA GPU, use CPU build instead.
echo.

call :run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if errorlevel 1 goto :fail

REM -------------------------
REM Install Ultralytics + Roboflow + deps
REM -------------------------
echo.
echo 📥 Installing Ultralytics (YOLO)...
call :run pip install ultralytics
if errorlevel 1 goto :fail

echo.
echo 📥 Installing Roboflow...
call :run pip install roboflow
if errorlevel 1 goto :fail

echo.
echo 📥 Installing additional dependencies...
call :run pip install opencv-python matplotlib pandas tqdm
if errorlevel 1 goto :fail

REM -------------------------
REM Verify installation
REM -------------------------
echo.
echo ============================================================
echo    Verifying Installation
echo ============================================================
echo.

echo 🔍 Checking PyTorch...
call :run python -c "import torch; print('   PyTorch:', torch.__version__)"
if errorlevel 1 goto :fail
call :run python -c "import torch; print('   CUDA Available:', torch.cuda.is_available())"
if errorlevel 1 goto :fail
call :run python -c "import torch; print('   CUDA Device:', (torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'))"
if errorlevel 1 goto :fail

echo.
echo 🔍 Checking Ultralytics...
call :run python -c "import ultralytics; print('   Ultralytics:', ultralytics.__version__)"
if errorlevel 1 goto :fail

echo.
echo 🔍 Checking Roboflow...
call :run python -c "import roboflow; print('   Roboflow:', roboflow.__version__)"
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
echo 📝 Log saved at: %LOG%
echo.
pause
exit /b 0


:run
echo.>> "%LOG%"
echo [RUN] %*>> "%LOG%"
%*>> "%LOG%" 2>&1
set "ERR=%errorlevel%"
echo [EXIT] !ERR!>> "%LOG%"
exit /b !ERR!
goto :eof


:fail
echo.
echo ❌ Setup failed. Please review the error above.
echo 📝 Log saved at: %LOG%
echo.
pause
exit /b 1
