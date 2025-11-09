#!/bin/bash
# Start CloudDrive2 Media Streaming Application

set -e

echo "========================================"
echo "CloudDrive2 Media Streaming"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file to configure:"
    echo "   - CLOUDDRIVE_MOUNT_PATH (path to your CloudDrive2 mount)"
    echo "   - SECRET_KEY (use a secure random string)"
    echo "   - AUTH_USERNAME and AUTH_PASSWORD (if you want authentication)"
    echo ""
    echo "Press Enter to continue or Ctrl+C to exit and edit .env first..."
    read
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install/update dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create logs directory
mkdir -p logs
echo "✓ Logs directory ready"

# Check mount path
if [ -f .env ]; then
    MOUNT_PATH=$(grep CLOUDDRIVE_MOUNT_PATH .env | cut -d '=' -f2)
    if [ ! -z "$MOUNT_PATH" ] && [ ! -d "$MOUNT_PATH" ]; then
        echo ""
        echo "⚠️  WARNING: CloudDrive mount path does not exist: $MOUNT_PATH"
        echo "   The application will create it on startup."
        echo ""
    fi
fi

# Start application
echo ""
echo "========================================"
echo "Starting server..."
echo "========================================"
echo ""
echo "Access the application at:"
echo "  🌐 Web Interface: http://localhost:8000"
echo "  📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
