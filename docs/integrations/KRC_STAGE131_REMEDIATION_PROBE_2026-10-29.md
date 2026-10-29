# Stage131 remediated dependency probe — 2026-10-29

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

After vulnerability audit identified Pillow 12.3.0 and pytest 8.4.2 in the 19-wheel historical hash lock as affected, created an independent unprivileged venv `/home/krcops/stage131-remediation-probe-venv`. Installed *candidate only* `Pillow==13.0.0`, `pytest==9.0.3` plus existing Pydantic 2.14.1, PyYAML 6.0.3, python-dotenv 1.2.4, jsonschema 4.26.0 and pypdf 6.21.4. Targeted Stage131 entrypoint, permissions, schema, private GET and PDF Inventory tests **19/19 PASS (1.76 s)**.

**Not yet proven:** remediation candidate complete dependency audit, full regression with pytest9/Pillow13, hash lock, vulnerability-free upstream artifacts, publisher attestation, production acceptability. Existing `requirements.txt` (pytest<9) and `requirements-stage131-test.txt` (Pillow<13) currently forbid these versions. Do not change requirements/public plugin until release compatibility and security review. No services changed or started.

Next: run scanner against exact candidate installed environment, full suite, record actual remaining failures, create versioned test-only remediation lock (not replace historical lock), and obtain independent provenance. No root install or consent issuance.
