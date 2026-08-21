# A9 Zero-Client Public Media URL and Local Upload Ingestion Plan

Version: 1.3
Status: IN_PROGRESS
Started: 2026-08-20
Updated: 2026-08-21

## Product goal

Final private owner-only UX:

```text
public media URL in ChatGPT
 -> analysis mode if missing
 -> no separate media opening
 -> no Helper
 -> no manual Job ID
 -> no beta-code prompt
 -> managed credit preflight when provider credits may be spent
 -> explicit user consent
 -> transcript acquisition
 -> K-Research & Critic workflow
 -> result in the same conversation
```

A future local-upload path should converge on the same normalized transcript/evidence contract.

## Public-only boundary

Remote source adapters support only public media. Do not request or store platform logins, passwords, cookies, authenticated sessions, account tokens or imported authenticated state.

If access requires authentication, return:

`UNSUPPORTED_PRIVATE_OR_AUTH_REQUIRED`

This restriction does not prevent a future owner-supplied `local_upload` path.

## Supported and planned source adapters

Live accepted for owner zero-client backend:
- YouTube public prerecorded video through managed native transcript provider.

Planned, not yet accepted:
- Instagram public Reels/video posts;
- Facebook public Video/Reels;
- Telegram public video posts;
- local audio/video attachment;
- other public platforms only after separate validation.

Support must be reported per adapter; do not imply universal platform support.

## Current normalized backend path

```text
public YouTube URL
 -> private Action bearer authentication
 -> server-side owner beta admission injection
 -> managed credit preflight
 -> explicit user approval
 -> Supadata native transcript
 -> durable KRCM_ job + timestamped segments in Postgres
 -> Action status/segment retrieval
 -> Research/Critic workflow
```

Current provider:
`Supadata`

Current mode:
`native`

Current native cost cap:
`1 credit`

Automatic managed AI fallback:
`DISABLED`

Native unavailability must stop at:
`AWAITING_AI_CONSENT`

Any future AI generation requires a new cost preflight and a second explicit user approval.

## Credit consent invariant

Before any billable managed transcript operation, the GPT must show actual preflight values:

```text
Доступно: N кредитів
Очікувана вартість: C кредитів
Після обробки залишиться: R кредитів

Продовжити?
1 - Так
2 - Ні
```

Only explicit option `1` authorizes the displayed operation. Option `2`, refusal or ambiguity means no billable transcript request.

For current Supadata native mode the backend additionally enforces:

`credit_consent.max_credits = 1`

## A9 implementation state

### A9.0 - Architecture audit

Status: COMPLETE.

The legacy server-side `KRCB_` path and the accepted browser-assisted `KRCC_` path were audited. The browser-assisted path remains a validated A8 fallback baseline only.

### A9.1 - Server-side AssemblyAI EU parity

Status: PASS / COMPLETE.

The server-side fallback path uses configurable `KRC_MEDIA_ASSEMBLYAI_BASE_URL`; isolated beta is configured for the accepted EU endpoint.

### A9.2 - Direct Render-to-YouTube probe

Status: BLOCKED / CLOSED AS PRIMARY STRATEGY.

A normal prerecorded public YouTube source returned the YouTube bot/login challenge from Render before metadata/captions/STT.

Disposition:

`DIRECT_RENDER_YOUTUBE = BLOCKED_BY_DATACENTER_ANTIBOT`

Blind yt-dlp player-client permutations are not the primary A9 route.

### A9.2R - Managed provider native route

Status: PASS / COMPLETE_FOR_NATIVE_OWNER_BETA.

Live acceptance source:
`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Accepted result:
- Supadata native transcript;
- detected language `ru`;
- 277 timestamped segments;
- exactly one approved credit;
- no Helper/cookies/platform login;
- no automatic AI fallback.

Canonical record:
`26_A9_MANAGED_PROVIDER_ACCEPTANCE.md`.

### A9.3 - Durable managed jobs and credit-safe idempotency

Status: PASS / COMPLETE.

Accepted live code:
`7736f2e7acc5abbb3415e3753d0ca022c1b8d7b2`

Accepted proof:
- durable `KRCM_` job and segments before restart;
- runtime restart;
- same job/segments after restart;
- duplicate start reused the same completed job while provider key was intentionally invalid;
- provider balance changed only by the one approved request, 99 -> 98;
- uncertain interrupted provider requests are not auto-replayed.

Canonical record:
`27_A9_DURABLE_MANAGED_ACCEPTANCE.md`.

### A9.5 - Private GPT Action integration

Status: PACKAGE_AND_BACKEND_PREFLIGHT_READY / PRIVATE_GPT_LIVE_CONFIG_PENDING.

VoiceBridge accepted implementation:
`970d7cc5819a623ec1d3cc7a70aceb44bfe311b9`

Backend live acceptance proved:
- bearer authentication remains mandatory;
- user beta access code is not required;
- owner beta admission is injected server-side only after bearer authentication;
- managed preflight works with URL + language hint only;
- health `ok`;
- Supadata/native estimated cost 1;
- credits available 98;
- estimated after 97;
- preflight spent zero transcript credits.

KRC private GPT package now contains:
- managed OpenAPI schema without user-facing `beta_access_code`;
- Builder instructions for zero-client flow;
- mandatory 1/2 credit gate;
- no visible `KRCM_` Job ID;
- no Helper in normal owner flow;
- no auto AI fallback;
- all transcript pages retrieved internally;
- fact-check CriticProfile gate preserved.

KRC Tests #545: SUCCESS.

Canonical record:
`28_A9_5_PRIVATE_GPT_ACTION_INTEGRATION.md`.

A9.5 is not complete until the actual private GPT Builder is updated and the owner runs a real private-GPT end-to-end acceptance.

### A9.6 - Multi-platform adapters

Status: NOT STARTED.

After YouTube private-GPT zero-client acceptance, validate adapters independently:
- Instagram;
- Facebook;
- Telegram;
- later public platforms only after separate compatibility proof.

Each adapter requires public positive case, auth/private negative case, normalized transcript metadata, and privacy/resource regression checks.

### A9.7 - Local upload

Status: ARCHITECTURE_APPROVED / TRANSPORT_NOT VALIDATED.

Target:

```text
local audio/video attachment
 -> validate type/size/duration
 -> embedded subtitle/text first
 -> otherwise temporary audio normalization
 -> accepted EU STT path when required
 -> normalized transcript
 -> delete temporary media
 -> same Research/Critic workflow
```

The ChatGPT attachment-to-Action/backend transport must be validated before this is marked supported.

### A9.8 - Owner-only final acceptance

Status: PENDING.

First accepted final test must occur from the actual private GPT:

```text
public YouTube URL
 -> no beta code
 -> no Helper
 -> no manual Job ID
 -> credit quote displayed
 -> explicit owner 1/2 decision
 -> if 1: transcript obtained
 -> requested analysis completed in same chat
```

For fact-check mode, CriticProfile approval remains mandatory before independent research.

## Final acceptance marker

Only after actual private-GPT end-to-end acceptance may the first source path be marked:

`OWNER_ONLY_ZERO_CLIENT_COMPLETE`

Additional platform adapters and `local_upload` receive separate acceptance markers.

## Non-goals for current A9 gate

A9 does not require:
- private/login-required platform media;
- user cookies or authenticated source sessions;
- external testers;
- public GPT publication;
- merge to `main`;
- automatic paid/AI fallback;
- visual-frame evidence extraction in the first local-upload path;
- permanent public free-media architecture.
