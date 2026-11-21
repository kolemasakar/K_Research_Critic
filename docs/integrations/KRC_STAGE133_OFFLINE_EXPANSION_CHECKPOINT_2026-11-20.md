# Stage133 offline operation expansion checkpoint
Date: 2026-11-20
Disposition: SOURCE_CANDIDATE / ISOLATED_WIRE_PASS / NOT_INSTALLED / NO_SEND / PRODUCTION_NO_GO.
Base: 8694172a2aa0c6f0a4f35007120fc0572dbbb1c1. Actual external matrix 2/48 accepted; 46 not credited. Do not replay spent grant.

## Scope
Opt-in offline allowlist for research.evidence.preflight and research.inspection.review on existing producer/relay/GET route. Default set remains profile.validate; runtime entrypoint unchanged. Bibliography explicitly denied pending provider contract. No Sentinel source/config change. Exact stored profile operation/payload and server-owned consent/ledger required. External preflight user_profile_approved rejected; internal engine compatibility flag derived from stored profile, with actual owner claim mandatory before dispatch. Inspection rejects caller trace_verified=true; no independent trace verification implied. No new identities, network provider calls, credentials, consent or live execution.

## Tested
Actual krc-cobalt, isolated existing Stage132 candidate copy, baseline blobs match GitHub. Original profile regression plus expanded boundary, actual AF_UNIX relay, loopback HTTP through pinned Sentinel release b2a8064027c887065522b4b96f846c3d0540194f and existing legacy source overlay. Synthetic OIDC/Tailnet, temporary private state, fixture keys. 24/24 PASS, 13.83s, no skips. Initial combined run 22/24 due fixture private umask; fixed fixture and reran. Absence of consent403, disabled route403, false authority assertion403, payload mismatch409, one execution, descriptor/GET/hash/task correlation and replay409. Scientific approval false. No actual external E2E credited. All four services active, PIDs broker10179/gateway10271/reader5267/Sentinel10278, NRestarts0.

## Remaining gates
- Strict external schema and nested input constraints (manuscript/search-run types, detector provenance), semantic checker reconciliation with partial search counts and detector states, malformed nested input rejection before consent consumption. Full regression and independent review pending.
- K_Science default-off sender and operation-specific receiver; current main pinned to profile pilot. Reconcile two externally verified cases in matrix. No blanket approval.
- Explicit opt-in runtime config for both relay roles, cross-UID release parity, rollback, coordinated staging switch.
- Specific owner approval of each real pilot, no retry or reuse of prior grant.
- Bibliography FREE_ONLY provider readiness separate. No external provider calls. Sentinel transport only.

Tested blobs:
- src/krc_research/stage132_project_post_wire.py d49fce41b8a2bcbc457ab9c6c0198e00d86bcee4
- src/krc_research/stage132_project_post_contract.py 1c75cd123dcbfca152b070047b983be5e8aed285
- src/krc_research/stage132_project_post_relay.py 040da938b35c7f3260253a531d70434a7cacdb38
- src/krc_research/stage131_project_research_route.py 2bda58e666b60315257d33d6e8db64e74f4ab088
- tests/test_stage132_project_post_relay.py ca890dee7f8d656fe88e60f0333d574147d1221e
- tests/test_stage133_offline_expansion.py 09f55f14e7ca6dd0811ee618ff1e46b1b2bc5783
