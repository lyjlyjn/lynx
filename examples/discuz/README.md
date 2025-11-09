# Discuz Integration Guide

This directory contains example code for integrating CloudDrive2 Media Streaming with Discuz forum.

## Files

- `streaming_integration.php` - Main integration library with authentication and display functions
- `streaming_proxy.php` - Proxy script for secure file streaming
- `README.md` - This file

## Installation

### 1. Setup Streaming Server

First, ensure CloudDrive2 Media Streaming is installed and running:

```batch
REM On Windows Server
cd C:\lynx
install.bat
setup.bat
install_service.bat
```

### 2. Configure Discuz Integration

1. Copy integration files to your Discuz directory:
   ```
   /your-discuz/source/plugin/streaming/
   ```

2. Edit `streaming_integration.php` configuration:
   ```php
   define('STREAMING_SERVER_URL', 'http://localhost:8000');
   define('STREAMING_USERNAME', 'discuz_user');
   define('STREAMING_PASSWORD', 'your_secure_password');
   ```

3. Create corresponding user in streaming server `.env`:
   ```ini
   AUTH_USERNAME=discuz_user
   AUTH_PASSWORD=your_secure_password
   ```

### 3. Integration Methods

#### Method A: Template Integration (Simple)

Modify your attachment display template:

```php
<?php
// In your attachment template
require_once 'source/plugin/streaming/streaming_integration.php';

// For video files
if (is_video_file($attachment['filename'])) {
    echo render_video_player($attachment['remote_path']);
}

// For all files
echo render_download_link($attachment['remote_path']);
?>
```

#### Method B: Plugin Integration (Recommended)

Create a Discuz plugin:

1. Create plugin directory: `/source/plugin/streaming/`
2. Create plugin files following Discuz plugin structure
3. Use integration functions in plugin code

#### Method C: Hook Integration

Use Discuz hooks to intercept attachment downloads:

```php
<?php
// In your plugin or hook file
function streaming_attachment_hook($attachment) {
    require_once 'source/plugin/streaming/streaming_integration.php';
    
    // Check if file should be streamed
    if (should_use_streaming($attachment)) {
        proxy_file_stream($attachment['remote_path']);
        exit;
    }
}

// Register hook
// (Adjust according to Discuz version)
add_hook('attachment_download', 'streaming_attachment_hook');
?>
```

## Usage Examples

### Video Player

```php
<?php
require_once 'source/plugin/streaming/streaming_integration.php';

$video_path = 'videos/movie.mp4';

// Basic player
echo render_video_player($video_path);

// Custom options
echo render_video_player($video_path, [
    'width' => '800',
    'height' => '450',
    'autoplay' => false,
    'controls' => true
]);
?>
```

### Download Link

```php
<?php
require_once 'source/plugin/streaming/streaming_integration.php';

$file_path = 'documents/file.pdf';

// Basic link
echo render_download_link($file_path);

// Custom text
echo render_download_link($file_path, 'Download Document');
?>
```

### File Information

```php
<?php
require_once 'source/plugin/streaming/streaming_integration.php';

$file_path = 'videos/movie.mp4';
$file_info = get_file_info($file_path);

if ($file_info) {
    echo "File: " . $file_info['name'] . "<br>";
    echo "Size: " . format_bytes($file_info['size']) . "<br>";
    echo "Type: " . $file_info['type'] . "<br>";
    echo "Streamable: " . ($file_info['is_streamable'] ? 'Yes' : 'No') . "<br>";
}
?>
```

### Direct Streaming (with Range support)

```php
<?php
require_once 'source/plugin/streaming/streaming_integration.php';

// This will proxy the stream with Range request support
// Perfect for large files and video seeking
$file_path = $_GET['file'];
proxy_file_stream($file_path);
?>
```

## Security Considerations

### 1. Authentication

Always use authentication to protect your streaming server:

```php
// In streaming_integration.php
define('STREAMING_USERNAME', 'strong_username');
define('STREAMING_PASSWORD', 'very_strong_password_here');
```

### 2. Path Validation

Validate file paths to prevent directory traversal:

```php
function validate_file_path($file_path) {
    // Remove directory traversal attempts
    $file_path = str_replace(['../', '..\\'], '', $file_path);
    
    // Only allow specific directories
    $allowed_dirs = ['videos', 'audio', 'documents'];
    $parts = explode('/', ltrim($file_path, '/'));
    
    if (empty($parts[0]) || !in_array($parts[0], $allowed_dirs)) {
        return false;
    }
    
    return $file_path;
}

// Use in proxy
$file_path = validate_file_path($_GET['file']);
if ($file_path === false) {
    header('HTTP/1.1 403 Forbidden');
    exit;
}
```

### 3. User Permissions

Check Discuz user permissions before streaming:

```php
function check_streaming_permission($file_path) {
    global $_G;
    
    // Check if user is logged in
    if (!$_G['uid']) {
        return false;
    }
    
    // Check user group permissions
    // Add your permission logic here
    
    return true;
}

// Use in proxy
if (!check_streaming_permission($file_path)) {
    header('HTTP/1.1 403 Forbidden');
    echo 'Access denied';
    exit;
}
```

