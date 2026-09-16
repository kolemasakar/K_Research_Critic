# KRC MEDIA Remote MCP Canary

Bounded deployment package for the repository-accepted `krc_media_capabilities_canary`.

## Scope

- exactly one MCP tool;
- deterministic and read-only;
- no VoiceBridge calls;
- no provider work;
- no durable MEDIA jobs;
- no embedded credentials;
- no public KRC mutation.

The service exposes `POST /mcp` and `GET /healthz`. TLS is expected to terminate at the selected remote deployment platform, secure tunnel, or reverse proxy. No deployment target is selected by this package.

## Protocol

The HTTP wrapper supports the modern stateless MCP `2026-07-28` request model, including `server/discover`, protocol/method/name header validation, and request `_meta` version validation. It also keeps bounded `2025-11-25` initialize compatibility for connection fallback testing.

## Authentication boundary

`KRC_MCP_AUTH_MODE` is intentionally pluggable:

- `none` — suitable only for an isolated/bounded canary connection test or a trusted authenticated outer tunnel/proxy;
- `bearer` — requires `KRC_MCP_BEARER_TOKEN` from deployment environment state.

No token value belongs in the repository. The future production VoiceBridge bearer is unrelated to this canary edge and remains forbidden here.

If a browser-style `Origin` header is present, it is rejected unless its exact value appears in the comma-separated `KRC_MCP_ALLOWED_ORIGINS` environment variable. Server-to-server requests without `Origin` are accepted.

## Local smoke command

Build from repository root using this Dockerfile, then run the resulting image locally. The package itself does not create an external endpoint and does not authorize deployment.
