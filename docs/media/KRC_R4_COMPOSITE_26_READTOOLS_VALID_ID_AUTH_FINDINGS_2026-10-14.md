# KRC R4 Private composite 26-read-tools audit — interpretation and validated status probes
Date 2026-10-14. User supplied the actual report of a new chat using private composite R4 0.1.1. All 26 available read tools were attempted, no start tools executed. The report should be preserved as historical observed evidence, not retroactively rewritten into blanket PASS.

## User-reported composite audit
Summary by surface:
- R3C: PASS 3, PARTIAL 6, FAIL 0
- E1: PASS 2, PARTIAL 5, FAIL 2 (Instagram preflight/lookup => HTTP 401)
- E2: PASS 1, PARTIAL 3, FAIL 0
- E3: PASS 0, PARTIAL 2, FAIL 0
- E4: PASS 0, PARTIAL 2, FAIL 0
The synthetic UUID and plain 32-hex job IDs produced JSON-RPC -32602 Invalid params for status/segments, no request ID. Lookup of an absent/expired job returned HTTP 404. These do not demonstrate successful actual stored-job reads nor a broken read API.

## Source-code contract confirmation
On KRC integration branch, `plugins/krc_migration_candidate/mcp_canary/r3c.py` explicitly uses `_JOB_ID_RE = re.compile(r"^KRCM_[A-Za-z0-9-]+$")`. The status/segments schema requires the KRCM_ prefix and segment args must have integer cursor >=0 and integer limit 1..50. This explains rejection of the two invalid test-ID formats without backend traffic.
`plugins/krc_migration_candidate/mcp_canary/r3e1.py` deliberately advertises R3C's nine read tools and one YouTube execution tool; only *other execution starts* are explicitly disabled. Thus an HTTP 401 on **read-only Instagram preflight/lookup via E1** is NOT directly justified by the visible Python wrapper's explicit disabled-start table; backend scope/auth must be audited.

## Fresh valid-format nonexistent job checks
A syntactically valid but deliberately nonexistent `KRCM_00000000-0000-4000-8000-000000000000` was used. NO provider work. Each call passed tool schema and reached a VoiceBridge HTTP response, not -32602:
- R3C YouTube status: HTTP 404, request `bfdb314c-246f-48b1-b2cc-0d998e806a23`, origin confirmed.
- R3C non-YouTube status: HTTP 404, request `87bd6255-ef8e-4ceb-9292-d59389a264c9`, origin confirmed.
- E1 YouTube status: HTTP 404, request `c686989c-abbd-4a98-b879-80a9cdac2f63`.
- E2 non-YouTube status: **HTTP 401**, request `f50fdf07-53f2-4cdd-9dd4-e0edcac47649`. This needs investigation; a valid-format *nonexistent* job may have a scoped authorization response, but do not assume without code evidence.
- E3 non-YouTube status: HTTP 404, request `684c37f5-38c1-47db-bb0f-8b22dccb0f9f`.
- E4 non-YouTube status: HTTP 404, request `78ba67c6-1a10-43a5-a4bb-358c6ae7e323`.
Backend 404 on an *invented but schema-valid* ID is a safe test of argument validation and reachability, not a successful retrieved-job read.

## Verdict / acceptance
- New composite private R4 chat launched all 26 read tools, proving surface enumeration and callable access in new plugin chat; no starts.
- R3C/E1/E2 safe capabilities/preflight PASS; E3/E4 read routes return proper nonexistence response with valid KRCM format, rather than -32602.
- **E1 read-only Instagram HTTP 401** and **E2 non-YouTube status HTTP 401** remain independent AUTHORIZATION GAPS requiring narrowly targeted diagnosis.
- Full successful status/segments on currently retained jobs: NOT VERIFIED from that new-chat report. Existing historical jobs may have expired under 1h TTL; no new job should be created just to mask gaps.
- Current global KRC R4 public release HOLD, Telegram LIVE BLOCKED, all paid fallback DISABLED.
- Next: compare per-app scoped token/audience/allowed-route definitions and backend HTTP auth check order using safe code/log review; do not print bearer values, and do not relax auth based solely on these responses.