### 4. Rate Limiting

Implement rate limiting to prevent abuse:

```php
function check_rate_limit($user_id) {
    // Implement rate limiting logic
    // e.g., max 100 requests per hour per user
    
    return true;
}
```

### 5. HTTPS

Use HTTPS for production:

```php
// Force HTTPS
if (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off') {
    header('Location: https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
    exit;
}
```

## Testing

### Test Authentication

```bash
# Test from command line
curl -u discuz_user:password http://localhost:8000/api/auth/token
```

### Test File Access

```bash
# Test file info
curl -u discuz_user:password http://localhost:8000/api/files/info/videos/test.mp4

# Test streaming
curl -u discuz_user:password http://localhost:8000/api/stream/videos/test.mp4 -o test.mp4

# Test range request
curl -u discuz_user:password -H "Range: bytes=0-1000000" http://localhost:8000/api/stream/videos/test.mp4 -o chunk.mp4
```

### Test Through Discuz

```php
<?php
// Test page (test_streaming.php)
require_once 'source/plugin/streaming/streaming_integration.php';

echo "<h1>Streaming Integration Test</h1>";

// Test authentication
$token = get_streaming_token();
echo "<h2>Authentication</h2>";
echo $token ? "✓ Token obtained" : "✗ Authentication failed";
echo "<br><br>";

// Test file info
$test_file = 'videos/test.mp4';
echo "<h2>File Info</h2>";
$file_info = get_file_info($test_file);
if ($file_info) {
    echo "<pre>";
    print_r($file_info);
    echo "</pre>";
} else {
    echo "✗ Failed to get file info";
}

// Test video player
echo "<h2>Video Player</h2>";
if (is_video_file($test_file)) {
    echo render_video_player($test_file);
} else {
    echo "Not a video file";
}

// Test download link
echo "<h2>Download Link</h2>";
echo render_download_link($test_file);
?>
```

## Troubleshooting

### Common Issues

#### 1. Authentication Failed

**Error**: "Unable to connect to streaming server"

**Solutions**:
- Check `STREAMING_SERVER_URL` is correct
- Verify streaming server is running
- Check username/password match `.env` configuration
- Test with curl: `curl -u username:password http://server:8000/api/auth/token`

#### 2. File Not Found

**Error**: "File not found"

**Solutions**:
- Verify file path is relative to `CLOUDDRIVE_MOUNT_PATH`
- Check CloudDrive2 is mounted and accessible
- Test with: `curl -u username:password http://server:8000/api/files/info/path/to/file`

#### 3. Video Won't Play

**Solutions**:
- Check browser console for errors
- Verify video codec is supported (H.264/AAC recommended)
- Test streaming URL directly in browser
- Check CORS settings if cross-domain

#### 4. Download Interrupted

**Solutions**:
- Verify `ENABLE_RANGE_REQUESTS=True` in `.env`
- Check proxy configuration forwards Range headers
- Test with curl: `curl -H "Range: bytes=0-1000" URL`

#### 5. Slow Performance

**Solutions**:
- Enable caching in streaming server
- Increase `CHUNK_SIZE` in `.env`
- Use CDN or reverse proxy (nginx/IIS)
- Check network bandwidth

### Debug Mode

Enable debug output:

```php
// At top of streaming_integration.php
define('DEBUG_MODE', true);

// Add debug function
function debug_log($message) {
    if (defined('DEBUG_MODE') && DEBUG_MODE) {
        error_log('[Streaming] ' . $message);
    }
}

// Use in functions
debug_log('Getting token from: ' . $url);
```

Check PHP error log for debug messages.

## Performance Optimization

### 1. Token Caching

The integration already implements token caching. Ensure your Discuz cache is working:

```php
// Verify cache is working
$token = get_streaming_token();
debug_log('Token from cache: ' . ($token ? 'Yes' : 'No'));
```

### 2. File Info Caching

Cache file information:

```php
function get_file_info_cached($file_path, $ttl = 300) {
    $cache_key = 'fileinfo_' . md5($file_path);
    
    // Try cache
    $cached = getcache($cache_key);
    if ($cached) {
        return $cached;
    }
    
    // Get from server
    $file_info = get_file_info($file_path);
    if ($file_info) {
        savecache($cache_key, $file_info, $ttl);
    }
    
    return $file_info;
}
```

### 3. Use CDN/Proxy

For better performance, use nginx or IIS as reverse proxy:

```nginx
# nginx config
location /stream/ {
    proxy_pass http://localhost:8000/api/stream/;
    proxy_http_version 1.1;
    proxy_set_header Range $http_range;
    proxy_set_header If-Range $http_if_range;
    proxy_cache_bypass $http_range;
}
```

## Support

For issues with integration:

1. Check this README
2. Review WINDOWS_README.md in main directory
3. Test streaming server independently
4. Check Discuz logs and PHP error log
5. Report issues on GitHub

## License

MIT License - Same as main application
