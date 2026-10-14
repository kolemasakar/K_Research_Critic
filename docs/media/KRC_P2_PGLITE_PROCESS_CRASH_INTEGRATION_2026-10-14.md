# KRC P2 — Isolated PostgreSQL-engine crash and duplicate replay tests
Date: 2026-10-14 UTC. Scope: manual, provider-free, test-only, NO production changes. Outcome **ISOLATED CRASH/REPLAY PASS** with explicitly bounded coverage.

## Isolation and implementation
- Test host: authorized Oracle `krc-cobalt`, unprivileged user `krcops`.
- VoiceBridge source isolated at `/tmp/krc_p2_offline_20261014/src/cloud`, source commit `48354ded605a6c703342678695bdce8cabe6d692` (not the older Render-deployed `072658ff512802262cef00ff424b87eedde1f934`).
- System Docker socket denied to `krcops`; no attempt to widen permissions or use sudo. A standalone PostgreSQL server was not available. Instead installed `@electric-sql/pglite` in temporary unprivileged test dependencies; **PGlite is a disk-persisted PostgreSQL engine (WASM), not the standard server/psql driver**.
- Executed **actual compiled VoiceBridge `ManagedMediaService`** business logic, with a test-only `ManagedMediaJobStore` backed by PGlite SQL, durable file-backed data directories, and deterministic fake provider calls counted in append-only text files. No actual media downloaded, no external STT/retrieval or paid fallback, no production PostgreSQL writes.
- Persisted reproducible Node test harness (131 lines) at `docs/media/tests/p2_pg_crash_harness.mjs`. Copy it into isolated VoiceBridge `src/cloud/` next to `dist/src` after `npm ci`, `npm run build`, and test-only `npm install --no-save --package-lock=false @electric-sql/pglite` to reproduce. Paths within harness are local `/tmp/krc_p2_pg_crash_20261014`; run in an isolated, fresh local data directory to prevent preexisting job key reuse.

## Tests and exact observed assertions
1. **COMPLETED + lost-response replay**: first `startNative` completes and persisted job is stored. Return value intentionally discarded as simulated lost client response. New independently initialized service/store opens identical disk-backed database, calls same `startNative`; same job id, `COMPLETED`, `reused=true`, same segment, external mock provider count **1**. Terminal trace: `LOST_REPLY_COMPLETED_REUSE_PASS provider_calls=1 job_same=true`.
2. **Concurrent start**: one service instance with gated provider starts two same-key requests; second returns reused `PROCESSING`; after winner resumes, `COMPLETED`, external mock provider count **1**. Terminal trace: `CONCURRENT_SINGLE_WINNER_PASS provider_calls=1`.
3. **Real process crash during PROCESSING, credit-uncertain legacy native path**: start a separate Node child holding in fake provider after persistent reservation, write a verified provider counter and ready marker, send `SIGKILL` to the known test child PID (no production PID touched). New Node process opens same disk database and calls start. `FAILED`, error `MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED`, `retryable=false`, `credit_charge_uncertain=true`, provider counter remains exactly **1**, on-disk record now `FAILED`. Terminal trace: `PROCESSING_KILL_CONFIRMED` then `CRASH_RECOVERY_FAIL_CLOSED_PASS provider_calls=1 status=FAILED`.
4. **Real process crash during Facebook free-only route**: separate isolated child starts `startFacebookFallback`, dummy Cobalt retrieval counter 1, persistent PROCESSING record, then SIGKILL. Fresh process opens same disk database and issues another user-origin start. Previous job becomes `FAILED` and a distinct retry-key job becomes `COMPLETED`; **2 free retrieval attempts, 1 mock AssemblyAI STT, 0 paid retrieval calls**, and two durable job states FAILED + COMPLETED. Terminal trace: `FB_PROCESSING_CRASH_INJECTED` then `FREE_FACEBOOK_CRASH_CONTROLLED_RETRY_PASS free_retrieval_calls=2 fake_stt_calls=1 paid_calls=0 two_job_states=FAILED_COMPLETED`.
- All these separate scenario-specific assertions passed. The initial all-in-one harness launcher timed out because its PGlite initialization readiness window was set to 8 seconds; **that first orchestrated test failed before crash injection**. Increased window in preserved harness to 60 seconds and successfully executed its crash/recovery component separately. Do not report first all-in-one attempt as PASS. Other individual components passed.
- PGlite disk startup was slower than an ordinary in-memory mock. Isolated source code was not merged or deployed.

## Interpretation
**This demonstrates actual two-process persistence and explicit process kill with PostgreSQL-engine storage and original VoiceBridge service logic**, beyond a single-process mock. It does **not** prove end-to-end production PostgreSQL adapter behavior (the original `ManagedMediaPersistentStore` psql-spawn implementation was replaced by a test-only store), Render fault injection, provider real-world idempotency or billing after transport ambiguity. The prior actual Render sleep/restart test separately proved COMPLETED short Instagram state survived a real cold stop/start.
- Credit-uncertain native route: never automatically replay orphan PROCESSING.
- Facebook free route: controlled retry **can result in a second free retrieval operation** after an interruption. This is expected in FREE_ONLY semantics, not exactly-once retrieval. No paid fallback occurs in this tested harness.
- Telegram live remains blocked; no test start.

## P2 acceptance
| Gate | State |
|---|---|
| Actual VoiceBridge business logic across independent Node processes | PASS isolated |
| PostgreSQL-engine persisted record across SIGKILL | PASS PGlite |
| Duplicate completed request no extra provider call | PASS |
| Same-service concurrent start one mock provider | PASS |
| Credit-uncertain orphan PROCESSING fail closed | PASS |
| Facebook free-only interrupted PROCESSING controlled retry | PASS, 2 free retrieval attempts |
| Paid fallback absent in Facebook harness | PASS, 0 calls |
| Exact production psql/Neon adapter process kill | NOT TESTED |
| Actual external provider lost-reply exactly-once | NOT TESTED |
| Global KRC MEDIA release acceptance | HOLD |

## Next boundary
If full P2 production-adapter evidence remains mandatory, use a disposable real Postgres instance with the **exact** `ManagedMediaPersistentStore` adapter and isolated runtime/credentials, and test an externally injected crash under a fake provider. Do not mutate production Neon's authoritative branch or use a paid server without approval. Existing offline suite at `48354de`: 276/276 PASS.
