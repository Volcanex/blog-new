#!/usr/bin/env python3
import os
import json
import shutil
from pathlib import Path

class BlogCompiler:
    def __init__(self, pages_dir="pages", output_dir="output"):
        self.pages_dir = Path(pages_dir)
        self.output_dir = Path(output_dir)
        self.categories = {}
        
    def clean_output(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_page(self, page_path):
        """Parse a page file and extract metadata, HTML, and CSS"""
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata (JSON block at the top)
        if not content.startswith('---\n'):
            raise ValueError(f"Page {page_path} must start with metadata block")
        
        end_meta = content.find('\n---\n')
        if end_meta == -1:
            raise ValueError(f"Page {page_path} metadata block not properly closed")
        
        metadata_str = content[4:end_meta]
        remaining_content = content[end_meta + 5:]
        
        try:
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON metadata in {page_path}: {e}")
        
        # Extract HTML and CSS sections
        html_start = remaining_content.find('<html>')
        css_start = remaining_content.find('<style>')
        
        if html_start == -1:
            raise ValueError(f"No HTML section found in {page_path}")
        
        html_content = remaining_content[html_start:]
        css_content = ""
        
        if css_start != -1:
            css_end = remaining_content.find('</style>') + 8
            css_content = remaining_content[css_start:css_end]
            # Remove CSS from HTML content
            html_content = remaining_content[:css_start] + remaining_content[css_end:]
            html_content = html_content.strip()
        
        return metadata, html_content, css_content
    
    def compile_page(self, page_path):
        """Compile a single page"""
        metadata, html, css = self.parse_page(page_path)
        
        # Create full HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata.get('title', 'Blog Post')}</title>
    {css}
</head>
<body>
    {html}
</body>
</html>"""
        
        # Determine output filename
        slug = metadata.get('slug', page_path.stem)
        output_file = self.output_dir / f"{slug}.html"
        
        # Write compiled page
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Track categories
        categories = metadata.get('categories', [])
        for category in categories:
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append({
                'title': metadata.get('title', 'Untitled'),
                'slug': slug,
                'date': metadata.get('date', ''),
                'description': metadata.get('description', '')
            })
        
        return metadata, slug
    
    def generate_homepage(self):
        """Generate a simple homepage listing all posts"""
        pages_list = []
        
        # Collect all pages
        for page_file in self.pages_dir.glob('*.md'):
            try:
                metadata, slug = self.compile_page(page_file)
                pages_list.append({
                    'title': metadata.get('title', 'Untitled'),
                    'slug': slug,
                    'date': metadata.get('date', ''),
                    'description': metadata.get('description', ''),
                    'categories': metadata.get('categories', [])
                })
            except Exception as e:
                print(f"Error compiling {page_file}: {e}")
        
        # Sort by date (newest first)
        pages_list.sort(key=lambda x: x['date'], reverse=True)
        
        # Generate homepage HTML
        homepage_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
</head>
<body>
    <h1>Blog</h1>
    <div class="posts">
"""
        
        for page in pages_list:
            homepage_html += f"""        <article>
            <h2><a href="{page['slug']}.html">{page['title']}</a></h2>
            <p class="date">{page['date']}</p>
            <p class="description">{page['description']}</p>
            <p class="categories">Categories: {', '.join(page['categories'])}</p>
        </article>
"""
        
        homepage_html += """    </div>
</body>
</html>"""
        
        # Write homepage
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(homepage_html)
    
    def compile_all(self):
        """Compile all pages and generate homepage"""
        print("Cleaning output directory...")
        self.clean_output()
        
        print("Generating homepage...")
        self.generate_homepage()
        
        print("Compilation complete!")
        print(f"Generated {len(list(self.output_dir.glob('*.html')))} pages")
        if self.categories:
            print(f"Categories found: {', '.join(self.categories.keys())}")

if __name__ == "__main__":
    compiler = BlogCompiler()
    compiler.compile_all()