"""
AI Agent Platform - Interactive UI Launcher (Windows Compatible)
Opens the deployment dashboard in your browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if index.html exists
    if not Path('index.html').exists():
        print("=" * 60)
        print("ERROR: index.html not found!")
        print("=" * 60)
        print("\nPlease download index.html from the outputs folder.")
        print("It should be in the same directory as this script.\n")
        sys.exit(1)
    
    print("=" * 60)
    print("AI AGENT PLATFORM - INTERACTIVE DEPLOYMENT UI")
    print("=" * 60)
    print(f"\n🚀 Starting server on http://localhost:{PORT}")
    print("\n📊 Opening deployment dashboard in browser...")
    print("\n🤖 Click 'DEPLOY AGENTS' button to start deployment")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 60)
    
    # Open browser
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    
    # Start server
    Handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"\n✓ Server running at http://localhost:{PORT}/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped")

if __name__ == "__main__":
    main()
