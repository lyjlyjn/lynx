@echo off
REM CloudDrive2 Media Streaming Application - Stop Script
REM This script stops the running application process

echo ============================================================
echo CloudDrive2 Media Streaming - Stopping Server
echo ============================================================
echo.

REM Find and kill Python processes running uvicorn
echo Looking for running server processes...

tasklist | findstr /i "python.exe" >nul
if errorlevel 1 (
    echo No Python processes found running.
    pause
    exit /b 0
)

echo.
echo Found Python processes:
tasklist | findstr /i "python.exe"
echo.

set /p confirm="Stop all Python processes (including uvicorn servers)? (y/n): "
if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Stopping processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>nul

if errorlevel 1 (
    REM Try broader approach
    echo Attempting to stop all Python processes...
    taskkill /F /IM python.exe
)

echo.
echo Server stopped.
echo.
pause
