# Cobalt authentication diagnostic, 16 October 2026

Status: deployed diagnostic; Instagram retrieval acceptance remains PARTIAL.

Observed: Cobalt v11.7.1 responds HTTP 200 at localhost port 9000 and at public HTTPS endpoint. Instagram is advertised. A direct unauthenticated local POST returned HTTP 400 with error.api.auth.key.missing; this proves local authentication is enforced but does NOT prove VoiceBridge lacks credentials.

Earlier real Instagram job KRCM_ca65efea-6ca0-4aec-bfbc-18ec530eeb41 failed with COBALT_PUBLIC_MEDIA_FAILED before STT; both status and empty segments were read successfully, and Neon confirmed persistence. Charges reported as 0.

VoiceBridge source normalized all Cobalt non-2xx responses into one code. New bounded categories distinguish auth key missing, auth key rejected, or other rejection without copying upstream message, URL or secret. Source commit df7b4d70129e70d5ec73814c862603d5f848cab4; tests commit 38a30cac8e33194cefba04ea2771e91c99531f17. Exact-sha TypeScript build PASS, targeted 10/10 PASS, full 281/281 PASS.

Render VoiceBridge srv-da1kic5bedkc73d6fk60 deployed commit 38a30cac8e33194cefba04ea2771e91c99531f17 via dep-db8u19jrjlhs73dhvn60, status live, finished 2026-10-16T08:31:42Z. Post-deploy E2 Instagram preflight PASS, request bfd9b922-6109-4196-a68c-a1f37f549e24. Lookup returned reused=true and the previous failed job, request ba1025cb-3d3f-4b89-a7ae-d8420247428d. No further MEDIA start was made: duplicate reuse means this URL cannot yield new diagnostics until policy permits a genuinely new source or expired state.

Security: FREE_ONLY unchanged; no paid fallback, no Telegram LIVE. No change to Cobalt keys or Docker privileges. Authenticated VoiceBridge to Cobalt upstream response category remains unobserved for a new request, hence root cause is not established. Full R4 acceptance stays PARTIAL, public release HOLD.
