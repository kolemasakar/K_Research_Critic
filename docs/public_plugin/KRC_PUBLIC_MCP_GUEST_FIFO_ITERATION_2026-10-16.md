# KRC Public MCP — guest FIFO iteration (2026-10-16)
Status: TEST_ONLY / PUBLIC_DEPLOYMENT_HOLD.
Owner: guest access without signup; 10h retention or FIFO displacement; implement/test/deploy conditionally on gate pass. KRC Cobalt only; KGM/K-Trader reserved.
## Evidence
- Offline source package: `KRC_PUBLIC_MCP_GUEST_FIFO_ITERATION_2026-10-16.zip` (attached in conversation, source files not yet uploaded to repository).
- 16/16 local Python unittests PASS.
- Synthetic 1/3/10 concurrent submissions: all completed, local ~1.95 / 3.80 / 22.38 ms (not OCI).
- Local HTTP initialize and tools/list tests pass with 6 tools; anonymous guest-session tool returns random capability.
- Guest isolation by bearer capability (no ChatGPT account sign-in); anyone with leaked bearer may read same job.
- SQLite FIFO queue and one worker; queued/running documents protected from eviction.
- 10h retention counted from explicit delivery ACK, capacity eviction oldest *eligible* document. Unclaimed results fallback 24h is temporary and requires final owner review.
## Known blockers
- NOT fully compliant with MCP Streamable HTTP or complete real ChatGPT client verification.
- No production-grade replay/CSRF/origin/throttling/DoS protection; no total disk/queue upper bound when all records protected.
- SQLite connection cleanup warnings.
- Owner-provided retention rule requires clarification of unclaimed results when user never receives delivery.
- OCI KRC Cobalt resource snapshot: about 545MiB available RAM, 349MiB swap used; active MEDIA peak and simultaneous stress test not performed.
- No new OCI accounts/permissions/service/hostnames, no public deployment. Do not treat local tests as production acceptance.
## Next actions
Harden secret handling and guest isolation, retention semantics, rate limits/queue spool, full MCP protocol validation, OCI read-only co-load baseline, authorized isolated staging, 1/3/10 HTTP load, Caddy/TLS and public review after PASS.
