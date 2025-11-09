@echo off
REM CloudDrive2 Media Streaming Application - Windows Firewall Configuration
REM This script configures Windows Firewall rules for the application

echo ============================================================
echo CloudDrive2 Media Streaming - Firewall Configuration
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

REM Load port from .env or use default
set PORT=8000
if exist .env (
    for /f "tokens=2 delims==" %%a in ('findstr /r "^PORT=" .env 2^>nul') do set PORT=%%a
)

echo Current configuration:
echo   Port: %PORT%
echo   Rule Name: CloudDrive2 Streaming
echo.

REM Check if rule already exists
netsh advfirewall firewall show rule name="CloudDrive2 Streaming" >nul 2>&1
if not errorlevel 1 (
    echo Firewall rule already exists.
    set /p update="Do you want to update it? (y/n): "
    if /i not "%update%"=="y" (
        echo Configuration cancelled.
        pause
        exit /b 0
    )
    echo Removing existing rule...
    netsh advfirewall firewall delete rule name="CloudDrive2 Streaming"
)

echo.
echo Select firewall rule type:
echo   1. Allow from any IP (least secure, for testing)
echo   2. Allow from local network only (192.168.x.x)
echo   3. Allow from specific IP address
echo   4. Allow from specific subnet
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo Creating rule to allow from any IP...
    netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=%PORT%
) else if "%choice%"=="2" (
    echo Creating rule to allow from local network...
    netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=%PORT% remoteip=192.168.0.0/16,10.0.0.0/8,172.16.0.0/12
) else if "%choice%"=="3" (
    set /p remote_ip="Enter IP address to allow: "
    echo Creating rule to allow from %remote_ip%...
    netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=%PORT% remoteip=%remote_ip%
) else if "%choice%"=="4" (
    set /p subnet="Enter subnet (e.g., 192.168.1.0/24): "
    echo Creating rule to allow from %subnet%...
    netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=%PORT% remoteip=%subnet%
) else (
    echo Invalid choice.
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create firewall rule
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Firewall Configuration Complete
echo ============================================================
echo.
echo Rule Name: CloudDrive2 Streaming
echo Port: %PORT%
echo.
echo To verify the rule:
echo   netsh advfirewall firewall show rule name="CloudDrive2 Streaming"
echo.
echo To remove the rule:
echo   netsh advfirewall firewall delete rule name="CloudDrive2 Streaming"
echo.
echo To test connectivity from another machine:
echo   telnet your-server-ip %PORT%
echo   or
echo   Test-NetConnection your-server-ip -Port %PORT%  (PowerShell)
echo.
pause
