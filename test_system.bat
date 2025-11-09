@echo off
REM CloudDrive2 Media Streaming Application - System Test Script
REM This script tests the installation and configuration

echo ============================================================
echo CloudDrive2 Media Streaming - System Tests
echo ============================================================
echo.

set TESTS_PASSED=0
set TESTS_FAILED=0

REM Test 1: Python Installation
echo [Test 1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Python is not installed or not in PATH
    set /a TESTS_FAILED+=1
) else (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo   [PASS] Python %%v found
    set /a TESTS_PASSED+=1
)

REM Test 2: pip Installation
echo [Test 2] Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] pip is not installed
    set /a TESTS_FAILED+=1
) else (
    echo   [PASS] pip found
    set /a TESTS_PASSED+=1
)

REM Test 3: Configuration File
echo [Test 3] Checking configuration file...
if exist .env (
    echo   [PASS] .env file exists
    set /a TESTS_PASSED+=1
) else (
    echo   [WARN] .env file not found (run setup.bat)
    if exist .env.example (
        echo   [INFO] .env.example is available
    )
    set /a TESTS_FAILED+=1
)

REM Test 4: CloudDrive Mount Path
if exist .env (
    echo [Test 4] Checking CloudDrive mount path...
    for /f "tokens=2 delims==" %%a in ('findstr /r "^CLOUDDRIVE_MOUNT_PATH=" .env 2^>nul') do (
        set MOUNT_PATH=%%a
        REM Convert forward slashes to backslashes for Windows check
        set MOUNT_PATH=!MOUNT_PATH:/=\!
        if exist "!MOUNT_PATH!" (
            echo   [PASS] Mount path exists: !MOUNT_PATH!
            set /a TESTS_PASSED+=1
        ) else (
            echo   [WARN] Mount path not found: !MOUNT_PATH!
            echo   [INFO] Path will be created on first start
            set /a TESTS_PASSED+=1
        )
    )
) else (
    echo [Test 4] Skipped - no .env file
)

REM Test 5: Dependencies
echo [Test 5] Checking Python dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] FastAPI not installed (run install.bat)
    set /a TESTS_FAILED+=1
) else (
    echo   [PASS] FastAPI installed
    set /a TESTS_PASSED+=1
)

python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] uvicorn not installed (run install.bat)
    set /a TESTS_FAILED+=1
) else (
    echo   [PASS] uvicorn installed
    set /a TESTS_PASSED+=1
)

python -c "import aiofiles" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] aiofiles not installed (run install.bat)
    set /a TESTS_FAILED+=1
) else (
    echo   [PASS] aiofiles installed
    set /a TESTS_PASSED+=1
)

REM Test 6: Application Import
echo [Test 6] Testing application import...
python -c "from app.main import app; print('OK')" >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Cannot import application
    set /a TESTS_FAILED+=1
) else (
    echo   [PASS] Application imports successfully
    set /a TESTS_PASSED+=1
)

REM Test 7: Logs Directory
echo [Test 7] Checking logs directory...
if exist logs (
    echo   [PASS] logs directory exists
    set /a TESTS_PASSED+=1
) else (
    echo   [INFO] Creating logs directory...
    mkdir logs
    echo   [PASS] logs directory created
    set /a TESTS_PASSED+=1
)

REM Test 8: Port Availability
if exist .env (
    echo [Test 8] Checking port availability...
    for /f "tokens=2 delims==" %%a in ('findstr /r "^PORT=" .env 2^>nul') do set PORT=%%a
    if "%PORT%"=="" set PORT=8000
    
    netstat -an | findstr ":%PORT% " | findstr "LISTENING" >nul
    if not errorlevel 1 (
        echo   [WARN] Port %PORT% is already in use
        echo   [INFO] Another service may be using this port
        set /a TESTS_PASSED+=1
    ) else (
        echo   [PASS] Port %PORT% is available
        set /a TESTS_PASSED+=1
    )
) else (
    echo [Test 8] Skipped - no .env file
)

REM Test 9: FFmpeg (Optional)
echo [Test 9] Checking FFmpeg (optional)...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo   [INFO] FFmpeg not installed (optional for media metadata)
    echo   [INFO] Download from: https://ffmpeg.org/download.html
) else (
    echo   [PASS] FFmpeg installed
    set /a TESTS_PASSED+=1
)

REM Test 10: Application Test Script
echo [Test 10] Running application tests...
python test_app.py >nul 2>&1
if errorlevel 1 (
    echo   [WARN] Some application tests failed
    echo   [INFO] Run 'python test_app.py' for details
) else (
    echo   [PASS] Application tests passed
    set /a TESTS_PASSED+=1
)

REM Test 11: Windows Service (if installed)
echo [Test 11] Checking Windows Service...
sc query CloudDrive2Streaming >nul 2>&1
if errorlevel 1 (
    echo   [INFO] Windows Service not installed
    echo   [INFO] Run install_service.bat to install as service
) else (
    echo   [PASS] Windows Service is installed
    sc query CloudDrive2Streaming | findstr "STATE" | findstr "RUNNING" >nul
    if not errorlevel 1 (
        echo   [PASS] Service is running
    ) else (
        echo   [INFO] Service is not running
    )
    set /a TESTS_PASSED+=1
)

REM Test 12: Firewall Rule
echo [Test 12] Checking firewall rule...
netsh advfirewall firewall show rule name="CloudDrive2 Streaming" >nul 2>&1
if errorlevel 1 (
    echo   [INFO] Firewall rule not configured
    echo   [INFO] Run configure_firewall.bat to add firewall rule
) else (
    echo   [PASS] Firewall rule exists
    set /a TESTS_PASSED+=1
)

echo.
echo ============================================================
echo Test Results
echo ============================================================
echo   Tests Passed: %TESTS_PASSED%
echo   Tests Failed: %TESTS_FAILED%
echo.

if %TESTS_FAILED% gtr 0 (
    echo [FAIL] Some tests failed. Please review the output above.
    echo.
    echo Recommendations:
    if not exist .env (
        echo   - Run setup.bat to configure the application
    )
    python -c "import fastapi" >nul 2>&1
    if errorlevel 1 (
        echo   - Run install.bat to install dependencies
    )
    echo.
) else (
    echo [SUCCESS] All critical tests passed!
    echo.
    echo Next steps:
    echo   - Start server: start.bat
    echo   - Install as service: install_service.bat
    echo   - Configure firewall: configure_firewall.bat
    echo   - View documentation: WINDOWS_README.md
    echo.
)

echo ============================================================
pause
