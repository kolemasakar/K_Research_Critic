# KRC Stage124 — staging entrypoint and unit-template readiness (2026-10-28)

**No service installation, no activation, no credentials provisioned.** Development-only code and a non-installed systemd example.

Artifacts:
- `src/krc_research/staging_entrypoint124.py`: explicit `--config` CLI, checks private regular config owner/mode, exact config fields, separately loaded owner-only secrets >=32 bytes, distinct non-root configured peer UID, refuses existing/symlink socket path, composes Stage123-C verified UDS backend. This is a candidate requiring independent deployment security review.
- `docs/integrations/krc-research-v2.staging.service.example`: non-installed systemd template for `krcresearch` user, `krc-sentinel-ipc` group and restricted UDS/state directories. Parent ownership, runtime directory creation, systemd Python dependencies, socket 0660/ACL, key file ownership, unit security and rollback **NOT VERIFIED**. Never activate unreviewed example as-is.
- `tests/test_staging_entrypoint124.py`: four file-protection and config parsing tests.

**Focused isolated regression: 76 passed in 9.01 seconds**, including four entrypoint tests, legacy science dispatch tests and Stage123 auth/UDS/artifact tests. This is not the full repository regression nor a full authenticated 4-operation UDS run. Prior full-suite baseline 884 PASS, 8 FAIL, 17 SKIP (legacy Core Skill/Builder snapshots); full suite not rerun.

**Next KRC-owned acceptance gates:** implement four-operation operation-specific positive/negative contract fixtures through the combined verified UDS, approved offline bibliography adapter; verify protected directory and socket group ownership with an actual dedicated staging account; verify permission/secret/key rotation and service stop/restart behavior; exercise 20s deadlines and crash/partial write; immutable artifact stream and 200MiB quota stress; obtain real Sentinel OIDC/Tailscale provenance via independent live staging E2E. Use no production or Stage114 v1 changes, FREE_ONLY.

Decision: **ENTRYPOINT TEMPLATE READY FOR REVIEW / STAGING SERVICE NOT DEPLOYED / E2E NO-GO / PRODUCTION NO-GO**.