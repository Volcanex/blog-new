# Artist Site System

How to create, manage, and deploy artist websites on the blog-new platform.

## Architecture

```
pages/artists/
  _shared/
    admin_api.py    # Flask blueprint — all API endpoints
    auth.py         # Token-based authentication
    dashboard.html  # Shared admin dashboard (single file, inline CSS/JS)
  {artist-slug}/
    config.json     # Artist config (name, slug, domain, admin_token, etc.)
    api.py          # Optional — artist-level Flask Blueprint (auto-discovered)
    bookings.json   # Booking enquiries (auto-created when first enquiry arrives)
    home/
      content.md    # Format: <style>...</style>\n<html>...</html>
      config.json   # Page config (title, description, categories)
    gallery/
      content.md
      config.json
    {page-slug}/
      content.md
      config.json
    assets/
      images/       # All image files
      fonts/        # Font files (woff2, ttf, etc.)
    widgets/        # Custom dashboard widgets (JS files)
      manage-bookings.js
```

## Creating a New Artist Site

### 1. Create the directory structure

```bash
SLUG=myartist
mkdir -p pages/artists/$SLUG/{home,about,gallery,assets/images,assets/fonts,widgets}
```

### 2. Create config.json

```json
{
    "name": "Artist Name",
    "slug": "myartist",
    "domain": "",
    "admin_token": "choose-a-token",
    "description": "Short description of the artist",
    "contact_email": "artist@email.com"
}
```

The `admin_token` is what the artist uses to log into their dashboard. There's also a `DEV_ADMIN_TOKEN` fallback in auth.py for dev access.

### 3. Create pages

Each page needs a `content.md` in the format:

```
<style>
/* CSS here */
</style>
<html>
<!-- HTML here -->
</html>
```

And a `config.json`:

```json
{
    "title": "Page Title",
    "slug": "artists/myartist/pagename",
    "description": "Page description",
    "categories": ["category"]
}
```

### 4. Add assets

Put images in `pages/artists/$SLUG/assets/images/` and fonts in `assets/fonts/`.

Reference them in content.md with relative paths: `../assets/images/photo.jpg`

This works in both preview mode (`/artists/slug/page/`) and domain mode (`/page/`).

### 5. Compile

```bash
cd /home/gabriel/blog-new
python3 compile.py
```

This generates static HTML in `output/artists/$SLUG/` and copies assets.

### 6. Restart the server

```bash
sudo systemctl restart blog-server
```

Needed for: new API endpoints, new artist configs, widget loading.

## Accessing the Dashboard

URL: `https://gabrielpenman.com/api/sandbox/dashboard`

Login with:
- Artist slug (e.g., `leahmclaine`)
- Admin token (from config.json, or the DEV_ADMIN_TOKEN)

Dashboard features:
- **AI Edit** — Gemini-powered code editor with function calling
- **Manual Edit** — Split CSS/HTML editors with live preview
- **Config** — Page metadata, custom fields with asset picker
- **Assets** — Upload/manage files, drag & drop
- **History** — Snapshots (localStorage), save/restore
- **Custom Domain** — DNS/SSL status checker
- **Custom Widgets** — Per-artist JS widgets loaded as extra tabs

## Widget System

Widgets are JS files in `pages/artists/{slug}/widgets/`. Each gets loaded as a new tab in the dashboard.

Widget JS receives a `ctx` object with:

```javascript
ctx.container       // DOM element to render into
ctx.name            // Widget name (from filename)
ctx.artistSlug      // Current artist slug
ctx.token           // Auth token
ctx.apiFetch(url, opts)  // Authenticated fetch wrapper
ctx.toast(msg, type)     // Show toast notification
ctx.assetList       // Array of {filename, path, url, size, is_image}
ctx.pages           // Array of page objects
ctx.getPageContent(slug) // Fetch a page's content
ctx.savePage(slug, content, config) // Save a page
ctx.getCss() / ctx.setCss(v)   // Get/set CSS editor
ctx.getHtml() / ctx.setHtml(v) // Get/set HTML editor
ctx.loadAssets()     // Refresh asset list
ctx.parseContent(raw)    // Parse content.md format
ctx.schedulePreview(delay)   // Trigger preview update
ctx.setUnsaved(bool)     // Set unsaved indicator
```

Example widget pattern:

```javascript
(function(ctx) {
    const container = ctx.container;
    container.style.cssText = 'display:flex;flex-direction:column;flex:1;min-height:0;padding:0;overflow:hidden;';
    container.innerHTML = `
        <div style="padding:20px 20px 12px;flex-shrink:0;">
            <h3 style="margin:0;">Widget Title</h3>
        </div>
        <div style="flex:1;overflow-y:auto;padding:0 20px;">
            <!-- scrollable content -->
        </div>
        <div style="padding:12px 20px;border-top:1px solid var(--border);background:var(--bg2);flex-shrink:0;">
            <!-- sticky footer actions -->
        </div>
    `;
    // widget logic...
})(ctx);
```

