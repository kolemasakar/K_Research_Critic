# Instagram Cobalt FETCH_EMPTY confirmed — 2026-10-16

## Authorized controlled probe
Owner selected the next controlled classifier check. Used historically verified 41.11675s speech-bearing reel https://www.instagram.com/reel/Dcea3BiPTBm/ after readiness/preflight and lookup, without changing language or identity to bypass a stored job. No reusable job was found. One start only.

- Capabilities request 05e64479-180c-4feb-86a9-455190822f02: configured, postgres, paid fallbacks false.
- Preflight request d9fe6615-a860-497e-a077-950c01c31d0a: can_continue=true, Cobalt+AssemblyAI, estimated retrieval credits 0.
- Lookup request 391a77cf-94f4-453c-acfc-03cf682daa2a: HTTP 404.
- Start request da6cc2e8-7506-420e-bfd6-af80f87fd5a4; job KRCM_f264cb29-554c-49d4-9750-bcb2d407606e, reused=false.
- Created 2026-10-16T09:56:51.652Z, terminal 09:56:53.626Z.
- FAILED, COBALT_PUBLIC_MEDIA_FETCH_EMPTY, retryable=false; STT 0 seconds, reported credits 0, transcript/segments 0, charge_uncertain=false.
- Status request 3e4580ec-678d-424e-9f72-a50d3b75e4e1 confirms same persisted failure.
- Segments request dd70c731-0969-4bab-957c-be534b17baa8: empty, next_cursor=null.

## Meaning and limits
Deployed VoiceBridge 65737cfb exact allowlist maps upstream error.api.fetch.empty on HTTP 400 to FETCH_EMPTY. This is a content retrieval failure category, not the known Cobalt API key/header/body rejection categories, HTTP 429 or STT error. Do not claim it proves Instagram login/cookies/network restrictions absent.

Exact installed Cobalt a636575b09de1fc55d9b8cd98cac88f5f2f16b42 Instagram handler returns fetch.empty after failed extraction or after an inconclusive error-context probe. Therefore the code alone does not distinguish unavailable/deleted content, changed response shape, restricted anonymous retrieval or an extraction/fallback defect. The reel had succeeded historically, but current original availability is not independently established by this check.

Next: bounded sanitized stage/response-shape diagnostics in the Cobalt Instagram handler, including whether mobile/embed/GraphQL data actually contain media fields. No speculative credential/cookie changes, no automatic repeated MEDIA starts. Provider repair remains OPEN; R4 PRIVATE PARTIAL/public HOLD/Telegram LIVE BLOCKED. FREE_ONLY preserved.
