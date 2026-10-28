# Stage131 isolated test environment evidence — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

- Host `krc-cobalt`; nonprivileged disposable venv `/home/krcops/stage131-test-venv`; no unit restart and no Stage131 service install.
- GitHub branch head checked before run: `9d2c49a36b0a5544dedeef4cba2d907b89ca4611`. Host source `/home/krcops/krc-stage128-test` is **not a git checkout**, and **does not prove this exact SHA**; results are local source regression only.
- `requirements.txt` installed in venv; added test imports `jsonschema` and `pypdf` independently in venv, not system Python.
- Focused pytest run: 29/29 PASS on signer, consent, bibliography, metadata and four-operation inventory.
- UDS/research boundary/artifact/science adapter: 23/23 PASS.
- Full `pytest -q --disable-warnings --maxfail=1 tests`: **103 passed, 1 failed**. The first failure is `tests/test_gpt_store_package.py::test_manifest_preserves_store_first_invariants`: public Builder instructions exceed 8000 characters, unrelated to Stage131 local science transport. Test stopped at first failure; whole-suite PASS NOT CLAIMED.
- No owner-issued real consent, no new service started, no live bibliography metadata lookup, no real E2E-01–05.
- Stage126 PID37979 NRestarts0 observed before tests.

## Release blockers
1. Immutable full SHA-attested Stage131 source checkout and isolated dependency lock.
2. Determine whether GPT Store overlength is preexisting test fixture or code issue; keep public publication paused, do not edit its instructions merely to force PASS.
3. Complete local Stage131 integration regression with actual new code and explicit approvals_dir.
4. Finalize private science schemas and artifact exchange and stage public DOI-only metadata smoke.
