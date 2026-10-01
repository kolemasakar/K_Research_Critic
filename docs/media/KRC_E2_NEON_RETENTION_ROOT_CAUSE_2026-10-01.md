# KRC E2 Neon retention investigation — 2026-10-01

## Evidence
- VoiceBridge Render live deploy `dep-daqp1iou01pc73fgjb00`, commit `d3873bf13e60c4932ab08cae449c924051be4a37`.
- At this **exact deployed commit**, `src/cloud/src/managed_media_persistence.ts` `purgeExpired()` executes `DELETE FROM krc_managed_media_jobs WHERE expires_at <= now()` and `DELETE FROM krc_media_stt_charges WHERE day_utc < current_date - interval '2 days'`.
- At the same commit, `src/cloud/src/media_client_persistence.ts` `purgeExpired()` deletes expired client jobs and old STT charges with the same age cutoff.
- At this commit `src/cloud/src/config.ts` `mediaJobTtlSeconds` defaults to 3600 seconds, permitted 300–86400; `.env.example` specifies `MEDIA_JOB_TTL_SECONDS=3600`. **Current Render override has not been read**; do not claim exact runtime TTL.
- Neon read-only check on documented project `plain-snow-71973546`, primary/default `production` branch `br-summer-union-b2qlszfv`, database `krc_media_beta`: `krc_managed_media_jobs=0`, `krc_media_client_jobs=0`, `krc_media_stt_charges=0`. The project branch is ready; the database and tables exist.
- Historical checkpoint 127 recorded 10 STT charge rows on this same Neon target after 2026-09-19 cutover; checkpoints 137–138 recorded a successful Instagram E2E job and restart replay on 2026-09-19. Deployed retention/purge rules plausibly explain disappearance of historical records by 2026-10-01. **No proof of migration or data loss** from empty tables alone.
- New attempted URL `https://www.instagram.com/reel/Dcea3BiPTBm/` read-only lookup returned HTTP 404 after VoiceBridge warmup. No result was captured from the one attempted start. Owner's before/after AssemblyAI Free balance remained $48.31, but delayed accounting is possible.
- Existing E2 remains healthy, bound and `confirmation_probe_only:true` after verified rollback. No additional start authorized or executed during this investigation.

## Remaining verification
1. Compare current Render VoiceBridge `KRC_MEDIA_DATABASE_URL` **non-secret target identity only** (host/project/db, never password or full DSN) with documented Neon project; connected Render tools do not expose environment reads. An authorized owner-side dashboard comparison or secure remote inspection is required.
2. Inspect non-secret effective `MEDIA_JOB_TTL_SECONDS` and purge invocation timings without exposing credentials.
3. For future E2E, capture returned job ID immediately, poll status/segments within actual TTL and record audit before expiry; do not treat a later 404 as evidence no job was ever created.
4. If owner elects to repeat the real start, request fresh explicit approval after reviewing this evidence; keep Free-only and restore probe-only mode afterward.
5. Unused isolated E2 remains pending deletion after owner verification gate; connected Render integration has no delete-service action.

## Conclusion
`RETENTION_PURGE_EXPLAINS_HISTORICAL_EMPTY_TABLES=SUPPORTED_BY_DEPLOYED_CODE`; `ACTUAL_RUNTIME_TTL=UNVERIFIED`; `CURRENT_RENDER_DSN_TARGET=UNVERIFIED`; `LATEST_INSTAGRAM_START_OUTCOME=INCONCLUSIVE`.
