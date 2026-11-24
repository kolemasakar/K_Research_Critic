# KRC Stage134: real Crossref profile, signed POST source gate and privileged release handoff

Date: 2026-11-24
Disposition: REAL_PUBLIC_METADATA_CAPTURE_PASS / IMMUTABLE_PROFILE_PROPOSED /
SIGNED_POST_SOURCE_ACCEPTED / EXTERNAL_SIGNED_E2E_NOT_RUN /
PRIVILEGED_MAIN_GATEWAY_RELEASE_NOT_PERFORMED / PRODUCTION_NO_GO.

## 1. Exact source and validated scope

KRC PR36 source commit:
62007ba9de3700a8fbd24a527c49b6392e3a41e2.

- Created independent Stage134 signed POST release gate:
  separate enable_stage134=True application flag; all original
  Stage133 operations remain enabled exactly as before by default.
- KRC ProjectPostBoundary validates a complete bounded
  offline_bundles payload against the existing strict source
  provenance schema; rejects DOI-only requests, modified captures
  and attempts to execute without owner consent.
- Internal relay and gateway pass bibliography.audit only when the
  separately enabled operation allowlist admits it.
- Runtime requires both explicit --enable-stage134-bibliography
  and a separate root-owned 0600 marker
  /etc/krc-stage132-post/enable-reviewed-stage134-bibliography;
  Stage133 marker alone cannot enable Stage134.
- No live service, Sentinel ingress, broker key or OIDC provider
  was changed. The installed Stage133 route remains default deny.

Acceptance on the exact new Stage134 source commit:
- Focused signed POST/consent/replay/read tests: 53 PASS, 0 FAIL.
- Complete KRC repository regression: 1398 PASS, 24 SKIPPED,
  0 FAIL. Unit test exit code 0.
- Source tests include default 403, exact immutable consent match,
  synthetic signed POST result 200, artifact byte SHA256, duplicate
  submission 409, changed payload denial, wrong principal denial,
  and independent root-marker fail-closed checks.
- Not an authenticated Stage127 positive end-to-end execution.

## 2. Real four-DOI public metadata profile

Original K_Science article selection:
https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/docs/integrations/stage127-science-e2e/stage134-real-corpus-4doi.offline-candidate.json
Original Science PDF identity manifest:
https://github.com/kolemasakar/K_Science/blob/science/stage134-real-corpus-20261123/literature/source_register/STAGE134_REAL_PDF_CORPUS_2026-11-23.json

New captures from public FREE_ONLY Crossref JSON over verified HTTPS:
- 10.1016/j.acme.2013.10.006
  raw body SHA256: 27837699e9494ed8b8d66a4f58ad1c6f1b2dcadb529546983f771f0547a8c692
- 10.1016/j.proeng.2013.03.022
  raw body SHA256: 16a1c44f107a1b9c173728bded2e812b559b3c1c24a232d05bfd2cadb3f49096
- 10.1016/j.ndteint.2015.01.003
  raw body SHA256: c7fcfeea228f79a0f8e4d9cf8c924499dd7e8fe1e16dff9a32918f45cec9d910
- 10.1016/j.conbuildmat.2011.12.103
  raw body SHA256: 829442cf48d5bfe1e2b4ad123c93af6fee9ae0481adea8cbd3b9942695b280ff

Crossref original JSON bodies and exact canonical JSON were saved in
a mode0700 private root under the authorized krc-cobalt server:
  /home/krcops/krc-stage134-real-profile-crossref-20261124
All evidence files mode0400 and owned by krcops. No PDF or source
document was fetched, modified, exported or published to GitHub.

A separate attempt to capture Europe PMC stalled twice due to
actual provider timeout. No synthetic Europe PMC response was
substituted. The final immutable profile contains FOUR Crossref
captures only, and its correct research outcome is
PARTIAL_METADATA_ONLY for each publication, not full coverage.
It cannot claim verified scientific independence, retraction
clearance, full-text inspection or provider-signed authenticity.
PDF document hashes are carried only as previously reported
K_Science catalog claims, not independently reread locally.

