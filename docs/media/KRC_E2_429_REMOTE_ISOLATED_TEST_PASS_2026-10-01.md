# E2 429 diagnostics — remote isolated test checkpoint

Date: 2026-10-01. Remote machine: `krc-cobalt` via authorized Remote Desktop Commander. Downloaded current `agent/krc-public-media-r3-integration` GitHub branch as tarball to isolated `/tmp/krc_e2_diag_*` folder. No production service, environment, credentials, provider job or database modifications.

Commands executed from extracted repository root:
- `python3 -m unittest discover -s tests -p 'test*http*diagnos*.py' -v` — **6 tests PASS**, exit 0.
- `python3 -m unittest discover -s tests -p 'test_r3c_http_error_integration.py' -v` — **3 tests PASS**, exit 0.

Coverage includes allowlisted 429 RATE_LIMITED metadata and Retry-After, unstructured proxy 429, 503, malformed/oversized bodies, invalid headers/IDs, no secret leakage, and end-to-end MCP error mapping under mocked HTTP. This is NOT an actual deployed VoiceBridge E2E acceptance. No real Instagram start occurred. Existing E2 probe-only and VoiceBridge production remain unchanged. Next: inspect broader test compatibility and deploy only after a separate gate.
