# Reverse Proxy Setup for Development Services

This document explains how reverse proxies are handled on gabrielpenman.com for exposing local development services through `/dev/*` paths.

## Current Architecture

All development services are exposed through Nginx reverse proxy using the `/dev/{port}` pattern:

- **Public access**: `https://gabrielpenman.com/dev/{port}/`
- **Backend**: `http://localhost:{port}/`

## Active Proxied Services

| Path | Port | Service | Auth Required |
|------|------|---------|---------------|
| `/dev/3005` | 3005 | Arbitrage Trading Dashboard | ✓ Yes |
| `/dev/5123` | 5123 | Depopper Research Playground | ✓ Yes |
| `/dev/8100` | 8100 | Minecraft Live Map (BlueMap) | No |
| `/dev/3000` | 3000 | geo-butler (Next.js) | No |
| `/dev/4000` | 4000 | Firebase Emulator UI | No |
| `/dev/5001` | 5001 | Firebase Cloud Functions | No |
| `/dev/8081` | 8081 | Firebase Firestore Emulator | No |
| `/dev/9099` | 9099 | Firebase Auth Emulator | No |

### Services with Authentication

Services containing sensitive information are protected with HTTP Basic Auth:
- **Username**: `gabriel`
- **Password**: `Lasshamster5!`
- **Password file**: `/etc/nginx/.htpasswd_dev`

## Adding a New Proxied Service

### Step 1: Add Nginx Configuration

Edit `/etc/nginx/sites-available/blog` and add the location block to **both** server blocks (HTTP and HTTPS).

#### Template for Public Services (No Auth):

```nginx
location /dev/YOUR_PORT {
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

#### Template for Protected Services (With Auth):

```nginx
location /dev/YOUR_PORT {
    auth_basic "Development Services";
    auth_basic_user_file /etc/nginx/.htpasswd_dev;

    proxy_pass http://localhost:YOUR_PORT/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upstream;
    proxy_set_header Connection "upgrade";
}
```

#### Special Cases:

**Large file uploads** (like Depopper Research):
```nginx
location /dev/5123 {
    auth_basic "Development Services";
    auth_basic_user_file /etc/nginx/.htpasswd_dev;
    client_max_body_size 50M;  # Increase upload limit

    # ... rest of proxy config
}
```

**IPv6-only services** (like some Java apps):
```nginx
location /dev/8100/ {
    proxy_pass http://[::1]:8100/;  # Use IPv6 localhost
    # ... rest of proxy config
}
```

### Step 2: Test and Reload Nginx

```bash
# Test configuration
echo '01022366' | sudo -S nginx -t

# Reload if successful
echo '01022366' | sudo -S systemctl reload nginx
```

### Step 3: Add to Homepage (Optional)

To make the service easily discoverable, add it to the "Reverse Proxy Ports" section on the homepage.

Edit `/home/gabriel/blog-new/compile.py` and find the "Reverse Proxy Ports" section:

```python
<div class="status-section">
    <h3>Reverse Proxy Ports</h3>
    <div class="status-item">
        <span>→</span>
        <a href="/dev/8100/" style="color: #0066cc; text-decoration: none;">Minecraft Live Map</a>
    </div>
    <div class="status-item">
        <span>→</span>
        <a href="/dev/3005/" style="color: #0066cc; text-decoration: none;">Arbitrage Trading Dashboard</a>
    </div>
    <div class="status-item">
        <span>→</span>
        <a href="/dev/5123/" style="color: #0066cc; text-decoration: none;">Depopper Research Playground</a>
    </div>
    <!-- ADD NEW SERVICE HERE -->
</div>
```

Then recompile:
```bash
cd /home/gabriel/blog-new
python3 compile.py
```

## Authentication Management

### Adding a New User

```bash
echo '01022366' | sudo -S htpasswd /etc/nginx/.htpasswd_dev newusername
```

### Changing Password for Existing User

```bash
echo '01022366' | sudo -S htpasswd /etc/nginx/.htpasswd_dev gabriel
```

### Viewing Current Users

```bash
echo '01022366' | sudo -S cat /etc/nginx/.htpasswd_dev
```

## Troubleshooting

### Service shows 401 Unauthorized
- **Cause**: Wrong username/password or missing auth file
- **Fix**: Check credentials are `gabriel` / `devaccess2024`

### Service shows 502 Bad Gateway
- **Cause**: Backend service not running
- **Fix**: Start the service on the specified port

### Service shows 404 Not Found
- **Cause**:
  - Service doesn't serve content at root path
  - FastAPI mounting issue (serving at `/ui` instead of `/`)
- **Fix**:
  - Check service logs
  - For FastAPI, mount static files at root: `app.mount("/", StaticFiles(...))`

### WebSocket connection fails
- **Cause**: Missing Upgrade headers
- **Fix**: Ensure nginx config includes:
  ```nginx
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  ```

### CSS/JS files not loading
- **Cause**: Service expects to be at root, not `/dev/port/` prefix
- **Fix**:
  - Some services need path rewriting (avoid if possible)
  - Better: Configure the service to handle base path

## Best Practices

1. **Always use trailing slash** in `proxy_pass` URLs: `http://localhost:5123/`
2. **Use auth for sensitive services**: Any service with user data, uploads, or admin functions
3. **Test locally first**: Use `curl http://localhost:{port}` before adding nginx config
4. **Document in this file**: Keep this list updated when adding new services
5. **Use standard port ranges**:
   - 3000-3999: Web UIs (Next.js, React, etc.)
   - 4000-4999: Development tools (Firebase emulators, etc.)
   - 5000-5999: APIs and backends (Flask, FastAPI, etc.)
   - 8000-8999: Special services (BlueMap, monitoring, etc.)
   - 9000-9999: Auth and security services

## Service Discovery

All proxied services are listed on the homepage at:
- https://gabrielpenman.com/ (scroll to "Reverse Proxy Ports" section)

This provides a centralized portal for accessing all development services.

## Migration Notes

### Old Patterns (Deprecated)

- ~~`/proxy/dynmap/`~~ - Now standardized to `/dev/8100/`
- ~~Individual blog posts for services~~ - Now use homepage "Reverse Proxy Ports" section
- ~~Path rewriting with nginx rewrite rules~~ - Now configure services to serve at root

### Why `/dev/*` Pattern?

- **Consistent**: All dev services use same path pattern
- **Discoverable**: Easy to remember and find
- **Isolated**: Clear separation from production blog content
- **Scalable**: Can add unlimited services without URL conflicts
