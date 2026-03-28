# Artist Sites System

A shared artist portfolio system built into blog-new. Each artist gets their own domain, admin dashboard, and customizable pages.

## Architecture

- **Single Flask instance** serving multiple artist domains
- **Domain-based routing** - each artist domain maps to their pages
- **Shared admin endpoints** for common functionality
- **Per-artist authentication** with simple token-based auth
- **Optional custom APIs** per artist

## Directory Structure

```
pages/artists/
  _shared/                      # Shared utilities (not a page)
    admin_api.py                # Shared admin endpoints
    auth.py                     # Authentication utilities
    dashboard.html              # Admin dashboard UI

  example-artist/               # Artist slug (becomes part of URL path)
    config.json                 # Artist configuration & auth token
    home/                       # Homepage (shown at /)
      config.json
      content.md
    gallery/                    # Subpage (shown at /gallery)
      config.json
      content.md
    assets/                     # Shared assets for all pages
      logo.png
```

## How It Works

### 1. Domain Routing

Nginx proxies artist domains to the same Flask server (port 5000):

```nginx
server {
    server_name artist1.com;
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;  # Flask checks this header
    }
}
```

Flask checks the `Host` header and serves the correct artist's content:
- `artist1.com/` → `pages/artists/artist1/home/`
- `artist1.com/gallery` → `pages/artists/artist1/gallery/`

### 2. Admin Dashboard

All artists access the same dashboard at: `/api/sandbox/dashboard`

Login with:
- **Artist Slug**: `example-artist`
- **Admin Token**: From `config.json`

Dashboard features:
- List all pages
- Edit HTML/CSS content
- Upload files/images
- Create new pages
- Delete pages

### 3. Shared Admin API

Available at `/api/sandbox/*`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard` | GET | Admin dashboard UI |
| `/list-pages` | GET | List all pages for artist |
| `/get-page-content` | GET | Get page content & config |
| `/edit-page` | POST | Update page content/config |
| `/create-page` | POST | Create new page |
| `/delete-page` | POST | Delete a page |
| `/upload-file` | POST | Upload image/file |
| `/artist-info` | GET | Get artist config |

All endpoints require headers:
- `X-Artist-Slug`: The artist's slug
- `X-Admin-Token`: The artist's token from config.json

### 4. Authentication

Simple token-based auth:
1. Each artist has an `admin_token` in their `config.json`
2. Admin API checks this token via headers
3. Fallback to `DEV_ADMIN_TOKEN` env var for super admin

## Creating a New Artist Site

### Step 1: Create Directory Structure

```bash
cd /home/gabriel/blog-new/pages/artists
mkdir -p new-artist/home
```

### Step 2: Create Artist Config

`pages/artists/new-artist/config.json`:
```json
{
    "name": "Artist Name",
    "slug": "new-artist",
    "domain": "newartist.com",
    "admin_token": "generate-secure-token-here",
    "description": "Artist bio",
    "contact_email": "artist@example.com"
}
```

### Step 3: Create Homepage

`pages/artists/new-artist/home/config.json`:
```json
{
    "title": "Home",
    "slug": "home",
    "description": "Artist homepage",
    "categories": ["portfolio"]
}
```

`pages/artists/new-artist/home/content.md`:
```html
<style>
body {
    font-family: sans-serif;
    margin: 0;
    padding: 20px;
}
</style>

<html>
<h1>Welcome</h1>
<p>This is the homepage.</p>
</html>
```

### Step 4: Compile & Deploy

```bash
cd /home/gabriel/blog-new
python3 compile.py  # Generates static HTML
sudo systemctl restart blog-server
```

### Step 5: Configure Nginx

Add to `/etc/nginx/sites-available/blog`:

```nginx
server {
    server_name newartist.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static assets (optional optimization)
    location /assets/ {
        alias /home/gabriel/blog-new/output/assets/;
    }
}
```

Restart Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: DNS

Point `newartist.com` to your server's IP address.

## Admin Usage

### Accessing the Dashboard

1. Go to `https://newartist.com/api/sandbox/dashboard`
2. Enter artist slug: `new-artist`
3. Enter admin token from config.json
4. Start editing!

### Uploading Images

1. Select a page in the dashboard
2. Use the "Upload Files" section
3. Choose an image file
4. Copy the returned URL to use in your HTML

Example:
```html
<img src="/assets/new-artist/gallery/photo1.jpg" alt="Photo">
```

### Creating Pages

1. Click "Create New Page"
2. Enter slug: `about`
3. Enter title: `About Me`
4. Edit the content in the dashboard

Page will be available at: `https://newartist.com/about`

## Custom Artist API (Optional)

If an artist needs custom functionality, create `api.py`:

`pages/artists/new-artist/api.py`:
```python
from flask import Blueprint, jsonify

bp = Blueprint('new_artist', __name__, url_prefix='/api/new-artist')

@bp.route('/custom-endpoint')
def custom_endpoint():
    return jsonify({'message': 'Custom functionality'})
```

This will be auto-registered by Flask like regular blog pages.

## Shared Functionality

### Database

Uses the same shared database system:

```python
from shared.database import get_db

# Store artist-specific data
get_db().set_page_data('artists/new-artist', 'settings', {...})

# Retrieve it
settings = get_db().get_page_data('artists/new-artist', 'settings', {})
```

### WebSockets (Optional)

If needed, add to `api.py`:

```python
def register_websocket_handlers(socketio):
    @socketio.on('custom_event')
    def handle_event(data):
        # Handle WebSocket event
        pass
```

## Security Notes

1. **Token Security**: Generate strong tokens for `admin_token`
2. **HTTPS**: Always use HTTPS in production
3. **File Uploads**: Only allowed extensions are validated
4. **No SQL Injection**: Uses file-based storage (JSON)

## Troubleshooting

### Artist site returns 404

1. Check `pages/artists/{slug}/config.json` exists
2. Verify `domain` field matches nginx config
3. Run `python3 compile.py` to regenerate static files
4. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Admin dashboard won't login

1. Verify artist slug is correct (lowercase, hyphens only)
2. Check token in `config.json`
3. Look for Flask errors: `sudo journalctl -u blog-server -f`

### Changes not showing up

1. Save in dashboard (triggers auto-compile)
2. If that fails, manually run: `python3 compile.py`
3. Clear browser cache
4. Check Flask is running: `sudo systemctl status blog-server`

## Example Sites

- **example-artist** - Demo site with home and gallery pages
- Accessible at domain configured in `config.json`

## Technical Details

### Compilation

The `compile.py` script:
1. Recursively finds all pages (including nested in `artists/`)
2. Generates static HTML with proper paths
3. Outputs to: `output/artists/{artist-slug}/{page-slug}/index.html`

### Routing Priority

1. Artist domain match → serve artist pages
2. Regular blog domain → serve blog pages
3. API routes always handled by blueprints

### Performance

- Single Flask process handles all artists (low traffic sites)
- Nginx serves static assets directly (if configured)
- Compile once, serve many times
