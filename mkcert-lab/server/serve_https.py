#!/usr/bin/env python3
"""A tiny HTTPS server for the mkcert lab.

Serves one fixed page over TLS on https://127.0.0.1:18443 (and ::1 where
available), using a certificate and key named on the command line:

    python3 serve_https.py CERT.pem KEY.pem [PORT]

It prints each request it receives, so a transcript can show that the
client really did complete the handshake and ask for the page.
"""
import http.server
import ssl
import sys

CERT, KEY = sys.argv[1], sys.argv[2]
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 18443

PAGE = (
    "Hello from the mkcert lab server.\n"
    "If your client shows this without a warning, it trusted the certificate.\n"
).encode()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"server saw: {self.requestline}", flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()
        self.wfile.write(PAGE)

    def log_message(self, *args):  # keep the transcript clean
        pass


ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
server.socket = ctx.wrap_socket(server.socket, server_side=True)
print(f"serving on https://127.0.0.1:{PORT} with cert {CERT}", flush=True)
server.serve_forever()
