# MEDIA BETA Roadmap
Поточний roadmap приватного K-Research & Critic MEDIA BETA.

Version: 4.4
Status: RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED / R1_R2_HOLD
Updated: 2026-09-02

## Product position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main
closed-beta product branch: agent/video-url-research
technology/backend implementation source: kolemasakar/VoiceBridge
KRC media migration branch: agent/krc-media-gemini-migration
```

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

The owner explicitly authorized a temporary live canary on the isolated MEDIA BETA Render service.

Canary evidence:

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

### M4 post-canary gate

The canary is acceptance evidence only. It does not permanently promote the M4 target.

```text
M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
```

The next owner decision must keep repository integration and backend promotion separate:

```text
R1: merge selected MEDIA BETA work toward main - separate decision
R2: permanently promote tested backend target - separate decision
```

Before either gate, reverify current heads/CI, exact diffs/scope, current Render live baseline, rollback target, environment state, Neon connectivity, and release-hold invariants.

## M5 - Provider/new-infrastructure cutover

Status: NOT_AUTHORIZED.

M5 is not implied by M4 canary acceptance. Gemini prerecorded remains inactive and Hybrid C/D remains deferred.

## Release hold

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 backend/production promotion                 HOLD
R3 external testers                             HOLD
R4 public sharing / Store rollout               HOLD
```

## Current checkpoint

`72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`

## Exact continuation point

```text
OWNER POST-CANARY DECISION
R1 MERGE AND R2 BACKEND PROMOTION REMAIN SEPARATE GATES
```
