# KRC Media - Gemini 3.5 Transcribe Transition Instructions

Status: PENDING - DO NOT EXECUTE
Created: 2026-08-29
Activation: EXPLICIT USER ACTIVATION REQUIRED

## Activation gate

These instructions MUST NOT be executed until BOTH conditions are true:

1. The VoiceBridge real-time migration / A-B validation of Gemini 3.5 Transcribe has completed successfully and has been accepted by the user.
2. The user explicitly activates these instructions in the KRC Media project.

Until then this file is planning-only. Do not change KRC Media code, provider configuration, secrets, runtime environment, databases, or production infrastructure because of this plan.

## Purpose

Prepare KRC Media to support Gemini 3.5 Transcribe for prerecorded media without removing the existing AssemblyAI path and without coupling KRC Media provider selection to VoiceBridge provider selection.

The migration objective is quality, multilingual coverage, provider portability, and free-tier sustainability while preserving evidence integrity, job durability, API compatibility, and rollback.

## Known starting-point snapshot

This snapshot is informational only and MUST be re-verified at activation time.

At the time this plan was written, KRC Media implementation was observed in:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
```

Observed prerecorded STT path:

```text
media URL
 -> media retrieval / local audio file
 -> AssemblyAI upload
 -> AssemblyAI async transcription + polling
 -> transcript + words/timestamps/confidence
 -> normalized KRC Media segments
 -> downstream KRC workflow
```

Observed implementation characteristics:

```text
AssemblyAI async model: universal-2
provider value: assemblyai
ASSEMBLYAI_API_KEY: configured through environment
GEMINI_API_KEY: already present for other system capabilities
```

Do not assume these paths, models, branches, contracts, or limits remain current when this plan is activated.

## Mandatory activation preflight

Before the first code change:

1. RECOVER the current KRC Media state from its canonical repository / branch / deployment.
2. Identify the exact current STT implementation, provider contract, job state model, persistence model, API response schema, quota accounting, cleanup behavior, and tests.
3. Verify current official Google documentation for:
   - Gemini 3.5 Transcribe model identifiers;
   - prerecorded input limits;
   - file-size and duration limits;
   - limits when word timestamps and diarization are enabled;
   - supported languages;
   - custom vocabulary behavior and limits;
   - Free Tier availability and quotas;
   - data-use / retention terms for Free Tier;
   - uploaded-file retention / deletion behavior;
   - rate limits and retry guidance.
4. Verify current AssemblyAI behavior used by the baseline so the comparison is like-for-like.
5. Report the exact current state, affected files, tests, risks, and first implementation checkpoint.
6. STOP before the first production infrastructure or environment change until the user explicitly approves that phase.

Never substitute old screenshots, this planning snapshot, or remembered provider limits for activation-time verification.

## Target architecture

Provider selection for KRC Media MUST be independent from VoiceBridge live STT.

Target abstraction:

```text
KRC Media prerecorded STT
  -> MediaTranscriptionProvider
       -> AssemblyAIAsyncTranscriber
       -> GeminiTranscribeProvider
