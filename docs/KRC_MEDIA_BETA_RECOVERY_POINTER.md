# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик на поточний стан MEDIA BETA після live R2 Render promotion та часткового bounded canary.

Status: ACTIVE POINTER / R2 LIVE PROMOTED / CANARY PARTIAL / MANUAL MEDIA CANARY REQUIRED / R3 HOLD
Updated: 2026-09-04

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md`

## Current gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   LIVE PROMOTED / CANARY PARTIAL
R3   HOLD
R4   HOLD
```

## Current live backend

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live deploy: dep-dadf9t6kb8uc7399jmc0
live commit: 3a00d67bac0883a55f0f9c5eacf16e11acae85fe
status: live
rollback target: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
autoDeploy: no
configured branch: agent/krc-media-transcript
```

Before promotion, `archive/krc-media-transcript-pre-r2-20260904` was created at the previous configured branch head `a0d1d5a380d0d90a42510c3b28f6221385578d52`.

## Active free-only policy

```text
KRC_MEDIA_PUBLIC_MODE=true
KRC_MEDIA_FREE_TIER_ONLY=true
KRC_MEDIA_ASSEMBLYAI_FREE_TRIAL_ONLY=true
KRC_MEDIA_STT_PROVIDER=assemblyai
KRC_MEDIA_TRANSCRIBE_MODEL=gemini-3.5-transcribe
MEDIA_DAILY_STT_SECONDS=7200
MEDIA_MAX_CONCURRENT_JOBS=1
RATE_LIMIT_REQUESTS_PER_MINUTE=60
ScrapeCreators paid fallback disabled
```

AssemblyAI remains the active KRC prerecorded provider while its Free credit remains. After exhaustion, the product target is Gemini prerecorded STT, but the automatic runtime cutover is not yet implemented.

## Promotion validation completed

```text
exact candidate identity        PASS
Render build/deploy             PASS
runtime process start           PASS
free-only policy env            APPLIED
Neon schema/connectivity        PASS
post-start runtime error scan   PASS
rollback identity               PRESERVED
```

Post-promotion Neon read-only state:

```text
database: krc_media_beta
schema: public
expected MEDIA tables: 3
managed_jobs: 2
client_jobs: 0
stt_seconds_today: 0
```

## Remaining R2 canary

Before R2 can be called complete, use the existing private `K-Research & Critic - MEDIA BETA` GPT to run authenticated bounded canaries for:

```text
YouTube
Telegram
Instagram
Facebook
```

Then confirm:

- successful Action authentication without exposing credentials;
- provider/quota failure remains MEDIA-only and fail-closed;
- no paid fallback;
- Core KRC remains usable;
- no secret/transcript leakage in runtime logs.

## Administrative cleanup

An unrelated temporary Render service `noop` (`srv-dadf9am1egvs73d7ktj0`) was accidentally created during connector capability discovery. It is not referenced by KRC routing and does not affect the production MEDIA endpoint. The current Render connector has no delete-service operation, so it requires manual deletion in the Render Dashboard.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains usable
```

R3 remains a separate owner gate. No ChatGPT Builder update or public KRC configuration change occurred during R2 promotion.

Recovery must start from checkpoint 81.
