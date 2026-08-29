# MEDIA BETA Current State
Поточний канонічний стан приватного MEDIA BETA для відновлення без реконструкції історії.

Version: 6.9
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-29

## Executive State

```text
A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
YOUTUBE_ACCEPTED
INSTAGRAM_ACCEPTED
FACEBOOK_COBALT_ACCEPTED
FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED
FACEBOOK_COBALT_ONLY_SERVER_HARDENING_ACCEPTED
TELEGRAM_ACCEPTED
LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
NEON_POSTGRESQL_18_CUTOVER_ACCEPTED
POST_CUTOVER_DURABILITY_REGRESSION_ACCEPTED
NEON_READ_ONLY_OBSERVATION_CHECKPOINT_ACCEPTED
NEON_OBSERVATION_EXIT_READINESS_ACCEPTED
NEON_ROLLBACK_OBSERVATION_CLOSED_OWNER_APPROVED
RELEASE_HOLD_OWNER_TESTING
```

A9/A9.10/A10 are accepted in the private owner runtime. The isolated MEDIA BETA durable store has completed the Render PostgreSQL -> Neon PostgreSQL 18 migration stream: cutover, owner-only post-cutover durability regression, later read-only observation, final exit-readiness verification, and owner-approved rollback-observation closure. A later owner-testing hardening also aligned the active Facebook server boundary with the already accepted Cobalt-only Builder policy. The owner continues private testing before release decisions.

## Repositories

KRC:

```text
repo: kolemasakar/K_Research_Critic
branch: agent/video-url-research
implementation baseline before documentation-only release-hold/audit updates: c8588ec1f13c3c576d3f307a001c1d8964b5128e
draft PR: #8
```

VoiceBridge:

```text
repo: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
Facebook Cobalt-only live-hardening acceptance head at 2026-08-29 sync: 65d536a445126c47f2646e59ca31e12e7bd35514
draft PR: #28
```

Use live branch heads as authority after later documentation/regression commits.

## Isolated Runtime

```text
private GPT: K-Research & Critic - MEDIA BETA
beta service: voicebridge-krc-media-beta-kolemasakar
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
```

## Durable Store State

Active durable store:

```text
provider: Neon PostgreSQL
PostgreSQL major: 18
project: krc-media-beta-neon
database: krc_media_beta
region: AWS Europe Central 1 (Frankfurt)
connection mode: direct TLS
```

The isolated Render service still owns the MEDIA BETA application runtime. Only its protected `KRC_MEDIA_DATABASE_URL` target was changed during the approved cutover.

Original Render PostgreSQL:

```text
original Render PostgreSQL: voicebridge-krc-media-beta-db
state: retained intact after observation closure
source database deletion: NOT AUTHORIZED
```

Verified migration checkpoints in VoiceBridge:

```text
docs/KRC_MEDIA_NEON_MIGRATION_PLAN.md
docs/history/KRC_MEDIA_NEON_RESTORE_VERIFY_2026-08-29.md
docs/history/KRC_MEDIA_NEON_PRECUTOVER_VERIFY_2026-08-29.md
docs/history/KRC_MEDIA_NEON_CUTOVER_2026-08-29.md
docs/history/KRC_MEDIA_NEON_POSTCUTOVER_LIVE_REGRESSION_2026-08-29.md
docs/history/KRC_MEDIA_NEON_OBSERVATION_WINDOW_2026-08-29.md
docs/history/KRC_MEDIA_NEON_OBSERVATION_CHECKPOINT_2026-08-29.md
docs/history/KRC_MEDIA_NEON_OBSERVATION_EXIT_READINESS_2026-08-29.md
docs/history/KRC_MEDIA_NEON_OBSERVATION_CLOSURE_2026-08-29.md
```

Post-cutover owner-only live regression accepted:
- one Supadata native provider start;
- one provider credit charged;
- durable Neon write PASS;
- API job/segment read before restart PASS;
- exact-head Render restart PASS;
- API read after restart PASS;
- idempotent replay PASS;
- duplicate provider start not observed;
- paid Facebook fallback/ScrapeCreators not used.

Later read-only observation checkpoint accepted:
- isolated Render service still targets protected Neon direct TLS: PASS;
- managed capability after inactivity/resume: PASS;
- PostgreSQL major 18: PASS;
- non-terminal managed jobs: 0;
- accepted regression job remains COMPLETED and readable: PASS;
- accepted persisted regression segments remain readable: PASS;
- provider-consuming work: NONE;
- rollback trigger observed: NO.

