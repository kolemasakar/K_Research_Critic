# MEDIA_BETA_RUNBOOK
Інструкція оператора для поточної owner-only zero-client MEDIA BETA без зміни public Core або production VoiceBridge.

Version: 0.9-a9.9
Status: CLOSED_BETA_OWNER_ONLY
Date: 2026-08-26

## 1. Authority and isolation

K-Research & Critic public Core remains on:

```text
repository: kolemasakar/K_Research_Critic
branch: main
```

Closed MEDIA BETA package remains on:

```text
repository: kolemasakar/K_Research_Critic
branch: agent/video-url-research
PR: 8
```

VoiceBridge MEDIA backend remains on:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
```

Dedicated MEDIA BETA endpoint:

```text
https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

Do not deploy MEDIA BETA over the existing production VoiceBridge service. Do not merge the private MEDIA package into public Core merely because CI or isolated backend acceptance is green.

## 2. Current owner-only model

The normal MEDIA flow is zero-client:

```text
public media URL
-> private GPT Action
-> dedicated MEDIA BETA backend
-> durable KRCM job
-> transcript segments
-> K-Research & Critic workflow
```

The owner must not be asked for:

```text
beta access code
provider API key
Telegram login or cookies
browser session
Helper
KRCM job id
```

Action bearer authentication, owner admission, and provider credentials remain server-side.

External tester rollout is paused. The current intended tester count is one owner.

## 3. Current platform state

Live accepted in the current private GPT runtime:

```text
YouTube
Instagram Reel
Facebook Video/Reel free path
```

Telegram state at A9.9:

```text
backend implementation: PASS
isolated live backend E2E: PASS
retrieval provider: telegram_public_web
retrieval credits: 0
STT provider: AssemblyAI
Action package: READY
Builder runtime application: PENDING
private GPT Telegram NEW-chat E2E: PENDING
```

Telegram remains `in_progress` until the Builder package is applied and owner NEW-chat E2E is accepted.

## 4. Facebook safety contract

Active Facebook path:

```text
Facebook public media
-> Cobalt free retrieval
-> AssemblyAI STT
-> durable KRCM
```

Required behavior:

```text
Cobalt success -> continue
Cobalt fail -> unavailable
automatic paid fallback -> forbidden
paid offer after Cobalt fail -> forbidden
ScrapeCreators -> reserved/unconfigured/unaccepted
```

Do not call the reserved paid Facebook continuation operations in the active MEDIA BETA flow.

## 5. Telegram safety contract

Supported path:

```text
public Telegram post URL
-> public Telegram embed surface
-> trusted Telegram CDN media
-> AssemblyAI EU STT
-> durable KRCM
```

Required behavior:

```text
retrieval credits: 0
Telegram login: forbidden
cookies/session: forbidden
bot token: not required
paid Telegram fallback: none
automatic retry after terminal unavailable: forbidden
```

Only trusted Telegram media-host families accepted by the backend may be followed. Arbitrary external media hosts remain forbidden.

## 6. Private GPT Builder package

Use a separate private GPT:

```text
Name:
K-Research & Critic - MEDIA BETA

Builder instructions:
prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md

Canonical reference:
prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md

Action schema:
gpt_store/actions/media_managed_beta_openapi.yaml

Action schema version:
0.5.0-a9.9
```

Enable:

```text
Web search
Code Interpreter & Data Analysis
Actions
```

Keep disabled:

```text
Apps
Image generation
```

Action authentication:

```text
type: API key / bearer
value: KRC_MEDIA_ACTION_TOKEN configured on the dedicated MEDIA BETA service
```

Do not expose the bearer secret in chat, repository content, screenshots, checkpoints, or acceptance evidence.

## 7. Builder instruction invariants

The active Builder package must remain within 8000 characters and preserve:

```text
report-language invariant
CriticProfile approval gate
claim-level cross-check ledger
traceable independent evidence counting
no hidden Job IDs
native Supadata credit consent gate
separate Instagram AI consent gate
Facebook Cobalt fail -> unavailable
no automatic or offered paid Facebook fallback
Telegram public-video routing
no Telegram login/cookies/session
no paid Telegram fallback
```

## 8. A9.9 package state

Repository package state:

```text
instructions version: 0.8-beta-a9.9
Builder package version: 0.8-beta-a9.9
Action schema version: 0.5.0-a9.9
rollout state: A9_9_TELEGRAM_PACKAGE_READY_BUILDER_PENDING
Builder package ready: true
Builder runtime applied: false
Telegram backend complete: true
Telegram Action package complete: true
Telegram private GPT E2E complete: false
```

The committed Builder instruction package is below the 8000-character limit and repository/package validation is green.

## 9. Mandatory next acceptance gate

Apply the A9.9 Builder package to the existing private owner-only MEDIA GPT, then open a NEW chat and run a public Telegram video request.

Acceptance requires:

```text
private GPT selects startManagedTelegramPublicTranscription
no credit preflight is shown for Telegram retrieval
no Telegram login/cookies/session request appears
backend returns COMPLETED for a supported public Telegram video
all transcript pages are retrieved
KRCM job id remains hidden from the user
retrieval provider is telegram_public_web
retrieval credits charged is 0
paid fallback is not offered or called
fact-check/research workflow still obeys CriticProfile approval gate
final report follows report-language and cross-check traceability rules
```

If Telegram media is unavailable, the private GPT must report unavailable and stop media intake for that URL. It must not improvise a paid fallback.

## 10. Post-acceptance state update

Only after successful owner NEW-chat Telegram E2E may the repository state move to Telegram accepted. The acceptance update must set the authoritative state consistently across manifest, validator, tests, and acceptance evidence.

Expected target state after actual acceptance:

```text
public_platforms_live_accepted includes telegram
public_platforms_in_progress is empty
managed_telegram_builder_runtime_applied: true
managed_telegram_private_gpt_e2e_complete: true
a9_9_telegram_builder_runtime_applied: true
a9_9_telegram_private_gpt_e2e_complete: true
gpt_builder_private_update_required: false
```

Do not set these markers before the real private GPT UI acceptance occurs.

## 11. Regression requirements

Before and after Builder acceptance keep these green:

```text
Python 3.13 tests
Python 3.14 tests
repository policy validation
GPT Store package validation
ruff correctness checks
mypy boundary checks
coverage gate
```

Public `main`, public Store GPT, and production VoiceBridge must remain unchanged by A9.9 acceptance work.

## 12. Stop / rollback

If the private MEDIA GPT package behaves incorrectly:

```text
private GPT -> restore the last accepted A9.7-I Builder instructions and Action schema
MEDIA branch -> retain A9.9 package for diagnosis
public Core -> no rollback required
production VoiceBridge -> no rollback required
```

Do not use a production deployment as a rollback mechanism for an isolated private-GPT package problem.
