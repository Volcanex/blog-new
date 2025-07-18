#!/bin/bash

# Blog deployment script
# Compiles the blog and restarts the server

set -e  # Exit on any error

echo "🔨 Starting blog deployment..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Kill any existing server processes
echo "🛑 Stopping existing server..."
pkill -f "python.*server.py" || true
pkill -f "python.*blog.*server" || true

# Wait a moment for processes to stop
sleep 2

# Compile the blog
echo "📝 Compiling blog..."
python3 compile.py

# Check if compilation was successful
if [ ! -f "output/index.html" ]; then
    echo "❌ Error: Compilation failed - no index.html found"
    exit 1
fi

# Start the server in the background
echo "🚀 Starting server..."
nohup python3 server.py --port 8000 > server.log 2>&1 &

# Wait a moment for server to start
sleep 2

# Check if server started successfully
if pgrep -f "python.*server.py" > /dev/null; then
    echo "✅ Blog deployed successfully!"
    echo "📖 Blog available at: http://localhost:8000"
    echo "📋 Server logs: tail -f server.log"
    echo "🛑 To stop: pkill -f 'python.*server.py'"
else
    echo "❌ Error: Server failed to start"
    echo "Check server.log for details"
    exit 1
fi