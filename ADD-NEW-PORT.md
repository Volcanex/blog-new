# How to Add a New Port to Your Server Portal

Quick guide for exposing new services through gabrielpenman.com/dev/{port}

## Step 1: Add to Nginx Config

Edit `/etc/nginx/sites-available/blog` and add this block in **both** server blocks (HTTP and HTTPS):

### Template for Most Services:
```nginx
# Your Service Name
location /dev/YOUR_PORT {
    proxy_pass http://localhost:YOUR_PORT;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Template for Services Needing Subpath Support (like web UIs with assets):
```nginx
# Your Service Name - with trailing slash for subpaths
location = /dev/YOUR_PORT {
    return 301 /dev/YOUR_PORT/;
}

location /dev/YOUR_PORT/ {
    proxy_pass http://localhost:YOUR_PORT/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Special Case: IPv6 Required (like Dynmap):
```nginx
# Service requiring IPv6
location = /dev/YOUR_PORT {
    return 301 /dev/YOUR_PORT/;
}

location /dev/YOUR_PORT/ {
    proxy_pass http://[::1]:YOUR_PORT/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## Step 2: Test and Reload Nginx

```bash
# Test config
echo 'YOUR_SUDO_PASSWORD' | sudo -S nginx -t

# Reload if successful
echo 'YOUR_SUDO_PASSWORD' | sudo -S systemctl reload nginx
```

## Step 3: (Optional) Create a Blog Post Redirect

If you want a nice URL like `/my-service` that redirects to `/dev/YOUR_PORT`:

### 3a. Create page directory:
```bash
mkdir -p /home/gabriel/blog-new/pages/my-service
```

### 3b. Create config.json:
```json
{
  "title": "My Service",
  "date": "2025-12-11",
  "description": "Quick access to my service",
  "categories": ["tools"]
}
```

### 3c. Create content.md:
```html
<meta http-equiv="refresh" content="0;url=/dev/YOUR_PORT/">
<html>
<body>
    <p>Redirecting to service...</p>
</body>
</html>
```

### 3d. Compile:
```bash
cd /home/gabriel/blog-new
python3 compile.py
```

## Quick Reference

### When to Use Each Template:

1. **Basic Template** - Most CLI/API services
2. **Trailing Slash Template** - Web UIs that serve assets (CSS/JS)
3. **IPv6 Template** - Services that only listen on IPv6

### Troubleshooting:

**Problem:** Blank page or 404
- **Solution:** Use the trailing slash template (assets can't load)

**Problem:** 400 Bad Request
- **Solution:** Try IPv6 `[::1]` instead of `localhost`

**Problem:** WebSocket not working
- **Solution:** Make sure you have the `Upgrade` and `Connection` headers

## Examples from Your Current Setup:

- `/dev/3000` - Next.js (basic)
- `/dev/8100` - Dynmap (IPv6 + trailing slash)
- `/dev/4000` - Firebase UI (trailing slash)
- `/dev/5001` - Cloud Functions (basic with timeout overrides)

## Current Ports in Use:

- 3000 - geo-butler (Next.js)
- 4000 - Firebase Emulator UI
- 5000 - blog-new Flask API
- 5001 - Cloud Functions
- 8081 - Firestore Emulator
- 8085 - Pub/Sub Emulator
- 8100 - Dynmap
- 9099 - Auth Emulator
