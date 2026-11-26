# Stage135 isolated source acceptance - 2026-11-26

KRC candidate source baseline ca021fe800eb19403e5cfaea04b24bee1a3a43a7.
Executed exact GitHub blobs in memory on authorized krc-cobalt device,
Python3 unittest, temporary synthetic SQLite state and actual AF_UNIX
socket. Process 56251: Ran 27 tests in 1.423s; OK; TEST_COUNT 27
FAILURES 0 ERRORS 0; exit code 0. No real research data or services touched.

Blobs:
- stage135_prepared_read.py b56a226fcd26420f625846e8d60e1d7c1f971b69
- stage135_prepared_uds.py dd3661ea2c429eba26b78fd9436d5e0ada533566
- stage131_signed_artifact_uds.py 19df3c275460c747274bb790f46fe3a6448b29b7
- test_stage135_prepared_read.py 7c98ef16a42fcbea50dbefb4286cff19a7361a75

All 27 tests passed, including valid exact bytes, HMAC rejection without
nonce consumption, replay across registry reopen, revocation during read,
expiry, wrong workflow/run/peer/purpose, v1 denial, terminal execution
state, profile/body tampering, file permissions and symlink, duplicate
JSON, size limit and real UDS request success/replay/extra byte/wrong path.

Wire version is krc-prepared-read/2, not the earlier v1 Sentinel candidate.
Identity fields are principal, repository, workflow_ref (branch),
workflow_file_ref (full GitHub workflow claim), run_id (decimal string),
run_attempt (integer 1). Existing key ID stage135-prepared-read-v1 remains
a key identifier, not a wire version. Exact v2 agreement pending.

Scope: synthetic same-UID socket test, not cross-service UID custody or
live rollout. Source reader has injected authoritative profile_lookup;
live adapter, audited provisioning, independent cross-project acceptance,
full regression and rollback remain release gates. No claim of complete
security attestation. No real key generated, no real request disclosed,
no owner consent activated, no production change.

Next: Sentinel reviews source and aligns v2 synthetic signer/UDS client;
Science independently validates scope and existing authorized workflow.
Owner approval remains required before actual key installation/disclosure.
