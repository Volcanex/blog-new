#!/bin/bash
# HTTPS/SSL setup script for GCP using Certbot and Let's Encrypt

set -e

echo "🔒 Setting up HTTPS/SSL certificates..."
echo "======================================"

# Check if domain is provided
if [ -z "$1" ]; then
    echo "❌ Error: Domain name required"
    echo "Usage: ./setup_https.sh your-domain.com"
    echo "Example: ./setup_https.sh myblog.example.com"
    exit 1
fi

DOMAIN="$1"
EMAIL="${LETSENCRYPT_EMAIL:-admin@$DOMAIN}"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
NGINX_CONFIG="$NGINX_AVAILABLE/$DOMAIN"

echo "🌍 Domain: $DOMAIN"
echo "📧 Email: $EMAIL"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root (use sudo)"
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
apt-get update
apt-get install -y nginx certbot python3-certbot-nginx ufw

# Stop any service running on port 80
echo "🛑 Stopping services on port 80..."
systemctl stop nginx 2>/dev/null || true
pkill -f "flask_server.py" 2>/dev/null || true
pkill -f "python.*80" 2>/dev/null || true

# Configure firewall
echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Create Nginx configuration
echo "⚙️  Creating Nginx configuration..."
cat > "$NGINX_CONFIG" << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # Flask app proxy
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        # Increase timeouts for API calls
        proxy_connect_timeout       60s;
        proxy_send_timeout          60s;
        proxy_read_timeout          60s;
    }
    
    # Static files (if served directly by Nginx)
    location /static/ {
        alias /home/gabriel/master/blog/output/;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF

# Enable the site
ln -sf "$NGINX_CONFIG" "$NGINX_ENABLED/$DOMAIN"
rm -f "$NGINX_ENABLED/default"

# Test Nginx configuration
nginx -t

# Start Nginx
systemctl start nginx
systemctl enable nginx

echo "✅ Nginx configured and started"

# Obtain SSL certificate
echo "🔐 Obtaining SSL certificate from Let's Encrypt..."
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL" --redirect

# Test certificate auto-renewal
echo "🔄 Testing certificate auto-renewal..."
certbot renew --dry-run

echo ""
echo "🎉 HTTPS setup completed successfully!"
echo "=================================="
echo "✅ SSL certificate installed for: $DOMAIN"
echo "✅ Nginx reverse proxy configured"
echo "✅ Automatic HTTP -> HTTPS redirect enabled"
echo "✅ Auto-renewal configured"
echo ""
echo "📍 Your site is now available at:"
echo "   🔒 https://$DOMAIN"
echo "   🔒 https://$DOMAIN/api/health"
echo ""
echo "⚠️  Important: Update your Flask server configuration!"
echo "   1. Change Flask to run on port 5000 (internal only)"
echo "   2. Start your Flask server: ./deploy.sh"
echo ""
echo "🔧 Management commands:"
echo "   Check certificate: certbot certificates"
echo "   Renew certificate: certbot renew"
echo "   Nginx status: systemctl status nginx"
echo "   Nginx reload: systemctl reload nginx"