#!/bin/bash
# Stop the running Flask server

set -e  # Exit on any error

PID_FILE="flask_server.pid"

echo "🛑 Stopping Flask server..."

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "   Found server PID: $PID"
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "   Stopping server..."
        kill $PID
        sleep 2
        
        # Check if it's still running and force kill if needed
        if ps -p $PID > /dev/null 2>&1; then
            echo "   Force killing server..."
            kill -9 $PID
            sleep 1
        fi
        
        if ps -p $PID > /dev/null 2>&1; then
            echo "   ❌ Failed to stop server"
            exit 1
        else
            echo "   ✅ Server stopped successfully"
        fi
    else
        echo "   Server was not running"
    fi
    
    # Clean up PID file
    rm -f "$PID_FILE"
    echo "   Cleaned up PID file"
    
else
    echo "   No PID file found, checking for any running Flask servers..."
    
    # Try to find any running flask servers
    if pgrep -f "flask_server.py" > /dev/null; then
        echo "   Found running Flask servers, stopping them..."
        pkill -f "flask_server.py"
        sleep 2
        echo "   ✅ Stopped running Flask servers"
    else
        echo "   No running Flask servers found"
    fi
fi

echo "🎉 All Flask servers stopped!"