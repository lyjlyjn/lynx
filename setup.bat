@echo off
REM CloudDrive2 Media Streaming Application - Setup Script
REM This script helps configure the application for Windows Server

echo ============================================================
echo CloudDrive2 Media Streaming - Setup
echo ============================================================
echo.

REM Check if .env exists
if exist .env (
    echo Configuration file .env already exists.
    set /p overwrite="Do you want to reconfigure? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo Setup cancelled.
        pause
        exit /b 0
    )
)

REM Copy example config if .env doesn't exist
if not exist .env (
    if exist .env.example (
        echo Creating .env from .env.example...
        copy .env.example .env
    ) else (
        echo ERROR: .env.example not found
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo Configuration Setup
echo ============================================================
echo.

REM Get CloudDrive2 mount path
set /p mount_path="Enter CloudDrive2 mount path (e.g., C:\CloudDrive2): "
if "%mount_path%"=="" (
    set mount_path=C:\CloudDrive2
    echo Using default: C:\CloudDrive2
)

REM Create mount directory if it doesn't exist
if not exist "%mount_path%" (
    echo Mount path does not exist. Creating directory...
    mkdir "%mount_path%" 2>nul
)

REM Get port number
set /p port="Enter port number (default 8000): "
if "%port%"=="" set port=8000

REM Get authentication settings
set /p enable_auth="Enable authentication? (y/n, default n): "
if /i "%enable_auth%"=="y" (
    set /p username="Enter username (default admin): "
    if "%username%"=="" set username=admin
    
    set /p password="Enter password: "
    if "%password%"=="" (
        echo WARNING: Empty password not recommended
        set password=change_this_password
    )
) else (
    set username=
    set password=
)

echo.
echo Updating .env file...

REM Update .env file (basic replacement)
powershell -Command "(Get-Content .env) -replace 'CLOUDDRIVE_MOUNT_PATH=.*', 'CLOUDDRIVE_MOUNT_PATH=%mount_path%' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace 'PORT=.*', 'PORT=%port%' | Set-Content .env"

if not "%username%"=="" (
    powershell -Command "(Get-Content .env) -replace '# AUTH_USERNAME=.*', 'AUTH_USERNAME=%username%' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace '# AUTH_PASSWORD=.*', 'AUTH_PASSWORD=%password%' | Set-Content .env"
)

REM Create logs directory
if not exist logs mkdir logs

echo.
echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo Configuration:
echo   Mount Path: %mount_path%
echo   Port: %port%
if not "%username%"=="" (
    echo   Authentication: Enabled (User: %username%)
) else (
    echo   Authentication: Disabled
)
echo.
echo Next steps:
echo 1. Verify .env configuration
echo 2. Run start.bat to start the server manually
echo 3. Or run install_service.bat to install as a Windows Service
echo.
echo To test the server, run: start.bat
echo Then open: http://localhost:%port%
echo.
pause
