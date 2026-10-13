"""Owner-controlled, loopback-only FREE_ONLY one-shot wake relay.

Must sit behind a separately reviewed TLS reverse-proxy rule. It accepts no
target URL, media URL, job payload, path, or command from callers.
"""
from __future__ import annotations

import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

_TARGET = "https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health"
_PATH = "/krc-wake/v1"
_COOLDOWN_SECONDS = 90.0

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

class RateGate:
    def __init__(self):
        self._lock = Lock()
        self._next_at = 0.0
    def acquire(self) -> bool:
        with self._lock:
            now = monotonic()
            if now < self._next_at:
                return False
            self._next_at = now + _COOLDOWN_SECONDS
            return True

class Handler(BaseHTTPRequestHandler):
    token: str
    gate: RateGate
    def log_message(self, *_args):
        pass
    def reply(self, status: int, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        self.reply(405, b'{"status":"invalid_method"}')
    def do_POST(self):
        # All invalid requests share a low-information response, no secrets logged.
        auth = self.headers.get("Authorization", "")
        if (self.path != _PATH or
            not hmac.compare_digest(auth, "Bearer " + self.token)):
            self.reply(403, b'{"status":"forbidden"}')
            return
        try:
            n = int(self.headers.get("Content-Length","-1"))
        except ValueError:
            n = -1
        if n < 0 or n > 128:
            self.reply(400, b'{"status":"invalid"}')
            return
        raw = self.rfile.read(n)
        if raw != b'{"action":"wake_voicebridge"}':
            self.reply(400, b'{"status":"invalid"}')
            return
        if not self.gate.acquire():
            self.reply(429, b'{"status":"rate_limited"}')
            return
        # GET only, fixed destination and disallowed redirects, no media or STT.
        req = Request(_TARGET,headers={"Accept":"application/json"},method="GET")
        try:
            with build_opener(NoRedirect()).open(req,timeout=30) as response:
                valid = response.status == 200
                if valid:
                    obj = json.loads(response.read(4097).decode("utf-8"))
                    valid = isinstance(obj,dict) and obj.get("status")=="ok"
            if valid:
                self.reply(200,b'{"status":"woken"}')
            else:
                self.reply(503,b'{"status":"unavailable"}')
        except (HTTPError,URLError,TimeoutError,OSError,ValueError,UnicodeDecodeError):
            self.reply(503,b'{"status":"unavailable"}')

def main():
    token = os.environ.get("KRC_WAKE_RELAY_SERVER_TOKEN","")
    if not 32 <= len(token) <= 256:
        raise SystemExit("missing relay token: refusing to start")
    # No bind address control from env: always loopback only.
    Handler.token = token
    Handler.gate = RateGate()
    server = ThreadingHTTPServer(("127.0.0.1",9012),Handler)
    try: server.serve_forever()
    finally: server.server_close()

if __name__ == "__main__":
    main()
