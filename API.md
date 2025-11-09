# API Documentation

CloudDrive2 Media Streaming API provides RESTful endpoints for accessing and streaming files from CloudDrive2 mounted Google Drive.

## Base URL

```
http://localhost:8000
```

## Authentication

The API supports two authentication methods:

### 1. HTTP Basic Authentication
```bash
curl -u username:password http://localhost:8000/api/files/list
```

### 2. Bearer Token (JWT)
```bash
# Get token
curl -X POST -u username:password http://localhost:8000/api/auth/token

# Use token
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/files/list
```

**Note:** Authentication is optional. Set `AUTH_USERNAME` and `AUTH_PASSWORD` in `.env` to enable it.

---

## Endpoints

### System Endpoints

#### Health Check
Check if the service is running.

```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-01T12:00:00"
}
```

#### System Statistics
Get system configuration and statistics.

```
GET /api/stats
```

**Response:**
```json
{
  "app_name": "CloudDrive2 Media Streaming",
  "version": "1.0.0",
  "cache": {
    "enabled": true,
    "size": 0,
    "max_size": 1000,
    "ttl": 300
  },
  "settings": {
    "chunk_size": 1048576,
    "max_chunk_size": 10485760,
    "enable_range_requests": true,
    "allowed_extensions": ["mp4", "mkv", "..."]
  }
}
```

---

### File Management Endpoints

#### List Directory
List contents of a directory.

```
GET /api/files/list
GET /api/files/list/{dir_path}
```

**Parameters:**
- `dir_path` (optional): Directory path to list (default: `/`)

**Response:**
```json
{
  "name": "videos",
  "path": "/videos",
  "files": [
    {
      "name": "movie.mp4",
      "path": "/videos/movie.mp4",
      "size": 1024000000,
      "type": "video",
      "extension": "mp4",
      "modified": "2025-01-01T12:00:00",
      "mime_type": "video/mp4",
      "is_streamable": true
    }
  ],
  "subdirectories": ["movies", "tv-shows"],
  "total_files": 10,
  "total_size": 10240000000
}
```

#### Get File Information
Get detailed information about a specific file.

```
GET /api/files/info/{file_path}
```

**Parameters:**
- `file_path`: Path to the file

**Response:**
```json
{
  "name": "movie.mp4",
  "path": "/videos/movie.mp4",
  "size": 1024000000,
  "type": "video",
  "extension": "mp4",
  "modified": "2025-01-01T12:00:00",
  "mime_type": "video/mp4",
  "is_streamable": true
}
```

---

### Streaming Endpoints

#### Stream File
Stream a file with HTTP Range request support.

```
GET /api/stream/{file_path}
```

**Parameters:**
- `file_path`: Path to the file

**Headers:**
- `Range` (optional): Byte range to stream (e.g., `bytes=0-1048575`)

**Response Headers:**
- `Accept-Ranges: bytes`
- `Content-Length: <size>`
- `Content-Type: <mime-type>`
- `Content-Disposition: inline; filename="<filename>"`
- `Content-Range: bytes <start>-<end>/<total>` (if Range requested)

**Status Codes:**
- `200 OK` - Full file
- `206 Partial Content` - Range request
- `416 Range Not Satisfiable` - Invalid range

**Example:**
```bash
# Stream full file
curl http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4

# Stream range
curl -H "Range: bytes=0-1048575" http://localhost:8000/api/stream/videos/movie.mp4
```

#### HEAD Request
Get file headers without content.

```
HEAD /api/stream/{file_path}
```

**Response Headers:**
- `Accept-Ranges: bytes`
- `Content-Length: <size>`
- `Content-Type: <mime-type>`
- `Content-Disposition: inline; filename="<filename>"`

#### Get Stream Information
Get streaming information for a file.

```
GET /api/stream/{file_path}/info
```

**Response:**
```json
{
  "file_path": "/videos/movie.mp4",
  "file_size": 1024000000,
  "content_type": "video/mp4",
  "supports_range": true,
  "chunk_size": 1048576
}
```

#### Get Media Metadata
Get media metadata for video/audio files (requires FFmpeg).

```
GET /api/stream/{file_path}/metadata
```

**Response:**
```json
{
  "duration": 7200.5,
  "width": 1920,
  "height": 1080,
  "bitrate": 5000000,
  "codec": "h264",
  "format": "mp4",
  "audio_codec": "aac",
  "audio_channels": 2
}
```

**Returns:** `null` if metadata cannot be extracted or file is not a media file.

---

### Authentication Endpoints

#### Get Access Token
Authenticate and get a JWT access token.

```
POST /api/auth/token
```

**Authentication:** HTTP Basic Auth required

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Response:**
```json
{
  "detail": "Incorrect username or password"
}
```

---

## HTTP Range Requests

The streaming endpoint supports HTTP Range requests for resumable downloads and seeking in media players.

### Request Format
```
Range: bytes=<start>-<end>
```

### Examples
```bash
# First 1MB
Range: bytes=0-1048575

# From byte 1000000 to end
Range: bytes=1000000-

# Last 1MB (not supported in this implementation)
# Range: bytes=-1048576
```

