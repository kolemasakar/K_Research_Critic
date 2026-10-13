# KRC / VoiceBridge P0 — FREE_ONLY On-Demand Cold Recovery Design
Status: DESIGN / NOT DEPLOYED. Date 2026-10-13.
Owner goal: eliminate the MANUAL wakeup dependency without continuous keepalive and without paid services or duplicate provider jobs.

## Facts vs inferences
- Actual 2026-10-13 cold R3C->VoiceBridge failed HTTP 429 (22 health attempts), even though MCP OAuth and MCP transport worked.
- R3C error yielded server=cloudflare, cf-ray=a49ccaf70d1d18cb-FRA; first R3C health request at 07:57:19.950466563Z yielded cf-ray=a49ccaf77d4d0d18-FRA. No VoiceBridge application start until 07:58:59.629117948Z.
- A separate GET from owner-controlled krc-cobalt returned 200 and caused/was closely followed by warmup (13.352 sec). Subsequent capabilities succeeded.
- This supports route-dependent cold startup failure, but NOT proof that Cloudflare originated the 429 or that any arbitrary external relay will always work.
- Render docs: Free web services spin down after 15 minutes, approximately 1-minute startup; Free web services MAY SEND but CANNOT RECEIVE private network traffic. Therefore direct internal R3C->VoiceBridge is not supported at Free compute.
Sources: https://render.com/docs/free ; https://render.com/docs/private-network .

## Candidate approaches
A) Same Render public HTTPS, retries + longer wait: NO as principal solution. Existing 22 health attempts still failed; additional retries may amplify edge restrictions. Do not circumvent Retry-After or real rate limits.
B) Render private network: NOT APPLICABLE to Free receiving service.
C) Always-on keepalive: REJECTED by owner goal and free operating constraints.
D) Unauthenticated public self-invocation endpoint: REJECTED as SSRF/abuse risk.
E) BOUNDED ON-DEMAND EXTERNAL WAKE via secured owner-controlled independent egress: preferred **candidate**, subject to reachability/security/cost verification and cold trials. Existing krc-cobalt public service should not be assumed accessible or suitable until verified. Could instead use another *verified free* egress with outbound HTTPS. No continuous timers.
F) Migrate VoiceBridge runtime to free always-on host (e.g., owner existing Oracle Free capacity) with health+TLS: contingency only, separate capacity/security review; do not assume free allocation or migrate sensitive credentials prematurely.

## Proposed recoverer state machine (feature flag OFF by default)
- No changes to E1-E4 tool interfaces. Initiated by R3C inside current wait-for-readiness on **one** cold upstream failure if non-application proxy attribution is supported.
- First perform existing direct bounded GET to /api/v1/health (never POST processing). Classify reply using allowlisted HTTP code, application error code, Retry-After, content type, upstream_server/CF-Ray. If explicit legitimate 429 quota/admission or Retry-After -> fail closed; no relay or retry-bypass.
- If proxy-like 429, readiness still false, and feature flag + pinned relay endpoint enabled, send **one authenticated request to relay**. Relay must be owner-controlled, access-controlled, outbound URL fixed to VoiceBridge's exact public HTTPS /api/v1/health; no user-supplied URL, no redirects, no browser remote execution. Relay does not accept job IDs, transcripts, media URLs, arbitrary commands, provider tokens, or workload. Use limited short-lived authentication (rotatable), no secrets in logs/URL. Restrict method and response size. Resist SSRF/replay/abuse and apply rate limiter (e.g., one outstanding wake per target; bounded attempts).
- Wait a controlled startup budget (Render documents around a minute; choose 90 s initially by acceptance test, not unbounded). During wait only read-only GET to direct target, honoring explicit Retry-After; if ready, proceed to original GET or **at most one provider POST** after existing consequential-action confirmation. Do not replay POST after a lost response; use existing lookup-only mechanism.
- If relay unavailable, 429 persists, or timeout: return sanitized `voicebridge_not_ready` with stage, wake_attempted, relay_result enum, readiness attempts and CF-Ray (bounded). No paid fallback.
- Fail-safe: default flag OFF, relay timeout; no keepalive; never initiate proactively without a user request; no wake in bulk jobs; no blanket 429 bypass. Operator can revert flag without redeploy.

## Security and live acceptance gates before any deployment
1. Owner-controlled external relay HTTPS URL reachable independently of Render-to-Render Cloudflare path, authenticated from Render R3C; no free tier credits/charges or data leak. Explicitly verify from cold R3C environment.
2. Unit tests: first warm direct request -> no relay; legit 429 with Retry-After -> no relay; proxied 429 -> exactly one relay; relay failure -> fail-closed; cold eventual-ready -> original READ succeeds; POST start exactly once; uncertain POST response -> scoped lookup only; token never leaked in logs; malicious response/redirect/URLs rejected.
3. End-to-end controlled cold test after >15min idle (no artificial keepalive); capture CF-Ray, R3C and VoiceBridge app start. Run at least 3 cold cycles separated by true idle; all recover automatically without manual operator GET; log startup latency and FREE_ONLY.
4. Inspect outbound usage against quotas; stop if any paid usage. Production deploy only after unit, integration, user approval of relay exposure, and security gate.
5. Maintain provenance of any Render infrastructure ticket and their origin analysis. Distinguish inference from provider confirmation.

## Current disposition
Do not deploy an unimplemented/unverified relay or claim P0 fixed. No new Render resources or external service have been created. Ticket document prepared separately; sending requires authenticated Render Dashboard action (connector currently does not offer ticket creation).
