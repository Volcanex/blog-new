#!/bin/bash
# Setup virtual environment for the blog
# Run this once before using the deployment scripts

set -e  # Exit on any error

VENV_DIR="venv"

echo "🐍 Setting up Python virtual environment..."
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

# Check if venv module is available
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ Error: python3-venv is not installed"
    echo "   Install it with: sudo apt install python3-venv"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment already exists at: $VENV_DIR"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "📝 Using existing virtual environment"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "   ✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "   ✅ Dependencies installed"
else
    echo "⚠️  No requirements.txt found"
fi

# Show installed packages
echo ""
echo "📋 Installed packages:"
pip list

echo ""
echo "🎉 Virtual environment setup complete!"
echo "======================================"
echo "📁 Virtual environment: $VENV_DIR/"
echo "🐍 Python executable: $VENV_DIR/bin/python"
echo "📦 Pip executable: $VENV_DIR/bin/pip"
echo ""
echo "🚀 You can now run:"
echo "   ./full-deploy.sh    # Full deployment"
echo "   ./compile.sh        # Just compile"
echo "   ./deploy.sh         # Just deploy"
echo ""
echo "💡 To manually activate:"
echo "   source $VENV_DIR/bin/activate"