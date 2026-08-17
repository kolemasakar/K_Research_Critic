# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 1.6
Status: ACTIVE
Updated: 2026-08-17

## Phase A - Closed MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Delivered:
- separate K-Research & Critic beta identity;
- separate GPT Action contract;
- separate VoiceBridge media backend path;
- per-tester access-code model;
- dedicated Render beta target;
- production VoiceBridge unchanged;
- published K-Research & Critic unchanged.

### A2. Resource protection

Status: COMPLETE_IN_CODE

Current beta limits:
- max captured duration = 60 min;
- concurrency = 1;
- global AssemblyAI budget = 7200 sec / UTC day;
- helper upload guard = 32 MiB;
- STT normalization = mono 16 kHz approximately 32 kbps;
- temporary media cleanup;
- provider delete request;
- transcript/job TTL;
- access codes excluded from reports/checkpoints.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- plan `free`;
- production VoiceBridge isolated.

### A4. Live transcript validation

Status: IN_PROGRESS_CLIENT_ASSISTED_OWNER_RETEST

#### A4.1 Server-side YouTube ingress

Status: CLOSED_AS_UNSUITABLE_FOR_CURRENT_BETA

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition with YouTube `Sign in to confirm you're not a bot` and charged 0 AssemblyAI seconds:
- original yt-dlp;
- `web_embedded,android_vr`;
- `mweb` + `bgutil-ytdlp-pot-provider` 1.3.1.

Diagnostic run `32060462596` / job `95480351954` proved the PO-provider/runtime wiring was functional. Therefore repeated cloud/datacenter-IP retries are not an approved next step.

#### A4.2 Client/browser-assisted ingress

Status: IMPLEMENTED / CI_PASS / DEPLOYED / FIRST_BROWSER_CAPTURE_REACHED_BACKEND / DURATION_FIX_LIVE / RETEST_NEXT

Approved flow:
```text
YouTube URL
 -> beta Action creates KRCC_ job
 -> AWAITING_CLIENT
 -> separate KRC MEDIA BETA browser helper
 -> same active YouTube tab captured through tester browser/network path
 -> compressed audio uploaded to isolated beta backend
 -> bounded ffmpeg normalization
 -> reliable normalized-audio duration/source/quota validation
 -> AssemblyAI async STT
 -> timestamped transcript
 -> KRC claim inventory / CriticProfile workflow
```

Direct reliable transcript/caption intake remains preferred when already available through current built-in/web capabilities. Client-side caption extraction by the helper is not yet implemented and remains a planned optimization.

Implemented:
- `KRCC_` client jobs;
- `AWAITING_CLIENT` state;
- same-video validation;
- per-tester temporary job ownership digest;
- 32 MiB upload guard;
- bounded browser-audio normalization before duration probing;
- 60-minute captured-duration check;
- STT quota reservation only after valid duration is known;
- auto/uk/ru/en AssemblyAI async path;
- timestamped segments;
- provider delete request;
- separate Chrome/Edge MV3 helper;
- existing VoiceBridge translation extension unchanged.

Initial validation evidence:
- VoiceBridge CI run `32062552003`: SUCCESS;
- initial implementation commit `923389b3fdd89eef4a57b308b8fe2a98d41ce8e5`;
- explicit isolated Render deploy run `32063396120`: SUCCESS;
- deploy ID `dep-da1mgebutv3s73fd2grg`;
- KRC package CI run `32063557028`: SUCCESS.

First live browser acceptance evidence:
- job `KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5` created successfully;
- pre-upload state `AWAITING_CLIENT`, `client_upload_required=true`, `stt_seconds_charged=0`;
- helper 0.1.0 installed in Edge;
- helper reached `CAPTURING` on the correct YouTube tab;
- browser audio upload reached backend processing;
- first Stop ended with `MEDIA_DURATION_UNKNOWN` before AssemblyAI.

Root cause and fix:
- MediaRecorder streaming WebM/Opus may omit container-level duration metadata;
- raw WebM was originally probed before normalization;
- backend now normalizes first to MP3 with a hard processing cap, then probes duration on normalized audio;
- quota is reserved only after duration validation succeeds;
- helper 0.1.0 does not require reinstall.

