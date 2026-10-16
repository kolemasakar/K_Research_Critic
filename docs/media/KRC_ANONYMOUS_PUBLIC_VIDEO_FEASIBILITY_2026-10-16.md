# Public video access without platform authentication — 2026-10-16

## Owner policy
Only public videos accessible without social-platform account login, session cookies or credentials are in scope. No paid fallback. Pause a platform direction when no workable anonymous retrieval route is demonstrated. Existing infrastructure API authentication is distinct from a social-platform user session; FREE_ONLY remains required.

## Evidence and decisions

| Platform | Anonymous capability and KRC evidence | Decision |
| --- | --- | --- |
| Instagram | Public embedding exists, but embedding is not a usable audio asset. Container helper v3: oEmbed401 and GraphQL401 with login_required and temporary-wait markers; local Cobalt400 error.api.fetch.empty. No usable anonymous media retrieval established. | INSTAGRAM_DEVELOPMENT=PAUSED. No session/cookie test. Reopening requires reproducible anonymous video/audio retrieval. |
| Facebook | Official Public audience includes people off Facebook. Oct4 KRC job KRCM_27482717-917a-454a-a69d-c2a55821a86c completed167.275938s, STT168s, credits0. Fresh sampled page HTTP200 did not expose an asset to the limited parser; current retrieval reliability unconfirmed. | Anonymous option exists; limited direction retained, current end-to-end readiness PARTIAL. |
| YouTube | Gemini documents public YouTube URLs as video input, using infrastructure API authentication rather than a YouTube user session. Historical KRC job KRCM_fabae184-3b16-46c6-baca-c3df701dd61b completed with credits0. No fresh execution in this review. | Anonymous platform access option exists; FREE_ONLY and runtime readiness checks remain required, status PARTIAL. |
| Telegram | Official public post widgets/browser previews. Oct4 public-web job KRCM_afe3cfb7-cbec-44b2-a17a-ce2d76bd3e94 completed58.9s, STT58s, credits0. Fresh sampled HTML did not establish a current media asset; not proof anonymous access is absent. | Anonymous option exists; research retained. TELEGRAM LIVE BLOCKED remains owner gate. |

Historical operational evidence: KRC_LIVE_ACCEPTANCE_PROGRESS_2026-10-04.md.
Instagram evidence: KRC_INSTAGRAM_CONTAINER_LOGIN_THROTTLE_CONFIRMED_2026-10-16.md.
Cancelled proposal: KRC_INSTAGRAM_AUTH_SESSION_ISOLATED_TEST_PLAN_2026-10-16.md.

## Limits
Public page or embed availability is not proof of downloadable audio/video or successful transcription. Historical completed jobs demonstrate feasibility for those sources at those dates, not universal or current reliability. Instagram failures establish failure of the tested KRC route, not universal impossibility of anonymous Instagram viewing. No additional media starts, session tests, production deploys, paid providers or permission expansions were performed in this review.

## Primary references
- https://help.instagram.com/ — public content embedding help; platform viewing only, not a retrieval guarantee.
- https://developers.facebook.com/documentation/instagram-platform/oembed
- https://www.facebook.com/help/204305118221546
- https://ai.google.dev/gemini-api/docs/video-understanding
- https://core.telegram.org/widgets/post
- https://telegram.org/tour/channels/pl?setln=en

## Effective state
AUTH_SESSION_TEST=CANCELLED_NOT_EXECUTED
INSTAGRAM_DEVELOPMENT=PAUSED
FACEBOOK_ANONYMOUS_OPTION=EXISTS_CURRENT_RETRIEVAL_UNCONFIRMED
YOUTUBE_ANONYMOUS_OPTION=EXISTS_RUNTIME_PARTIAL
TELEGRAM_ANONYMOUS_OPTION=EXISTS_LIVE_BLOCKED
FREE_ONLY=REQUIRED
PUBLIC=HOLD
PRODUCTION_CHANGE_AUTHORIZED=NO
