"""Cross-repository integration over verified local TLS, never external providers.

Opt in with KRC_TEST_VOICEBRIDGE_ROOT pointing to a compiled VoiceBridge
src/cloud checkout; ordinary KRC tests do not require a second repository.
"""
from __future__ import annotations
import http.client
import json
import os
from pathlib import Path
import select
import ssl
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
import urllib.request
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plugins.krc_migration_candidate.mcp_canary.r3c import (
    VoiceBridgeBinding, call_voicebridge, dispatch_r3c,
)
from plugins.krc_migration_candidate.mcp_canary.r3e1 import dispatch_r3e1
from plugins.krc_migration_candidate.mcp_canary.r3e2 import dispatch_r3e2
from plugins.krc_migration_candidate.mcp_canary.r3e3 import dispatch_r3e3
from plugins.krc_migration_candidate.mcp_canary.r3e4 import dispatch_r3e4

URLS = {
    "youtube": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    "instagram": "https://www.instagram.com/reel/DF1CIrPSVmf/",
    "facebook": "https://www.facebook.com/reel/636216875539019/",
    "telegram": "https://t.me/techcrimes/12101",
}
DISPATCH = {
    "youtube": dispatch_r3e1, "instagram": dispatch_r3e2,
    "facebook": dispatch_r3e3, "telegram": dispatch_r3e4,
}
CONSENT = {"provider": "google_gemini", "tier": "free", "data_use_acknowledged": True}

class LocalStack:
    def __init__(self, node, proxy, initial):
        self.node = node
        self.proxy = proxy
        self.node_url = initial["url"]
        self.tokens = initial["tokens"]
        self.url = "https://localhost:" + str(proxy.server_port)
        self.transport_requests = 0

    def binding(self, platform="read"):
        return VoiceBridgeBinding(self.url, self.tokens[platform], timeout_seconds=5)

    def command(self, command):
        self.node.stdin.write(command + "\n")
        self.node.stdin.flush()
        return read_json(self.node)

    def call(self, platform, name, arguments=None):
        fn = dispatch_r3c if platform == "read" else DISPATCH[platform]
        response = fn({
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        }, self.binding(platform))
        assert response is not None
        assert "error" not in response, response
        return response["result"]

    def data(self, platform, name, arguments=None):
        result = self.call(platform, name, arguments)
        assert result["isError"] is False, result
        return result["structuredContent"]

def read_json(node):
    readable, _, _ = select.select([node.stdout], [], [], 10)
    assert readable, "Local VoiceBridge fixture timed out"
    line = node.stdout.readline()
    assert line, "Local VoiceBridge fixture exited unexpectedly"
    return json.loads(line)

