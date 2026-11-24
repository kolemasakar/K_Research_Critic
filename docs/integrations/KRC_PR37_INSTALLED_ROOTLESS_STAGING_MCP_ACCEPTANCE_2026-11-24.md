# KRC PR37: installed rootless staging MCP and actual systemd rollback

Date: 2026-11-24
Observation time: 2026-11-24T20:16:18Z
Disposition: MAIN_PRIVATE_MCP_SOURCE_TOOL_PASS /
INSTALLED_ROOTLESS_STAGING_PASS / REAL_SYSTEMD_ROLLBACK_3_OF_3_PASS /
LIVE_CROSSREF_PASS_EUROPE_PMC_UNAVAILABLE /
EXISTING_KRC_AND_SENTINEL_UNCHANGED / PRODUCTION_NOT_DEPLOYED.

## Scope and ownership

This is the owner-authorized KRC engineering staging implementation for
FREE_ONLY public DOI verification. The authorized KRC VM krc-cobalt runs
an isolated rootless user service under UID1002 (krcops), not the owner's
HP-OMEN or other personal local-computer disks.

No change was made to any root-owned /opt KRC release, system-wide
systemd service, installed Sentinel Stage127, owner consent ledger,
K_Science workflow admission, production server or private credentials.
The new staging endpoint is loopback ONLY and not routed by Sentinel.

## Main scholarly MCP tool wiring

Source commit: 8359fcfc3dea888e92e5e3a84545cd2c803e6c94.

- src/krc_research/public_doi_workflow.py: single FREE_ONLY public metadata
  function calling the audited Stage131 lookup_doi_metadata by default.
  Result schema KRC-PUBLIC-DOI-CHECK/1, with immutable false values for
  scientific_approval, full_text_verified and experimental_independence_verified.
  Publication/retraction clearance remains NOT_ESTABLISHED.
- src/krc_research/mcp_private_server.py: adds registered MCP tool
  krc_public_doi_check(doi) to the existing scholarly private MCP.
  Existing krc_doi_metadata, krc_doi_updates, krc_bibliography_audit,
  krc_scholarly_preflight, krc_inspection_receipt_review, signed-request
  and capabilities tools are preserved (seven existing tools).
- tests/test_public_doi_workflow.py: source-level tool registration
  preservation, metadata-only result shape and invalid DOI denial.

Full isolated KRC repository regression on exact source code commit:
1311 PASSED / 24 SKIPPED / 0 FAILED, exit 0. No provider network
queries in source test suite.

The staging service exports private scholarly MCP using the official
streamable HTTP SDK, not an ad-hoc stand-in HTTP endpoint.

## Pinned release and service configuration

Two private read-only release source snapshots are installed on VM:

- Candidate 8359fcfc3dea888e92e5e3a84545cd2c803e6c94 at
  /home/krcops/krc-stage131-doi-staging/releases/<candidate SHA>.
- Baseline 23418dda183ea2af818dcb746a24abc7fd83df0a at
  /home/krcops/krc-stage131-doi-staging/releases/<baseline SHA>.

Their selected native code blobs were recomputed and matched exactly
against Git before the releases were made read-only by owner krcops.
No symlinks replaced the installed root-owned service releases.

The installed rootless user unit:
krc-public-doi-staging.service
- Controlled by systemctl --user with krcops' own user D-Bus session;
  never by root systemctl or by direct modification of an existing unit.
- Source unit definitions version controlled as
  deploy/stage131/krc-public-doi-staging.candidate.service.example and
  deploy/stage131/krc-public-doi-staging.rollback.service.example.
- ExecStart uses the already available isolated Python MCP SDK venv,
  /opt/krc-public-mcp/venv/bin/python; exact KRC PYTHONPATH points to
  the pinned staging release under /home/krcops.
- Binds only 127.0.0.1:19147, no Tailnet or public listener.
- No Sentinel science key is supplied.
- NoNewPrivileges=yes; PrivateTmp=yes; ProtectSystem=strict;
  ProtectHome=read-only; UMask=0077; Restart=on-failure.
- Unit is static and explicitly started (not enabled for boot autostart).

## Actual installed service and MCP acceptance

