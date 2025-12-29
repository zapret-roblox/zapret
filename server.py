#!/usr/bin/env python3
"""
Render-compatible file server
Serves zapret.rar at /zapret.rar
"""

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


BASE_DIR = Path(__file__).parent
FILE_NAME = "zapret-IUHWBAOP.rar"
FILE_PATH = BASE_DIR / FILE_NAME


class FileHandler(SimpleHTTPRequestHandler):
    def _send_headers(self, file_size: int):
        self.send_response(200)
        self.send_header("Content-Type", "application/x-rar-compressed")
        self.send_header(
            "Content-Disposition",
            f'attachment; filename="{FILE_NAME}"'
        )
        self.send_header("Content-Length", str(file_size))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_HEAD(self):
        if self.path == f"/{FILE_NAME}" and FILE_PATH.exists():
            self._send_headers(FILE_PATH.stat().st_size)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path == f"/{FILE_NAME}":
            if not FILE_PATH.exists():
                self.send_response(404)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"File not found")
                return

            self._send_headers(FILE_PATH.stat().st_size)
            with open(FILE_PATH, "rb") as f:
                self.wfile.write(f.read())
        else:
            # простой health-check для Render
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")


def run_server():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    httpd = HTTPServer((host, port), FileHandler)
    print(f"[+] Server running on {host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
