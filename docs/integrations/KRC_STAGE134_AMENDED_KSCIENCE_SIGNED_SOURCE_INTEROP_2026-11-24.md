# Stage134: amended K_Science client with actual KRC private signed source integration

Date: 2026-11-24
Disposition: KRC_PRIVATE_SIGNED_SOURCE_TO_AMENDED_KSCIENCE_2_OF_2_PASS /
FULL_EXTERNAL_STAGE127_SIGNED_E2E_NOT_RUN / PRODUCTION_NO_GO.

## Verified source custody

- KRC Stage134 source code commit:
  91910da3b8c2c393b323e5bcf6048fe9ac95fddb
- K_Science client exact Git blob:
  dd2313377ec2b57bffbc03b80cbdc4135ac0ab5c
  tools/stage134_offline_provenance_client.py
- K_Science tests exact Git blob:
  658f30cac4be76d6c9a5a80fe5c76c6d4b9c0f1f
- K_Science pinned KRC input/result Draft2020-12 contract Git blobs:
  83c0ce5d950dc7efcce90f00f122369fc90584d4
  a621d85719ac1bc307dd15a501eaf866b8ea6ab9
- These four actual source/test/schema files on the authorized KRC VM
  were hashed again and matched the GitHub public PR17 blobs.
- The source engine was imported from the exact KRC PR36 worktree,
  not from installed staging/production services.

## Actual isolated signed private-source chain

Two scenarios were executed with completely synthetic public metadata
snapshots inside separate automatically cleaned private VM test roots.

1. Crossref synthetic DOI match + Europe PMC synthetic empty result:
   COVERAGE_GAP_METADATA_ONLY.
   - KRC signed private owner-consent/immutable profile, durable
     request ledger, internal Science signer, artifact store
     and artifact reader actually invoked in source-only test.
   - K_Science final amended client verified profile hash,
     request/task identifiers, headers and raw artifact SHA256.
   - Result: PASS.
   - Artifact SHA256:
     0bc37f65c4b089801f9fe527f3bfcc79bc7fe5cf39205e9d4f05243c2c503fb7.
2. Crossref and Europe PMC matching synthetic DOI/title/year:
   TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY.
   - Same actual KRC consent/ledger/signing/artifact stack and
     updated independent Science client.
   - Result: PASS.
   - Artifact SHA256:
     5b8bc40c2e8d166f169409f68af84edcccb225f97bb9aa519ca27bfd4974d216.

Both scenarios required KRC profile APPROVED in their temporary
local TEST ledger, rejected a second execution (one-shot replay),
and returned scientific_approval=false,
independent_experiments_verified=0.

## Strict boundaries

- This was a KRC VM source-only integration test, not an owner
  approval grant and not a real scientific operation.
- External Stage127 OIDC, Tailnet POST/GET, Sentinel ingress and
  real K_Science workflow were not called.
- Public Crossref/Europe PMC endpoints were NOT used; networking
  was explicitly disabled during the synthetic test.
- Existing real provider 8/8 receipt hashes do not contain complete
  original JSON bodies, so cannot be used to recreate an authentic
  signed real-provider snapshot.
- No installed KRC root-owned service, original PDF, owner's
  HP-OMEN/local-computer disk, or Production state was changed.
- This acceptance updates the previously pending source-only
  signed compatibility of the *final amended* K_Science client.
  It must NOT change the K_Science external E2E matrix, which remains
  4/48 accepted; bibliography 0/11, Production NO-GO.

## Partner handoff

K_Science PR17:
https://github.com/kolemasakar/K_Science/pull/17
K_Sentinel PR39:
https://github.com/kolemasakar/Sentinel-Remote/pull/39

Next gates: independent Sentinel signed Stage134 positive/negative
transport acceptance, KRC installation of signed bibliography
operation with explicit scoped owner grant and native replay tests,
and K_Science external 403/409/410 and TTL acceptance. The separate
KRC public DOI MCP service is available as a staging-only tool and
is not a grant to signed bibliography execution.
