@echo off
REM CloudDrive2 Media Streaming Application - Windows Service Uninstallation
REM This script removes the Windows Service

echo ============================================================
echo CloudDrive2 Media Streaming - Service Uninstallation
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

REM Set service name
set SERVICE_NAME=CloudDrive2Streaming

REM Check if service exists
sc query %SERVICE_NAME% >nul 2>&1
if errorlevel 1 (
    echo Service %SERVICE_NAME% is not installed.
    pause
    exit /b 0
)

echo Service %SERVICE_NAME% found.
echo.
set /p confirm="Are you sure you want to uninstall the service? (y/n): "
if /i not "%confirm%"=="y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo Stopping service...
net stop %SERVICE_NAME% 2>nul

echo Removing service...

REM Try NSSM first
where nssm >nul 2>&1
if not errorlevel 1 (
    nssm remove %SERVICE_NAME% confirm
) else (
    REM Use sc.exe
    sc delete %SERVICE_NAME%
)

if errorlevel 1 (
    echo ERROR: Failed to remove service
    pause
    exit /b 1
)

REM Remove wrapper if it exists
if exist service_wrapper.bat (
    echo Removing service wrapper...
    del service_wrapper.bat
)

echo.
echo ============================================================
echo Service Uninstallation Complete
echo ============================================================
echo.
echo Service %SERVICE_NAME% has been removed successfully.
echo.
pause
