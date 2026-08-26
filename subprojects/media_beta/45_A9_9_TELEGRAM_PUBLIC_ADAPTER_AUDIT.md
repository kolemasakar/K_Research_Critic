# A9.9 Telegram Public Video Adapter Audit
Аудит поточного коду і мінімального zero-client шляху для публічних Telegram video posts.

Status: AUDIT_COMPLETE / IMPLEMENTATION_READY
Date: 2026-08-26
Scope: isolated KRC MEDIA BETA and VoiceBridge feature branches only

## Current repository state

VoiceBridge `agent/krc-media-transcript` has no Telegram adapter, Telegram-specific source module, or Telegram-specific regression tests.

The current managed URL boundary is explicitly limited to:
- YouTube;
- Instagram;
- Facebook.

`ManagedMediaPlatform` currently contains only `youtube | instagram | facebook` and unsupported URLs return `MEDIA_URL_UNSUPPORTED`.

The existing durable managed-media service is reusable for a Telegram adapter, but its current job view/provider-mode types are platform-specific enough that Telegram must be added deliberately rather than passed through the existing Supadata native route.

## Provider audit

### Cobalt

The current upstream Cobalt supported-services list does not include Telegram. Therefore the existing isolated Cobalt service is not a valid Telegram dependency.

Source:
`https://github.com/imputnet/cobalt/blob/main/api/README.md`

Decision: DO NOT route Telegram through Cobalt.

### Supadata

Current Supadata transcript documentation lists YouTube, TikTok, X/Twitter, Instagram, Facebook and public file URLs. Telegram is not listed as a supported social platform.

Sources:
- `https://docs.supadata.ai/`
- `https://docs.supadata.ai/api-reference/endpoint/transcript/transcript`

Decision: DO NOT treat a `t.me` URL as a supported Supadata social URL. A direct media-file URL discovered from Telegram may be evaluated separately later, but the Telegram post itself must not be sent to Supadata as if it were a supported platform.

### yt-dlp

The long-standing yt-dlp Telegram support request documents that a `t.me/s/...` generic extraction can behave as a multi-post playlist rather than a precise single-post extractor. There is no accepted dedicated Telegram extractor in the current project.

Source:
`https://github.com/yt-dlp/yt-dlp/issues/2910`

Decision: DO NOT make generic yt-dlp extraction the canonical first implementation for Telegram posts.

## Public Telegram web surface

Telegram officially documents Post Widgets for messages from public groups and channels. A public post has a canonical shape such as:

`https://t.me/<public_channel>/<numeric_post_id>`

and can be embedded without a Telegram login.

Source:
`https://core.telegram.org/widgets/post`

Public `t.me/s/<channel>/<post>` preview pages expose message markup for public channels. Web-preview availability is not equivalent to guaranteed downloadable video availability: some posts expose browser-playable media while other or larger media may remain app-only.

Therefore the adapter must treat media extraction as best-effort and must never request a Telegram account, login code, cookies, MTProto session, bot token, or imported user session to bypass an unavailable public preview.

## Recommended minimal adapter

Implement a dedicated free `TelegramPublicWebRetriever` in VoiceBridge.

Accepted input form for the first version:

`https://t.me/<channel>/<post_id>`

Optional equivalent host:

`https://telegram.me/<channel>/<post_id>`

Normalization target:

`https://t.me/<channel>/<post_id>`

Validation rules:
- HTTPS only;
- public username/channel token only;
- positive numeric post id required;
- reject `joinchat`, `+invite`, `addlist`, `share`, login and non-post forms;
- no redirects to non-Telegram page are trusted as media;
- no cookies/session state;
- max source URL length remains 2048.

Retrieval flow:

```text
public t.me post URL
 -> normalize/validate
 -> GET public Telegram web preview
 -> identify exactly the requested data-post=<channel>/<post_id>
 -> extract direct browser-playable video/audio source only from that post
 -> validate media URL and content type
 -> AssemblyAI EU STT
 -> durable KRCM segments
```

If the exact post is absent, private, login-required, removed, or has no browser-downloadable media:

```text
TELEGRAM_MEDIA_UNAVAILABLE -> terminal FAILED -> STOP
```

No paid fallback is introduced in A9.9.

## Security boundary

The retriever must:
- fetch only normalized Telegram public web-preview URLs;
- accept a returned media URL only when it is HTTPS and originates from the expected Telegram/CDN retrieval response path;
- never fetch arbitrary links embedded in message text;
- enforce response-size and timeout limits;
- reject HTML/login/invite results as media;
- never log full media URLs if they contain temporary access tokens;
- never expose backend job IDs or credentials to the GPT user;
- preserve provider cleanup rules for AssemblyAI.

## Data model delta

Add platform:

`telegram`

Add provider mode:

`telegram_public_retrieval_stt`

Add retrieval provider:

`telegram_public_web`

Recommended fields reuse:
- retrieval credits charged = 0;
- STT seconds charged from AssemblyAI;
- provider data deleted;
- detected language;
- segment count;
- transcript characters;
- durable/reused state.

Do not reuse Facebook-specific `free_retrieval_*` names for new Telegram diagnostics. Add generic or Telegram-specific safe diagnostic fields only if needed.

## Action contract

Recommended isolated Action operation:

`startManagedTelegramPublicTranscription`

Recommended route:

`POST /api/v1/media/managed/telegram`

Request:
- `url`;
- optional `language_hint`.

Owner admission remains server-side exactly like the existing managed Action.

The operation is free at retrieval time and may consume AssemblyAI STT seconds. No Telegram credit-consent prompt is required because no paid retrieval provider is introduced. Existing STT quota/resource limits still apply.

## Acceptance matrix

Automated tests must cover:
- canonical `t.me/channel/123` normalization;
- `telegram.me/channel/123` normalization;
- query/fragment stripping;
- invalid/missing post id rejection;
- invite/private/login URL rejection;
- exact requested post selection, not neighboring posts;
- direct video source extraction from fixture HTML;
- no-media fixture -> terminal unavailable;
- login/private fixture -> terminal unavailable;
- redirect/foreign-host media rejection;
- retrieval timeout/oversize handling;
- zero retrieval credits;
- AssemblyAI success -> durable KRCM completion;
- durable duplicate start reuse;
- no automatic retry after terminal unavailable.

Live acceptance must include:
- one public small browser-playable Telegram video post;
- one public post with unavailable/app-only media or non-video content;
- one invalid/private/invite URL negative case;
- durable transcript reread and segment readback for the positive case.

## Decision

A9.9 architecture audit: PASS.

Implementation is feasible without a Telegram account and without a paid provider for the subset of public posts whose media is exposed through Telegram's public web surface.

The adapter must be explicitly best-effort. It must not claim universal Telegram video support and must return unavailable when Telegram does not expose a browser-downloadable media asset.

## Next step

Implement the URL normalizer/retriever and fixture tests first on `kolemasakar/VoiceBridge:agent/krc-media-transcript`. Do not modify Render, Builder, public KRC, or production VoiceBridge until code/CI is green and an isolated live positive Telegram sample is identified.
