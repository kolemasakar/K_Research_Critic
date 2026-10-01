# VoiceBridge peer diagnostics: integration design and security gate

Date: 2026-10-01. Status: **DESIGN ONLY / NO PRODUCTION INTEGRATION**.

## Baseline, source evidence

VoiceBridge deployed source commit `d3873bf13e60c4932ab08cae449c924051be4a37`:
- `src/cloud/src/server.ts` creates `RequestContext` and parses the path; OPTIONS and GET `/api/v1/health` return before the limiter. `clientKey(request)` is exactly `request.socket.remoteAddress || "unknown"`. `rateLimiter.allow(clientKey(request))` precedes `authenticate(...)`; rejection yields 429 `RATE_LIMITED` and `retry-after:60`.
- `src/cloud/src/rate_limit.ts` maintains a **per-process** in-memory fixed 60-second counter by the provided key. It is not a distributed/global limiter.
- `src/cloud/src/config.ts` uses `min(configured RATE_LIMIT_REQUESTS_PER_MINUTE, 60)` in public mode. Owner-provided Render screenshot shows the configured value 60; effective configured public-mode value is therefore 60/minute, subject to screenshot representing active runtime.
- Render request logs were not available for the inspected time window; observed 429 cause and actual TCP peer IP remain unknown.

## Prototype boundary

Research-only Python module `plugins/krc_migration_candidate/mcp_canary/proxy_peer_diagnostics.py` computes a truncated 96-bit HMAC-SHA256 tag from normalized socket peer using a caller-supplied >=32-byte key, and reports only **untrusted header shape** (absent/empty/single/multiple/oversize). It is not imported by production VoiceBridge, which is TypeScript. No implicit deployment or claim of TypeScript equivalence.

## Proposed TypeScript implementation (separate VoiceBridge research branch, not yet applied)

1. Implement a pure `peer_observation.ts` with IPv4/IPv6 normalization, an ephemeral 256-bit cryptographically random key generated at process start, `HMAC-SHA256` over normalized socket peer and a fixed purpose/version domain separator, truncate to 96 bits, and return only `peer_tag` plus untrusted header-presence/shape category. Avoid printing raw peer IP, forwarded value or HMAC key.
2. Integrate at a **single read-only observation point immediately before** `rateLimiter.allow`, behind a default-OFF flag; do not alter `clientKey`, authentication, response status, Retry-After, request order, or health/OPTIONS bypass.
3. Prefer **aggregate counts only** in a short bounded in-memory window: counts of allowed vs rejected by ephemeral tag and untrusted header-shape class. Expose no public endpoint; if logs are needed, emit only thresholded aggregate summaries with an approved finite retention period. Never log raw IP, raw headers, authorization tokens, secret key or unbounded request IDs.
4. Keep the feature OFF in production until owner approval and a documented threat/privacy review. If the observation key rotates on restart, tags must not be compared across restarts; an instance-specific key also prevents naive cross-instance comparisons.
5. Do **not** trust `X-Forwarded-For` or `Forwarded` as a client identity. Any future proxy-aware limiter needs verified Render trust-boundary behavior and spoof-resistance tests. Do not remove the pre-auth IP abuse guard to create an authenticated-principal limiter.

## Test plan (must pass before deployment consideration)

- Pure unit tests: same peer/same key, different peer, key rotation, IPv4/IPv6 canonicalization, malformed/unknown peer, no key/header/IP in outputs or exceptions, long/hostile header classification, 96-bit output format.
- Server integration tests with feature OFF vs ON: identical allow/deny decisions at limit 60, exact `Retry-After`, health/OPTIONS bypass, pre-auth behavior, no change to MEDIA execution or provider calls.
- Privacy/security tests: forged `X-Forwarded-For` must not change the limiter key; no raw header/IP/key in logs or error responses; bounded memory and finite retention; multi-instance behavior explicitly documented.
- Run VoiceBridge's full existing test suite on a non-production checkout with the same supported Node/TypeScript toolchain. Do not substitute the KRC Python test count for this gate.
- Deployment, if later approved, should be separately staged and reverted on any auth, availability, privacy or limiter regression.

## Open questions and decisions

- **Actual shared proxy IP**: not demonstrated. The design must gather only minimum necessary evidence, not assume the hypothesis.
- **Effective active environment**: owner screenshot says 60, but live instance peer observation remains absent.
- **Security tradeoff**: even truncated HMAC tags are linkable within the observation window; key custody, short retention and minimum access are mandatory. Header shape may still reveal traffic patterns.
- **Current owner authorization**: research/design and isolated tests only. No production VoiceBridge changes, no E2 mode change, no additional MEDIA jobs, no credential rotation, no paid fallback.

Next gate: obtain permitted isolated TypeScript prototype and regression results, then seek separate owner approval for any live instrumentation.
