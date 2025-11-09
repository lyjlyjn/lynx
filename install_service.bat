@echo off
REM CloudDrive2 Media Streaming Application - Windows Service Installation
REM This script installs the application as a Windows Service using NSSM

echo ============================================================
echo CloudDrive2 Media Streaming - Service Installation
echo ============================================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: This script requires administrator privileges
    echo Please run as Administrator
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please run setup.bat first to configure the application
    pause
    exit /b 1
)

REM Set service name
set SERVICE_NAME=CloudDrive2Streaming

REM Check if service already exists
sc query %SERVICE_NAME% >nul 2>&1
if not errorlevel 1 (
    echo Service %SERVICE_NAME% already exists.
    set /p reinstall="Do you want to reinstall? (y/n): "
    if /i "%reinstall%"=="y" (
        echo Stopping and removing existing service...
        net stop %SERVICE_NAME% 2>nul
        sc delete %SERVICE_NAME%
        timeout /t 2 >nul
    ) else (
        echo Installation cancelled.
        pause
        exit /b 0
    )
)

REM Get current directory
set APP_DIR=%cd%

REM Find Python executable
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    pause
    exit /b 1
)

REM Get Python path
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i

echo.
echo Python found at: %PYTHON_PATH%
echo Application directory: %APP_DIR%
echo.

REM Load port from .env
for /f "tokens=2 delims==" %%a in ('findstr /r "^PORT=" .env') do set PORT=%%a
if "%PORT%"=="" set PORT=8000

REM Check if NSSM is available
where nssm >nul 2>&1
if errorlevel 1 (
    echo.
    echo NSSM (Non-Sucking Service Manager) not found.
    echo.
    echo Option 1: Install NSSM
    echo   Download from: https://nssm.cc/download
    echo   Extract nssm.exe to a directory in your PATH
    echo   Or place nssm.exe in the current directory
    echo.
    echo Option 2: Use sc.exe (native Windows service manager)
    echo   This is more complex but doesn't require external tools
    echo.
    set /p use_sc="Use sc.exe instead of NSSM? (y/n): "
    if /i "%use_sc%"=="y" (
        goto USE_SC
    ) else (
        echo.
        echo Please install NSSM and run this script again.
        pause
        exit /b 1
    )
)

REM Install service using NSSM
echo Installing service using NSSM...
echo.

nssm install %SERVICE_NAME% "%PYTHON_PATH%" -m uvicorn app.main:app --host 0.0.0.0 --port %PORT%
nssm set %SERVICE_NAME% AppDirectory "%APP_DIR%"
nssm set %SERVICE_NAME% DisplayName "CloudDrive2 Media Streaming"
nssm set %SERVICE_NAME% Description "High-performance media streaming server for CloudDrive2 with HTTP Range support"
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START
nssm set %SERVICE_NAME% ObjectName LocalSystem
nssm set %SERVICE_NAME% AppStdout "%APP_DIR%\logs\service.log"
nssm set %SERVICE_NAME% AppStderr "%APP_DIR%\logs\service_error.log"
nssm set %SERVICE_NAME% AppStdoutCreationDisposition 4
nssm set %SERVICE_NAME% AppStderrCreationDisposition 4
nssm set %SERVICE_NAME% AppRotateFiles 1
nssm set %SERVICE_NAME% AppRotateOnline 1
nssm set %SERVICE_NAME% AppRotateBytes 1048576

echo.
echo Service installed successfully!
goto START_SERVICE

:USE_SC
REM Create a wrapper batch file for the service
echo Creating service wrapper...
set WRAPPER=%APP_DIR%\service_wrapper.bat

echo @echo off > "%WRAPPER%"
echo cd /d "%APP_DIR%" >> "%WRAPPER%"
echo "%PYTHON_PATH%" -m uvicorn app.main:app --host 0.0.0.0 --port %PORT% >> "%WRAPPER%"

REM Install service using sc
echo Installing service using sc.exe...
sc create %SERVICE_NAME% binPath= "\"%WRAPPER%\"" start= auto DisplayName= "CloudDrive2 Media Streaming"
sc description %SERVICE_NAME% "High-performance media streaming server for CloudDrive2 with HTTP Range support"

if errorlevel 1 (
    echo ERROR: Failed to create service
    pause
    exit /b 1
)

echo.
echo Service installed successfully!

:START_SERVICE
echo.
set /p start_now="Start the service now? (y/n): "
if /i "%start_now%"=="y" (
    echo Starting service...
    net start %SERVICE_NAME%
    if errorlevel 1 (
        echo ERROR: Failed to start service
        echo Check logs in %APP_DIR%\logs\
        pause
        exit /b 1
    )
    echo Service started successfully!
)

echo.
echo ============================================================
echo Service Installation Complete
echo ============================================================
echo.
echo Service Name: %SERVICE_NAME%
echo Port: %PORT%
echo.
echo Commands:
echo   Start:   net start %SERVICE_NAME%
echo   Stop:    net stop %SERVICE_NAME%
echo   Status:  sc query %SERVICE_NAME%
echo.
echo Access the application at: http://localhost:%PORT%
echo Logs location: %APP_DIR%\logs\
echo.
echo To uninstall the service, run: uninstall_service.bat
echo.
pause
