# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 1.2
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

Validation:
- VoiceBridge automated CI green;
- KRC Store/package tests green.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Completed:
- GitHub -> Render API control bridge validated;
- dedicated service `voicebridge-krc-media-beta-kolemasakar` created;
- service ID `srv-da1kic5bedkc73d6fk60`;
- branch `agent/krc-media-transcript` verified;
- plan `free` verified;
- service-level beta secrets configured;
- post-secret deploy reached `live`;
- beta `/api/v1/health` HTTP 200;
- `media_transcript.configured=true` verified;
- media mode `closed_beta` verified;
- production `voicebridge-cloud-us` health HTTP 200 / `status=ok` verified;
- production was not modified by beta deployment.

Resolved incident:
- first secret-enabled redeploy failed because a beta access-code entry was shorter than 12 characters;
- tester codes corrected;
- redeploy succeeded.

Exit criteria: COMPLETE.

### A4. Live transcript validation

Status: NEXT

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

Execution order:
1. short public YouTube video with usable captions — validate subtitle-first path without STT quota use;
2. separate short video with no usable captions — validate AssemblyAI fallback;
3. language matrix UK/RU/EN and auto;
4. access/resource guard cases;
5. provider cleanup evidence.

Exit criteria:
- captions path works without STT charge;
- fallback path works with expected quota charge;
- timestamps and language metadata are usable;
- `provider_data_deleted=true` observed on successful AssemblyAI cleanup where applicable;
- no beta secret appears in response/loggable payloads.

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
- captions and STT fallback paths;
- no research before CriticProfile approval;
- no self-corroboration of video claims;
- timestamp-to-claim traceability;
- ordinary text workflow regression passes;
- checkpoint workflow regression passes.

### A7. Controlled tester rollout

Status: BLOCKED_BY_A6

Tasks:
- owner tests first;
- issue independent tester codes to up to three testers;
- collect failures by category;
- monitor Render bandwidth and AssemblyAI credits;
- adjust limits only through explicit decision update.

## Phase B - Sustainable Free Media

Status: PLANNED_AFTER_BETA

### B1. Cloudflare Whisper proof of concept
Compare against AssemblyAI for Ukrainian, Russian, English, timestamps, names/numbers/acronyms, latency, and effective free daily capacity.

### B2. Provider-neutral transcript router

```text
captions
 -> free cloud Whisper quota
 -> optional local Whisper fallback
```

### B3. Local Media Node proof of concept
Evaluate faster-whisper, whisper.cpp, CPU-only operation, optional GPU acceleration, public HTTPS exposure, availability, and security.

### B4. Remove permanent AssemblyAI dependency from public free path
AssemblyAI may remain as development comparator, emergency fallback, or optional paid reliability path. It must not be required for intended sustainable free public mode.

## Phase C - Public media release

Status: FUTURE

Public release requires sustainable resource validation, privacy validation, Free-plan ChatGPT test, Actions runtime compatibility, production smoke tests, and explicit user approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation evidence exists. NEXT/BLOCKED/PLANNED must never be described as already validated.