Duration-fix validation/deployment:
- VoiceBridge CI run `32067365619`: SUCCESS;
- current commit `772901a167611f0197d1bc05cea8091da211dc47`;
- explicit isolated Render deploy run `32067505039`: SUCCESS;
- deploy ID `dep-da1n5rou01pc73b5v73g`;
- exact duration-fix commit reached `live`;
- beta health HTTP 200;
- service `status=ok`;
- `media_client_ingest.mode=client_assisted`;
- `media_client_ingest.configured=true`;
- `requires_browser_helper=true`.

Next acceptance sequence:
1. create a NEW `KRCC_...` job for the A4.1 URL because the previous job is terminal FAILED;
2. require `AWAITING_CLIENT`, `client_upload_required=true`, `stt_seconds_charged=0` before upload;
3. reuse already installed helper 0.1.0 in owner Edge/Chrome;
4. record approximately 60-90 seconds at normal speed;
5. require upload acceptance, `TRANSCRIBING`, then `COMPLETED`;
6. require non-empty timestamped segments, sensible detected language/STT charge, and provider cleanup evidence;
7. then expand to UK/RU/EN/auto and guard-condition matrix.

Remaining A4 matrix:
- successful owner real browser STT acceptance;
- Ukrainian case;
- Russian case;
- English case;
- automatic language detection;
- >60 min rejection;
- source mismatch rejection;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification;
- client-side caption optimization evaluation.

Exit criteria:
- real browser-assisted transcription reaches `COMPLETED`;
- timestamps are usable;
- language metadata is usable;
- quota charge is consistent with captured duration;
- `provider_data_deleted=true` is observed on successful AssemblyAI cleanup;
- no beta/developer secret appears in reports/checkpoints/loggable payloads.

### A5. Separate GPT Builder beta

Status: BLOCKED_BY_A4_LIVE_BROWSER_ACCEPTANCE

After A4 owner browser acceptance:
- create `K-Research & Critic - MEDIA BETA` separately from public GPT;
- import beta instructions and client-assisted OpenAPI schema;
- configure Action bearer secret;
- point to dedicated beta Render endpoint;
- configure privacy policy URL;
- keep public GPT unchanged.

### A6. End-to-end beta acceptance

Status: BLOCKED_BY_A5

Target:
```text
YouTube URL
 -> beta access
 -> KRCC browser-assisted transcript
 -> claim inventory
 -> CriticProfile
 -> user approval
 -> web research
 -> Critic
 -> FINAL REPORT
 -> CLAIM VERIFICATION
 -> REVIEW PROTOCOL
```

### A7. Controlled tester rollout

Status: BLOCKED_BY_A6

Owner tests first; then up to three additional tester codes. Monitor reliability, Render bandwidth, and AssemblyAI credits. Limit changes require explicit decision update.

## Phase B - Sustainable Free Media

Status: PLANNED_AFTER_BETA

### B1. Cloudflare Whisper proof of concept
Compare against AssemblyAI for Ukrainian, Russian, English, timestamps, names/numbers/acronyms, latency, and effective free daily capacity.

### B2. Provider-neutral transcript router

```text
captions/direct transcript
 -> free cloud Whisper quota
 -> optional local Whisper fallback
```

### B3. Local Media Node / residential ingress proof of concept
Evaluate browser-assisted/local-node acquisition, faster-whisper/whisper.cpp, CPU/GPU options, secure transport, availability, and operational burden.

### B4. Remove permanent AssemblyAI dependency from public free path
AssemblyAI may remain as comparator/emergency fallback but must not be mandatory for intended sustainable public free mode.

## Phase C - Public media release

Status: FUTURE

Requires sustainable resources, privacy validation, provider no-training gate, Free-plan ChatGPT test, Actions compatibility, production smoke tests, and explicit user approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation evidence exists. IN_PROGRESS/BLOCKED/PLANNED must never be described as already validated.
