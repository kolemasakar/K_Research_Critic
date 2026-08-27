# MEDIA BETA Roadmap
Поточний roadmap приватного MEDIA BETA після завершення A9-A10.

Version: 3.6
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## Completed Historical Baseline

```text
A4-A7 closed-beta infrastructure and provider validation   COMPLETE/HISTORICAL
A8 browser-assisted owner baseline                        COMPLETE/FALLBACK_ONLY
```

The A8 Helper remains evidence/fallback only and is not normal owner UX.

## A9 Owner Zero-Client Media Input

Status: COMPLETE / ACCEPTED.

```text
YouTube managed route                       ACCEPTED
Instagram managed route                     ACCEPTED
Facebook free Cobalt route                  ACCEPTED
Facebook Cobalt failure -> unavailable      ACCEPTED
Telegram public route                       ACCEPTED
local attachment transport + ingestion      ACCEPTED
CriticProfile integration                   ACCEPTED
claim-level cross-check enforcement         ACCEPTED
```

## A9.10 Local Attachment

Status: COMPLETE / ACCEPTED.

Accepted flow:

```text
current-conversation audio/video attachment
 -> openaiFileIdRefs
 -> trusted OpenAI temporary delivery
 -> bounded ingestion
 -> AssemblyAI
 -> durable KRCM
 -> CriticProfile
 -> Research/Critic
```

Retrieval credits are zero. Accepted max attachment size is 32 MiB.

## A10 Stabilization

Status: COMPLETE / ACCEPTED.

Delivered:
- strict visible four-column claim-summary table;
- mandatory fenced copy-safe duplicate;
- runtime preservation of real SHORTFALL;
- external ChatGPT Copy defect documented rather than hidden.

Builder package: `0.9.1-beta-a10`.
Action schema: `0.6.0-a9.10`.

## Current Phase: Release Hold Owner Testing

Status: ACTIVE.

Canonical checkpoint:

```text
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Current decisions:

```text
merge to KRC main = HOLD
production VoiceBridge promotion = HOLD
external tester onboarding = HOLD
public sharing/Store rollout = HOLD
```

During this phase, only owner testing, defect correction, regression hardening, and documentation maintenance are in scope unless the owner explicitly changes direction.

## Future Release Gates

R1 Merge: accept feature code into `main`.
R2 Production promotion: deploy/promote media backend to production infrastructure.
R3 External testers: enable a controlled non-owner group.
R4 Public rollout: public sharing/Store availability.

Each requires a separate explicit decision. No gate inherits approval from another.

## Optional Future Sustainability Work

Cloudflare/local Whisper or other provider-neutral cost reductions remain a future optional architecture track. They are not a prerequisite for continued private owner testing and must not silently replace the accepted beta route.
