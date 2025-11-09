#!/bin/bash
# CloudDrive2 Media Streaming API - cURL Examples

API_URL="http://localhost:8000"
USERNAME=""  # Set if authentication is enabled
PASSWORD=""

# Build auth flag
AUTH_FLAG=""
if [ ! -z "$USERNAME" ] && [ ! -z "$PASSWORD" ]; then
    AUTH_FLAG="-u $USERNAME:$PASSWORD"
fi

echo "=== CloudDrive2 Media Streaming API Examples ==="
echo ""

# 1. Health Check
echo "1. Health Check"
curl -s $AUTH_FLAG "$API_URL/api/health" | python3 -m json.tool
echo ""

# 2. Get System Stats
echo "2. System Statistics"
curl -s $AUTH_FLAG "$API_URL/api/stats" | python3 -m json.tool
echo ""

# 3. List Root Directory
echo "3. List Root Directory"
curl -s $AUTH_FLAG "$API_URL/api/files/list" | python3 -m json.tool
echo ""

# 4. List Specific Directory
echo "4. List Specific Directory (example: /videos)"
curl -s $AUTH_FLAG "$API_URL/api/files/list/videos" | python3 -m json.tool 2>/dev/null || echo "Directory not found"
echo ""

# 5. Get File Info
echo "5. Get File Information (example: /videos/sample.mp4)"
curl -s $AUTH_FLAG "$API_URL/api/files/info/videos/sample.mp4" | python3 -m json.tool 2>/dev/null || echo "File not found"
echo ""

# 6. Get Stream Info
echo "6. Get Stream Information (example: /videos/sample.mp4)"
curl -s $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4/info" | python3 -m json.tool 2>/dev/null || echo "File not found"
echo ""

# 7. Get Media Metadata
echo "7. Get Media Metadata (example: /videos/sample.mp4)"
curl -s $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4/metadata" | python3 -m json.tool 2>/dev/null || echo "File not found or not a media file"
echo ""

# 8. HEAD Request for File
echo "8. HEAD Request (check file without downloading)"
curl -I $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4" 2>/dev/null || echo "File not found"
echo ""

# 9. Download File (full)
echo "9. Download Full File (example: /videos/sample.mp4)"
echo "curl $AUTH_FLAG \"$API_URL/api/stream/videos/sample.mp4\" -o sample.mp4"
echo "(Uncomment to download)"
# curl $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4" -o sample.mp4
echo ""

# 10. Download File with Range Request
echo "10. Download with Range Request (first 1MB)"
echo "curl -H \"Range: bytes=0-1048575\" $AUTH_FLAG \"$API_URL/api/stream/videos/sample.mp4\" -o sample_part.mp4"
echo "(Uncomment to download)"
# curl -H "Range: bytes=0-1048575" $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4" -o sample_part.mp4
echo ""

# 11. Resume Download
echo "11. Resume Download (if partially downloaded)"
echo "curl -C - $AUTH_FLAG \"$API_URL/api/stream/videos/sample.mp4\" -o sample.mp4"
echo "(Uncomment to download)"
# curl -C - $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4" -o sample.mp4
echo ""

# 12. Authentication Token (if auth enabled)
if [ ! -z "$USERNAME" ] && [ ! -z "$PASSWORD" ]; then
    echo "12. Get Authentication Token"
    TOKEN=$(curl -s -X POST -u "$USERNAME:$PASSWORD" "$API_URL/api/auth/token" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "Token: $TOKEN"
    echo ""
    
    echo "13. Use Bearer Token"
    curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/api/files/list" | python3 -m json.tool
    echo ""
fi

# 14. Stream with wget
echo "14. Download with wget (supports resume)"
echo "wget --continue $AUTH_FLAG \"$API_URL/api/stream/videos/sample.mp4\""
echo "(Uncomment to download)"
# wget --continue $AUTH_FLAG "$API_URL/api/stream/videos/sample.mp4"
echo ""

# 15. Stream with ffmpeg
echo "15. Play with ffmpeg (audio/video)"
echo "ffmpeg -i \"$API_URL/api/stream/videos/sample.mp4\" -f null -"
echo "(Uncomment to test)"
# ffmpeg -i "$API_URL/api/stream/videos/sample.mp4" -f null -
echo ""

echo "=== Examples Complete ==="
