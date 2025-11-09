<?php
/**
 * CloudDrive2 Media Streaming - Proxy Script for Discuz
 * 
 * This script proxies file streaming requests through Discuz,
 * hiding streaming server credentials from end users.
 * 
 * Usage: streaming_proxy.php?file=path/to/file.mp4
 */

// Include Discuz framework (adjust path as needed)
// require_once './source/class/class_core.php';

// Include streaming integration functions
require_once 'streaming_integration.php';

// Get file path from query parameter
$file_path = isset($_GET['file']) ? $_GET['file'] : '';

if (empty($file_path)) {
    header('HTTP/1.1 400 Bad Request');
    echo 'Missing file parameter';
    exit;
}

// Security: Validate file path
// Add your own validation logic here
// For example, check if user has permission to access this file

// Proxy the file stream
proxy_file_stream($file_path);
?>
