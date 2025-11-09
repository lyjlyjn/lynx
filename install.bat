@echo off
REM CloudDrive2 Media Streaming Application - Installation Script
REM This script installs Python dependencies for Windows Server

echo ============================================================
echo CloudDrive2 Media Streaming - Installation
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Installing pip...
    python -m ensurepip --default-pip
    if errorlevel 1 (
        echo ERROR: Failed to install pip
        pause
        exit /b 1
    )
)

echo Pip found:
pip --version
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installation completed successfully!
echo ============================================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env: copy .env.example .env
echo 2. Edit .env and configure your CloudDrive2 mount path
echo 3. Run setup.bat to configure the application
echo 4. Run start.bat to start the server manually
echo 5. Or run install_service.bat to install as a Windows Service
echo.
pause
