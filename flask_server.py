#!/usr/bin/env python3
"""
Flask server that automatically registers API endpoints from page modules.
Each page can define its own Flask blueprint in api.py.
"""

import os
import sys
import importlib.util
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

class BlogFlaskServer:
    def __init__(self, pages_dir="pages", static_dir="output", port=5000):
        self.pages_dir = Path(pages_dir)
        self.static_dir = Path(static_dir)
        self.port = port
        self.app = Flask(__name__)
        
        # Enable CORS for API endpoints
        CORS(self.app)
        
        # Setup basic routes
        self._setup_basic_routes()
        
        # Auto-register page API endpoints
        self._register_page_apis()
    
    def _setup_basic_routes(self):
        """Setup basic Flask routes"""
        
        @self.app.route('/')
        def serve_homepage():
            """Serve the homepage"""
            try:
                return send_from_directory(self.static_dir, 'index.html')
            except FileNotFoundError:
                return jsonify({'error': 'Homepage not found. Run compile.py first.'}), 404
        
        @self.app.route('/<path:filename>')
        def serve_static(filename):
            """Serve static HTML files and assets"""
            try:
                return send_from_directory(self.static_dir, filename)
            except FileNotFoundError:
                return jsonify({'error': f'File {filename} not found'}), 404
        
        @self.app.route('/api/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'pages_loaded': len(self._get_page_directories()),
                'static_dir': str(self.static_dir),
                'pages_dir': str(self.pages_dir)
            })
        
        @self.app.route('/api/pages')
        def list_pages():
            """List all available pages"""
            pages = []
            for page_dir in self._get_page_directories():
                config_file = page_dir / 'config.json'
                if config_file.exists():
                    try:
                        import json
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                            pages.append({
                                'slug': config.get('slug', page_dir.name),
                                'title': config.get('title', page_dir.name),
                                'description': config.get('description', ''),
                                'categories': config.get('categories', []),
                                'date': config.get('date', ''),
                                'has_api': (page_dir / 'api.py').exists(),
                                'has_assets': (page_dir / 'assets').exists()
                            })
                    except (json.JSONDecodeError, IOError):
                        continue
            
            # Sort by date (newest first)
            pages.sort(key=lambda x: x.get('date', ''), reverse=True)
            return jsonify({'pages': pages})
    
    def _get_page_directories(self):
        """Get all page directories"""
        if not self.pages_dir.exists():
            return []
        
        page_dirs = []
        for item in self.pages_dir.iterdir():
            if item.is_dir() and (item / 'config.json').exists():
                page_dirs.append(item)
        
        return page_dirs
    
    def _register_page_apis(self):
        """Auto-register API endpoints from page modules"""
        registered_pages = []
        
        for page_dir in self._get_page_directories():
            api_file = page_dir / 'api.py'
            
            if api_file.exists():
                try:
                    # Load the page's API module
                    spec = importlib.util.spec_from_file_location(
                        f"pages.{page_dir.name}.api", 
                        str(api_file)
                    )
                    api_module = importlib.util.module_from_spec(spec)
                    
                    # Add the shared module to Python path so imports work
                    if str(Path.cwd()) not in sys.path:
                        sys.path.insert(0, str(Path.cwd()))
                    
                    spec.loader.exec_module(api_module)
                    
                    # Register the blueprint if it exists
                    if hasattr(api_module, 'bp'):
                        self.app.register_blueprint(api_module.bp)
                        registered_pages.append(page_dir.name)
                        print(f"Registered API endpoints for page: {page_dir.name}")
                    else:
                        print(f"Warning: {api_file} doesn't have a 'bp' blueprint")
                
                except Exception as e:
                    print(f"Error loading API for page {page_dir.name}: {e}")
        
        print(f"Successfully registered APIs for {len(registered_pages)} pages")
        return registered_pages
    
    def _serve_page_assets(self, page_slug, asset_path):
        """Serve assets for a specific page"""
        page_dir = self.pages_dir / page_slug
        assets_dir = page_dir / 'assets'
        
        if not assets_dir.exists():
            return jsonify({'error': 'Assets directory not found'}), 404
        
        try:
            return send_from_directory(assets_dir, asset_path)
        except FileNotFoundError:
            return jsonify({'error': f'Asset {asset_path} not found'}), 404
    
    def setup_asset_routes(self):
        """Setup routes for serving page assets"""
        @self.app.route('/assets/<page_slug>/<path:asset_path>')
        def serve_page_assets(page_slug, asset_path):
            return self._serve_page_assets(page_slug, asset_path)
    
    def run(self, debug=True):
        """Run the Flask server"""
        # Setup asset routes
        self.setup_asset_routes()
        
        print(f"Starting Flask server on port {self.port}")
        print(f"Static files served from: {self.static_dir}")
        print(f"Pages directory: {self.pages_dir}")
        print(f"API base URL: http://localhost:{self.port}/api/")
        print(f"Assets URL pattern: http://localhost:{self.port}/assets/<page>/<file>")
        
        self.app.run(
            host='0.0.0.0',
            port=self.port,
            debug=debug
        )

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Run the blog Flask server")
    parser.add_argument("--port", "-p", type=int, default=5000, 
                       help="Port to run on (default: 5000)")
    parser.add_argument("--pages", default="pages", 
                       help="Pages directory (default: pages)")
    parser.add_argument("--static", default="output", 
                       help="Static files directory (default: output)")
    parser.add_argument("--no-debug", action="store_true", 
                       help="Disable debug mode")
    
    args = parser.parse_args()
    
    server = BlogFlaskServer(
        pages_dir=args.pages,
        static_dir=args.static,
        port=args.port
    )
    
    server.run(debug=not args.no_debug)

if __name__ == "__main__":
    main()