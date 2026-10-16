# Instagram anonymous 401 error flags — 2026-10-16

Owner selected bounded JSON error classification. Existing root helper v2 was not changed. Ran one fixed-source independent diagnostic as host krcops with no cookies/proxy/credentials, no local Cobalt retrieval, no media start or STT. Same request pattern as reviewed helper v2, following redirects, exact HTTP statuses. Host PID74205.

## Observed output
Both oEmbed and GraphQL POST: HTTP401, JSON=true, status=fail, login_required flag=true, rate_limit_marker=true (fixed substring: please wait a few minutes). Challenge/checkpoint/feedback/consent/GraphQL errors markers false; numeric error code absent. No raw message/body/header/session data emitted.

Embed HTTP200 without legacy initializer; web200 with SiteData/PolarisSiteData/WebConfig/CSRF and actually extracted LSD. No media_id so mobile not attempted. No media data returned.

## Interpretation and limits
The response contains an explicit login requirement flag and a temporary-wait/throttling message marker for anonymous requests from this host. These are combined signals, not proof that a cookie will restore access, not proof of a fixed IP ban, and not HTTP429. No duration for a cooldown is established. Prior real container helper v2 independently showed the same401 status at both endpoints, but container error-body flags have NOT been measured. Do not conflate host and container evidence or retry repeatedly.

## Prepared sanitizer
scripts/diagnostics/cobalt_instagram_error_flags_v3_20261016.cjs extends reviewed v2 only with static booleans, bounded numeric error code, and exact allowlisted message categories. Unknown messages are suppressed. Local checks PASS: no private sentinel in serialized output, null/malformed input handling, combined login/throttle markers. It remains a research candidate; not installed as root helper or production adapter.

## Next action
Retain current failed state and avoid repeated retrieval. Container flags can be confirmed by installing reviewed diagnostic v3 via existing administrator channel if required; no new privileges. Any cookie/credential setup needs separate owner authorization and justification. Research fallback patch remains independently useful but does not overcome an Instagram401 policy response. No production adapter changes authorized. FREE_ONLY/public HOLD/Telegram LIVE BLOCKED.
