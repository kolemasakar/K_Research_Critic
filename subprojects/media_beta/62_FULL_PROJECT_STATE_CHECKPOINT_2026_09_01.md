# K-Research & Critic MEDIA BETA - Full Project State Checkpoint
Повний канонічний checkpoint стану KRC Core, MEDIA BETA, VoiceBridge та їх взаємозв'язків.

Version: 1.0
Status: CANONICAL_RECOVERY_CHECKPOINT / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Snapshot time: 2026-09-01 11:27 Europe/Kyiv

## Purpose

This checkpoint preserves the complete current K-Research & Critic / MEDIA BETA project state and the relationships between the KRC public Core, the closed MEDIA BETA module, VoiceBridge main, the VoiceBridge KRC prerecorded migration branch, accepted runtime infrastructure, provider boundaries, release gates, and the exact continuation point.

It is intended for deterministic recovery in a new chat without reconstructing state from older planning documents.

This checkpoint contains no credentials, API keys, bearer tokens, database passwords, signed URLs, or other secret material.

## 1. Product Hierarchy

```text
K-Research & Critic
|
+-- PUBLIC CORE
|   repo: kolemasakar/K_Research_Critic
|   branch: main
|   state: PUBLISHED / MAINTENANCE
|   roadmap: Phase 0-12 COMPLETE
|
+-- K-Research & Critic - MEDIA BETA
    role: closed-beta module of K-Research & Critic
    product/roadmap authority: K_Research_Critic
    KRC beta branch: agent/video-url-research
    state: RELEASE_HOLD_OWNER_TESTING
    |
    +-- media/backend technology source: VoiceBridge
        +-- current VoiceBridge project baseline: main
        +-- KRC prerecorded forward migration: agent/krc-media-gemini-migration
        +-- legacy accepted KRC runtime lineage: agent/krc-media-transcript
```

VoiceBridge is a technology/backend implementation and validation source. It is not the parent product and cannot independently authorize KRC product release gates.

## 2. Exact GitHub State at Snapshot

### K_Research_Critic main

```text
repo: kolemasakar/K_Research_Critic
branch: main
head: 17cb85361c2e5727e3de176a05b2a55660e5e2be
head message: DOCS: Account for VoiceBridge Gemini migration impact
CI workflow: Tests
CI run: 33486314648
CI result: SUCCESS
```

This main state records the published Core as maintenance and documents the closed-beta MEDIA BETA relationship without activating MEDIA in the public Builder.

### K_Research_Critic MEDIA BETA branch before this checkpoint write

```text
branch: agent/video-url-research
pre-checkpoint head: c29d8626df8bb799742cd0cc970e7e65d4fc254f
pre-checkpoint head message: DOCS: Record VoiceBridge Gemini impact on MEDIA BETA
CI run: 33486527423
CI result: SUCCESS
PR: #8
PR state: OPEN / DRAFT / UNMERGED
PR mergeable at snapshot: FALSE
```

The `mergeable=false` observation is an integration-state fact, not a release decision. Main has advanced independently with documentation synchronization commits. No merge, rebase, force update, or conflict resolution is authorized by this checkpoint.

### VoiceBridge main

```text
repo: kolemasakar/VoiceBridge
branch: main
head: a426ae331721dd36291874e45380faf603d854cf
head meaning: Phase 2 Universal Cloud Audio closure
CI run: 33290771682
CI result: SUCCESS
VoiceBridge Phase 1: COMPLETE
VoiceBridge Phase 2: COMPLETE
next VoiceBridge functional phase: Phase 3 Cloud Service Hardening
```

### VoiceBridge KRC prerecorded migration branch

```text
branch: agent/krc-media-gemini-migration
head: 7c2cac849d9322a8b532815ac3be44e87bd52e27
head message: Advance M3 corpus plan to locked source tranche
PR: #45
PR state: OPEN / DRAFT / UNMERGED
PR mergeable at snapshot: TRUE
Validate run: 33480804395
Validate result: SUCCESS
cloud: PASS
browser-extension: PASS
repository-docs: PASS
cloud regression baseline: 224/224 PASS
```

Current branch relation to VoiceBridge main:

```text
merge base: eba77183bee29621aa6c7cb859737a10edb6e4d4
migration branch vs current main: DIVERGED
migration branch ahead: 32 commits
migration branch behind: 13 commits
```

