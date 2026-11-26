# KRC Stage134 deployment checkpoint and next implementation (2026-11-25)

Supersedes the NOT_INSTALLED state in the November 24 release handoff.
Owner SSH terminal evidence: root access via ubuntu sudo -n id; archive and
17 member hashes PASS; immutable release 62007ba9de3700a8fbd24a527c49b6392e3a41e2
prepared under /opt/krc-stage134; backup /var/backups/krc-stage134-20261125-190029.
Gateway and broker import exact new runtime PASS. Root-owned systemd
90-stage134-release.conf drop-ins installed for both services without
Stage134 activation flag or marker. Owner reports deployment and postinstall
preflight PASS; sockets retain krcresearch/krcops identities and group
krc-sentinel-ipc, mode 0660. Warning logs empty in reported window.
Independent Desktop Commander read-only service check: gateway PID50197,
broker PID50189, Sentinel PID50199, active, zero reported restarts.
Unauthenticated Stage127 correct-route POST 403; malformed bearer POST/GET
400; GET without authorization not confirmed. These do not prove valid-
identity operation denial or Stage133 functional regression.

Owner human consent for exact Stage134 request was recorded November 24;
live ledger approval was not activated or consumed in these checks.
Existing Stage127 transport is reused; no operation-specific Science sender.
See KRC_STAGE134_OWNER_ARCHITECTURE_BOUNDARY_2026-11-25.md.

Next KRC source-only increment: prepare the exact generic Stage127 request
body from a server-owned immutable proposal, not caller-created wire fields.
Reuse existing payload validation and release allowlist; no network, signer,
approval mutation, provider calls or execution. Domain intent-to-profile
translation and actual generic caller entrypoint remain separate work.
Functional Stage133 postdeployment regression, valid-identity default denial,
real signed Stage134 E2E and three-party acceptance remain NOT_RUN.
Production NO_GO. Do not activate the 24-hour grant prematurely.
