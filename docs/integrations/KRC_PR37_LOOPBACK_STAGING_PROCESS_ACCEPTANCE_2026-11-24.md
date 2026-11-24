# KRC PR37: actual loopback HTTP staging and rollback acceptance

Date: 2026-11-24
Status: ISOLATED_LOOPBACK_HTTP_STAGE_PASS / ROLLBACK_PROCESS_PASS /
INSTALLED_KRC_SERVICE_NOT_MODIFIED / PRODUCTION_NO_GO

## Scope

The owner instructed KRC to perform its next available tasks, including
staging checks and rollback readiness for PR37. On authorized KRC staging
VM krc-cobalt, executed real short-lived HTTP server processes on
127.0.0.1 with a shared ephemeral port. The server is a controlled
test-only harness calling the existing Stage131 KRC DOI adapter. It is
not the installed KRC public/Science gateway nor the Stage127 ingress.

Code under test:
- Baseline: 23418dda183ea2af818dcb746a24abc7fd83df0a
- PR37 candidate: d7b48468c858f841f57ca44c25e3bb67232ecf61
- Reproducible test-only script pinned to PR37:
  tools/stage131_public_doi_staging_rehearsal.py
  (script SHA commit 2c2f34f1901ebc284955dcdcc12e923e828c83f4)
- Public reference DOI: 10.1016/j.proeng.2013.03.022
- No owner-computer local disk was accessed. No installed source,
  service, systemd unit, secret, consent ledger or artifact DB changed.

## Actual 3-phase server/process test

For EACH phase the harness:
- Starts a real child HTTP server in a separate Python process with
  its own pinned PYTHONPATH and a single ephemeral loopback port.
- Waits for live GET /health returning the correct source commit.
- Probes unknown route (404), invalid DOI (400), forbidden POST
  (405), and a deliberately encoded NUL in DOI.
- Sends a genuine loopback HTTP GET /v1/public/doi?doi=<DOI>,
  parses JSON, and requires the source-specific conservative
  bibliography classification.
- Stops the child server, waits for process termination, and
  verifies that the loopback port is free before the next stage.

| Phase | HTTP DOI response | Invalid control DOI | Process/port |
|---|---|---|---|
| Baseline 23418dd | 200 / PROVIDER_DISABLED | 200 (historical deficiency) | STOPPED/FREE |
| PR37 staging d7b4846 | 200 / COVERAGE_GAP_METADATA_ONLY | 400 (fail closed) | STOPPED/FREE |
| Baseline rollback 23418dd | 200 / PROVIDER_DISABLED | 200 (restored historical behavior) | STOPPED/FREE |

ALL phases PASS. Restarting the previous code restores its old
behavior, including its older and weaker input validation; this is
a documented rollback consequence, not a claim that older input
validation is secure. The staging test did not migrate any state.

The first ad hoc loopback run successfully reached the live Crossref
and Europe PMC public HTTPS APIs for the candidate DOI with a
metadata-only result. A later replay had a real Europe PMC upstream
TimeoutError. Because network availability does not prove or refute
service release/rollback behavior, the version-controlled script
uses deterministic in-memory provider JSON fixtures for the
three process lifecycle stages. This is an exact and repeatable
functional HTTP test, NOT a fresh real-provider receipt or
cryptographic provider-origin attestation.

The real default-on public HTTPS DOI smoke on the same candidate
source had previously passed, separately:
Crossref=METADATA_ONLY; Europe PMC=NOT_FOUND;
merged=COVERAGE_GAP_METADATA_ONLY; scientific approval=false.

## Reproduction (authorized KRC VM only)

Both arguments must point to isolated, pinned VM source worktrees,
NOT a desktop, personal workstation, or installed /opt KRC release.

PYTHONDONTWRITEBYTECODE=1 python -B \
  tools/stage131_public_doi_staging_rehearsal.py \
  --baseline /home/krcops/krc-public-web-rollback-baseline-20261124/src \
  --candidate /home/krcops/krc-public-web-release-candidate-20261123/src \
  --baseline-sha 23418dda183ea2af818dcb746a24abc7fd83df0a \
  --candidate-sha d7b48468c858f841f57ca44c25e3bb67232ecf61

Actual executed GitHub version:
git show 2c2f34f1901ebc284955dcdcc12e923e828c83f4:tools/stage131_public_doi_staging_rehearsal.py
This can be piped into a Python process with the above arguments.
Do not use arbitrary unverified worktree paths.

## Other acceptance evidence

- Independent PR37 code security findings fixed.
- Full PR37 repository regression on the pinned source commit:
  1308 PASSED, 24 SKIPPED, 0 FAILED.
- Precise original baseline from 2026-11-24 independently checked
  out on VM. No personal machine access.
- Four installed KRC/Sentinel services remained ACTIVE with
  NRestarts=0 at last post-test check.
- PR37 still draft, not merged, not installed into running KRC.
- Existing installed KRC public_discovery already supports live
  FREE_ONLY Crossref and OpenAlex public internet research; this
  additional Stage131 DOI adapter is not yet wired to the
  installed service endpoint.

## Outstanding true installation gate

A real KRC service rollout would need a reviewed, explicit call
path from the installed service (or an authorized KRC read-only
command interface) to the Stage131 DOI adapter, immutable release
record, rollback of the actual running service and operational
post-restart acceptance, not just this loopback harness.
The existing root-owned /opt service was deliberately not
modified, and no attempt to bypass its release permissions
or Stage127 signed Science operation allowlist was made.

KRC private Stage134 signed bibliography E2E remains a separate
three-project authorization and transport acceptance task.
Production remains NO_GO for the new signed route.
