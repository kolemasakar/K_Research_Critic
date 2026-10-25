# KRC №112 — private K_Sentinel preintegration acceptance package

Date: 2026-10-25. Executed exclusively on isolated `krc-cobalt` checkout `/tmp/krc-p0-offline-20261025`.

New `private_stage112.py` classifies signature/route authorization errors (`UNAUTHORIZED`), TTL failures (`EXPIRED_REQUEST`), ACL failures (`OPERATION_DENIED`), replay rejection (`REPLAY_REJECTED`), schema failures (`INVALID_REQUEST`), and internal handler faults (`HANDLER_ERROR`) into sanitized envelopes. Classification is based in part on message text from existing exceptions and is not yet a stable typed-error infrastructure. No listener, no production MCP change.

Approval evidence uses existing signed-key HMAC prototype and inspection receipt append/verify chain. Demonstrated tamper detection. This provides hash integrity and configured-key possession, **not** identity attestation, immutable storage, or independent final human review. No scientific approval granted.

Eight new tests cover success, wrong signature, expiry, ACL deny, replay, malformed message, tampered chain and unknown signer. Complete isolated KRC suite **334/334 PASS**, 2.81s, exit code 0. The venv's jsonschema is still provided from `/tmp/krc-mcp-sdk-isolated` without package installation.

Preintegration checklist: four private offline operations supported; input schemas DRAFT and not complete; output schemas not deployed; structured error response adapter isolated; replay registry must be durable in a deployed transport; authenticated owner CriticProfile approval not accepted; default bibliography adapter may contact external providers; zero test must use capabilities read or public MCP tools/list only; K_Sentinel private network route WAITING_FOR_SENTINEL_READY. FREE_ONLY. Production/MEDIA/public unchanged. FINAL NETWORK ACCEPTANCE NO_GO.
