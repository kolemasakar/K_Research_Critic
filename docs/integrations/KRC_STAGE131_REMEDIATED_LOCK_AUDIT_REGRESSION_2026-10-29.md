# Stage131 remediated dependency audit and offline hash lock — 2026-10-29

**STAGING ONLY / FREE_ONLY / Production NO-GO**

- Independently isolated remediation venv with Pillow **13.0.0**, pytest **9.0.3**, 19 packages in total. pip-audit 2.10.1 using `--disable-pip --no-deps -r <(pip freeze) --format=json`: **19 audited, 0 reported vulnerabilities, RC0**, no identified errors. Tool result does not guarantee absence of unknown vulnerabilities or provenance.
- Full source regression with remediated venv: **987 passed, 8 failed, 17 skipped in 41.35s**; remaining eight are known public GPT Store/Builder/Core snapshots, not new Stage131 failures. Full repository PASS not claimed.
- Separate host-local 19-wheel remediation wheelhouse generated for Linux CPython 3.12 x86_64. Hash-enforced lock `locks/stage131-remediation-cp312-linux-x86_64.requirements.txt`. **SHA-256: `aa9644375f6f90b7ca384722b55cc07c433009e9a6e03599ac7939865d00da48`**, byte-for-byte matches host-generated lock (`cmp` RC0).
- Independent new `/home/krcops/stage131-remediation-hash-venv` installed using `--no-index --require-hashes --find-links=/home/krcops/stage131-remediation-wheelhouse` with successful `pip check` (no broken requirements). Targeted tests on hash-installed environment **7/7 PASS** (permissions, HTTP GET, PDF).
- Main `requirements.txt` remains constrained to pytest<9 and `requirements-stage131-test.txt` still Pillow<13. Remediated lock is a **TEST-ONLY separate candidate**, not a replacement production lock or fully compatible declaration. No Stage126/Stage127 runtime changes, no Stage131 activation, consent or scientific E2E.
- Pending: decide isolated Stage131 test-specific requirement override vs broader dependency policy; independently review package provenance/signatures, complete config/secret operator acceptance, confirm Sentinel T4 and E2E criteria.
