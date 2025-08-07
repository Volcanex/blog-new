#!/bin/bash
# Full deployment script that compiles and deploys the blog
# This script calls both compile.sh and deploy.sh in sequence

set -e  # Exit on any error

echo "🚀 Full Blog Deployment"
echo "======================="
echo "This will compile all pages and deploy the blog with APIs"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Compile the blog
echo "🔧 STEP 1: Compiling blog..."
echo "----------------------------"
if [ -f "compile.sh" ]; then
    chmod +x compile.sh
    ./compile.sh
    
    if [ $? -eq 0 ]; then
        echo "✅ Compilation successful!"
    else
        echo "❌ Compilation failed!"
        exit 1
    fi
else
    echo "❌ Error: compile.sh not found"
    exit 1
fi

echo ""

# Step 2: Deploy the blog
echo "🚀 STEP 2: Deploying blog..."
echo "-----------------------------"
if [ -f "deploy.sh" ]; then
    chmod +x deploy.sh
    ./deploy.sh
    
    if [ $? -eq 0 ]; then
        echo "✅ Deployment successful!"
    else
        echo "❌ Deployment failed!"
        exit 1
    fi
else
    echo "❌ Error: deploy.sh not found"
    exit 1
fi

echo ""
echo "🎉 FULL DEPLOYMENT COMPLETE!"
echo "============================"

# Show final summary
if [ -d "output" ]; then
    html_count=$(find output -name "*.html" | wc -l)
    asset_dirs=$(find output/assets -maxdepth 1 -type d 2>/dev/null | wc -l || echo "1")
    asset_dirs=$((asset_dirs - 1))  # Subtract 1 for the assets directory itself
    
    echo "📊 Final Status:"
    echo "   ✅ $html_count HTML pages compiled"
    echo "   ✅ $asset_dirs pages with assets"
    echo "   ✅ Flask API server running"
    echo "   ✅ Static files deployed"
fi

echo ""
echo "🌐 Your blog is now live at:"
echo "   🏠 Homepage: http://localhost:5000/"
echo "   🔌 API: http://localhost:5000/api/health"
echo ""
echo "📝 Management:"
echo "   📋 View logs: tail -f logs/flask_server.log"
echo "   🔄 Redeploy: ./full-deploy.sh"
echo "   🛑 Stop server: kill \$(cat flask_server.pid)"
echo ""
echo "✨ Happy blogging!"