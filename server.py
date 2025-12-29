#!/usr/bin/env python3
"""
Simple file server to serve zapret.rar
Run: python server.py
Then access: http://localhost:8000/zapret.rar
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class FileHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/zapret.rar':
            file_path = Path(__file__).parent / 'zapret.rar'
            
            if not file_path.exists():
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'File not found: zapret.rar')
                print(f"[!] File not found: {file_path}")
                return
            
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/x-rar-compressed')
                self.send_header('Content-Disposition', 'attachment; filename="zapret.rar"')
                self.send_header('Content-Length', str(file_path.stat().st_size))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                
                print(f"[+] Served: zapret.rar ({file_path.stat().st_size} bytes)")
            except Exception as e:
                print(f"[!] Error serving file: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            super().do_GET()

def run_server(host='localhost', port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, FileHandler)
    print(f"[+] Server started at http://{host}:{port}")
    print(f"[+] Download zapret.rar at: http://{host}:{port}/zapret.rar")
    print(f"[+] Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] Server stopped")
        sys.exit(0)

if __name__ == '__main__':
    run_server()
