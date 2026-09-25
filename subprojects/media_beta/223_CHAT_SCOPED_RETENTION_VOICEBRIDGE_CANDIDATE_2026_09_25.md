# KRC MEDIA checkpoint 223 — VoiceBridge chat-scoped retention candidate

Date: 2026-09-25
Status: DEVELOPMENT_CANDIDATE / NO_DEPLOY / NO_PROVIDER_WORK / TEST_EXECUTION_PENDING

## Owner-approved policy
- MEDIA data serves a time-sensitive investigation within the current ChatGPT chat.
- Temporary job/transcript technical TTL: six hours (21600 seconds) after last persisted update.
- Read all segments promptly when a job completes; verify segment count, order and transcript character count before analysis.
- Do not automatically create a permanent archive. Retain beyond the chat only on separate owner instruction.
- Chat closure cannot be detected reliably by the backend; TTL is a fallback, not chat-lifecycle synchronization.
- A failed or interrupted provider request must not trigger another Gemini call without new explicit owner consent.

## Verified implementation
- VoiceBridge repository: kolemasakar/VoiceBridge
- Candidate branch: agent/krc-media-chat-retention-6h-20260925
- Candidate commit at this checkpoint: 304bd968cfe878c7f7082f7d127d49a5c742e2a5
- config.ts default MEDIA_JOB_TTL_SECONDS changed 3600 -> 21600; explicit environment override retained.
- public_gemini_youtube.ts direct-engine fallback TTL changed 3600 -> 21600.
- tests/public_gemini_youtube.test.ts: added fixture-based tests for default/override TTL, read-only lookup after a lost response, paginated complete read and no implicit retry following failure.
- Candidate documentation: docs/KRC_MEDIA_CHAT_RETENTION_6H_2026-09-25.md.
- Test code committed; full Node/TypeScript suite has NOT been executed/verified. No claim of test PASS.

## Runtime and recovery boundary
- Render service voicebridge-krc-media-beta-kolemasakar currently deploys the earlier VoiceBridge agent/krc-media-gemini-migration branch at d3873bf13e60c4932ab08cae449c924051be4a37; the candidate is not deployed.
- Earlier old job KRCM_a01a95b5-b91a-47b4-9d2d-5323fa36c8a4: historical 30 segments/47289 characters, later 404. Full original transcript still unavailable.
- Previous Neon production read-only SELECT returned no old-job row and no rows with updated_at on 2026-09-25 at time checked. Exact active Render->Neon project/branch endpoint identity is not independently proven. Do not infer historical provider work never occurred or irreversible deletion.
- Original checkpoint 222 remains authoritative for the historical transcript-recovery evidence and audit checkpoint 221 remains authoritative for partial report traceability. This checkpoint governs only the newer owner-approved development task.

## Next gate
1. Run npm ci && npm run check against the exact candidate SHA, record pass/fail and logs.
2. Review client/plugin flow for prompt all-pages readback and safe temporary in-chat export; do not claim it is already automated.
3. Check Render effective MEDIA_JOB_TTL_SECONDS before deployment. If an environment override is 3600, changing code defaults alone will not alter runtime.
4. Review PR/commit and obtain separate deployment authorization.
5. No Gemini provider execution, Render changes, public GPT/Plugin changes, database writes/restores or merges without separate authorization.
