# KRC Stage133 KRC-owned server acceptance and consumer handoff
Date: 2026-11-21
Disposition: SOURCE_CANDIDATE / DEFAULT_OFF / NO_SEND / NOT_DEPLOYED / PRODUCTION_NO_GO.

## Scope
KRC owns the private owner approval, execution ledger, scientific dispatch, result semantics, artifacts and signed GET. K_Science owns request construction and result checks. K_Sentinel is transparent authenticated transport ONLY.

First Stage132 external approved profile E2E: PASS. Separate missing-consent external denial: PASS. Joint scientific matrix remains 2/48; 46 not credited. Do not replay consumed grant.

## Implemented in source, default disabled
- research.evidence.preflight: strict nested manuscript, claims, independent-origin evidence and search-run input validation. Requires timezone-aware timestamps, no duplicate claim IDs, no invalid counts or caller-supplied user_profile_approved. The legacy engine flag is derived only AFTER server-owned grant and ledger. It is never scientific approval.
- research.inspection.review: receipt schema (SHA, sections, locators and timestamp); caller trace_verified=true forbidden. A metadata receipt cannot prove experimental truth.
- Existing profile validation remains the ONLY enabled runtime operation by default.
- Bibliography audit still denied by the private project route and external allowlist, pending provider readiness.
Input schemas: schemas/stage133/external_offline_payloads_v1.schema.json. Date-time format requires timezone and must be validated by consumer independently.

## Existing external protocol unchanged
POST /staging/v2/execute with existing Stage127 verified identity and exact request_id,operation,payload; owner prepares and separately approves the full immutable request. No client consent boolean or authority digest. An approved one-shot grant may be consumed only once; on HTTP409/504 or network loss, reconcile the original RID and do not redispatch.
Successful POST returns correlated completed descriptor; GET is independently authorized with new OIDC token, precise X-KRC-Request-ID and artifact path. Consumer validates task_id, operation, size, TTL, SHA256 and semantic shape; scientific_approval=false always.

## Staging-only opt-in and nondeployment
New runtime source option --enable-stage133-offline-operations must be set for BOTH broker and gateway AND requires new root-owned 0600 marker /etc/krc-stage132-post/enable-reviewed-stage133-offline. Without this explicit additional gate, existing profile-only behavior remains. None of these flags or markers were installed and no services restarted.
Future release gates: strict contract ACK from K_Science, independent review, full regression, cross-UID runtime/security checks, immutable root release parity, rollback and coordinated operator action. A new real pilot requires distinct exact owner approval.

## Crossref / Europe PMC
Existing KRC metadata-only adapters are source-prepared and fixture-tested. Crossref and Europe PMC provide metadata, not primary-source inspection, independence or full retraction clearance. Europe PMC has biomedical/life-science emphasis and may not index concrete-engineering research. Crossref recommends contact details for polite API access and reports rate-limit headers. Do not invent a project contact.
FREE_ONLY_OFFLINE prohibits provider network calls. Enabling metadata requires an explicitly authorized FREE_ONLY_METADATA scope, verified redirect controls, proper rate limiting and 429 handling, evidence provenance and separate E2E. No API calls were made in this stage.
References: https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ ; https://dev.europepmc.org/RestfulWebService .

## Tests and status
Initial KRC source full regression: 1110 PASS,17 SKIPPED,0 FAIL.
Stage132+133 isolated suite after validation and runtime opt-in tests: 66 PASS,0 FAIL (synthetic identities; actual local UNIX/HTTP POST and GET).
Combined single-process source regression in either test order: 1167 PASS,18 SKIPPED,3 FAIL. When Stage131 runs first, Stage132 GET returns 502 UPSTREAM_FAILURE in three cases. When Stage133 runs first, Stage131 signed artifact UDS tests time out in three cases. This combined mode is NOT accepted; investigate shared-process/module/fixture interactions and repeat isolation tests before rollout. These results do not invalidate separate suites but must not be called a combined PASS.
New external Stage133 E2E: 0 confirmed. K_Science has not enabled new-operation client. Production NO-GO.
