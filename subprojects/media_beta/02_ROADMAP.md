# MEDIA BETA Roadmap
Дорожня карта реалізації закритого beta-медіарежиму та наступного сталого безкоштовного режиму.

Version: 2.3
Status: ACTIVE
Updated: 2026-08-20

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

Status: IN_PROGRESS_TEXT_QUALITY

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
- Ukrainian auto-generated captions with 227/227 Action-facing segments;
- Russian auto-generated captions with 524 segments / 19206 characters;
- English manual captions with 247 segments / 8872 characters;
- manual-caption classification;
- `language_hint=auto` selecting Italian `detected_language=it`;
- zero STT charge for caption cases;
- AssemblyAI `universal-2` audio fallback;
- measured audio duration accounting;
- provider deletion request;
- Action-facing audio segment readback;
- large-caption-payload persistence remediation;
- browser/helper stale-state fix.

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

Status: COMPLETE

Accepted:
- durable Postgres KRCC job state;
- waiting job survives isolated beta process replacement;
- same Job ID resumes after restart;
- completed job remains readable after later restart;
- external `created_at` remains immutable through restart, rehydration and completion;
- durable STT quota ledger enabled;
- live restart restoration of a newly charged 57-second AssemblyAI job;
- fresh post-restart job showed runtime quota `used_seconds=57`, `remaining_seconds=7143`;
- forced active-audio process loss during `TRANSCRIBING` produces deterministic terminal `FAILED`;
- failure code is `MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED` with `retryable=true`;
- same durable Job ID remains readable after resume;
- measured 250-second STT reservation was not duplicated after process replacement.

Accepted active-audio job:
`KRCC_8da975c7-e338-4d02-8783-3b30d7071dce`

Canonical records:
- `subprojects/media_beta/12_A4_4_DURABILITY_ACCEPTANCE.md`;
- `subprojects/media_beta/15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md`;
- `subprojects/media_beta/16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md`.

Residual release-hardening note:
- after a hard process death, `provider_data_deleted` can remain null because the killed runtime cannot record provider cleanup; orphan-provider cleanup is tracked separately and does not reopen the retry-safety acceptance.

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
- Russian auto-generated captions;
- English manual captions;
- manual-caption classification;
- `auto -> it` language/track selection;
- large Russian caption payload persisted durably after remediation;
- zero STT charge for caption cases;
- immutable external `created_at` preserved.

Canonical acceptance:
`subprojects/media_beta/14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`

#### Remaining A4 work

Pending before A4 exit:
- STT replacement-character (`U+FFFD`) investigation and disposition.

Already accepted and no longer pending:
- Ukrainian, Russian, English and Italian/AUTO caption cases;
- manual-caption classification;
- captions unavailable/audio fallback path;
- successful audio fallback after duration fix;
- >60 min rejection;
- source mismatch rejection;
- concurrency rejection;
- daily STT quota exhaustion simulation;
- provider cleanup verification for normal AssemblyAI completion;
- waiting/completed restart durability and `created_at` continuity;
- durable quota-ledger restart restoration after a real STT charge;
- large-caption-payload durable persistence boundary;
- active-audio forced process-loss retry-safe behavior.

A4 exit criteria:
- captions-first real browser jobs are usable across required language/source cases;
- audio fallback remains usable when captions are unavailable;
- language/source metadata is usable;
- quota accounting matches selected path and survives required restart checks;
- active-audio process replacement has deterministic retry-safe behavior;
- provider cleanup is verified where normal AssemblyAI completion occurs;
- STT replacement-character anomaly is investigated and dispositioned;
- no beta/developer secret appears in reports/checkpoints/loggable payloads.

### A5. Separate GPT Builder beta

Status: BLOCKED_BY_REMAINING_A4_TEXT_QUALITY

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
