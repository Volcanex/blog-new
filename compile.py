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
    def __init__(self, pages_dir="pages", output_dir="output"):
        self.pages_dir = Path(pages_dir)
        self.output_dir = Path(output_dir)
        self.categories = {}
        
    def clean_output(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create assets directory in output
        (self.output_dir / "assets").mkdir(exist_ok=True)
    
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

            html_content = content[html_start:]
            css_content = ""
            meta_tags = ""

            # Extract CSS
            if css_start != -1:
                css_end = content.find('</style>') + 8
                css_content = content[css_start:css_end]
                # Remove CSS from HTML content
                html_content = content[:css_start] + content[css_end:]
                html_content = html_content.strip()

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
    {html_content}
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
                    'assets': assets
                })
                print(f"Compiled page: {page_dir.name}")
            except Exception as e:
                print(f"Error compiling {page_dir.name}: {e}")
        
        # Organize pages hierarchically
        top_level_pages = []
        subpages_map = {}
        
        for page in pages_list:
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
    <title>Gabrielpenman.com</title>
    <style>
    body {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .subpages {
        margin-left: 20px;
        margin-top: 10px;
        border-left: 2px solid #e1e8ed;
        padding-left: 15px;
    }
    
    .subpage-item {
        margin: 8px 0;
        font-size: 0.9em;
    }
    
    .subpage-item a {
        color: #0066cc;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .subpage-item a:hover {
        text-decoration: underline;
    }
    
    .subpage-item a:visited {
        color: #551a8b;
    }
    
    .subpage-toggle {
        cursor: pointer;
        background: none;
        border: none;
        color: #666;
        font-size: 0.9em;
        margin-top: 8px;
        padding: 4px 8px;
        border-radius: 3px;
        background: #f8f9fa;
    }
    
    .subpage-toggle:hover {
        background: #e9ecef;
    }
    
    .subpages.collapsed {
        display: none;
    }
    
    article {
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 1px solid #eee;
    }
    
    article:last-child {
        border-bottom: none;
    }
    
    .date {
        color: #666;
        font-size: 0.9em;
        margin: 5px 0;
    }
    
    .description {
        margin: 8px 0;
        color: #333;
    }
    
    .categories {
        font-size: 0.85em;
        color: #888;
    }
    
    .assets-info {
        font-size: 0.8em;
        color: #999;
        margin-top: 5px;
    }

    .status-section {
        margin-top: 50px;
        padding: 20px;
    }

    .status-section h3 {
        margin-top: 0;
        color: #333;
    }

    .status-item {
        margin: 12px 0;
        font-size: 0.95em;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 2px;
        background: #22c55e;
        flex-shrink: 0;
    }

    .status-label {
        font-weight: 500;
        color: #555;
        min-width: 100px;
    }

    .cpu-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0;
        width: 310px;
    }

    .cpu-row {
        display: flex;
        gap: 2px;
        margin-bottom: 10px;
    }

    .cpu-core-pair {
        display: flex;
        gap: 2px;
    }

    .cpu-core {
        display: flex;
        gap: 2px;
    }

    .cpu-square {
        width: 16px;
        height: 16px;
        border-radius: 1px;
        background: #e5e7eb;
    }

    .cpu-square.active {
        background: #22c55e;
    }

    .ram-bar {
        display: flex;
        width: 200px;
        height: 16px;
        border-radius: 2px;
        overflow: hidden;
        background: #e5e7eb;
    }

    .ram-used {
        background: #22c55e;
        height: 100%;
        transition: width 0.3s ease;
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

    function refreshStatus() {
        fetch('/api/server-details')
            .then(response => response.json())
            .then(data => {
                // CPU cores grid - 8 cores x 8 squares = 64 squares total
                const cpuGrid = document.getElementById('cpu-grid');
                cpuGrid.innerHTML = '';

                // Get first 8 cores and create 8 squares per core
                const cores = data.cpu.per_core.slice(0, 8);

                // Create 4 rows of 2 cores each
                for (let row = 0; row < 4; row++) {
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'cpu-row';

                    for (let coreInRow = 0; coreInRow < 2; coreInRow++) {
                        const coreIndex = row * 2 + coreInRow;
                        const coreUsage = cores[coreIndex] || 0;

                        const coreDiv = document.createElement('div');
                        coreDiv.className = 'cpu-core';

                        // Create 8 squares per core
                        for (let j = 0; j < 8; j++) {
                            const square = document.createElement('div');
                            square.className = 'cpu-square';
                            // Light up square if usage percentage is high enough for this square
                            const squareThreshold = (j / 8) * 100;
                            if (coreUsage > squareThreshold) {
                                square.classList.add('active');
                            }
                            coreDiv.appendChild(square);
                        }

                        rowDiv.appendChild(coreDiv);

                        // Add spacer between cores in the same row
                        if (coreInRow === 0) {
                            const spacer = document.createElement('div');
                            spacer.style.width = '12px';
                            rowDiv.appendChild(spacer);
                        }
                    }

                    cpuGrid.appendChild(rowDiv);
                }

                document.getElementById('cpu-name').textContent = data.cpu.cores + ' - ' + data.cpu.usage_percent.toFixed(1) + '%';

                // RAM bar
                const ramPercent = data.ram.usage_percent;
                const ramUsedGb = (ramPercent * data.ram.total_gb / 100).toFixed(1);
                document.getElementById('ram-bar-used').style.width = ramPercent + '%';
                document.getElementById('ram-usage').textContent = ramPercent.toFixed(1) + '% (' + ramUsedGb + 'GB / ' + data.ram.total_gb.toFixed(1) + 'GB)';

                // GPU
                const gpuText = data.gpu.available ? data.gpu.usage_percent.toFixed(1) + '% (' + data.gpu.model + ')' : 'Not available';
                document.getElementById('gpu-status').textContent = gpuText;

                // Services
                document.getElementById('minecraft-status').textContent = data.minecraft_healthy ? 'Running' : 'Offline';
                document.getElementById('api-status').textContent = 'Online';

                // BlueMap check
                fetch('/proxy/dynmap/', { method: 'GET' })
                    .then(r => {
                        document.getElementById('bluemap-status').textContent = r.ok ? 'Active' : 'Inactive';
                    })
                    .catch(() => {
                        document.getElementById('bluemap-status').textContent = 'Inactive';
                    });
            })
            .catch(error => {
                console.error('Failed to fetch status:', error);
            });
    }

    // Load status on page load
    document.addEventListener('DOMContentLoaded', refreshStatus);
    </script>
</head>
<body>
    <h1>Gabrielpenman.com</h1>
    <div class="posts">
"""
        
        for page in top_level_pages:
            asset_info = ""
            if page['assets']:
                asset_info = f"<div class=\"assets-info\">{len(page['assets'])} assets included</div>"
            
            subpages = subpages_map.get(page['slug'], [])
            
            homepage_html += f"""        <article>
            <h2><a href="{page['slug']}">{page['title']}</a></h2>
            <div class="date">{page['date']}</div>
            <div class="description">{page['description']}</div>
            <div class="categories">Categories: {', '.join(page['categories'])}</div>
            {asset_info}"""
            
            if subpages:
                # Show subpages, with collapse if more than 5
                should_collapse = len(subpages) > 5
                collapse_class = " collapsed" if should_collapse else ""
                
                if should_collapse:
                    homepage_html += f"""
            <button class="subpage-toggle" id="toggle-{page['slug']}" onclick="toggleSubpages('{page['slug']}')">Show subpages ▼</button>"""
                
                homepage_html += f"""
            <div class="subpages{collapse_class}" id="subpages-{page['slug']}">"""
                
                for subpage in subpages:
                    # Create a clean subpage title
                    subpage_title = subpage['title']
                    
                    # Remove parent title prefix if it exists
                    if page['title'] in subpage_title:
                        subpage_title = subpage_title.replace(page['title'], '').strip(' -')
                    
                    # If title is empty or too similar, use the path name
                    if not subpage_title or subpage_title.lower() == page['title'].lower():
                        path_name = subpage['slug'].split('/')[-1]
                        subpage_title = path_name.replace('-', ' ').title()
                    
                    homepage_html += f"""
                <div class="subpage-item">
                    <a href="{subpage['slug']}">
                        <span>→</span>
                        <span>{subpage_title}</span>
                    </a>
                </div>"""
                
                homepage_html += """
            </div>"""
            
            homepage_html += """
        </article>
"""
        
        homepage_html += """    </div>

    <div class="status-section">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0;">System Status</h3>
            <button onclick="refreshStatus()" style="padding: 6px 12px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9em;">Refresh</button>
        </div>
        <div class="status-item">
            <span class="status-dot"></span>
            <span class="status-label">Minecraft:</span>
            <span id="minecraft-status">Loading...</span>
        </div>
        <div class="status-item">
            <span class="status-dot"></span>
            <span class="status-label">API:</span>
            <span id="api-status">Loading...</span>
        </div>
        <div class="status-item">
            <span class="status-dot"></span>
            <span class="status-label">BlueMap:</span>
            <span id="bluemap-status">Loading...</span>
        </div>
        <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
        <div class="status-item">
            <span class="status-label">CPU:</span>
            <span id="cpu-name">Loading...</span>
        </div>
        <div style="margin: 12px 0 12px 108px;">
            <div class="cpu-grid" id="cpu-grid">
                <!-- 8 cores x 8 squares = 64 squares total -->
            </div>
        </div>
        <div class="status-item">
            <span class="status-label">RAM:</span>
            <div style="display: flex; gap: 8px; align-items: center;">
                <div class="ram-bar">
                    <div class="ram-used" id="ram-bar-used" style="width: 0%;"></div>
                </div>
                <span id="ram-usage">Loading...</span>
            </div>
        </div>
        <div class="status-item">
            <span class="status-label">GPU:</span>
            <span id="gpu-status">Loading...</span>
        </div>
    </div>

    <footer style="margin-top: 50px; text-align: center; color: #7f8c8d; font-size: 0.9em;">
        <p>Email me at gabrielpenman@gmail.com • <a href="/api/health">API Status</a></p>
    </footer>
</body>
</html>"""
        
        # Write homepage
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(homepage_html)
    
    def compile_all(self):
        """Compile all pages and generate homepage"""
        print("=== Modular Blog Compiler ===")
        print("Cleaning output directory...")
        self.clean_output()
        
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