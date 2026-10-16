# Instagram stage diagnostics — 2026-10-16

## Scope
Owner selected mobile/embed/GraphQL diagnostic. No managed MEDIA start, STT, paid service, Docker mutation, credential/cookie read or privilege expansion. Public source Dcea3BiPTBm. Authorized krc-cobalt identity krcops.

## Initial direct anonymous shape checks
Python urllib with generic User-Agent: oEmbed HTTP 401; embed HTTP 200 (419638 bytes), no legacy initializer pattern or video_url; web HTTP 200 (417843 bytes), no video_url. These are shape checks, not a reproduction of configured container cookie/proxy context.

## Exact installed-source isolated reproduction
Cobalt upstream commit a636575b09de1fc55d9b8cd98cac88f5f2f16b42 (11.7.1). Actual Instagram module evaluated in isolation with mocked dependencies and no network.
1. Missing embed initializer throws inside requestHTML. The encompassing getPost catch suppresses subsequent GraphQL fallback. Reproduced fetch.empty without calling a GraphQL fixture that would succeed.
2. Empty parsed context object passes hasData because undefined !== null. GraphQL fallback is skipped and extraction returns empty. Reproduced independently.

Local candidate patch checks actual media-bearing fields and catches failures per extraction attempt. Both scenarios reach successful fixture GraphQL retrieval after patch. Baseline and patched assertions PASS; syntax check PASS. No global provider regression or production compatibility acceptance claimed.

## Live anonymous candidate-stage diagnostic
Candidate exact module ran in memory on krc-cobalt, not installed in container. Cookie/token providers stubbed absent, generic User-Agent, no container dispatcher/proxy settings. Bounded at 12 requests/15s per request; actual six requests:
- oembed 401
- embed 200
- web 200
- graphql 401; parsed data absent, video absent
- web 200
- error_context 200
Terminal fetch.empty, no media URL. Only static stage/status/boolean metadata emitted. Raw responses and tokens not persisted.

## Interpretation
Two fallback defects are proven in installed source. The candidate fixes those defects in isolation but does not restore anonymous retrieval from this host: GraphQL and oEmbed return HTTP 401. HTTP 401 does NOT alone prove an IP block, login requirement, cookie expiration, source deletion or the exact failure path of the configured live container. Production cookies/proxy configuration remain uninspected due existing access boundaries.

## Artifacts and next gate
- docs/media/diagnostics/instagram_fallback_2026-10-16.patch
- docs/media/diagnostics/instagram_fallback_2026-10-16.mjs (argument: exact module path; add --patched for candidate)

Production Cobalt was not modified. Next needs narrow sanitized operator diagnostics of the configured container's actual stage status and credential/cookie presence booleans, without exporting values; then assess a supported Instagram authentication setup or upstream retrieval repair. Do not blindly rotate keys, inject cookies, change IP/identity or repeat MEDIA starts. VoiceBridge remains 65737cfb LIVE. FREE_ONLY; R4 PRIVATE PARTIAL/public HOLD; Telegram LIVE BLOCKED.
