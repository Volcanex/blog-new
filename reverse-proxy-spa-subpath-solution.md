# Reverse Proxying SPAs on Subpaths: The PufferPanel Solution

## The Problem

Modern Single Page Applications (SPAs) built with frameworks like Vue.js, React, and Angular are designed to run at the root path (`/`) of a domain. When you try to reverse proxy them to a subpath like `/dev/8677/`, they break because:

1. **Hardcoded asset paths** - The compiled JavaScript builds paths like `/js/app.js` instead of `/dev/8677/js/app.js`
2. **Client-side routing** - The router navigates to `/login` instead of `/dev/8677/login`
3. **API calls** - Requests go to `/api/config` instead of `/dev/8677/api/config`

This affects PufferPanel, Pterodactyl, MCSManager, Crafty Controller, and most modern web panels.

## The Solution

We used a multi-layered approach combining nginx routing tricks and HTML injection:

### 1. **Direct Asset Routing** (Catch Missing Prefixes)

Since the blog doesn't use `/js/`, `/css/`, `/fonts/`, `/img/`, or `/theme/` at root level, we can safely proxy these to PufferPanel:

```nginx
# Catch PufferPanel asset requests without /dev/8677/ prefix
location ~ ^/(js|css|fonts|img|theme)/ {
    proxy_pass http://localhost:8677;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location ~ ^/(manifest\.json|service-worker.*\.js|favicon\..+|apple-touch-icon\..+)$ {
    proxy_pass http://localhost:8677;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2. **Internal Route Handling** (SPA Routes)

Catch SPA internal routes like `/errors/404`, `/auth/`, `/login/`:

```nginx
location ~ ^/(errors|auth|login|register|install)/ {
    proxy_pass http://localhost:8677;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 3. **Smart API Routing** (Referer-Based)

The `/api/` path conflicts with the blog's Flask API. Use referer checking:

```nginx
location /api/ {
    # Route to PufferPanel if request came from /dev/8677/
    set $backend "http://127.0.0.1:5000";
    if ($http_referer ~ "/dev/8677") {
        set $backend "http://localhost:8677";
    }
    proxy_pass $backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### 4. **HTML Injection** (The Magic Fix!)

Inject a `<base>` tag and router interception script into the HTML:

```nginx
location /dev/8677/ {
    auth_basic "Development Services";
    auth_basic_user_file /etc/nginx/.htpasswd_dev;
    proxy_pass http://localhost:8677/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Accept-Encoding "";

    # Inject base tag and router fix
    sub_filter_once off;
    sub_filter_types text/html;
    sub_filter '<head>' '<head><base href="/dev/8677/"><script>(function(){const basePath="/dev/8677";window.__pufferBasePath=basePath;const originalPushState=history.pushState;const originalReplaceState=history.replaceState;history.pushState=function(state,title,url){if(url&&typeof url==="string"&&!url.startsWith(basePath)&&!url.startsWith("http")&&url.startsWith("/")){url=basePath+url}return originalPushState.call(this,state,title,url)};history.replaceState=function(state,title,url){if(url&&typeof url==="string"&&!url.startsWith(basePath)&&!url.startsWith("http")&&url.startsWith("/")){url=basePath+url}return originalReplaceState.call(this,state,title,url)};if(window.location.pathname.startsWith(basePath)){history.replaceState(null,"",basePath+"/")}})();</script>';
}
```

### 5. **Manifest Exception** (No Auth for PWA)

The manifest.json needs to be accessible without auth for PWA features:

```nginx
location = /dev/8677/manifest.json {
    auth_basic off;
    proxy_pass http://localhost:8677/manifest.json;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## How It Works

### The `<base>` Tag
The `<base href="/dev/8677/">` tag is an HTML standard that tells the browser to resolve all relative URLs from this base path. This is what many SPAs check for when determining their base URL.

### Router Interception
The injected JavaScript intercepts `history.pushState()` and `history.replaceState()` - the methods Vue Router uses for navigation. When the router tries to navigate to `/login`, our script rewrites it to `/dev/8677/login`.

### Direct Asset Proxying
Since JavaScript builds asset paths at compile time, we catch requests like `/js/chunk-xxx.js` at the nginx level and proxy them directly to PufferPanel.

## Docker Setup

PufferPanel container setup:

```bash
docker create --name pufferpanel \
    -p 8677:8080 -p 5657:5657 \
    -v pufferpanel-config:/etc/pufferpanel \
    -v /var/lib/pufferpanel:/var/lib/pufferpanel:z \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --restart=on-failure \
    pufferpanel/pufferpanel:latest

docker start pufferpanel
```

Access at: `https://gabrielpenman.com/dev/8677/`

## Why This Worked When sub_filter Alone Didn't

Initially, we tried using only `sub_filter` to rewrite paths in the HTML/JS. This failed because:

1. **Runtime path building** - Vue Router builds paths in JavaScript at runtime, after the HTML is already loaded
2. **Dynamic imports** - Webpack's code splitting creates dynamic import paths that can't be caught by string replacement
3. **Service worker scope** - The service worker tried to register for `/` scope instead of `/dev/8677/`

The `<base>` tag solves this by telling the browser itself (not just the app) where to resolve paths from.

## Lessons Learned

1. **The `<base>` tag is powerful** - Most SPAs will respect it for routing
2. **Client-side routing needs runtime interception** - You can't just rewrite the HTML
3. **Multiple layers of defense** - Asset routing + API routing + HTML injection + base tag
4. **Not all paths can be rewritten** - Some require direct proxy rules
5. **Disable compression** - `sub_filter` only works on uncompressed content

## Alternative Approaches That Don't Work

- **sub_filter alone** - Can't catch runtime-built paths
- **Rewrite rules** - Client-side routing defeats them
- **Environment variables** - PufferPanel doesn't support BASE_URL env var
- **Nginx location wildcards** - Too broad, conflicts with blog routes

## When This Approach Won't Work

- If the SPA uses hash routing (`#/login`) - conflicts with base tag
- If there's no `<head>` tag to inject into
- If the app makes hardcoded absolute URL calls
- If the blog uses the same paths (`/js/`, `/css/`, etc.)

## Credits

This solution combines techniques from:
- HTML `<base>` tag specification
- History API interception patterns
- Nginx sub_filter module
- Referer-based smart routing

Date: January 3, 2026
Challenge: Getting PufferPanel to work on `/dev/8677/` subpath
Result: Success! Login screen loads, authentication works, dashboard accessible

---

**TL;DR**: To proxy an SPA to a subpath, you need:
1. Direct asset routing for `/js/`, `/css/`, etc.
2. Internal route handlers for SPA routes
3. HTML injection with `<base>` tag + router interception
4. Smart API routing with referer checking
5. Patience and lots of trial and error
