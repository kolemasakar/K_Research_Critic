# GPT Store Builder 8000-character remediation — 2026-10-31

Target: public Builder instructions at `prompts/GPT_STORE_INSTRUCTIONS.md`.

- Before: 21,793 characters, exceeding the 8,000-character Builder limit by 13,793.
- After: 6,943 characters (verified from the updated source).
- Retained required profile approval choices, exact claim floor phrase, independent source counting, Critic traceability, required report headings/tables and explicit checkpoint handling.
- `tests/test_gpt_store_package.py`: **10/10 PASS**.
- No changes to public GPT installation, user settings, Stage131 installed services or external routes.

## Full regression transparency
Full repo suite after source change: **1044 passed, 17 skipped, 6 failed**.
- Three failures: exact-core-snapshot tests compare legacy plugin skill/unified R39 snapshot against the now-condensed `GPT_STORE_INSTRUCTIONS.md`. These are **real synchronization debt**; do not alter historical snapshots or silently weaken assertions without independent review and a versioned migration.
- Three failures: `test_staging_entrypoint131.py` under unprivileged `krcops` hits PermissionError on live `/run/krc-stage131/backend.sock`; environment-dependent fail-closed checks need isolated socket path/permissions to run, not an active service mutation.

**Outcome:** Builder length blocker itself CLOSED / targeted package tests PASS. Repo-wide release regression remains NO-GO (6 outstanding failures). Prior source-only RC branch `stage131-rc-source-only-20261031` is NOT auto-updated to these changes; no deployment/activation.
