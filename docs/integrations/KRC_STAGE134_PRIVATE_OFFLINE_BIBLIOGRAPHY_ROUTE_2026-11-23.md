# Stage134 offline bibliography owner-approval route: source acceptance

## Architectural clarification: KRC research network is not offline-only

Per the owner directive on 2026-11-23, OFFLINE in the title refers
**only to this reproducible signed private Stage134 snapshot test route**.
It is not a restriction on KRC's fundamental public internet research.
Free public web searches, Crossref/OpenAlex/Europe PMC lookups and
independent fact-checking are permitted as routine research by default.
This document's external E2E restrictions apply to signed scientific
execution and deployment, not to the research engine's public reads.

Canonical owner policy:
https://github.com/kolemasakar/K_Research_Critic/blob/main/docs/RESEARCH_NETWORK_ACCESS_POLICY_2026-11-23.md

Source implementation correction:
docs/integrations/STAGE134_PUBLIC_INTERNET_RESEARCH_CORRECTION_2026-11-23.md

---

Date: 2026-11-23
Disposition: SOURCE_ONLY_OFFLINE_SIGNED_PRIVATE_ACCEPTED /
EXTERNAL_WIRE_NOT_ENABLED / NOT_INSTALLED / NO_NETWORK / PRODUCTION_NO_GO.

## Scope and release safety

This implementation adds the source-only ability to process immutable,
caller-supplied offline bibliography metadata snapshots under the existing
KRC private single-owner consent and internal science-signing process.

It is NOT a signed external Stage134 E2E, a new deployed KRC operation,
a Crossref/Europe PMC API authorization, or a production change.

- ProjectResearchRoute(..., enable_stage134_offline=False) remains the
  default, including the installed private CLI and the Stage132 POST boundary.
  The explicit True flag is only used in isolated source tests.
- The Stage132 external enabled_operations allowlist still excludes
  research.bibliography.audit. Its external POST returns HTTP 403.
- The Stage132 relay and Stage127 Sentinel ingress are unchanged and
  cannot be made to accept bibliography.audit by a client-provided boolean.
- No installed service, ACL, provider client, secrets, user account,
  broker ledger, Tailscale identity, original scientific PDF or owner
  local computer disk was modified during this source-only test.

## New source components

1. src/krc_research/stage134_offline_bibliography_route.py
   - Accepts only {"offline_bundles":[...]} (1 to 4 bundles).
   - Total canonical JSON payload <=200000 bytes.
   - Every immutable bundle includes strict DOI, provider-supplied
     snapshot JSON and SHA256, allowed canonical provider URL, date and
     optional self-declared source lineage; validated by existing
     Stage134 bibliography_provenance module before consent proposal.
   - Duplicate DOI, malicious provider URL, altered SHA, oversized
     payload, network flags, legacy DOI-only provider calls and
     arbitrary input fields are rejected.
   - Computes KRC-BIB-PROV-1 response strictly from already-supplied
     JSON snapshots, no provider fetch callback, no raw PDF/download.
   - Preserves metadata coverage gaps, provenance unverified,
     verified scientific origins=0, retraction clearance NOT_ESTABLISHED,
     human evidence review required and scientific_approval=false.
2. src/krc_research/stage131_project_research_route.py
   - Adds explicit source-only opt-in to the existing owner consent path.
   - Defaults to DISABLED; only immutable APPROVED profile and matching
     SHA256 enters existing durable request ledger and single-use signer.
   - Explicitly injects offline-only bibliography function; no fallback
     to older bibliography_audit with live-network defaults.
3. src/krc_research/science_dispatch.py
   - Recognizes offline_bundles only when the explicit bibliography
     callback is supplied; never silently uses legacy DOI lookup.
4. src/krc_research/private_contract_schemas.py
   - Requires exactly one of DOI-only (historical) or offline_bundles
     (new) forms, rejects mixed payloads.
   - Private source-only route further requires offline_bundles;
     the legacy DOI-only form can never execute through this route.
5. src/krc_research/stage131_science_semantic_contract.py
   - Independently validates KRC-BIB-PROV-1 result shape and no
     scientific promotion, while retaining old KRC-BIB-1 semantics.
6. tests/test_stage134_private_offline_route.py
   - Exercises default deny, explicit opt-in, immutable full-profile
     approval hash, signed one-time dispatch, replay denial, artifact
     content SHA256, no-network assertions, invalid source captures,
     wrong DOI/provider URL/source SHA, duplicate snapshot, invented
     scientific provenance, and Stage133 external 403 denial.

