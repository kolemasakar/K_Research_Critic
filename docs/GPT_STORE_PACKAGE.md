# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, optional media path та release-gates для GPT Store.

Version: 2.0
Status: PRODUCTION CORE / MEDIA PREVIEW

## 1. Purpose

This document is the operator-facing packaging specification for the published K-Research & Critic Custom GPT and the optional video URL upgrade.

Repository:

```text
kolemasakar/K_Research_Critic
```

Core production baseline:

```text
K-Research & Critic v1.0.0
```

The package separates two scopes.

Core text path invariants:

```text
no developer API key required
no mandatory external backend
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for research
mandatory CriticProfile approval gate
```

Optional media path invariants:

```text
Media Transcript Action enabled
external media backend required only for media ingestion
provider API key owned by the service, not the user
public YouTube initial source platform
auto / uk / ru / en source-language baseline
transcript is source content, not independent proof
existing CriticProfile / Research / Critic workflow preserved
```

Default user-facing language is Ukrainian (`uk-UA`).

## 2. Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
gpt_store/actions/media_transcript_openapi.yaml
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
docs/VIDEO_INPUT_UPGRADE.md
docs/PRIVACY_POLICY.md
```

The manifest is the canonical human/machine-readable Builder configuration source.

## 3. Builder Configuration

### Name

```text
K-Research & Critic
```

### Description

Copy `product.description` from `gpt_store/manifest.yaml` into Builder exactly.

### Default language

```text
uk-UA
```

### Recommended model

Leave the recommended model unset.

The workflow must not depend on one named model. Use runtimes exposed by the user's plan and compatible with the configured capabilities.

### Core Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
```

Disable:

```text
Image generation
Apps
```

### Media Action

Media preview requires Custom Actions enabled and the schema from:

```text
gpt_store/actions/media_transcript_openapi.yaml
```

Configure Action authentication as a bearer/API-key secret using the same secret as VoiceBridge `KRC_MEDIA_ACTION_TOKEN`.

Never place the bearer secret or AssemblyAI API key into GPT instructions, Knowledge files, repository files, or user-visible text.

The Action server is:

```text
https://voicebridge-cloud-us.onrender.com
```

Before public rollout configure a public privacy-policy URL for the Action. The repository source document is:

```text
docs/PRIVACY_POLICY.md
```

### Knowledge

No uploaded Knowledge file is mandatory for the core product or the media adapter.

## 4. Conversation Starters

Use the starters from `gpt_store/manifest.yaml`.

The media candidate includes a YouTube claim-verification starter while preserving general research, comparison, direct claim verification, and checkpoint recovery starters.

## 5. Store Workflow Mapping

Text task:

```text
Supervisor stage
  -> Domain/risk assessment
  -> CriticProfile proposal
  -> USER CHOICE: 1=APPROVE / 2=EDIT / 3=REJECT
  -> Research stage
  -> Critic stage
  -> autonomous REVISE/PASS loop
  -> Final report
  -> Review protocol
```

Media URL task:

```text
Public YouTube URL
  -> transcript acquisition
  -> material claim inventory
  -> Domain/risk assessment
  -> CriticProfile proposal
  -> USER CHOICE: 1=APPROVE / 2=EDIT / 3=REJECT
  -> independent claim research
  -> Critic stage
  -> autonomous REVISE/PASS loop
  -> Final report with claim verification
  -> Review protocol
```

Media intake before approval may acquire and classify source content only. Independent external truth verification begins after profile approval.

The Store Edition provides logical multi-agent separation inside one ChatGPT runtime rather than process-isolated model instances.

## 6. Media Action Contract

Operations:

```text
startMediaTranscription
getMediaTranscriptionStatus
getMediaTranscriptSegments
```

The Action returns asynchronous job state and paged transcript segments with timestamps/confidence where available.

The GPT should follow all transcript pages until `next_cursor` is null.

If bounded status checks do not reach `COMPLETED`, the GPT must not claim that it is continuing work independently. It may ask the user to send `continue` to check the same job again.

The media adapter is not a fact-checking provider. It supplies source content only.

## 7. Checkpoint and Fresh-chat Recovery

Cross-chat continuation uses the existing explicit user-controlled checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Checkpoint schema remains:

```text
1.0
```

Checkpoint generation is explicit-request only. Normal profile gates and final reports must not auto-create checkpoints.

