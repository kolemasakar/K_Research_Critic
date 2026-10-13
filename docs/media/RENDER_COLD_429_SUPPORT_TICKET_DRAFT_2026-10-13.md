# DRAFT — Render infrastructure support case — NOT SUBMITTED
Subject: Free-to-Free public HTTPS cold startup returns 429; external GET wakes target — CF-Ray correlation request

Hello Render Support,

We are investigating a reproducible, route-dependent cold-start failure with two Render Free web services in our workspace, both in Frankfurt.

Workspace: tea-d9dsqdjrjlhs73ba1ga0
Source: krc-mcp-auth-sentinel — srv-dale3r942hec73c5t9hg
Destination: voicebridge-krc-media-beta-kolemasakar — srv-da1kic5bedkc73d6fk60
Destination public route: GET /api/v1/health (no auth, health only)
Time zone for events below: UTC, 2026-10-13

After >15 minutes idle, a request from the source service to the destination public *.onrender.com HTTPS endpoint received HTTP 429. The MCP route itself returned HTTP 200, but the embedded upstream read-only operation failed after 22 bounded health attempts. We instrumented safe response headers:
1. Initial upstream failed request: CF-Ray a49ccaf70d1d18cb-FRA; HTTP 429; Server: cloudflare.
2. First readiness health GET: CF-Ray a49ccaf77d4d0d18-FRA; HTTP 429; Server: cloudflare. Source application log timestamp 07:57:19.950466563Z.
3. Source MCP completed HTTP 200 (tool error embedded) at 07:58:04.897761260Z.
The destination application did not log a startup within the failing request window; service_started appeared at 07:58:59.629117948Z, after an independent external health request was initiated from our authorized krc-cobalt machine.

The separate external GET /api/v1/health returned HTTP 200 in 13.352 s (response Server: cloudflare, X-Render-Origin-Server: Render, X-Request-Id: f11bfe03-f9f4-4053-8785-4e929e5bc0b4, CF-Ray: a49ccd386f6befff-FRA). After that, a normal read-only upstream call through the source service succeeded.

Could you please:
- Trace BOTH failing CF-Ray IDs and clarify which layer produced HTTP 429: Cloudflare, Render edge/routing, or the application path?
- Explain whether expected Free instance spin-up through a public *.onrender.com URL differs for a request originating from another Render Free service in the same workspace/region.
- Recommend the supported way to wake the destination on demand from the source, without periodic keepalive or paid compute.
- Confirm whether there is a platform-side issue or abuse/rate limit relevant to the two service IDs, and whether any further request IDs/timestamps are required.

We are NOT asking for application debugging, paid upgrades, higher limits, or bypass of legitimate throttling. No consequential MEDIA processing occurred during this test.

Thank you.
