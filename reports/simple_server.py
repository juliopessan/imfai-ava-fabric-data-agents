#!/usr/bin/env python3
"""
Simple Static File Server for Einstein-HIAE Dashboards
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
        
        # Handle root request - serve INDEX.html from einstein-hiae
        if path == "/" or path == "":
            self.path = "/reports/einstein-hiae/INDEX.html"
        
        # Handle einstein-hiae dashboard requests
        elif path.startswith("/einstein-hiae/"):
            self.path = f"/reports{path}"
        
        # Handle direct dashboards access
        elif path.startswith("/einstein-"):
            self.path = f"/reports/einstein-hiae{path}"
        
        # Add index.html for directories
        elif path.endswith("/") and not path.endswith("einstein-hiae/"):
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
║                   EINSTEIN-HIAE DASHBOARD SERVER                  ║
║                                                                    ║
║  📊 http://localhost:{PORT}                                        ║
║  📊 http://localhost:{PORT}/einstein-hiae/                        ║
║  📊 http://localhost:{PORT}/einstein-executive-dashboard.html     ║
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
