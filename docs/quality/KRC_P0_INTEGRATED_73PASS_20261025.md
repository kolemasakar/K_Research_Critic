# KRC P0 A–D — integrated offline research checkpoint

Date: 2026-10-25. Branch: `agent/krc-public-media-r3-integration`.

## Verified
New `integrated_research.py`, `integrated_cli.py` and 10 new regression tests. Actual pytest on isolated `krc-cobalt` runner: **73/73 PASSED (0.96s)**. All fixtures synthetic. CLI blocks input-supplied attestation claims and hashes the exact research input. Pipeline rejects missing external inspection attestation, duplicate origin counting, missing search logs and invalid self-described Critic rounds. It never returns publication approval.

## Outstanding
Source receipt hashes can be independently injected only from trusted code; attestation issuer is not implemented. Recorded Critic rounds are not an independently executed Critic. Scientific first-source reading, complete corrections/retractions clearance, revision execution and journal/author approval remain pending. Private plugin 0.19.14, existing KRC service 9013, public endpoints and MEDIA unchanged.

Status: `OFFLINE_TESTS_PASS / SCHOLARLY_E2E_PARTIAL / PUBLICATION_NO_GO`.
