#!/bin/bash
# Server setup script for Adze Studio
# Run this once on a new server to configure system-level dependencies.
# Everything else lives in the git repo.

set -e

echo "=== Adze Studio Server Setup ==="
echo ""

# Detect current user
ADZE_USER="${ADZE_USER:-$(whoami)}"
echo "Setting up for user: $ADZE_USER"

# Check for required system packages
echo ""
echo "Checking dependencies..."
for cmd in nginx certbot python3 node; do
    if command -v $cmd &>/dev/null; then
        echo "  ✓ $cmd found: $(command -v $cmd)"
    else
        echo "  ✗ $cmd NOT FOUND"
        MISSING=1
    fi
done

if [ "$MISSING" = "1" ]; then
    echo ""
    echo "Install missing packages:"
    echo "  sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx python3 python3-venv"
    echo "  # For node: https://nodejs.org/ or use nvm"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
fi

# Set up sudoers rule for passwordless nginx/certbot management
echo ""
echo "Setting up sudoers rule for domain management..."
SUDOERS_FILE="/etc/sudoers.d/adze"

SUDOERS_CONTENT="# Adze Studio - allow $ADZE_USER to manage nginx and certbot for domain setup
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/sbin/nginx
$ADZE_USER ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx
$ADZE_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/bin/certbot
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/bin/cp /tmp/tmp*.conf /etc/nginx/sites-available/*
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/bin/ln -s /etc/nginx/sites-available/* /etc/nginx/sites-enabled/*
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/bin/rm -f /etc/nginx/sites-enabled/*
$ADZE_USER ALL=(ALL) NOPASSWD: /usr/bin/rm -f /etc/nginx/sites-available/*"

echo "$SUDOERS_CONTENT" | sudo tee "$SUDOERS_FILE" > /dev/null
sudo chmod 440 "$SUDOERS_FILE"
sudo visudo -c || { echo "ERROR: sudoers validation failed!"; sudo rm -f "$SUDOERS_FILE"; exit 1; }
echo "  ✓ Sudoers rule created at $SUDOERS_FILE"

# Set up Python venv
echo ""
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi
source venv/bin/activate
pip install -r requirements.txt --quiet
echo "  ✓ Dependencies installed"

# Test
echo ""
echo "Testing passwordless sudo..."
if sudo nginx -t 2>&1 | grep -q "syntax is ok"; then
    echo "  ✓ Passwordless nginx access works"
else
    echo "  ✗ Passwordless nginx access failed"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To deploy:"
echo "  ./full-deploy.sh"
echo ""
echo "Dashboard will be at:"
echo "  https://yourdomain.com/api/adze/dashboard"
echo ""
