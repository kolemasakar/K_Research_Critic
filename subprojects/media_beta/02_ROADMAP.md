# MEDIA BETA Roadmap

Roadmap for the closed MEDIA BETA and the later sustainable free-media architecture.

Version: 2.8
Status: ACTIVE
Updated: 2026-08-20

## Phase A - Closed MEDIA BETA

### A1. Architecture and isolation

Status: COMPLETE

Delivered:
- separate MEDIA BETA GPT identity;
- separate GPT Action contract;
- separate VoiceBridge media backend path;
- per-tester access-code model;
- dedicated Render beta target;
- production VoiceBridge unchanged;
- published K-Research & Critic unchanged.

### A2. Resource protection

Status: COMPLETE_IN_CODE_AND_PRIMARY_LIVE_GUARDS

Current beta limits:
- max source/capture duration 60 min;
- concurrency 1;
- global AssemblyAI fallback budget 7200 sec per UTC day;
- captions path STT charge 0;
- helper audio upload guard 32 MiB;
- mono 16 kHz speech normalization at about 32 kbps;
- temporary audio cleanup;
- provider delete request on normal AssemblyAI completion;
- per-tester access codes;
- durable Postgres job state and STT quota ledger.

Accepted negative-path guards:
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
- isolated from production VoiceBridge.

### A4. Live transcript validation

Status: COMPLETE

Accepted:
- captions-first browser-assisted ingestion;
- UK auto captions 227/227;
- RU auto captions 524;
- EN manual captions 247;
- AUTO language/track selection with IT case;
- zero STT charge for captions;
- Audio fallback through AssemblyAI Universal-2;
- measured duration/quota accounting;
- normal provider cleanup;
- Action status and segment readback;
- large-caption durable persistence remediation;
- guard matrix;
- durable restart/resume behavior;
- immutable `created_at`;
- durable quota-ledger restart restoration;
- forced active-audio process loss -> deterministic retry-safe `FAILED` with `MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED`;
- no duplicate STT charge after process replacement;
- U+FFFD text-quality anomaly investigated and dispositioned as non-reproducible / non-blocking.

Canonical acceptance records:
- `10_A4_2_CAPTIONS_ACCEPTANCE.md`;
- `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md`;
- `12_A4_4_DURABILITY_ACCEPTANCE.md`;
- `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md`;
- `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`;
- `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md`;
- `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md`;
- `17_A4_STT_TEXT_QUALITY_DISPOSITION.md`.

### A5. Separate GPT Builder beta

Status: COMPLETE

Accepted:
- separate `K-Research & Critic - MEDIA BETA` Builder identity;
- Builder-safe instructions under the current 8000-character limit;
- web search enabled;
- image generation disabled;
- code interpreter/data analysis enabled;
- API Key/Bearer Action authentication;
- `gpt_store/actions/media_beta_openapi.yaml` imported;
- Action server restricted to isolated beta Render endpoint;
- privacy policy URL configured;
- Builder recognized the three intended operations;
- missing tester code correctly triggers `MEDIA BETA ACCESS REQUIRED` before Action start;
- Builder-created KRCC job interoperates with Helper 0.2.2;
- captions-first completion returns 227 segments and STT=0;
- GPT returns DRAFT CriticProfile and stops at the approval gate before independent research.

Accepted Builder job:
`KRCC_8945357e-d6cf-4483-b7ca-178b81729665`

Credential attribution:
- the owner/operator performed this live acceptance using the code designated for `Tester 1`;
- the owner-designated code was not the credential used.

Canonical acceptance:
`subprojects/media_beta/18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md`

Canonical credential correction:
`subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`

### A6. End-to-end beta acceptance

Status: COMPLETE_FOR_FIRST_OWNER_OPERATED_CAPTIONS_FIRST_FLOW

Accepted owner-operated flow:

