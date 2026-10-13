# KRC parallel offline audit — 2026-10-13 (P0 cold-test isolation)

Scope: authorized owner audit of KRC R3C and E1–E4, FREE_ONLY, release/docs consistency, based on active branches only. No live MEDIA starts, VoiceBridge health GET, Caddy edits, provider calls, Render restarts/deploys, paid operations or main-branch merge from this audit.

## Audited repository and branches
- KRC: `kolemasakar/K_Research_Critic`, branch `agent/krc-public-media-r3-integration`.
- VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-gemini-migration`.
- R3C: `plugins/krc_migration_candidate/mcp_canary/r3c.py`.
- E1–E4: corresponding `r3e1.py` through `r3e4.py`.
- Relay: `plugins/krc_migration_candidate/p0_wake_relay_client.py`, `p0_wake_relay_server.py`.
- Code and route review performed by reading seven live GitHub branch files. The checks were static; do not misrepresent as a new test-suite execution.

## Static review
- R3C publishes read-only capabilities/status/lookup routes; its bounded readiness path detects a Cloudflare-labeled 429 and can attempt a single authenticated external relay wake. Consequential POST paths have explicit ambiguity handling; do not automatically replay a lost start response.
- E1 allows the single start `media_youtube_start` and requires `gemini_free_consent`.
- E2 allows the single start `media_instagram_start`; validates Instagram reel/post URL structure.
- E3 allows the single start `media_facebook_start`; validates Facebook media URLs.
- E4 allows the single start `media_telegram_start`; validates Telegram media URLs. This is a source-code contract, **not** evidence that live Telegram starts are permitted or unblocked.
- E2–E4 explicitly describe automatic paid fallback as forbidden. Static string scanning found no explicit `paid_fallback=true` assignment in the seven reviewed modules; this is not a full runtime/provider audit.
- Relay client pins HTTPS host, exact request body, bearer header, rejects redirect and is feature-gated. Server binds to loopback, uses fixed upstream health GET and a per-process cooldown, not a persistent keepalive.

## Existing tests and limitations
- `tests/test_p0_wake_recovery.py` contains isolated disabled-state, 429 attribution/readiness and one-relay-call tests.
- `tests/test_p0_wake_relay_server.py` checks missing auth => 403, bad body => 400, invalid method => 405, fixed upstream health GET and cooldown.
- Previous documented isolated full local test: 493 PASS, 17 opt-in skipped. Previous cross-repo fixture overlay: 17/17 PASS. These results were **not rerun** during this checkpoint.
- `docs/media/KRC_R3C_E1_E4_FINAL_ACCEPTANCE_MATRIX_2026-10-10.md` lists R3C OPEN, E1/E2/E3 PARTIAL, E4 BLOCKED; live long-media 480–720-second coverage remains unverified, and fixture compatibility is not evidence of live durable persistence.
- `docs/media/KRC_LONG_MEDIA_LIVE_TEST_PROTOCOL_2026-10-10.md` is the future P1 runbook; use it only after P0 cold-gate acceptance.

## Live P0 status as recorded from 2026-10-13 operations
- Authorized owner installed Caddy exact path `/krc-wake/v1` with original Cobalt fallback preserved; independent public checks: wake GET=405, unauth POST=403, Cobalt GET=200. Backup `/etc/caddy/Caddyfile.bak-krc-p0-20261013T092409Z`.
- Local authenticated `krc-cobalt` relay wake returned HTTP 200; this proves local client-to-relay, not Render authentication.
- Render R3C service `srv-dale3r942hec73c5t9hg` deployed with `KRC_WAKE_RELAY_ENABLED=1`.
- Cold test #1 around 10:51 UTC: VoiceBridge 429 and relay_rejected.
- Cold test #2 around 11:16 UTC: VoiceBridge 429 and relay_rejected; relay log `reason=auth_or_path`. Subsequent diagnostic update separated auth/path reasons without exposing secrets.
- Owner independently identified one missing token character in Render and corrected it. Latest Render deploy `dep-db71bq2d0e5s73ana93g` LIVE at 11:29:14 UTC. Third cold retest scheduled; **no PASS claimed** pending evidence.
- Root origin of Render/Cloudflare edge HTTP 429 remains unverified by human support. Do not claim Cloudflare emitted it merely from `server: cloudflare`.
- No paid provider jobs or new MEDIA processing were initiated by this audit.

## Remaining acceptance gates
1. Third genuine cold test after corrected token: R3C capabilities, relay server authenticated success, VoiceBridge startup and no hidden provider work; collect corroborating logs.
2. At least two more independent cold successes after first true success; no keepalive in between; measure elapsed startup, document origin uncertainty.
3. P1 long-media Instagram and Facebook 480–720s tests only after P0; Telegram live execution remains blocked until specifically unblocked through the approved safety mechanism.
4. Reproduce all opt-in cross-repo tests in a committed fixture-compatible environment; then audit actual PostgreSQL durability after controlled restart in a separate approved window.
5. Update main roadmap/final acceptance matrix only after real evidence. FREE_ONLY, no paid fallback, no public plugin publication and no arbitrary URL relay remain non-negotiable.

This is an additive docs-only checkpoint on an existing development branch, not acceptance, a code change or a claim of new runtime testing.
