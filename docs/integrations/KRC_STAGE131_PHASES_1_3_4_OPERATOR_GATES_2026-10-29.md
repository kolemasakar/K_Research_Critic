# KRC Stage131 — operator decisions and execution gates (2026-10-29)

**STAGING ONLY / FREE_ONLY / Production NO-GO.** Owner-requested phases: 1,3,4.

## Completed by KRC (evidence)
- Stage127 sole external staging transport approved ACK_WITH_LIMITATIONS; internal Stage131 UDS not yet installed.
- Shared service user `krcresearch` UID988 and group `krc-sentinel-ipc` retained by explicit owner decision.
- Hash-locked Stage131 *test-only* dependency candidate, 19 packages, audit reported 0 findings at query time; base public package version bounds are different. Separate source candidate and negative tests exist.
- Actual `krc-transport/2` UDS response schema and separate proposed scientific request and response schemas exist; local tests passed. **Do not confuse draft `science_response_v1` with actual transport wire.**
- Crossref and Europe PMC return matching metadata for tested DOI values. DOI field for Europe PMC is `DOI:`, not `EXT_ID:`. No fulltext attested, no provider wired into scientific dispatch.
- The latest preinstall probe produced six NOT_READY (config, keys, state/runtime paths); owner grant and internal signer remain OFF.

## KRC action map
### Gate 1: Stage131 controlled operator deployment
Operator accepts exact new immutable release SHA and rollback method, then provisions *dedicated* Stage131 configuration and nonreused secret keys as UID988: /etc/krc-stage131 (0700), staging.json/transport.key/science.key (0600), /var/lib/krc-stage131 (0700), /run/krc-stage131 (0750), socket 0660. Use existing service User=krcresearch and Group=krc-sentinel-ipc. No key bytes in GitHub, chat or logs. Service manually started only after audit and admin confirmation. No Stage126/Stage127 change.
**Note:** runtime is created by systemd, and `/run` need not exist before manual start. Adjust prestart audit to distinguish installation preflight from runtime poststart.

### Gate 3: Scientific schema acceptance
KRC and K_Science confirm pinned SHAs for `science_request_envelope_v1.schema.json` and actual `uds_response_transport_v2.schema.json`. K_Sentinel agrees with outer transport error mapping. Confirm metadata/ARTIFACT response, STATUS 409/reconciliation and exact operation names. Draft `science_response_v1` not wire adopted. Explicit partner ACK required; offline tests are not partner acceptance.

### Gate 4: Bibliography integration
Recommend FREE_ONLY metadata-first Crossref + Europe PMC DOI: lookup. A provider response is METADATA_ONLY by default; OA=Y is not verified full text. Fail closed on mismatched DOI or invalid provider response, bounded timeout/retries/backoff 429/503, license audit before fulltext, source independence and DOI evidence. Network-enabled science dispatcher remains disabled until authorization, consent and provider terms sign-off.

## Manual owner actions
**Required now**: approve scope of a *staging-only controlled installation and manual start* of Stage131 with separate secrets under existing UID988. This is a service/filesystem write, not implied by earlier read-only approvals. Confirm whether operator should proceed with service provisioning; no actual research execution.
**Required later**: issue a specific consent grant for one test operation and corpus only when signer/consent custody has passed negative tests. K_Science/Sentinel separate schema ACK and bibliographic provider selection may be handled through project comments; no need for user to provide JWT, HMAC or key material.
**No action needed**: new Unix UID, new VM, second external port, paid provider, production approval.

## Hard NO-GO
Do not mark Phase1 deployed or Phase3 cross-project ACK or Phase4 provider-in-backend PASS until independently demonstrated. Stage127 transport acceptance remains valid.
