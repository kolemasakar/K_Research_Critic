# K-Research & Critic - MEDIA BETA
## Checkpoint 70 - M3 Closed / M4 Preflight Blocked on Image Parity

Date: 2026-09-02
Status: M3_CLOSED / RETAIN_ASSEMBLYAI / M4_PREFLIGHT_COMPLETE / CANARY_BLOCKED
Release state: RELEASE_HOLD_OWNER_TESTING

## Owner decision now recorded

The completed M3/M3B seven-case evidence did not establish a decisive global quality winner. The owner subsequently approved a deferred Hybrid C/D free-first plan for the future, but explicitly deferred implementation until AssemblyAI free credits are exhausted.

Therefore the current provider decision is closed as:

```text
M3_PROVIDER_EVIDENCE: COMPLETE
M3_CLOSURE: CLOSED
CURRENT KRC PRERECORDED PROVIDER: AssemblyAI universal-2
GEMINI PRERECORDED NORMAL ACTIVATION: FALSE
PROVIDER CUTOVER NOW: FALSE
FUTURE HYBRID C/D: PLANNED / NOT_IMPLEMENTED
FUTURE HYBRID TRIGGER: AssemblyAI free credits exhausted
```

Detailed future plan:

`69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

## Accepted M3 evidence retained

First tranche:

```text
cases: 3
AssemblyAI token-weighted WER: 3.23%
Gemini token-weighted WER: 6.45%
preference: ASSEMBLYAI_FOR_THIS_TRANCHE
```

Expanded M3B tranche:

```text
new cases: 4
provider results: SUCCESS 8/8
M3B lexical WER: TIE_FOR_THIS_TRANCHE
numeric sequence factual completeness: GEMINI_PREFERRED_FOR_THIS_FIXTURE
```

Seven-case synthesis:

```text
reviewed reference tokens: 117
AssemblyAI lexical WER: 13.68%
Gemini lexical WER: 14.53%
SEVEN_CASE_GLOBAL_WINNER: NOT_ESTABLISHED
```

The mixed evidence is not reinterpreted as a provider superiority claim.

## M4 repository-only preflight

A static deployment-image parity preflight was performed against the current VoiceBridge KRC migration branch.

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_DEPLOYMENT_IMAGE_PARITY_PREFLIGHT.md`

Preflight findings:

```text
KRC managed routes mounted in shared server: PASS_STATIC
KRC environment/configuration surface: PASS_STATIC
Node 24 runtime contract: PASS_STATIC
Facebook Cobalt HTTP transport: PASS_STATIC
Telegram public route: PASS_STATIC
local attachment image parity: FAIL
PostgreSQL/Neon persistence image parity: FAIL
```

Hard blockers:

```text
1. ffmpeg/ffprobe are required by the accepted local-attachment pipeline
   but are not installed in the current VoiceBridge runtime Docker image.

2. psql is required by the durable KRC PostgreSQL store
   but is not installed in the current VoiceBridge runtime Docker image.
```

Therefore:

```text
M4_PREFLIGHT: COMPLETE
M4_CANARY_READY: FALSE
M4_DEPLOYMENT: NOT_AUTHORIZED / NOT_PERFORMED
```

## Required next engineering step

Before an M4 canary can even be considered:

1. patch the VoiceBridge cloud runtime image with the minimum required media/PostgreSQL client packages;
2. add CI image-parity checks against the final runtime image;
3. prove `ffmpeg`, `ffprobe`, and `psql` are available in that final image;
4. perform a no-provider-call KRC route startup smoke check in the built image;
5. re-run VoiceBridge validation;
6. stop again at a separate owner deployment/canary authorization gate.

No Render, Neon, Action URL, Builder package, secrets, provider selector, or deployed backend was changed during this preflight.

## Active policy boundaries

```text
Facebook Cobalt fail -> unavailable
NO automatic paid fallback
Telegram public-only / zero retrieval credits
local attachment max 32 MiB / zero retrieval credits
AssemblyAI universal-2 remains active
Gemini prerecorded remains inactive for normal KRC jobs
R1 merge: HOLD
R2 backend promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
```

## Exact continuation point

```text
M4 IMAGE-PARITY REMEDIATION ON FEATURE BRANCH
NO DEPLOYMENT / NO CANARY WITHOUT NEW OWNER APPROVAL
```

Recovery command:

`recover KRC MEDIA BETA checkpoint 70 M3 closed M4 preflight blocked 2026-09-02`
