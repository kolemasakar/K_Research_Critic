# K-Research & Critic MEDIA BETA
Короткий вступ до поточного приватного MEDIA BETA та його release-hold меж.

Version: 2.0
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## Purpose

MEDIA BETA is the isolated owner-only zero-client media-input path for K-Research & Critic. It is additive to the public text Core and does not replace or weaken the normal CriticProfile -> Research -> Critic workflow.

## Accepted Owner Inputs

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel
supported public Telegram video post
one current-conversation local audio/video attachment
```

A9 owner media input, A9.10 local attachment, and A10 copy-safe output stabilization are runtime accepted for the private owner GPT.

## Normal Flow

```text
supported media input
 -> private GPT Action
 -> isolated VoiceBridge MEDIA BETA
 -> durable KRCM transcript
 -> CriticProfile gate
 -> explicit owner approval
 -> Research
 -> Critic
 -> localized final report
```

The transcript proves what the media said, not that its claims are true.

## Critical Route Policies

Facebook:

```text
Cobalt success -> AssemblyAI -> durable KRCM
Cobalt failure -> unavailable -> STOP
paid fallback -> inactive/not offerable
```

Telegram:

```text
public web/embed -> trusted Telegram CDN -> AssemblyAI -> durable KRCM
retrieval credits = 0
no login/cookies/session/bot token/paid fallback
```

Local attachment:

```text
openaiFileIdRefs -> trusted OpenAI temporary delivery -> AssemblyAI -> durable KRCM
max attachment = 32 MiB
retrieval credits = 0
```

## Package State

```text
Builder package = 0.9.1-beta-a10
Action schema = 0.6.0-a9.10
Builder runtime applied = true
```

The accepted package remains frozen during the owner-testing hold unless a real defect requires a validated change.

## Release Hold

```text
merge to main = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

No release gate is implied by another.

## Read First

```text
00_INDEX.md
03_CURRENT_STATE.md
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
```

Then use the architecture, roadmap, runbook, test plan, and decision log in this directory.

Historical numbered phase/acceptance records remain evidence and must not override later accepted current-state records.
