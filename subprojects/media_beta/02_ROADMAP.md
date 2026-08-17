# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 1.7
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
- max source/capture duration = 60 min;
- concurrency = 1;
- global AssemblyAI fallback budget = 7200 sec / UTC day;
- captions path charges 0 STT seconds;
- audio helper upload guard = 32 MiB;
- STT normalization = mono 16 kHz approximately 32 kbps;
- temporary media cleanup;
- provider delete request for AssemblyAI fallback;
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

Status: IN_PROGRESS_CAPTIONS_FIRST_OWNER_ACCEPTANCE

#### A4.1 Server-side YouTube ingress

Status: CLOSED_AS_UNSUITABLE_FOR_CURRENT_BETA

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Three server-side attempts failed before transcript acquisition with YouTube `Sign in to confirm you're not a bot` and charged 0 AssemblyAI seconds:
- original yt-dlp;
- `web_embedded,android_vr`;
- `mweb` + `bgutil-ytdlp-pot-provider` 1.3.1.

Diagnostic run `32060462596` / job `95480351954` proved the PO-provider/runtime wiring was functional. Repeated cloud/datacenter-IP retries are not an approved next step.

#### A4.2 Client/browser-assisted ingress

Status: CAPTIONS_FIRST_IMPLEMENTED / CI_PASS / DEPLOYED / HELPER_0_2_LIVE_ACCEPTANCE_NEXT

Approved flow:
```text
YouTube URL
 -> beta Action creates KRCC_ job
 -> AWAITING_CLIENT
 -> Helper 0.2.0 on same YouTube tab
 -> Use subtitles first
    -> browser caption track + timestamps
    -> /captions browser-only upload
    -> validation
    -> COMPLETED / youtube_captions / STT=0
 -> if captions unavailable/unusable
    -> Audio fallback
    -> tabCapture + backend normalization
    -> AssemblyAI async STT
 -> timestamped transcript
 -> KRC claim inventory / CriticProfile workflow
```

Implemented captions-first controls:
- browser `activeTab` + `scripting` extraction initiated only by the tester;
- active/requested/source caption-track selection;
- manual vs auto-generated caption metadata;
- browser fetch of timestamped YouTube timed-text;
- same-video validation;
- per-tester job ownership digest;
- caption timestamp/text bounds;
- `transcript_source=youtube_captions`;
- `caption_type=manual|auto_generated`;
- `provider=youtube`;
- `stt_seconds_charged=0` and no STT quota reservation;
- timestamped segment paging through the existing Action route.

Audio fallback remains implemented:
- tabCapture/offscreen recording;
- 32 MiB upload guard;
- WebM/Opus normalization before duration probing;
- 60-minute duration check;
- STT quota reservation only after valid duration;
- auto/uk/ru/en AssemblyAI async transcription;
- provider transcript delete request.

Validation/deployment evidence:
- VoiceBridge captions-first CI run `32069122559`: SUCCESS;
- current VoiceBridge commit `92f809440098fd42eb562a36c6feddeaa9c17155`;
- Helper `0.2.0` CI artifact produced;
- isolated Render deploy run `32069270467`: SUCCESS;
- deploy ID `dep-da1nf76gekts738dst5g`;
- exact captions-first commit reached `live`;
- health HTTP 200;
- `media_client_ingest.mode=client_assisted`;
- `configured=true`;
- `requires_browser_helper=true`.

Previous browser/audio evidence retained:
- job `KRCC_aa3b2cbc-4d4e-4f89-b6e6-4549766f34f5` proved helper installation, active-tab capture and backend upload;
- its `MEDIA_DURATION_UNKNOWN` failure exposed a MediaRecorder WebM metadata issue;
- duration handling was fixed before captions-first work and the fix remains in the current commit.

Next acceptance sequence:
1. install/reload Helper 0.2.0;
2. create a NEW `KRCC_...` job for the acceptance URL;
3. require `AWAITING_CLIENT`, `client_upload_required=true`, `stt_seconds_charged=0`;
4. click `Use subtitles` first;
5. require `COMPLETED`, `transcript_source=youtube_captions`, caption type, non-empty timestamped segments and `stt_seconds_charged=0`;
6. verify the STT quota did not decrease;
7. only if captions are unavailable, validate `Audio fallback` and AssemblyAI cleanup;
8. then expand to UK/RU/EN/auto and guard-condition matrix.

Remaining A4 matrix:
- owner real Helper 0.2.0 captions-first acceptance;
- Ukrainian captions case;
- Russian captions case;
- English captions case;
- auto language/track selection;
- manual-caption classification;
- auto-generated-caption classification;
- caption-unavailable -> audio fallback;
- successful audio fallback after duration fix;
- >60 min rejection;
- source mismatch rejection;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification for AssemblyAI fallback.

Exit criteria:
- captions-first real browser job reaches `COMPLETED` with usable timestamps and zero STT charge;
- audio fallback can reach `COMPLETED` when captions are unavailable;
- language/source metadata is usable;
- quota accounting matches the selected path;
- provider cleanup is verified where AssemblyAI is used;
- no beta/developer secret appears in reports/checkpoints/loggable payloads.

### A5. Separate GPT Builder beta

Status: BLOCKED_BY_A4_LIVE_BROWSER_ACCEPTANCE

After A4 owner browser acceptance:
- create `K-Research & Critic - MEDIA BETA` separately from public GPT;
- import beta instructions and captions-first client-assisted OpenAPI schema;
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
 -> KRCC captions-first/browser-assisted transcript
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

Owner tests first; then up to three additional tester codes. Monitor reliability, Render bandwidth, caption success rate, and AssemblyAI fallback credits. Limit changes require explicit decision update.

## Phase B - Sustainable Free Media

Status: PLANNED_AFTER_BETA

### B1. Caption path hardening
Evaluate robustness across YouTube UI/player variants, manual/ASR tracks, language selection and failure modes. Preserve audio fallback when player internals change.

### B2. Cloudflare Whisper proof of concept
Compare against AssemblyAI for Ukrainian, Russian, English, timestamps, names/numbers/acronyms, latency, and effective free daily capacity.

### B3. Provider-neutral transcript router

```text
captions/direct transcript
 -> free cloud Whisper quota
 -> optional local Whisper fallback
```

### B4. Local Media Node / residential ingress proof of concept
Evaluate browser-assisted/local-node acquisition, faster-whisper/whisper.cpp, CPU/GPU options, secure transport, availability, and operational burden.

### B5. Remove permanent AssemblyAI dependency from public free path
AssemblyAI may remain as comparator/emergency fallback but must not be mandatory for intended sustainable public free mode.

## Phase C - Public media release

Status: FUTURE

Requires sustainable resources, privacy validation, provider no-training gate for any fallback provider, Free-plan ChatGPT test, Actions compatibility, production smoke tests, and explicit user approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation evidence exists. IN_PROGRESS/BLOCKED/PLANNED must never be described as already validated.
