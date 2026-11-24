#!/usr/bin/env python3
"""Stage131 PUBLIC DOI read-only loopback staging and rollback rehearsal.

MANUAL USE ONLY, never from installed KRC/Sentinel services or CI by default.

Usage (on an authorized isolated KRC staging VM only):
  PYTHONDONTWRITEBYTECODE=1 python -B tools/stage131_public_doi_staging_rehearsal.py \
      --baseline /vm/baseline/src --candidate /vm/candidate/src \
      --baseline-sha <verified baseline git SHA> --candidate-sha <verified candidate git SHA>

The caller explicitly provides two approved local VM source snapshots.
This tool does not access user-owned local computer disks, modify installed
services, create consent/authorization, or enable signed bibliography.audit.
It runs three short-lived HTTP servers on the same ephemeral 127.0.0.1 port
and verifies release/rollback behavior. One candidate DOI lookup may send
bounded FREE_ONLY Crossref and Europe PMC HTTPS metadata requests.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DOI = "10.1016/j.proeng.2013.03.022"
SERVER_CODE = r'''
import json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from krc_research.stage131_bibliography_adapter import lookup_doi_metadata

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def reply(self, status, body):
        data = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self.reply(405, {"error": "READ_ONLY"})

    def do_GET(self):
        if len(self.path) > 400:
            self.reply(414, {"error": "LONG_QUERY"})
            return
        path = urlsplit(self.path)
        if path.path == "/health" and not path.query:
            self.reply(200, {
                "status": "up",
                "source_pin": os.environ["STAGING_SOURCE_PIN"],
                "bound": "127.0.0.1",
            })
            return
        if path.path != "/v1/public/doi":
            self.reply(404, {"error": "NOT_FOUND"})
            return
        values = parse_qs(path.query, keep_blank_values=True)
        if set(values) != {"doi"} or len(values["doi"]) != 1:
            self.reply(400, {"error": "INVALID_REQUEST"})
            return
        try:
            result = lookup_doi_metadata(values["doi"][0], timeout_seconds=6)
        except ValueError:
            self.reply(400, {"error": "INVALID_DOI"})
            return
        self.reply(200, result)

server = ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), Handler)
assert server.server_address[0] == "127.0.0.1"
server.serve_forever(poll_interval=0.1)
'''


def source_sha(source: Path) -> str:
    process = subprocess.run(
        ["git", "-C", str(source.parent), "rev-parse", "HEAD"],
        text=True, capture_output=True, check=True, timeout=8,
    )
    return process.stdout.strip()


def fetch(base_url: str, path: str, method: str = "GET", timeout: float = 22):
    request = urllib.request.Request(base_url + path, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read(8192))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read(8192))


def is_port_free(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def phase(label: str, source: Path, source_pin: str, port: int, expected: str, *, hardened: bool):
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(source),
        STAGING_SOURCE_PIN=source_pin,
        PYTHONNOUSERSITE="1",
        PYTHONDONTWRITEBYTECODE="1",
        no_proxy="127.0.0.1,localhost",
    )
    # Each stage has a separate process and an isolated import path.
    process = subprocess.Popen(
        [sys.executable, "-B", "-c", SERVER_CODE, str(port)],
        env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE, text=True,
    )
    base_url = "http://127.0.0.1:" + str(port)
    try:
        for _ in range(50):
            if process.poll() is not None:
                raise AssertionError(label + ": server exit " + process.stderr.read()[:500])
            try:
                status, health = fetch(base_url, "/health", timeout=0.8)
                if status == 200:
                    break
            except (TimeoutError, OSError):
                time.sleep(0.12)
        else:
            raise AssertionError(label + ": health timeout")

        assert health["source_pin"] == source_pin
        assert health["bound"] == "127.0.0.1"
        assert fetch(base_url, "/private")[0] == 404
        assert fetch(base_url, "/v1/public/doi?doi=invalid")[0] == 400
        assert fetch(base_url, "/v1/public/doi?doi=10.1000%2Ftest", method="POST")[0] == 405

        invalid_status, _ = fetch(base_url, "/v1/public/doi?doi=10.1000%2Fbad%00control")
        # Baseline is deliberately less strict, and must be documented as such.
        assert invalid_status == (400 if hardened else 200), (label, invalid_status)

        encoded = urllib.parse.quote(DOI, safe="")
        status, result = fetch(base_url, "/v1/public/doi?doi=" + encoded)
        assert status == 200 and result["status"] == expected, (label, status, result)
        assert result.get("full_text_verified", False) is False
        assert result.get("experimental_independence_verified", False) is False
        if hardened:
            assert result["sources"]["crossref"]["status"] == "METADATA_ONLY"
            assert result["sources"]["europe_pmc"]["status"] == "NOT_FOUND"

        print(
            label + "_LOOPBACK_HTTP_PASS",
            "status=" + result["status"],
            "invalid_doi_http=" + str(invalid_status),
            "source=" + source_pin,
            flush=True,
        )
    finally:
        process.terminate()
        try:
            process.wait(timeout=4)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        for _ in range(20):
            if is_port_free(port):
                break
            time.sleep(0.1)
        assert is_port_free(port), label + "_LISTENER_LEAK"
        print(label + "_STOPPED_AND_PORT_FREE_PASS", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--baseline-sha", required=True)
    parser.add_argument("--candidate-sha", required=True)
    args = parser.parse_args()

    for root, pin in ((args.baseline, args.baseline_sha), (args.candidate, args.candidate_sha)):
        if not root.is_dir() or not (root / "krc_research/stage131_bibliography_adapter.py").is_file():
            parser.error("Existing isolated src/ tree required, no owner-computer disk fallback")
        if source_sha(root) != pin:
            parser.error("Expected Git commit does not match the pinned source")

    with socket.socket() as socket_probe:
        socket_probe.bind(("127.0.0.1", 0))
        port = socket_probe.getsockname()[1]
    try:
        phase("BASELINE", args.baseline, args.baseline_sha, port, "PROVIDER_DISABLED", hardened=False)
        phase("PR37_STAGING", args.candidate, args.candidate_sha, port,
              "COVERAGE_GAP_METADATA_ONLY", hardened=True)
        phase("ROLLBACK_BASELINE", args.baseline, args.baseline_sha, port,
              "PROVIDER_DISABLED", hardened=False)
        print("REAL_LOOPBACK_PROCESS_STAGING_AND_ROLLBACK_3_OF_3_PASS", flush=True)
        print("INSTALLED_KRC_UNCHANGED_STAGING_ONLY", flush=True)
    finally:
        assert is_port_free(port), "UNEXPECTED_LISTENER_ON_EXIT"


if __name__ == "__main__":
    main()