Immutable complete private profile:
  /home/krcops/krc-stage134-real-profile-crossref-20261124/profile.json
Profile bytes: 66491
Complete canonical profile SHA256:
  5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7
Approved inner payload SHA256:
  1b567f79f529a43699b5f395e8e5194c5b3aeb08ff7bf239d7a70fc1aa631e62

The raw provider response bodies are intentionally NOT posted to
public GitHub. Complete profile access requires the authorized KRC
VM service identity and owner review before approval.

## 3. Real live KRC proposal and consent status

Using KRC source with Stage134 explicitly enabled ONLY for
PROPOSE, not execution, a new immutable profile was recorded
in the existing owner consent SQLite ledger.

Request ID:
  KS-50902e5cfe263a8c760fc2dfa4a26882
Profile SHA256:
  5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7
Observed status:
  PROPOSED
Owner approval:
  NOT_GRANTED
Stage134 execution:
  NOT_RUN
New signed external E2E:
  NOT_RUN

Before mutation, SQLite PRAGMA quick_check returned ok and a
restricted SQLite backup was taken under the same private VM
capture root, not uploaded to GitHub.
The exact request was re-read, its stored hash matched the
captured private profile, and only one PROPOSED ledger row was
added. No APPROVE or execution call was made. All earlier
Science grants retain their prior status and cannot be reused.

## 4. Independently prepared privileged main-gateway release

A PRIVATE read-only source release candidate was assembled from
the exact KRC SHA under:
  /home/krcops/krc-stage134-privileged-release-candidate-20261124

- 15 modified KRC Python modules and two JSON schemas;
  17 total files selected and verified against Git blob hashes.
- Ready-for-root-operator source tar:
  release-src.tar.gz
- Verified tar SHA256:
  b9be29ea0737622d88dd02de324afde6a9179d3f7453c9e04b01a8d53971cd1f
- Manifest SHASUMS.txt and exact COMMIT_SHA are stored privately
  alongside that archive.
- Source overlay import parity PASS with the actual installed
  broker and gateway fallback namespace/module paths.
- Offline audit using that packaged source against the FOUR
  real Crossref profile records PASS: four conservative
  PARTIAL_METADATA_ONLY statuses, zero provider network calls.

Root-owned installed main service boundaries:
- krc-research-v2.service (UID krcresearch, gateway) uses source
  /opt/krc-stage133-offline/current/gateway-src followed by
  /opt/krc-research-v2/src.
- krc-project-n39-post.service (UID krcops, broker) uses
  /opt/krc-stage133-offline/current/src followed by
  /opt/krc-project-n39-read/.../src.
- Both units and their /etc systemd drop-ins are root-owned.
- Current access is UID1002 krcops. sudo -n rights are restricted
  to unrelated status/media/Stage114 commands. The account
  cannot perform arbitrary root install, create the root marker,
  or restart root-owned signed services.
- No escalation, service overwrite or policy bypass attempted.
  Therefore this new Stage134 source remains NOT INSTALLED.

## 5. Root-operator release sequence (pending authorized access)

This section is a controlled handoff, not an executable deployment.

1. Verify the operator has authorized root privileges on
   krc-cobalt and independently check the exact release tar hash,
   all 17 file hashes and target source/base/venv compatibility.
   Archive existing installed immutable root releases and
   record their systemd fragment/drop-in hashes and process state.
2. Prepare a NEW root-owned immutable overlay from the verified
   candidate archive under an approved /opt/krc-stage134 release
   directory; never overwrite existing /opt/krc-stage133-offline
   or /opt/krc-research-v2 code in place.
3. Separately inspect the gateway and broker Python namespace
   source precedence. The explicit release overlay must be
   first, preserving original fallback paths, service roles,
   SO_PEERCRED, HMAC keys and nonce/consent/artifact databases.
4. Install default-DENY code first without the Stage134 marker
   and without --enable-stage134-bibliography. Restart and
   observe both existing signed services independently;
   assert original Stage133 operations and GET remain intact.
   Test external bibliography POST remains denied.
