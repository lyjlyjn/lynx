<?php
/**
 * CloudDrive2 Media Streaming - Discuz Integration Example
 * 
 * This file demonstrates how to integrate the CloudDrive2 Media Streaming
 * application with Discuz forum for serving large media files.
 * 
 * Features:
 * - Authentication with streaming server
 * - Range request support for resumable downloads
 * - Video player integration
 * - File download links
 * - Error handling
 * 
 * Installation:
 * 1. Copy this file to your Discuz template or plugin directory
 * 2. Configure settings below
 * 3. Include in your attachment display logic
 */

// ============================================================
// Configuration
// ============================================================

// Streaming server configuration
define('STREAMING_SERVER_URL', 'http://your-streaming-server:8000');
define('STREAMING_USERNAME', 'discuz_user');
define('STREAMING_PASSWORD', 'secure_password');

// Cache settings (optional)
define('TOKEN_CACHE_KEY', 'streaming_auth_token');
define('TOKEN_CACHE_DURATION', 1800); // 30 minutes

// ============================================================
// Authentication Functions
// ============================================================

/**
 * Get authentication token from streaming server
 * Uses HTTP Basic Auth to obtain JWT token
 */
function get_streaming_token() {
    global $_G;
    
    // Check cache first
    if (defined('TOKEN_CACHE_KEY')) {
        $cached_token = loadcache(TOKEN_CACHE_KEY);
        if ($cached_token && !is_token_expired($cached_token)) {
            return $cached_token;
        }
    }
    
    // Request new token
    $url = STREAMING_SERVER_URL . '/api/auth/token';
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
    curl_setopt($ch, CURLOPT_USERPWD, STREAMING_USERNAME . ':' . STREAMING_PASSWORD);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code === 200 && $response) {
        $data = json_decode($response, true);
        if (isset($data['access_token'])) {
            $token = $data['access_token'];
            
            // Cache token
            if (defined('TOKEN_CACHE_KEY')) {
                savecache(TOKEN_CACHE_KEY, $token, TOKEN_CACHE_DURATION);
            }
            
            return $token;
        }
    }
    
    return false;
}

/**
 * Check if token is expired (basic check)
 */
function is_token_expired($token) {
    // JWT tokens have expiration in payload
    // This is a simplified check
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return true;
    }
    
    $payload = json_decode(base64_decode($parts[1]), true);
    if (isset($payload['exp'])) {
        return $payload['exp'] < time();
    }
    
    return false;
}

// ============================================================
// Streaming Functions
// ============================================================

/**
 * Get streaming URL for a file
 * 
 * @param string $file_path Relative path to file in CloudDrive
 * @param bool $with_auth Include authentication in URL
 * @return string Streaming URL
 */
function get_streaming_url($file_path, $with_auth = false) {
    $file_path = ltrim($file_path, '/');
    $url = STREAMING_SERVER_URL . '/api/stream/' . urlencode($file_path);
    
    if ($with_auth) {
        $auth = base64_encode(STREAMING_USERNAME . ':' . STREAMING_PASSWORD);
        // Note: Including credentials in URL is less secure
        // Better to use Authorization header or token
    }
    
    return $url;
}

/**
 * Get file information from streaming server
 * 
 * @param string $file_path Relative path to file
 * @return array|false File information or false on error
 */
function get_file_info($file_path) {
    $token = get_streaming_token();
    if (!$token) {
        return false;
    }
    
    $file_path = ltrim($file_path, '/');
    $url = STREAMING_SERVER_URL . '/api/files/info/' . urlencode($file_path);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $token
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code === 200 && $response) {
        return json_decode($response, true);
    }
    
    return false;
}

/**
 * Proxy file stream through Discuz (with authentication)
 * This allows hiding streaming server credentials from users
 * 
 * @param string $file_path Relative path to file
 */
