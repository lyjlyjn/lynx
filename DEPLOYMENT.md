# CloudDrive2 Media Streaming Application

A high-performance Python streaming media application for CloudDrive2 mounted Google Drive files with HTTP Range request support, designed to solve disconnection issues when serving large files.

## Features

- ✅ **HTTP Range Request Support**: Resumable downloads and seeking in media players
- ✅ **Large File Streaming**: Optimized for files of any size without disconnections
- ✅ **CloudDrive2 Integration**: Direct access to mounted Google Drive directories
- ✅ **RESTful API**: Comprehensive API with file browsing and streaming endpoints
- ✅ **Web Interface**: Simple browser-based UI for file exploration
- ✅ **Authentication**: Built-in security with HTTP Basic and Bearer token auth
- ✅ **Media Metadata**: Extract video/audio metadata using FFmpeg
- ✅ **Async I/O**: High-performance asynchronous file operations
- ✅ **Caching**: Intelligent metadata caching for improved performance
- ✅ **Docker Support**: Easy deployment with Docker and docker-compose
- ✅ **Multiple Formats**: Support for video, audio, and document files

## Quick Start

### Prerequisites

- Python 3.8 or higher
- CloudDrive2 with mounted Google Drive
- (Optional) FFmpeg for media metadata extraction
- (Optional) Docker for containerized deployment

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lyjlyjn/lynx.git
cd lynx
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or use the convenience script:
```bash
cd app
python main.py
```

5. Access the web interface:
```
http://localhost:8000
```

6. View API documentation:
```
http://localhost:8000/docs
```

## Configuration

Edit the `.env` file to configure the application:

```ini
# CloudDrive2 Settings
CLOUDDRIVE_MOUNT_PATH=/mnt/clouddrive
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,wmv,flv,webm,mp3,wav,flac,aac,ogg,m4a,pdf,doc,docx,txt,epub

# Security
SECRET_KEY=your-secret-key-here
AUTH_USERNAME=admin
AUTH_PASSWORD=secure_password

# Streaming
CHUNK_SIZE=1048576
ENABLE_RANGE_REQUESTS=True

# Cache
CACHE_ENABLED=True
CACHE_TTL=300
```

See `.env.example` for all available options.

## Docker Deployment

### Using Docker Compose (Recommended)

1. Edit `docker-compose.yml` to configure your CloudDrive2 mount path:
```yaml
volumes:
  - /path/to/your/clouddrive:/mnt/clouddrive:ro
```

2. Start the service:
```bash
docker-compose up -d
```

3. Check logs:
```bash
docker-compose logs -f
```

4. Stop the service:
```bash
docker-compose down
```

### Using Docker

Build and run manually:

```bash
# Build image
docker build -t clouddrive-stream .

# Run container
docker run -d \
  --name clouddrive-stream \
  -p 8000:8000 \
  -v /path/to/clouddrive:/mnt/clouddrive:ro \
  -e AUTH_USERNAME=admin \
  -e AUTH_PASSWORD=secure_password \
  clouddrive-stream
```

## API Usage

### Authentication

If authentication is enabled, you can authenticate in two ways:

**1. HTTP Basic Authentication:**
```bash
curl -u username:password http://localhost:8000/api/files/list
```

**2. Bearer Token:**
```bash
# Get token
curl -X POST -u username:password http://localhost:8000/api/auth/token

# Use token
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/files/list
```

### Streaming Files

Stream a file with Range request support:

```bash
# Stream entire file
curl http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4

# Stream with range (bytes 0-1000000)
curl -H "Range: bytes=0-1000000" http://localhost:8000/api/stream/videos/movie.mp4
```

### Listing Files

List directory contents:

```bash
# List root directory
curl http://localhost:8000/api/files/list

# List specific directory
curl http://localhost:8000/api/files/list/videos
```

### Get File Information

```bash
curl http://localhost:8000/api/files/info/videos/movie.mp4
```

### Get Media Metadata

