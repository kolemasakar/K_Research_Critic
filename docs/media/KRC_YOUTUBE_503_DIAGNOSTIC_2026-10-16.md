# YouTube Gemini 503 diagnostic — 2026-10-16

Render reports live deploy dep-db8v5g3rjlhs73dlhhm0, commit65737cfb7e3a89bdaaed95bdf5519d65abae0acf. No new deployment performed.
Capabilities reported active model gemini-3.8-flash. Source default gemini-3.7-flash can be overridden by KRC_MEDIA_YOUTUBE_GEMINI_MODEL; no secret environment values read or configuration altered.
Provider code sends direct POST to Gemini Interactions, preserves actual non-2xx response.status in GeminiYoutubeProviderHttpError and sets retryable=true on5xx. Missing configuration has a distinct GEMINI_YOUTUBE_NOT_CONFIGURED code; network failures GEMINI_YOUTUBE_UNREACHABLE.
Observed job8f3accb1... had GEMINI_YOUTUBE_FAILED, provider_http_status503,provider_error_code service_unavailable. This supports an upstream unavailable response rather than a Cobalt or social login error. It does not prove every aspect of Gemini configuration correct.
Render logs queries13:30–13:32UTC (with/without gemini filter) returned empty,hasMore=false; no additional runtime cause established.
Google official error reference describes service_unavailable503 as temporarily overloaded or down:
https://ai.google.dev/gemini-api/docs/api-errors
Troubleshooting recommends exponential backoff for transient errors:
https://ai.google.dev/gemini-api/docs/troubleshooting

A single repeat start on the same public source6yXU8a5CK2Q was submitted after the first failure and diagnostic interval, using existing Gemini Free consent. No immediate retry loop, model fallback, paid tier, platform session or configuration mutation.
Response pending at this checkpoint; do not duplicate pending work.
Instagram development PAUSED; Telegram LIVE BLOCKED; PUBLIC HOLD; FREE_ONLY.
