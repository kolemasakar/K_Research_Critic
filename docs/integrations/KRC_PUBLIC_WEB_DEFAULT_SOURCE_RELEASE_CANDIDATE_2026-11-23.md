# KRC core public research: narrow source release candidate

Date: 2026-11-23
Status: SOURCE_TESTED / PRE-DEPLOYMENT REVIEW / NO INSTALLED CHANGES
Owner decision: routine public searching, fact-checking and FREE_ONLY
internet metadata retrieval is a standard KRC capability.

## Release candidate identity

- Narrow PR: https://github.com/kolemasakar/K_Research_Critic/pull/37
- Source commit tested: db1a201eeb7281511609fadd800df16d436b481c
- Base: science/stage133-offline-expansion-20261120
- Base commit: cfdfe1f281b8c408cde7a1f87e030e32e0141570
- Exactly 10 source/test files changed.
- This patch is intentionally independent of the remaining Stage134
  research.bibliography.audit private signed-route implementation in PR36.
- Default-on FREE_ONLY read-only DOI lookup is implemented in the Stage131
  adapter/composition route. Explicit OFFLINE remains usable by
  allow_network=False, not globally imposed.

## Acceptance evidence

In an isolated, source-only worktree on the authorized KRC VM
(krc-cobalt, not an owner laptop), execute:
PYTHONPATH=src PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
python -m pytest -q -p no:cacheprovider tests

The full test suite completed:
- 1299 PASSED
- 24 SKIPPED (not claimed as validated)
- 0 FAILED
- Runtime: 70.88 seconds; process exit code 0.

No external metadata providers were called by the test suite; network
proxies were disabled for its child environment. Integration and
provider-failure behavior were exercised with isolated injected
responses, including bad URL, redirect, MIME type, response size,
timeout, rate-limit handling and incomplete catalog coverage.

Independent read-only smoke against the CURRENT INSTALLED KRC public
discovery module (not this candidate Stage131 adapter):
- Crossref public search: METADATA_RETRIEVED, two public records, PASS
- OpenAlex public search: METADATA_RETRIEVED, two public records, PASS
- scientific_evidence_verified=false; no owner grants, paid resources,
  local user computer drives or production state mutations.

This confirms the basic deployed discovery capability is already
network-functional. It does NOT constitute installed deployment or
on-service acceptance of the new Stage131 lookup behavior.

## Operational difference and security gates

Previous Stage131 adapter required allow_network=True and the
composition wrapper additionally required provider_approved=True
for any publicly available metadata lookup. The candidate removes
both per-query gates. A user's normal instruction to research public
information already authorizes public read-only search.

- HTTPS only, bounded replies and deadlines, strict exact provider
  URLs, redirects blocked, no authenticated or paid APIs.
- No arbitrary URL supplied to the KRC signed endpoint.
- No automated claims of scientific independence, full-text validation,
  publication eligibility or retraction clearance.
- The existing KRC private Stage131/132/133/134 signed operations
  retain separate immutable owner consent and external operation
  admission, not a general browsing ban.

## Deployment boundary and rollback preparation

- Installed KRC gateway and Sentinel services have NOT been modified.
- DO NOT deploy the broad 28-file Stage134 PR36 as a shortcut for this
  public research correction.
- Before any release, independently review this exact ten-file diff,
  verify staging unit/operational smoke and the installed destination
  version, preserve the prior immutable release, and record its SHA.
- On failed staging checks, restore the prior installed immutable
  release and verify public discovery, process health and consent
  deny/replay invariants. Do not delete consent or artifact databases.
- Owner local-computer disks remain prohibited without explicit,
  task-scoped instruction.
- Stage134 signed bibliography external E2E and full security acceptance
  remain an independent workstream, Production NO-GO for that new route.

Release candidate PASS does not certify that source-only changes have
been promoted to a currently running service.
