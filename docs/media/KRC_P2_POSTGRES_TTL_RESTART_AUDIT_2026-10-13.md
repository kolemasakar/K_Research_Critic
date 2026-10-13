# KRC P2 — Postgres persistence, TTL and restart acceptance audit (2026-10-13)

## Scope and non-destructive evidence
Owner requested execution of P2: verify VoiceBridge job persistence and expiration, then controlled restart/resume. This checkpoint is a read-only audit of deployed source, Neon schema/data, and Render runtime identity/logs. A live restart was **not** performed because neither an active, nonexpired test job nor a confirmed Render→Neon DSN identity was available. Restarting an empty service would not prove persistence; seeding synthetic jobs in live production DB without provenance would contaminate owner MEDIA job state. No MEDIA starts, SQL writes, Render deploys or restarts.

## Production identities
- Render VoiceBridge service `srv-da1kic5bedkc73d6fk60`, Free plan, 1 instance, autoDeploy off, branch `agent/krc-media-gemini-migration`.
- Latest live Render deployment `dep-db4vlu0473hc739b20sg`, **exact deployed Git SHA `072658ff512802262cef00ff424b87eedde1f934`**, deployed 2026-10-10T08:45:08Z; GitHub source audited at that exact commit.
- Connected Neon project `plain-snow-71973546`, one primary production branch `br-summer-union-b2qlszfv`, current connected database `krc_media_beta`.
- Render connection integration exposes service metadata and deployment identity, but not read-only environment values. Therefore **actual Render KRC_MEDIA_DATABASE_URL target and MEDIA_JOB_TTL_SECONDS override remain unverified**; no secrets attempted or displayed. Capabilities previously reported `durable_store=postgres` and `restart_resilient_jobs=true`; configuration claims are not live durability evidence.

## Exact deployed code semantics
- `src/cloud/src/config.ts` lines 429–434: default `MEDIA_JOB_TTL_SECONDS=3600`, validated min 300 / max 86400 seconds; actual live override not exposed. Do not assert an effective one-hour TTL.
- `src/cloud/src/managed_media_persistence.ts`: `ManagedMediaPersistentStore` Postgres store, `findByRequestKey()` and `get()` both require `expires_at>now()`, `purgeExpired()` deletes rows with `expires_at<=now()`; stored job includes payload and segments JSONB, immutable job id and request key.
- `src/cloud/src/media_client_persistence.ts`: `MediaClientPersistentStore` with active `expires_at>now()` lookups, `purgeExpired()` deletes expired client jobs; quota charges retention deletes day rows earlier than current UTC date minus 2 days.
- All observations are actual deployed-commit source inspection, not only unmerged branch design.

## Read-only Neon and Render evidence
- 2026-10-13T20:07:38Z Neon SQL `current_database()=krc_media_beta` yielded `managed_rows=0`, `client_rows=0`, `charges_rows=0`; both active job counts 0. Tables and expected non-null job_id/request_key/status/expires_at/updated_at and charges columns were verified via `information_schema`.
- Prior historical Instagram 41s and Facebook 180s jobs were observed earlier as COMPLETED, but their current status request returns 404, consistent with (not proving) expiry/purge. Current connected Neon has zero rows; no job still inside TTL can be used as an authoritative restart proof.
- Render logs from Oct 10–13 contained many normal `service_started` and `service_stopping` (auto-sleep) observations, including Oct 13 18:45:51Z startup and 19:12:57Z shutdown. Those prove process lifecycle only, not durable job survival. No explicit persistence failure appeared in the subset of logs returned; absence of messages is not a health proof.

## Gate ledger
| Gate | Status | Why |
|---|---|---|
| Deployed source TTL expiry/cleanup behavior | PASS (static source) | At deployment SHA |
| Connected Neon schema/table integrity (read-only) | PASS | Expected fields and reachable DB |
| Connected Neon active job inventory | PASS (0 active) | No testable live job |
| Effective runtime TTL | UNVERIFIED | Render env value inaccessible |
| Confirm Render database DSN identity | UNVERIFIED | No read-only Render env |
| Nonexpired same-job before/after controlled restart | NOT RUN | No eligible active record |
| Content, job_id, segments, billing parity after restart | NOT RUN | Dependent on previous gate |
| Full P2 durability acceptance | OPEN | Direct restart evidence missing |

## Safe next acceptance protocol
1. Verify only non-secret Render runtime connection target (database name/host identity) and effective TTL. Avoid outputting DSN, token, password, environment dump.
2. Use one owner-approved short reel test that yields `COMPLETED`, capture `job_id`, `expires_at`/effective TTL, segment count, canonical segment text checksum and billing figures before expiry, with FREE_ONLY provider safeguards. No duplicate post.
3. Within TTL, confirm the matching job/record on authoritative Neon using read-only SQL; reconcile external public ID vs internal ID.
4. Perform one authorized Render controlled restart only while record is still unexpired and after ensuring no pending job. Then read status and all paginated segments; compare same IDs, sha256/UTF-16 counts, charge state. A normal Render autosleep/awake without such before/after data does not satisfy gate.
5. After expiry, separately test that API returns safe expired/not-found status and that cleanup eventually removes records, without mistaking expected expiry for lost durability. Preserve compliance, FREE_ONLY, owner consent and zero paid fallback.

Verdict: **P2 STATIC TTL + READONLY SCHEMA PASS; LIVE RESTART DURABILITY OPEN**. Product release remains HOLD.
