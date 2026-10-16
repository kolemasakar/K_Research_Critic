# KRC exact Cobalt reason classifier — live 2026-10-16

## Contract audit
Authorized local GET on krc-cobalt reported Cobalt 11.7.1, upstream commit a636575b09de1fc55d9b8cd98cac88f5f2f16b42. Exact upstream schema/API sources confirm current VoiceBridge JSON options and header/auth scheme syntax. No contract mismatch demonstrated.

Cobalt returns HTTP 400 for multiple rejection paths, including API key not_found/IP/User-Agent policy, session auth, headers/body/URL/service and content fetch failures. Existing VoiceBridge mapped most to generic HTTP_400. This is a confirmed observability gap, not proof of the live failure reason.

## Tested narrow repair
VoiceBridge commit 65737cfb7e3a89bdaaed95bdf5519d65abae0acf, branch agent/krc-media-gemini-migration. Three files only: classifier, tests, audit document. Static exact upstream-code allowlist maps to sanitized local categories on HTTP 400. Unknown/malformed values remain generic; raw codes/context/messages/keys never forwarded. Retrieval requests, credentials and provider retry rules unchanged.

TypeScript build PASS; public Cobalt tests 13/13 PASS; full suite 284/284 PASS, zero failures/skips, exit 0, 48.937s. Tested local tree and GitHub tree exactly match 0423e2998384db550d6afd6b8d568399e0a55b75. Compare against deployed baseline befff428: ahead 1, behind 0.

## Deployment verification
Existing Render free service srv-da1kic5bedkc73d6fk60, autoDeploy off, unchanged plan/config. Deploy dep-db8v5g3rjlhs73dlhhm0 exact SHA 65737cfb7e3a89bdaaed95bdf5519d65abae0acf LIVE at 2026-10-16T09:48:15.367512Z.
Postdeploy R3C capabilities request d1871dc0-93e2-4601-b374-1ef5dd93a1e1 PASS: configured=true, postgres, deduplication/restart persistence advertised, automatic/paid retrieval/paid STT fallback=false.

## Open boundary
No new MEDIA start performed during this patch/deploy. Existing KRCM_e3e37765-cc0d-4240-a668-4ae5aefaa910 only retains generic HTTP_400; more specific information cannot be retroactively recovered. Render logs for its time window yielded none. Specific live root cause and Instagram retrieval repair remain OPEN. Next requires one appropriately authorized and suitable bounded probe with new classifier, or narrow sanitized host diagnostics. No Docker privileges expanded. R4 PRIVATE PARTIAL, public HOLD, Telegram LIVE BLOCKED.

Detailed source/validation: https://github.com/kolemasakar/VoiceBridge/blob/agent/krc-media-gemini-migration/docs/media/KRC_COBALT_EXACT_1171_REASON_DIAGNOSTICS_2026-10-16.md