## Verified tests

Reviewed branch source at commit:
ddea2c46f088adbdc7908e41c80dfad4ea1df9e8

Isolated source-only test process on the authorized KRC VM, using
non-service source worktree (not HP-OMEN, and not installed /opt):

- Focused bibliography / provenance / private route / Stage133
  boundary regression: 84 PASSED, 0 FAILED.
- Full KRC repository test suite: 1372 PASSED, 24 SKIPPED,
  0 FAILED, 72.79 seconds.
- Existing Stage133 external operation allowlist remains unchanged,
  with negative test proving BIBLIOGRAPHY returns 403.
- Source test uses synthetic in-memory provider snapshots only.
  Zero provider API requests and no imported live provider fetch
  callback were required to pass.
- GitHub source branch and original Stage133 deployment remain
  separated; external signed Stage134 POST/GET has NOT been performed.

## Real K_Science evidence and critical shortfall

The preceding 2026-11-23 owner-directed one-shot metadata pilot
received four Crossref matches and four Europe PMC coverage gaps.
The eight HTTPS responses and their SHA256 hashes are recorded at:
docs/integrations/STAGE134_OWNER_ONESHOT_REAL_PROVIDER_RECEIPTS_2026-11-23.json.

For minimization, raw original provider response bodies were NOT
retained in that public receipt. Their SHA256 digests are not
reversible. Consequently those historical real payload objects
cannot be reconstructed from the receipt to build a genuine
immutable Stage134 offline_bundles profile. It would be incorrect
to invent the original provider JSON or claim a real Stage134 signed
server E2E using only these hashes.

A future real Stage134 artifact flow requires independently approved
provider capture/retention (prefer access-restricted artifact storage),
tight per-provider budget, source rights review and a fresh explicit
owner approval of the exact full immutable payload. The previous
8-request owner scope is CONSUMED; do not reuse it.

## Cross-project next gates

1. K_Science: accept and test new KRC-BIB-PROV-1 offline result schema.
   Existing K_Science Stage134 candidate client currently recognizes
   only legacy KRC-BIB-1, so ACK remains PENDING.
2. K_Sentinel: independently review single-owner consent/cross-UID
   security and the Stage127 exact workflow-family allowlist. Existing
   admission remains unchanged until explicit signed-release approval.
3. KRC: review bounded signed POST contract for real Stage134 source
   profile, server-side replay semantics, GET/TTL and cancellation.
   Stage132 and Stage127 operation allowlist modifications require a
   separate reviewed release and controlled rollback.
4. Perform negative external Stage134 E2E, one positive real snapshot
   E2E with exact owner-approved profile and actual full JSON
   payload bytes, and independently verify artifact SHA256.
5. Independent scientific methods/results and dataset independence
   remain UNVERIFIED. Two catalog metadata matches do not constitute
   independent scientific evidence. PRODUCTION_NO_GO.

No further provider network requests are authorized by this report.

## Independent K_Science source-only ACK

K_Science draft PR17 added an independently implemented read-only
KRC-BIB-PROV-1 client and negative tests. Its new and historical
Stage134 bibliography source tests passed 55/55.

Two synthetic end-to-end private VM source-chain tests used the actual
KRC private consent ledger, owner-approved immutable profile, internal
science signer, durable request ledger and artifact store. The independent
K_Science client checked the exact authorized result envelope,
response headers, artifact expiry and SHA256.

- Europe PMC no-match: PASS, raw artifact SHA256
  c511f63f7872f157da0297c5fd16c321419fa918198a10700390ba10d2faa476.
- Two matching provider metadata fixtures: PASS, raw artifact SHA256
  a4de94f9b6db18baa4feac58da3eb848bab241ef582e15ed40d5212c2bc3c186.
- Both tests confirmed scientific_approval=false, no live provider
  network, one-shot consent and no replay. The private isolated VM
  temporary states were discarded; installed runtime was unchanged.

K_Science report:
https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/docs/integrations/stage127-science-e2e/STAGE134_BIBLIOGRAPHY_PROVENANCE_SOURCE_ACK_2026-11-23.md

This upgrades ONLY the cross-project source-level semantic ACK.
The Stage127 external transport still rejects bibliography.audit;
no live provider data bundle or production E2E was signed or run.