@pytest.fixture
def stack(tmp_path, monkeypatch):
    vb_root = os.getenv("KRC_TEST_VOICEBRIDGE_ROOT")
    if not vb_root:
        pytest.skip("Opt-in cross-repository VoiceBridge integration")
    assert (Path(vb_root) / "dist/src/managed_server.js").is_file(), "Build VoiceBridge first"
    cert, key = tmp_path / "local.pem", tmp_path / "local.key"
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
        "-subj", "/CN=localhost", "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
        "-keyout", str(key), "-out", str(cert),
    ], check=True, capture_output=True)
    monkeypatch.setenv("SSL_CERT_FILE", str(cert))
    monkeypatch.setattr(urllib.request, "_opener", None)
    environment = dict(os.environ)
    environment.pop("KRC_MEDIA_DATABASE_URL", None)
    environment["KRC_TEST_VOICEBRIDGE_ROOT"] = vb_root
    node = subprocess.Popen(
        ["node", str(ROOT / "tests/fixtures/voicebridge_all_routes.mjs")],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=environment,
    )
    try:
        initial = read_json(node)
        holder = {}
        class Proxy(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass
            def forward(self):
                current = holder["stack"]
                target = urlsplit(current.node_url)
                connection = http.client.HTTPConnection(target.hostname, target.port, timeout=5)
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                    body = self.rfile.read(size) if size else None
                    headers = {k: v for k, v in self.headers.items()
                               if k.lower() not in {"host", "connection"}}
                    headers["Connection"] = "close"
                    connection.request(self.command, self.path, body, headers)
                    response = connection.getresponse()
                    raw = response.read()
                    current.transport_requests += 1
                    self.send_response(response.status)
                    for name, value in response.getheaders():
                        if name.lower() not in {"connection", "transfer-encoding", "content-length"}:
                            self.send_header(name, value)
                    self.send_header("Content-Length", str(len(raw)))
                    self.end_headers()
                    self.wfile.write(raw)
                finally:
                    connection.close()
            do_GET = forward
            do_POST = forward
            do_OPTIONS = forward
        proxy = ThreadingHTTPServer(("127.0.0.1", 0), Proxy)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        proxy.socket = context.wrap_socket(proxy.socket, server_side=True)
        local = LocalStack(node, proxy, initial)
        holder["stack"] = local
        thread = threading.Thread(target=proxy.serve_forever, daemon=True)
        thread.start()
        try:
            yield local
        finally:
            proxy.shutdown()
            proxy.server_close()
            thread.join(timeout=5)
    finally:
        if node.poll() is None:
            node.stdin.write("stop\n")
            node.stdin.flush()
            try:
                node.wait(timeout=5)
            except subprocess.TimeoutExpired:
                node.kill()
                node.wait(timeout=5)
        for stream in (node.stdin, node.stdout, node.stderr):
            if stream:
                stream.close()

def start_arguments(platform):
    args = {"url": URLS[platform], "language_hint": "auto"}
    if platform == "youtube":
        args["gemini_free_consent"] = CONSENT
    return args

def counts_for(platform):
    if platform == "youtube":
        return {"youtube": 1}
    return {platform + "Retrieval": 1, platform + "Stt": 1}

@pytest.mark.parametrize("platform", list(URLS))
def test_all_routes_real_https_start_status_complete_pagination_and_reuse(stack, platform):
    capability = stack.data("read", "media_get_capabilities")
    assert capability["platforms"] == ["youtube", "instagram", "facebook", "telegram"]
    assert capability["automatic_paid_fallback"] is False
    assert capability["durable_store"] == "memory"  # Explicit fixture limitation.
    assert not any(stack.command("counts")["counts"].values())

    if platform in {"youtube", "instagram"}:
        preflight = stack.data("read", "media_" + platform + "_preflight", {"url": URLS[platform]})
        assert preflight["can_continue"] is True
        assert not any(stack.command("counts")["counts"].values())

    started = stack.data(platform, "media_" + platform + "_start", start_arguments(platform))
    assert started["status"] == "COMPLETED"
    assert started["credits_charged"] == 0
    assert started["segment_count"] == 3
    job = started["job_id"]
    status_tool = "media_youtube_status" if platform == "youtube" else "media_non_youtube_status"
    segment_tool = "media_youtube_segments" if platform == "youtube" else "media_non_youtube_segments"
    status = stack.data("read", status_tool, {"job_id": job})
    assert status["job_id"] == job
    assert status["status"] == "COMPLETED"

    segments, cursor, seen = [], 0, set()
    while True:
        assert cursor not in seen
        seen.add(cursor)
        page = stack.data("read", segment_tool, {"job_id": job, "cursor": cursor, "limit": 1})
        assert page["job_id"] == job
        assert page["cursor"] == cursor
        segments.extend(page["segments"])
        if page["next_cursor"] is None:
            break
        assert page["next_cursor"] > cursor
        cursor = page["next_cursor"]
    assert [s["index"] for s in segments] == [0, 1, 2]
    transcript = "\n".join(s["text"] for s in segments)
    assert len(transcript.encode("utf-16-le")) // 2 == status["transcript_characters"]

    if platform in {"youtube", "instagram"}:
        looked_up = stack.data("read", "media_" + platform + "_lookup", {"url": URLS[platform]})
        assert looked_up["job_id"] == job
    before = stack.command("counts")["counts"]
    for name, value in before.items():
        assert value == counts_for(platform).get(name, 0)
    repeated = stack.data(platform, "media_" + platform + "_start", start_arguments(platform))
    assert repeated["job_id"] == job
    assert repeated["reused"] is True
    assert stack.command("counts")["counts"] == before
    assert stack.transport_requests >= 7

    # Recreate the HTTP wrapper against the SAME fixture engine/store objects.
    # This proves routing/read continuity, not PostgreSQL/process durability.
    restarted = stack.command("restart")
    stack.node_url = restarted["url"]
    assert stack.data("read", status_tool, {"job_id": job})["job_id"] == job
    assert stack.command("counts")["counts"] == before


@pytest.mark.parametrize("platform", ["instagram", "facebook", "telegram"])
def test_cross_platform_execution_and_read_scopes_fail_closed(stack, platform):
    response = DISPATCH[platform]({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": "media_youtube_start", "arguments": start_arguments("youtube")},
    }, stack.binding(platform))
    assert response["error"]["code"] == -32602
    assert stack.transport_requests == 0
    from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeError
    with pytest.raises(VoiceBridgeError) as error:
        call_voicebridge(stack.binding(platform), "GET",
                         "/api/v1/media/youtube-gemini/transcriptions/KRCM_other", None, {})
    assert error.value.http_status in {401, 403}
    assert not any(stack.command("counts")["counts"].values())

def test_real_media_read_routes_do_not_consume_legacy_socket_limiter(stack):
    for _ in range(65):
        assert stack.data("read", "media_get_capabilities")["configured"] is True
    assert not any(stack.command("counts")["counts"].values())

def test_all_dispatchers_preserve_real_429_metadata_without_replaying_provider_work(stack, monkeypatch):
    from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeError
    for _ in range(60):
        with pytest.raises(VoiceBridgeError) as error:
            call_voicebridge(stack.binding(), "GET", "/fixture-legacy-unknown", None, {})
        assert error.value.http_status == 401

    def saturated(binding, _method, _path, _payload, _query):
        return call_voicebridge(binding, "GET", "/fixture-legacy-unknown", None, {})

    for platform, dispatch in [("read", dispatch_r3c), *DISPATCH.items()]:
        name = "media_get_capabilities" if platform == "read" else "media_" + platform + "_start"
        args = {} if platform == "read" else start_arguments(platform)
        message = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": name, "arguments": args}}
        if platform == "youtube":
            monkeypatch.setattr(
                "plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge", saturated)
            response = dispatch(message, stack.binding(platform))
        else:
            response = dispatch(message, stack.binding(platform), backend_call=saturated)
        detail = response["result"]["structuredContent"]["error"]
        assert detail["http_status"] == 429
        assert detail["retryable"] is True
        assert detail["retry_after_seconds"] == 60
        assert detail["upstream_code"] == "RATE_LIMITED"
        assert detail["request_id"]
        assert detail["correlation_id"]
        serialized = json.dumps(detail)
        assert all(token not in serialized for token in stack.tokens.values())
    assert not any(stack.command("counts")["counts"].values())
