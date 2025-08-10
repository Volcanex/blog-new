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
        """Get all valid page directories"""
        if not self.pages_dir.exists():
            return []
        
        page_dirs = []
        for item in self.pages_dir.iterdir():
            if item.is_dir():
                config_file = item / 'config.json'
                content_file = item / 'content.md'
                
                if config_file.exists() and content_file.exists():
                    page_dirs.append(item)
                else:
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
            
            # Extract CSS and HTML sections (same logic as before)
            html_start = content.find('<html>')
            css_start = content.find('<style>')
            
            if html_start == -1:
                raise ValueError(f"No HTML section found in {content_file}")
            
            html_content = content[html_start:]
            css_content = ""
            
            if css_start != -1:
                css_end = content.find('</style>') + 8
                css_content = content[css_start:css_end]
                # Remove CSS from HTML content
                html_content = content[:css_start] + content[css_end:]
                html_content = html_content.strip()
            
            return html_content, css_content
            
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
        html_content, css_content = self.parse_page_content(page_dir)
        
        # Copy page assets
        assets = self.copy_page_assets(page_dir, config.get('slug', page_dir.name))
        if assets:
            print(f"  Copied {len(assets)} assets for {page_dir.name}")
        
        # Create full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.get('title', 'Blog Post')}</title>
    {css_content}
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Determine output filename
        slug = config.get('slug', page_dir.name)
        output_file = self.output_dir / f"{slug}.html"
        
        # Write compiled page
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Create extensionless version for URL-friendly access
        extensionless_dir = self.output_dir / slug
        extensionless_dir.mkdir(exist_ok=True)
        extensionless_file = extensionless_dir / "index.html"
        with open(extensionless_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Track categories
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
        
        # Sort by date (newest first)
        pages_list.sort(key=lambda x: x['date'], reverse=True)
        
        # Generate homepage HTML (same as before, with asset info)
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
    }
    </style>
</head>
<body>
    <h1>Gabrielpenman.com</h1>
    <div class="posts">
"""
        
        for page in pages_list:
            asset_info = ""
            if page['assets']:
                asset_info = f"<div class=\"assets-info\">{len(page['assets'])} assets included</div>"
            
            homepage_html += f"""        <article>
            <h2><a href="{page['slug']}">{page['title']}</a></h2>
            <div class="date">{page['date']}</div>
            <div class="description">{page['description']}</div>
            <div class="categories">Categories: {', '.join(page['categories'])}</div>
            {asset_info}
        </article>
"""
        
        homepage_html += """    </div>
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