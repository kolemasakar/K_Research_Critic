# K_Science → KRC gateway status — 2026-10-25

Status: **PRIVATE krc_capabilities ROUTE PASS / REPLAY REJECTION PASS / SCIENTIFIC WORKFLOW NOT ACCEPTED**

## KRC backend boundary

- KRC backend remains on `krc-cobalt`, loopback `127.0.0.1:19014`.
- Public research MCP remains loopback `127.0.0.1:9013`.
- The Sentinel-Remote gateway is a separate service on the Cobalt Tailscale address `100.118.132.8:19015`; it calls only the existing private backend and carries a six-tool allowlist.
- Existing MCP services and scientific data were not changed by the route setup. The route probe sent only `krc_capabilities` with an empty payload; it did not transmit the K_Science research corpus.
- One bounded read-only `krc_capabilities` response has been verified through the route; this is not acceptance of a scientific research task or wider operation scope.

## Probe evidence

K_Science workflow #4, ID `40206034957`, ran from `main` with `probe_gateway=true` on 2026-10-25. Tailscale runner join and identity steps passed. The gateway POST returned HTTP 403.

Owner-provided journal output:

```json
{"event":"request_failed","error_type":"ValueError"}
```

The handler intentionally hides exception details. The precise denial stage is unknown, and successful dispatch to the KRC backend is not established. Do not claim a route acceptance PASS.

Run: https://github.com/kolemasakar/K_Science/actions/runs/40206034957

## Historical next gate before successful probe

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


## Superseding live route and replay result — 2026-10-25

The earlier workflow #4 HTTP 403 entry above is historical and is superseded for the bounded capability route by the following verified results:

- Workflow #8 (`40216011229`) returned PASS for read-only `krc_capabilities`; Cobalt journal recorded matching `dispatch_completed` for `KS-051748b26b824634b82a308855f94852`.
- Workflow #9 (`40216975746`) sent the identical signed envelope twice and reported `replay_status=REJECTED`; Cobalt journal recorded `dispatch_completed` for `KS-572b7cac7d0e415fb50571343352372d`, followed by `request_failed / envelope_replay / REPLAY_REJECTED`.
- The gateway-only updater confirmed the module updated, service active on `100.118.132.8:19015`, and existing backend listeners unchanged.
- PR #31 was merged into `Sentinel-Remote/main` on 2026-10-25 17:50:41 UTC; merge commit `bbeec5f5faed49d41c12a8a3c10c8eebbfab7537`, merged head `73753453ab6bf9945368b12c839d24ac4656ddc4`. The P2 slow-connection thread is resolved/outdated; deployed code has bounded workers and an absolute 10-second request-read deadline.

Run #8: https://github.com/kolemasakar/K_Science/actions/runs/40216011229  
Run #9: https://github.com/kolemasakar/K_Science/actions/runs/40216975746

**Accepted boundary:** this private route is verified only for one bounded read-only `krc_capabilities` call and persistent replay rejection. No scientific corpus was transmitted. Other operations, K_Science research-data transfer, KRC P0, scientific conclusions, and publication readiness remain separate gates. FREE_ONLY remains in force; no public endpoint or provider/payment fallback was enabled.


## Capabilities-only route merge update — 2026-10-25

Sentinel-Remote PR #32 was merged into `main` as merge commit `b07e232d002b656d12afc22d5a6fad04bd57bc9f`. The live gateway source now accepts only `krc_capabilities`; other candidate operations are rejected before backend dispatch. This is a source change only: deployment to `krc-cobalt` and a post-deploy capability probe remain pending. No Research operation or project corpus was sent. The connected ChatGPT KRC R3C surface has returned MEDIA capabilities only; that does not establish Research-handler readiness.


## Post-deployment verification — 2026-10-25

- Sentinel-Remote PR #32 merge commit `b07e232d002b656d12afc22d5a6fad04bd57bc9f` is deployed on `krc-cobalt`.
- Installed gateway module SHA-256: `0a84375e1b38b709fb685edf5972fce832862ead202258a4b5f9afd3bc58eb09`.
- Deployment reported module updated, service active, expected listener `100.118.132.8:19015`, and unchanged MCP backend listeners.
- K_Science workflow #10 (run ID `40226898639`, branch `main`, commit `648201864c8320d6e00924fbe1eaf99b52353c33`) completed successfully, including the bounded read-only `krc_capabilities` probe.
- This confirms the capabilities-only route. No `research.*` operation, scientific corpus, or research result was sent; broader research readiness remains unverified.
- Deployment-script defect found: committed updater expected SHA-256 `b3da222c9ff0ed00c4c7e0fed1e36b3f8bc626b90e21980de88edac58d4238f9`, which did not match the merged module. Only the temporary on-host updater copy was corrected to the verified digest above. The repository updater still needs a follow-up fix.


## Updater checksum follow-up — 2026-10-25

A draft fix is open as [Sentinel-Remote PR #33](https://github.com/kolemasakar/Sentinel-Remote/pull/33). It updates only `deploy/update_gateway.sh` so the expected digest matches the verified PR #32 module. This PR is not merged and has no production effect.