## Preview Routes

All artist sites are accessible at: `https://gabrielpenman.com/artists/{slug}/`

Pages: `https://gabrielpenman.com/artists/{slug}/{page}/`

This works before any custom domain is configured.

## Setting Up a Custom Domain

### 1. DNS

Add an A record for the domain pointing to the server IP. The dashboard's "Custom Domain" tab shows the IP and checks DNS automatically.

### 2. Set the domain in config.json

```json
{
    "domain": "artistdomain.com"
}
```

### 3. Nginx configuration

Add a server block to `/etc/nginx/sites-available/blog` (or create a new file):

```nginx
server {
    listen 80;
    server_name artistdomain.com www.artistdomain.com;
    root /home/gabriel/blog-new/output/artists/{slug};

    location /assets/ {
        alias /home/gabriel/blog-new/output/artists/{slug}/assets/;
        expires 24h;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ @api;
    }

    location @api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. SSL with Let's Encrypt

```bash
sudo certbot --nginx -d artistdomain.com -d www.artistdomain.com
```

### 5. Restart Nginx

```bash
sudo nginx -t && sudo systemctl reload nginx
```

The Flask server also checks the Host header for domain-based routing (see `_get_artist_by_domain()` in `flask_server.py`).

## Feature System

Artists opt into features via `config.json`:

```json
{ "features": ["bookings"] }
```

Features live in `pages/artists/_shared/features/` and each exports a `create_blueprint(artist_slug)` function. At startup, `flask_server.py` reads each artist's config and registers the relevant feature Blueprints scoped to that artist.

This means artists only get the endpoints they actually use — no phantom routes.

### Available Features

#### bookings

Per-artist booking/enquiry system.

Opt in: `"features": ["bookings"]`

Public endpoint (no auth): `POST /api/artists/{slug}/bookings/submit`

```json
{
    "name": "Client Name",
    "email": "client@email.com",
    "service": "Portraiture",
    "subject": "Project description",
    "message": "Full message..."
}
```

Enquiries are stored in `pages/artists/{slug}/bookings.json` and managed via the "Manage Bookings" dashboard widget.

Auth-required endpoints:
- `GET /api/artists/{slug}/bookings/list`
- `POST /api/artists/{slug}/bookings/update` — `{id, status, notes}`
- `POST /api/artists/{slug}/bookings/delete` — `{id}`

### Adding a New Feature

1. Create `pages/artists/_shared/features/myfeature.py`
2. Export `create_blueprint(artist_slug)` returning a Flask Blueprint
3. Optionally export `ENDPOINT_DESCRIPTIONS` dict for the API tab
4. Add `"myfeature"` to the artist's `config.json` features list
5. Restart the server

## Per-Artist Backend (api.py)

Artists can have their own backend by adding an `api.py` to their directory (`pages/artists/{slug}/api.py`). It works identically to blog page backends — export a Flask Blueprint named `bp`, and it gets auto-discovered and registered at server startup.

### Example

```python
# pages/artists/leahmclaine/api.py
from flask import Blueprint, jsonify, request
from shared.database import get_db

bp = Blueprint('artist_leahmclaine', __name__, url_prefix='/api/artists/leahmclaine')

@bp.route('/prints')
def list_prints():
    db = get_db()
    prints = db.get_page_data('artists-leahmclaine', 'prints', [])
    return jsonify(prints)
```

### Convention

- Blueprint name: `artist_{slug}` (e.g. `artist_leahmclaine`)
- URL prefix: `/api/artists/{slug}` (e.g. `/api/artists/leahmclaine`)
- Data namespace: `artists-{slug}` (e.g. `data/artists-leahmclaine/`)
- No changes needed to flask_server.py or compile.py — just drop in the file and restart

This is separate from the shared `admin_api.py` (dashboard/editing/bookings). Use this for artist-specific features like print shops, mailing lists, custom forms, etc.

## Current Artist Sites

### whitethornapple (Maria Slaughter)
- Domain: whitethornapple.com (pending setup)
- Style: Gothic dark aesthetic, tiled backgrounds, custom fonts
- Pages: home, gallery, music
- Custom widget: add-to-gallery (append images to gallery page)
- Token: adele

### leahmclaine (Leah Mclaine)
- Domain: TBD
- Style: Minimal warm cream, muted olive accent, analogue photography aesthetic
- Pages: home, about, gallery, bookings, + 6 works + 2 Having Had Faith + 3 exhibition/press
- Custom widget: manage-bookings
- Token: leah

## Key Files

- `flask_server.py` — Main Flask app, domain routing, static serving
- `compile.py` — Static site compiler, processes content.md -> HTML
- `pages/artists/_shared/admin_api.py` — All API endpoints (Blueprint)
- `pages/artists/_shared/auth.py` — Token authentication
- `pages/artists/_shared/dashboard.html` — Shared dashboard (1200+ lines)
- `/etc/nginx/sites-available/blog` — Nginx config
- `systemd service: blog-server` — Flask server service
