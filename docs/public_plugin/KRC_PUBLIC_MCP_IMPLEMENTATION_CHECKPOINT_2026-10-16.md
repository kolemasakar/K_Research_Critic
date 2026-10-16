# KRC Public MCP — execution checkpoint (2026-10-16)
Status: OFFLINE_PROTOTYPE_TESTED / PRODUCTION_HOLD

## Owner authorization
Sequential work: (1) OCI Cobalt resource audit, (2) MCP + durable FIFO, (3) transient document storage, (4) 1/3/10-user testing, (5) controlled deployment only after acceptance. K-Trader is excluded; KGM reserved for public KGM. Existing Cobalt production remains untouched.

## 1 — Resource audit
OCI `krc-cobalt`: 952 MiB RAM total, 545 MiB MemAvailable, 349 MiB swap used of 2047 MiB, 37 GiB disk available, load 0.05/0.09/0.09, Docker/Caddy active. These are idle snapshots; peak concurrent Cobalt MEDIA workload remains unmeasured. No evidence yet for accepting production memory/CPU budgets.

## 2–3 — Offline prototype
Local source artifact: `KRC_PUBLIC_MCP_OFFLINE_PROTOTYPE_2026-10-16.zip` (conversation artifact; not yet committed to repository). Python standard library, SQLite durable queue with monotonic sequence and restart requeue; proof-of-concept MCP JSON-RPC initialize/tools/list/tools/call; 3 research validators, status lookup, base64 chunked document storage, cleaner. Not ready for public exposure.

## 4 — Tests
Offline unittest: 10/10 PASS. Local synthetic user counts 1/3/10: 1/1, 3/3, 10/10 completed in approximately 2.34/3.83/41.09 ms on isolated build environment (NOT OCI production; not a concurrency throughput guarantee). Neither existing Cobalt load nor HTTP user journey was included.

## Release-blocking findings
- No per-user authorization on job status; current prototype MUST NOT be exposed publicly.
- Temp document TTL currently begins at upload, not 10 h after completion AND result delivery, contrary to owner decision.
- MCP protocol requires complete client interoperability and error handling; prototype is partial.
- Resilience, bounding and security review of FIFO/durable storage outstanding.
- CPU/RAM limits and Caddy HTTPS deployment not configured.
- Existing privilege model `krcops` cannot be silently elevated; configure new service through authorized Sentinel manager.

## Stage 5
NOT DEPLOYED: stop at release gates; no OCI/Render writes, production mutations, provider calls or paid services occurred.

## Next implementation fix order
1. Authenticated job ownership and verified delivery ACK; then retention bound to ACK + 10 hours.
2. MCP transport compliance, integration and server restart/load tests.
3. OCI co-load tests and isolation config as an explicit reviewed change.
4. Deploy to OCI only if all safety/functional gates PASS.
