# Bounded live MEDIA acceptance results — 2026-10-04

Status: LIVE ATTEMPTS COMPLETED WITH FAILURES; FULL LIVE TRANSCRIPT ACCEPTANCE NOT PASS.
This supersedes the earlier workspace blocker and probe-only observations for this bounded test.

## Authorization and workspace
Owner approved independent public video selection, Gemini Free data-use consent and free STT minutes. Owner then explicitly confirmed Render My Workspace / kolemasakar@gmail.com / tea-d9dsqdjrjlhs73ba1ga0. Reuse this workspace without asking again. Provider consent remains valid. Do not auto-replay failed provider jobs.

## Execution and restoration
All env updates used replace=false and changed ONLY the relevant KRC_R3Ex_CONFIRMATION_PROBE_ONLY flag. Render automatically triggered deployment at KRC SHA 4b7458b3c836dc4f9cb9df3cd39054683474e147. No separate duplicate deploy was triggered.

| Route | Activation deploy | Restore deploy | Final health |
|---|---|---|---|
| E2 Instagram | dep-db16gmh42hec73a8921g | dep-db16infavr4c73agpn6g | HTTP 200, probe-only=true, binding=true |
| E3 Facebook | dep-db16j4ad0e5s73ebqaf0 | dep-db16lb2d0e5s73ec40f0 | HTTP 200, probe-only=true, binding=true |
| E4 Telegram | dep-db16lougekts73cf8i40 | dep-db16mf49v7es73e73ai0 | HTTP 200, probe-only=true, binding=true |

Each activation and restore deploy reached live. Activated routes were verified probe-only=false before ONE real start; the next route was activated only after the preceding route was restored. Final all-three health read confirmed probe-only=true.

## Actual results
- YouTube jNQXAC9IVRw: previous start was uncertain due to 429; current lookup also initially returned 429. Canonical health returned 200 (request 062ecd69-7d61-4b97-ab98-f5d79ff16d21), then lookup returned 404. No job identity established, no repeat start. Job/provider consumption remains unproven, not claimed zero.
- Instagram C_bnaTAO2Ll: preflight can_continue=true, request 9c1b4d9e-92fa-4242-8f78-e6da2abfbd66; lookup404; real start FAILED, job KRCM_2c69d8b7-41f3-491c-ad3e-9589682b53df, request f12a3163-a888-4cdf-9309-91be9c16a738, FACEBOOK_AUDIO_NORMALIZATION_FAILED. Independent R3C status confirms same failed job.
- Facebook NASA video: FAILED, job KRCM_54d7f28a-1a04-44c8-b2a4-769abef45035, request 2e7556ab-0b25-4245-8929-259513cd5a31, FACEBOOK_RETRIEVAL_UNAVAILABLE. Independent R3C status confirms same failed job.
- Telegram GeneralStaffZSU/4530: FAILED, job KRCM_91086416-6df8-4178-8f52-5b9ecebfd4da, request 8f1a7afb-d808-4030-8f7a-ed39701f9f0f, TELEGRAM_MEDIA_UNAVAILABLE; public post exposes no browser-playable asset. Independent R3C status confirms same failed job.

All three real non-YouTube jobs report credit_charge_uncertain=false, credits_charged=0, stt_seconds_charged=0, segment_count=0, transcript_characters=0. STT was not reached. No segments were claimed verified or exported from these failed jobs.

## Confirmed code defect and isolated repair
Facebook live source_url dropped numeric ID 8368792419872400 from /videos/<title>/<ID>/. Exact source reproduction confirmed managed_media_url.ts retaining the title slug instead of video identity. VoiceBridge repair canonicalizes descriptive video URLs to /videos/<ID>/, retains distinct identities and rejects ambiguous trailing components.

Repair commit: f416d8c37b1c63e1c34521ebbcadf8445cb62b44, branch research/krc-peer-observation-isolated. NO VoiceBridge production deployment. The fix does not prove the live Facebook failure has no further causes.

Validation of repair:
- TypeScript build PASS, exit0.
- Facebook regression suites 28/28 PASS, exit0, including 3 new identity/parser/collision/ambiguous-input tests.
- Actual local cross-repository integration 9/9 PASS in20.87s, exit0, after repair.
- git diff --check PASS.

Instagram uses the shared Facebook-named file normalization implementation. Its error naming does not indicate incorrect platform dispatch. ffmpeg nonzero exit is mapped to a generic audio failure and stderr is discarded; specific root cause is not established. Earlier commentary calling it a separate diagnostic defect is clarified: naming is misleading, but no cross-platform routing defect was demonstrated.

## HTTP429 evidence limits
Render request queries returned no entries for 13:10–13:30Z, 14:30–14:53Z, and 14:53 onward, including a window with known successful route calls/jobs. App logs showed lifecycle events (service start13:13:52Z, stop13:29:11Z, start14:53:22Z), not per-request failure evidence. Absence of request logs cannot prove lack of upstream requests or identify cold-start/quota/limiter cause.

Correction to previous checkpoint timing: earlier proposed13:13–13:20Z log window was based on the health probe, not exact live start time. E2 real start was14:57:06Z, E3 15:02:47Z, E4 15:05:06Z; real timestamps above take precedence. 429 root cause remains OPEN.

## Remaining work
- Review/pin a bounded VoiceBridge rollout of the tested URL fix before any new Facebook provider attempt.
- Improve free retrieval/audio observability and validate candidates with actual playable audio before new jobs.
- Resolve YouTube 429 with upstream diagnostics; only explicitly instructed fresh retry of failed/uncertain work, never blind replay.
- Complete one successful transcript per direction with every segment page, contiguous indexes, exact count/UTF-16 character reconciliation and same-job read continuity.

No paid fallback, credential rotation, new service/infrastructure, main merge or Plugin publication. This is evidence of real failure points and one tested isolated fix, not completed live provider integration.
