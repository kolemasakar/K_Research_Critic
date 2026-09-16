# KRC MEDIA Remote MCP Canary

Bounded Remote MCP package used by the repository-accepted `krc_media_capabilities_canary` and the isolated R3-B authentication gate.

## Scope

- exactly one MCP tool;
- deterministic and read-only;
- no VoiceBridge calls;
- no provider work;
- no durable MEDIA jobs;
- no embedded credentials;
- no public KRC mutation.

The service exposes `POST /mcp` and `GET /healthz`. TLS must terminate at the selected remote deployment platform, secure tunnel, or reverse proxy.

## Protocol

The HTTP wrapper supports the modern stateless MCP `2026-07-28` request model, including `server/discover`, protocol/method/name header validation, and request `_meta` version validation. It also keeps bounded `2025-11-25` initialize compatibility for connection fallback testing.

## Authentication modes

`KRC_MCP_AUTH_MODE` is pluggable:

- `none` — bounded evidence-only canary use; never acceptable for future VoiceBridge binding;
- `bearer` — test/support mode using `KRC_MCP_BEARER_TOKEN` from deployment environment state;
- `oauth` — R3-B isolated authenticated mode using authorization-code + PKCE, dynamic client registration, rotating refresh tokens, and protected-resource / authorization-server metadata discovery.

OAuth mode requires:

```text
KRC_MCP_AUTH_MODE=oauth
KRC_MCP_PUBLIC_BASE_URL=https://<isolated-service-host>
KRC_MCP_OWNER_CODE=<owner-provisioned secret in deployment dashboard only>
```

`KRC_MCP_OWNER_CODE` must be created and entered directly by the owner in the deployment platform secret/environment UI. It must never be pasted into chat, committed to Git, included in tool arguments, written to evidence/checkpoints, or emitted to logs/responses. The service fails closed at authorization until this value is configured.

OAuth discovery endpoints:

```text
/.well-known/oauth-protected-resource
/.well-known/oauth-protected-resource/mcp
/.well-known/oauth-authorization-server
/oauth/register
/oauth/authorize
/oauth/token
```

The R3-B OAuth store is intentionally isolated and in-memory. A service restart invalidates issued access/refresh tokens and may require owner reauthorization. Durable identity/session hardening belongs to the later private-operational-hardening phase, not R3-B.

No OAuth credential is the VoiceBridge bearer. The future VoiceBridge credential remains server-side-only and is still forbidden from this isolated auth canary.

If a browser-style `Origin` header is present, it is rejected unless its exact value appears in the comma-separated `KRC_MCP_ALLOWED_ORIGINS` environment variable. Server-to-server requests without `Origin` are accepted.

## R3-B boundary

R3-B may prove authenticated ChatGPT connection and one read-only canary invocation only. It must not expose the 9 MEDIA backend-read tools, the 4 start/execution tools, provider calls, or VoiceBridge credentials.
