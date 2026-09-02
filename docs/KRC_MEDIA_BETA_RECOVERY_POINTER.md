# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик на актуальний checkpoint закритого MEDIA BETA з public Core.

Status: ACTIVE POINTER / PUBLIC CORE UNCHANGED
Updated: 2026-09-02

`K-Research & Critic - MEDIA BETA` is the closed-beta media module of the published `K-Research & Critic` product.

The public Core remains on `K_Research_Critic/main` and is not activated or functionally modified by MEDIA BETA runtime/provider work.

## Canonical current checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`agent/video-url-research`

Path:

`subprojects/media_beta/72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`

Recovery command:

`recover KRC MEDIA BETA checkpoint 72 M4 owner canary accepted rollback complete 2026-09-02`

## Current high-level state

```text
PUBLIC CORE                             PUBLISHED / MAINTENANCE
MEDIA BETA                              CLOSED BETA / RELEASE HOLD
KRC PRERECORDED ASSEMBLYAI              ACTIVE / universal-2
KRC GEMINI PRERECORDED                  IMPLEMENTED / INACTIVE
M3                                       CLOSED
FUTURE HYBRID C/D                        PLANNED / NOT IMPLEMENTED
HYBRID TRIGGER                           ASSEMBLYAI FREE CREDITS EXHAUSTED + FRESH OWNER GATE
M4 PREFLIGHT                             COMPLETE
M4 IMAGE PARITY                          PASS
M4 OWNER CANARY                          PASS
M4 REAL STT                              PASS
M4 DURABILITY / IDEMPOTENCY              PASS
M4 ROLLBACK                              PASS
M4 PERMANENT BACKEND PROMOTION           NOT AUTHORIZED
CURRENT MILESTONE                        OWNER POST-CANARY DECISION
PROVIDER CUTOVER                         NOT AUTHORIZED
R1/R2/R3/R4                              HOLD
```

VoiceBridge owner-canary authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

Exact canary evidence:

```text
M4 target: 6a9491359795840ec9e79c9edc0ea82f595e9784
workflow run: 33580592224
result: SUCCESS
real Telegram -> AssemblyAI STT: PASS
stt_seconds_charged: 53
retrieval credits: 0
provider cleanup: PASS
Neon durable readback: PASS
duplicate reuse / single reservation: PASS
rollback: PASS
restored Render commit: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The canary target was temporary and the isolated Render service was restored to its exact pre-canary commit. The one-shot workflow was removed after execution.

This pointer does not authorize permanent backend promotion, provider cutover, merge, external testers, public rollout, Gemini prerecorded activation, Hybrid C/D activation, or any change to the public KRC Builder/runtime.