```text
YouTube URL
 -> beta access using Tester 1 credential
 -> Builder Action creates KRCC job
 -> Helper captions-first completion
 -> GPT status/segments
 -> claim inventory
 -> DRAFT CriticProfile
 -> user APPROVE
 -> independent web research
 -> Critic/revision path
 -> finalization
```

The owner/operator entered standalone `1`; profile transitioned to APPROVED; the workflow continued through transcript retrieval, independent research, Critic/revision/finalization, and the owner/operator confirmed successful completion.

This validates the workflow with a valid allowlisted Tester 1 credential but does not count as an independent external Tester 1 human run.

Canonical acceptance:
`subprojects/media_beta/18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md`

### A7. Controlled tester rollout

Status: READY_FOR_TESTER1

Accepted rollout gates:
- captions-first path READY;
- separate tester-code model READY;
- Helper 0.2.2 onboarding procedure READY;
- failure-report template READY;
- AssemblyAI client-assisted Audio fallback routed through `https://api.eu.assemblyai.com` in isolated beta;
- EU Audio fallback live acceptance PASS;
- normal provider deletion confirmed on EU live job;
- exact measured STT quota accounting confirmed;
- production VoiceBridge unchanged.

Credential status:
- Tester 1 credential has already been live-used extensively by the owner/operator;
- owner-designated credential has not yet been separately live-validated;
- no independent external Tester 1 human run has occurred yet.

Accepted EU Audio fallback job:
`KRCC_a79ad701-d5a0-40ca-91f8-6fbdfc6c3bc6`

The EU live job was also performed by the owner/operator using the Tester 1 credential.

Accepted result:

```text
status=COMPLETED
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
duration_seconds=122.292
stt_seconds_charged=123
segment_count=3
error=null
```

Canonical A7 records:
- `subprojects/media_beta/19_A7_CONTROLLED_TESTER_ROLLOUT.md`;
- `subprojects/media_beta/20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md`;
- `subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`.

Next:
- invite the actual external Tester 1 using the already designated Tester 1 code;
- require at least one independent captions-first end-to-end flow without owner intervention beyond onboarding;
- require one additional tester-selected YouTube video;
- observe CriticProfile approval behavior and failure-report usability;
- use Audio fallback only when captions are unavailable/unusable;
- monitor captions-vs-STT ratio, STT seconds, Render health/bandwidth, cleanup state, failures, and Postgres lifecycle;
- expand to Tester 2/3 only after acceptable Tester 1 reliability/resource observations;
- keep public GPT and production VoiceBridge unchanged.

A7 remains incomplete until external tester evidence exists.

## Phase B - Sustainable Free Media

Status: PLANNED_AFTER_BETA

### B1. Caption path hardening
Evaluate robustness across YouTube UI/player variants, manual/ASR tracks, language selection and failure modes. Preserve audio fallback when caption internals change.

### B2. Cloudflare Whisper proof of concept
Compare against AssemblyAI for Ukrainian, Russian, English, timestamps, names/numbers/acronyms, latency, and effective renewable/free capacity.

### B3. Provider-neutral transcript router

```text
captions/direct transcript
 -> free cloud Whisper quota
 -> optional local Whisper fallback
```

### B4. Local Media Node / residential ingress proof of concept
Evaluate browser-assisted/local-node acquisition, faster-whisper/whisper.cpp, CPU/GPU options, secure transport, availability, and operational burden.

### B5. Remove permanent AssemblyAI dependency from public free path
AssemblyAI may remain as comparator/emergency fallback but must not be mandatory for the intended sustainable public free mode.

## Phase C - Public media release

Status: FUTURE

Requires:
- sustainable resource architecture;
- privacy/no-training re-validation;
- provider cleanup strategy;
- Free-plan/paid runtime compatibility;
- stable privacy policy URL;
- Actions compatibility;
- production smoke tests;
- explicit user approval.

## Roadmap rule

A roadmap item marked COMPLETE means implementation/acceptance evidence exists. READY/IN_PROGRESS/BLOCKED/PLANNED must never be described as already validated.
