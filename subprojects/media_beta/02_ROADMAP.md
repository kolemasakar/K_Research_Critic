# MEDIA BETA Roadmap
Поточний roadmap приватного K-Research & Critic MEDIA BETA.

Version: 4.3
Status: RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_IMAGE_PARITY_READY / OWNER_CANARY_DECISION
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

VoiceBridge final runtime image now installs the required media and PostgreSQL client tooling.

Exact acceptance:

```text
VoiceBridge commit: 6a9491359795840ec9e79c9edc0ea82f595e9784
Validate run: 33577022166
krc-image-parity: SUCCESS
cloud: SUCCESS
browser-extension: SUCCESS
repository-docs: SUCCESS
```

CI proves:

```text
final image builds: PASS
ffmpeg available/working: PASS
ffprobe available/working: PASS
psql available/working: PASS
no-provider KRC startup smoke: PASS
```

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

### M4.2 owner deployment/canary - OWNER DECISION REQUIRED

No external deployment has occurred.

Before canary execution, revalidate the exact target Render service, branch/commit, environment configuration, Neon connectivity, Cobalt health, AssemblyAI operating state, Action compatibility, and rollback target.

Then owner must explicitly authorize the exact deployment/canary scope.

## M5 - Provider/new-infrastructure cutover

Status: NOT_AUTHORIZED.

M5 is not implied by M4 image readiness or an eventual owner-only canary.

## Release hold

```text
R1 merge selected MEDIA BETA work toward main   HOLD
R2 backend/production promotion                 HOLD unless separately scoped for owner canary
R3 external testers                             HOLD
R4 public sharing / Store rollout               HOLD
```

## Current checkpoint

`71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md`

## Exact continuation point

```text
M4.2 OWNER DEPLOYMENT/CANARY DECISION
NO EXTERNAL DEPLOYMENT WITHOUT EXPLICIT APPROVAL
```
