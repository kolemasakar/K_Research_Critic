# KRC shared science engine — K_Science offline integration acceptance
Date: 2026-10-25
**Status: I2 OFFLINE CONTRACT PASS; I3 ADAPTER PASS; I4 CONTROL POLICY REGISTERED; I5 SYNTHETIC OFFLINE PASS; I6 BOUNDED UNIT SUITE PASS; I1 FULL KRC P0 STILL OPEN; I7 CHATGPT PLUGIN DEFERRED**

## Owner decisions
Finish KRC functions and independent quality acceptance first. Make the engine reusable for K_Science and other expressly approved projects under Sentinel-Remote. Do not require or rush private-plugin ChatGPT integration; policy may change. FREE_ONLY, no publication, no media changes.

## Existing architecture checked
- `kolemasakar/Sentinel-Remote` main: actual remote-access authority is hybrid OIDC/Tailscale SSH/RDC, not a generic unrestricted proxy. Canonical docs ARCHITECTURE.md and SECURITY_MODEL.md confirm isolated project rights; KRC automation ceiling tier0/tier1/tier2_restart; K-Trader sole SentinelX-managed host.
- `kolemasakar/K_Science` main: private research repository initialized for geodetic methods, mathematical adjustments, concrete-strength modeling and experimental validation; no scientific assertions of validated strength estimation solely from geodetic data.
- `kolemasakar/K_Research_Critic` branch `agent/krc-public-media-r3-integration`: KRC private executor on loopback :19014 offers six existing MCP tools; end-to-end P0 scholarly completion still pending.

## Implemented
`src/krc_research/cross_project_contract.py` on KRC side:
- signed HMAC-SHA256 canonical JSON requests, fixed caller K_Science and KRC audience, versioned `kscience-krc-research-v1`, fixed ACL (six currently implemented read-only/audit operations), bounded 256 KiB JSON, ±300s timestamp, request ID format, fail-closed tamper check and replay rejection;
- **no production secret, no live network API**, in-memory replay registry fixture MUST become persistent atomic identity-scoped registry before route admission.
`tests/test_i2_cross_project_contract.py`: 10 tests.

K_Science private repo contains `research/integrations/kscience_krc_adapter.py`, five adapter tests and two synthetic full-cycle tests; local source data are hashed but not exported, owner approval remains False, external transport must be injected explicitly and defaults to NOT_CONNECTED.

Sentinel-Remote private repo documents policy/route in `docs/KSCIENCE_KRC_ROUTE_V1_2026-10-25.md`; no new credentials, roles, host routes or Tailscale ACLs deployed.

## Actual executed tests
All code staged from corresponding live GitHub files into isolated test dir `/tmp/krc-kscience-contract-20261025` on krc-cobalt under unprivileged krcops; reused project-only Python 3.12.3 and pytest 9.1.1 venv.
Command:
`PYTHONPATH=krc/src:science /home/krcops/krc-research-private/.venv/bin/python -m pytest -q krc/tests/test_i2_cross_project_contract.py science/tests/test_kscience_krc_adapter.py science/tests/test_i5_kscience_krc_offline_cycle.py`
**17 passed in 0.18s**.
Positive: K_Science signed request → injected synthetic Sentinel verification → KRC offline scholarly preflight `NO_GO` on missing evidence → result returned to K_Science without scientific owner signoff or changed measurements.
Negative: request tampering, wrong caller/key, replayed IDs, future timestamps, unauthorized operations, huge payloads and absent network transport.

This is **not a live cross-host transport** and does not certify scientific model claims. No real unpublished research data were transferred to KRC.

## Acceptance gates
I1 KRC full scholarly/factcheck/core acceptance: NOT_COMPLETE; see canonical KRC P0 roadmap and NO_GO.
I2 versioned offline API: PASS_BOUNDED.
I3 KScience adapter: PASS_OFFLINE.
I4 Sentinel ACL/security policy: REGISTERED_NOT_DEPLOYED.
I5 full scientific cycle: SYNTHETIC_OFFLINE_PASS; actual dataset/research cycle not run.
I6 17-test interoperability fixtures: PASS; independent production suite still pending.
I7 ChatGPT plugin integration: DEFERRED_BY_OWNER.

## Future transport requirements
Private authenticated route under Sentinel control; distinct service identity for K_Science; dedicated secret with fail-closed revocation; audit events; persistent atomic replay ledger with TTL; disallow any implicit inherited KGM/K-Trader/K_AI credentials; separate rights to K_Science data. No publication, public port exposure or privileged service mutation.
