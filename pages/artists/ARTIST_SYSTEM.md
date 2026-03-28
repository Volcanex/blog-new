# Artist Sites System — Technical Reference

This document explains how artist sites work within the blog-new platform,
how to create new ones, and how to connect custom domains.

## Architecture Overview

```
blog-new/
  flask_server.py        # Main Flask app (port 5000)
  compile.py             # Static site compiler
  pages/
    artists/
      _shared/
        dashboard.html   # Shared admin dashboard (all artists)
        admin_api.py     # Flask Blueprint for admin API
        auth.py          # Token-based auth
      whitethornapple/   # Example artist
        config.json      # Artist-level config (name, domain, token)
        home/
          config.json    # Page config (title, slug, etc.)
          content.md     # Page content (<style>...</style>\n<html>...</html>)
        gallery/
          config.json
          content.md
        assets/          # Shared assets (images, fonts, gifs)
          images/
          fonts/
          gifs/
        widgets/         # Custom dashboard widgets (JS files)
          add-to-gallery.js
  output/
    artists/
      whitethornapple/
        home/index.html    # Compiled static HTML
        gallery/index.html
        assets/            # Copied from pages/ during compile
        index.html         # Auto-generated redirect to home/
```

## Content Format (content.md)

Each page's `content.md` uses a simple format:

```
<style>
  body { background: #000; color: #fff; }
  /* CSS here */
</style>

<html>
  <h1>Page Title</h1>
  <p>HTML content here</p>
</html>
```

The compiler extracts the CSS and HTML, wraps them in a full HTML document.

## Asset Paths

All asset references in content.md use relative paths from the page directory:
```
../assets/images/photo.jpg
../assets/fonts/MyFont.ttf
../assets/gifs/animation.gif
```

This works because pages are served at `/artists/{slug}/{page}/` — so `../assets/`
resolves to `/artists/{slug}/assets/`.

## Creating a New Artist Site

### 1. Create the directory structure

```bash
mkdir -p pages/artists/myartist/{home,assets}
```

### 2. Create artist config.json

```json
{
    "name": "Artist Name",
    "slug": "myartist",
    "domain": "myartist.com",
    "admin_token": "a-secure-token-here",
    "description": "What the artist does",
    "contact_email": "artist@email.com"
}
```

Place this at `pages/artists/myartist/config.json`.

### 3. Create a home page

```bash
mkdir pages/artists/myartist/home
```

`pages/artists/myartist/home/config.json`:
```json
{
    "title": "Home",
    "slug": "home",
    "description": "Homepage"
}
```

`pages/artists/myartist/home/content.md`:
```
<style>
body { background: #1a1a2e; color: #e0e0e0; font-family: sans-serif; }
</style>

<html>
<h1>Welcome</h1>
<p>This is the homepage.</p>
</html>
```

### 4. Add assets

Put images, fonts, etc. in `pages/artists/myartist/assets/`.
Organize with subdirs if needed: `images/`, `fonts/`, `gifs/`.

### 5. Compile and restart

```bash
cd /home/gabriel/blog-new
python3 compile.py
sudo systemctl restart blog-server
```

### 6. Access the site

Preview URL (no domain needed):
```
https://gabrielpenman.com/artists/myartist/
```

Admin dashboard:
```
https://gabrielpenman.com/api/sandbox/dashboard
```
Login with slug + admin_token from config.json.

Dev admin token (bypasses per-artist tokens): configured in auth.py.

## Custom Widgets

Widgets are per-artist JS files in `pages/artists/{slug}/widgets/`.
They appear as extra tabs in the dashboard.

### Widget API

Each widget JS file receives a `ctx` object:

