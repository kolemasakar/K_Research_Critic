# KRC Stage133 unified regression and rootless deployment preflight
Date: 2026-11-21
Scope: KRC-owned Stage133 source only; no service cutover, new science dispatch, consent creation, private credential disclosure or network/provider access.
Disposition: UNIFIED_SOURCE_ACCEPTED / RELEASE_PACKAGE_PRECHECK_PASS / LIVE_CROSS_UID_NOT_RUN / PRODUCTION_NO_GO.

## Exact root cause and remediation
Two KRC source snapshots were imported in a single pytest process, selected by test import order. Original Stage131 verified source commit 4e8352e26eb836c10ce7bbcaf5c7b1b84da5dd55 had an older signed Artifact GET HTTP/UDS server. Newer Stage133-pinned source Git blob 19df3c275460c747274bb790f46fe3a6448b29b7 requires explicit request write-half-close and has current descriptor behavior. Some historical Stage131 test clients sent Content-Length bytes but did not shutdown(SHUT_WR). Thus Stage133-first runs timed out; Stage131-first runs loaded older UDS code and Stage132 descriptor GET returned 502 UPSTREAM_FAILURE. This was real source/fixture incompatibility, not a demonstrated defect in the installed runtime.

A second historical contract drift was discovered when using one authoritative source tree: the new SignedArtifactReadBoundary requires an independent retrieval_authorizer after completed RequestLedger, whereas old Stage131 tests instantiated it without an authorizer. This correctly denied with 403 (rather than returning previously expected success, expiry, corruption, or length errors). Updated test fixtures supply an exact synthetic retrieval-authorizer only in approved positive cases. Added negative test proving that completed ledger without retrieval authorization returns 403 and no bytes.

No production authorization check, GET/UDS timeout or HTTP framing security rule was weakened. No deployed source edited. Historical test expectations corrected against the newer protocol in isolated unified copy.

## Unified source and acceptance runs
Working tree: /home/krcops/stage133-unified-acceptance-20261121 (isolated; does not modify original Stage131 or installed Stage132). Copy of 177 source baseline tests plus Stage132/133 specific tests, 185 test modules before extra frame test, namespace package uses a single Stage133 src root. K_Sentinel pinned release b2a8064027c887065522b4b96f846c3d0540194f, K_Science receiver pinned from installed Stage132 fixture. All data synthetic.
- Ordinary-order unified regression before extra explicit framing tests: 1182 PASS,17 SKIPPED,0 FAIL in 56.65 s.
- Reverse-file-order unified regression after extra two strict framing tests: 1184 PASS,17 SKIPPED,0 FAIL in 73.62 s.
- Forward-order unified regression with same final test inventory: 1184 PASS,17 SKIPPED,0 FAIL in 60.53 s.
- Separate preinstalled Python 3.12 / pytest 9.0.3 remediation-probe environment: 1184 PASS,17 SKIPPED,0 FAIL in 59.98 s (independent dependency/pytest environment; same source and host).
- Independent focused N39+UDS historical fixtures: 14 PASS.
- Extra test: Content-Length followed by undeclared bytes => 400 before any dispatch; proof of no premature dispatch until write-half-close => dispatch exactly once after EOF.
- Runtime opt-in synthetic fixture remains explicit default-off. Stage133 scientific approval remains false.
The 17 intentionally skipped Stage131 integration tests were not credited as passes. No live external Stage133 E2E credited.

## Rootless release package and security preflight
Reproducible builder: tools/stage133_release_preflight.py; package generated locally only:
  /home/krcops/stage133-unified-acceptance-20261121/stage133-release-candidate-20261121/stage133-offline-release.tar
  SHA256 d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6
  16 archive members, strict explicit allowlist and SHA256SUMS; no symlinks, absolute/parent paths, special files, credentials, private DBs or tokens.
Pinned Stage132 template source archive SHA256 e1e03b5afd04d22f033711c02272e9c4b3160fc1c8c642a73988bc5c5c750993. Package includes 7 broker-source files, 3 gateway-source files, strict Stage133 schema and four deployment templates (broker/gateway default-off and reviewed opt-in).
Package verification (separate local archive verification and sha256sum -c): PASS.
Broker source imports PASS using installed /usr/bin/python3 and previously pinned private read source. Gateway source imports PASS using installed /opt/krc-research-v2/.venv/bin/python and original gateway source. Opt-in unit and default-off unit pass systemd-analyze verify with zero diagnostics. CLI and marker checks are staged source only.
Default-off templates omit --enable-stage133-offline-operations and retain profile-only. Reviewed opt-in requires BOTH broker and gateway flags and a root-owned 0600 /etc/krc-stage132-post/enable-reviewed-stage133-offline marker. No new external listener.
Installed Stage132 broker, gateway, Reader and Sentinel remain active with unchanged PIDs and NRestarts=0 at preflight. This is a static and unprivileged import/package dry-run; not a root-owned service installation, not a cross-UID functional test, not a rollback drill.

## Still required before STAGING live enablement
1. Independent root/operator review of this EXACT archive SHA and unit templates; stage root-owned immutable release and execute actual UID1002/UID988, group984 socket/key custody and nonce checks without leaking keys. Re-run existing verified Stage132 baseline and graceful rollback plan. Existing Stage132 operator script pins an older archive and MUST NOT be used directly to install Stage133.
2. Independent authorized K_Science client ACK and operation-specific artifact/result validators. Owner must separately approve one precise immutable profile per live science operation. No automatic redispatch of spent grants.
3. Coordinated maintenance when enabling broker and gateway. Stage127 transport availability and signed GET must be monitored and restored on rollback.
4. E2E tests, matrix updates and any provider network expansion remain separate work; bibliography external APIs are not enabled by this checkpoint.
5. External reviewer/other independent party signoff is NOT claimed from this self-contained acceptance. Root cross-UID and live deployment remain NO-GO.

## Audit outcome
KRC isolated source and rootless package readiness: PASS.
Third-party independent security attestation: NOT RUN.
Actual Stage133 deployment/cross-UID acceptance: NOT RUN.
Science E2E matrix: unchanged 2/48 historical accepted; 46 pending.
Production: NO-GO.
