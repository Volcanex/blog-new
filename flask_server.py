#!/usr/bin/env python3
"""
Flask server that automatically registers API endpoints from page modules.
Each page can define its own Flask blueprint in api.py.
Includes WebSocket support for real-time features.
"""

import os
import sys
import importlib.util
from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

class BlogFlaskServer:
    def __init__(self, pages_dir="pages", static_dir="output", port=5000):
        self.pages_dir = Path(pages_dir)
        self.static_dir = Path(static_dir)
        self.port = port
        self.app = Flask(__name__)
        
        # Enable CORS for API endpoints
        CORS(self.app)
        
        # Initialize SocketIO with CORS support
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Setup basic routes
        self._setup_basic_routes()
        
        # Auto-register page API endpoints and WebSocket handlers
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
            # Skip API routes (they're handled by blueprints)
            if filename.startswith('api/'):
                return jsonify({'error': f'File {filename} not found'}), 404
            
            # First try the exact filename (must be a file, not directory)
            file_path = self.static_dir / filename
            if file_path.exists() and file_path.is_file():
                return send_from_directory(str(self.static_dir), filename)
            
            # If not found and no extension, try looking for directory/index.html
            if '.' not in filename:
                index_path = self.static_dir / filename / "index.html"
                if index_path.exists():
                    return send_from_directory(str(self.static_dir / filename), "index.html")
            
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
        """Auto-register API endpoints and WebSocket handlers from page modules"""
        registered_pages = []
        registered_routes = {}  # Track routes for collision detection
        
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
                        # Check for route collisions before registering
                        blueprint = api_module.bp
                        page_routes = []
                        
                        # Register first, then check routes from Flask app
                        self.app.register_blueprint(blueprint)
                        
                        # Check for route collisions by examining all registered routes
                        for rule in self.app.url_map.iter_rules():
                            if rule.endpoint.startswith(f"{blueprint.name}."):
                                route_path = rule.rule
                                page_routes.append(route_path)
                                
                                # Check for collisions (excluding the blueprint prefix)
                                base_route = route_path.replace(blueprint.url_prefix or '', '') if blueprint.url_prefix else route_path
                                collision_key = f"{base_route}#{rule.methods}"
                                
                                if collision_key in registered_routes and registered_routes[collision_key] != page_dir.name:
                                    print(f"⚠️  WARNING: Route collision detected!")
                                    print(f"   Route: {route_path} {rule.methods}")
                                    print(f"   Page '{page_dir.name}' conflicts with page '{registered_routes[collision_key]}'")
                                    print(f"   Recommendation: Use page-specific route names")
                                else:
                                    registered_routes[collision_key] = page_dir.name
                        
                        registered_pages.append(page_dir.name)
                        print(f"Registered API endpoints for page: {page_dir.name}")
                        if page_routes:
                            print(f"  Routes: {', '.join(page_routes)}")
                    else:
                        print(f"Warning: {api_file} doesn't have a 'bp' blueprint")
                    
                    # Register WebSocket handlers if they exist
                    if hasattr(api_module, 'register_websocket_handlers'):
                        try:
                            api_module.register_websocket_handlers(self.socketio)
                            print(f"Registered WebSocket handlers for page: {page_dir.name}")
                        except Exception as ws_error:
                            print(f"Error registering WebSocket handlers for {page_dir.name}: {ws_error}")
                
                except Exception as e:
                    print(f"Error loading API for page {page_dir.name}: {e}")
        
        print(f"Successfully registered APIs for {len(registered_pages)} pages")
        if any("⚠️" in line for line in []):  # This will show warnings if any were printed above
            print("\n🔍 Endpoint Collision Check Complete - Review warnings above")
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
        
        print(f"Starting Flask server with WebSocket support on port {self.port}")
        print(f"Static files served from: {self.static_dir}")
        print(f"Pages directory: {self.pages_dir}")
        print(f"API base URL: http://localhost:{self.port}/api/")
        print(f"WebSocket URL: http://localhost:{self.port}")
        print(f"Assets URL pattern: http://localhost:{self.port}/assets/<page>/<file>")
        
        # Use socketio.run instead of app.run for WebSocket support
        self.socketio.run(
            self.app,
            host='0.0.0.0',
            port=self.port,
            debug=debug,
            allow_unsafe_werkzeug=True
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