5. Independently review the exact PROPOSED profile and consent
   hash with the owner; do NOT infer APPROVED from the command
   to develop or deploy software. New signed execution requires
   an explicit APPROVE decision for the exact request ID/hash.
6. Confirm the Sentinel independent current workflow-family
   admission, OIDC trusted identity, nonce and cross-UID
   negative tests, then use the separately protected 0600
   root marker and explicit command flag for this one
   reviewed staging window.
7. Have authorized K_Science run exactly one scoped signed
   Stage134 workflow against the exact approved payload,
   retrieve the corresponding signed artifact, verify SHA256,
   403/409/410, TTL and one-shot replay. Independently
   cross-check the KRC consent and request ledgers afterward.
8. On any failure, remove Stage134 activation, restore
   previous immutable source+drop-ins and validate the
   original Stage133 signed route. Never reset, delete or
   replay consent, nonce or artifact database state.
   Do not call an ambiguous POST a failed/non-executed
   request; reconcile the server ledger before retrying.

## 6. Partner checkpoints and remaining blockers

- K_Sentinel PR39 independent 74/74 selected security
  regression, 6/6 synthetic transport tests, four genuine
  unsigned-negative staging HTTP denials passed. Genuine
  signed positive Stage134 still NOT_RUN.
- K_Science PR17 exact schema independent 66/66 tests
  passed; final amended client was retested by KRC against
  its actual internal signer and artifact store in two
  synthetic source-only cases, 2/2 PASS. No external E2E.
- Owner-approved Stage134 profile currently absent; this
  report records one real NEW PROPOSED profile only.
- Existing KRC public FREE_ONLY search remains available and
  must not be blocked by the separate signed workflow gate.
- No user HP-OMEN local disk access.

Overall:
STAGE134_CODE_QA_PASS / REAL_METADATA_PROFILE_CREATED /
CONSENT_PROPOSED_ONLY / ROOT_PRIVILEGED_DEPLOYMENT_PENDING /
EXTERNAL_STAGE134_SIGNED_E2E_NOT_RUN / PRODUCTION_NO_GO.

## 7. Actual four-real-Crossref source POST/GET interop

After full source acceptance and real Crossref capture, a separate
private, mode0700 isolated VM test re-used the exact captured FOUR
Crossref payloads, the final amended K_Science PR17 client and
the current Stage134 signed POST boundary source.

- Same immutable private full profile SHA256:
  5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7.
- Source POST with no approval: HTTP 403, PASS.
- A completely separate synthetic test-only consent database was
  then APPROVED. The real live KRC PROPOSED owner request was
  NOT approved, edited, consumed or replayed.
- Source ProjectPostBoundary with explicit test-only Stage134
  operation flag: POST 200, PASS.
- Actual KRC internal signer and request ledger, artifact store,
  ProjectArtifactAuthority GET, raw result byte length and
  SHA256: PASS.
- Final amended Science client with exact pinned KRC input/result
  schemas authenticated the received bundle/result shape and the
  descriptor/header/body digest: PASS.
- FOUR real Crossref publications: four PARTIAL_METADATA_ONLY
  outcomes; science_approval=false; independent_origins_verified=0.
- Artifact body SHA256:
  92745440c3ff3e52eb635fb752e67e06a11c999b030a448197dc0cefc609004d.
- Second POST of the same synthetic test request: HTTP 409, PASS.
- Zero provider network calls during this local replay.
- Actual external Stage127/Sentinel OIDC POST/GET was NOT performed.

Initial ad hoc diagnostic before this successful test used an
incorrect permissive umask, causing the existing source read-only
database custody check to reject a test requests.sqlite file.
The source server itself already sets umask 077. Repeating with
umask 077 reproduced the proper operational file protection and
passed all local Stage134 POST/GET checks without weakening custody.

Disposition:
REAL_CROSSREF_SOURCE_POST200_AND_GET_SHA_PASS /
KSCIENCE_AMENDED_CLIENT_ACK_PASS /
ISOLATED_REPLAY409_PASS /
EXTERNAL_STAGE127_SIGNED_E2E_NOT_RUN /
REAL_OWNER_PROFILE_STILL_PROPOSED.
