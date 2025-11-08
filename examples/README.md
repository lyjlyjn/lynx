# Client Examples

This directory contains example client code for interacting with the CloudDrive2 Media Streaming API.

## Files

### 1. python_client.py
A Python client library demonstrating:
- Authentication with the API
- Listing files and directories
- Getting file information
- Downloading files with Range request support
- Resumable downloads

**Usage:**
```bash
python python_client.py
```

Edit the `main()` function to customize the base URL and authentication credentials.

**Example: Download a file**
```python
from python_client import CloudDriveClient

client = CloudDriveClient(
    base_url="http://localhost:8000",
    username="admin",  # Optional
    password="password"
)

# Download with resume support
client.download_file("/videos/movie.mp4", "local_movie.mp4", resume=True)
```

### 2. video_player.html
An HTML5 video player demonstrating:
- Loading and playing video files
- Displaying file information
- Showing media metadata (duration, resolution, codec)
- Range request support for seeking

**Usage:**
Simply open the file in a web browser. No server required.

**Features:**
- Enter API URL and file path
- Optional authentication
- Display file information
- Extract and display media metadata
- Video playback with seeking support

### 3. curl_examples.sh
A bash script with cURL command examples demonstrating:
- All API endpoints
- Authentication methods
- Range requests
- Resumable downloads
- File listing and browsing

**Usage:**
```bash
./curl_examples.sh
```

Edit the script to set your API URL and credentials:
```bash
API_URL="http://localhost:8000"
USERNAME="admin"  # Set if auth is enabled
PASSWORD="password"
```

## Quick Examples

### List Files
```bash
curl http://localhost:8000/api/files/list
```

### Stream a File
```bash
curl http://localhost:8000/api/stream/videos/movie.mp4 -o movie.mp4
```

### Stream with Range Request
```bash
curl -H "Range: bytes=0-1048575" http://localhost:8000/api/stream/videos/movie.mp4
```

### Get File Info
```bash
curl http://localhost:8000/api/files/info/videos/movie.mp4
```

### Get Media Metadata
```bash
curl http://localhost:8000/api/stream/videos/movie.mp4/metadata
```

### With Authentication
```bash
# Using Basic Auth
curl -u username:password http://localhost:8000/api/files/list

# Using Bearer Token
TOKEN=$(curl -X POST -u username:password http://localhost:8000/api/auth/token | jq -r '.access_token')
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/files/list
```

## Integration Examples

### JavaScript/Fetch API
```javascript
// List files
fetch('http://localhost:8000/api/files/list')
  .then(response => response.json())
  .then(data => console.log(data));

// Stream with Range
fetch('http://localhost:8000/api/stream/video.mp4', {
  headers: {
    'Range': 'bytes=0-1048575'
  }
})
  .then(response => response.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    document.getElementById('video').src = url;
  });
```

### Python Requests
```python
import requests

# List files
response = requests.get('http://localhost:8000/api/files/list')
files = response.json()

# Stream with Range
headers = {'Range': 'bytes=0-1048575'}
response = requests.get(
    'http://localhost:8000/api/stream/video.mp4',
    headers=headers,
    stream=True
)

with open('video_part.mp4', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### FFmpeg
```bash
# Play a remote file
ffmpeg -i http://localhost:8000/api/stream/video.mp4 -f null -

# Extract audio
ffmpeg -i http://localhost:8000/api/stream/video.mp4 -vn -acodec copy audio.aac

# Re-encode
ffmpeg -i http://localhost:8000/api/stream/video.mp4 -c:v libx264 -c:a aac output.mp4
```

### VLC Media Player
Simply use the streaming URL:
```
http://localhost:8000/api/stream/videos/movie.mp4
```

VLC will automatically use Range requests for seeking.

## Notes

- All examples assume the server is running on `http://localhost:8000`
- Adjust the base URL if your server is running elsewhere
- Enable authentication in `.env` if security is needed
- Range requests require `ENABLE_RANGE_REQUESTS=True` in configuration
