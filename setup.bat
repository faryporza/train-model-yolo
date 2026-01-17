@echo off
chcp 65001 >nul
echo ============================================================
echo        YOLO Training Setup - Windows
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist venv (
    echo    Virtual environment already exists.
    set /p RECREATE="   Recreate? (y/N): "
    if /i "%RECREATE%"=="y" (
        rmdir /s /q venv
        python -m venv venv
    )
) else (
    python -m venv venv
)

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install PyTorch with CUDA
echo.
echo ============================================================
echo    Installing PyTorch with CUDA support
echo ============================================================
echo.
echo    This will install PyTorch with CUDA 12.1 support.
echo    If you have a different CUDA version, please modify this script.
echo.

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

REM Install Ultralytics (YOLOv11)
echo.
echo 📥 Installing Ultralytics (YOLO)...
pip install ultralytics

REM Install Roboflow
echo.
echo 📥 Installing Roboflow...
pip install roboflow

REM Install additional dependencies
echo.
echo 📥 Installing additional dependencies...
pip install opencv-python
pip install matplotlib
pip install pandas
pip install tqdm

REM Verify installation
echo.
echo ============================================================
echo    Verifying Installation
echo ============================================================
echo.

echo 🔍 Checking PyTorch...
python -c "import torch; print(f'   PyTorch: {torch.__version__}')"
python -c "import torch; print(f'   CUDA Available: {torch.cuda.is_available()}')"
python -c "import torch; print(f'   CUDA Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

echo.
echo 🔍 Checking Ultralytics...
python -c "import ultralytics; print(f'   Ultralytics: {ultralytics.__version__}')"

echo.
echo 🔍 Checking Roboflow...
python -c "import roboflow; print(f'   Roboflow: {roboflow.__version__}')"

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
