# KRC Public MCP — HTTP test candidate (2026-10-16)

Status: **OFFLINE PASS / PUBLIC RELEASE HOLD**.

## Executed
- Reused V3 prototype; added bounded JSON-RPC HTTP handler and a dedicated HTTP integration suite.
- Handler implements `POST /mcp` for initialize, notifications/initialized, ping, tools/list and tools/call, plus GET /health; GET /mcp returns 405 rather than pretending to support SSE.
- Rejects Origin browser requests by default; emits protocol version and JSON-RPC-style tool errors.
- Combined unittest results **25/25 PASS** (19 preceding + 6 HTTP tests), on local isolated environment only.
- ZIP `KRC_PUBLIC_MCP_HTTP_CANDIDATE_2026-10-16.zip` created and archive integrity verified. **ZIP is conversation artifact; code not yet committed to repository.**
- No production or OCI changes, no public endpoint.

## Known limitations and hard blocks
- HTTP transport implements only a subset of MCP Streamable HTTP; full interoperability with ChatGPT and session handling not yet proven.
- Lack of complete public abuse protection, queue storage hard cap, and reliable strong capability lifecycle.
- Possible SQLite resource cleanup warnings and queue/retention edge cases.
- OCI Cobalt concurrent load and memory/CPU budget tests are not yet performed.
- Domain/TLS/host protections and Sentinel service identity not provisioned.
- Do not publish or connect as an externally exposed public plugin.

## Release order
1. Audit and commit source; implement conformant MCP transport / client tests.
2. Harden input/queue and retention controls.
3. Isolated loopback staging on KRC Cobalt, Sentinel least-privileged service, observe media co-load and run 1/3/10-user tests.
4. Only on pass, explicitly expose Caddy HTTPS endpoint, verify external client and publish.
