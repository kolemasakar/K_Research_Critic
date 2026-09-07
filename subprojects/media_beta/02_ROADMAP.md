# MEDIA BETA Roadmap

Поточний roadmap K-Research & Critic MEDIA BETA після live YouTube Gemini acceptance.

Version: 4.7
Status: R2_PARTIAL_PASS / YOUTUBE_LIVE_ACCEPTED / NON_YOUTUBE_AND_CORE_ISOLATION_PENDING / R3_HOLD
Updated: 2026-09-07

## Product position

`K-Research & Critic - MEDIA BETA` is a private owner-only validation surface for an additive MEDIA capability planned for the already-published `K-Research & Critic` GPT.

```text
product/release authority: kolemasakar/K_Research_Critic
public KRC: existing published GPT / unchanged
private MEDIA BETA GPT: owner-only
backend implementation: kolemasakar/VoiceBridge
VoiceBridge branch: agent/krc-media-gemini-migration
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains usable and accessible
```

## Canonical recovery authority

`86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md`

Recovery command:

`recover KRC MEDIA BETA checkpoint 86 YouTube Gemini live acceptance R3 readiness hold 2026-09-07`

## Current provider routing

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> durable KRCM/Neon
```

Policy:

```text
Supadata public: inactive
ScrapeCreators public paid retrieval: forbidden
paid retrieval fallback: false
paid STT fallback: false
paid proxy fallback: false
YouTube Cobalt fallback: none
YouTube AssemblyAI fallback: none
user cookies/login: forbidden
```

## R0 - Public KRC Update Safety Preflight

Status: PASS.

The existing public KRC identity was confirmed accessible/editable and its public Builder boundary remained unchanged during R2 recovery. No MEDIA Action is attached to public KRC.

## R1 - Repository integration

Status: COMPLETE.

KRC repository now contains the public MEDIA candidate Action, private canary package, privacy candidate, regression tests, and recovery documentation.

## R2 - Permanent MEDIA backend promotion/readiness

Status: PARTIAL PASS.

Completed:

```text
R2-A public free-tier admission: PASS
R2-B failure isolation/free quota: PASS
R2-C privacy/promotion preparation: COMPLETE
exact VoiceBridge Gemini-direct deployment: PASS
Render health/startup: PASS
private MEDIA BETA Builder activation: PASS
Action bearer auth: PASS
capability read: PASS
YouTube Gemini consent canary: PASS
YouTube durable completion: PASS
YouTube transcript retrieval: PASS
YouTube duplicate reuse/idempotency: PASS
YouTube no-paid/no-fallback boundary: PASS
```

Exact live backend:

```text
Render service: voicebridge-krc-media-beta-kolemasakar
branch: agent/krc-media-gemini-migration
autoDeploy: no
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
live deploy: dep-dafgkjm7bikc738hmi20
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac
```

Still required before full R2 PASS:

```text
1. bounded Instagram canary on current deployment
2. bounded Facebook canary on current deployment
3. bounded Telegram canary on current deployment
4. Render + Neon delta/no-paid-fallback verification for remaining routes
5. Core KRC isolation regression including forced MEDIA failure
```

## R3 - Update existing published KRC GPT

Status: HOLD / NOT READY.

R3 cannot start until full R2 PASS is recorded.

When R2 is complete, R3 remains a separate critical owner gate:

```text
existing published KRC
  -> Edit
  -> draft changes only
  -> add MEDIA additively
  -> Preview Core regression
  -> Preview MEDIA regression
  -> forced MEDIA failure / Core remains usable
  -> explicit owner authorization
  -> Update existing GPT
```

No current authorization exists to modify or update the public GPT.

## R4 - Post-update public verification

Status: HOLD until R3.

Required after any future R3 update:

- same public KRC identity/URL remains accessible;
- Core tasks work without MEDIA;
- MEDIA works only as intended;
- MEDIA failure does not degrade Core;
- sharing state remains intact;
- rollback remains available.

## Current gate model

```text
R0  PASS
R1  COMPLETE
R2  PARTIAL PASS / remaining non-YouTube canaries + Core isolation
R3  HOLD / NOT READY
R4  HOLD
```

Every gate remains independent. Approval of one does not imply approval of the next.

## Exact continuation point

```text
R2 REMAINING ACCEPTANCE
- Instagram
- Facebook
- Telegram
- Render/Neon delta + no-paid-fallback checks
- Core isolation regression

NO PUBLIC GPT CHANGE
NO PR #45 MERGE
```
