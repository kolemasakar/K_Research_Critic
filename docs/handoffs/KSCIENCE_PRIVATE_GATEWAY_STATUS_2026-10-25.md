# K_Science → KRC gateway status — 2026-10-25

Status: **PRIVATE GATEWAY DEPLOYED / FIRST READ-ONLY PROBE FAILED / E2E NOT ACCEPTED**

## KRC backend boundary

- KRC backend remains on `krc-cobalt`, loopback `127.0.0.1:19014`.
- Public research MCP remains loopback `127.0.0.1:9013`.
- The Sentinel-Remote gateway is a separate service on the Cobalt Tailscale address `100.118.132.8:19015`; it calls only the existing private backend and carries a six-tool allowlist.
- Existing MCP services and scientific data were not changed by the route setup. The route probe sent only `krc_capabilities` with an empty payload; it did not transmit the K_Science research corpus.
- The KRC operation response has not been verified through this route.

## Probe evidence

K_Science workflow #4, ID `40206034957`, ran from `main` with `probe_gateway=true` on 2026-10-25. Tailscale runner join and identity steps passed. The gateway POST returned HTTP 403.

Owner-provided journal output:

```json
{"event":"request_failed","error_type":"ValueError"}
```

The handler intentionally hides exception details. The precise denial stage is unknown, and successful dispatch to the KRC backend is not established. Do not claim a route acceptance PASS.

Run: https://github.com/kolemasakar/K_Science/actions/runs/40206034957

## Next engineering gate

1. Sentinel-Remote PR #31 head `e3edf6154256640c3e2442b00af670848b9f7ea8` contains the allow-listed failure codes and bounded request handling. 28/28 synthetic tests passed; the OIDC cryptographic test was not run because PyJWT was unavailable. The P2 thread is resolved. The candidate is not deployed on Cobalt.
2. Owner-stage the reviewed files and run `deploy/update_gateway.sh` on the gateway service only; keep `:9013` and `:19014` unchanged.
3. Run one new bounded `krc_capabilities` probe and require a matching request/response plus a `dispatch_completed` record.
4. Verify persistent replay rejection separately. This route test does not complete KRC P0, validate scientific claims, or authorize a K_Science research-data workflow.

## Cross-project records

- Sentinel-Remote route: `docs/KSCIENCE_KRC_ROUTE_V1_2026-10-25.md`
- Sentinel-Remote runtime checkpoint: `docs/KSCIENCE_KRC_GATEWAY_RUNTIME_CHECKPOINT_2026-10-25.md`
- K_Science integration: `docs/KRC_RESEARCH_INTEGRATION_V1_2026-10-25.md`
- K_Science next-chat handoff: `docs/BOOTSTRAP_PACKAGE_2026-10-25_KSCIENCE_KRC_GATEWAY.md`

FREE_ONLY remains in force. No provider/payment fallback or public endpoint is authorized.
