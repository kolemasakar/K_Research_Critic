# MEDIA readiness and Gemini diagnostics installation — 2026-10-04

User authorized installation. FREE_ONLY remains in force.

## Changes

- VoiceBridge: preserve numeric gateway error codes and an allowlist of google.rpc.ErrorInfo reasons. Never persist raw provider messages, detail metadata, API keys, or arbitrary reasons. String Interactions codes and legacy statuses remain supported. No model, billing, credentials or retry changes.
- KRC platform execution: immediately before a managed or YouTube consequential POST, perform one unauthenticated GET /api/v1/health with the existing bounded timeout. Require HTTP200 and JSON status=ok. Failure returns voicebridge_not_ready before POST. Never replay POST after ambiguous send or provider failure. Readonly routes have no extra request. This gate is a readiness measure, not proof that cold start caused the prior429.

## Validation

- VoiceBridge npm run check: 274/274 PASS, zero failures,88.430s.
- KRC focused readiness and readonly tests:27 PASS.
- Full KRC:421 PASS,9 fixture-dependent tests skipped,18.51s.
- All nine real-HTTPS cross-repository tests:9 PASS,16.49s using isolated research fixture injection with the new production Gemini file. The fixture injection is excluded from the production deployment. An initial run against the production-only root failed5/9 because it lacks fixture provider injection; retained separately as a harness prerequisite limitation.
- New tests cover readiness failure/timeout/non200, exact GET-before-singlePOST ordering, readonly behavior, no uncertain POST replay, numeric gateway metadata, reason allowlisting and secret exclusion.

## Scope and limitations

Deploy only to existing free VoiceBridge beta and four platform sentinels. E2/E3/E4 remain probe-only. Existing Facebook repair remains included. No new infrastructure, main merge, paid fallback or automatic provider work.

YouTube provider400 and Instagram429 root causes remain open. These changes provide safer execution and diagnostic metadata; they do not constitute successful live transcription acceptance for those two platforms.

## Installed and verified

- VoiceBridge production commit: c2ba34f292d0c2189bc9e994121011693488dc84.
- Four sentinels production commit: caa9db7f407ebe23842993ad4df0341d4f536b2a.
- srv-da1kic5bedkc73d6fk60: dep-db1855dg1s2s7390kn3g, status=live, finishedAt=2026-10-04T16:45:46.594472Z.
- srv-dall4qv40ujc73ednpqg: dep-db1855jncjis73bken9g, status=live, finishedAt=2026-10-04T16:45:56.505994Z.
- srv-dan7vsijnfac73fmrtl0: dep-db1855qd0e5s73ei73i0, status=live, finishedAt=2026-10-04T16:45:57.602946Z.
- srv-danerqmgekts738oejsg: dep-db18561srm7s73ah60l0, status=live, finishedAt=2026-10-04T16:45:59.077577Z.
- srv-danertv40ujc73bn9hog: dep-db1856hsrm7s73ah65t0, status=live, finishedAt=2026-10-04T16:46:02.293629Z.

All five post-deployment health checks returned HTTP200/statusok at 2026-10-04T16:46:44Z. E2/E3/E4 confirmation_probe_only=true. R3C capabilities request2477cf8b-8d24-416f-824a-8abdc8e9c68d returnedconfiguredtrue/allfourplatforms, GeminiFreeonlytrue, allpaidfallbackfalse. No new provider start or free STT consumption was initiated during this installation. Current live acceptance remains Facebook+TelegramPASS; YouTube400 and Instagram429 remain unresolved.
