# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.1
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## 1. Executive state

Current phase:

`A3 - Dedicated Render beta deployment`

Current state:

`CODE_READY / CI_GREEN / RENDER_API_BRIDGE_READY / LIVE_BETA_NOT_DEPLOYED`

GitHub-to-Render control has been established and validated with a read-only Render API request. The dedicated beta service itself does not yet exist.

The next action is to create the dedicated Render beta service from the VoiceBridge feature branch using the approved isolated configuration. Do not proceed to GPT Builder before live backend validation.

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

Latest verified KRC CI:

- Python 3.13 tests: PASS;
- Python 3.14 tests: PASS;
- dependency integrity: PASS;
- Ruff: PASS;
- Mypy: PASS;
- repository policy: PASS;
- GPT Store package validation: PASS;
- coverage gate: PASS.

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
- dedicated Render Blueprint `render.media-beta.yaml`;
- GitHub Actions Render control workflow `.github/workflows/render-media-beta-control.yml`.

Latest verified VoiceBridge implementation CI:

- TypeScript build: PASS;
- cloud tests: PASS;
- media beta tests: PASS;
- browser-extension regressions: PASS;
- repository documentation checks: PASS.

Latest Render control verification:

- GitHub Actions workflow: `Render Media Beta Control`;
- run ID: `32050872616`;
- operation: `inspect`;
- `RENDER_API_KEY` available from GitHub Actions Secrets: YES;
- Render API authentication/discovery request: PASS / HTTP 200;
- dedicated beta service discovery: NOT FOUND;
- deployment operation: NOT EXECUTED;
- production Render service: NOT TOUCHED.

## 4. GitHub -> Render control boundary

The Render API credential is stored only as the GitHub Actions repository secret:

`RENDER_API_KEY`

Repository containing the secret/control workflow:

`kolemasakar/VoiceBridge`

The secret value is not stored in GitHub files, KRC documentation, checkpoints, reports, or chat output.

Control workflow:

`.github/workflows/render-media-beta-control.yml`

Current supported operations:

- `inspect` - read-only discovery/status;
- `deploy` - manual deployment of the isolated beta service only, after the service exists.

Safety rules implemented in the workflow:

- required deploy branch is `agent/krc-media-transcript`;
- target service name is fixed to `voicebridge-krc-media-beta-kolemasakar`;
- deployment is refused if that isolated service does not exist;
- production service `voicebridge-cloud-us` is never selected by the workflow;
- automatic push-triggered execution is read-only `inspect`.

## 5. Production endpoints and beta target

Existing VoiceBridge production:

`https://voicebridge-cloud-us.onrender.com`

Status rule:

Do not deploy beta code over this service.

Dedicated beta target defined in infrastructure configuration:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Checkpoint status:

`NOT YET CREATED / NOT YET LIVE-VALIDATED`

## 6. Secrets

Render control credential:

- `RENDER_API_KEY` - configured in VoiceBridge GitHub Actions Secrets and validated against the Render API.

Required service-level secrets for the dedicated beta service:

- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

Service-level secret checkpoint status:

- not committed to GitHub;
- not configured in a dedicated beta Render service yet because that service does not yet exist.

`KRC_MEDIA_BETA_CODES` should contain four independent random tester codes separated according to the backend configuration contract. Never place real values in repository documentation.

## 7. What is NOT complete

The following are explicitly not complete:

- dedicated Render beta service creation;
- beta Render service-level secrets configuration;
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

## 8. Current next action

Create the dedicated Render beta service using the VoiceBridge repository and the isolated beta configuration from `render.media-beta.yaml`.

The GitHub-to-Render API bridge is now available for read-only inspection and later manual beta deployment, but it deliberately does not create or modify production resources automatically.

Required rule:

Do not merge PR #28 or PR #8 merely to perform the first beta test unless the deployment mechanism explicitly requires it. Prefer the feature branch/isolated beta path that preserves production isolation.

After Render service creation:

1. configure the three service-level secrets;
2. deploy the beta branch;
3. check `/api/v1/health`;
4. verify production VoiceBridge remains healthy;
5. begin live transcript tests from `05_TEST_PLAN.md`.

## 9. Update rule

Whenever a release gate changes state, update this file before ending the chat or before generating a cross-chat handoff.