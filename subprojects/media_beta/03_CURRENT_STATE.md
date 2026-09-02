# MEDIA BETA Current State
Поточний канонічний стан приватного MEDIA BETA для відновлення без реконструкції історії.

Version: 8.0
Status: RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED
Updated: 2026-09-02

## Executive state

```text
PUBLIC CORE                               PUBLISHED / MAINTENANCE
MEDIA BETA                                CLOSED BETA / OWNER TESTING
A9 / A9.10 / A10                          ACCEPTED
M3 PROVIDER EVIDENCE                      COMPLETE
M3                                        CLOSED
M4 IMAGE PARITY                           PASS
M4 OWNER-ONLY CANARY                      PASS
M4 PERMANENT BACKEND PROMOTION            NOT AUTHORIZED
R1 / R2 / R3 / R4                         HOLD
```

Current recovery authority:

`72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`

Earlier full operational baseline remains available in checkpoint 62 and Git history; this file intentionally summarizes the current state rather than duplicating the full historical audit trail.

## Product and repository boundary

```text
product: K-Research & Critic
public Core repo: kolemasakar/K_Research_Critic
public Core branch: main
MEDIA BETA branch: agent/video-url-research
VoiceBridge repo: kolemasakar/VoiceBridge
VoiceBridge KRC migration branch: agent/krc-media-gemini-migration
VoiceBridge PR: #45 / draft / unmerged unless reverified otherwise
```

VoiceBridge is the technology/backend source. `K_Research_Critic` remains product and roadmap authority.

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

Hybrid C/D is recorded as a future plan only:

```text
state: PLANNED / NOT IMPLEMENTED
trigger: AssemblyAI free credits exhausted
additional gate: fresh owner authorization and mutable-assumption revalidation
```

Planned future roles:

```text
Gemini Transcribe Live -> preferred free eligible route
Gemini unary Transcribe -> timestamps/diarization feature route when free quota permits
AssemblyAI universal-2 -> rollback/fallback technology; paid use disabled by default
```

No implementation or automatic paid fallback is currently authorized.

Product plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

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

Accepted runtime contract:

```text
durable_store: postgres
restart_resilient_jobs: true
duplicate start reuses existing job: true
durable STT quota ledger: active
```

The M4 owner canary directly verified Neon connectivity, required KRC tables, durable job readback, segment readback, and idempotent duplicate reuse.

## M3 closure

Seven reviewed cases across the first and expanded A/B tranches did not establish a global STT quality winner.

```text
AssemblyAI lexical WER: 13.68%
Gemini lexical WER: 14.53%
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

M3 was closed retaining AssemblyAI `universal-2` as the current KRC prerecorded provider.

## M4 image parity

VoiceBridge M4 target:

`6a9491359795840ec9e79c9edc0ea82f595e9784`

Validate run:

`33577022166` - SUCCESS.

Accepted final-image requirements:

```text
ffmpeg: PASS
ffprobe: PASS
psql: PASS
final Docker image build: PASS
no-provider KRC startup smoke: PASS
```

Authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

## M4 bounded owner-only canary

Owner-authorized live canary workflow run:

`33580592224` - SUCCESS.

Isolated service:

`voicebridge-krc-media-beta-kolemasakar`

Temporarily tested exact target:

`6a9491359795840ec9e79c9edc0ea82f595e9784`

One real accepted Telegram fixture was processed through AssemblyAI:

```text
KRCM job: KRCM_8c0f6a9e-b3c9-4c9a-8978-69d6c5acc535
status: COMPLETED
provider: assemblyai
STT seconds: 53
retrieval credits: 0
segment count: 1
provider cleanup: PASS
```

Canary additionally proved:

```text
owner bearer boundary: PASS
Cobalt configured/reachable: PASS
ScrapeCreators inactive: PASS
Neon connectivity/schema: PASS
no-provider durable mutation: NONE
durable readback: PASS
duplicate reuse: PASS
one durable job row: PASS
one STT reservation row: PASS
invalid/private Telegram boundary: PASS
```

Mandatory rollback restored exact pre-canary Render commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

Post-rollback health passed. The one-shot canary workflow was removed after execution.

Authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

## Current release boundary

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 permanent backend promotion                  HOLD
R3 external testers                             HOLD
R4 public rollout                               HOLD
```

M4 canary acceptance does not imply any of these gates.

## Exact continuation point

```text
OWNER POST-CANARY DECISION
R1 MERGE AND R2 PERMANENT BACKEND PROMOTION REMAIN SEPARATE GATES
```

Before either R1 or R2, reverify current repository heads/CI, exact scope/diff, current Render live baseline and rollback target, environment presence without exposing secrets, Neon connectivity, provider state, and release-hold invariants.
