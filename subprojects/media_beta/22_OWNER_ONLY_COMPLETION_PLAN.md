# MEDIA BETA Owner-Only Completion Plan

Version: 1.1
Status: COMPLETE_BASELINE / SUPERSEDED_BY_A9
Updated: 2026-08-20

## Decision

The owner paused GPT public/link sharing investigation and external Tester 1/2/3 rollout. The active product target remains private owner-only use with GPT access set to `Only me`.

This plan originally defined completion around the browser-assisted Helper flow. That baseline has now passed and is recorded in:

`subprojects/media_beta/23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`

The owner subsequently clarified that the final product target is zero-client media ingestion. Final product completion therefore moved to A9:

`subprojects/media_beta/24_A9_ZERO_CLIENT_INGESTION_PLAN.md`

## A8 result

Status: PASS / BASELINE COMPLETE.

Accepted private owner path:

```text
private GPT
 -> public YouTube URL
 -> owner-designated beta credential
 -> KRCC job
 -> Helper 0.2.2
 -> captions-first transcript
 -> complete transcript retrieval
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> independent Research
 -> Critic/revision
 -> localized final report
```

The accepted AssemblyAI Audio fallback remains routed through:

`https://api.eu.assemblyai.com`

The browser-assisted path remains a validated fallback/development baseline, but it is not the final normal UX.

## Final owner-only product target

The desired final flow is now:

```text
media input in ChatGPT
 -> zero-client ingestion
 -> transcript
 -> requested Research/Critic workflow
 -> result in the same conversation
```

Approved input directions:
- public media URLs through a platform-neutral `MediaSourceRouter`;
- initial public URL adapters: YouTube, Instagram, Facebook, Telegram;
- public sources only, with no user logins/cookies/sessions/tokens;
- local video/audio upload as a separate `local_upload` ingress mode.

Private/auth-required media must return:

`UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`

## Deferred items

The following remain outside the current completion boundary:
- public/link GPT sharing and appeal work;
- external tester rollout;
- Free-plan compatibility;
- public Store promotion;
- merge of KRC PR #8 or VoiceBridge PR #28 into production `main`.

## Canonical transition state

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_ZERO_CLIENT_MEDIA_ROUTER_PLANNED / A9_IMPLEMENTATION_NOT_STARTED`

Do not resume external sharing/tester rollout or production merge without a new explicit owner decision.
