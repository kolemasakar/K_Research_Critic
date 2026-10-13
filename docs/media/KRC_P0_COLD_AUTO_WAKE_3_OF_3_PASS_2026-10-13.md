# KRC P0 third cold recovery verification — 2026-10-13

## Final three independent successful cold cycles (after relay token correction)
All times UTC; add +03:00 for Kyiv. Evidence: Render app logs from `srv-dale3r942hec73c5t9hg` (R3C) and `srv-da1kic5bedkc73d6fk60` (VoiceBridge). No MEDIA start operation was made in these checks, only R3C `media_get_capabilities`. No paid fallback was enabled.

| Successful cycle | Initial cold R3C HTTP 429 | VoiceBridge service_started | R3C relay_success | R3C MCP 200 | VoiceBridge stopped |
| --- | --- | --- | --- | --- | --- |
| #1 | 11:49:40 | 11:49:47 | 11:49:53 | 11:49:57 | 12:04:57 |
| #2 | 13:14:14 | 13:14:21 | 13:14:27 | 13:14:31 | 13:29:31 |
| #3 | 13:42:48 | 13:42:58 | 13:43:02 | 13:43:07 | 13:58:07 |

Cycle #3 initial CF-Ray: `a49ec5077d3c1d8a-FRA`.
Earlier cycles #1/#2 CF-Ray: `a49e1f4e4f67dbfa-FRA`, `a49e9b30c8745d3d-FRA`.

## Findings
- **Cold auto-wake acceptance criterion 3/3 PASS** within the tested Render Free configuration after owner corrected one missing character in R3C `KRC_WAKE_RELAY_TOKEN`.
- Initial two failed attempts before correction were traced to relay rejection. They were not counted as successful cycles.
- Render R3C recorded `relay_success` and VoiceBridge independently recorded `service_started`, followed by MCP HTTP 200 in each of the three accepted cycles.
- VoiceBridge stopped about 15 minutes after each success; the relay did not require a standing keepalive for these tests.
- Request ID of cycle #2: `b9bc4ea0-faaf-490f-8070-114e67575ca9`. The automation ran cycle #3; the request ID was not extracted.
- These tests demonstrate read-only recovery, not paid-provider billing, the completion of media jobs, or full MEDIA release readiness.

## Outstanding evidence / constraints
- Direct krc-cobalt relay journal access timed out during the parallel audits; endpoint-server-side success logs for all three cycles have not been independently read in this report. R3C's `relay_success` plus VoiceBridge start is strong independent service evidence.
- Root emitter of edge-labeled 429 has not been established by Render human support. `upstream_server=cloudflare` is an observed header, not attribution.
- Further P1 Instagram/Facebook 480–720s, Telegram live safety release, Postgres durability after restart and clean reproducible cross-repo tests remain OPEN.
- Do not mark the overall R4 Plugin / MEDIA acceptance COMPLETE solely from this P0 success.
- Preserve FREE_ONLY, no automatic paid fallback, single-read-only-wake on eligible 429, fail-closed behavior and no permanent keepalive.

Verdict: **P0 COLD AUTOMATIC RECOVERY 3/3 PASS; overall KRC MEDIA final acceptance OPEN.**
