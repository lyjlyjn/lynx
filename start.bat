@echo off
REM CloudDrive2 Media Streaming Application - Start Script
REM This script starts the application manually (not as a service)

echo ============================================================
echo CloudDrive2 Media Streaming - Starting Server
echo ============================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please run setup.bat first to configure the application
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Load port from .env (basic extraction)
for /f "tokens=2 delims==" %%a in ('findstr /r "^PORT=" .env') do set PORT=%%a
if "%PORT%"=="" set PORT=8000

echo Starting server on port %PORT%...
echo.
echo Press Ctrl+C to stop the server
echo.
echo Web Interface: http://localhost:%PORT%
echo API Docs: http://localhost:%PORT%/docs
echo.

REM Start the application
python -m uvicorn app.main:app --host 0.0.0.0 --port %PORT% --reload

REM If we get here, the server stopped
echo.
echo Server stopped.
pause
