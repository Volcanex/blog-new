#!/bin/bash
# Deployment script for GCP e2-micro instance
# Handles static file deployment and Flask API server management

set -e  # Exit on any error

echo "🚀 Starting blog deployment..."
echo "=============================="

# Configuration
STATIC_DIR="output"
API_PORT="${API_PORT:-5000}"
LOG_DIR="logs"
PID_FILE="flask_server.pid"

# Create logs directory
mkdir -p "$LOG_DIR"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to stop existing Flask server
stop_flask_server() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        echo "🛑 Stopping existing Flask server (PID: $pid)..."
        
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            sleep 2
            
            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                echo "   Force killing server..."
                kill -9 $pid
            fi
        fi
        
        rm -f "$PID_FILE"
        echo "   ✅ Flask server stopped"
    fi
}

# Check if output directory exists
if [ ! -d "$STATIC_DIR" ]; then
    echo "❌ Error: $STATIC_DIR directory not found!"
    echo "   Run ./compile.sh first to generate static files"
    exit 1
fi

# Check if required files exist
if [ ! -f "flask_server.py" ]; then
    echo "❌ Error: flask_server.py not found"
    exit 1
fi

# Setup virtual environment and install dependencies
VENV_DIR="venv"

if [ -f "requirements.txt" ]; then
    echo "📦 Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        echo "   Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    
    # Activate virtual environment and install dependencies
    echo "   Installing dependencies in virtual environment..."
    source "$VENV_DIR/bin/activate"
    pip install -r requirements.txt --quiet
    
    echo "   ✅ Dependencies ready in virtual environment"
    
    # Update Python command to use venv
    PYTHON_CMD="$VENV_DIR/bin/python"
else
    echo "⚠️  No requirements.txt found, using system Python"
    PYTHON_CMD="python3"
fi

# Stop any existing Flask server
stop_flask_server

# Deploy static files (copy to a web-accessible location if needed)
echo "📁 Deploying static files..."
echo "   Static files location: $(pwd)/$STATIC_DIR"
echo "   File count: $(find $STATIC_DIR -type f | wc -l)"

# Start Flask API server in background
echo "🌐 Starting Flask API server on port $API_PORT..."
nohup $PYTHON_CMD flask_server.py --port $API_PORT > "$LOG_DIR/flask_server.log" 2>&1 &
FLASK_PID=$!

# Store the PID for later management
echo $FLASK_PID > "$PID_FILE"

# Wait a moment and check if the server started successfully
sleep 3

if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "   ✅ Flask API server started successfully (PID: $FLASK_PID)"
    echo "   📊 API Status: http://localhost:$API_PORT/api/health"
    echo "   🔍 Logs: tail -f $LOG_DIR/flask_server.log"
    
    # Check for endpoint collision warnings in the log
    if grep -q "⚠️.*collision" "$LOG_DIR/flask_server.log" 2>/dev/null; then
        echo ""
        echo "⚠️  ENDPOINT COLLISION WARNINGS DETECTED:"
        echo "========================================"
        grep -A 2 "⚠️.*collision" "$LOG_DIR/flask_server.log" | head -20
        echo ""
        echo "Please review your API endpoints to avoid conflicts!"
        echo "Consider using page-specific route prefixes."
    fi
else
    echo "   ❌ Flask server failed to start"
    echo "   Check logs: cat $LOG_DIR/flask_server.log"
    exit 1
fi

# Show deployment summary
echo ""
echo "🎉 Deployment completed successfully!"
echo "=================================="
echo "📍 URLs available:"
echo "   🏠 Homepage: http://localhost:$API_PORT/"
echo "   🔌 API Health: http://localhost:$API_PORT/api/health"
echo "   📋 Pages List: http://localhost:$API_PORT/api/pages"
echo ""
echo "📂 Static files: $STATIC_DIR/"
echo "📊 API Server PID: $FLASK_PID (saved to $PID_FILE)"
echo "📝 Server logs: $LOG_DIR/flask_server.log"
echo ""
echo "🛠️  Management commands:"
echo "   View logs: tail -f $LOG_DIR/flask_server.log"
echo "   Restart: ./deploy.sh"

# Test the deployment
echo ""
echo "🧪 Testing deployment..."
if command -v curl &> /dev/null; then
    echo "   Testing API health endpoint..."
    sleep 1  # Give server another moment
    
    if curl -s -f "http://localhost:$API_PORT/api/health" > /dev/null; then
        echo "   ✅ API responding correctly"
    else
        echo "   ⚠️  API may not be fully ready yet (check logs)"
    fi
    
    # Validate nginx configuration for asset serving
    echo ""
    echo "📋 Validating nginx asset configuration..."
    if command -v nginx &> /dev/null; then
        if nginx -T 2>/dev/null | grep -q "location /assets/"; then
            echo "   ✅ nginx configured to serve assets directly"
        else
            echo "   ⚠️  WARNING: nginx not configured for /assets/ directory"
            echo "   Add this to your nginx server block:"
            echo "   location /assets/ { alias $(pwd)/output/assets/; expires 1h; }"
        fi
    else
        echo "   ℹ️  nginx not found - if using production, ensure /assets/ is configured"
    fi
else
    echo "   ⚠️  curl not found, skipping API test"
fi

echo ""
echo "✨ Blog is now live and ready!"