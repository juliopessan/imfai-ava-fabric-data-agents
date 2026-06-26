#!/usr/bin/env python3
"""
Simple Static File Server for Reference-Sa�de Dashboards
Serves HTML files from reports/ directory without dependencies
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path
from urllib.parse import unquote

PORT = 8888
HOST = "127.0.0.1"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for serving dashboards from reports/ directory"""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve from
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        # Decode URL
        path = unquote(self.path)
        
        # Handle root request - serve INDEX.html from Reference-Sa�de
        if path == "/" or path == "":
            self.path = "/reports/Reference-Sa�de/INDEX.html"
        
        # Handle Reference-Sa�de dashboard requests
        elif path.startswith("/Reference-Sa�de/"):
            self.path = f"/reports{path}"
        
        # Handle direct dashboards access
        elif path.startswith("/reference-"):
            self.path = f"/reports/Reference-Sa�de{path}"
        
        # Add index.html for directories
        elif path.endswith("/") and not path.endswith("Reference-Sa�de/"):
            if not path.endswith("index.html"):
                self.path = path + "index.html"
        
        # Serve the file
        return super().do_GET()
    
    def end_headers(self):
        """Add headers for CORS and caching"""
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    """Start the dashboard server"""
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"""
╔════════════════════════════════════════════════════════════════════╗
║                   Reference-Sa�de DASHBOARD SERVER                  ║
║                                                                    ║
║  📊 http://localhost:{PORT}                                        ║
║  📊 http://localhost:{PORT}/Reference-Sa�de/                        ║
║  📊 http://localhost:{PORT}/reference-executive-dashboard.html     ║
║                                                                    ║
║  Press Ctrl+C to stop                                             ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}/")
        print(f"📁 Serving from: {project_root}")
        print(f"🎯 Open http://localhost:{PORT} in browser\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✋ Server stopped")
            sys.exit(0)


if __name__ == "__main__":
    main()