```bash
curl http://localhost:8000/api/stream/videos/movie.mp4/metadata
```

## API Endpoints

### Streaming

- `GET /api/stream/{file_path}` - Stream a file with Range support
- `HEAD /api/stream/{file_path}` - Get file headers
- `GET /api/stream/{file_path}/info` - Get streaming information
- `GET /api/stream/{file_path}/metadata` - Get media metadata

### File Management

- `GET /api/files/list` - List root directory
- `GET /api/files/list/{dir_path}` - List specific directory
- `GET /api/files/info/{file_path}` - Get file information

### Authentication

- `POST /api/auth/token` - Get authentication token (requires Basic Auth)

### System

- `GET /api/health` - Health check
- `GET /api/stats` - System statistics

See the interactive API documentation at `/docs` for detailed information.

## Client Examples

See `examples/` directory for client code examples:

- `python_client.py` - Python client with Range request support
- `javascript_client.html` - JavaScript/HTML5 video player
- `curl_examples.sh` - Command-line examples

## Architecture

```
app/
├── api/              # API endpoints
│   ├── auth.py       # Authentication endpoints
│   ├── files.py      # File browsing endpoints
│   ├── stream.py     # Streaming endpoints
│   └── system.py     # System endpoints
├── core/             # Core functionality
│   ├── config.py     # Configuration management
│   └── security.py   # Authentication & security
├── models/           # Data models
│   └── __init__.py   # Pydantic models
├── services/         # Business logic
│   ├── cache_service.py   # Caching service
│   ├── file_service.py    # File management
│   └── media_service.py   # Media metadata
├── static/           # Static files
├── templates/        # HTML templates
│   └── index.html    # Web interface
└── main.py          # Application entry point
```

## Performance Optimization

### Chunk Size

Adjust `CHUNK_SIZE` based on your needs:
- Smaller chunks (64KB-256KB): Better for many concurrent users
- Larger chunks (1MB-10MB): Better for fewer users with high bandwidth

### Caching

Enable caching to reduce repeated metadata queries:
```ini
CACHE_ENABLED=True
CACHE_TTL=300
CACHE_MAX_SIZE=1000
```

### Workers

For production, use multiple worker processes:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Troubleshooting

### File Not Found Errors

1. Check CloudDrive2 mount path is correct
2. Verify files exist in the mount point
3. Check file permissions

### Permission Denied

1. Ensure the application has read access to CloudDrive2 mount
2. In Docker, check volume mount permissions

### Streaming Issues

1. Verify `ENABLE_RANGE_REQUESTS=True`
2. Check client supports Range requests
3. Monitor logs for errors

### Media Metadata Not Working

1. Install FFmpeg: `apt-get install ffmpeg`
2. Verify FFmpeg is in PATH
3. Check file is a valid media file

## Security Considerations

1. **Change default credentials**: Always set strong `AUTH_USERNAME` and `AUTH_PASSWORD`
2. **Use HTTPS**: Deploy behind a reverse proxy with SSL/TLS
3. **Set SECRET_KEY**: Use a long, random string for JWT tokens
4. **Restrict mount access**: Mount CloudDrive2 as read-only
5. **Configure CORS**: Limit `CORS_ORIGINS` to trusted domains
6. **Regular updates**: Keep dependencies up to date

## Production Deployment

### Nginx Reverse Proxy

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

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
        proxy_no_cache $http_range $http_if_range;
    }
}
```

### Systemd Service

Create `/etc/systemd/system/clouddrive-stream.service`:

```ini
[Unit]
Description=CloudDrive2 Media Streaming
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/clouddrive-stream
Environment="PATH=/opt/clouddrive-stream/venv/bin"
ExecStart=/opt/clouddrive-stream/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable clouddrive-stream
sudo systemctl start clouddrive-stream
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/lyjlyjn/lynx/issues
- Documentation: http://localhost:8000/docs (when running)

## Acknowledgments

- FastAPI for the excellent web framework
- CloudDrive2 for Google Drive mounting
- FFmpeg for media processing