The observed 13-commit main-only delta contains VoiceBridge Phase 2 documentation/closure synchronization and no additional runtime source files. Immediate KRC runtime re-port is not required solely because of that delta, but the relationship must be re-checked before later integration/M4 work.

## 3. Published KRC Core State

```text
Phase 0-12: COMPLETE
GPT Store product: PUBLISHED
Core mode: MAINTENANCE
public Actions: DISABLED
public Apps: DISABLED
web search: ENABLED
Code Interpreter/Data Analysis: ENABLED
request logging Action: DISABLED
script.google.com consent interruption: ABSENT
MEDIA BETA activation in public Core: FALSE
```

Core invariants remain unchanged:

- CriticProfile approval gate before autonomous independent research;
- immutable approved profile unless a material amendment is re-approved;
- Research/Critic separation and bounded revision loop;
- claim-level independent cross-check ledger;
- visible SHORTFALL when evidence requirements are not met;
- underlying-source/origin traceability and syndication de-duplication;
- explicit limitations/failure state;
- private chain-of-thought is not required for auditability.

## 4. MEDIA BETA Accepted Runtime Baseline

Current accepted private runtime baseline:

```text
A8 browser-assisted owner baseline: COMPLETE / FALLBACK ONLY
A9 owner zero-client media input: ACCEPTED
A9.10 local attachment: ACCEPTED
A10 copy-safe claim-summary stabilization: ACCEPTED
release state: RELEASE_HOLD_OWNER_TESTING
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder runtime applied: TRUE
```

Accepted owner inputs:

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel
supported public Telegram video post
one current-conversation local audio/video attachment
```

Normal product flow:

```text
supported media input
 -> private KRC MEDIA BETA Action
 -> isolated VoiceBridge KRC media runtime
 -> source-specific retrieval / transcript path
 -> durable KRCM transcript state
 -> CriticProfile
 -> explicit owner approval
 -> Research
 -> Critic
 -> localized final report
```

Transcript evidence proves what the media said; it does not independently prove that the media claim is true.

## 5. Accepted Media Route Policies

### YouTube / Instagram

Managed transcript route remains accepted. Provider/credit-consuming work remains consent-gated. Instagram AI generation is not an automatic fallback and requires a separate preflight and consent after native-unavailable state.

### Facebook

```text
Cobalt success -> active prerecorded STT -> durable KRCM
Cobalt failure -> unavailable -> STOP
automatic paid fallback -> FORBIDDEN / INACTIVE
ScrapeCreators -> reserve compatibility only / not offerable
```

The no-automatic-paid-fallback regression policy is accepted.

### Telegram

```text
public web/embed
 -> trusted Telegram media delivery
 -> active prerecorded STT
 -> durable KRCM
retrieval credits = 0
no login/cookies/session/bot token/paid fallback
```

### Local attachment

```text
one current-conversation audio/video attachment
 -> openaiFileIdRefs
 -> trusted OpenAI temporary delivery
 -> bounded probe/ingestion
 -> active prerecorded STT
 -> durable KRCM
