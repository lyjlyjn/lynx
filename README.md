# CloudDrive2 Media Streaming Application

A high-performance Python streaming media application for CloudDrive2 mounted Google Drive files with HTTP Range request support.

> 📖 **中文使用指南**: [USAGE_CN.md](USAGE_CN.md) - 详细的中文使用说明

## Overview

This application provides a robust solution for streaming large files from CloudDrive2 mounted Google Drive without disconnections. It solves the common issue where Nginx disconnects when serving large files through Discuz, while small files work fine.

## Key Features

- ✅ **HTTP Range Request Support**: Enable resumable downloads and seeking in media players
- ✅ **Large File Streaming**: Optimized for files of any size without disconnections
- ✅ **CloudDrive2 Integration**: Direct access to mounted Google Drive directories
- ✅ **RESTful API**: Comprehensive API with file browsing and streaming endpoints
- ✅ **Web Interface**: Simple browser-based UI for file exploration
- ✅ **Authentication**: Built-in security with HTTP Basic and Bearer token auth
- ✅ **Media Metadata**: Extract video/audio metadata using FFmpeg
- ✅ **Async I/O**: High-performance asynchronous file operations
- ✅ **Caching**: Intelligent metadata caching for improved performance
- ✅ **Docker Support**: Easy deployment with Docker and docker-compose
- ✅ **Windows Server Support**: Native Windows Service, batch scripts, and firewall configuration
- ✅ **Discuz Integration**: Ready-to-use PHP integration for Discuz forums
- ✅ **Multiple Formats**: Support for video, audio, and document files

## Quick Start

> 🪟 **Windows Server Users**: See [WINDOWS_README.md](WINDOWS_README.md) for Windows-specific installation guide

### Windows Server Installation

1. Install dependencies:
```batch
install.bat
```

2. Configure application:
```batch
setup.bat
```

3. Start server:
```batch
start.bat
```

Or install as Windows Service:
```batch
install_service.bat
```

See [WINDOWS_README.md](WINDOWS_README.md) for comprehensive Windows Server guide.

### Using Docker (Recommended for Linux)

1. Edit `docker-compose.yml` to set your CloudDrive2 mount path:
```yaml
volumes:
  - /path/to/your/clouddrive:/mnt/clouddrive:ro
```

2. Start the service:
```bash
docker-compose up -d
```

3. Access the web interface:
```
http://localhost:8000
```

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure settings:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the application:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Documentation

- **Windows Server Guide**: See [WINDOWS_README.md](WINDOWS_README.md) for Windows-specific setup
- **Windows Service Setup**: See [WINDOWS_SERVICE_GUIDE.md](WINDOWS_SERVICE_GUIDE.md) for service configuration
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- **API Documentation**: See [API.md](API.md) or visit `http://localhost:8000/docs` when running
- **Discuz Integration**: See [examples/discuz/](examples/discuz/) for PHP integration examples
- **Examples**: Check the `examples/` directory for client code examples

## Project Structure

```
.
├── app/                      # Main application
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   ├── models/               # Data models
│   ├── services/             # Business logic
│   ├── templates/            # HTML templates
│   └── main.py              # Application entry point
├── examples/                 # Client examples
│   ├── python_client.py     # Python client
│   ├── video_player.html    # HTML5 video player
│   └── curl_examples.sh     # cURL examples
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Example configuration
└── DEPLOYMENT.md           # Deployment documentation
```

## API Endpoints

### Streaming
- `GET /api/stream/{file_path}` - Stream file with Range support
- `HEAD /api/stream/{file_path}` - Get file headers
- `GET /api/stream/{file_path}/info` - Get streaming info
- `GET /api/stream/{file_path}/metadata` - Get media metadata

### File Management
- `GET /api/files/list` - List root directory
- `GET /api/files/list/{dir_path}` - List directory
- `GET /api/files/info/{file_path}` - Get file info

### Authentication
- `POST /api/auth/token` - Get authentication token

### System
- `GET /api/health` - Health check
- `GET /api/stats` - System statistics

## Configuration

Key configuration options in `.env`:

```ini
# CloudDrive2 mount path
CLOUDDRIVE_MOUNT_PATH=/mnt/clouddrive

# Authentication (optional)
AUTH_USERNAME=admin
AUTH_PASSWORD=secure_password

# Streaming settings
CHUNK_SIZE=1048576
ENABLE_RANGE_REQUESTS=True
```

See `.env.example` for all available options.

## Tech Stack

- **Framework**: FastAPI
- **Python**: 3.8+
- **Async I/O**: aiofiles, asyncio
- **Media Processing**: FFmpeg
- **Authentication**: python-jose, passlib
- **Deployment**: Docker, docker-compose

## Use Cases

1. **Media Streaming**: Stream video/audio files to web browsers or media players
2. **Large File Downloads**: Provide resumable downloads for large files
3. **Google Drive Access**: Access CloudDrive2 mounted Google Drive files via HTTP
4. **API Integration**: Integrate with other applications via RESTful API

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/lyjlyjn/lynx/issues
- Documentation: See DEPLOYMENT.md