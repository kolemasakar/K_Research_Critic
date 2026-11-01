# KRC — NEW CHAT BOOTSTRAP (2026-11-01)

Project: K-Research & Critic. Restore exact snapshot `docs/integrations/KRC_PROJECT_SNAPSHOT_HANDOFF_2026-11-01.md` at immutable Git commit `2168dec979bc528dc5b3e52aeae1d9664160b06a` in `kolemasakar/K_Research_Critic` branch `agent/krc-public-media-r3-integration`. Its conclusions supersede earlier chat claims. Keep sources distinct: KRC, K_Sentinel, K_Science.

## Operating limits
STAGING ONLY, FREE_ONLY, Production NO-GO. Never enable deployed Artifact GET or Science signer, change active Stage127 :19017, install live Stage131, run external providers or science dispatch without explicit new authorization. Backup only on user request.

## Current execution
- Isolated source-only signed UDS artifact endpoint POST /v1/artifacts/read (not existing science /v1/execute), HMAC-SHA256, SO_PEERCRED, durable nonce, RequestLedger COMPLETE and artifact scope/TTL/SHA256, bounded spool <=200 MiB.
- Source-only HTTP hardening: TE+CL/duplicate CL reject, socket inactivity timeout 5 s, threaded server, sanitized 503.
- Latest isolated targeted HTTP hardening test **3/3 PASS**; latest full source suite *before* HTTP hardening **1108 PASS /17 SKIP**. No claim of post-hardening full suite.
- Sentinel 40 external GET negatives NOT_RUN, Science 48 real E2E NOT_RUN, partner final ACK absent.
- Open immediate work: absolute deadline, concurrent worker cap, extra declared-body bytes, early exceptions, disconnected clients, captured negative HTTP fixtures, near-200MiB/quota/expiry tests, complete repo regression, partner ACK.
- Related partner sources: Sentinel review commit `90beb13c2c3d2c8dd729e56ff565424f211e6901`; Sentinel PR38; Science PR7; KRC issue28.

## First action in next chat
1. Fetch pinned snapshot and latest GitHub source/partner comments.
2. Complete outstanding UDS security fixes in a non-deployed branch; execute tests and source full regression.
3. Update docs with immutable commit/fixtures and ask Sentinel for source-only ACK; maintain NO-GO.