First candidate service start:
- systemd MainPID 45015, ACTIVE/RUNNING, NRestarts=0.
- Official SDK MCP ClientSession.initialize + list_tools: PASS.
- Existing seven scholarly tool names preserved.
- New krc_public_doi_check tool present and callable.
- Malformed DOI with actual NUL returned MCP isError=True: PASS.
- Actual FREE_ONLY DOI network call for
  10.1016/j.proeng.2013.03.022:
  Crossref METADATA_ONLY; Europe PMC PROVIDER_UNAVAILABLE after
  upstream timeout; aggregated REVIEW_REQUIRED.
  This is a correct conservative partial-provider status, not an
  unqualified two-provider pass or scientific evidence approval.
- No paid provider, full text or user workstation disk was used.

## Real installed systemd service rollback and restoration

With the SAME krc-public-doi-staging.service user unit:

1. Candidate PID 45015 -> rollback baseline unit from GitHub ->
   systemd --user daemon-reload/restart -> baseline PID 45093.
   Official MCP ClientSession confirmed the new tool ABSENT while
   ALL existing legacy scholarly tools were PRESENT. PASS.
2. Reinstall exact candidate unit file from GitHub, daemon-reload,
   restart -> candidate PID 45114, not equal to baseline PID.
   Official MCP client confirmed new tool PRESENT again and
   malformed DOI rejected. PASS.
3. Final unit ACTIVE/RUNNING, MainPID 45114, NRestarts=0,
   ExecMainStatus=0, listener 127.0.0.1:19147, no leaking child
   staging server processes. PASS.

The unit file Git blob was verified against the pinned GitHub
candidate service template after restoration. Baseline was also
verified against its source template before the rollback.

This is an ACTUAL installed staging SERVICE restart and rollback,
not merely a code import/worktree switch. It is NOT an installed
production KRC service rollback, nor an external Stage127 signed E2E.

## Independent KRC / Sentinel / Science status

At final read-only check, the installed krc-research-v2,
krc-project-n39-post, krc-project-n39-read and
krc-sentinel-stage127 services all remained ACTIVE with NRestarts=0.
The installed krc-public-mcp.service was also ACTIVE/NRestarts=0.
kscience-krc-gateway.service was ACTIVE with a cumulative NRestarts=1
at observation; this task did not restart or mutate that unit.

K_Sentinel PR39 independent Stage134 source/transport report:
74/74 selected security/identity/half-close tests, 6/6 synthetic
Stage134 transport tests, and live unauthenticated HTTP denials
4/4 (POST 403, GET 401). One additional test module was NOT_RUN
due to unavailable fixture; no real signed Stage134 positive E2E.

K_Science PR17 independent exact-schema source QA:
66/66 client tests and 2/2 synthetic engine/client interop PASS.
Earlier signed private source-chain 2/2 was NOT rerun after the
amended Science client; no real external bibliography E2E.
Science acceptance matrix remains 4/48 technical cases PASS,
with bibliography 0/11 and Production NO-GO.

## Remaining release and security gates

- For PR37, a review and deliberate release of the main installed
  KRC/private integration is separate from this rootless staging
  demonstration. The new tool is available on the isolated
  127.0.0.1:19147 staging MCP, not through the deployed K_Sentinel
  ingress or the root-owned public KRC MCP service.
- PR36 research.bibliography.audit has separate immutable owner
  profile, replay, ledger, artifact and Stage127 operation admission.
  It remains default denied externally, source-only acceptance
  cannot grant execution permissions.
- KRC/Sentinel/Science must accept a real scoped Stage134 signed
  OIDC POST+GET and independent negative/replay matrix before
  any new external or production activation.
- Normal read-only KRC web research remains default-allowed:
  this release does not impose a general internet ban.
- Owner personal-computer local disks are forbidden without explicit
  instructions; this task used only the authorized KRC server VM.

Final: MCP SOURCE INTEGRATION PASS / INSTALLED STAGING SERVICE PASS /
ACTUAL STAGING ROLLBACK PASS / PARTIAL LIVE PROVIDER EVIDENCE /
EXTERNAL STAGE134 NOT_RUN / PRODUCTION NOT DEPLOYED.
