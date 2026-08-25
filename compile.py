#!/usr/bin/env python3
"""
Enhanced blog compiler that works with the new modular page structure.
Supports per-page assets and the new config.json + content.md format.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

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

    def copy_artist_assets(self):
        """Copy artist-level assets to output directory for preview routes.

        Copies pages/artists/{slug}/assets/ -> output/artists/{slug}/assets/
        This allows artist pages to reference assets via ../assets/ relative paths
        that work in both preview mode (/artists/{slug}/page) and domain mode (/page).
        """
        artists_dir = self.pages_dir / 'artists'
        if not artists_dir.exists():
            return

        for artist_dir in artists_dir.iterdir():
            if not artist_dir.is_dir() or artist_dir.name.startswith('_'):
                continue

            assets_dir = artist_dir / 'assets'
            if not assets_dir.exists():
                continue

            output_assets_dir = self.output_dir / 'artists' / artist_dir.name / 'assets'
            output_assets_dir.mkdir(parents=True, exist_ok=True)

            asset_count = 0
            for asset_file in assets_dir.rglob('*'):
                if asset_file.is_file():
                    relative_path = asset_file.relative_to(assets_dir)
                    output_path = output_assets_dir / relative_path
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.copy2(asset_file, output_path)
                        asset_count += 1
                    except IOError as e:
                        print(f"Warning: Could not copy artist asset {asset_file}: {e}")

            if asset_count:
                print(f"  Copied {asset_count} assets for artist '{artist_dir.name}'")

    def generate_artist_root_indexes(self):
        """Generate root index.html for each artist that serves their home page.

        This enables preview routes: /artists/{slug}/ serves the home page.
        """
        artists_dir = self.pages_dir / 'artists'
        if not artists_dir.exists():
            return

        for artist_dir in artists_dir.iterdir():
            if not artist_dir.is_dir() or artist_dir.name.startswith('_'):
                continue

            # Check if artist has a home page
            home_output = self.output_dir / 'artists' / artist_dir.name / 'home' / 'index.html'
            artist_root = self.output_dir / 'artists' / artist_dir.name
            artist_root.mkdir(parents=True, exist_ok=True)

            if home_output.exists():
                # Redirect to home/ so relative paths (../assets/, ../gallery) resolve correctly
                redirect_html = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=home/"></head></html>'
                with open(artist_root / 'index.html', 'w') as f:
                    f.write(redirect_html)
                print(f"  Generated root index for artist '{artist_dir.name}' -> home")
            else:
                # Generate a simple redirect to the first available page
                for subdir in (self.output_dir / 'artists' / artist_dir.name).iterdir():
                    if subdir.is_dir() and (subdir / 'index.html').exists() and subdir.name != 'assets':
                        redirect_html = f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url={subdir.name}/"></head></html>'
                        with open(artist_root / 'index.html', 'w') as f:
                            f.write(redirect_html)
                        print(f"  Generated redirect index for artist '{artist_dir.name}' -> {subdir.name}")
                        break
    
    def compile_page(self, page_dir):
        """Compile a single page from the modular structure"""
        config = self.parse_page_config(page_dir)
        html_content, css_content, meta_tags = self.parse_page_content(page_dir)

        # Calculate the page's URL path based on its location relative to pages_dir
        relative_path = page_dir.relative_to(self.pages_dir)
        url_path = str(relative_path).replace('\\', '/')  # Ensure forward slashes for URLs

        # Use slug from config, or fall back to the full relative path
        slug = config.get('slug', url_path)

        # Safety: if page lives under artists/, force slug to start with artists/
        # This prevents artist pages from accidentally overwriting main blog pages
        if str(relative_path).startswith('artists/') and not slug.startswith('artists/'):
            corrected_slug = url_path
            print(f"  WARNING: Artist page slug '{slug}' doesn't match path, using '{corrected_slug}'")
            slug = corrected_slug

        # Copy page assets
        assets = self.copy_page_assets(page_dir, slug)
        if assets:
            print(f"  Copied {len(assets)} assets for {slug}")

        # Build meta tags section (only include if meta_tags exist)
        meta_section = f"\n    {meta_tags}" if meta_tags else ""

        # No CRT effects on blog posts - they render normally
        crt_scripts = ""

        # Inject current compile date for artist home pages
        if slug.endswith('/home') or slug == 'artists/cliveburgess/home':
            compile_date = datetime.now()
            # Replace the hardcoded date in JavaScript with current compile date
            html_content = html_content.replace(
                'let updateDate = new Date(2026, 2, 1);',
                f'let updateDate = new Date({compile_date.year}, {compile_date.month - 1}, {compile_date.day});'
            )

        # Calculate relative path to favicon based on nesting level
        # Add 1 because the file is index.html inside a directory
        nesting_level = slug.count('/') + 1
        favicon_file = config.get('favicon', 'favicon.svg')
        favicon_path = '../' * nesting_level + favicon_file if nesting_level > 0 else favicon_file

        # Check for artist-specific favicon
        if str(relative_path).startswith('artists/'):
            parts = str(relative_path).split('/')
            if len(parts) >= 2:
                artist_config_file = self.pages_dir / 'artists' / parts[1] / 'config.json'
                if artist_config_file.exists():
                    try:
                        with open(artist_config_file, 'r', encoding='utf-8') as f:
                            artist_config = json.load(f)
                        if artist_config.get('favicon'):
                            favicon_path = '../assets/' + artist_config['favicon']
                    except (json.JSONDecodeError, IOError):
                        pass

        # Create full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">{meta_section}
    <script defer src="https://baselinelabs.ai/js/tracker.js" data-site="09f6d274c6a90724de51d9a3"></script>
    <title>{config.get('title', 'Blog Post')}</title>
    <link rel="icon" href="{favicon_path}">
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
                    'hidden': config.get('hidden', False),
                    'preview_video': config.get('preview_video', '')
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
    <script defer src="https://baselinelabs.ai/js/tracker.js" data-site="09f6d274c6a90724de51d9a3"></script>
    <link rel="icon" href="favicon.svg">
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
        margin: 0 auto 1ch auto;
        color: #00FFFF;
        letter-spacing: 0.2ch;
        flex-shrink: 0;
        font-weight: normal;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px 0 #000000;
        padding: 0 1ch;
        width: 100%;
        max-width: 1400px;
        box-sizing: border-box;
    }

    /* Preview video in blog blocks */
    .ascii-block.blog-post .preview-video {
        width: 100%;
        max-height: 65%;
        object-fit: contain;
        display: block;
        margin: 0.5ch auto;
        border-radius: 0;
        pointer-events: none;
    }

    /* Mosaic container - CSS grid with small cells, big blocks span 2x2 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(6, 16.5ch);
        gap: 2ch;
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        min-height: calc(100vh - 12ch);
        position: relative;
        grid-auto-rows: 16.5ch;
        grid-auto-flow: dense;
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
        box-sizing: border-box;
        font-size: 20px;
        font-weight: bold;
        opacity: 0.85;  /* More transparency to show photo background better */
        /* CSS bevel effect - light top-left, dark bottom-right */
        box-shadow:
            inset 2px 2px 0px rgba(255, 255, 255, 0.3),
            inset -2px -2px 0px rgba(0, 0, 0, 0.5);
    }

    /* Blog post blocks - big 2x2 */
    .ascii-block.blog-post {
        grid-column: span 2;
        grid-row: span 2;
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

    .block-preview-video {
        width: 100%;
        max-height: 16ch;
        object-fit: contain;
        border-radius: 2px;
        pointer-events: none;
        display: block;
        margin: 0.5ch 0;
    }

    .ascii-block.blog-post a {
        display: block;
        margin-top: auto;
        color: inherit;
        padding-top: 1ch;
        text-decoration: underline;
    }

    /* System status - big 2x2 - Green background */
    .ascii-block.system-status {
        grid-column: span 2;
        grid-row: span 2;
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

    /* Dev ports - big 2x2 - Cyan background */
    .ascii-block.dev-ports {
        grid-column: span 2;
        grid-row: span 2;
        background-color: #00AAAA;
        color: #FFFF00;
    }

    .ascii-block.dev-ports h3 {
        margin: 0 0 1ch 0;
        font-size: 1.2em;
        font-weight: bold;
    }

    .ascii-block.dev-ports a {
        display: flex;
        align-items: center;
        gap: 0.8ch;
        margin: 0.5ch 0;
        font-size: 0.9em;
        color: #FFFF00;
        font-weight: bold;
    }

    svg.port-icon {
        width: 1.2em;
        height: 1.2em;
        fill: #FFFF00;
        flex-shrink: 0;
    }

    /* ── Individual widgets (1x1 grid cells) ── */
    .widget {
        grid-column: span 1;
        grid-row: span 1;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        gap: 0.4ch;
        font-family: 'VT323', 'Courier New', monospace;
        font-size: 20px;
        font-weight: bold;
        padding: 1ch;
        box-sizing: border-box;
        text-decoration: none;
        color: #FFFF00;
        opacity: 0.85;
        box-shadow:
            inset 2px 2px 0px rgba(255, 255, 255, 0.3),
            inset -2px -2px 0px rgba(0, 0, 0, 0.5);
        overflow: hidden;
    }
    .widget:hover {
        opacity: 1;
    }
    .widget h3 {
        font-size: 0.9em;
        margin: 0;
        color: #FFFFFF;
        font-family: inherit;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    .widget .widget-icon {
        line-height: 1;
        color: #FFFFFF;
    }
    .widget .widget-icon svg {
        width: 32px;
        height: 32px;
        fill: #FFFFFF;
    }
    .widget .widget-label {
        font-size: 0.6em;
        color: #FFFF00;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    .widget .widget-status {
        font-size: 0.55em;
        color: #00FF00;
    }

    /* Empty gap slot - 1x1 invisible spacer */
    .layout-gap {
        grid-column: span 1;
        grid-row: span 1;
        visibility: hidden;
    }

    .widget.wg-github { background-color: #333333; }
    .widget.wg-linkedin { background-color: #0055AA; }
    .widget.wg-instagram { background-color: #AA3377; }
    .widget.wg-soundcloud { background-color: #FF5500; }
    .widget.wg-email { background-color: #AA5500; }
    .widget.wg-bluemap { background-color: #00AA00; }
    .widget.wg-portal { background-color: #AA00AA; }
    .widget.wg-mgmt { background-color: #005500; }
    .widget.wg-templeos { background-color: #AA00AA; }
    .widget.wg-xp { background-color: #0055AA; }
    .widget.wg-services { background-color: #336699; }
    .widget.wg-default { background-color: #0000AA; }

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


    /* Loading screen — CRT power-on effect */
    #loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #000000;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        transition: background-color 0.25s ease-out 0.55s;
    }

    .crt-dot {
        width: 5px;
        height: 5px;
        background: #ffffff;
        border-radius: 50%;
        box-shadow:
            0 0 3px 1px rgba(255, 255, 255, 0.95),
            0 0 10px 3px rgba(220, 255, 230, 0.55),
            0 0 28px 8px rgba(170, 220, 195, 0.22);
        animation: crt-dot-pulse 1.6s ease-in-out infinite;
        will-change: width, height, opacity, border-radius;
    }

    @keyframes crt-dot-pulse {
        0%, 100% { opacity: 0.85; transform: scale(0.92); }
        50%      { opacity: 1;    transform: scale(1.08); }
    }

    #loading-screen.hidden {
        pointer-events: none;
        background-color: transparent;
    }

    #loading-screen.hidden .crt-dot {
        animation: crt-power-on 1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    @keyframes crt-power-on {
        0% {
            width: 5px;
            height: 5px;
            border-radius: 50%;
            opacity: 1;
            background: #ffffff;
            box-shadow:
                0 0 3px 1px rgba(255, 255, 255, 0.95),
                0 0 10px 3px rgba(220, 255, 230, 0.55);
        }
        28% {
            width: 100vw;
            height: 3px;
            border-radius: 0;
            opacity: 1;
            background: #ffffff;
            box-shadow:
                0 0 22px 6px rgba(255, 255, 255, 0.9),
                0 0 50px 14px rgba(220, 255, 230, 0.5);
        }
        58% {
            width: 100vw;
            height: 100vh;
            border-radius: 0;
            opacity: 1;
            background: #ffffff;
            box-shadow: none;
        }
        100% {
            width: 100vw;
            height: 100vh;
            border-radius: 0;
            opacity: 0;
            background: #ffffff;
            box-shadow: none;
        }
    }

    @media (max-width: 768px) {
        .grid-container {
            grid-template-columns: repeat(2, 1fr);
            grid-auto-rows: auto;
        }

        .ascii-block.blog-post,
        .ascii-block.system-status,
        .ascii-block.dev-ports {
            grid-column: span 2;
            grid-row: span 1;
            min-height: 20ch;
        }

        .widget {
            grid-column: span 1;
            grid-row: span 1;
            min-height: 8ch;
            font-size: 12px;
        }

        .preview-video,
        .block-preview-video {
            display: none;
        }

        .layout-gap {
            display: none;
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
    <!-- Loading Screen — CRT power-on -->
    <div id="loading-screen">
        <div class="crt-dot"></div>
    </div>

    <div id="page-content" class="crt">
    <h1>GABRIELPENMAN.COM</h1>
    <div class="grid-container" id="grid-container">
"""

        import random
        import json as json_module

        # ── Load widgets and blocks from widgets.json ──
        widgets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widgets.json')
        with open(widgets_path, 'r') as f:
            widgets_config = json_module.load(f)

        # ── Build individual widget blocks (each 1x1 in the grid) ──
        all_widgets = widgets_config['widgets']
        widget_blocks = {}  # id -> html
        for w in all_widgets:
            wid = f"widget-{w['id']}"
            target_attr = f' target="{w["target"]}"' if w.get('target') else ''
            css_class = w.get('css_class', 'wg-default')
            status_html = ''
            if w.get('status_id'):
                status_html = f'<div class="widget-status" id="{w["status_id"]}">OFF</div>'
            widget_blocks[wid] = f'        <a href="{w["url"]}"{target_attr} class="widget {css_class}" data-block-id="{wid}"><div class="widget-icon">{w["icon"]}</div><h3>{w["title"]}</h3><div class="widget-label">{w["label"]}</div>{status_html}</a>\n'

        # ── Dev ports block (only dev tools) ──
        dev_ports_block = """        <div class="ascii-block dev-ports" data-block-id="dev-ports">
            <h3>DEV PORTS</h3>
            <div><a href="/dev/3005/"><svg class="port-icon" viewBox="0 0 24 24"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>Trading :3005</a> <span id="trading-port-status">OFF</span></div>
            <div><a href="/dev/5123/"><svg class="port-icon" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>Depopper :5123</a> <span id="depopper-port-status">OFF</span></div>
            <div><a href="/dev/8888/"><svg class="port-icon" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>Jupyter :8888</a> <span id="jupyter-port-status">OFF</span></div>
            <div><a href="/dev/8889/lab"><svg class="port-icon" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>Titan SAR :8889</a> <span id="titansar-port-status">OFF</span></div>
            <div><a href="/dev/8890/"><svg class="port-icon" viewBox="0 0 24 24"><path d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>Geopolitical :8890</a> <span id="geopolmarkets-port-status">OFF</span></div>
            <div><a href="/dev/8891/"><svg class="port-icon" viewBox="0 0 24 24"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>Geopol Web :8891</a> <span id="geopolweb-port-status">OFF</span></div>
        </div>
"""

        # ── Build block registry: id -> html ──
        colors = ['red', 'blue', 'yellow', 'cyan', 'magenta', 'green']
        block_registry = {}  # id -> html string

        # System status block (2x2)
        block_registry['system-status'] = """        <div class="ascii-block system-status" data-block-id="system-status">
            <h3>SYSTEM</h3>
            <div>MC:  <span id="minecraft-status">OFF</span></div>
            <div>API: <span id="api-status">OFF</span></div>
            <div>MAP: <span id="bluemap-status">OFF</span></div>
            <div>CPU: <span id="cpu-name">0%</span></div>
            <div id="cpu-grid"></div>
            <div>RAM: <span id="ram-usage">0%</span></div>
            <div id="ram-grid"></div>
        </div>\n"""

        # Individual widget blocks (1x1 each)
        for wid, whtml in widget_blocks.items():
            block_registry[wid] = whtml

        # Dev ports block (2x2)
        block_registry['dev-ports'] = dev_ports_block

        # Blog post blocks
        color_idx = 0
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

        def make_blog_block(page, color):
            description = page.get('description', '')
            if len(description) > 200:
                description = description[:197] + '...'
            cats = ','.join(page.get('categories', []))
            video_html = ''
            if page.get('preview_video'):
                video_html = f'<video class="preview-video" src="{page["preview_video"]}" autoplay muted loop playsinline></video>'
            return f"""        <div class="ascii-block blog-post color-{color}" data-categories="{cats}" data-block-id="post-{page['slug']}" onclick="window.location.href='/{page['slug']}'">
            <h3>{page['title']}</h3>
            <div class="description">{description}</div>
            {video_html}
            <a href="/{page['slug']}">/{page['slug']}</a>
        </div>\n"""

        ordered_posts = []
        if photography_post:
            ordered_posts.append(photography_post)
        if music_post:
            ordered_posts.append(music_post)
        ordered_posts.extend(other_posts)

        for page in ordered_posts:
            block_id = f"post-{page['slug']}"
            block_registry[block_id] = make_blog_block(page, colors[color_idx % len(colors)])
            color_idx += 1

        # Admin block
        block_registry['admin'] = """        <div class="ascii-block blog-post color-magenta" data-block-id="admin" onclick="window.photoBackground && window.photoBackground.toggleAdminMode();" style="cursor: pointer;">
            <h3>ADMIN</h3>
            <div class="description">Configure glitchGL effects for background and title</div>
            <a href="#" onclick="window.photoBackground && window.photoBackground.toggleAdminMode(); return false;">→ Settings Panel</a>
        </div>\n"""

        # ── Layout from layout.json (or default order) ──
        layout_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'layout.json')
        default_order = list(block_registry.keys())
        layout_order = None

        if os.path.exists(layout_path):
            try:
                with open(layout_path, 'r') as f:
                    layout_data = json_module.load(f)
                layout_order = layout_data.get('order', [])
            except Exception:
                layout_order = None

        if layout_order:
            # Use saved order. Slots can be block IDs or "__gap__" for empty spaces.
            # Any new blocks not in layout get appended at the end.
            known_ids = set()
            for slot in layout_order:
                if slot != '__gap__':
                    known_ids.add(slot)
            # Append any blocks not in the saved layout
            for block_id in default_order:
                if block_id not in known_ids:
                    layout_order.append(block_id)
        else:
            # No saved layout — use default order with no gaps
            layout_order = default_order

        # Emit the grid based on layout order
        empty_block = '        <div class="layout-gap" data-block-id="__gap__"></div>\n'
        for slot in layout_order:
            if slot == '__gap__':
                homepage_html += empty_block
            elif slot in block_registry:
                homepage_html += block_registry[slot]
            # skip unknown IDs silently (deleted posts etc)

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

                        const titansarStatus = document.getElementById('titansar-port-status');
                        if (titansarStatus) {
                            titansarStatus.textContent = portData.services.titansar.running ? 'ON' : 'OFF';
                        }

                        const bluemapPortStatus = document.getElementById('bluemap-port-status');
                        if (bluemapPortStatus) {
                            bluemapPortStatus.textContent = portData.services.bluemap.running ? 'ON' : 'OFF';
                        }

                        const xpvncStatus = document.getElementById('xpvnc-port-status');
                        if (xpvncStatus) {
                            xpvncStatus.textContent = portData.services.xpvnc.running ? 'ON' : 'OFF';
                        }

                        const templeosStatus = document.getElementById('templeos-port-status');
                        if (templeosStatus) {
                            templeosStatus.textContent = portData.services.templeos.running ? 'ON' : 'OFF';
                        }

                        const geopolmarketsStatus = document.getElementById('geopolmarkets-port-status');
                        if (geopolmarketsStatus) {
                            geopolmarketsStatus.textContent = portData.services.geopolmarkets.running ? 'ON' : 'OFF';
                        }

                        const geopolwebStatus = document.getElementById('geopolweb-port-status');
                        if (geopolwebStatus) {
                            geopolwebStatus.textContent = portData.services.geopolweb.running ? 'ON' : 'OFF';
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

        // Always start loading background immediately
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

        print("Copying artist assets...")
        self.copy_artist_assets()

        print("Compiling pages...")
        self.generate_homepage()

        print("Generating artist preview indexes...")
        self.generate_artist_root_indexes()

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
