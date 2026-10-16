# KRC Public MCP V5 — live localhost HTTP test checkpoint (2026-10-16)
Status: LOCAL_HTTP_PASS / OCI_DEPLOYMENT_HOLD.

## Observations
- Original archive `KRC_PUBLIC_MCP_V5_SQLITE_CLOSE_2026-10-16.zip`: present, validated via unzip -t; 27/27 original tests PASS with ResourceWarning-as-error.
- Spawned separate V5 `ThreadingHTTPServer` process on `127.0.0.1:19013` in disposable local directory; sent real HTTP JSON-RPC requests using urllib.
- `initialize`: negotiated `2025-03-26`; `tools/list`: six tools.
- Ten simultaneous guest flows: create guest_session, submit research_profile_validate, poll job_status with delivery ACK: **10/10 completed** in localhost synthetic test.
- Additional localhost HTTP tests: **2/2 PASS**; existing tests **27/27 PASS** (29 in total across suites, independently executed).
- This is NOT proof of official MCP SDK / ChatGPT interoperability or OCI capacity.

## Safety/release gates
- Source archive still NOT committed into GitHub repository: only docs are archived; committing verified source remains pending.
- Original README contains superseded historical cautions; need canonical updated README.
- Source offers HTTP 2025-03-26 subset, not a complete current Streamable HTTP conformance statement.
- Guest capability may be exposed to the language model as tool response; no identity mapping guaranteed by ChatGPT installation. Protect all job retrievals and logs.
- Database cleanup and document eviction under concurrent pressure require further test.
- No production modifications. No public endpoint. OCI Cobalt loopback staging and 1/3/10 co-load tests remain pending.
