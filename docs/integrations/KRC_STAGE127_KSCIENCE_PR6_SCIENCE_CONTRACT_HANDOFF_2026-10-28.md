# Stage127 Science HMAC and K_Science PR #6 — contract/acceptance handoff
Date: 2026-10-28. **STAGING ONLY / FREE_ONLY / production NO-GO**.

## Actual KRC code baseline
Current KRC draft contract is `KRC-SCIENCE-CONTRACT-1-DRAFT` in `src/krc_research/private_contract_schemas.py`, over inner `krc-science/1` envelope and outer `krc-transport/2`. **Not final/deployed**. K_Science PR #6 packages are unsigned fixtures, NOT v2 wire requests; its 29 scenarios NOT_RUN. No unpublished scientific corpus should be submitted.

## Trust boundaries
Outer request requires verified UID 987 via `SO_PEERCRED`, valid Transport HMAC and allowlisted identity, durable request ledger; Sentinel v2 must check genuine GitHub OIDC RS256/JWKS+Tailnet StableID+mandatory jti replay. Current KRC installed UID988 backend still only accepts `principal=K_Science` and `workflow_ref=refs/heads/main`; Sentinel currently produces a GitHub sub and full workflow reference. **Wire format mismatch unresolved until Sentinel projection AND envelope validator are updated and tested**.

The candidate `science_signer127.py` (NOT deployed) accepts: request_id; task_id; operation; operation payload; trusted principal; profile_ref; evidence_refs; consent_ref. It checks the actual operation input schema, payload digest, validates nonempty bindings and delegates to a KRC-owned trusted `authorizer(context)`. The authorizer must be independently implemented with persisted consent custody, profile content digest/version verification, expiry, scope, actor and replay checks. It cannot trust `user_profile_approved` or a synthetic fixture as consent. After exact authorization, KRC alone creates `krc-science/1` envelope and HMAC and calls private science dispatcher. **No generic remote sign API, no Science key export.** Candidate tests: 5/5 PASS isolated; mock authorizer is NOT a real authorization verifier. This candidate is not yet wired into running `staging_service123c`.

## Inner science envelope
Required exact fields: `version=krc-science/1`, `task_id`, `client=K_Science`, `provider=K_Research_Critic`, `operation`, `created_at` (timezone-aware), `payload` object, `payload_sha256` (canonical JSON SHA256). HMAC is internal and separate, not part of caller input. `task_id` pattern `^[a-zA-Z0-9][a-zA-Z0-9_.:-]{7,119}$`. Request ID is separate transport correlation identifier. Current science envelope does **not** itself include request_id, profile or consent: those must be bound and verified by KRC authorization custody/ledger before science signing; further schema evolution/pinning may be required.

## Existing input schemas (draft, actual, not claims of final strict validation)
| Operation | Required payload | Optional / nested constraints | Limitations |
| --- | --- | --- | --- |
| `research.profile.validate` | `critic_profile` object with `profile_id`, `version`, `protocol`, `topic` | `user_profile_approved` boolean | Structural profile validation is not independent evidence of user consent |
| `research.evidence.preflight` | `user_profile_approved=true`; `manuscript_gate` object | `claims` array of `CLAIM`; `search_runs` array | A client true flag is not KRC authorization; scientific result may be NO_GO |
| `research.bibliography.audit` | `dois` array 1..24 strings | no extra fields | Running staging currently has `bibliography_fn=None`, so actual live audit is DENIED; metadata-only cannot count as bibliographic verification |
| `research.inspection.review` | `receipt` object | `RECEIPT` requires source_id, origin_id, doi, SHA256, inspected_sections, passage_locators, checked_at, inspector_id, method, evidence_relation, external_trace_id | receipt data and `trace_verified` do not alone prove independent inspection |

`CLAIM` requires `claim_id` (C followed by 2+ digits), `required` integer >=1, `evidence` array of EVIDENCE entries. EVIDENCE includes source_id, origin_id, access tier, support, inspected_methods_results, scope_matched, provenance_verified, primary_url. See code for full exact nested schema and additionalProperties behavior; consumers must use versioned JSON Schema rather than this prose summary.

## Existing inner output and error schemas (draft)
Successful dispatcher output has `task_id`, `operation`, `status` (`REVISE` or `PENDING`), `engine_result` object, `scientific_approval=false`. Error output: `status=error`, `error.code` in `INVALID_REQUEST, UNAUTHORIZED, OPERATION_DENIED, REPLAY_REJECTED, EXPIRED_REQUEST, HANDLER_ERROR`, and sanitized `error.message`. **Outer UDS** returns HTTP 200 only if transport boundary output `status=completed`; otherwise 409 (including some errors/ambiguity). Do not conflate HTTP codes with scientific verdicts.

## Acceptance evidence levels
1. `SYNTHETIC_FIXTURE`: schema/wire/replay test only. NEVER scientific evidence.
2. `METADATA_ONLY`: DOI/title/author bibliographic identity and resolvability only; cannot certify experimental claims.
3. `ABSTRACT_ONLY`: abstract content only; not full method/results verification.
4. `FULL_TEXT` or `METHODS_RESULTS_EXCERPT`: traceable passages/methods/results; verify source origin, scope, independent experimental provenance, and contradiction.
5. `SCIENTIFIC_EVIDENCE_ACCEPTED`: only when independent primary sources and their relevant methods/results were inspected, search strategy reproduced, DOI/citation metadata reconciled, Critic iterations and owner approval documented. Human scientific review remains distinct.

Real bibliography audit gate must use an expressly approved provider/offline corpus and report each DOI matched/unmatched, canonical bibliographic fields, source-access tier, origin independence, and discrepancy/audit trace. **No external provider enabled now.** Synthetic fake DOI must not be marked valid. Real peer-review/owner acceptance not automated.

## Joint E2E gates
- E2E-01: actual new v2 ingress with GitHub OIDC, Tailnet ACL, stable peer, durable jti replay, exact pinned identities; existing :19015 is v1 and not proof.
- E2E-02: all four operations positive/negative through internally authorized signing; bibliography must remain denied until a real audit backend exists.
- E2E-03: inline/GET SHA256, principal isolation, TTL, quota; real or bounded isolated evidence.
- E2E-04: request/task replay, timeout ambiguity, cancellation/restart and rollback; must not restart live Stage114/v1.
- E2E-05: evidence matrix actual outputs, immutable hashes and run IDs, K_Science/Sentinel/KRC SHAs, Critic approval and scientific reviewer reconciliation.

**Pending before claiming final schemas:** versioned published machine-readable schemas with external request/response/HTTP mapping, actual custody verifier, approved bibliography provider and comprehensive interoperability tests. Keep K_Science PR #6 and Sentinel PR #38 Draft.
