# CloudDrive2 Media Streaming Application - Windows Server Guide

A production-ready Python streaming media application optimized for Windows Server with CloudDrive2 integration, HTTP Range request support, and Windows Service management.

## Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Windows Service Setup](#windows-service-setup)
7. [Windows Firewall Configuration](#windows-firewall-configuration)
8. [Discuz Integration](#discuz-integration)
9. [API Documentation](#api-documentation)
10. [Troubleshooting](#troubleshooting)
11. [Performance Optimization](#performance-optimization)
12. [Security Best Practices](#security-best-practices)

## Features

### Core Features
- ✅ **HTTP Range Request Support** - Resumable downloads and media player seeking
- ✅ **Large File Streaming** - No disconnections for files of any size
- ✅ **CloudDrive2 Integration** - Direct access to mounted Google Drive
- ✅ **Windows Service Support** - Run as background service on Windows Server
- ✅ **Async I/O** - High-performance concurrent request handling
- ✅ **RESTful API** - Comprehensive API with file management
- ✅ **Web Interface** - Browser-based file browsing and playback
- ✅ **Authentication** - HTTP Basic and Bearer token authentication
- ✅ **Media Metadata** - Video/audio metadata extraction
- ✅ **Caching** - Intelligent metadata caching for performance
- ✅ **Multiple File Types** - Video, audio, document support

### Windows-Specific Features
- ✅ Windows path separator handling (C:\, D:\, etc.)
- ✅ Windows Service wrapper (NSSM or native sc.exe)
- ✅ Batch scripts for easy setup and management
- ✅ Windows Firewall configuration helpers
- ✅ Port configuration for network services
- ✅ Automatic log rotation
- ✅ Service monitoring and restart

## System Requirements

### Required
- **Operating System**: Windows Server 2012 R2 or later (Windows 10/11 also supported)
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB, recommended 4GB+
- **Disk Space**: 500MB for application + space for CloudDrive2 cache
- **Network**: Open port for HTTP server (default: 8000)

### Optional
- **FFmpeg**: For media metadata extraction (video duration, codec info, etc.)
- **NSSM**: For easier Windows Service management
- **Redis**: For distributed caching (multi-server deployments)
- **CloudDrive2**: For Google Drive mounting

## Quick Start

### 1. Installation (5 minutes)

```batch
REM Clone or download the repository
cd C:\
git clone https://github.com/lyjlyjn/lynx.git
cd lynx

REM Install dependencies
install.bat

REM Configure application
setup.bat

REM Start server manually (for testing)
start.bat
```

### 2. Access Web Interface

Open browser: `http://localhost:8000`

### 3. API Documentation

View interactive API docs: `http://localhost:8000/docs`

## Installation

### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
   ```batch
   python --version
   pip --version
   ```

### Step 2: Download Application

```batch
REM Option A: Using Git
cd C:\
git clone https://github.com/lyjlyjn/lynx.git
cd lynx

REM Option B: Download ZIP
REM Download from GitHub and extract to C:\lynx
```

### Step 3: Install Dependencies

```batch
REM Run the installation script
install.bat
```

Or manually:
```batch
pip install -r requirements.txt
```

### Step 4: Install FFmpeg (Optional but Recommended)

1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH
4. Verify: `ffmpeg -version`

## Configuration

### Automatic Configuration

Run the setup wizard:
```batch
setup.bat
```

This will:
1. Create `.env` configuration file
2. Set CloudDrive2 mount path
3. Configure port number
4. Setup authentication (optional)
5. Create necessary directories

### Manual Configuration

1. Copy example configuration:
   ```batch
   copy .env.example .env
   copy config.ini.example config.ini
   ```

2. Edit `.env` with your settings:
   ```ini
   # CloudDrive2 mount path (Windows style)
   CLOUDDRIVE_MOUNT_PATH=C:/CloudDrive2
   
   # Or with escaped backslashes
   CLOUDDRIVE_MOUNT_PATH=C:\\CloudDrive2
   
   # Server port
   PORT=8000
   
   # Authentication (recommended)
   AUTH_USERNAME=admin
   AUTH_PASSWORD=YourSecurePassword
   
   # Security key (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
   SECRET_KEY=your-random-secret-key-here
   ```

### Configuration Options

See `config.ini.example` for all available options including:
- Application settings
- CloudDrive2 paths
- Security & authentication
- Performance tuning
- Caching configuration
- Logging settings
- CORS settings

## Windows Service Setup

### Option 1: Using NSSM (Recommended)

NSSM (Non-Sucking Service Manager) provides easy service management with logging and monitoring.

#### Install NSSM

1. Download NSSM from [nssm.cc](https://nssm.cc/download)
2. Extract `nssm.exe` to a directory in PATH or to the application directory
3. Or place in `C:\Windows\System32\`

#### Install Service

```batch
REM Run as Administrator
install_service.bat
```

The script will:
- Install the service with NSSM
- Configure automatic startup
- Setup log rotation
- Configure service recovery

#### Service Management

```batch
REM Start service
net start CloudDrive2Streaming

REM Stop service
net stop CloudDrive2Streaming

REM Check status
sc query CloudDrive2Streaming

REM View logs
type logs\service.log
type logs\service_error.log
```

### Option 2: Using Native sc.exe

If NSSM is not available, the installation script will use Windows native service manager.

```batch
REM Run as Administrator
install_service.bat

REM Choose "Use sc.exe" when prompted
```

### Service Configuration

Service settings:
- **Name**: CloudDrive2Streaming
- **Display Name**: CloudDrive2 Media Streaming
- **Startup Type**: Automatic
- **Log Location**: `logs\service.log`

### Uninstall Service

```batch
REM Run as Administrator
uninstall_service.bat
```

## Windows Firewall Configuration

### Automatic Configuration

The application needs an inbound rule for the configured port. Add the rule:

```batch
REM Run as Administrator (replace 8000 with your port)
netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=8000

REM For a specific program
netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow program="C:\Python312\python.exe" enable=yes
```

### GUI Configuration

1. Open **Windows Defender Firewall with Advanced Security**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → Click **Next**
4. Select **TCP** and enter port number (e.g., 8000) → Click **Next**
5. Select **Allow the connection** → Click **Next**
6. Select network types (Domain, Private, Public) → Click **Next**
7. Enter name: "CloudDrive2 Streaming" → Click **Finish**

### Verify Firewall Rule

```batch
netsh advfirewall firewall show rule name="CloudDrive2 Streaming"
```

### Remove Firewall Rule

```batch
netsh advfirewall firewall delete rule name="CloudDrive2 Streaming"
```

## Discuz Integration

### Overview

This application can serve as a media streaming backend for Discuz forums, replacing problematic Nginx configurations that disconnect on large files.

### Integration Steps

#### 1. Configure Application

Ensure the application is accessible from your Discuz server:

```ini
# In .env
PORT=8000
AUTH_USERNAME=discuz_user
AUTH_PASSWORD=secure_password
CORS_ORIGINS=http://your-discuz-domain.com
```

#### 2. Install as Windows Service

```batch
install_service.bat
```

#### 3. Configure Network Access

Ensure Discuz server can reach the streaming server:
- Same server: Use `localhost:8000`
- Different server: Use `server-ip:8000`
- Configure firewall rules appropriately

### Discuz Template Integration

#### Example: Attachment Download Link

```php
<?php
// Discuz attachment streaming
$streaming_server = 'http://your-streaming-server:8000';
$file_path = urlencode($attachment_path);

// Basic authentication
$username = 'discuz_user';
$password = 'secure_password';

$stream_url = $streaming_server . '/api/stream/' . $file_path;

// With authentication header
$context = stream_context_create([
    'http' => [
        'header' => "Authorization: Basic " . base64_encode("$username:$password")
    ]
]);

// Output download link
echo '<a href="' . $stream_url . '" download>Download File</a>';
?>
```

#### Example: Video Player Integration

```php
<?php
$streaming_server = 'http://your-streaming-server:8000';
$video_path = urlencode($video_file_path);
$stream_url = $streaming_server . '/api/stream/' . $video_path;
?>

<video width="100%" height="480" controls>
    <source src="<?php echo $stream_url; ?>" type="video/mp4">
    Your browser does not support the video tag.
</video>
```

#### Example: cURL-based Proxy

```php
<?php
// Proxy through Discuz for authentication
$streaming_server = 'http://localhost:8000';
$file_path = $_GET['file'];
$stream_url = $streaming_server . '/api/stream/' . urlencode($file_path);

// Get authentication token
$token_url = $streaming_server . '/api/auth/token';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $token_url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($ch, CURLOPT_USERPWD, "discuz_user:secure_password");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$response = curl_exec($ch);
curl_close($ch);

$token_data = json_decode($response, true);
$token = $token_data['access_token'];

// Stream file with token
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . basename($file_path) . '"');

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $stream_url);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Authorization: Bearer " . $token]);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 0);
curl_exec($ch);
curl_close($ch);
?>
```

### Testing Discuz Integration

```batch
REM Test file listing
curl -u username:password http://localhost:8000/api/files/list

REM Test file streaming
curl -u username:password http://localhost:8000/api/stream/path/to/file.mp4 -o test.mp4

REM Test range request
curl -u username:password -H "Range: bytes=0-1000000" http://localhost:8000/api/stream/path/to/file.mp4 -o test_chunk.mp4
```

## API Documentation

### Authentication

#### Get Access Token

**Endpoint**: `POST /api/auth/token`

**Authentication**: HTTP Basic Auth

```bash
curl -X POST -u username:password http://localhost:8000/api/auth/token
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Use Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/files/list
```

### File Management

#### List Directory

**Endpoint**: `GET /api/files/list/{dir_path}`

**Parameters**:
- `dir_path` (optional): Relative directory path

```bash
REM List root
curl http://localhost:8000/api/files/list

REM List subdirectory
curl http://localhost:8000/api/files/list/Videos
```

**Response**:
```json
{
  "name": "Videos",
  "path": "/Videos",
  "files": [
    {
      "name": "movie.mp4",
      "path": "/Videos/movie.mp4",
      "size": 1073741824,
      "type": "video",
      "extension": "mp4",
      "modified": "2024-01-01T12:00:00",
      "mime_type": "video/mp4",
      "is_streamable": true
    }
  ],
  "subdirectories": ["Action", "Comedy"],
  "total_files": 1,
  "total_size": 1073741824
}
```

#### Get File Info

**Endpoint**: `GET /api/files/info/{file_path}`

```bash
curl http://localhost:8000/api/files/info/Videos/movie.mp4
```

### Streaming

#### Stream File

**Endpoint**: `GET /api/stream/{file_path}`

**Headers**:
- `Range` (optional): Byte range (e.g., `bytes=0-1000000`)

```bash
REM Stream entire file
curl http://localhost:8000/api/stream/Videos/movie.mp4 -o movie.mp4

REM Stream with range
curl -H "Range: bytes=0-1000000" http://localhost:8000/api/stream/Videos/movie.mp4 -o chunk.mp4

REM Resume download
curl -C - http://localhost:8000/api/stream/Videos/movie.mp4 -o movie.mp4
```

**Response Headers**:
```
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1000000/1073741824
Accept-Ranges: bytes
Content-Length: 1000001
Content-Type: video/mp4
```

#### Get Stream Info

**Endpoint**: `GET /api/stream/{file_path}/info`

```bash
curl http://localhost:8000/api/stream/Videos/movie.mp4/info
```

**Response**:
```json
{
  "file_path": "/Videos/movie.mp4",
  "file_size": 1073741824,
  "content_type": "video/mp4",
  "supports_range": true,
  "chunk_size": 1048576
}
```

#### Get Media Metadata

**Endpoint**: `GET /api/stream/{file_path}/metadata`

```bash
curl http://localhost:8000/api/stream/Videos/movie.mp4/metadata
```

**Response**:
```json
{
  "duration": 7200.0,
  "bit_rate": 5000000,
  "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
  "format_long_name": "QuickTime / MOV",
  "width": 1920,
  "height": 1080,
  "codec_name": "h264",
  "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
  "fps": 24.0
}
```

### System

#### Health Check

**Endpoint**: `GET /api/health`

```bash
curl http://localhost:8000/api/health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### System Statistics

**Endpoint**: `GET /api/stats`

```bash
curl http://localhost:8000/api/stats
```

**Response**:
```json
{
  "uptime": 3600,
  "requests_total": 1500,
  "requests_active": 5,
  "cache_size": 250,
  "cache_hits": 800,
  "cache_misses": 200
}
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for:
- Complete API reference
- Interactive testing
- Request/response examples
- Schema documentation

## Troubleshooting

### Common Issues

#### 1. Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH:
  1. Right-click **This PC** → **Properties**
  2. Click **Advanced system settings**
  3. Click **Environment Variables**
  4. Edit **Path** in System Variables
  5. Add Python directory (e.g., `C:\Python312\`)

#### 2. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```batch
REM Find process using port 8000
netstat -ano | findstr :8000

REM Kill the process (replace PID)
taskkill /F /PID <PID>

REM Or change port in .env
PORT=8001
```

#### 3. CloudDrive2 Mount Path Not Found

**Error**: `CloudDrive mount path does not exist`

**Solution**:
- Verify CloudDrive2 is running
- Check mount path in CloudDrive2 settings
- Update `CLOUDDRIVE_MOUNT_PATH` in `.env`
- Ensure path uses forward slashes: `C:/CloudDrive2`

#### 4. Permission Denied

**Error**: `Permission denied` or `Access denied`

**Solution**:
- Run command prompt as Administrator
- Check file/folder permissions
- Ensure CloudDrive2 mount is accessible
- Check Windows Firewall isn't blocking access

#### 5. Service Won't Start

**Error**: Service fails to start

**Solution**:
```batch
REM Check service status
sc query CloudDrive2Streaming

REM View service logs
type logs\service_error.log

REM Check event viewer
eventvwr.msc
REM Navigate to: Windows Logs → Application

REM Verify Python path
where python

REM Test manual start
start.bat
```

#### 6. Cannot Access from Network

**Error**: Connection refused from other machines

**Solution**:
- Check `HOST=0.0.0.0` in `.env` (not `127.0.0.1`)
- Configure Windows Firewall (see [Firewall Configuration](#windows-firewall-configuration))
- Check network connectivity: `ping server-ip`
- Verify port is open: `telnet server-ip 8000`

#### 7. Media Metadata Not Available

**Error**: Metadata endpoint returns empty or error

**Solution**:
- Install FFmpeg (see [Installation](#step-4-install-ffmpeg-optional-but-recommended))
- Verify FFmpeg in PATH: `ffmpeg -version`
- Check file is valid media file
- Review logs for FFmpeg errors

### Log Files

Check log files for detailed error information:

```batch
REM Application log
type logs\app.log

REM Service log (when running as service)
type logs\service.log
type logs\service_error.log

REM View last 50 lines
powershell Get-Content logs\app.log -Tail 50 -Wait
```

### Debug Mode

Enable debug mode for verbose logging:

```ini
# In .env
DEBUG=True
LOG_LEVEL=DEBUG
```

Then restart the application.

### Testing Commands

```batch
REM Test application loading
python test_app.py

REM Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/files/list

REM Test with authentication
curl -u admin:password http://localhost:8000/api/files/list

REM Check server is listening
netstat -ano | findstr :8000
```

## Performance Optimization

### Tuning for Windows Server

#### 1. Worker Processes

Adjust based on CPU cores:

```ini
# In .env
MAX_WORKERS=4  # Set to number of CPU cores
```

For production with 8 cores:
```batch
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 8
```

#### 2. Chunk Size

Optimize for your use case:

```ini
# Smaller chunks for many concurrent users
CHUNK_SIZE=262144  # 256KB

# Larger chunks for fewer users with high bandwidth
CHUNK_SIZE=2097152  # 2MB
```

#### 3. Caching

Enable caching for better performance:

```ini
CACHE_ENABLED=True
CACHE_TTL=600  # 10 minutes
CACHE_MAX_SIZE=5000  # 5000 items
```

For distributed caching with Redis:

```ini
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

#### 4. Keep-Alive Timeout

Adjust for your network:

```ini
# Longer timeout for slow networks
KEEP_ALIVE_TIMEOUT=120

# Shorter timeout for fast networks
KEEP_ALIVE_TIMEOUT=30
```

#### 5. Operating System Tuning

**Increase TCP connections**:
```batch
REM Run as Administrator
netsh int ipv4 set dynamicport tcp start=10000 num=55535
```

**Optimize network buffers**:
```batch
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=enabled
```

### Monitoring Performance

**Resource usage**:
```batch
REM CPU and memory
tasklist /FI "IMAGENAME eq python.exe" /V

REM Network connections
netstat -an | findstr :8000
```

**Performance Monitor**:
1. Run `perfmon.msc`
2. Add counters:
   - Processor → % Processor Time
   - Network Interface → Bytes Total/sec
   - Process → Private Bytes (python.exe)

### Load Testing

Use Apache Bench or similar tools:

```batch
REM Install Apache Bench
REM Download from: https://www.apachelounge.com/download/

REM Test concurrent requests
ab -n 1000 -c 10 http://localhost:8000/api/files/list

REM Test with authentication
ab -n 1000 -c 10 -A username:password http://localhost:8000/api/files/list
```

## Security Best Practices

### 1. Strong Authentication

Always enable and use strong credentials:

```ini
# Generate strong password
# Use password manager or: python -c "import secrets; print(secrets.token_urlsafe(24))"
AUTH_USERNAME=admin
AUTH_PASSWORD=your-very-strong-password-here
```

### 2. Secret Key

Generate a strong secret key:

```batch
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the output in `.env`:
```ini
SECRET_KEY=your-generated-secret-key
```

### 3. HTTPS/SSL

Deploy behind IIS or nginx with SSL:

**Using IIS**:
1. Install IIS
2. Install URL Rewrite module
3. Install ARR (Application Request Routing)
4. Configure reverse proxy to `http://localhost:8000`
5. Add SSL certificate

**Using nginx**:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Important for Range requests
        proxy_http_version 1.1;
        proxy_set_header Range $http_range;
        proxy_set_header If-Range $http_if_range;
    }
}
```

### 4. CORS Configuration

Restrict to specific domains:

```ini
# Only allow specific origins
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 5. Read-Only Access

Mount CloudDrive2 as read-only to prevent modifications:
- Configure in CloudDrive2 settings
- Or set NTFS permissions to Read-only

### 6. Network Isolation

Use Windows Firewall to restrict access:

```batch
REM Only allow from specific IP
netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=8000 remoteip=192.168.1.100

REM Allow from subnet
netsh advfirewall firewall add rule name="CloudDrive2 Streaming" dir=in action=allow protocol=TCP localport=8000 remoteip=192.168.1.0/24
```

### 7. Regular Updates

Keep dependencies up to date:

```batch
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

### 8. Monitoring and Logging

Monitor logs for suspicious activity:

```batch
REM Check for failed authentication attempts
findstr /i "authentication failed" logs\app.log

REM Check for unusual access patterns
findstr /i "403" logs\app.log
findstr /i "404" logs\app.log
```

### 9. Disable Debug Mode

Never run in debug mode in production:

```ini
DEBUG=False
LOG_LEVEL=INFO
```

### 10. File Extension Restrictions

Limit allowed file types:

```ini
# Only allow media files
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,wmv,mp3,wav,flac
```

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Enable authentication (`AUTH_USERNAME` and `AUTH_PASSWORD`)
- [ ] Set `DEBUG=False`
- [ ] Configure CORS to specific domains
- [ ] Install as Windows Service
- [ ] Configure Windows Firewall
- [ ] Setup SSL/TLS (via IIS or nginx)
- [ ] Configure automated backups
- [ ] Setup monitoring and alerting
- [ ] Test failover and recovery
- [ ] Document access credentials securely
- [ ] Review and test disaster recovery plan

## Support

### Getting Help

- **Documentation**: This README and `/docs` endpoint
- **GitHub Issues**: [github.com/lyjlyjn/lynx/issues](https://github.com/lyjlyjn/lynx/issues)
- **API Docs**: `http://localhost:8000/docs`

### Reporting Issues

When reporting issues, include:
1. Windows version
2. Python version
3. Application version
4. Error messages from logs
5. Steps to reproduce
6. Configuration (sanitized)

### Contributing

Contributions welcome! Please submit pull requests or issues on GitHub.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- FastAPI - Modern web framework
- CloudDrive2 - Google Drive mounting
- FFmpeg - Media processing
- NSSM - Windows service management
- Python community - Excellent libraries and tools
