# N39 restricted KRC read service: installed STAGING internal acceptance
Date: 2026-11-18
Disposition: INSTALLED_INTERNAL_SMOKE_PASS / POST-INSTALL_READ_ONLY_PARITY_PASS / EXTERNAL_GET_OFF / PRODUCTION_NO-GO.

## Owner-executed installation evidence
Owner ran the approved root-only install script, source 39a0ef94abf1e67ba27234c164cb10dbab40986c, SHA256 eda3ab02893e255839c11c1c14ddde530e24b5c0e016b3527e29177c9489e2da. The user supplied the complete successful terminal output in the KRC project chat.
- Script and archive checksums, archive allowlist, all eight pinned source/config/unit/schema hashes: PASS.
- GET_FLAG_OFF, RETRIEVAL_KEY_SEPARATION, KRC_DEPENDENCY_AND_AUTHORITY_IMPORT, SENTINEL_DEPENDENCY_AND_KEY, SENTINEL_NO_PRIVATE_STATE_ACCESS: PASS.
- ACTUAL_UID_GID_SOCKET_READONLY_MOUNTS, LIVE_UID987_DESCRIBE_READ_SHA_EOF, DURABLE_NONCE_REPLAY, BAD_MAC_AND_WRONG_SCOPE_DENIED, ACTUAL_WRONG_UID_DENIED, PRODUCER_STATE_UNCHANGED: PASS.
- Final KRC_READ_INSTALLED_INTERNAL_SMOKE_PASS_GET_OFF and PRODUCTION_UNCHANGED.
Actual root-only smoke evidence comes from the owner-run script, not a second independent privileged replay.

## Post-install verification executed by KRC through existing authorized UID1002
- Immutable root-owned release /opt/krc-project-n39-read/46aebfcd52117d564624fd708709a097bb533362; current symlink resolves to exact pin. No group/world-writable entry or non-root ownership detected.
- Recomputed eight installed package file SHA256 values plus installed unit hash; all match previously reviewed manifest.
- New unit krc-project-n39-read.service loaded, inactive, PID0; configured krcops / krc-sentinel-ipc. New UDS absent after smoke. No restart or activation in this verification.
- Config dir root:984 0750; dedicated nonce state dir krcops:984 0700; nonce SQLite UID1002 mode0600, four persisted rows, PRAGMA quick_check=ok. Retrieval key contents were not inspected or disclosed in post-install verification.
- Existing Stage127 active PID157909 at reviewed pin 963540fe08055b65f0b25a5a6484a61712c282f8; Stage131 active PID46327; Research v2 active PID37979. All three PIDs equal preinstall baseline.
- Fresh local canonical Stage127 GET for a synthetic selector returns HTTP404 JSON NOT_FOUND.
- Existing approved technical fixture KS-b190d3c43f52c07516170ecebbcd7641 remains COMPLETED/COMPLETE. Actual installed ProjectArtifactAuthority re-verified 398 bytes and SHA256 840fcb4faf75519d8a55b0569720e9912d35d969c6ea2165b82086d66225042e. Exactly one science replay task still recorded. No new dispatch or consent mutation.
- This verifies installed parity and producer integrity, not external OIDC GET or independently repeated root smoke.

## Next gate
K_Sentinel and K_Science: record installed internal smoke evidence; review temporary canonical Stage127 GET ON procedure with exact rollback. Owner must separately approve temporary external activation. Activate only restricted KRC UDS and existing canonical Stage127 listener; no production activation, no scientific/provider execution. External N01-N40 remains 0/40 FULL PASS until actual evidence accepted. Disable GET and stop new read unit after tests; preserve nonce, producer and audit state. Prior POST T3 acceptance stands; recheck POST after activation/deactivation. Recurring audit publisher remains pending, outside this installation scope.
