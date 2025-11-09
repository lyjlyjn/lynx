# Windows Service Setup Guide

This guide provides detailed instructions for setting up CloudDrive2 Media Streaming as a Windows Service.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [NSSM Installation](#nssm-installation)
4. [Service Configuration](#service-configuration)
5. [Service Management](#service-management)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

## Prerequisites

Before installing as a Windows Service:

1. **Administrator Privileges**: Required for service installation
2. **Application Configuration**: Complete `setup.bat` first
3. **Test Manual Start**: Verify application works with `start.bat`
4. **Python in PATH**: Ensure Python is accessible system-wide

## Installation Methods

### Method 1: Automated Installation (Recommended)

Run the automated installer:

```batch
REM Right-click Command Prompt → "Run as Administrator"
install_service.bat
```

The script will:
- Check prerequisites
- Detect NSSM or use native sc.exe
- Configure service settings
- Install the service
- Optionally start the service

### Method 2: Manual NSSM Installation

If you prefer manual control:

```batch
REM Download and extract NSSM first

REM Install service
nssm install CloudDrive2Streaming "C:\Python312\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000

REM Set working directory
nssm set CloudDrive2Streaming AppDirectory "C:\lynx"

REM Set service description
nssm set CloudDrive2Streaming DisplayName "CloudDrive2 Media Streaming"
nssm set CloudDrive2Streaming Description "High-performance media streaming server for CloudDrive2"

REM Configure startup
nssm set CloudDrive2Streaming Start SERVICE_AUTO_START

REM Setup logging
nssm set CloudDrive2Streaming AppStdout "C:\lynx\logs\service.log"
nssm set CloudDrive2Streaming AppStderr "C:\lynx\logs\service_error.log"

REM Enable log rotation
nssm set CloudDrive2Streaming AppRotateFiles 1
nssm set CloudDrive2Streaming AppRotateOnline 1
nssm set CloudDrive2Streaming AppRotateBytes 1048576

REM Start service
nssm start CloudDrive2Streaming
```

### Method 3: Manual sc.exe Installation

Using Windows native service manager:

```batch
REM Create wrapper script
echo @echo off > service_wrapper.bat
echo cd /d C:\lynx >> service_wrapper.bat
echo C:\Python312\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >> service_wrapper.bat

REM Install service
sc create CloudDrive2Streaming binPath= "C:\lynx\service_wrapper.bat" start= auto DisplayName= "CloudDrive2 Media Streaming"

REM Set description
sc description CloudDrive2Streaming "High-performance media streaming server for CloudDrive2"

REM Start service
sc start CloudDrive2Streaming
```

## NSSM Installation

### What is NSSM?

NSSM (Non-Sucking Service Manager) is a service helper that makes it easy to run Windows services with:
- Automatic restart on failure
- Log file rotation
- Service monitoring
- Easy configuration

### Download and Install NSSM

1. **Download**:
   - Visit [nssm.cc/download](https://nssm.cc/download)
   - Download latest version (e.g., nssm-2.24.zip)

2. **Extract**:
   ```batch
   REM Extract to C:\nssm
   mkdir C:\nssm
   REM Extract nssm.exe from win64 folder to C:\nssm
   ```

3. **Add to PATH** (Optional):
   ```batch
   REM Add to system PATH
   setx /M PATH "%PATH%;C:\nssm"
   ```

4. **Verify**:
   ```batch
   nssm version
   ```

### NSSM GUI Configuration

NSSM also provides a GUI for configuration:

```batch
REM Open GUI installer
nssm install CloudDrive2Streaming

REM Open GUI editor for existing service
nssm edit CloudDrive2Streaming
```

**GUI Tabs**:
- **Application**: Program path and arguments
- **Details**: Service name and description
- **Log on**: Service account
- **Dependencies**: Service dependencies
- **Process**: CPU and memory limits
- **Shutdown**: Shutdown methods
- **Exit actions**: Actions on exit
- **I/O**: Input/output redirection
- **File rotation**: Log rotation settings
- **Environment**: Environment variables

## Service Configuration

### Basic Configuration

Minimal service configuration:

```batch
REM Service name
SET SERVICE_NAME=CloudDrive2Streaming

REM Application path
SET PYTHON_PATH=C:\Python312\python.exe
SET APP_DIR=C:\lynx

REM Port (from .env)
SET PORT=8000

REM Install
nssm install %SERVICE_NAME% "%PYTHON_PATH%" -m uvicorn app.main:app --host 0.0.0.0 --port %PORT%
nssm set %SERVICE_NAME% AppDirectory "%APP_DIR%"
```

### Advanced Configuration

#### Auto-Restart on Failure

```batch
REM Reset failures after 60 seconds
nssm set CloudDrive2Streaming AppThrottle 60000

REM Restart on failure
nssm set CloudDrive2Streaming AppExit Default Restart

REM Restart delay (5 seconds)
nssm set CloudDrive2Streaming AppRestartDelay 5000
```

#### Resource Limits

```batch
REM Set CPU affinity (use cores 0-3)
nssm set CloudDrive2Streaming AppAffinity 0-3

REM Set process priority (NORMAL, ABOVE_NORMAL, HIGH)
nssm set CloudDrive2Streaming AppPriority NORMAL

REM Memory limit (in KB, 2GB = 2097152)
nssm set CloudDrive2Streaming AppNoConsole 1
```

#### Environment Variables

```batch
REM Set environment variables
nssm set CloudDrive2Streaming AppEnvironmentExtra PYTHONUNBUFFERED=1
nssm set CloudDrive2Streaming AppEnvironmentExtra PATH=C:\Python312;C:\ffmpeg\bin;%PATH%
```

#### Log Rotation

```batch
REM Rotate logs when they reach 10MB
nssm set CloudDrive2Streaming AppRotateBytes 10485760

REM Rotate online (while service is running)
nssm set CloudDrive2Streaming AppRotateOnline 1

REM Keep rotated logs
nssm set CloudDrive2Streaming AppRotateFiles 1
```

#### Service Dependencies

If your service depends on others (e.g., Redis):

```batch
REM Add dependency on Redis service
sc config CloudDrive2Streaming depend= Redis
```

## Service Management

### Start Service

```batch
REM Using net command
net start CloudDrive2Streaming

REM Using sc command
sc start CloudDrive2Streaming

REM Using NSSM
nssm start CloudDrive2Streaming
```

### Stop Service

```batch
REM Using net command
net stop CloudDrive2Streaming

REM Using sc command
sc stop CloudDrive2Streaming

REM Using NSSM
nssm stop CloudDrive2Streaming
```

### Restart Service

```batch
REM Using net command
net stop CloudDrive2Streaming && net start CloudDrive2Streaming

REM Using NSSM
nssm restart CloudDrive2Streaming
```

### Query Service Status

```batch
REM Basic status
sc query CloudDrive2Streaming

REM Detailed status
sc queryex CloudDrive2Streaming

REM Using NSSM
nssm status CloudDrive2Streaming
```

### View Service Configuration

```batch
REM Using sc
sc qc CloudDrive2Streaming

REM Using NSSM (all settings)
nssm dump CloudDrive2Streaming
```

### Modify Service

```batch
REM Change port
nssm set CloudDrive2Streaming AppParameters -m uvicorn app.main:app --host 0.0.0.0 --port 8001

REM Change startup type
sc config CloudDrive2Streaming start= auto
REM or start= demand (manual)
REM or start= disabled

REM Change service account
sc config CloudDrive2Streaming obj= "NT AUTHORITY\LocalService"
```

### Uninstall Service

```batch
REM Run uninstall script
uninstall_service.bat

REM Or manually with NSSM
nssm stop CloudDrive2Streaming
nssm remove CloudDrive2Streaming confirm

REM Or with sc
sc stop CloudDrive2Streaming
sc delete CloudDrive2Streaming
```

## Troubleshooting

### Service Won't Start

**Check Event Viewer**:
```batch
REM Open Event Viewer
eventvwr.msc

REM Navigate to: Windows Logs → Application
REM Filter for Source: CloudDrive2Streaming or Service Control Manager
```

**Check Service Logs**:
```batch
type logs\service.log
type logs\service_error.log
```

**Test Manual Start**:
```batch
REM Stop service first
net stop CloudDrive2Streaming

REM Try manual start
start.bat

REM Check for errors
```

**Common Issues**:

1. **Python not found**:
   ```batch
   REM Verify Python path in service
   nssm get CloudDrive2Streaming Application
   
   REM Update if needed
   nssm set CloudDrive2Streaming Application "C:\Python312\python.exe"
   ```

2. **Working directory wrong**:
   ```batch
   REM Check directory
   nssm get CloudDrive2Streaming AppDirectory
   
   REM Fix
   nssm set CloudDrive2Streaming AppDirectory "C:\lynx"
   ```

3. **Port already in use**:
   ```batch
   REM Find process using port
   netstat -ano | findstr :8000
   
   REM Kill process or change port
   taskkill /F /PID <PID>
   ```

4. **Permission denied**:
   ```batch
   REM Run as administrator
   REM Or change service account
   sc config CloudDrive2Streaming obj= LocalSystem
   ```

### Service Keeps Stopping

**Check throttling**:
```batch
REM Increase throttle time (milliseconds)
nssm set CloudDrive2Streaming AppThrottle 60000
```

**Check exit codes**:
```batch
REM View service status
sc query CloudDrive2Streaming

REM Check logs
type logs\service_error.log
```

**Disable auto-restart temporarily**:
```batch
REM Stop auto-restart
nssm set CloudDrive2Streaming AppExit Default Exit
```

### Service Running but Not Accessible

**Check firewall**:
```batch
REM Test locally first
curl http://localhost:8000/api/health

REM Check firewall rule
netsh advfirewall firewall show rule name="CloudDrive2 Streaming"

REM Add rule if missing
netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=8000
```

**Check host binding**:
```batch
REM Should be 0.0.0.0, not 127.0.0.1
nssm get CloudDrive2Streaming AppParameters
```

**Check network connectivity**:
```batch
REM From another machine
ping server-ip
telnet server-ip 8000
```

### High Resource Usage

**Check process stats**:
```batch
REM Memory and CPU
tasklist /FI "IMAGENAME eq python.exe" /V

REM Set limits
nssm set CloudDrive2Streaming AppPriority BELOW_NORMAL
```

**Enable logging verbosity**:
```ini
# In .env temporarily
LOG_LEVEL=DEBUG
```

Then check logs for issues.

## Advanced Configuration

### Multiple Instances

Run multiple instances on different ports:

```batch
REM Instance 1 on port 8000
nssm install CloudDrive2Streaming8000 "C:\Python312\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
nssm set CloudDrive2Streaming8000 AppDirectory "C:\lynx"

REM Instance 2 on port 8001  
nssm install CloudDrive2Streaming8001 "C:\Python312\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8001
nssm set CloudDrive2Streaming8001 AppDirectory "C:\lynx"
nssm set CloudDrive2Streaming8001 AppEnvironmentExtra PORT=8001
```

### Load Balancing

Use nginx or IIS as load balancer:

**nginx config**:
```nginx
upstream clouddrive_backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://clouddrive_backend;
    }
}
```

### Service Account

Run as specific user:

```batch
REM Create service account
net user clouddriveuser SecurePassword123! /add
net localgroup Users clouddriveuser /add

REM Grant folder permissions
icacls "C:\lynx" /grant clouddriveuser:(OI)(CI)F /T

REM Configure service
sc config CloudDrive2Streaming obj= ".\clouddriveuser" password= "SecurePassword123!"

REM Or with NSSM GUI
nssm edit CloudDrive2Streaming
REM Go to "Log on" tab
```

### Monitoring and Alerts

**PowerShell monitoring script**:

```powershell
# monitor_service.ps1
$serviceName = "CloudDrive2Streaming"

while ($true) {
    $service = Get-Service -Name $serviceName
    
    if ($service.Status -ne "Running") {
        # Send alert (email, log, etc.)
        Write-Host "WARNING: Service $serviceName is not running!"
        
        # Try to restart
        Start-Service -Name $serviceName
    }
    
    Start-Sleep -Seconds 60
}
```

Run monitoring as another service:
```batch
nssm install CloudDrive2StreamingMonitor powershell.exe -ExecutionPolicy Bypass -File "C:\lynx\monitor_service.ps1"
nssm start CloudDrive2StreamingMonitor
```

### Scheduled Tasks Integration

Create scheduled task for periodic checks:

```batch
REM Create task to check service every 5 minutes
schtasks /create /tn "Check CloudDrive2 Streaming" /tr "powershell -Command \"if ((Get-Service CloudDrive2Streaming).Status -ne 'Running') { Start-Service CloudDrive2Streaming }\"" /sc minute /mo 5 /ru SYSTEM
```

## Best Practices

1. **Test Before Service**: Always test with `start.bat` before installing service
2. **Use NSSM**: Easier management and better logging than native sc.exe
3. **Enable Logging**: Configure log rotation to prevent disk space issues
4. **Set Auto-Restart**: Configure service to restart on failure
5. **Monitor Logs**: Regularly check service logs for errors
6. **Document Changes**: Keep track of configuration changes
7. **Backup Config**: Backup .env and service configuration
8. **Test Recovery**: Test service restart and recovery procedures
9. **Use Monitoring**: Implement monitoring and alerting
10. **Update Regularly**: Keep application and dependencies updated

## References

- NSSM Documentation: [nssm.cc](https://nssm.cc/)
- Windows Service Manager: `sc.exe` documentation
- Event Viewer: `eventvwr.msc`
- Service Management: `services.msc`
- Task Scheduler: `taskschd.msc`

## Support

For issues with Windows Service setup:
1. Check service logs in `logs\service_error.log`
2. Review Event Viewer (Windows Logs → Application)
3. Test manual start with `start.bat`
4. Consult WINDOWS_README.md troubleshooting section
5. Report issues on GitHub with service configuration details
