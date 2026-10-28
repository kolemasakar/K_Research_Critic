# KRC Stage131 PDF dependency and full regression — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Root cause
The two previously failing PDF figure inventory tests failed because isolated Python venv did not contain Pillow (`ModuleNotFoundError: No module named 'PIL'`), not due to a proven defect in PDF extraction or policy. Added Pillow 12.3.0 in isolated venv only. PDF suite `tests/test_p0_figure_asset_inventory.py`: **4/4 PASS**.

Declared isolated test dependencies in `requirements-stage131-test.txt`, commit `50a64e972076074d182c5032efa0f6cd70522c17`: project requirements + jsonschema, pypdf, Pillow; no unreviewed runtime system dependencies and no machine-level installations.

## Full regression
Command from SHA-pinned checkout based on `d824af7f58cc6507f57e659fe0c0eb3c13aa87cd`:
`PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q --disable-warnings tests`
Result: **987 passed, 8 failed, 17 skipped in 40.53 s**. All PDF inventory tests passed. Remaining eight FAIL: GPT Store packaging, public Core exact snapshot, public Builder text limit, Media R3/public plugin legacy snapshot; do not change public package as collateral damage. Full suite **NOT PASS**.

## Release/build gates still open
- `requirements-stage131-test.txt` uses bounded ranges, not a hashed wheel lock. Do not call it an immutable dependency lockfile.
- Immutable root-owned release under /opt still absent, review-only systemd ExecStart placeholder unresolved.
- Stage131 /etc config & secret files not yet created; UID988 read permissions cannot be proven.
- No Stage131 start, external artifact GET, Sentinel recovery, real consent or scientific E2E.
