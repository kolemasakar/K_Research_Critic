# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.0
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## 1. Executive state

Current phase:

`A3 - Dedicated Render beta deployment`

Current state:

`CODE_READY / CI_GREEN / LIVE_BETA_NOT_DEPLOYED`

The next action is to create the dedicated Render beta service from the VoiceBridge feature branch using its beta Blueprint. Do not proceed to GPT Builder before live backend validation.

## 2. K-Research & Critic repository

Repository:

`kolemasakar/K_Research_Critic`

Production branch:

`main`

Media feature branch:

`agent/video-url-research`

Draft PR:

`#8 - Add isolated closed MEDIA BETA video claim workflow`

PR state at checkpoint:

- open;
- draft;
- unmerged;
- base `main`;
- production public GPT intentionally unchanged.

Implemented on feature branch:

- optional YouTube media workflow;
- transcript evidence boundary;
- CriticProfile gate preserved;
- independent claim verification after approval;
- CLAIM VERIFICATION output;
- beta Action OpenAPI schema;
- separate beta GPT instructions;
- separate beta manifest;
- beta privacy notes;
- package validator and tests;
- closed-beta runbook;
- this documentation subproject.

Latest verified KRC CI before this documentation checkpoint:

- Python 3.13 tests: PASS;
- Python 3.14 tests: PASS;
- dependency integrity: PASS;
- Ruff: PASS;
- Mypy: PASS;
- repository policy: PASS;
- GPT Store package validation: PASS;
- coverage gate: PASS.

Documentation-only commits created after that CI may trigger a new run; check current GitHub CI before any merge.

## 3. VoiceBridge repository

Repository:

`kolemasakar/VoiceBridge`

Production branch:

`main`

Media feature branch:

`agent/krc-media-transcript`

Draft PR:

`#28 - Add closed MEDIA BETA transcript backend for K-Research & Critic`

PR state at checkpoint:

- open;
- draft;
- unmerged;
- base `main`;
- existing production VoiceBridge remains unchanged.

Implemented on feature branch:

- public HTTPS YouTube URL validation;
- metadata inspection;
- live-stream rejection;
- subtitle-first acquisition;
- source languages `auto`, `uk`, `ru`, `en`;
- AssemblyAI Universal-2 fallback;
- per-tester access-code allowlist;
- max video 60 min for beta;
- concurrency 1 for beta;
- daily STT fallback budget 7200 sec UTC;
- fallback audio optimized to mono 16 kHz approximately 32 kbps;
- async media job states;
- timestamped segment pagination;
- temporary media cleanup;
- AssemblyAI transcript delete attempt;
- beta quota diagnostics;
- dedicated Render Blueprint `render.media-beta.yaml`.

Latest verified VoiceBridge CI:

- TypeScript build: PASS;
- cloud tests: PASS;
- media beta tests: PASS;
- browser-extension regressions: PASS;
- repository documentation checks: PASS.

## 4. Production endpoints and beta target

Existing VoiceBridge production:

`https://voicebridge-cloud-us.onrender.com`

Status rule:

Do not deploy beta code over this service.

Dedicated beta target defined in infrastructure configuration:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Checkpoint status:

`NOT YET CREATED / NOT YET LIVE-VALIDATED`

## 5. Secrets

Required for the dedicated beta service:

- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

Checkpoint status:

- not committed to GitHub;
- not configured in a dedicated beta Render service yet.

`KRC_MEDIA_BETA_CODES` should contain four independent random tester codes separated according to the backend configuration contract. Never place real values in repository documentation.

## 6. What is NOT complete

The following are explicitly not complete:

- dedicated Render beta service creation;
- beta Render secrets configuration;
- beta `/api/v1/health` live check;
- real YouTube captions test;
- real AssemblyAI fallback test;
- live Ukrainian media test;
- live Russian media test;
- live English media test;
- automatic language detection live test;
- provider deletion live verification;
- live quota/concurrency validation;
- separate GPT Builder beta creation;
- beta Action bearer secret in Builder;
- hosted valid privacy policy URL for Builder if required;
- GPT Preview end-to-end test;
- Free-plan beta test;
- tester rollout;
- public media production rollout.

## 7. Current next action

Create the dedicated Render beta service using the VoiceBridge repository and `render.media-beta.yaml`.

Required rule:

Do not merge PR #28 or PR #8 merely to perform the first beta test unless the deployment mechanism explicitly requires it. Prefer the feature branch/Blueprint path that preserves production isolation.

After Render service creation:

1. configure the three server-side secrets;
2. deploy;
3. check `/api/v1/health`;
4. verify production VoiceBridge remains healthy;
5. begin live transcript tests from `05_TEST_PLAN.md`.

## 8. Update rule

Whenever a release gate changes state, update this file before ending the chat or before generating a cross-chat handoff.