max accepted attachment = 32 MiB
retrieval credits = 0
```

No normal owner flow exposes or asks for a raw file token, signed attachment URL, KRCM internal job ID, platform cookies/session, or provider credential.

## 6. Durable State and Infrastructure Baseline

Accepted MEDIA BETA durable-store baseline:

```text
provider: Neon PostgreSQL
PostgreSQL major: 18
project label: krc-media-beta-neon
database: krc_media_beta
region: AWS Europe Central 1 (Frankfurt)
connection mode: direct TLS
```

The accepted isolated application runtime remains the dedicated MEDIA BETA service lineage. The original Render PostgreSQL source database is retained as a separately gated rollback source and must not be deleted without explicit authorization.

Accepted durability/security behavior includes:

- durable KRCM job and segment persistence;
- restart readability and idempotent replay where defined;
- concurrency-safe shared STT quota ledger;
- fail-closed durable-store/quota behavior before provider start;
- no automatic replay of uncertain-charge operations;
- provider/local temporary cleanup reporting;
- no signed attachment URL persistence;
- no raw owner admission persistence;
- configured retention and purge rules;
- metadata-only/redacted diagnostics for sensitive paths.

This checkpoint does not claim a fresh live database read. These values are the latest accepted documented runtime baseline and remain subject to later exact runtime revalidation when a deployment-changing action is considered.

## 7. VoiceBridge Gemini Migration - Correct Interpretation

VoiceBridge real-time streaming STT migration is complete:

```text
VoiceBridge live STT selector: STT_PROVIDER
VoiceBridge live default: gemini
VoiceBridge live model: gemini-3.5-transcribe-live
VoiceBridge live AssemblyAI: explicit rollback
state: ACCEPTED DEFAULT
```

This is separate from KRC prerecorded evidence transcription.

Current KRC prerecorded provider state on the migration branch:

```text
KRC selector: KRC_MEDIA_STT_PROVIDER
normal active provider: AssemblyAI
normal active model: universal-2
provider boundary: MediaTranscriptionProvider
Gemini prerecorded model: gemini-3.5-transcribe
Gemini prerecorded adapter: IMPLEMENTED / TESTED
Gemini normal prerecorded activation: FALSE
```

The current provider factory fails closed if normal KRC jobs attempt to select Gemini before the activation gate. VoiceBridge live Gemini acceptance therefore does not equal KRC prerecorded Gemini cutover.

## 8. KRC Prerecorded Gemini Migration Track

```text
M0 recovery/migration preflight                 COMPLETE
M1 provider abstraction                        PASS
M2 Gemini prerecorded adapter                  PASS / INACTIVE
M3 offline evaluator                           PASS
M3 same-asset execution contract               PASS
M3 corpus manifest/readiness contract          PASS
M3 byte-exact evidence preparation helper      PASS
first public corpus source tranche             LOCKED
M4 new-infrastructure canary                    NOT_STARTED
M5 provider/new-infrastructure cutover          NOT_AUTHORIZED
```

First locked public cases:

```text
ua-clean-public-001
ru-clean-public-001
en-clean-public-001
```

Current real-evidence boundary:

```text
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED       TRUE
REAL_ASSET_BYTES_CAPTURED                FALSE
ASSET_SHA256                             NOT_CREATED
REFERENCE_TRANSCRIPT_SHA256              NOT_CREATED
REFERENCE_INDEPENDENT_REVIEW             NOT_COMPLETE
READY_FOR_AB                             FALSE
M3_LIVE_PRERECORDED_AB                   NOT_RUN
ASSEMBLYAI_CORPUS_CALLS                  NONE
GEMINI_PRERECORDED_CORPUS_CALLS          NONE
```

## 9. Exact Current Roadmap Position

```text
CURRENT_MILESTONE = M3 BYTE CAPTURE + SHA-256
```

Required transition:

```text
SOURCE_LOCKED_PENDING_BYTE_CAPTURE
 -> capture exact public media bytes
 -> compute byte-exact media SHA-256
 -> retain only non-secret digest/metadata evidence
 -> DO NOT retain raw media as GitHub artifact
 -> delete temporary raw media after hashing
 -> prepare independent reference transcript outside raw-media repository storage
 -> manually reconcile reference text to actually spoken audio
 -> compute exact reference-transcript SHA-256
 -> independent review
 -> READY_FOR_AB
 -> controlled same-asset AssemblyAI vs Gemini prerecorded A/B
 -> deterministic metrics + manual factual/hallucination review
 -> M3 closure decision
