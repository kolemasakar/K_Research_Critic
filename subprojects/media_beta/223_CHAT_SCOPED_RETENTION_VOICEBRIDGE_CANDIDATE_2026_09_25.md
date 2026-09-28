# KRC MEDIA checkpoint 223 — VoiceBridge chat-scoped retention candidate

Date: 2026-09-25
Status: DEVELOPMENT_CANDIDATE / NO_DEPLOY / NO_PROVIDER_WORK / TESTS_PASS_DEPLOY_PENDING

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
- Candidate commit at this checkpoint: 8cd7fbd95b826982475dabaf08d3f6e872a9c4d8
- config.ts default MEDIA_JOB_TTL_SECONDS changed 3600 -> 21600; explicit environment override retained.
- public_gemini_youtube.ts direct-engine fallback TTL changed 3600 -> 21600.
- tests/public_gemini_youtube.test.ts: added fixture-based tests for default/override TTL, read-only lookup after a lost response, paginated complete read, explicit provider call count = 1 and no implicit retry following failure.
- Candidate documentation: docs/KRC_MEDIA_CHAT_RETENTION_6H_2026-09-25.md.
- Test code committed and tested on an isolated checkout on krc-cobalt under /tmp/krc-voicebridge-validation-20260925/repo (no production service modification). Exact SHA: 8cd7fbd95b826982475dabaf08d3f6e872a9c4d8. Node v24.21.0; npm 11.19.0; npm ci --ignore-scripts --no-audit --no-fund succeeded; npm run check: TypeScript build PASS, complete suite 273 PASS / 0 FAIL, exit code 0; targeted Gemini test file 12 PASS / 0 FAIL. Tests use fixtures; no Gemini provider execution. GitHub PR workflow runs for earlier candidate commit 304bd968: none returned. No claim of test PASS.

## Runtime and recovery boundary
- Render service voicebridge-krc-media-beta-kolemasakar currently deploys the earlier VoiceBridge agent/krc-media-gemini-migration branch at d3873bf13e60c4932ab08cae449c924051be4a37; the candidate is not deployed.
- Earlier old job KRCM_a01a95b5-b91a-47b4-9d2d-5323fa36c8a4: historical 30 segments/47289 characters, later 404. Full original transcript still unavailable.
- Previous Neon production read-only SELECT returned no old-job row and no rows with updated_at on 2026-09-25 at time checked. Exact active Render->Neon project/branch endpoint identity is not independently proven. Do not infer historical provider work never occurred or irreversible deletion.
- Original checkpoint 222 remains authoritative for the historical transcript-recovery evidence and audit checkpoint 221 remains authoritative for partial report traceability. This checkpoint governs only the newer owner-approved development task.

## Next gate
1. COMPLETE: npm ci && npm run check against exact candidate SHA 8cd7fbd95b826982475dabaf08d3f6e872a9c4d8; 273 PASS / 0 FAIL, exit 0.
2. Review client/plugin flow for prompt all-pages readback and safe temporary in-chat export; do not claim it is already automated.
3. Check Render effective MEDIA_JOB_TTL_SECONDS before deployment. If an environment override is 3600, changing code defaults alone will not alter runtime.
4. Review PR/commit and obtain separate deployment authorization.
5. No Gemini provider execution, Render changes, public GPT/Plugin changes, database writes/restores or merges without separate authorization.

## Follow-up validation
VoiceBridge candidate code commit 0e0b4d0: added a read-only paginated transcript collector. On an isolated krc-cobalt checkout, TypeScript build passed and 278 of 278 tests passed (exit 0). The dedicated collector suite passed 5 of 5 tests. Current live Render health still reports a 3600-second TTL; the candidate is not deployed. Plugin integration and preservation of original transcript separators remain open. No provider execution or production changes.

## Owner decision: returning after temporary retention expires
The owner clarified that the earlier YouTube transcript was unavailable because they returned to the chat after a significant delay. On return, check existing job and transcript first. If no longer accessible, offer reprocessing of the original video, and obtain fresh explicit consent before any provider start. Never automatically re-run a provider merely because a status/segments endpoint returns HTTP 404; distinguish expiry from identity/storage faults as far as read-only checks allow. Reuse the existing YouTube, Instagram, Facebook and Telegram pipelines. VoiceBridge candidate policy doc commit c9911cb2 records this decision. This is an approved policy/documentation change, not a production deployment.

## Existing-module audit and text-integrity correction
The current VoiceBridge cloud already has pagination paths in media_client_http, public_cobalt_media, managed_media_service and public_gemini_youtube. New helper is not a replacement for the four existing platform pipelines. Inspected Gemini's chunkTranscriptWords fallback: it trimmed each 1600-character segment, losing boundary whitespace. Candidate code commit dabed98 preserves exact chunk boundaries and adds a long transcript round-trip test. Isolated exact-code-SHA TypeScript build passed; targeted 12/12 tests passed; full 279/279 tests passed, exit 0. VoiceBridge documentation commit 8b86fa8. No production or private Plugin mutation; existing-module late-return wiring remains to be checked.
