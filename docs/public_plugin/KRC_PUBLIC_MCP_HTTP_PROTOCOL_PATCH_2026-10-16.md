# KRC Public MCP HTTP protocol patch — 2026-10-16

Status: LOCAL TEST CANDIDATE / RELEASE HOLD.

## Work completed
- Verified original HTTP candidate baseline: 25/25 tests PASS on local isolated Python.
- Reviewed official MCP Streamable HTTP transport 2025-03-26 and current draft evolution.
- Added Accept header check requiring both `application/json` and `text/event-stream` for JSON-RPC POST requests.
- Added rejection of non-notification requests without a JSON-RPC id.
- Added two corresponding HTTP integration tests.
- **27/27 offline unit/integration tests PASS**, with ResourceWarnings suppressed for reporting; SQLite connection ResourceWarning still requires fix.

Local revised code artifact: `KRC_PUBLIC_MCP_HTTP_PATCH_V4_2026-10-16.zip` (conversation attachment). **Code in this ZIP is not yet committed to GitHub.**

## Release gates
- No full MCP SDK/ChatGPT end-to-end validation, including newer protocol version interoperability.
- Guest credentials are opaque bearer capabilities; no separate user login, but security review outstanding.
- No OCI isolated staging or OCI load measurements yet.
- No public HTTPS host, Caddy changes, or production rollout.
- Retention 10 h and 10% disk admission tests remain local.

Risk: Do not expose internet-facing prototype without reviewing per-job token lifecycle, resource exhaustion, and concurrency.