### Response
```
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1048575/1024000000
Content-Length: 1048576
Accept-Ranges: bytes
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message"
}
```

### Common Status Codes

- `200 OK` - Success
- `206 Partial Content` - Range request success
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - File or directory not found
- `416 Range Not Satisfiable` - Invalid range
- `500 Internal Server Error` - Server error

---

## Interactive Documentation

For interactive API documentation with the ability to test endpoints:

**Swagger UI:** `http://localhost:8000/docs`
**ReDoc:** `http://localhost:8000/redoc`

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider adding rate limiting using tools like:
- Nginx rate limiting
- FastAPI rate limiting middleware
- Redis-based rate limiting

---

## CORS

CORS is configured by default to allow all origins. To restrict origins, set the `CORS_ORIGINS` environment variable:

```ini
CORS_ORIGINS=http://localhost:3000,https://example.com
```

---

## Security Considerations

1. **HTTPS:** Always use HTTPS in production
2. **Authentication:** Enable authentication for sensitive data
3. **Token Expiry:** Tokens expire after 30 minutes by default
4. **Path Traversal:** The API prevents directory traversal attacks
5. **File Types:** Only allowed file extensions can be accessed

---

## Client Libraries

See the `examples/` directory for client libraries:
- Python client: `examples/python_client.py`
- JavaScript/HTML: `examples/video_player.html`
- cURL examples: `examples/curl_examples.sh`
- Discuz integration: `examples/discuz/` - PHP integration for Discuz forums

---

## Windows-Specific Examples

### PowerShell

```powershell
# Get file list
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/files/list" `
    -Method Get `
    -Headers @{Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("username:password"))}

# Stream file
Invoke-WebRequest -Uri "http://localhost:8000/api/stream/videos/movie.mp4" `
    -OutFile "C:\Downloads\movie.mp4" `
    -Headers @{Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("username:password"))}

# Stream with range
$headers = @{
    Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("username:password"))
    Range = "bytes=0-1048575"
}
Invoke-WebRequest -Uri "http://localhost:8000/api/stream/videos/movie.mp4" `
    -OutFile "C:\Downloads\chunk.mp4" `
    -Headers $headers
```

### Batch Script

```batch
@echo off
REM Download file using curl (install from https://curl.se/)
curl -u username:password http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4

REM Download with progress
curl -u username:password -# http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4

REM Resume download
curl -u username:password -C - http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4
```

### C# (.NET)

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        using var client = new HttpClient();
        
        // Set base URL
        client.BaseAddress = new Uri("http://localhost:8000");
        
        // Set authentication
        var credentials = Convert.ToBase64String(
            Encoding.ASCII.GetBytes("username:password"));
        client.DefaultRequestHeaders.Authorization = 
            new AuthenticationHeaderValue("Basic", credentials);
        
        // Get file list
        var response = await client.GetAsync("/api/files/list");
        var content = await response.Content.ReadAsStringAsync();
        Console.WriteLine(content);
        
        // Download file
        var fileResponse = await client.GetAsync("/api/stream/videos/movie.mp4");
        using var fileStream = await fileResponse.Content.ReadAsStreamAsync();
        using var outputFile = File.Create("movie.mp4");
        await fileStream.CopyToAsync(outputFile);
    }
}
```

### VBScript (Legacy)

```vbscript
' Download file using WinHTTP
Dim http, stream
Set http = CreateObject("WinHttp.WinHttpRequest.5.1")

' Configure authentication
http.Open "GET", "http://localhost:8000/api/stream/videos/movie.mp4", False
http.SetCredentials "username", "password", 0

' Send request
http.Send

' Save to file
Set stream = CreateObject("ADODB.Stream")
stream.Type = 1  ' Binary
stream.Open
stream.Write http.ResponseBody
stream.SaveToFile "movie.mp4", 2
stream.Close

WScript.Echo "Download complete"
```

---

## Discuz Integration

For integrating with Discuz forums, see the comprehensive examples in `examples/discuz/`:

- `streaming_integration.php` - Complete PHP integration library
- `streaming_proxy.php` - Proxy script for secure streaming
- `README.md` - Detailed integration guide

**Key features:**
- Authentication with streaming server
- Range request support for resumable downloads
- Video player integration
- File browser integration
- Security and permission checks

**Quick example:**

```php
<?php
require_once 'examples/discuz/streaming_integration.php';

// Display video player
echo render_video_player('videos/movie.mp4');

// Display download link
echo render_download_link('documents/file.pdf');

// Get file information
$info = get_file_info('videos/movie.mp4');
echo "Size: " . format_bytes($info['size']);
?>
```

See `examples/discuz/README.md` for complete documentation.

---

## Support

For issues and questions:
- **GitHub Issues**: https://github.com/lyjlyjn/lynx/issues
- **Documentation**: See DEPLOYMENT.md and WINDOWS_README.md
- **Windows Setup**: See WINDOWS_SERVICE_GUIDE.md
- **Discuz Integration**: See examples/discuz/README.md
