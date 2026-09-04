# MEDIA BETA Current State
Поточний канонічний стан приватного MEDIA BETA для відновлення без реконструкції історії.

Version: 8.1
Status: CROSS_SYSTEM_CHECKPOINT_73 / R0_PUBLIC_KRC_UPDATE_PREFLIGHT_NEXT
Updated: 2026-09-04

## Executive state

Owner-confirmed product state plus repository/runtime evidence:

```text
PUBLIC KRC GPT                            PUBLISHED / USER-ACCESSIBLE
MEDIA BETA GPT                            OWNER-ONLY / NOT SEPARATELY PUBLISHED
A9 / A9.10 / A10                          ACCEPTED
M3                                        CLOSED
M4 IMAGE PARITY                           PASS
M4 OWNER-ONLY CANARY                      PASS
M4 PERMANENT BACKEND PROMOTION            NOT AUTHORIZED
KRC PR #8                                 OPEN / DRAFT / DIRTY / UNMERGED
VOICEBRIDGE PR #45                        OPEN / DRAFT / UNMERGED
R0                                        NEXT / NO LIVE CHANGE
R1 / R2 / R3 / R4                         HOLD
```

Current recovery authority:

`73_PUBLIC_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT_2026_09_04.md`

## Product and repository boundary

```text
product: K-Research & Critic
public product identity: existing published KRC GPT
public Core repo: kolemasakar/K_Research_Critic
public Core branch: main
MEDIA BETA product branch: agent/video-url-research
MEDIA BETA GPT: private / owner-only
VoiceBridge repo: kolemasakar/VoiceBridge
VoiceBridge KRC migration branch: agent/krc-media-gemini-migration
```

`K_Research_Critic` is product/roadmap authority. VoiceBridge is the media/backend implementation and validation source only.

Future public MEDIA capability must be integrated into the **same existing public KRC identity**, not through a new GPT publication dependency.

## Critical availability invariant

```text
MEDIA backend/action/source unavailable
        -> MEDIA unavailable / fail closed

Core KRC
        -> remains accessible and functional
```

The private MEDIA BETA GPT must never become required for public KRC users.

## Current repository evidence

KRC public `main` observed head before checkpoint 73:

`39629886e9f1f3841661c759f75279f779a937c8`

KRC MEDIA branch pre-checkpoint head:

`5241c36460f7dfe4222ab1b4f0b933cb4da0281c`

KRC MEDIA Tests:

`33870130947` — SUCCESS.

PR #8:

```text
OPEN
DRAFT
UNMERGED
mergeable: false
mergeable_state: dirty
```

Branch divergence versus current `main` at audit time:

```text
status: diverged
ahead_by: 568
behind_by: 78
```

Therefore direct merge of PR #8 as-is is not the next safe action.

VoiceBridge pre-transition-reference head:

`0252751ca3f4e04b60423cb506de630680fd83a7`

VoiceBridge Validate:

`33860807242` — SUCCESS.

PR #45:

```text
OPEN
DRAFT
UNMERGED
mergeable: true
```

## Current STT provider boundary

```text
KRC prerecorded active provider: AssemblyAI
active model: universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
```

VoiceBridge live streaming remains a separate provider domain and does not change the KRC prerecorded provider decision.

## Deferred free-first plan

Hybrid C/D remains future-only:

```text
state: PLANNED / NOT IMPLEMENTED
trigger: AssemblyAI free credits exhausted
additional gate: fresh owner authorization + mutable-assumption revalidation
```

Planned future roles:

```text
Gemini Transcribe Live -> preferred free eligible route
Gemini unary Transcribe -> timestamps/diarization route when free quota permits
AssemblyAI universal-2 -> rollback/fallback; billable use disabled by default
```

Product plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

Technical plan:

`kolemasakar/VoiceBridge/docs/planning/2026-09-02_KRC_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_IMPLEMENTATION_PLAN.md`

No Hybrid implementation or automatic paid fallback is currently authorized.

## Active accepted media routes

```text
YouTube / supported Instagram -> managed transcript path with existing consent gates
Facebook -> free Cobalt retrieval only -> AssemblyAI -> durable KRCM
Telegram -> public web/embed retrieval -> AssemblyAI -> durable KRCM
local attachment -> openaiFileIdRefs -> media normalization -> AssemblyAI -> durable KRCM
```

Critical policies:

```text
Facebook Cobalt failure -> unavailable / STOP
ScrapeCreators -> reserve only / inactive
no automatic paid provider fallback
Telegram retrieval credits -> 0
local attachment retrieval credits -> 0
local attachment max size -> 32 MiB
```

## Durable state

Active durable store remains Neon PostgreSQL for the isolated MEDIA BETA contour.

Accepted contract:

```text
durable_store: postgres
restart_resilient_jobs: true
duplicate start reuses existing job: true
durable STT quota ledger: active
```

## M3 closure

Seven reviewed cases did not establish a global STT quality winner:

```text
AssemblyAI lexical WER: 13.68%
Gemini lexical WER: 14.53%
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

M3 closed retaining AssemblyAI `universal-2` as current KRC prerecorded provider.

## M4 accepted evidence

VoiceBridge exact tested target:

`6a9491359795840ec9e79c9edc0ea82f595e9784`

Image-parity Validate:

`33577022166` — SUCCESS.

Final image requirements:

```text
ffmpeg: PASS
ffprobe: PASS
psql: PASS
final Docker image build: PASS
no-provider KRC startup smoke: PASS
```

Owner-only canary:

`33580592224` — SUCCESS.

Real canary path:

```text
public Telegram -> AssemblyAI universal-2 -> durable KRCM / Neon
STT seconds: 53
retrieval credits: 0
provider cleanup: PASS
durable readback: PASS
duplicate reuse: PASS
single STT reservation: PASS
invalid/private Telegram boundary: PASS
```

Mandatory rollback restored exact pre-canary Render commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

Permanent backend promotion was not performed.

VoiceBridge authorities:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

## Public KRC + MEDIA integration plan

Product plan:

`planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`

VoiceBridge technical plan:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

Independent gates:

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Current state:

```text
R0: NEXT / NO LIVE GPT CHANGE
R1: HOLD
R2: HOLD
R3: HOLD
R4: HOLD
```

R0 must establish safe edit/update of the same existing public KRC, current sharing/publication state, public Action/Privacy requirements, public KRC URL/identity preservation, and a rollback/reconstruction snapshot of the current GPT configuration.

R1 must not direct-merge current PR #8 as-is; after R0 PASS it requires a dedicated integration/conflict strategy plus Core and MEDIA regressions.

## Exact continuation point

```text
R0 PUBLIC KRC UPDATE SAFETY PREFLIGHT
NO LIVE GPT CHANGE
NO DIRECT MERGE OF CURRENT DIRTY PR #8
```

Recovery command:

`recover KRC MEDIA BETA cross-system checkpoint 73 public KRC MEDIA VoiceBridge 2026-09-04`