```

Suggested independent configuration contract:

```text
KRC_MEDIA_STT_PROVIDER=assemblyai|gemini
KRC_MEDIA_TRANSCRIBE_MODEL=<explicit-approved-model>
```

The exact names may be adapted to the recovered codebase, but the separation invariant is mandatory:

```text
VoiceBridge STT provider change != automatic KRC Media STT provider change
```

## Normalized provider result contract

Both provider adapters should normalize into one stable internal result shape containing, where actually available:

```text
provider
provider_model
text
segments
word timestamps or normalized timestamps
segment start/end timestamps
detected_language
language_confidence
confidence
speaker identity / diarization metadata
provider request/job identifier when operationally needed
provider data deletion / cleanup state
processing latency
retry / error classification
```

Rules:

- Never invent confidence, language confidence, timestamps, diarization, or other fields a provider did not return.
- Use null / unavailable state explicitly when data is absent.
- Keep provider-specific raw payloads outside the canonical KRC contract unless explicitly required and privacy-reviewed.
- Persist the actual provider and model used for each job.

## Evidence-integrity rule

The canonical KRC evidence transcript MUST preserve the source speech as faithfully as the provider allows.

Gemini Smart transcription MUST NOT silently replace the canonical evidence transcript because it can clean fillers, false starts, self-corrections, formatting, dates, numbers, or other spoken structure.

Required model:

```text
canonical evidence transcript -> verbatim / minimally transformed
optional readable derivative   -> Smart transcription, if separately enabled
```

If Smart mode is used, label it as a derived readable representation and keep it distinguishable from the canonical evidence transcript.

## Migration phases

### Phase 0 - Recovery and baseline freeze

- Recover canonical KRC Media source and deployment state.
- Record current provider/model configuration.
- Record current job/API/persistence contracts.
- Select a reproducible baseline media corpus.
- Capture current AssemblyAI results and quality metrics before refactoring.
- Do not change provider behavior in this phase.

Checkpoint: CURRENT_STATE_ACCEPTED.

### Phase 1 - Provider abstraction with zero behavior change

- Introduce a provider-neutral transcription interface.
- Move current AssemblyAI async logic behind an AssemblyAI adapter.
- Preserve AssemblyAI as the only/default active provider.
- Preserve current API shape, job states, persistence, idempotency, error semantics, cleanup behavior, and quotas.
- Add regression tests proving no behavioral change.

Checkpoint: PROVIDER_ABSTRACTION_PASS.

### Phase 2 - Gemini adapter behind an inactive selector

- Add Gemini prerecorded transcription adapter.
- Keep the selector default on AssemblyAI.
- Reuse an existing Gemini credential only if the recovered security/configuration model makes that appropriate; otherwise use a dedicated secret.
- Keep all secrets in environment/secret storage only.
- Add explicit model selection; do not rely on provider defaults.
- Implement provider-specific upload/request/response/cleanup handling.

Checkpoint: GEMINI_ADAPTER_UNIT_PASS.

### Phase 3 - Result normalization and contract tests

Normalize Gemini output to the KRC Media canonical result contract.

Validate:

- complete transcript text;
- segment ordering;
- timestamp monotonicity;
- word timestamp normalization when enabled;
- detected language handling;
- confidence semantics;
- diarization semantics when enabled;
- provider/model reporting;
- retryable vs non-retryable errors;
- provider data cleanup state;
- no secret or raw provider payload leakage.

Checkpoint: NORMALIZATION_PASS.

### Phase 4 - Long-media strategy

At activation time, use the CURRENT official Gemini limits, not values copied from this plan.

If media duration exceeds the current limit for the selected feature set:

```text
media
 -> deterministic chunking
 -> transcribe each chunk
 -> apply exact timestamp offsets
 -> deterministic ordered merge
 -> validate no gaps / overlaps / truncation
