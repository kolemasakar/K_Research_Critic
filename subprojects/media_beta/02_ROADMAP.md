# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 2.1
Status: ACTIVE
Updated: 2026-08-18

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

Status: COMPLETE_IN_CODE_AND_PRIMARY_LIVE_GUARDS

Current beta limits:
- max source/capture duration = 60 min;
- concurrency = 1;
- global AssemblyAI fallback budget = 7200 sec / UTC day;
- captions path charges 0 STT seconds;
- audio helper upload guard = 32 MiB;
- STT normalization = mono 16 kHz approximately 32 kbps;
- temporary media cleanup;
- provider delete request for AssemblyAI fallback;
- per-tester access codes;
- durable Postgres job state and STT quota ledger.

Live negative-path guards accepted:
- invalid beta code;
- wrong YouTube source;
- >60 minute content;
- concurrency >1;
- daily STT quota exhaustion before provider submission.

### A3. Dedicated Render beta deployment

Status: COMPLETE

Dedicated service:
- `voicebridge-krc-media-beta-kolemasakar`;
- ID `srv-da1kic5bedkc73d6fk60`;
- plan `free`;
- production VoiceBridge isolated.

### A4. Live transcript validation

Status: IN_PROGRESS_DURABILITY_AND_AUDIO_EDGE_CASES

#### A4.1 Server-side YouTube ingress

Status: CLOSED_AS_UNSUITABLE_FOR_CURRENT_BETA

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Server-side attempts from Render failed before transcript acquisition with YouTube `Sign in to confirm you're not a bot`, including PO-provider/runtime configurations. Repeated cloud/datacenter-IP retries are not an approved beta path.

Approved ingress is browser-assisted.

#### A4.2 Client/browser-assisted ingress

Status: PRIMARY_OWNER_ACCEPTANCE_PASS

Approved flow:
```text
YouTube URL
 -> beta Action creates durable KRCC_ job
 -> AWAITING_CLIENT
 -> Helper 0.2.2 on same YouTube tab
 -> Use subtitles first
    -> direct timed-text if usable
    -> transcript-panel fallback otherwise
    -> /captions browser-only upload
    -> COMPLETED / youtube_captions / STT=0
 -> if captions unavailable/unusable
    -> Audio fallback
    -> tabCapture + backend normalization
    -> duration/quota checks
    -> AssemblyAI async STT
 -> timestamped transcript
 -> GPT Action status/segments
 -> KRC claim inventory / CriticProfile workflow
```

Accepted live evidence:
- Ukrainian auto-generated captions job completed with 227 timestamped segments;
- full Action pagination 227/227 passed;
- Russian auto-generated captions job completed through transcript-panel fallback with 524 segments / 19206 transcript characters;
- English manual captions job completed with 247 segments / 8872 transcript characters;
- manual-caption classification accepted on the English case;
- `language_hint=auto` accepted an Italian manual-caption track and persisted `detected_language=it`;
- captions charged zero STT seconds in all accepted caption cases;
- audio fallback completed with AssemblyAI `universal-2`;
- measured audio duration charged correctly;
- provider deletion request succeeded;
- Action-facing audio segments were readable;
- browser/helper stale-state issue fixed in Helper 0.2.2;
- large caption payload persistence boundary fixed and live revalidated.

#### A4.3 Audio fallback acceptance

Status: COMPLETE_FOR_PRIMARY_UKRAINIAN_SAMPLE

Accepted:
- browser capture/upload;
- WebM/Opus normalization;
- duration probing;
- measured quota charging;
- AssemblyAI async transcription;
- provider delete request;
- Action-facing status and segments.

Open quality item:
- `U+FFFD` replacement-character artifacts observed in returned STT text.

#### A4.4 Restart durability

Status: COMPLETE_FOR_JOB_STATE_AND_CREATED_AT

Accepted:
- durable Postgres KRCC job state;
- waiting job survives isolated beta process replacement;
- same Job ID resumes after restart;
- completed job remains readable after later restart;
- durable STT quota ledger enabled;
- external `created_at` remains immutable through restart, rehydration and completion.

Still pending:
- live restart acceptance of the quota ledger after a newly charged audio job;
- process-replacement behavior during active audio upload/transcription.

Canonical acceptance:
`subprojects/media_beta/12_A4_4_DURABILITY_ACCEPTANCE.md`

#### A4.5 Guard matrix

Status: COMPLETE

Accepted live contracts:
- invalid beta code -> HTTP 403 / `MEDIA_BETA_ACCESS_DENIED`;
- source mismatch -> HTTP 409 / `MEDIA_CLIENT_SOURCE_MISMATCH`;
- concurrency -> HTTP 429 / `MEDIA_TRANSCRIPT_BUSY`;
- >60 min -> HTTP 413 / `MEDIA_DURATION_LIMIT`;
- quota exhaustion -> `MEDIA_DAILY_STT_QUOTA_EXHAUSTED`, zero STT charge before provider use.

The temporary 60-second quota used for the exhaustion test was restored to 7200 sec/day after acceptance. Production was not targeted.

Canonical acceptance:
`subprojects/media_beta/13_A4_5_GUARD_MATRIX_ACCEPTANCE.md`

#### A4.6 Language/source matrix

Status: COMPLETE

Accepted:
- Ukrainian auto-generated captions;
- Russian auto-generated captions via YouTube transcript-panel fallback;
- English manual captions;
- manual-caption classification;
- explicit `language_hint=auto` case selecting/persisting Italian `detected_language=it`;
- 524-segment / 19206-character large Russian payload persisted durably after remediation;
- zero STT charge for caption cases;
- immutable external `created_at` preserved.

Canonical acceptance:
`subprojects/media_beta/14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`

#### Remaining A4 matrix

Pending before A4 exit:
- durable quota-ledger restart acceptance after a newly charged audio job;
- audio fallback behavior if process replacement occurs during active upload/transcription;
- STT replacement-character investigation.

Already accepted and no longer pending:
- Ukrainian auto-generated captions;
- Russian auto-generated captions;
- English manual captions;
- manual-caption classification;
- `auto -> it` language/track selection;
- captions unavailable/audio fallback path;
- successful audio fallback after duration fix;
- >60 min rejection;
- source mismatch rejection;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification;
- restart durability and `created_at` continuity;
- large-caption-payload durable persistence boundary.

A4 exit criteria:
- captions-first real browser jobs are usable across required language/source cases;
- audio fallback remains usable when captions are unavailable;
- language/source metadata is usable;
- quota accounting matches selected path and survives required restart checks;
- provider cleanup is verified where AssemblyAI is used;
- no beta/developer secret appears in reports/checkpoints/loggable payloads.

### A5. Separate GPT Builder beta

Status: BLOCKED_BY_REMAINING_A4_EDGE_CASES

After A4 acceptance:
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

Owner tests first; then up to three additional tester codes. Monitor reliability, Render bandwidth, caption success rate, AssemblyAI fallback credits and Postgres lifecycle. Limit changes require explicit decision update.

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
