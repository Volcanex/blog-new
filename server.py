#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
from pathlib import Path

class BlogServer:
    def __init__(self, port=8000, directory="output"):
        self.port = port
        self.directory = Path(directory)
        
    def start(self):
        """Start the HTTP server"""
        if not self.directory.exists():
            print(f"Error: Output directory '{self.directory}' does not exist.")
            print("Run compile.py first to generate the site.")
            sys.exit(1)
        
        # Change to output directory
        os.chdir(self.directory)
        
        # Create server
        handler = http.server.SimpleHTTPRequestHandler
        
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"Serving blog at http://localhost:{self.port}")
                print("Press Ctrl+C to stop the server")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Error: Port {self.port} is already in use.")
                print("Try a different port or stop the existing server.")
            else:
                print(f"Error starting server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Serve the blog")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--dir", "-d", default="output", help="Directory to serve (default: output)")
    
    args = parser.parse_args()
    
    server = BlogServer(port=args.port, directory=args.dir)
    server.start()