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
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_socketio import SocketIO
import psutil
import platform
import subprocess
from datetime import datetime
import socket

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

    def _check_port_open(self, port, host='localhost', timeout=1):
        """Check if a port is open on the local machine"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _get_process_cpu_by_port(self, port):
        """Get CPU usage of process listening on a specific port"""
        try:
            # Use netstat/ss to find the PID listening on the port
            result = subprocess.run(
                ['lsof', '-i', f':{port}', '-t'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                pid = int(result.stdout.strip().split('\n')[0])
                # Get CPU usage for this process
                proc = psutil.Process(pid)
                cpu_usage = proc.cpu_percent(interval=0.1)
                return cpu_usage
        except (FileNotFoundError, ValueError, psutil.NoSuchProcess, subprocess.TimeoutExpired):
            pass
        return None
    
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
            """Serve static HTML files (assets handled by nginx in production)"""
            # Skip API routes (they're handled by blueprints)
            if filename.startswith('api/'):
                return jsonify({'error': f'File {filename} not found'}), 404
            
            # In production, assets are served by nginx directly
            # Only allow Flask to serve assets in development (when nginx not present)
            if filename.startswith('assets/'):
                # Check if we're in production by looking for nginx headers
                is_production = 'X-Real-IP' in request.headers or 'X-Forwarded-For' in request.headers
                if is_production:
                    return jsonify({'error': 'Assets should be served by nginx in production'}), 404
                # Development mode - allow Flask to serve assets for convenience
            
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
        
        @self.app.route('/test-asset')
        def test_asset():
            """Test route to check if routing works"""
            return jsonify({'message': 'Asset routing test successful'})
            
        @self.app.route('/api/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'pages_loaded': len(self._get_page_directories()),
                'static_dir': str(self.static_dir),
                'pages_dir': str(self.pages_dir)
            })

        @self.app.route('/api/server-details')
        def server_details():
            """Get server hardware and usage details"""
            try:
                # CPU info
                cpu_count = psutil.cpu_count(logical=False)
                cpu_logical = psutil.cpu_count(logical=True)
                cpu_model = platform.processor() or "Unknown"
                cpu_usage = psutil.cpu_percent(interval=0.1)

                # Get per-core CPU usage
                cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)

                cpu_info = {
                    'model': cpu_model,
                    'cores': f"{cpu_count} cores / {cpu_logical} threads" if cpu_count else f"{cpu_logical} threads",
                    'usage_percent': round(cpu_usage, 1),
                    'per_core': [round(core, 1) for core in cpu_per_core]
                }

                # RAM info
                ram = psutil.virtual_memory()
                ram_info = {
                    'total_gb': round(ram.total / (1024**3), 1),
                    'usage_percent': round(ram.percent, 1)
                }

                # GPU info - try nvidia-smi
                gpu_info = {
                    'available': False,
                    'model': None,
                    'memory_gb': None,
                    'usage_percent': None
                }

                try:
                    result = subprocess.run(
                        ['nvidia-smi', '--query-gpu=name,memory.total,utilization.gpu', '--format=csv,noheader'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        gpu_line = result.stdout.strip().split('\n')[0]
                        parts = gpu_line.split(',')
                        if len(parts) >= 3:
                            gpu_info = {
                                'available': True,
                                'model': parts[0].strip(),
                                'memory_gb': parts[1].strip(),
                                'usage_percent': round(float(parts[2].strip().rstrip('%')), 1)
                            }
                except (FileNotFoundError, subprocess.TimeoutExpired, ValueError, IndexError):
                    pass

                # OS info
                os_info = platform.platform()

                # Check Minecraft server on port 25565
                minecraft_healthy = self._check_port_open(25565)
                minecraft_cpu = self._get_process_cpu_by_port(25565) if minecraft_healthy else None

                # Get API (Flask) CPU usage - check port we're running on
                api_cpu = self._get_process_cpu_by_port(self.port)

                return jsonify({
                    'cpu': cpu_info,
                    'ram': ram_info,
                    'gpu': gpu_info,
                    'os': os_info,
                    'minecraft_healthy': minecraft_healthy,
                    'minecraft_cpu': minecraft_cpu,
                    'api_cpu': api_cpu,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                })
            except Exception as e:
                return jsonify({
                    'error': 'Failed to retrieve server details',
                    'details': str(e)
                }), 500

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

        @self.app.route('/api/dev/restart-services', methods=['POST'])
        def restart_dev_services():
            """
            Restart geo-butler development services (Firebase emulators and Next.js dev server)
            Requires admin token for security
            """
            # Check for admin authorization token
            auth_token = request.headers.get('X-Admin-Token')
            admin_token = os.environ.get('DEV_ADMIN_TOKEN', 'dev-restart-token')

            if not auth_token or auth_token != admin_token:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Missing or invalid X-Admin-Token header'
                }), 403

            try:
                # Restart the geo-butler-dev systemd service
                result = subprocess.run(
                    ['sudo', '-S', 'systemctl', 'restart', 'geo-butler-dev.service'],
                    input='01022366\n',  # sudo password piped in (string, not bytes)
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    return jsonify({
                        'success': True,
                        'message': 'Development services restarting',
                        'service': 'geo-butler-dev.service',
                        'timestamp': datetime.utcnow().isoformat() + 'Z',
                        'details': 'Firebase emulators and Next.js dev server will restart in ~5-10 seconds'
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Failed to restart service',
                        'stderr': result.stderr,
                        'stdout': result.stdout
                    }), 500

            except subprocess.TimeoutExpired:
                return jsonify({
                    'error': 'Restart command timed out',
                    'message': 'Service restart is taking too long'
                }), 500
            except Exception as e:
                return jsonify({
                    'error': 'Failed to restart services',
                    'details': str(e)
                }), 500

        @self.app.route('/api/dev/services-status', methods=['GET'])
        def check_dev_services_status():
            """
            Check status of development services
            Returns port availability for Firebase emulators and Next.js dev server
            """
            ports = {
                'nextjs_dev': 3000,
                'firebase_functions': 5001,
                'firebase_hosting': 5002,
                'firestore_emulator': 8081,
                'auth_emulator': 9099,
                'pubsub_emulator': 8085,
            }

            status = {}
            for service_name, port in ports.items():
                is_open = self._check_port_open(port)
                status[service_name] = {
                    'port': port,
                    'running': is_open,
                    'url': f'http://localhost:{port}' if is_open else None
                }

            all_healthy = all(s['running'] for s in status.values())

            return jsonify({
                'all_healthy': all_healthy,
                'services': status,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })

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