function proxy_file_stream($file_path) {
    $token = get_streaming_token();
    if (!$token) {
        header('HTTP/1.1 503 Service Unavailable');
        echo 'Streaming service unavailable';
        exit;
    }
    
    $file_path = ltrim($file_path, '/');
    $url = STREAMING_SERVER_URL . '/api/stream/' . urlencode($file_path);
    
    // Get range header from client
    $range_header = isset($_SERVER['HTTP_RANGE']) ? $_SERVER['HTTP_RANGE'] : '';
    
    // Initialize cURL
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 0);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER, 1);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    // Set headers
    $headers = [
        'Authorization: Bearer ' . $token
    ];
    
    if ($range_header) {
        $headers[] = 'Range: ' . $range_header;
    }
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    // Header callback to forward response headers
    curl_setopt($ch, CURLOPT_HEADERFUNCTION, function($ch, $header) {
        $len = strlen($header);
        
        // Forward important headers
        if (preg_match('/^Content-Type:/i', $header) ||
            preg_match('/^Content-Length:/i', $header) ||
            preg_match('/^Content-Range:/i', $header) ||
            preg_match('/^Accept-Ranges:/i', $header) ||
            preg_match('/^Content-Disposition:/i', $header)) {
            header(trim($header));
        }
        
        // Check for 206 Partial Content
        if (preg_match('/^HTTP.*206/i', $header)) {
            header('HTTP/1.1 206 Partial Content');
        }
        
        return $len;
    });
    
    // Execute and stream
    curl_exec($ch);
    curl_close($ch);
    exit;
}

// ============================================================
// Display Functions
// ============================================================

/**
 * Generate video player HTML
 * 
 * @param string $file_path Path to video file
 * @param array $options Player options
 * @return string HTML for video player
 */
function render_video_player($file_path, $options = []) {
    $defaults = [
        'width' => '100%',
        'height' => '480',
        'controls' => true,
        'autoplay' => false,
        'preload' => 'metadata'
    ];
    
    $options = array_merge($defaults, $options);
    
    // Get file info
    $file_info = get_file_info($file_path);
    $file_name = $file_info ? $file_info['name'] : basename($file_path);
    
    // Get streaming URL (proxy through Discuz for security)
    $stream_url = 'streaming_proxy.php?file=' . urlencode($file_path);
    
    $html = '<div class="video-player-container">';
    $html .= '<video';
    $html .= ' width="' . htmlspecialchars($options['width']) . '"';
    $html .= ' height="' . htmlspecialchars($options['height']) . '"';
    
    if ($options['controls']) $html .= ' controls';
    if ($options['autoplay']) $html .= ' autoplay';
    
    $html .= ' preload="' . htmlspecialchars($options['preload']) . '"';
    $html .= '>';
    $html .= '<source src="' . htmlspecialchars($stream_url) . '" type="video/mp4">';
    $html .= 'Your browser does not support the video tag.';
    $html .= '</video>';
    $html .= '</div>';
    
    return $html;
}

/**
 * Generate download link HTML
 * 
 * @param string $file_path Path to file
 * @param string $link_text Link text (optional)
 * @return string HTML for download link
 */
function render_download_link($file_path, $link_text = null) {
    // Get file info
    $file_info = get_file_info($file_path);
    
    if ($file_info) {
        $file_name = $file_info['name'];
        $file_size = format_bytes($file_info['size']);
        
        if (!$link_text) {
            $link_text = $file_name . ' (' . $file_size . ')';
        }
    } else {
        $file_name = basename($file_path);
        if (!$link_text) {
            $link_text = $file_name;
        }
    }
    
    // Use proxy URL
    $download_url = 'streaming_proxy.php?file=' . urlencode($file_path);
    
    $html = '<a href="' . htmlspecialchars($download_url) . '" class="download-link">';
    $html .= '<i class="icon-download"></i> ';
    $html .= htmlspecialchars($link_text);
    $html .= '</a>';
    
    return $html;
}

// ============================================================
// Utility Functions
// ============================================================

/**
 * Format bytes to human readable
 */
function format_bytes($bytes, $precision = 2) {
    $units = ['B', 'KB', 'MB', 'GB', 'TB'];
    $bytes = max($bytes, 0);
    $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
    $pow = min($pow, count($units) - 1);
    $bytes /= pow(1024, $pow);
    return round($bytes, $precision) . ' ' . $units[$pow];
}

?>