```javascript
(function(ctx) {
    // ctx.container    — DOM element to render into
    // ctx.name         — widget name (from filename)
    // ctx.artistSlug   — current artist slug
    // ctx.token        — auth token
    // ctx.apiFetch     — authenticated fetch wrapper
    // ctx.toast(msg, type)  — show notification
    // ctx.assetList    — array of asset objects [{filename, path, url, is_image, size}]
    // ctx.pages        — array of page objects [{slug, title, config}]
    // ctx.getCss() / ctx.setCss(v)   — get/set CSS editor
    // ctx.getHtml() / ctx.setHtml(v) — get/set HTML editor
    // ctx.getPageContent(slug)       — fetch a page's content
    // ctx.savePage(slug, content, config)  — save a page
    // ctx.loadAssets()               — refresh asset list
    // ctx.parseContent(raw)          — split content.md into {css, html}
    // ctx.schedulePreview(delay)     — trigger preview update
    // ctx.setUnsaved(bool)           — mark unsaved changes
    // ctx.showModal(id) / ctx.hideModal(id)

    ctx.container.innerHTML = '<h3>My Widget</h3><p>Hello!</p>';
})(ctx);
```

### Creating a widget

1. Create a `.js` file in `pages/artists/{slug}/widgets/`
2. The filename becomes the tab name (dashes/underscores become spaces, title-cased)
3. Restart blog-server: `sudo systemctl restart blog-server`

## Connecting a Custom Domain

### DNS Setup

At your domain registrar, add:

| Type  | Name | Value                                          |
|-------|------|-------------------------------------------------|
| A     | @    | 151.226.233.153                                 |
| AAAA  | @    | 2a06:5902:39c1:9900:92a9:f065:784e:2260         |
| CNAME | www  | yourdomain.com                                  |

### Nginx Config

Create `/etc/nginx/sites-available/yourdomain.com`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;

    root /home/gabriel/blog-new/output;

    # Artist assets with caching
    location /artists/yourslug/assets/ {
        alias /home/gabriel/blog-new/output/artists/yourslug/assets/;
        expires 24h;
        add_header Cache-Control "public, max-age=86400";
    }

    # Rewrite domain paths to artist preview paths
    location / {
        rewrite ^/$ /artists/yourslug/home/ last;
        rewrite ^/([^/]+)/?$ /artists/yourslug/$1/ last;
        rewrite ^/([^/]+)/(.*)$ /artists/yourslug/$1/$2 last;
    }

    location /artists/ {
        try_files $uri $uri/ @api;
        expires 1h;
    }

    location @api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot auto-updates the nginx config for HTTPS.

### Verify

The Domain tab in the admin dashboard shows live status for DNS, Nginx, and SSL.
It also generates the exact commands needed for your specific artist.

## Admin API Endpoints

All endpoints require `X-Artist-Slug` and `X-Admin-Token` headers.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/sandbox/dashboard` | GET | Serve dashboard HTML |
| `/api/sandbox/list-pages` | GET | List artist's pages |
| `/api/sandbox/get-page-content?page_slug=X` | GET | Get page content + config |
| `/api/sandbox/edit-page` | POST | Update page content/config |
| `/api/sandbox/create-page` | POST | Create new page |
| `/api/sandbox/delete-page` | POST | Delete a page |
| `/api/sandbox/upload-file` | POST | Upload asset file |
| `/api/sandbox/list-assets` | GET | List all assets |
| `/api/sandbox/artist-info` | GET | Get artist config |
| `/api/sandbox/list-widgets` | GET | List custom widgets |
| `/api/sandbox/get-widget?filename=X` | GET | Get widget JS |
| `/api/sandbox/check-domain` | GET | Check domain DNS/nginx/SSL status |

## Key Files

- `flask_server.py` — Main Flask server, domain-based routing via Host header
- `compile.py` — Builds static HTML from content.md, copies assets, generates indexes
- `pages/artists/_shared/dashboard.html` — Full admin dashboard (single HTML file)
- `pages/artists/_shared/admin_api.py` — All admin API endpoints
- `pages/artists/_shared/auth.py` — Token auth (per-artist + dev fallback)
- `/etc/nginx/sites-available/blog` — Main nginx config
- systemd service: `blog-server` (restart with `sudo systemctl restart blog-server`)

## Compilation

`compile.py` handles:
1. Compiling all content.md files to output HTML
2. Copying static assets (`copy_artist_assets()`)
3. Generating root index.html redirects for each artist (`generate_artist_root_indexes()`)
4. Generating the main site homepage

Run: `cd /home/gabriel/blog-new && python3 compile.py`

Saving pages via the dashboard auto-triggers compilation.
