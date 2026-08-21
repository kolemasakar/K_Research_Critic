# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 4.4
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-21

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_COMPLETE / A9_8_OWNER_ZERO_CLIENT_YOUTUBE_COMPLETE / A9_6_MULTI_PLATFORM_NEXT`

Current product target achieved for the first source adapter:

`PRIVATE OWNER-ONLY ZERO-CLIENT YOUTUBE MEDIA ANALYSIS = COMPLETE`

The public GPT, external tester rollout, merge to `main`, and production VoiceBridge remain outside the current gate.

## Repositories and isolation boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

Isolated beta runtime:
- service `voicebridge-krc-media-beta-kolemasakar`;
- service ID `srv-da1kic5bedkc73d6fk60`;
- endpoint `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`;
- auto-deploy false.

Do not merge PR #8 or PR #28 and do not target production without a separate explicit owner decision.

## Accepted owner UX

```text
public YouTube URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no beta-code prompt
 -> no manual Job ID
 -> managed credit preflight
 -> explicit user consent
 -> ChatGPT consequential-Action confirmation
 -> native transcript
 -> requested K-Research & Critic workflow
 -> result in same conversation
```

Current live-accepted zero-client source adapter:
`YouTube public prerecorded video`.

Planned but not accepted:
- Instagram public Reels/video posts;
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment.

Remote adapters remain public-only. Do not request platform login/password/cookies/session state/account tokens. Auth/private content must return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

## A8 browser-assisted baseline

Status: PASS / COMPLETE_BASELINE.

A8 Helper 0.2.2 / `KRCC_` remains emergency/dev fallback evidence only. It is not the normal owner UX.

Canonical record:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

## A9.1 - Server-side STT privacy parity

Status: PASS / COMPLETE.

AssemblyAI EU routing remains available for the accepted browser-assisted fallback path.

## A9.2 - Direct Render-to-YouTube

Status: BLOCKED / CLOSED AS PRIMARY STRATEGY.

Disposition:
`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`.

## A9.2R - Managed provider native route

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.

Provider: `Supadata`.
Mode: `native`.

Initial acceptance source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`.

Accepted transcript facts:
- detected language `ru`;
- 277 timestamped segments;
- one approved native credit;
- no Helper, YouTube cookies, login/session state or residential proxy;
- no automatic AI fallback.

Canonical record:
`26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`.

## Credit consent invariant

A billable managed transcript request must never start merely because a URL was pasted.

Required preflight:
- current available credits;
- estimated operation cost;
- estimated remaining balance;
- explicit `1 - Так / 2 - Ні`.

Only explicit `1` authorizes the quoted operation.

Current Supadata native hard cap:
`credit_consent.max_credits = 1`.

If native transcript is unavailable, stop at `AWAITING_AI_CONSENT`. Previous consent does not authorize managed AI generation. Any future AI fallback requires a separate preflight and second explicit consent.

## A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.

Accepted live code:
`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`.

Accepted durability proof:
- durable `KRCM_` job and timestamped segments before restart;
- same durable result after restart;
- duplicate start reused the same completed job while provider key was intentionally invalid;
- no duplicate valid provider call;
- provider balance changed only by the one approved request, `99 -> 98`;
- uncertain interrupted provider operations are not auto-replayed.

Canonical record:
`27_A9_DURABLE_MANAGED_ACCEPTANCE.md`.

## A9.5 - Private GPT Action integration

Status: PASS / COMPLETE.

### Backend / Action contract

Accepted VoiceBridge owner-auth implementation:
`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`.

The managed Action path:
- requires bearer authentication;
- injects owner beta admission server-side only after successful bearer auth;
- exposes no user-facing `beta_access_code`;
- preserves durable request keys, credit consent and idempotency;
- exposes managed preflight/start/status/segments operations;
- keeps automatic AI fallback disabled.

### Actual private GPT Builder

The actual `K-Research & Critic - MEDIA BETA` Custom GPT was updated on 2026-08-21:
- managed A9.5 OpenAPI schema imported;
- four managed operations visible;
- bearer API-key authentication preserved;
- zero-client Builder instructions installed;
- GPT remained private/owner-only.

Builder preflight from the actual GPT succeeded with:

```text
credits_available: 98
estimated_credits: 1
credits_after_estimate: 97
```

No transcript credit was spent by preflight.

### Actual private GPT zero-client E2E

Test source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`.

Mode:
`Перевірити факти/твердження`.

Observed end-to-end result:

```text
provider: Supadata
mode: native
source_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 98
provider_balance_after: 97
```

The GPT:
- requested no owner beta code, Helper, Job ID, cookies, platform login or provider key;
- obtained the transcript in the same chat;
- detected probable transcript uncertainty;
- built material claims with timestamps;
- produced a DRAFT CriticProfile and stopped for `1 / 2 / 3` approval;
- after owner approval, performed independent source research;
- produced the final fact-check report in the same chat;
- reported final fact-check `reliability_score: 0.91`;
- recorded actual managed transcript charge `1 credit`;
- ended `PASS / COMPLETED`.

The ChatGPT platform displayed its own `Allow` confirmation for the consequential external Action. This remained inside the same chat and did not require opening the video or exposing credentials.

Canonical E2E record:
`30_A9_5_PRIVATE_GPT_ZERO_CLIENT_E2E_ACCEPTANCE.md`.

## First zero-client source completion marker

`OWNER_ONLY_ZERO_CLIENT_YOUTUBE = COMPLETE`

This completion applies only to the accepted public prerecorded YouTube adapter and owner-only private GPT.

It does not authorize public rollout, external testers, production merge, automatic managed AI fallback, private/authenticated media, or other source adapters.

## Next task

`A9.6 - Validate additional public source adapters independently, preserving YouTube as the regression baseline.`

Recommended order:
1. Instagram public Reels/video posts;
2. Facebook public Video/Reels;
3. Telegram public video posts;
4. local upload as a separate A9.7 transport gate.
