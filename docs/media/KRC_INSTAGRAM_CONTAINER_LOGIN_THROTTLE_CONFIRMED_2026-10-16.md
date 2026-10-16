# Container Instagram error flags confirmed — 2026-10-16

Owner installed root diagnostic helper v3 and reported production container unchanged. KRC verified SHA256 306c49816b384385c38b3d54fcbd8741f5f19bd1a65088fb9f7ec3953477193b matches reviewed candidate. One approved systemd diagnostic; PID74274, exit0,4.35s. No managed media start/STT, cookies, credentials, privileges or production adapter changes.

## Container-context results
- oEmbed HTTP401, JSON status fail, login_required=true, rate_limit_marker=true, media_id absent.
- mobile not attempted.
- embed HTTP200, legacy initializer/context absent.
- web HTTP200; SiteData/PolarisSiteData/WebConfig/CSRF present; LSD extracted=true, synthetic=false.
- GraphQL POST HTTP401, JSON status fail, login_required=true, rate_limit_marker=true, data/media absent.
- Both errors: challenge/checkpoint/consent/feedback/GraphQL-error-array flags false, numeric error code absent. Arbitrary message suppressed.
- Authenticated local Cobalt retrieval HTTP400, internal API key loaded=true, exact allowlisted error.api.fetch.empty.
- secrets_exposed=false.

## Conclusion
Prior host error flag observation now reproduced inside the container by independent diagnostic requests. Instagram responses explicitly combine a login requirement flag with a temporary-wait message marker. This confirms a specific response category for anonymous requests, not a permanent IP ban, not HTTP429, and not proof that adding cookies will fix retrieval. No exact cooldown duration established. Independent diagnostic calls are not a literal trace of the unmodified live handler; real local Cobalt final failure is confirmed.

Fallback defects remain independently reproduced and research-only. They do not overcome the observed401 response. Do not deploy them as a claimed recovery or run repeated anonymous probes. Further authentication/cookie experiment requires separate reasoned owner authorization; credentials should never be provided in chat. Production image/digest still not exposed by helper. FREE_ONLY; R4 PRIVATE PARTIAL; PUBLIC HOLD; Telegram LIVE BLOCKED.
