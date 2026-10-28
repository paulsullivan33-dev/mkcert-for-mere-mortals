#!/usr/bin/env python3
"""A small HTTPS client for the mkcert lab.

    python3 check_https.py URL [CAFILE]

With no CAFILE it uses the client's default trust (which does not know
the mkcert root, so the check is expected to fail). With CAFILE it
trusts exactly that root certificate file.
"""
import ssl
import sys
import urllib.request

url = sys.argv[1]
if len(sys.argv) > 2:
    ctx = ssl.create_default_context(cafile=sys.argv[2])
else:
    ctx = ssl.create_default_context()
try:
    with urllib.request.urlopen(url, context=ctx) as r:
        print(f"HTTP {r.status}")
        print(r.read().decode(), end="")
except Exception as e:
    print(f"FAILED: {type(e).__name__}: {e}")
    sys.exit(1)
