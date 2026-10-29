# KRC Stage131 vulnerability audit checkpoint — 2026-10-29

**STAGING ONLY / FREE_ONLY / Production NO-GO. This audit blocks promotion of the previously hash-pinned test set until remediated or justified.**

## Evidence
Host: krc-cobalt, separately installed `pip-audit==2.10.1` in `/home/krcops/stage131-audit-venv` (not service runtime). Source lock: `locks/stage131-test-cp312-linux-x86_64.requirements.txt`, 19 packages.
Command: `pip-audit --disable-pip --no-deps -r locks/stage131-test-cp312-linux-x86_64.requirements.txt --format=json`, output `/home/krcops/stage131-audit-report.json` (host-local).
Result **AUDIT_RC=1**, **19 dependencies examined**, **41 vulnerability entries across two packages**, **no query errors**:
- `pillow 12.3.0`: 39 advisory entries (examples `PYSEC-2026-4327`, `PYSEC-2026-4328`, `PYSEC-2026-4326`), tool fix_version `13.0.0`.
- `pytest 8.4.2`: 2 entries referring to the **same** ID `PYSEC-2026-1845` (duplicate ID, do not count as two independent issues); tool fix_version `9.0.3`.
These are results reported by the vulnerability database at query time, not confirmed exploitability in Stage131. A 41-row count is not 41 independent CVEs. An exact deduplication/triage and provider advisory verification are required.

## Dependency policy conflict
Current `requirements-stage131-test.txt` inherits `pytest>=8,<9` and sets `Pillow>=10,<13`. The scanner-recommended fixed versions 9.0.3 and 13.0.0 are beyond those constraints. Do **not** silently upgrade or loosen requirements, as plugin/public package regression compatibility and the PDF processing change need review. No affected packages were installed into Stage126 or Stage127.

## Status
- Hash-enforced installation previously PASS for frozen 19-pkg test set, but **security approval now NOT PASS**.
- No claim of clean vulnerability audit or authorized /opt install.
- Root-owned Stage131 release absent; no service start, real owner grant, scientific E2E or external Artifact GET.
- Safe next steps: investigate distinct advisory IDs and applicability; test separately pinned candidate with `Pillow 13` and `pytest 9` only in isolated venv, run focused and full regression, then regenerate exact hashes if accepted. Existing lock remains immutable historical evidence.
