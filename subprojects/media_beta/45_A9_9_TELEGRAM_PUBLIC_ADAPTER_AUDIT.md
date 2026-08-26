# A9.9 Telegram Public Video Adapter Audit
Аудит поточного коду і мінімального zero-client шляху для публічних Telegram video posts.

Status: AUDIT_COMPLETE / IMPLEMENTATION_SLICE_1_IN_PROGRESS
Date: 2026-08-26
Scope: isolated KRC MEDIA BETA and VoiceBridge feature branches only

## Current repository state

Before A9.9 implementation VoiceBridge `agent/krc-media-transcript` had no Telegram adapter, Telegram-specific source module, or Telegram-specific regression tests.

The existing durable managed-media service is reusable for a Telegram adapter, but Telegram must be added deliberately rather than passed through the existing Supadata native route.

## Provider audit

### Cobalt

The current upstream Cobalt supported-services list does not include Telegram. Therefore the existing isolated Cobalt service is not a valid Telegram dependency.

Source:
`https://github.com/imputnet/cobalt/blob/main/api/README.md`

Decision: DO NOT route Telegram through Cobalt.

### Supadata

Current Supadata transcript documentation lists YouTube, TikTok, X/Twitter, Instagram, Facebook and public file URLs. Telegram is not listed as a supported social platform.

Sources:
- `https://docs.supadata.ai/`;
- `https://docs.supadata.ai/api-reference/endpoint/transcript/transcript`.

Decision: DO NOT treat a `t.me` URL as a supported Supadata social URL.

### yt-dlp

The current upstream yt-dlp tree DOES contain a dedicated `TelegramEmbedIE` for URLs of the form `https://t.me/<channel>/<numeric_post_id>`.

It requests the Telegram embed page with `embed=1` and `single`, then selects `tgme_widget_message_video_player`, extracts the `<video src=...>` URL and duration, and supports single-post selection for multi-video posts.

Source:
`https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/telegram.py`

The VoiceBridge runtime image already installs yt-dlp. This is useful compatibility evidence, but the first A9.9 implementation uses a small native Node retriever for the same public embed surface so the exact-post, host-trust, timeout, size and zero-credit rules remain explicit and fixture-testable inside VoiceBridge.

Decision: dedicated yt-dlp Telegram support is a valid fallback/reference implementation, not the initial routing dependency.

## Public Telegram web surface

Telegram officially documents Post Widgets for messages from public groups and channels. A public post has a canonical shape such as:

`https://t.me/<public_channel>/<numeric_post_id>`

and can be embedded without a Telegram login.

Source:
`https://core.telegram.org/widgets/post`

Observed Telegram embed HTML uses:
- `data-post="<channel>/<post_id>"` on the message;
- `tgme_widget_message_video_player` for a browser-playable video;
- `<video src="https://cdn*.cdn-telegram.org/...mp4?...">` for the direct temporary media URL;
- `message_video_duration` for duration.

A current captured Telegram widget fixture confirms this markup pattern. This aligns with the current upstream yt-dlp Telegram extractor.

Web-preview availability is not equivalent to guaranteed downloadable video availability. Some media may remain app-only or otherwise unavailable through the public embed surface.

Therefore the adapter is best-effort and must never request a Telegram account, login code, cookies, MTProto session, bot token, or imported user session to bypass an unavailable public preview.

## Minimal adapter

Implement a dedicated free `TelegramPublicWebRetriever` in VoiceBridge.

Accepted input forms:

`https://t.me/<channel>/<post_id>`

`https://telegram.me/<channel>/<post_id>`

`https://t.me/s/<channel>/<post_id>`

Normalization target:

`https://t.me/<channel>/<post_id>`

Validation rules:
- HTTPS only;
- public username/channel token only;
- positive numeric post id required;
- reject `joinchat`, `+invite`, `addlist`, `share`, login and non-post forms;
- no cookies/session state;
- max source URL length remains 2048.

Retrieval flow:

```text
public t.me post URL
 -> normalize/validate
 -> GET exact Telegram embed with embed=1&single=1
 -> verify exact data-post=<channel>/<post_id>
 -> select exact tgme_widget_message_video_player href
 -> extract direct browser-playable HTTPS Telegram CDN MP4 source
 -> AssemblyAI EU STT
 -> durable KRCM segments
```

If the exact post is absent, private, login-required, removed, or has no browser-downloadable video:

```text
TELEGRAM_MEDIA_UNAVAILABLE -> terminal FAILED -> STOP
```

No paid fallback is introduced in A9.9.

## Security boundary

The retriever must:
- fetch only normalized Telegram public embed URLs;
- accept media only from trusted Telegram CDN HTTPS hosts;
- require an MP4 path for the initial video-only adapter;
- never fetch arbitrary links embedded in message text;
- enforce response-size and timeout limits;
- reject non-HTML preview responses;
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

Do not reuse Facebook-specific `free_retrieval_*` names for new Telegram diagnostics.

## Action contract

Recommended isolated Action operation:

`startManagedTelegramPublicTranscription`

Recommended route:

`POST /api/v1/media/managed/telegram`

Request:
- `url`;
- optional `language_hint`.

Owner admission remains server-side exactly like the existing managed Action.

The operation is free at retrieval time and may consume AssemblyAI STT seconds. No Telegram retrieval credit-consent prompt is required because no paid retrieval provider is introduced.

## Acceptance matrix

Automated tests must cover:
- canonical `t.me/channel/123` normalization;
- `telegram.me/channel/123` normalization;
- `t.me/s/channel/123` normalization;
- query/fragment stripping;
- invalid/missing post id rejection;
- invite/private/login URL rejection;
- exact requested post selection, not neighboring posts;
- direct video source extraction from fixture HTML;
- trusted Telegram CDN host requirement;
- no-media fixture -> terminal unavailable;
- retrieval timeout/oversize handling;
- zero retrieval credits;
- AssemblyAI success -> durable KRCM completion;
- durable duplicate start reuse;
- no automatic paid fallback or retry after terminal unavailable.

Live acceptance must include:
- one public small browser-playable Telegram video post;
- one public post with unavailable/app-only media or non-video content;
- one invalid/private/invite URL negative case;
- durable transcript reread and segment readback for the positive case.

## Implementation slice 1

VoiceBridge branch implementation now contains:
- Telegram added to managed URL platform normalization;
- `TelegramPublicWebRetriever`;
- exact-post embed parsing;
- trusted Telegram CDN MP4 filtering;
- timeout and HTML-size guards;
- zero retrieval-credit contract;
- Telegram-specific regression tests.

Current VoiceBridge commits for this slice:
- `25afbcd3903b9c4e589df16f74a3a9e392287457` - Telegram URL normalization;
- `0c43c21af8d5ada9c80768906a485b9976813c1e` - Telegram public web retriever;
- `41f7e69e73576b0c3cf6f3d757e81951bdf0372a` - Telegram retriever regressions.

The retriever is not yet connected to the managed HTTP/Action/durable STT execution path. No Render or Builder change is authorized at this slice.

## Decision

A9.9 architecture audit: PASS.

Implementation is feasible without a Telegram account and without a paid provider for the subset of public posts whose media is exposed through Telegram's public embed surface.

The adapter must not claim universal Telegram video support and must return unavailable when Telegram does not expose a browser-downloadable media asset.

## Next step

After VoiceBridge CI is green, connect `TelegramPublicWebRetriever` to the managed durable KRCM + AssemblyAI path behind an isolated Telegram operation and add service/HTTP regression coverage. Do not modify Render, Builder, public KRC, or production VoiceBridge before that code path is green.