Final observation exit readiness accepted:
- current Render target remains Neon: PASS;
- original Render PostgreSQL rollback source recoverable: PASS;
- managed capability: PASS;
- Neon durable state stable: PASS;
- provider-consuming work: NONE;
- environment/database mutation: NONE.

The owner approved closure of the rollback observation window. Neon remains the active durable store. The original Render PostgreSQL database remains retained; its deletion is still separately gated and not authorized. The database migration stream is complete, but RELEASE_HOLD_OWNER_TESTING remains active.

## Accepted Inputs

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel
supported public Telegram video post
one local current-conversation audio/video attachment
```

## Route Invariants

YouTube/Instagram: managed transcript route; billable work remains consent-gated.

Facebook: free Cobalt retrieval only. Success may continue to AssemblyAI/KRCM. Failure is unavailable/STOP. ScrapeCreators is unconfigured/inactive/reserve-only and not offerable. The isolated live HTTP boundary now additionally rejects Facebook on generic Supadata native preflight/start before provider invocation, and managed capability no longer advertises Facebook AI generation as active. The dedicated Cobalt route is unchanged. Historical compatibility internals remain outside the active Builder path.

Telegram: public web/embed only, trusted media delivery, AssemblyAI/KRCM, zero retrieval credits, no auth/session/bot token/paid fallback.

Local attachment: `openaiFileIdRefs`, trusted OpenAI delivery, max 32 MiB, AssemblyAI/KRCM, zero retrieval credits, no user-visible file token.

## Facebook Cobalt-Only Server Hardening

Accepted owner-testing hardening record in VoiceBridge:

```text
docs/history/KRC_MEDIA_FACEBOOK_COBALT_ONLY_HARDENING_2026-08-29.md
```

Verified:
- generic Facebook Supadata preflight blocked at HTTP boundary: PASS;
- generic Facebook Supadata transcript start blocked at HTTP boundary: PASS;
- capability `facebook_ai_fallback = false`: PASS;
- capability `facebook_ai_requires_duration_metadata = false`: PASS;
- capability `facebook_ai_metadata_credits = 0`: PASS;
- active Facebook retrieval/STT capability preserved: PASS;
- automatic paid Facebook retrieval remains false: PASS;
- full VoiceBridge cloud suite after hardening: 134/134 PASS;
- isolated live no-provider-spend smoke: PASS;
- Facebook retrieval endpoint called by smoke: NO;
- Supadata/AssemblyAI credits consumed by smoke: NO;
- Render environment mutation: NONE;
- Neon data mutation: NONE.

This hardening is defense in depth. It does not indicate that the accepted Builder had previously used the forbidden generic Facebook Supadata route; Builder policy already selected the dedicated Cobalt route.

## Research/Critic Invariants

- no independent research before profile approval;
- two-stage profile gate remains accepted;
- option `1` approves the current profile and starts research;
- material edits require re-approval;
- risk floors: LOW 0, MEDIUM 1, HIGH 2, CRITICAL 3;
- each material factual claim tracks required/achieved/exception;
- evidence independence is based on origins, not URL count;
- achieved cannot exceed visible traceable origins;
- unresolved shortage is SHORTFALL and qualifies final status.

## A10 State

Runtime accepted:
- visible four-column claim-summary table;
- copy-safe fenced duplicate with literal pipe delimiters;
- row values identical between forms;
- real SHORTFALL preserved.

The ordinary rendered table header may still be corrupted by ChatGPT whole-response Copy. This is an accepted external UI limitation; the fenced duplicate is the mitigation.

## Current Release Decision

```text
merge KRC feature branch to main = HOLD
merge VoiceBridge PR #28 = HOLD
production VoiceBridge promotion = HOLD
external tester onboarding = HOLD
public sharing / Store rollout = HOLD
original Render PostgreSQL deletion = HOLD
```

Canonical release-hold record:

```text
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Project/documentation audit record:

```text
54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
```

## Current Work Rule

Owner testing may continue. The Render PostgreSQL -> Neon migration stream and rollback observation window are closed with Neon as the active durable store. The active Facebook server boundary is now hardened to the accepted Cobalt-only policy. Confirmed defects should be fixed only in the owning isolated feature branch and revalidated there. Do not delete the original Render PostgreSQL database, merge either MEDIA branch, change public Core, promote production infrastructure, onboard external testers, or activate paid Facebook/ScrapeCreators behavior unless the owner explicitly opens the corresponding gate.

No additional A10 Builder remediation is pending.
