# KRC Stage134 - live read-only privileged-release handoff

Date: 2026-11-24
Branch: research/stage134-bibliography-hardening-20261121
Disposition: PREDEPLOY_READONLY_VERIFIED / PRIVILEGED_INSTALL_NOT_RUN /
OWNER_APPROVAL_NOT_GRANTED / EXTERNAL_SIGNED_E2E_NOT_RUN / PRODUCTION_NO_GO

## 1. Exact release artifact (independent live read)

Target: authorized krc-cobalt Desktop Commander connection, UID krcops.
No root execution, service changes, provider calls, ledger mutations,
consent approval, or workstation access were performed in this check.

Release source:
- COMMIT_SHA: 62007ba9de3700a8fbd24a527c49b6392e3a41e2
- Archive: /home/krcops/krc-stage134-privileged-release-candidate-20261124/release-src.tar.gz
- SHA256: b9be29ea0737622d88dd02de324afde6a9179d3f7453c9e04b01a8d53971cd1f
- Manifest: /home/krcops/krc-stage134-privileged-release-candidate-20261124/SHASUMS.txt
- Manifest has 17 entries (15 Python source files and two JSON schemas).
- Archive SHA256 was recomputed live, not copied only from a prior report.
- Manifest and COMMIT_SHA were read live; individual archive member
  hashes and unpack/venv compatibility were not independently rerun
  during this read-only checkpoint.

Exact real source profile:
- Request: KS-50902e5cfe263a8c760fc2dfa4a26882
- Path: /home/krcops/krc-stage134-real-profile-crossref-20261124/profile.json
- SHA256: 5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7
- Profile SHA256 was recomputed live. Do not publish the private JSON
  bodies, raw provider captures or owner consent database.
- Earlier KRC live ledger checkpoint: PROPOSED / NOT APPROVED / NOT CONSUMED.
  The ledger state was not re-queried in this read-only checkpoint.

## 2. Live installed-service preflight

Using read-only systemctl show on krc-cobalt:

| Service | State | MainPID | NRestarts | Role |
| --- | --- | ---: | ---: | --- |
| krc-research-v2.service | active/running | 19631 | 0 | gateway, krcresearch |
| krc-project-n39-post.service | active/running | 19623 | 0 | broker, krcops |
| krc-sentinel-stage127.service | active/running | 27988 | 0 | Sentinel ingress |

The root-owned installed gateway and broker ExecStart lines both have
--enable-reviewed-staging-post and --enable-stage133-offline-operations.
Neither ExecStart line has --enable-stage134-bibliography.

- Gateway unit: /etc/systemd/system/krc-research-v2.service
- Gateway drop-in: /etc/systemd/system/krc-research-v2.service.d/20-project-pilot-post.conf
- Broker unit: /etc/systemd/system/krc-project-n39-post.service
- Existing installed code paths are documented in
  KRC_STAGE134_REAL_PROFILE_RELEASE_GATE_2026-11-24.md.
- Listener check: 127.0.0.1:19147 was listening, consistent with
  separate DOI rootless staging. This does NOT establish live MCP
  protocol acceptance in this particular check.
- Query of the rootless user service over systemctl --user was unavailable
  from this shell (no user D-Bus session); prior actual installed
  staging acceptance remains separately recorded in PR37.
- Remote execution layer rejected sudo -n -l; do not interpret this
  as fresh independent enumeration of sudo privileges. The prior
  documented krcops non-root installation boundary remains binding.

## 3. Root-operator release acceptance sequence (NOT executed)

1. Use separately authorized privileged access, never krcops permission
   bypass. Reverify SHA256 of the full archive, SHA256 of all 17
   unpacked files against SHASUMS.txt, import precedence, schema
   compatibility and both Python runtimes. Capture old immutable release
   identities, unit/drop-in hashes, service state and a rollback plan.

2. Install a NEW root-owned immutable Stage134 overlay without changing
   either existing Stage133 release in place. Review both gateway and
   broker source search paths; preserve existing service identities,
   runtime Python selection, secrets, UDS peer checks, nonce/consent/
   artifact databases and prior signed Stage133 functionality.

3. Deploy and test Stage134 code FIRST in default-DENY mode: no
   Stage134 marker and no --enable-stage134-bibliography in either
   service. Independently check normal Stage133 POST and GET, old
   nonce/ledger continuity, external bibliography POST denial and
   the public FREE_ONLY research route. Record process state and
   inspect new logs. Revert on any regression.

4. Before opening a positive Stage134 execution window obtain an
   EXPLICIT NEW OWNER APPROVAL for request
   KS-50902e5cfe263a8c760fc2dfa4a26882 and complete profile
   SHA256 5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7.
   Scope: one research.bibliography.audit invocation for FOUR
   previously captured FREE_ONLY Crossref JSON bodies only;
   Europe PMC capture absent, no PDF retrieval and no extension
   to other operations. Approval is neither inferred from development
   instructions nor inherited from earlier Science approvals.
   Verify live ledger remains PROPOSED before any state change.

5. Only after separate security and identity acceptance may a
   privileged operator install the independent root-owned 0600
   /etc/krc-stage132-post/enable-reviewed-stage134-bibliography
   marker and add the explicit CLI flag to BOTH matching broker
   and gateway service launch paths. Validate owner/mode/link
   custody and ensure no non-reviewed ingress expansion.

6. K_Science runs exactly one separately scoped signed Stage134
   OIDC POST + authenticated artifact GET with final patched client.
   Independently verify matching profile, HTTP 200 result, artifact
   byte SHA256, 403/409/410 negatives, TTL/expiry, rejected replay,
   durable ledger outcomes and unchanged Stage133. Any ambiguous
   HTTP outcome must be reconciled with the server ledger before
   any repeat request.

7. Disable Stage134 activation after the bounded staging acceptance
   and restore the previous immutable release and unit/drop-ins on
   failure. Do not reset or delete real consent, nonce or artifact
   ledgers. A successful test is not a Production release decision.

## 4. Current blockers / owner action

- PRIVILEGED_MAIN_GATEWAY_RELEASE: NOT_DONE, requires separately
  authorized root operator.
- EXACT_PROFILE_OWNER_APPROVAL: NOT_GRANTED.
- REAL_EXTERNAL_STAGE127_SIGNED_STAGE134_E2E: NOT_RUN.
- K_Sentinel PR39 and K_Science PR17 have independent SOURCE/TRANSPORT
  acceptance only; this preflight does not promote their E2E matrices.
- Production remains NO-GO.

Related authoritative source: docs/integrations/
KRC_STAGE134_REAL_PROFILE_RELEASE_GATE_2026-11-24.md.