```

The byte-capture step must not call AssemblyAI or Gemini and must not consume provider transcription quota/credits.

## 10. M4 / M5 Boundary

M4 cannot start merely because VoiceBridge Phase 2 is complete.

Before M4 canary, KRC-specific deployment-image parity must be verified for at least:

```text
media retrieval dependencies
media probing/transcoding
managed KRC HTTP routes
Neon/PostgreSQL tooling and durable persistence
quota ledger
retention and provider cleanup
Facebook/Telegram/attachment route isolation
privacy/log-redaction guards
```

M5 provider or infrastructure cutover requires separate explicit owner approval and a verified rollback path.

## 11. Release Gates

All KRC MEDIA BETA release gates remain independent and closed:

```text
R1 merge selected MEDIA BETA work toward KRC main   HOLD
R2 backend/production promotion                     HOLD
R3 external testers                                 HOLD
R4 public sharing / Store rollout                   HOLD
```

Completion of M3, successful CI, VoiceBridge Phase 2 completion, or a favorable Gemini comparison does not automatically authorize any R1-R4 gate.

## 12. Known Current Integration / Documentation Conditions

1. KRC PR #8 is draft/open/unmerged and currently reports `mergeable=false`. Do not attempt merge/rebase solely to make the PR green while release hold is active.
2. VoiceBridge PR #45 is draft/open/unmerged and currently reports `mergeable=true`; it remains a technical forward-port/evidence branch, not a KRC release authorization.
3. `subprojects/media_beta/03_CURRENT_STATE.md` remains the accepted operational baseline through the 2026-08-29 hardening state. Its older VoiceBridge branch identifiers are historical runtime lineage. Newer cross-repository/provider interpretation is governed by records 60, 61, and this checkpoint.
4. VoiceBridge `main` and `agent/krc-media-gemini-migration` are diverged; the currently observed main-only delta is documentation/Phase 2 closure. Re-check before M4/integration because future deltas may include runtime changes.
5. No current documentation should label KRC Gemini prerecorded as active before M3 evidence and a separate explicit activation decision.

## 13. Source-of-Truth Precedence

When records disagree, use this order:

```text
1. current code + exact-head CI + verified current runtime evidence
2. this full-state checkpoint for the 2026-09-01 recovery snapshot
3. 61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
4. 60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
5. 03_CURRENT_STATE.md for accepted operational runtime baseline
6. 53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md for owner release authority
7. latest capability-specific acceptance record
8. older historical/planning records
```

VoiceBridge records are authoritative for VoiceBridge implementation evidence, but cannot independently authorize a KRC release gate.

## 14. Recovery Procedure

For a fresh chat:

```text
recover KRC MEDIA BETA full state checkpoint 2026-09-01
```

Recovery order:

```text
1. 62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md
2. 00_INDEX.md
3. 61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
4. 60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
5. 03_CURRENT_STATE.md
6. 53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
7. 01_ARCHITECTURE.md
8. 02_ROADMAP.md
9. 06_DECISION_LOG.md
10. 04_OPERATIONS_RUNBOOK.md / 05_TEST_PLAN.md as needed
```

Then verify current GitHub heads/CI for:

```text
K_Research_Critic/main
K_Research_Critic/agent/video-url-research / PR #8
VoiceBridge/main
VoiceBridge/agent/krc-media-gemini-migration / PR #45
```

If any head differs from this checkpoint, inspect the delta before changing code or roadmap state.

## 15. Non-Negotiable Safety/Policy Boundary

Do not silently:

- merge MEDIA BETA to public Core;
- change public KRC Builder/Action state;
- promote/replace the beta backend;
- activate Gemini prerecorded for normal KRC jobs;
- enable automatic paid fallback;
- enable ScrapeCreators as an automatic Facebook fallback;
- weaken Facebook Cobalt-failure -> unavailable policy;
- weaken Telegram public-only/zero-credit policy;
- persist raw media, signed attachment URLs, provider credentials, or secret admission material in documentation/artifacts;
- delete the retained rollback database/runtime lineage;
- start M4/M5 without their explicit gates.

## 16. Snapshot Marker

```text
KRC_PUBLIC_CORE_PHASE_0_12_COMPLETE
KRC_PUBLIC_CORE_MAINTENANCE
KRC_MEDIA_BETA_CLOSED_BETA
A9_A9_10_A10_ACCEPTED
RELEASE_HOLD_OWNER_TESTING
VOICEBRIDGE_LIVE_GEMINI_DEFAULT_ACCEPTED
VOICEBRIDGE_PHASE_2_COMPLETE
KRC_PRERECORDED_ASSEMBLYAI_ACTIVE
KRC_GEMINI_PRERECORDED_IMPLEMENTED_INACTIVE
KRC_M0_COMPLETE
KRC_M1_PASS
KRC_M2_PASS_INACTIVE
KRC_M3_ACTIVE
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED
REAL_ASSET_BYTES_CAPTURED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_PRERECORDED_AB_NOT_RUN
CURRENT_MILESTONE_M3_BYTE_CAPTURE_SHA256
M4_NOT_STARTED
M5_NOT_AUTHORIZED
R1_R2_R3_R4_HOLD
```

Canonical checkpoint marker:

`KRC_MEDIA_BETA_FULL_STATE_2026_09_01_M3_BYTE_CAPTURE_SHA256`
