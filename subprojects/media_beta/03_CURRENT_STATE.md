# MEDIA BETA Current State
Поточний канонічний стан приватного MEDIA BETA для відновлення без реконструкції історії.

Version: 6.5
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## Executive State

```text
A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
YOUTUBE_ACCEPTED
INSTAGRAM_ACCEPTED
FACEBOOK_COBALT_ACCEPTED
FACEBOOK_FAILURE_POLICY_E2E_ACCEPTED
TELEGRAM_ACCEPTED
LOCAL_ATTACHMENT_PRIVATE_GPT_E2E_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
RELEASE_HOLD_OWNER_TESTING
```

A9/A9.10/A10 are accepted in the private owner runtime. The owner has chosen an extended private testing period before release decisions.

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
implementation head at audit start: 20afd2e54b87b4a2a8858961a03e22f78a565189
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

Facebook: free Cobalt retrieval only. Success may continue to AssemblyAI/KRCM. Failure is unavailable/STOP. ScrapeCreators is unconfigured/inactive/reserve-only and not offerable.

Telegram: public web/embed only, trusted media delivery, AssemblyAI/KRCM, zero retrieval credits, no auth/session/bot token/paid fallback.

Local attachment: `openaiFileIdRefs`, trusted OpenAI delivery, max 32 MiB, AssemblyAI/KRCM, zero retrieval credits, no user-visible file token.

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
production VoiceBridge promotion = HOLD
external tester onboarding = HOLD
public sharing / Store rollout = HOLD
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

Owner testing may continue. Confirmed defects should be fixed only in the owning isolated feature branch and revalidated there. Do not change public Core or production infrastructure unless the owner explicitly opens a release gate.

No additional A10 Builder remediation is pending.
