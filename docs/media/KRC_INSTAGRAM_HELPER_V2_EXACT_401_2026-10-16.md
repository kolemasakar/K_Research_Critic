# Instagram helper v2 exact results — 2026-10-16

Owner reported diagnostic helper installation PASS, production container unchanged. Verified live root helper SHA256 452b97842180a5537319485704eee0f4b3b436f017110e5972eccc22ba29b970 matches tested candidate. One approved systemd instagram diagnostic from krcops; PID74128, exit0, 4.34s. No managed media start/STT or production adapter modification.

## Fresh container-context diagnostic
- oEmbed: HTTP401, JSON present, media_id absent.
- mobile: not attempted because media_id absent.
- embed: HTTP200 after redirect following; legacy initializer/contextJSON absent.
- web prerequisites: HTTP200; SiteData, PolarisSiteData, WebConfig and CSRF present. LSD extracted=true, synthetic=false.
- GraphQL POST: HTTP401; JSON present, data/media absent.
- local internally authenticated Cobalt retrieval: HTTP400, internal API key loaded, status error, exact allowlisted error.api.fetch.empty.
- secrets_exposed=false.

## Updated interpretation
The earlier missing-prerequisites observation was an artifact of the diagnostic wrapper's manual redirect behavior. With redirects followed, valid-shaped web prerequisites are available yet the diagnostic GraphQL POST is rejected with401. Thus missing prerequisite fields are not supported as the cause of this diagnostic failure. This is rejection at Instagram content endpoints, distinct from Cobalt API authentication.

HTTP401 alone does not establish whether Instagram requires login, applies automation/IP/session policy, rejects outdated GraphQL document/request fields, or restricts this source. No raw Instagram error body has been exposed. Independent diagnostic stage calls still do not prove the exact stage sequence executed inside the unmodified production handler; the local Cobalt final failure is real.

## Next research work
Extend bounded sanitization to fixed Instagram JSON error fields/markers, not arbitrary messages. Compare diagnostic request document ID/headers with current official adapter and reviewed PRs; reproduce using local isolated tests before any runtime candidate. Keep fallback patch as research-only because previous anonymous candidate still failed. No cookies or credentials without separate justified owner authorization. Exact production image/digest remains open. FREE_ONLY, PUBLIC HOLD, Telegram LIVE BLOCKED retained.