Safe states remain:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
APPROVED
FINALIZED
COMPLETED_WITH_LIMITATIONS
FAILED
```

The full media transcript is not stored in checkpoints. A pending external transcription job is not represented as a recoverable checkpoint state under schema 1.0.

## 8. Static Validation

Run after Store package changes:

```text
python -m scripts.validate_store_package
python -m pytest
```

CI additionally validates repository policy, typed boundaries, lint correctness, dependency integrity, and coverage.

The Store package validator also checks:

```text
manifest media scope
Action schema and operation IDs
bearer authentication declaration
YouTube platform baseline
uk / ru / en language baseline
media PREVIEW_REQUIRED state
privacy-policy source document
claim-verification instruction tokens
unchanged checkpoint compatibility
```

## 9. Existing Production Regression Matrix

The original pre-publication matrix completed successfully on 2026-08-14:

```text
P1 New low-risk research task - PASS
P2 High-risk domain task and conservative risk floor - PASS
P3 Explicit APPROVE gate including numeric alias 1 - PASS
P4 EDIT/2 then approve - PASS
P5 REJECT/3 stops autonomous execution - PASS
P6 Research -> Critic -> PASS - PASS
P7 Forced REVISE then corrected second iteration - PASS
P8 Web-search-unavailable/freshness limitation behavior - PASS
P9 Generate checkpoint at PROFILE_APPROVED - PASS
P10 Paste checkpoint into a fresh GPT conversation and resume - PASS
P11 Malformed checkpoint rejection - PASS
P12 Final report plus review protocol without hidden reasoning - PASS
```

These scenarios must remain regression tests for the media upgrade.

## 10. Media Preview Test Matrix

The media feature must not move to production until at least these scenarios pass:

```text
M1 Action schema imports in GPT Builder
M2 Action bearer authentication works and rejects invalid secret
M3 Real Ukrainian YouTube transcript
M4 Real Russian YouTube transcript
M5 Real English YouTube transcript
M6 Automatic source-language detection
M7 Timestamp-to-claim traceability
M8 Names/dates/numbers transcription uncertainty handling
M9 Video/transcript not treated as independent corroboration
M10 Supporting and contradicting source search
M11 CriticProfile approval still blocks research
M12 Forced media REVISE -> corrected PASS
M13 Existing text workflow unchanged
M14 Existing checkpoint workflow unchanged
M15 Free-plan live media test
M16 Paid-plan compatible-runtime media test
M17 provider model-training opt-out verified
M18 provider deletion status verified
M19 privacy-policy public URL configured
M20 production media smoke test
```

## 11. Account/Plan Boundary

Existing live validation on 2026-08-14 remains valid for the core text product.

Media mode requires a runtime/account path that supports the configured Action. If a selected runtime does not expose Actions, media transcription is unavailable for that run; the product must surface the limitation rather than degrade silently.

The user is never asked for the developer provider key or Action bearer secret.

## 12. Privacy and Retention

The candidate policy is documented in `docs/PRIVACY_POLICY.md`.

Required release controls include:

```text
public media URL only
dedicated Action bearer secret
temporary downloaded media deletion
bounded in-memory transcript retention
provider transcript/audio delete request
provider_data_deleted status surfaced
no full transcript in checkpoints
provider model-training opt-out verified before production
public privacy-policy URL configured before Store rollout
```

## 13. Publication State

Core product publication remains:

```text
publication_state: published
published_at: 2026-08-14
store_category: Research & Analysis
core production smoke test: PASS
```

Media candidate state remains separate:

```text
media_input.rollout_state: PREVIEW_REQUIRED
media_input.production_smoke_test_passed: false
```

Do not change the media fields to production values until the media test matrix and privacy gates pass.

## 14. Production Smoke Test Baseline

The original text-production smoke test on 2026-08-14 used:

```text
high-risk geodesy/construction task
CriticProfile approval gate
web_search=AVAILABLE
Research
Critic review
REVISE
corrected research
Critic PASS
final report + review protocol
```

Observed final result:

```text
Critic history: REVISE -> PASS
final reliability score: 0.93
workflow status: FINALIZED
automatic checkpoint: absent
internal citation/tool markup: absent
normal visible sources: present
```

The media release requires an additional independent smoke test and must not overwrite the historical core result.

## 15. Maintenance Rules

Any Builder change is a product update and must be revalidated before applying it to the published GPT.

Allowed K-Research & Critic work includes:

```text
bug/security fixes
OpenAI/ChatGPT compatibility changes
Store-package compatibility changes
regression fixes
documentation corrections
input/UX extensions that preserve the Research-Critic core
maintenance releases
```

The general Modular Agent Platform remains outside this repository and continues in `K_Supervisor`.
