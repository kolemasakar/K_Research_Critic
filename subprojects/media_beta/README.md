# K-Research & Critic MEDIA BETA
Короткий вступ до поточного приватного MEDIA BETA, його місця в K-Research & Critic та release-hold меж.

Version: 2.1
Status: RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Updated: 2026-09-01

## Purpose

MEDIA BETA is the isolated owner-only zero-client media-input module of the published `K-Research & Critic` product. It is additive to the public text Core and does not replace or weaken the normal CriticProfile -> Research -> Critic workflow.

Product boundary:

```text
K-Research & Critic                    published parent product
K_Research_Critic/main                 public Core authority
K-Research & Critic - MEDIA BETA       closed-beta module
VoiceBridge                            media/backend technology source
```

VoiceBridge implementation work does not independently authorize a KRC product release or public-Core change.

## Accepted Owner Inputs

```text
prerecorded YouTube
Instagram Reel
public Facebook Video/Reel
supported public Telegram video post
one current-conversation local audio/video attachment
```

A9 owner media input, A9.10 local attachment, and A10 copy-safe output stabilization are runtime accepted for the private owner GPT.

## Normal Accepted Runtime Flow

```text
supported media input
 -> private GPT Action
 -> isolated VoiceBridge MEDIA BETA runtime
 -> durable KRCM transcript
 -> CriticProfile gate
 -> explicit owner approval
 -> Research
 -> Critic
 -> localized final report
```

The transcript proves what the media said, not that its claims are true.

## Active Engineering Track

The accepted private runtime remains on release hold while prerecorded STT/provider migration work proceeds separately in VoiceBridge branch `agent/krc-media-gemini-migration`.

Current milestone:

```text
M0 preflight                         COMPLETE
M1 provider abstraction              PASS
M2 Gemini prerecorded adapter        PASS / INACTIVE
M3 evidence/A-B gate                 ACTIVE
first public source tranche          LOCKED
READY_FOR_AB                         FALSE
M3 live A/B                          NOT_RUN
NEXT                                 M3 BYTE CAPTURE + SHA-256
```

AssemblyAI `universal-2` remains the active KRC prerecorded provider. Gemini prerecorded is an inactive candidate.

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

Accepted private runtime baseline:

```text
Builder package = 0.9.1-beta-a10
Action schema = 0.6.0-a9.10
Builder runtime applied = true
```

The accepted package remains frozen during the owner-testing hold unless a real defect requires a validated change or a separately approved migration gate is reached.

## Release Hold

```text
merge to main = HOLD
production/backend promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

No release gate is implied by another, and M3 technical work does not change these hold decisions.

## Read First

```text
00_INDEX.md
60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
03_CURRENT_STATE.md
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
02_ROADMAP.md
```

Then use the architecture, runbook, test plan, and decision log in this directory.

Historical numbered phase/acceptance records remain evidence and must not override later accepted current-state records.
