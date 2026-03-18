#!/usr/bin/env python3
"""
Enhanced blog compiler that works with the new modular page structure.
Supports per-page assets and the new config.json + content.md format.
"""

import os
import json
import shutil
from pathlib import Path

class ModularBlogCompiler:
    def __init__(self, pages_dir="pages", output_dir="output", static_dir="static"):
        self.pages_dir = Path(pages_dir)
        self.output_dir = Path(output_dir)
        self.static_dir = Path(static_dir)
        self.categories = {}

    def clean_output(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create assets directory in output
        (self.output_dir / "assets").mkdir(exist_ok=True)

    def copy_static_files(self):
        """Copy static files (gifs, images, etc.) to output directory"""
        if not self.static_dir.exists():
            return

        for static_file in self.static_dir.rglob('*'):
            if static_file.is_file():
                # Preserve directory structure
                relative_path = static_file.relative_to(self.static_dir)
                output_path = self.output_dir / relative_path

                # Create parent directories if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    shutil.copy2(static_file, output_path)
                except IOError as e:
                    print(f"Warning: Could not copy static file {static_file}: {e}")
    
    def get_page_directories(self):
        """Get all valid page directories (including nested subpages)"""
        if not self.pages_dir.exists():
            return []
        
        page_dirs = []
        
        def find_pages_recursive(directory, depth=0):
            """Recursively find all page directories"""
            # Limit depth to prevent infinite recursion
            if depth > 3:  # Allow up to 3 levels deep: pages/main/sub1/sub2
                return
                
            for item in directory.iterdir():
                if item.is_dir():
                    config_file = item / 'config.json'
                    content_file = item / 'content.md'
                    
                    if config_file.exists() and content_file.exists():
                        page_dirs.append(item)
                    
                    # Always check subdirectories regardless of whether this directory is a page
                    find_pages_recursive(item, depth + 1)
        
        find_pages_recursive(self.pages_dir)
        
        # Warn about skipped directories only for top-level directories
        for item in self.pages_dir.iterdir():
            if item.is_dir():
                config_file = item / 'config.json'
                content_file = item / 'content.md'
                
                if not config_file.exists() or not content_file.exists():
                    # Check if this directory contains any valid subpages
                    has_subpages = any(p for p in page_dirs if str(p).startswith(str(item)))
                    if not has_subpages:
                        print(f"Warning: Skipping {item.name} - missing config.json or content.md")
        
        return page_dirs
    
    def parse_page_config(self, page_dir):
        """Parse a page's config.json file"""
        config_file = page_dir / 'config.json'
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Error reading config.json in {page_dir.name}: {e}")
    
    def parse_page_content(self, page_dir):
        """Parse a page's content.md file"""
        content_file = page_dir / 'content.md'

        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract CSS, HTML, and meta tags
            html_start = content.find('<html>')
            css_start = content.find('<style>')

            if html_start == -1:
                raise ValueError(f"No HTML section found in {content_file}")

            # Strip the <html> marker tag itself — it's just a section delimiter
            html_content = content[html_start + len('<html>'):]
            css_content = ""
            meta_tags = ""

            # Extract CSS
            if css_start != -1:
                css_end = content.find('</style>') + 8
                css_content = content[css_start:css_end]
                # HTML content starts after <html> marker; CSS is always before it so no need to splice it out
                html_content = content[html_start + len('<html>'):].strip()

            # Extract meta tags from before <html> tag
            # Look for any <meta> tags that appear before the HTML section
            before_html = content[:content.find('<html>')]
            import re
            meta_pattern = r'<meta[^>]+>'
            meta_matches = re.findall(meta_pattern, before_html, re.IGNORECASE)
            if meta_matches:
                meta_tags = '\n    '.join(meta_matches)

            return html_content, css_content, meta_tags

        except IOError as e:
            raise ValueError(f"Error reading content.md in {page_dir.name}: {e}")
    
    def copy_page_assets(self, page_dir, slug):
        """Copy page assets to output directory"""
        assets_dir = page_dir / 'assets'
        
        if not assets_dir.exists():
            return []
        
        # Create page-specific assets directory in output
        output_assets_dir = self.output_dir / "assets" / slug
        output_assets_dir.mkdir(parents=True, exist_ok=True)
        
        copied_assets = []
        
        # Copy all files from page assets to output assets
        for asset_file in assets_dir.rglob('*'):
            if asset_file.is_file():
                # Preserve directory structure
                relative_path = asset_file.relative_to(assets_dir)
                output_asset_path = output_assets_dir / relative_path
                
                # Create parent directories if needed
                output_asset_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(asset_file, output_asset_path)
                    copied_assets.append(str(relative_path))
                except IOError as e:
                    print(f"Warning: Could not copy asset {asset_file}: {e}")
        
        return copied_assets
    
    def compile_page(self, page_dir):
        """Compile a single page from the modular structure"""
        config = self.parse_page_config(page_dir)
        html_content, css_content, meta_tags = self.parse_page_content(page_dir)

        # Calculate the page's URL path based on its location relative to pages_dir
        relative_path = page_dir.relative_to(self.pages_dir)
        url_path = str(relative_path).replace('\\', '/')  # Ensure forward slashes for URLs

        # Use slug from config, or fall back to the full relative path
        slug = config.get('slug', url_path)

        # Copy page assets
        assets = self.copy_page_assets(page_dir, slug)
        if assets:
            print(f"  Copied {len(assets)} assets for {slug}")

        # Build meta tags section (only include if meta_tags exist)
        meta_section = f"\n    {meta_tags}" if meta_tags else ""

        # No CRT effects on blog posts - they render normally
        crt_scripts = ""

        # Create full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{meta_section}
    <title>{config.get('title', 'Blog Post')}</title>
    {css_content}
</head>
<body>
    {html_content}{crt_scripts}
</body>
</html>"""
        
        # Create nested directory structure for subpages
        if '/' in slug:
            # This is a subpage - create nested directory structure
            output_dir = self.output_dir / slug
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "index.html"
            
            # Also create the flat .html file for backward compatibility
            flat_slug = slug.replace('/', '-')
            flat_output_file = self.output_dir / f"{flat_slug}.html"
            with open(flat_output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
        else:
            # This is a top-level page - use existing logic
            output_file = self.output_dir / f"{slug}.html"
            
            # Create extensionless version for URL-friendly access
            extensionless_dir = self.output_dir / slug
            extensionless_dir.mkdir(exist_ok=True)
            extensionless_file = extensionless_dir / "index.html"
            with open(extensionless_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            output_file = extensionless_file  # Use the extensionless version as primary
        
        # Write the compiled page
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Track categories - but exclude subpages from homepage listing
        # Only include top-level pages (no '/' in slug) in the homepage
        is_top_level = '/' not in slug
        if is_top_level:
            categories = config.get('categories', [])
            for category in categories:
                if category not in self.categories:
                    self.categories[category] = []
                self.categories[category].append({
                    'title': config.get('title', 'Untitled'),
                    'slug': slug,
                    'date': config.get('date', ''),
                    'description': config.get('description', ''),
                    'assets': assets
                })
        
        return config, slug, assets
    
    def generate_homepage(self):
        """Generate homepage by compiling all pages first"""
        pages_list = []
        
        # Compile all pages and collect metadata
        for page_dir in self.get_page_directories():
            try:
                config, slug, assets = self.compile_page(page_dir)
                pages_list.append({
                    'title': config.get('title', 'Untitled'),
                    'slug': slug,
                    'date': config.get('date', ''),
                    'description': config.get('description', ''),
                    'categories': config.get('categories', []),
                    'assets': assets,
                    'hidden': config.get('hidden', False)
                })
                print(f"Compiled page: {page_dir.name}")
            except Exception as e:
                print(f"Error compiling {page_dir.name}: {e}")
        
        # Organize pages hierarchically
        top_level_pages = []
        subpages_map = {}
        
        for page in pages_list:
            # Skip hidden pages (pages with "hidden": true in config.json)
            if page.get('hidden', False):
                continue

            if '/' not in page['slug']:
                # Top-level page
                top_level_pages.append(page)
                subpages_map[page['slug']] = []
            else:
                # Subpage - find its parent
                parent_slug = page['slug'].split('/')[0]
                if parent_slug not in subpages_map:
                    subpages_map[parent_slug] = []
                subpages_map[parent_slug].append(page)
        
        # Sort top-level pages by date (newest first)
        top_level_pages.sort(key=lambda x: x['date'], reverse=True)
        
        # Sort subpages by title
        for parent in subpages_map:
            subpages_map[parent].sort(key=lambda x: x['title'])
        
        # Generate homepage HTML with nested structure
        homepage_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-geo-butler-verify" content="012AB09C9E49C2F7">
    <title>Gabrielpenman.com</title>
    <style>
    :root {
        --crt-red: rgb(218, 49, 49);
        --crt-green: rgb(112, 159, 115);
        --crt-blue: rgb(40, 129, 206);
    }

    /* Character-grid based layout */
    * {
        box-sizing: border-box;
    }

    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    body {
        margin: 0;
        padding: 1ch;
        font-family: 'VT323', 'Courier New', monospace;
        background-color: #000000;  /* Fallback if no photo selected */
        color: #FFFFFF;
        font-size: 20px;
        line-height: 1.2;
        overflow-y: auto;
        min-height: 100vh;
        position: relative;
    }

    #page-content {
        width: 100%;
        min-height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
        padding-bottom: 5ch;
        background-color: transparent;  /* Let photo background show through */
    }

    h1 {
        text-align: center;
        font-size: 2.5em;
        margin: 0 0 1ch 0;
        color: #00FFFF;
        letter-spacing: 0.2ch;
        flex-shrink: 0;
        font-weight: normal;
        font-family: 'VT323', monospace;
        text-shadow: 2px 2px 0 #000000;
        padding: 0 1ch;
    }

    /* Mosaic container - blocks flow and wrap naturally */
    .grid-container {
        display: flex;
        flex-wrap: wrap;
        gap: 2ch;
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        min-height: calc(100vh - 12ch);
        position: relative;
        align-content: flex-start;
        align-items: flex-start;
        justify-content: center;
        overflow: visible;
    }

    /* Teletext/Prestel block styling - solid bright colors */
    .ascii-block {
        background-color: #0000AA;
        color: #FFFF00;
        padding: 1ch;
        margin: 0;
        position: relative;
        font-family: 'VT323', 'Courier New', monospace;
        border: none;
        flex-shrink: 0;
        box-sizing: border-box;
        font-size: 20px;
        font-weight: bold;
        opacity: 0.85;  /* More transparency to show photo background better */
        /* CSS bevel effect - light top-left, dark bottom-right */
        box-shadow:
            inset 2px 2px 0px rgba(255, 255, 255, 0.3),
            inset -2px -2px 0px rgba(0, 0, 0, 0.5);
    }

    /* Blog post blocks - SQUARE */
    .ascii-block.blog-post {
        width: 35ch;
        height: 35ch;
        cursor: pointer;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .ascii-block.blog-post:hover {
        background-color: #001100;
    }

    .ascii-block.blog-post h3 {
        margin: 0 0 1ch 0;
        font-size: 1.2em;
        font-weight: bold;
    }

    .ascii-block.blog-post .description {
        flex: 1;
        overflow: hidden;
        margin: 1ch 0;
        line-height: 1.4;
        font-size: 0.9em;
    }

    .ascii-block.blog-post a {
        display: block;
        margin-top: auto;
        color: inherit;
        padding-top: 1ch;
        text-decoration: underline;
    }

    /* System status - SQUARE - Green background */
    .ascii-block.system-status {
        width: 35ch;
        height: 35ch;
        background-color: #00AA00;
        color: #FFFF00;
    }

    .ascii-block.system-status h3 {
        margin: 0 0 1ch 0;
        font-size: 1.2em;
        font-weight: bold;
    }

    .ascii-block.system-status div {
        margin: 0.5ch 0;
        font-size: 0.9em;
    }

    /* Dev ports - SQUARE - Cyan background */
    .ascii-block.dev-ports {
        width: 35ch;
        height: 35ch;
        background-color: #00AAAA;
        color: #FFFF00;
    }

    .ascii-block.dev-ports h3 {
        margin: 0 0 1ch 0;
        font-size: 1.2em;
        font-weight: bold;
    }

    .ascii-block.dev-ports a {
        display: block;
        margin: 0.5ch 0;
        font-size: 0.9em;
        color: #FFFF00;
        font-weight: bold;
    }

    /* CPU grid styling - 4 rows of 4 characters */
    #cpu-grid {
        font-family: 'VT323', monospace;
        line-height: 1.2;
    }

    .cpu-row {
        letter-spacing: 0.1ch;
    }

    .ascii-block a {
        color: inherit;
        text-decoration: none;
    }

    .ascii-block a:hover {
        text-decoration: underline;
    }

    /* Teletext color variations - solid backgrounds */
    .ascii-block.blog-post.color-red {
        background-color: #AA0000;
        color: #FFFF00;
    }
    .ascii-block.blog-post.color-blue {
        background-color: #0000AA;
        color: #FFFFFF;
    }
    .ascii-block.blog-post.color-yellow {
        background-color: #AAAA00;
        color: #0000AA;
    }
    .ascii-block.blog-post.color-cyan {
        background-color: #00AAAA;
        color: #FFFF00;
    }
    .ascii-block.blog-post.color-magenta {
        background-color: #AA00AA;
        color: #FFFF00;
    }
    .ascii-block.blog-post.color-green {
        background-color: #00AA00;
        color: #FFFF00;
    }


    /* Loading screen */
    #loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #000000;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #4dd0e1;
        font-family: 'Courier New', monospace;
        transition: opacity 0.5s ease-out;
    }

    #loading-screen.hidden {
        opacity: 0;
        pointer-events: none;
    }

    .loading-text {
        font-size: 1.5em;
        margin-bottom: 20px;
        animation: pulse 1.5s ease-in-out infinite;
    }

    .loading-dots {
        font-size: 2em;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    @media (max-width: 768px) {
        .grid-container {
            flex-direction: column;
        }

        .ascii-block {
            width: 100% !important;
            height: auto !important;
            min-height: 20ch;
        }

        body {
            padding: 1ch;
        }

        h1 {
            font-size: 1.5em;
            padding: 0 0.5ch;
        }

        #glitched-title {
            font-size: 1.5em !important;
            padding: 0 0.5ch !important;
        }
    }


    /* RAM grid styling - 8GB sections */
    #ram-grid {
        display: flex;
        flex-direction: column;
        gap: 0.25ch;
        margin: 0.5ch 0;
        font-family: 'VT323', monospace;
    }

    .ram-section {
        font-size: 0.9em;
    }

    h1 {
        color: #ffffff;
        font-size: 2.5em;
        margin: 15px 0;
    }

    h2 {
        color: #ffffff;
        font-size: 1.6em;
        margin: 12px 0;
    }

    h3 {
        color: #ffffff;
        font-size: 1.3em;
        margin: 10px 0;
    }

    a {
        color: #cccccc;
        font-size: 1em;
    }

    a:visited {
        color: #aaaaaa;
    }

    a:hover {
        color: #ffffff;
        text-decoration: underline;
    }

    @media (max-width: 768px) {
        body {
            padding: 10px;
        }

        .status-section {
            padding: 10px;
            overflow-x: auto;
        }

        .status-item {
            flex-wrap: wrap;
            gap: 5px;
            font-size: 0.85em;
        }

        .status-label {
            min-width: 70px;
            font-size: 0.9em;
        }

        #cpu-grid {
            font-size: 0.9em;
        }

        #ram-grid {
            font-size: 0.8em;
        }

        #spidey-container img {
            max-width: 150px;
        }
    }

    @media (max-width: 480px) {
        .status-label {
            min-width: 60px;
        }

        #cpu-grid {
            font-size: 0.8em;
        }

        #ram-grid {
            font-size: 0.7em;
        }

        h1 {
            font-size: 1.5em;
        }

        article h2 {
            font-size: 1.2em;
        }
    }

    /* CRT Effect - Full RGB separation with scanlines */
    .crt {
        text-shadow: 0 0 0.2em currentColor, 1px 1px rgba(255, 0, 255, 0.5),
            -1px -1px rgba(0, 255, 255, 0.4);
        position: relative;
    }

    .crt:before,
    .crt:after {
        content: "";
        transform: translateZ(0);
        pointer-events: none;
        position: fixed;
        height: 100vh;
        width: 100vw;
        left: 0;
        top: 0;
        z-index: 9999;
    }

    /* Horizontal scanlines */
    .crt:before {
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.15) 0px,
            rgba(0, 0, 0, 0.15) 1px,
            transparent 1px,
            transparent 2px
        );
    }

    /* RGB color separation overlay */
    .crt:after {
        background:
            repeating-linear-gradient(
                0deg,
                var(--crt-red) 0px,
                var(--crt-red) 1px,
                transparent 1px,
                transparent 3px
            ),
            repeating-linear-gradient(
                0deg,
                var(--crt-green) 1px,
                var(--crt-green) 2px,
                transparent 2px,
                transparent 3px
            ),
            repeating-linear-gradient(
                0deg,
                var(--crt-blue) 2px,
                var(--crt-blue) 3px,
                transparent 3px,
                transparent 3px
            );
        opacity: 0.08;
        mix-blend-mode: screen;
    }
    </style>
    <script>
    function toggleSubpages(parentSlug) {
        const subpages = document.getElementById('subpages-' + parentSlug);
        const button = document.getElementById('toggle-' + parentSlug);

        if (subpages.classList.contains('collapsed')) {
            subpages.classList.remove('collapsed');
            button.textContent = 'Hide subpages ▲';
        } else {
            subpages.classList.add('collapsed');
            button.textContent = 'Show subpages ▼';
        }
    }

    </script>
</head>
<body>
    <!-- Loading Screen -->
    <div id="loading-screen">
        <div class="loading-text">INITIALIZING</div>
        <div class="loading-dots">...</div>
    </div>

    <div id="page-content" class="crt">
    <h1>GABRIELPENMAN.COM</h1>
    <div class="grid-container" id="grid-container">
"""

        # Add system status block first
        homepage_html += """        <div class="ascii-block system-status">
            <h3>SYSTEM</h3>
            <div>MC:  <span id="minecraft-status">OFF</span></div>
            <div>API: <span id="api-status">OFF</span></div>
            <div>MAP: <span id="bluemap-status">OFF</span></div>
            <div>CPU: <span id="cpu-name">0%</span></div>
            <div id="cpu-grid"></div>
            <div>RAM: <span id="ram-usage">0%</span></div>
            <div id="ram-grid"></div>
        </div>
"""

        # Random primary colors for blog posts
        colors = ['red', 'blue', 'yellow', 'cyan', 'magenta', 'green']

        # Separate music and photography from other posts
        music_post = None
        photography_post = None
        other_posts = []

        for page in top_level_pages:
            if page['slug'] == 'music':
                music_post = page
            elif page['slug'] == 'photography':
                photography_post = page
            else:
                other_posts.append(page)

        # Add photography first
        color_idx = 0
        if photography_post:
            color = colors[color_idx % len(colors)]
            color_idx += 1

            description = photography_post.get('description', '')
            if len(description) > 200:
                description = description[:197] + '...'

            homepage_html += f"""        <div class="ascii-block blog-post color-{color}" onclick="window.location.href='/{photography_post['slug']}'">
            <h3>{photography_post['title']}</h3>
            <div class="description">{description}</div>
            <a href="/{photography_post['slug']}">/{photography_post['slug']}</a>
        </div>
"""

        # Add dev ports after photography
        homepage_html += """        <div class="ascii-block dev-ports">
            <h3>DEV PORTS</h3>
            <div><a href="/dev/8100/">→ BlueMap:8100</a> <span id="bluemap-port-status">OFF</span></div>
            <div><a href="/dev/3005/">→ Trading:3005</a> <span id="trading-port-status">OFF</span></div>
            <div><a href="/dev/5123/">→ Depopper:5123</a> <span id="depopper-port-status">OFF</span></div>
            <div><a href="/dev/6767/">→ WTA:6767</a> <span id="wta-port-status">OFF</span></div>
            <div><a href="/dev/8888/">→ Jupyter:8888</a> <span id="jupyter-port-status">OFF</span></div>
        </div>
"""

        # Add music
        if music_post:
            color = colors[color_idx % len(colors)]
            color_idx += 1

            description = music_post.get('description', '')
            if len(description) > 200:
                description = description[:197] + '...'

            homepage_html += f"""        <div class="ascii-block blog-post color-{color}" onclick="window.location.href='/{music_post['slug']}'">
            <h3>{music_post['title']}</h3>
            <div class="description">{description}</div>
            <a href="/{music_post['slug']}">/{music_post['slug']}</a>
        </div>
"""

        # Add all other blog posts
        for page in other_posts:
            color = colors[color_idx % len(colors)]
            color_idx += 1

            description = page.get('description', '')
            if len(description) > 200:
                description = description[:197] + '...'

            homepage_html += f"""        <div class="ascii-block blog-post color-{color}" onclick="window.location.href='/{page['slug']}'">
            <h3>{page['title']}</h3>
            <div class="description">{description}</div>
            <a href="/{page['slug']}">/{page['slug']}</a>
        </div>
"""

        # Add admin block at the bottom
        homepage_html += """        <div class="ascii-block blog-post color-magenta" onclick="window.photoBackground && window.photoBackground.toggleAdminMode();" style="cursor: pointer;">
            <h3>ADMIN</h3>
            <div class="description">Configure glitchGL effects for background and title</div>
            <a href="#" onclick="window.photoBackground && window.photoBackground.toggleAdminMode(); return false;">→ Settings Panel</a>
        </div>
"""

        homepage_html += """    </div>
    </div>

    <script>
    function refreshStatus() {
        fetch('/api/server-details')
            .then(response => response.json())
            .then(data => {
                // Update system status with ON/OFF text
                const mcStatus = document.getElementById('minecraft-status');
                if (data.minecraft_healthy) {
                    mcStatus.textContent = 'ON';
                } else {
                    mcStatus.textContent = 'OFF';
                }

                const apiStatus = document.getElementById('api-status');
                apiStatus.textContent = 'ON';

                // CPU info
                const cpuCores = data.cpu.cores || '8 cores / 16 threads';
                document.getElementById('cpu-name').textContent = cpuCores + ' @ ' + data.cpu.usage_percent.toFixed(0) + '%';

                // CPU grid - 16 threads as bars
                const cpuGrid = document.getElementById('cpu-grid');
                if (data.cpu.per_core) {
                    const cores = data.cpu.per_core.slice(0, 16);
                    cpuGrid.innerHTML = '';

                    // Create 4 rows of 4 bars each
                    for (let row = 0; row < 4; row++) {
                        const rowDiv = document.createElement('div');
                        rowDiv.className = 'cpu-row';

                        let rowBar = '';
                        for (let col = 0; col < 4; col++) {
                            const coreIndex = row * 4 + col;
                            const usage = cores[coreIndex] || 0;

                            // 4 blocks per core (each = 25%)
                            const blocks = Math.round(usage / 25);
                            rowBar += '█'.repeat(blocks) + '░'.repeat(4 - blocks) + ' ';
                        }

                        rowDiv.textContent = rowBar.trim();
                        cpuGrid.appendChild(rowDiv);
                    }
                }

                // RAM - Split into 8GB sections (31GB = 8+8+8+7)
                if (data.ram && data.ram.usage_percent !== undefined && data.ram.total_gb !== undefined) {
                    const totalGb = data.ram.total_gb;
                    const usedGb = (data.ram.usage_percent * totalGb / 100);

                    // Update header
                    document.getElementById('ram-usage').textContent =
                        data.ram.usage_percent.toFixed(0) + '% (' + usedGb.toFixed(1) + '/' + totalGb.toFixed(0) + 'GB)';

                    // Calculate sections (8GB each, last one is remainder)
                    const sectionSize = 8;
                    const numFullSections = Math.floor(totalGb / sectionSize);
                    const lastSectionSize = totalGb % sectionSize || sectionSize;
                    const totalSections = numFullSections + (lastSectionSize > 0 && lastSectionSize < sectionSize ? 1 : 0);

                    const ramGrid = document.getElementById('ram-grid');
                    ramGrid.innerHTML = '';

                    let remainingUsed = usedGb;

                    for (let i = 0; i < totalSections; i++) {
                        const sectionCapacity = (i === totalSections - 1 && lastSectionSize < sectionSize) ? lastSectionSize : sectionSize;
                        const sectionUsed = Math.min(remainingUsed, sectionCapacity);
                        remainingUsed -= sectionUsed;

                        const sectionDiv = document.createElement('div');
                        sectionDiv.className = 'ram-section';

                        const sectionPercent = (sectionUsed / sectionCapacity) * 100;
                        const barLength = 16; // 16 blocks per section
                        const filledLength = Math.round((sectionPercent / 100) * barLength);

                        const bar = '█'.repeat(filledLength) + '░'.repeat(barLength - filledLength);
                        sectionDiv.textContent = bar + ' ' + sectionUsed.toFixed(1) + '/' + sectionCapacity.toFixed(0) + 'GB';

                        ramGrid.appendChild(sectionDiv);
                    }
                }

                // Check dev port status (using API endpoint that doesn't require auth)
                fetch('/api/dev/port-status')
                    .then(response => response.json())
                    .then(portData => {
                        // BlueMap
                        const mapStatus = document.getElementById('bluemap-status');
                        if (mapStatus) {
                            mapStatus.textContent = portData.services.bluemap.running ? 'ON' : 'OFF';
                        }

                        // Update other port statuses if elements exist
                        const tradingStatus = document.getElementById('trading-port-status');
                        if (tradingStatus) {
                            tradingStatus.textContent = portData.services.trading.running ? 'ON' : 'OFF';
                        }

                        const depopperStatus = document.getElementById('depopper-port-status');
                        if (depopperStatus) {
                            depopperStatus.textContent = portData.services.depopper.running ? 'ON' : 'OFF';
                        }

                        const wtaStatus = document.getElementById('wta-port-status');
                        if (wtaStatus) {
                            wtaStatus.textContent = portData.services.wta.running ? 'ON' : 'OFF';
                        }

                        const jupyterStatus = document.getElementById('jupyter-port-status');
                        if (jupyterStatus) {
                            jupyterStatus.textContent = portData.services.jupyter.running ? 'ON' : 'OFF';
                        }
                    })
                    .catch(error => {
                        console.error('Failed to fetch port status:', error);
                    });
            })
            .catch(error => {
                console.error('Failed to fetch status:', error);
            });
    }

    // Load status on page load and refresh every half second
    document.addEventListener('DOMContentLoaded', refreshStatus);
    setInterval(refreshStatus, 500);
    </script>

    <!-- glitchGL Photo Background - ENABLED -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lil-gui@0.21"></script>
    <script src="/assets/js/glitchGL.min.js"></script>
    <script src="/assets/js/photo-background.js"></script>
    <script>
        // Initialize photo background with glitchGL effects
        window.pageConfig = {
            crt_effects: 'full',          // Options: 'none', 'subtle', 'full'
            photo_background: true        // Enable photo background system
        };

        // Photo background controller will handle everything
        if (window.photoBackground) {
            window.photoBackground.init(window.pageConfig);
        }
    </script>
</body>
</html>
"""

        # Write homepage
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(homepage_html)

    def compile_all(self):
        """Compile all pages and generate homepage"""
        print("=== Modular Blog Compiler ===")
        print("Cleaning output directory...")
        self.clean_output()

        print("Copying static files...")
        self.copy_static_files()

        print("Compiling pages...")
        self.generate_homepage()

        # Generate summary
        html_files = list(self.output_dir.glob('*.html'))
        asset_dirs = list((self.output_dir / 'assets').glob('*')) if (self.output_dir / 'assets').exists() else []

        print("\n=== Compilation Complete! ===")
        print(f"Generated {len(html_files)} HTML pages")
        print(f"Created asset directories for {len(asset_dirs)} pages")

        if self.categories:
            print(f"Categories found: {', '.join(self.categories.keys())}")

        print(f"\nTo serve static files: python server.py")
        print(f"To serve with API: python flask_server.py")
        print(f"Static files location: {self.output_dir}")

if __name__ == "__main__":
    compiler = ModularBlogCompiler()
    compiler.compile_all()
