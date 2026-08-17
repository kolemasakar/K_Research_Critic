# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 1.4
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
- beta `/api/v1/health` HTTP 200;
- `media_transcript.configured=true` verified;
- media mode `closed_beta` verified;
- production `voicebridge-cloud-us` health HTTP 200 / `status=ok` verified;
- production was not modified by beta deployment.

Exit criteria: COMPLETE.

### A4. Live transcript validation

Status: BLOCKED_SERVER_SIDE_YOUTUBE_INGRESS / ARCHITECTURE_DECISION_REQUIRED

#### A4.1 server-side acceptance history

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Verified:
- bearer auth PASS;
- invalid tester code rejection PASS;
- owner tester code PASS;
- job creation PASS.

Three live fetch attempts failed before transcript acquisition with YouTube `Sign in to confirm you're not a bot` and each charged 0 AssemblyAI STT seconds.

R1:
- `web_embedded,android_vr` clients;
- CI/deploy PASS;
- live retest FAIL with same anti-bot challenge.

R2:
- `mweb`;
- `bgutil-ytdlp-pot-provider` 1.3.1;
- local provider in the same beta container;
- `yt-dlp[default]==2026.07.04`;
- Node.js 24 EJS runtime;
- no YouTube cookies;
- no additional paid/free Render service;
- CI PASS;
- Render deploy LIVE;
- live retest FAIL with same anti-bot challenge.

One-shot diagnostic run `32060462596` / job `95480351954` confirmed:
- provider `/ping` works;
- yt-dlp detects `PO Token Providers: bgutil:http-1.3.1 (external)`;
- Node EJS runtime works;
- YouTube still returns the same bot challenge.

Decision: stop repeated server-side cloud-IP retries. The blocker is not missing PO-provider integration.

#### A4.2 recommended client-assisted ingress

Status: PENDING_USER_APPROVAL

Recommended closed-beta architecture:
```text
YouTube URL
 -> beta job/session
 -> browser helper / VoiceBridge extension
 -> captions or tab audio acquired through tester residential IP
 -> upload derived captions/audio to beta backend
 -> AssemblyAI only if captions unavailable
 -> timestamped transcript
 -> KRC claim inventory / CriticProfile workflow
```

Implementation targets after approval:
- reuse existing VoiceBridge browser-extension transport where practical;
- one-time media job/session binding;
- beta access-code enforcement remains server-side;
- captions preferred over tab-audio STT;
- do not upload full video unless technically unavoidable;
- no personal YouTube cookies stored in cloud;
- no permanent local file storage;
- preserve 60 min, concurrency 1 and daily STT limits;
- test with same A4.1 URL first.

Exit target:
- same acceptance URL reaches `COMPLETED` through client-assisted ingress;
- captions path, if available, consumes 0 STT seconds;
- otherwise audio fallback consumes expected quota;
- timestamps usable.

#### Other ingress alternatives

Paid residential proxy:
- preserves URL-only server UX;
- introduces recurring cost and new privacy/provider dependency;
- conflicts with primary free-tier objective.

Personal YouTube cookies in Render:
- not recommended as default;
- account/session/privacy risk;
- fragile against IP/session enforcement;
- requires explicit user decision if ever tested.

#### Remaining A4 matrix after ingress succeeds

- Ukrainian captions case;
- Russian captions case;
- English captions case;
- STT fallback case;
- automatic language detection;
- >60 min rejection;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification.

Exit criteria:
- captions path works without STT charge;
- fallback path works with expected quota charge;
- timestamps and language metadata are usable;
- `provider_data_deleted=true` observed where applicable;
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

### B3. Local Media Node / residential ingress proof of concept
Evaluate browser-assisted and local-node acquisition, faster-whisper/whisper.cpp, CPU-only operation, optional GPU acceleration, secure transport, availability and operational burden.

### B4. Remove permanent AssemblyAI dependency from public free path
AssemblyAI may remain as development comparator, emergency fallback, or optional paid reliability path. It must not be required for intended sustainable free public mode.

## Phase C - Public media release

Status: FUTURE

Public release requires sustainable resource validation, privacy validation, Free-plan ChatGPT test, Actions runtime compatibility, production smoke tests, and explicit user approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation evidence exists. BLOCKED/PENDING/PLANNED must never be described as already validated.
