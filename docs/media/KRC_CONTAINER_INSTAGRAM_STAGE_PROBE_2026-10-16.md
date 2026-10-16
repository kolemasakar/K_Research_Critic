# Container Instagram stage probe — 2026-10-16

Owner authorized execution. Existing root-owned helper now exposes summary/logs/probe/instagram. krcops started krc-cobalt-diag@instagram.service successfully via the approved systemd channel. Process PID74009, exit0, runtime3.49s. No managed MEDIA start/STT, production code or privileges changed.

## Observed sanitized output
- cobalt_retrieval: internal API key loaded=true, HTTP4xx, response status error, exact allowlisted code error.api.fetch.empty.
- oembed: HTTP4xx, JSON=true, media_id_present=false.
- mobile: not_attempted, item_present=false.
- embed: HTTP3xx, legacy_init_marker=false, context_json_present=false.
- web_prereq: HTTP3xx; site_data/polaris_site_data/web_config/csrf absent; lsd_present=true.
- graphql: HTTP4xx, JSON=false, data_present=false, media_present=false.
- secrets_exposed=false.

## Evidence boundary
Successful internal Cobalt authentication and a content-retrieval error are demonstrated for this local request. This does not compare the internal helper-selected key with the exact VoiceBridge key. Summary previously confirmed COOKIE_PATH and proxy unset.

Read helper code before execution. It performs independent stage approximations plus one actual local Cobalt retrieval. It is not instrumentation of the live handler. redirect=manual differs from Cobalt fetch default follow; hence 3xx and missing web prerequisites cannot establish a failure in the production fetch. lsd_present may be synthetic random fallback, not a token extracted from Instagram. Current output contains HTTP classes only. GraphQL wrapper differs in headers/cookie behavior from exact source. Do not infer that all observed independent stages were actually executed by the production request.

## Next concrete diagnostic correction
Root-owned stage helper should output exact numeric HTTP status, distinguish extracted from synthetic prerequisite tokens, and preserve production redirect behavior with bounded total/body time and size. Prefer actual installed-handler tracing with sanitized fetch stage metadata; no raw response/session/cookie export. Retain fixed source, no arbitrary command/URL inputs and existing systemd authorization. Provider repair remains OPEN. R4 PRIVATE PARTIAL/public HOLD, Telegram LIVE BLOCKED, FREE_ONLY retained.
