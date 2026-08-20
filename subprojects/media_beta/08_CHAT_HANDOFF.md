# MEDIA BETA Chat Handoff

Canonical recovery and cross-chat continuation document for K-Research & Critic MEDIA BETA.

Version: 2.0
Status: ACTIVE_HANDOFF
Checkpoint date: 2026-08-20

## Recovery command

`recover MEDIA BETA A9`

## Mandatory recovery order

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/06_DECISION_LOG.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`
6. `subprojects/media_beta/24_A9_ZERO_CLIENT_INGESTION_PLAN.md`
7. `subprojects/media_beta/22_OWNER_ONLY_COMPLETION_PLAN.md`
8. `subprojects/media_beta/01_ARCHITECTURE.md`
9. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md`
10. `subprojects/media_beta/05_TEST_PLAN.md`

Then verify live GitHub state for KRC PR #8 and VoiceBridge PR #28 before any write.

## Repository context

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28.

Production branches, production VoiceBridge, and the published text-only KRC GPT remain unchanged.

Do not merge or promote either feature branch without explicit owner approval.

## Current checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

Current final product target:

`PRIVATE OWNER-ONLY ZERO-CLIENT MEDIA ANALYSIS`

## Accepted A8 baseline

The private GPT has passed an actual owner-operated end-to-end browser-assisted run:

```text
public YouTube URL
 -> private K-Research & Critic - MEDIA BETA GPT
 -> owner-designated beta credential
 -> KRCC job
 -> Helper 0.2.2
 -> captions-first transcript
 -> complete transcript retrieval
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> independent Research
 -> Critic/revision
 -> localized final report
```

Accepted report behavior:
- Ukrainian by default unless another response language is explicitly requested;
- media/transcript/source language does not switch report language;
- displayed headings localized;
- verdict labels localized;
- exactly one canonical verdict per material claim.

Canonical acceptance:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

Helper 0.2.2 remains a validated baseline/fallback, not the desired final normal UX.

## Accepted privacy/runtime baseline

Dedicated beta service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- endpoint `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`.

Accepted client-assisted Audio fallback:
- AssemblyAI EU base URL `https://api.eu.assemblyai.com`;
- Universal-2;
- normal provider deletion confirmed;
- durable KRCC Postgres jobs;
- durable STT quota ledger;
- 7200 sec/UTC day beta STT budget;
- retry-safe forced process-loss behavior.

## A9 approved direction

A9 is a platform-neutral `MediaSourceRouter`, not a YouTube-only product.

Target UX:

```text
media input in ChatGPT
 -> zero-client ingestion
 -> transcript
 -> requested Research/Critic workflow
 -> result in the same conversation
```

Approved ingress modes:

### Public media URLs

Initial adapters:
- YouTube public videos;
- Instagram public Reels/posts containing video;
- Facebook public Video/Reels;
- Telegram public posts containing video.

Boundary:
- public content only;
- no logins/passwords/cookies/account tokens/authenticated sessions;
- no private, friends-only, group-only or account-gated content;
- return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED` when authentication is required.

### Local media upload

Approved future ingress mode:
`local_upload`

Target:
- local video or audio attachment;
- embedded subtitles/text first when available;
- otherwise audio extraction/normalization -> accepted EU STT path;
- source media temporary and deleted after processing;
- ChatGPT attachment transport into the Action/backend still requires a technical feasibility test.

## A9 architecture audit

Status: COMPLETE.

VoiceBridge already contains a legacy server-side `KRCB_` flow:

```text
/api/v1/media/transcriptions
 -> yt-dlp server-side
 -> captions attempt
 -> audio fallback
 -> ffmpeg
 -> AssemblyAI
 -> transcript pages
```

Docker already contains yt-dlp, Node runtime support, and bgutil PO-token provider infrastructure.

Known blockers:
- legacy server-side AssemblyAI path is not yet aligned with the accepted EU endpoint contract;
- KRCB jobs/quota are in-memory instead of durable Postgres state;
- GPT Action still exposes client-assisted KRCC operations;
- public-platform adapters require separate live acceptance.

## A9 reachability evidence

Probe job:
`KRCB_252bb38a-aba7-4e2e-8148-b31d55974161`

Result:
`MEDIA_FETCH_FAILED: This live stream recording is not available.`

Interpretation:
- Render reached the YouTube extractor/source;
- no bot/login response;
- no HTTP 403/429;
- no PO-token failure;
- STT charge remained zero.

Marker:
`A9_2A_YOUTUBE_SERVER_REACHABILITY_PARTIAL_PASS`

This does not yet prove prerecorded metadata, captions-first extraction, Audio fallback, durability, or GPT zero-client integration.

## Latest verified CI before transition edits

KRC commit:
`0e283509aafd52de06a7f23a398ad8758a75d875`

GitHub Actions:
`Tests #503 - SUCCESS`

Transition-document commits after that point must be checked in the next chat before their CI state is called green.

## Exact next task in the new chat

1. Recover this handoff and the current-state/roadmap/decision documents.
2. Verify current KRC and VoiceBridge branch heads and CI.
3. Do not modify production or merge PRs.
4. Do not automatically resume public sharing/tester work.
5. Do not automatically start A9 implementation; wait for explicit owner instruction to continue A9.

When A9 implementation is authorized, the first engineering gate is privacy parity for the legacy server-side fallback: configurable AssemblyAI base URL using the accepted EU endpoint plus regression test. After that, use a normal prerecorded captioned public YouTube video for server-side metadata/captions proof.

## Terminal markers

`MEDIA_BETA_HANDOFF_V2_0`

`A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE`

`A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED`

`A9_IMPLEMENTATION_NOT_STARTED`

`PRODUCTION_ISOLATED_DRAFT_PRS_UNMERGED`
