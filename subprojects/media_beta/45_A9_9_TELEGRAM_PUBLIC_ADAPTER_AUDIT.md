# A9.9 Telegram Public Video Adapter Audit
Аудит і фактичне приймання zero-client шляху для публічних Telegram video posts.

Status: BACKEND_LIVE_ACCEPTED / ACTION_PACKAGE_PENDING
Date: 2026-08-26
Scope: isolated KRC MEDIA BETA and VoiceBridge feature branches only

## Provider decision

### Cobalt

The upstream Cobalt supported-services list does not include Telegram.

Decision: DO NOT route Telegram through Cobalt.

### Supadata

Telegram is not declared as a supported social-platform URL in the project-approved Supadata transcript path.

Decision: DO NOT send a `t.me` post URL to Supadata as a supported social URL.

### yt-dlp

The current upstream yt-dlp tree contains a dedicated `TelegramEmbedIE` that uses the public Telegram embed surface.

VoiceBridge keeps yt-dlp only as compatibility/reference evidence for this path. The accepted A9.9 implementation uses a small native Node retriever so exact-post selection, host trust, timeout, size limits and zero-credit behavior remain explicit and regression-testable.

## Accepted public Telegram surface

Accepted input forms:

```text
https://t.me/<channel>/<post_id>
https://telegram.me/<channel>/<post_id>
https://t.me/s/<channel>/<post_id>
```

Normalization target:

```text
https://t.me/<channel>/<post_id>
```

The implementation rejects invite/login/share/non-post forms and does not use Telegram credentials, cookies, MTProto sessions, bot tokens or imported user sessions.

Retrieval flow:

```text
public Telegram post URL
 -> normalize and validate
 -> GET exact Telegram embed with embed=1&single=1
 -> verify exact data-post=<channel>/<post_id>
 -> select exact tgme_widget_message_video_player
 -> extract trusted Telegram CDN HTTPS MP4
 -> AssemblyAI EU STT
 -> durable KRCM job and timestamped segments
```

Observed live Telegram embed media host shape on 2026-08-26:

```text
cdn1.telesco.pe
cdn4.telesco.pe
```

The retriever therefore accepts `telesco.pe` and its subdomains, plus the previously supported `cdn-telegram.org` host family. Arbitrary external media origins remain rejected.

If the exact post is absent, private, login-required, removed or has no browser-playable video:

```text
TELEGRAM_MEDIA_UNAVAILABLE -> terminal FAILED -> STOP
```

No paid Telegram fallback exists in A9.9.

## Security boundary

The accepted retriever:
- fetches only normalized public Telegram embed URLs;
- requires the exact requested `data-post` and video-player href;
- accepts media only from trusted Telegram CDN HTTPS hosts;
- requires an MP4 path for this initial video adapter;
- never follows arbitrary links from message text as media;
- enforces preview timeout and maximum HTML size;
- rejects non-HTML preview responses;
- does not log full temporary media URLs in acceptance output;
- keeps Action bearer/provider credentials server-side;
- preserves AssemblyAI provider-data deletion behavior.

## Data model

Platform:

```text
telegram
```

Provider mode:

```text
telegram_public_retrieval_stt
```

Retrieval provider:

```text
telegram_public_web
```

Retrieval credit contract:

```text
retrieval_credits_charged = 0
credits_charged = 0
```

AssemblyAI STT seconds still count against the isolated MEDIA BETA STT quota.

## VoiceBridge implementation

VoiceBridge branch:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
```

Important implementation commits:

```text
25afbcd3903b9c4e589df16f74a3a9e392287457  Telegram URL normalization
0c43c21af8d5ada9c80768906a485b9976813c1e  Telegram public web retriever
41f7e69e73576b0c3cf6f3d757e81951bdf0372a  Telegram retriever regressions
4c985b10c946d6f89d1045cd01fabb7048db8931  durable managed Telegram HTTP/STT integration
7d58d09708550843f0accfc936ac1dc6c974b0f1  accept live telesco.pe CDN subdomains
c58210761a58c36ddef16cd120737fea034ae119  live-CDN regression coverage
```

Managed endpoint implemented in VoiceBridge:

```text
POST /api/v1/media/managed/telegram
```

The endpoint uses the same server-side owner admission as the existing managed beta and returns durable `KRCM_` jobs.

## Automated acceptance

After the live CDN host fix, VoiceBridge `Validate` passed all jobs:

```text
repository-docs: PASS
browser-extension: PASS
cloud build/tests: PASS
```

The Cobalt package validation also remained green, so A9.9 did not regress the Facebook free-first/no-automatic-paid-fallback contract.

## Live acceptance

First live attempt correctly exposed a real-world whitelist mismatch: Telegram returned media from `cdn4.telesco.pe`, while the initial retriever accepted only the exact `cdn.telesco.pe` host. The job stopped with `TELEGRAM_MEDIA_UNAVAILABLE`; retrieval credits remained zero and no paid provider was called.

A safe public-embed diagnostic confirmed the real Telegram host family and the code/test fix above was applied.

Final isolated live acceptance:

```text
workflow: A9.9 Telegram Live Acceptance
run: 32969713110
target: https://t.me/techcrimes/12107
Render service: srv-da1kic5bedkc73d6fk60
Render deploy: dep-da7dstgae00c73bi4p1g
deployed commit: 7daee7e751d5485f9bb65c5d7e4d0afd1920e2ec
job: KRCM_1599ca1f-8e3b-49ed-87ce-4f9ce1367dbb
result: PASS
```

Positive-path result:

```text
status: COMPLETED
provider: assemblyai
provider_mode: telegram_public_retrieval_stt
retrieval_provider: telegram_public_web
retrieval_credits_charged: 0
credits_charged: 0
stt_seconds_charged: 53
segment_count: 1
transcript_characters: 769
provider_data_deleted: true
reused: false
```

Durability/idempotency acceptance:

```text
status reread: PASS
segment reread: PASS / 1 segment
duplicate start: PASS / reused=true / same durable job
retrieval credits on duplicate: 0
```

Invalid/private boundary acceptance:

```text
invite-form input -> HTTP 400 / INVALID_REQUEST
```

Production VoiceBridge and both repositories' `main` branches were not changed by this live acceptance.

## A9.9 backend verdict

```text
URL normalization                 PASS
exact public post selection       PASS
trusted live Telegram CDN         PASS
zero retrieval credits            PASS
no paid Telegram fallback         PASS
AssemblyAI STT                     PASS
durable KRCM persistence           PASS
duplicate reuse                    PASS
provider-data deletion             PASS
invalid/private URL boundary       PASS
isolated Render deployment         PASS
production isolation               PASS

A9.9 TELEGRAM BACKEND LIVE         ACCEPTED
```

## Remaining package work

Backend acceptance does not by itself make Telegram available in the private GPT Action package.

Remaining work:
- add the Telegram endpoint and capability fields to the KRC managed OpenAPI Action schema;
- add Telegram routing to the compact Builder instructions;
- update media-beta manifest/validator state without changing public KRC;
- run KRC package CI;
- apply the updated package to the private MEDIA BETA GPT Builder;
- run a NEW-chat private-GPT Telegram E2E before declaring Telegram product-level live acceptance.

Until those steps pass, Telegram remains `in_progress` at the private-GPT product layer even though its isolated backend is live accepted.
