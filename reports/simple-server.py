#!/usr/bin/env python3
"""
Simple HTTP Server for serving dashboards
No external dependencies required - uses Python built-in http.server
"""

import http.server
import socketserver
import os
from pathlib import Path
import argparse
import sys

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for serving dashboards"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Serve index for root
        if self.path == '/':
            self.path = '/index.html'
        
        # Log request
        print(f"📨 {self.command} {self.path}")
        
        # Call parent implementation
        return super().do_GET()
    
    def end_headers(self):
        """Add custom headers"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        return super().end_headers()

def main():
    parser = argparse.ArgumentParser(description='Dashboard Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    args = parser.parse_args()
    
    # Change to reports directory
    os.chdir(Path(__file__).parent)
    
    port = args.port
    handler = DashboardHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("\n" + "="*70)
        print("🚀 DASHBOARD SERVER STARTED")
        print("="*70)
        print(f"\n📊 Serving dashboards from: {Path.cwd()}")
        print(f"\n🌐 Access dashboard at:")
        print(f"   ✓ Main:      http://{args.host}:{port}/")
        print(f"   ✓ Bradesco:  http://{args.host}:{port}/bradesco/")
        print(f"   ✓ Executive: http://{args.host}:{port}/bradesco/bradesco-executive-dashboard.html")
        print(f"   ✓ 3-Tier:    http://{args.host}:{port}/bradesco/bradesco-3tier-dashboard.html")
        print(f"   ✓ ROI:       http://{args.host}:{port}/bradesco/ROI_ANALYSIS_VISUAL.html")
        print(f"\n⚠️  Press Ctrl+C to stop")
        print("="*70 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped")
            sys.exit(0)

if __name__ == "__main__":
    main()
