# KRC parallel tracks 1+3+4 checkpoint — 2026-10-29

**STAGING ONLY / FREE_ONLY / Production NO-GO. No real science dispatch, no installation, no owner consent created.**

## 1 — Stage131 backend pre-install
On `krc-cobalt`, KRC source checkout SHA `90283e9b46531fa4df11c3892f7b282c02ea4fb0`. Read-only `scripts/stage131_preinstall_audit.py --service-uid 988` reports six NOT_READY: /etc/krc-stage131, /var/lib/krc-stage131, /run/krc-stage131, and /etc/krc-stage131/{staging.json,transport.key,science.key}; exit 2. User decision retained shared `krcresearch` UID988. Root-owned reviewed immutable /opt source/venv and private config/keys are still absent. No new external transport; Stage127 sole :19017.

## 3 — Contracts
Focused isolated `pytest` selection `tests/test_stage131_actual_wire_contract.py`, `tests/test_stage131_actual_uds_response_schema.py`, `tests/test_stage131_schema_v1.py`, `tests/test_stage131_response_schema_v1.py`, `tests/test_stage131_preinstall_audit.py`: **9/9 PASS** in 1.16s on pinned source. Actual private UDS response is `krc-transport/2`, completed inline|artifact or rejected|pending_reconciliation; proposed separate science_response_v1 is **NOT** actual wire, and cannot be presented as adopted. External Sentinel/K_Science schema sign-off is still PENDING; align error code, owner IDs, artifact GET and operation schemas before science E2E.

## 4 — Read-only bibliography live probes
krc-cobalt stdlib HTTPS read-only, no personal data or full text:
- Crossref `https://api.crossref.org/works/10.1038%2Fnature12373`: HTTP200, returned DOI `10.1038/nature12373`.
- Europe PMC `search?query=EXT_ID:10.1038/nature12373`: HTTP200 but zero hits; **wrong query field for DOI**, not outage or evidence article absent.
- Europe PMC `search?query=DOI:10.1038/nature12373`: HTTP200, hitCount=1, DOI matches, `isOpenAccess=N`.
- Europe PMC `search?query=DOI:10.1038/s41586-020-2649-2`: HTTP200, hitCount=1, DOI matches, `isOpenAccess=Y`.
The earlier Europe PMC HTTP503 blocker was not reproduced in these probes; network access is not guaranteed or authenticated publication-level provenance. Distinguish METADATA_ONLY from verified FULL_TEXT. No fulltext retrieved; provider adapter integration, timeout/retry/backoff/429/503, licensing, cross-provider field reconciliation and independent provenance are still PENDING. Crossref is a free metadata source (<https://www.crossref.org/documentation/retrieve-metadata/rest-api/>); Europe PMC availability confirmed on two sample identifiers only.

## Decision
1 = PREINSTALL_BLOCKED (6 NOT_READY).
3 = LOCAL_CONTRACT_TEST_PASS (9/9), CROSS-PROJECT SCHEMA ACK PENDING.
4 = TWO_METADATA_PROVIDER_READONLY_PROBES_PASS, LIVE PROVIDER INTEGRATION PENDING.
No E2E-01..05, no scientific publication approval, no production.
