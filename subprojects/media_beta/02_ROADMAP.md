# MEDIA BETA Roadmap
Поточний roadmap приватного K-Research & Critic MEDIA BETA.

Version: 4.6
Status: RELEASE_HOLD_OWNER_TESTING / CROSS_SYSTEM_CHECKPOINT_73 / R0_PUBLIC_KRC_UPDATE_SAFETY_PREFLIGHT_NEXT
Updated: 2026-09-04

## Product position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the already-published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main / already published GPT / owner-confirmed user-accessible
closed-beta product branch: agent/video-url-research
private MEDIA BETA GPT: owner-only / not separately published
technology/backend implementation source: kolemasakar/VoiceBridge
KRC media migration branch: agent/krc-media-gemini-migration
```

The future integration target is the **same existing published KRC identity**. MEDIA must remain additive and failure-isolated; a MEDIA backend/action failure must never make Core KRC unavailable.

## Current cross-system recovery authority

`73_PUBLIC_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT_2026_09_04.md`

This checkpoint freezes public KRC, private MEDIA BETA, VoiceBridge, their relationships, current repository/CI state, and the R0-R4 continuation plan. It does not itself change any live runtime.

## Accepted runtime baseline

```text
A9 / A9.10 / A10                           ACCEPTED
Builder package                            0.9.1-beta-a10
Action schema                              0.6.0-a9.10
release state                              RELEASE_HOLD_OWNER_TESTING
KRC prerecorded provider                   AssemblyAI universal-2
Gemini prerecorded normal activation       FALSE
```

Policy remains:

```text
Facebook Cobalt failure -> unavailable
NO automatic paid fallback
ScrapeCreators reserve only / inactive
Telegram public-only / zero retrieval credits
local attachment max 32 MiB / zero retrieval credits
```

## M3 - Provider evidence

Status: CLOSED.

```text
first A/B tranche: COMPLETE
expanded M3B A/B: COMPLETE
manual factual/hallucination review: COMPLETE
seven-case global winner: NOT_ESTABLISHED
current provider retained: AssemblyAI universal-2
provider cutover now: FALSE
```

## Deferred Hybrid C/D

Status: PLANNED / NOT_IMPLEMENTED.

Implementation trigger remains AssemblyAI free-credit exhaustion, followed by fresh owner authorization and revalidation of mutable Gemini quota/model/privacy assumptions.

Product plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

## M4 - New-infrastructure readiness

### M4.0 preflight - COMPLETE

Initial repository preflight found missing `ffmpeg`/`ffprobe` and `psql` in the final VoiceBridge runtime image.

### M4.1 image parity remediation - COMPLETE / ACCEPTED

Exact accepted evidence:

```text
VoiceBridge target commit: 6a9491359795840ec9e79c9edc0ea82f595e9784
Validate run: 33577022166
final image build: PASS
ffmpeg/ffprobe: PASS
psql: PASS
no-provider startup smoke: PASS
```

### M4.2 bounded owner-only canary - COMPLETE / ACCEPTED

```text
workflow run: 33580592224
result: SUCCESS
exact target temporarily live: 6a9491359795840ec9e79c9edc0ea82f595e9784
real STT fixture: public Telegram techcrimes/12107
provider: AssemblyAI universal-2
STT seconds: 53
retrieval credits: 0
provider cleanup: PASS
durable Neon readback: PASS
duplicate reuse: PASS
STT reservation rows for job: 1
invalid/private Telegram boundary: PASS
mandatory rollback: PASS
```

The isolated Render service was restored to exact pre-canary commit:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

### M4 post-canary state

```text
M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
```

## Current repository integration risk

Checkpoint 73 records the current KRC MEDIA branch as:

```text
PR #8: OPEN / DRAFT / UNMERGED / mergeable=false / dirty
branch vs main: diverged
ahead_by: 568
behind_by: 78
```

Therefore direct merge of PR #8 as-is is not the next action. R1 requires a dedicated integration/conflict strategy after R0 passes.

VoiceBridge PR #45 remains:

```text
OPEN / DRAFT / UNMERGED / mergeable=true
```

## Public KRC + MEDIA integration safety plan

Product plan:

`planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`

VoiceBridge technical plan:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

### R0 - Public KRC Update Safety Preflight

Status: REQUIRED NEXT / NO LIVE CHANGE.

Required evidence includes:

- current public KRC URL/identity and sharing/publication state;
- same existing GPT can still be edited by owner;
- a safe `Update` path exists without creating/publishing a new GPT;
- current OpenAI update/public-Action requirements are revalidated;
- Privacy Policy requirements/URL are satisfied;
- current GPT configuration is captured sufficiently for rollback/reconstruction;
- current Actions/knowledge/capabilities/instructions baseline is recorded;
- public KRC identity remains preserved.

If safe update of the existing published GPT cannot be verified without a new publication event, STOP.

### R1 - Repository integration

Status: HOLD until R0 PASS + explicit owner authorization.

Purpose: integrate selected MEDIA code/docs into the KRC repository while leaving the live published GPT untouched.

Required invariant:

```text
MEDIA failure/unavailability -> MEDIA unavailable
Core KRC -> remains usable
```

R1 must resolve current branch divergence/conflicts explicitly and pass Core + MEDIA regression tests. R1 does not authorize R2 or R3.

### R2 - Permanent MEDIA backend promotion/readiness

Status: HOLD / separate owner decision.

Before promotion, verify exact Render target/rollback, Neon durability, public-user admission/auth design, provider/quota policies, Cobalt-only Facebook behavior, no automatic paid fallback, and failure isolation from Core.

R2 does not authorize live GPT update.

### R3 - Update existing published KRC GPT

Status: HOLD / critical live-product gate.

```text
existing published KRC
  -> Edit
  -> Draft changes only
  -> add MEDIA additively
  -> Preview Core regression
  -> Preview MEDIA regression
  -> explicit owner authorization
  -> Update existing GPT
```

Do not create or depend on a new GPT publication event.

### R4 - Post-update public-access verification

Status: HOLD until R3.

Verify same public KRC URL, Core without MEDIA, MEDIA operation, MEDIA failure isolation, preserved sharing state, and rollback availability.

## Gate model

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Every gate is independent. Approval of one must never imply approval of the next.

## M5 - Provider/new-infrastructure cutover

Status: NOT_AUTHORIZED.

Gemini prerecorded remains inactive and Hybrid C/D remains deferred.

## Exact continuation point

```text
R0 PUBLIC KRC UPDATE SAFETY PREFLIGHT
NO LIVE GPT CHANGE
NO DIRECT MERGE OF CURRENT DIRTY PR #8
NO PERMANENT BACKEND PROMOTION / GPT UPDATE WITHOUT SEPARATE AUTHORIZATION
```
