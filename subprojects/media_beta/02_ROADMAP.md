# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 1.0
Status: ACTIVE
Updated: 2026-08-17

## Phase A - Closed MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Deliverables:

- separate K-Research & Critic beta identity;
- separate GPT Action contract;
- separate VoiceBridge media backend path;
- per-tester access-code model;
- dedicated Render beta target;
- production VoiceBridge unchanged;
- published K-Research & Critic unchanged.

Exit criteria:

- architecture documented;
- production boundaries explicit;
- feature branches and draft PRs created.

### A2. Resource protection

Status: COMPLETE_IN_CODE

Deliverables:

- subtitle-first acquisition;
- max video = 60 min;
- concurrency = 1;
- global STT budget = 7200 sec / UTC day;
- 16 kHz mono ~32 kbps STT fallback audio;
- temporary media cleanup;
- provider delete request;
- transcript/job TTL;
- access codes excluded from reports/checkpoints.

Exit criteria:

- automated CI green in VoiceBridge;
- KRC Store/package tests green.

### A3. Dedicated Render beta deployment

Status: NEXT

Tasks:

- create a new Render Blueprint/service from VoiceBridge feature branch;
- use `render.media-beta.yaml`;
- confirm service name `voicebridge-krc-media-beta-kolemasakar`;
- configure secrets only in Render Dashboard;
- do not modify `voicebridge-cloud-us`;
- validate `/api/v1/health`.

Required secrets:

- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

Exit criteria:

- dedicated beta endpoint reachable;
- health shows media beta configured;
- production VoiceBridge health unchanged.

### A4. Live transcript validation

Status: BLOCKED_BY_A3

Test set:

- Ukrainian YouTube video with captions;
- Russian YouTube video with captions;
- English YouTube video with captions;
- Ukrainian/Russian/English video requiring STT fallback;
- auto language detection case;
- invalid tester code;
- video >60 min;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification.

Exit criteria:

- captions path works without STT charge;
- fallback path works with expected quota charge;
- timestamps and language metadata are usable;
- `provider_data_deleted=true` observed on successful AssemblyAI cleanup where applicable;
- no beta secret appears in output/loggable response payloads.

### A5. Separate GPT Builder beta

Status: BLOCKED_BY_A4

Tasks:

- create `K-Research & Critic - MEDIA BETA` separately from public GPT;
- import beta instructions;
- import beta OpenAPI schema;
- configure Action bearer secret;
- point schema/server to dedicated beta Render endpoint;
- set unlisted/link distribution;
- configure privacy policy URL if required by Builder;
- do not alter public GPT.

Exit criteria:

- Action callable from GPT Preview;
- missing tester code handled correctly;
- invalid tester code handled correctly;
- transcript acquired and CriticProfile shown before research.

### A6. End-to-end beta acceptance

Status: BLOCKED_BY_A5

Scenario:

```text
YouTube URL
 -> beta access
 -> transcript
 -> claim inventory
 -> CriticProfile
 -> user approval
 -> web research
 -> Critic
 -> FINAL REPORT
 -> CLAIM VERIFICATION
 -> REVIEW PROTOCOL
```

Acceptance targets:

- 3 languages;
- both captions and STT fallback paths;
- no research before CriticProfile approval;
- no self-corroboration of video claims;
- useful timestamp-to-claim traceability;
- ordinary text workflow regression passes;
- checkpoint workflow regression passes.

### A7. Controlled tester rollout

Status: BLOCKED_BY_A6

Tasks:

- owner tests first;
- issue independent tester codes to up to three testers;
- collect failures by category;
- monitor Render bandwidth and AssemblyAI credits;
- adjust limits only through an explicit decision update.

Exit criteria:

- stable operation over representative beta workload;
- no material production regression;
- documented resource consumption.

## Phase B - Sustainable Free Media

Status: PLANNED_AFTER_BETA

### B1. Cloudflare Whisper proof of concept

Compare against AssemblyAI for:

- Ukrainian;
- Russian;
- English;
- timestamps;
- names/numbers/acronyms;
- latency;
- effective free daily capacity.

### B2. Provider-neutral transcript router

Routing target:

```text
captions
 -> free cloud Whisper quota
 -> optional local Whisper fallback
```

### B3. Local Media Node proof of concept

Evaluate:

- faster-whisper;
- whisper.cpp;
- CPU-only operation;
- optional GPU acceleration;
- public HTTPS exposure;
- availability and security model.

### B4. Remove permanent AssemblyAI dependency from public free path

AssemblyAI may remain as:

- development comparator;
- emergency fallback;
- optional paid reliability path.

It must not be required for the intended sustainable free public mode.

## Phase C - Public media release

Status: FUTURE

Public release is allowed only after:

- sustainable resource model validated;
- privacy configuration validated;
- Free-plan ChatGPT test passed;
- Actions runtime compatibility validated;
- production smoke tests passed;
- explicit user approval to promote from beta.

## Roadmap rule

A roadmap item marked COMPLETE means implementation evidence exists. A roadmap item marked NEXT/BLOCKED/PLANNED must never be described as already deployed or validated.