#!/bin/bash
# Compile script for modular blog
# Compiles all pages and prepares static output

set -e  # Exit on any error

echo "🔧 Starting blog compilation..."
echo "================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if compile.py exists
if [ ! -f "compile.py" ]; then
    echo "❌ Error: compile.py not found in current directory"
    exit 1
fi

# Setup Python command (use venv if it exists)
if [ -d "venv" ] && [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
    echo "   Using virtual environment: venv/"
else
    PYTHON_CMD="python3"
    echo "   Using system Python"
fi

# Run the compiler
echo "📝 Running modular blog compiler..."
$PYTHON_CMD compile.py

# Check if compilation was successful
if [ $? -eq 0 ] && [ -d "output" ]; then
    echo "✅ Compilation completed successfully!"
    
    # Show what was generated
    html_count=$(find output -name "*.html" | wc -l)
    asset_dirs=$(find output/assets -maxdepth 1 -type d 2>/dev/null | wc -l)
    asset_dirs=$((asset_dirs - 1))  # Subtract 1 for the assets directory itself
    
    echo "📊 Generated:"
    echo "   - $html_count HTML pages"
    echo "   - $asset_dirs page asset directories"
    echo "   - Static files ready in: output/"
    
    # List the generated files
    echo ""
    echo "📂 Generated files:"
    ls -la output/
    
    if [ -d "output/assets" ]; then
        echo ""
        echo "🎨 Asset directories:"
        ls -la output/assets/
    fi
    
else
    echo "❌ Compilation failed!"
    exit 1
fi

echo ""
echo "🎉 Ready to deploy or serve locally!"
echo "   - Local static: python3 server.py"
echo "   - Local with API: python3 flask_server.py"
echo "   - Deploy: ./deploy.sh"