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

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/lyjlyjn/lynx/issues
- Documentation: See DEPLOYMENT.md
