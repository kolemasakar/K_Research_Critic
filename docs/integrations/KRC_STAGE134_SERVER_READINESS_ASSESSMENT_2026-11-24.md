# KRC Stage134 server integration - source review and readiness assessment

Date: 2026-11-24
State: PRIVATE_SOURCE_TESTED / EXTERNAL_STAGE127_NOT_ENABLED /
NOT_DEPLOYED / PRODUCTION_NO_GO

## Changes and independent regression

KRC PR36 source branch:
https://github.com/kolemasakar/K_Research_Critic/pull/36

The source-level private bibliography operation already:
- Requires explicit enable_stage134_offline=True opt-in;
  default private ProjectResearchRoute still denies bibliography.audit.
- Requires complete immutable supplied offline snapshot profiles,
  separately approved by the existing owner-consent ledger, including
  profile SHA256, durable request and one-shot replay controls.
- Never silently selects legacy DOI-only live-provider fallback for
  signed offline_bundles.
- Signs internal Science result, validates conservative result status,
  materializes JSON artifact and validates byte SHA256.
- Preserves metadata-only and experimental-independence claims:
  no retraction clearance, no full text, no scientific approval.
- Leaves the installed Stage127/Stage132 external bibliography
  operation default-denied; existing signed preflight and inspection
  transport behavior is not changed.

New source security changes from independent PR37 were integrated
without discarding the Stage134 offline provenance feature:
- Distinguish Europe PMC nonempty wrong DOI from actual no-hit
  coverage gap; wrong DOI is REVIEW_REQUIRED.
- Reject literal or percent-encoded control chars and Unicode
  whitespace in DOI/URL before provider queries.
- Preserve HTTPS exact host/path/query allowlists and no redirects.
- Keep unrelated ordinary FREE_ONLY public research enabled by default.
- Source integration commit:
  91910da3b8c2c393b323e5bcf6048fe9ac95fddb.

Isolated KRC VM test evidence at that exact commit:
- Focused Stage134 private signer/provenance/public DOI security:
  **126 PASSED**, 0 FAILED, exit 0.
- Full KRC source repository tests:
  **1386 PASSED / 24 SKIPPED / 0 FAILED**, 77.76 seconds,
  exit code 0.
- Tests are source-level with synthetic controlled data, not
  a real Stage127 external signed transport deployment.

K_Science PR17 has an independent candidate
KRC-BIB-PROV-1 client (55 previous tests PASSED) and two
synthetic source-chain signed KRC -> Science client checks;
their external E2E is still NOT_RUN.

## Architecture separation

The owner expressly requires KRC FREE_ONLY public internet research
available without per-source grant. This is implemented independently
in narrow KRC PR37 and already supported for existing deployed
Crossref/OpenAlex public discovery. Stage134 signed external
research.bibliography.audit has a separate immutable profile,
consent, replay, data custody and transport identity scope.
Do not repurpose signed authorization as a blanket web-search ban.

PR37: https://github.com/kolemasakar/K_Research_Critic/pull/37
PR37 security review:
https://github.com/kolemasakar/K_Research_Critic/blob/research/public-web-default-20261123/docs/integrations/KRC_PR37_INDEPENDENT_SECURITY_STAGING_REVIEW_2026-11-24.md

## Actual release blockers

1. KRC installed Stage133/132 gateway currently has NO signed
   bibliography.audit external operation; it returns 403 by design.
   An installed Stage134 release must be explicitly reviewed and
   admitted under existing consent and trusted workflow identities.
2. K_Sentinel must independently check OIDC workflow family, cross-UID
   trust, negative matrix, replay/nonce/half-close and signed
   POST/GET boundaries before admission of a new operation.
3. K_Science must finish independent client and fixture interop
   acceptance under the exact agreed schema, including failure
   403/409/410, TTL and replay behavior.
4. The previous owner-directed live public provider pilot retained
   SHA256 fingerprints, but not the original complete JSON response
   bytes. The original provider responses cannot be recovered from
   hashes to form a genuinely immutable live-provenance profile.
   A future real external pilot needs separately authorized provider
   capture and access-restricted artifact custody.
5. Production security release and source-level scientific
   truth/experimental independence are separate acceptance gates.

## Rollout and rollback controls

- Do not overwrite installed /opt runtime, consent DB or artifact store
  as a shortcut from this unmerged draft PR.
- Prepare an immutable staging release with an exact git SHA and
  preserve the previous release, config and service dependencies.
- Default disabled until the KRC/Sentinel/Science three-project review
  authorizes Stage134 operation-specific admission.
- Run negative tests before any one-shot external positive E2E.
- On failure, restore previous immutable release and verify
  service health, permission boundaries, replay DB and artifacts,
  without deleting or altering consent history.
- Local owner computer disk access remains prohibited without
  direct task-specific permission.

Final outcome: KRC signed PRIVATE SOURCE integration technically
accepted in its bounded offline mode; NO claim of deployed external
Stage134 or full scientific acceptance; Production remains NO-GO.
