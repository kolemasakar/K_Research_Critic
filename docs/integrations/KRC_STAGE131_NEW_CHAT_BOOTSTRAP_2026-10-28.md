# KRC — NEW CHAT BOOTSTRAP — 2026-10-28 (Stage130 → Stage131)

## Authoritative checkpoint
Read first:
`docs/integrations/KRC_STAGE130_PROJECT_CHECKPOINT_AND_HANDOFF_2026-10-28.md`
in `kolemasakar/K_Research_Critic`, branch `agent/krc-public-media-r3-integration`, checkpoint commit `19105985abd8ebedb5c704163807217427d6ea77`.
Do NOT assume the old runtime has received newer GitHub code.

## Mission
Priority: safely finish KRC internal science signature authorization and isolated Stage131 proof; coordinate with K_Sentinel v2 ingress and K_Science final four-operation contract and real bibliography metadata audit; then joint E2E-01–05.
Mode: STAGING ONLY / FREE_ONLY / production NO-GO. No public release. No unpublished science material upload without new explicit consent.

## Confirmed working
- Live `krc-research-v2.service` manually active, PID 37979, 0 restarts at last read; isolated UDS `/run/krc-research-v2/backend.sock`, backend UID988 `krcresearch`, Sentinel UID987 `krcsentinel`, shared GID984 `krc-sentinel-ipc`.
- Existing Stage114 v1, K_Science gateway and KRC Public MCP active, unchanged. Existing workflow targets legacy :19015 and is **not** a v2 E2E proof.
- Sentinel true local Transport HMAC valid (HTTP409 because science payload intentionally incomplete), bad HMAC HTTP403; /healthz 200 staging. Real GitHub OIDC/Tailscale origin through new v2 ingress NOT RUN.
- KRC source Stage128–130 has opt-in internal `science_signer127.py`, `consent_custody128.py`, optional `staging_service123c.py` wiring, `bibliography_bounded129.py`, `metadata_store130.py`. 38/38 selected synthetic/isolated regression PASS; current *running* daemon contains older source and NOT these additions.
- User manually created root-controlled `/etc/krc-research-v2` and `approvals`, `approvals-test`: root:krc-sentinel-ipc mode 0750; stored config+secret access by krcresearch confirmed. Test-only KRC module `/opt/krc-consent-test/consent_custody128.py` root:root mode 0644, SHA256 `bc8ee4406a5628347ab24ef0f91a634394ab691276dea7c0bfe55fb0e3d228af`. Separate test replay DB `/var/lib/krc-research-v2/consent-test/replay.sqlite`, krcresearch:krc-sentinel-ipc mode 0600.
- ACTUAL Linux UID988 + root-owned SYNTHETIC grant: changed payload denied, first use PASS, replay denied, replay after reopen denied, wrong principal denied. Grant `synthetic-consent-stage130-001` is CONSUMED. This does NOT mean real user science consent.
- Bibliography policy: FREE_ONLY Crossref+Europe PMC public DOI metadata read-only; full text/scientific evidence independent and not certified by metadata. Live provider calls NOT RUN, active bibliography_fn remains None. Metadata cache/TTLs and audit code tested synthetically.

## Main blockers / no-claims
- No real authenticated Sentinel v2 ingress. PR `kolemasakar/Sentinel-Remote#38` Draft. Verified GitHub OIDC `sub`/full workflow_ref do not match current KRC transport allowlist `K_Science`/`refs/heads/main`; strict post-OIDC projection exists as candidate but not integrated into live ingress.
- Real human approval issuance/attestation is NOT implemented or verified. File custody proves service permissions, not consent provenance. Never issue grants just from incoming payload boolean.
- Internal Science signer NOT deployed into active daemon; no actual live scientific success.
- Bibliography live provider policy needs egress limit, durable provenance, error/429 cases and explicit public DOI scope before live verification.
- `kolemasakar/K_Science#6` Draft contains unsigned synthetic packages and 29 NOT_RUN cases. Four operation input/output/error schemas are still DRAFT, not final.
- E2E-01 full NOT RUN, E2E-02–05 live NOT RUN; no production acceptance.

## First actions in the next chat
1. Read canonical checkpoint and latest issue #28 / PR #38 / PR #6; verify repository head and current process states independently via connected GitHub/Remote Desktop Commander.
2. Plan Stage131 **distinct isolated backend** with distinct UDS/state, immutable pinned source SHA, and no interference with active Stage126/Stage114. Complete root-issued consent workflow design and real UID/security negative tests. No silent enable/start of permanent services.
3. Coordinate Sentinel protected v2 ingress entrypoint, durable OIDC jti replay, Tailnet StableID/ACL and claims projection; do not repoint :19015.
4. Test metadata-only bibliography on approved PUBLIC DOI with read-only nonpaid provider and no claims of primary scientific proof; prepare final schema and handoff for K_Science.
5. Only after signed identity, owner consent and positive/negative tests run E2E-01–05. Pin KRC/Sentinel/K_Science SHAs, keep true results versus NOT_RUN.

## Safety/operational constraints
- Do not read or output HMAC keys, MACs, raw JWT or other secrets.
- Remote Desktop Commander operates unprivileged and may forbid sudo; user runs one short SSH sudo command at a time after careful review.
- Do not execute unreviewed code as root. Preserve existing production, Stage114 v1 and staging services and verify rollback.
- Scientific approval != transport authenticated; synthetic metadata != independent verified source.
- User replies Ukrainian, numbered; expects direct actions, tests, GitHub sync and concise manual instructions only if privileges require them.