```

Requirements:

- chunk boundaries must be reproducible;
- timestamp offsets must remain monotonic;
- no silent truncation;
- partial failure must be visible;
- retries must preserve idempotency;
- merged transcript must preserve provenance to source chunk ranges.

Checkpoint: LONG_MEDIA_PASS.

### Phase 5 - Controlled A/B evaluation

Run the SAME accepted media corpus through AssemblyAI and Gemini.

Recommended corpus: at least 5-10 representative items, including where available:

- clear single-speaker English;
- noisy speech;
- interviews / multiple speakers;
- proper names and domain jargon;
- numbers, dates, acronyms;
- Ukrainian / Russian / English multilingual material;
- code-switching;
- longer material requiring chunk handling.

Compare:

```text
factual word accuracy
proper names / entities
numbers / dates
omissions
hallucinated content
language detection / code-switching
timestamp quality
diarization quality when enabled
segment completeness
processing time
provider failures / retries
free-tier quota consumption
```

Do not select a winner from aesthetic fluency alone. For KRC, factual fidelity has priority over polished wording.

Checkpoint: A_B_EVIDENCE_REVIEW.

### Phase 6 - Canary beta

Only after A/B acceptance:

- enable Gemini for a small controlled subset of KRC Media jobs;
- keep AssemblyAI available for immediate rollback;
- persist provider/model per job;
- verify persistence across restart/redeploy;
- verify job status/failure accounting/idempotency;
- verify provider data cleanup;
- monitor quota and confirm zero paid usage.

Checkpoint: GEMINI_CANARY_PASS.

### Phase 7 - Cutover decision

Gemini may become the KRC Media default only when ALL acceptance criteria below pass and the user explicitly approves cutover.

A provider switch must be configuration-driven and reversible.

Expected rollback concept:

```text
KRC_MEDIA_STT_PROVIDER=assemblyai
```

Rollback must not require destructive schema changes or data repair.

Checkpoint: USER_CUTOVER_APPROVAL_REQUIRED.

### Phase 8 - Observation and stabilization

After cutover:

- keep the AssemblyAI adapter during an observation period;
- validate multiple real KRC jobs;
- compare production quality against the accepted A/B baseline;
- watch quotas, rate limits, provider failures, and latency;
- update architecture, deployment, privacy, recovery, and operator documentation;
- remove legacy provider support only under a separate explicit decision.

Checkpoint: TRANSITION_COMPLETE.

## Free-only constraint

The migration is constrained to zero paid usage unless the user explicitly approves otherwise.

Mandatory rules:

- verify Free Tier availability and quotas before implementation and again before cutover;
- no automatic paid upgrade;
- no automatic fallback path that can create charges;
- no paid provider feature without explicit user approval;
- expose quota exhaustion as a controlled state instead of silently switching to a paid route;
- document quota accounting for test and production jobs.

## Security and privacy constraints

- Never commit API keys, bearer tokens, cookies, database credentials, or provider secrets.
- Provider credentials stay server-side.
- Review current Free Tier data-use terms before activation.
- Explicitly handle deletion / cleanup of uploaded provider files and provider-side transcript artifacts where supported.
- Do not persist raw audio or full provider responses unless KRC policy explicitly requires it and retention is documented.
- Do not weaken existing KRC privacy guarantees as part of STT migration.

## Compatibility constraints

The migration MUST preserve unless a separately approved versioned change is required:

```text
public/internal job IDs
job state machine
idempotency
persistence and restart durability
failure accounting
API response compatibility
pagination / transcript segment access
source URL provenance
provider/model audit metadata
```

A provider migration is not permission to redesign unrelated KRC Media subsystems.

## Database boundary

The Render PostgreSQL -> Neon migration is a separate KRC Media initiative.

Do not combine database migration and STT provider migration into one cutover or one failure domain unless the user explicitly requests consolidation after both plans are independently validated.

## Acceptance criteria

Transition to Gemini is accepted only if all applicable checks pass:

```text
automated tests: PASS
provider abstraction regression: PASS
Gemini adapter contract: PASS
no transcript truncation: PASS
timestamps monotonic after normalization/chunk merge: PASS
provider/model metadata accurate: PASS
API compatibility or approved versioning: PASS
persistence/durability after restart/redeploy: PASS
idempotency: PASS
failure accounting: PASS
provider cleanup behavior: PASS
security/privacy review: PASS
free-tier preflight: PASS
paid usage: 0 unless explicitly approved
rollback to AssemblyAI: VERIFIED
A/B factual fidelity: accepted by user
```

Gemini should not become default merely because it is newer. It must be at least as reliable as the AssemblyAI baseline for KRC's evidence-oriented workload and must show an acceptable quality/cost/privacy profile.

## Development discipline

- One bounded PR/checkpoint per migration phase where practical.
- CI must be green before the next phase.
- Do not mix unrelated refactors.
- Preserve rollback at every provider-changing phase.
- Record decisions and live acceptance evidence.
- Do not claim live validation without an actual live run.

## Activation command / first action

When the user explicitly activates this plan in KRC Media, begin with exactly this workflow:

```text
RECOVER current KRC Media from canonical repo/branch
 -> read this pending plan
 -> verify current Gemini official model/docs/pricing/free-tier/data-use/limits
 -> audit current AssemblyAI STT implementation and contracts
 -> identify exact affected files/tests/deployment variables
 -> report CURRENT_STATE + RISKS + PHASE_1 CHECKPOINT PLAN
 -> STOP before first infrastructure/environment change until user approves
```

Status transition after explicit activation:

```text
PENDING - DO NOT EXECUTE
 -> ACTIVE - RECOVERY/PREFLIGHT
```

Do not self-activate this plan based on VoiceBridge completion alone. Explicit user activation in KRC Media remains mandatory.
