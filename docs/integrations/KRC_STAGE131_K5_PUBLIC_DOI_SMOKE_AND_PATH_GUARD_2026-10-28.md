# Stage131 K5+K3 path security continuation — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## K5 public metadata live smoke (KRC only; non-scientific)
One manually selected public test DOI `10.1038/nature12373` was queried through existing read-only provider adapters on krc-cobalt, using isolated verified-source test environment. Crossref returned `METADATA_ONLY`; Europe PMC returned `HTTPError` (exact HTTP code not captured; do not claim absence in catalog). Scientific methods verified: false. Thus two-provider metadata reconciliation **NOT PASS**. No private documents, no credentials, no paid fallback and no automatic science approval.

## Stage131 config isolation
Fixed secret-key path escape: `/etc/krc-stage131/../krc-research-v2/...` is now denied by exact parent check; symlinked secret files are also refused. Added explicit negative regression. Commit `4fbd014b1711ab2df833c6f1aa7720b62ddcc516`. On pinned cloned checkout: entrypoint/consent custody/isolated UDS signer/bibliography/metadata focused tests **20/20 PASS**.

## Still open
- K5: inspect whether Europe PMC HTTP failure is transient/provider access, retry only with bounded nonsecret public DOI requests and provider-status logging. Keep scientific approval denied on partial results.
- K2: no Stage131 server install or start.
- K3/K4: no real owner grant; signer off at entrypoint; isolated approvals directory mandatory.
- K6/K7: final reviewed schemas, artifact GET/expiry/quotas and bilateral signing protocol.
- K8: complete full suite previous pinned checkpoint 971 PASS/10 FAIL/17 SKIPPED; current head only focused tests, no new full pass asserted.
- K9: genuine scientific E2E NOT_RUN.
