# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 4.3
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-21

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_BROWSER_ASSISTED_OWNER_BASELINE_COMPLETE / A9_IMPLEMENTATION_ACTIVE / A9_1_COMPLETE / A9_2_DIRECT_YOUTUBE_BLOCKED / A9_2R_MANAGED_NATIVE_COMPLETE / A9_3_DURABLE_MANAGED_COMPLETE / A9_5_PACKAGE_AND_BACKEND_PREFLIGHT_READY / A9_5_PRIVATE_GPT_LIVE_CONFIG_PENDING`

Current product target:

`PRIVATE OWNER-ONLY ZERO-CLIENT MEDIA ANALYSIS`

The public GPT, external tester rollout and production merge remain outside the current gate.

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

## Product contract

Final normal owner UX:

```text
public media URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no beta-code prompt
 -> no manual Job ID
 -> managed credit preflight
 -> explicit user consent
 -> transcript
 -> requested K-Research & Critic workflow
 -> result in same conversation
```

Current live-accepted zero-client source adapter:
`YouTube public prerecorded video`

Planned but not accepted:
- Instagram public Reels/video posts;
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment.

Public URL adapters must not request platform login/password/cookies/session state/account tokens. Auth/private content must return `UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`.

## A8 browser-assisted baseline

Status: PASS / COMPLETE_BASELINE.

A8 remains a proven emergency/dev fallback only:

```text
YouTube -> private GPT -> KRCC_ -> Helper 0.2.2
 -> captions-first or AssemblyAI EU audio fallback
 -> timestamped transcript
 -> Research/Critic workflow
```

It is not the normal A9 owner UX.

Canonical record:
`23_A8_OWNER_ONLY_BROWSER_ASSISTED_ACCEPTANCE.md`.

## A9.1 - Server-side STT privacy parity

Status: PASS / COMPLETE.

Server-side AssemblyAI routing uses configurable `KRC_MEDIA_ASSEMBLYAI_BASE_URL`; isolated beta retains the accepted EU endpoint `https://api.eu.assemblyai.com`.

## A9.2 - Direct Render-to-YouTube

Status: BLOCKED / CLOSED AS PRIMARY STRATEGY.

Normal prerecorded public YouTube acquisition from Render returned:

`Sign in to confirm you're not a bot`

Failure occurred before captions/STT.

Disposition:

`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`

## A9.2R - Managed provider native route

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.

Primary provider:
`Supadata`

Mode:
`native`

Accepted source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Accepted initial managed result:
- detected language `ru`;
- 277 timestamped segments;
- one approved credit;
- no Helper, YouTube cookies, login/session state or residential proxy;
- no automatic managed AI fallback.

Canonical record:
`26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`.

## Credit consent invariant

A managed billable transcript request must never start merely because a URL was pasted.

Required preflight:
- current available credits;
- estimated operation cost;
- estimated remaining balance;
- explicit `1 - Так / 2 - Ні`.

Only explicit `1` authorizes the displayed operation.

Current Supadata native hard cap:

`credit_consent.max_credits = 1`

If native transcript is unavailable, stop at `AWAITING_AI_CONSENT`. Previous consent does not authorize managed AI generation. Any future AI fallback requires a separate preflight and second explicit consent.

## A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.

Accepted live code:
`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`

Final acceptance:

```text
job_id: KRCM_6f359971-b061-4db8-b4a2-9f6422f351b6
status: COMPLETED
detected_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 99
provider_balance_after: 98
```

Proven:
- durable job and segments before restart;
- same durable result after restart;
- duplicate start reused same completed job while provider key was intentionally invalid;
- no duplicate valid provider call;
- valid provider key restored;
- uncertain interrupted provider operations are not auto-replayed.

Canonical record:
`27_A9_DURABLE_MANAGED_ACCEPTANCE.md`.

## A9.5 - Private GPT Action integration

Status: PACKAGE_AND_BACKEND_PREFLIGHT_READY / PRIVATE_GPT_LIVE_CONFIG_PENDING.

### VoiceBridge owner-auth change

CI-green implementation:
`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`

VoiceBridge Validate #278:
`32440143389` -> SUCCESS.

The managed HTTP layer now:
- requires private Action bearer authentication;
- rejects missing/invalid bearer before owner admission handling;
- after successful bearer authentication, injects the configured owner beta admission code server-side when the managed request does not include one;
- preserves the existing beta gate, durable access digest/request key, consent gate and idempotency contract.

Therefore the normal owner never supplies `OWNER_...` to the GPT.

### Live isolated A9.5 preflight

Run:
`32440430655`

Job:
`96649891795`

Result: SUCCESS.

Accepted live facts:

```text
live_code: 970d7cc5819a623ec1d3cc7a70aceb44bfe311b9
health: ok
user_beta_access_code_required: false
owner_access_injected_server_side: true
provider: supadata/native
credits_available: 98
estimated_credits: 1
credits_after_estimate: 97
transcript_endpoint_called: false
credits_spent: 0
```

The one-time A9.5 deploy/preflight workflow was removed after acceptance.

### KRC private GPT package

A9.5 package contains:
- managed OpenAPI schema `gpt_store/actions/media_managed_beta_openapi.yaml`;
- no user-facing `beta_access_code` field;
- Builder instructions for mandatory preflight + explicit 1/2 consent;
- no Helper in normal owner flow;
- no visible `KRCM_` Job ID;
- no automatic AI fallback;
- internal complete segment pagination;
- Ukrainian default;
- CriticProfile gate retained for fact-check mode.

KRC validator/package commit:
`cfb01afb44551519612994cf60918d6c822ffccc`

KRC Tests #545:
`32440399651` -> SUCCESS.

Canonical A9.5 checkpoint:
`28_A9_5_PRIVATE_GPT_ACTION_INTEGRATION.md`.

## Remaining blockers before first OWNER_ONLY_ZERO_CLIENT_COMPLETE

- update the actual private Custom GPT Builder instructions to the A9.5 package;
- replace its old client-assisted Action schema with the managed A9.5 schema while preserving bearer authentication;
- keep GPT private/owner-only;
- execute a fresh private-GPT preflight;
- show the user the actual quote and wait for explicit `1` before any billable native transcript;
- confirm no beta-code prompt, Helper, separate media opening or visible Job ID;
- retrieve transcript/status/segments internally;
- complete the requested analysis in the same private GPT conversation.

Additional public-platform adapters and local upload are later independent acceptance gates.

## Next task

`A9.5 - Update actual private GPT Builder and run owner zero-client E2E acceptance.`

No billable transcript acceptance may be started until a fresh preflight is shown and the owner explicitly replies `1`.
