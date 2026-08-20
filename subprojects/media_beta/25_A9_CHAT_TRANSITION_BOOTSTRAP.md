# A9 New-Chat Transition Bootstrap

Version: 1.0
Status: ACTIVE_BOOTSTRAP
Created: 2026-08-20

## Start command

In the new project chat, send:

`recover MEDIA BETA A9`

Then instruct the assistant to use this repository checkpoint before continuing.

## Repository sources

KRC:
- `kolemasakar/K_Research_Critic`
- branch `agent/video-url-research`
- draft PR #8

VoiceBridge:
- `kolemasakar/VoiceBridge`
- branch `agent/krc-media-transcript`
- draft PR #28

Do not merge either PR or modify production without explicit owner approval.

## Mandatory read order

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/06_DECISION_LOG.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/08_CHAT_HANDOFF.md`
6. `subprojects/media_beta/23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`
7. `subprojects/media_beta/24_A9_ZERO_CLIENT_INGESTION_PLAN.md`
8. `subprojects/media_beta/22_OWNER_ONLY_COMPLETION_PLAN.md`

Then verify live GitHub branch heads and CI before writes.

## Canonical checkpoint

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

## What is already accepted

- isolated MEDIA BETA backend;
- browser-assisted captions-first intake;
- AssemblyAI EU Universal-2 Audio fallback;
- durable KRCC Postgres jobs and quota ledger;
- forced process-loss behavior;
- separate private MEDIA BETA GPT;
- CriticProfile approval gate;
- owner-operated end-to-end Research/Critic flow;
- Ukrainian default response language;
- localized headings and verdicts;
- exactly one verdict per material claim;
- owner-designated credential live validation;
- A8 private browser-assisted baseline PASS.

## What is paused

- external Tester 1/2/3 rollout;
- GPT public/link sharing investigation and appeal;
- public Store promotion;
- production merge.

Do not resume these automatically.

## A9 target

Final normal UX:

```text
media input in ChatGPT
 -> MediaSourceRouter
 -> zero-client transcript acquisition
 -> requested analysis
 -> result in the same conversation
```

Approved future ingress:
- public YouTube;
- public Instagram video/Reels;
- public Facebook Video/Reels;
- public Telegram video posts;
- local video/audio upload via `local_upload`.

Public URL policy:
- public content only;
- no user login/password/cookies/authenticated session/account token;
- auth/private content -> `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

## A9 code audit result

VoiceBridge already has legacy server-side `KRCB_` ingestion:

```text
/api/v1/media/transcriptions
 -> yt-dlp
 -> captions attempt
 -> audio fallback
 -> ffmpeg
 -> AssemblyAI
 -> transcript pages
```

Main blockers:
1. legacy server-side AssemblyAI endpoint must be aligned with accepted configurable EU routing;
2. KRCB jobs/quota are in-memory and need durable persistence;
3. GPT Action currently uses client-assisted KRCC operations;
4. every public platform adapter requires separate live acceptance;
5. ChatGPT attachment-to-backend transport for `local_upload` still needs feasibility validation.

## Existing A9 probe evidence

Job:
`KRCB_252bb38a-aba7-4e2e-8148-b31d55974161`

Result:
`MEDIA_FETCH_FAILED: This live stream recording is not available.`

Interpretation:
- server-side Render -> YouTube extractor reachability confirmed for that probe;
- no bot/login, 403, 429 or PO-token failure;
- STT charge zero;
- prerecorded metadata/captions/audio not yet accepted.

## Next action rule

Do not automatically implement A9 on recovery.

Wait for explicit owner instruction. When authorized, first close privacy parity for server-side STT (configurable EU AssemblyAI endpoint + test), then run a normal prerecorded captioned YouTube server-side metadata/captions probe.

## Terminal marker

`A9_NEW_CHAT_BOOTSTRAP_READY`
