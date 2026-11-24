# Independent KRC PR37 security audit and staging rollback rehearsal

Date: 2026-11-24
Disposition: SOURCE_SECURITY_AUDIT_PASS / ISOLATED_STAGING_ROLLBACK_PASS /
REAL_PUBLIC_DISCOVERY_PASS / INSTALLED_PATCH_NOT_DEPLOYED

## Source identity

- PR: https://github.com/kolemasakar/K_Research_Critic/pull/37
- Independently reviewed and tested code SHA:
  d7b48468c858f841f57ca44c25e3bb67232ecf61.
- Parent target branch at review:
  science/stage133-offline-expansion-20261120.
- Baseline checked out independently at:
  23418dda183ea2af818dcb746a24abc7fd83df0a.
- Work performed in isolated source worktrees under the dedicated KRC
  research VM only. The owner's local-computer disks were not accessed.
- This review did not alter installed /opt releases or restart services.

## Code review findings and changes

1. The extracted public-web PR originally retained an
   audit_doi_provenance_offline function importing
   stage134_bibliography_provenance, a module not present in its
   target baseline. Removed the unused Stage134 dependency from
   PR37. The broader PR36 retains its own audited offline feature.
2. Europe PMC resultList containing non-matching non-empty records
   was incorrectly reported NOT_FOUND, then could be promoted to
   COVERAGE_GAP_METADATA_ONLY. Correct classification is DOI_MISMATCH
   with final REVIEW_REQUIRED. A truly empty results list remains
   NOT_FOUND and is correctly treated as a coverage gap.
3. DOI validation and provider URL decoding now reject control bytes,
   ASCII DEL and Unicode whitespace before any default network call.
   Tests include actual bad code points, not a literal backslash
   escape sequence; a test-fixture encoding mistake was discovered
   and corrected before final acceptance.
4. Preserved the owner's original requirement: FREE_ONLY public web
   research is default-enabled without a separate owner grant per
   search/DOI. Explicit allow_network=False remains available for
   reproducible offline tests only.

## Security review boundaries

- Strict Crossref and Europe PMC HTTPS hostname, path and query
  allowlists; no arbitrary user-supplied host, non-HTTPS URL,
  URL credentials or alternate port.
- Redirects denied, response final URL checked, JSON content type
  required, encoded non-JSON and oversized content rejected.
- Maximum response length 262144 bytes, timeout 0..10 sec,
  bounded retry attempts and no paid or authenticated provider.
- This logic performs metadata retrieval only; scientific truth,
  experiment independence and full-text verification remain False.
- Legacy signed KRC/K_Science authorization and external operation
  allowlist are not modified by this PR.

## Tests

- Focused security/provider/DOI negative tests on audited pre-final
  source: 57 PASSED, 0 FAILED.
- Final COMPLETE repository regression on exact code commit:
  **1308 PASSED, 24 SKIPPED, 0 FAILED**, 71.19 seconds,
  pytest process exit code 0.
- Negative tests include bad DOI controls/Unicode whitespace,
  wrong DOI returned by non-empty Europe PMC results, direct
  percent-encoded invalid DOI in both allowlisted API URLs,
  forged provider hostname/port/query, malicious redirects,
  invalid MIME or encoding, oversized response, 404 vs 429 vs 503,
  no unsupported scientific truth promotion.
- The 24 skipped tests were not executed and are not called PASS.

## Isolated staging + rollback rehearsal

Three ordered executions against pinned source trees, with no installed
service mutation:

- BASELINE:
  23418dda183ea2af818dcb746a24abc7fd83df0a
  -> adapter and composition return PROVIDER_DISABLED by default;
  PASS for historical baseline behavior.
- ISOLATED STAGING CANDIDATE:
  d7b48468c858f841f57ca44c25e3bb67232ecf61
  -> adapter and composition return COVERAGE_GAP_METADATA_ONLY
  using bounded injected public metadata; PASS.
- RESTORED BASELINE:
  23418dda183ea2af818dcb746a24abc7fd83df0a
  -> PROVIDER_DISABLED again; PASS.

This is code-level staging and rollback simulation. It is NOT an
on-service deployment or a production rollback proof. A future
installed-service rollout must separately validate unit startup,
import paths, immutable prior release, approval databases and
controlled rollback before production promotion.

## Live public data and currently running server

Prior isolated candidate real HTTPS lookup for
10.1016/j.proeng.2013.03.022 returned Crossref METADATA_ONLY,
Europe PMC NOT_FOUND and valid COVERAGE_GAP_METADATA_ONLY.
Separately, the currently installed KRC public_discovery component
already successfully queried Crossref and OpenAlex (two records
each) without per-query owner consent. Existing live public research
has never been globally blocked.

Installed services checked after rehearsal:
krc-project-n39-post, krc-research-v2, krc-project-n39-read and
krc-sentinel-stage127 all ACTIVE, NRestarts=0, no mutations.

## Interaction with PR36 and remaining gates

- KRC Stage134 PR36 carries an independent signed bibliography.audit
  integration. Its exact operation allowlist still denies external
  Stage127 bibliography POST/GET pending reviewed authorization.
- Critical public metadata safety corrections from this audit have
  also been ported to PR36 without removing its private Stage134
  offline bibliography feature. Independent full PR36 regression
  must be run against that separate resulting commit.
- Before actually installing PR37's Stage131 adapter in a running
  staging service, verify immutable service source location, exact
  runtime dependencies, complete rollback copy and a bounded real
  invocation. This code-source acceptance alone is insufficient.
- Signed external Stage134 E2E, missing real full provider JSON
  custody, source independence and publication acceptance are
  separate unresolved gates.

Conclusion: PR37 SOURCE SECURITY + ISOLATED STAGING PASS;
no completed live deployment, installed-state change or Production
release is claimed.
