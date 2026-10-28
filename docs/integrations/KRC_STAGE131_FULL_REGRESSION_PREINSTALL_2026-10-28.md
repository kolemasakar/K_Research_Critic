# KRC Stage131 — isolated source and regression checkpoint, 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.** No service modifications.

On krc-cobalt unprivileged verified Git checkout:
- Head SHA `9d57289552de7088d44dfbbe22d26b2e3fe9f990`, working tree dirty files 0.
- Stage131 paths /etc/krc-stage131, /run/krc-stage131, /var/lib/krc-stage131 absent. Thus real UID988 config/secret filesystem access cannot yet be confirmed; neither secrets nor grants were opened.
- `systemd-analyze verify` after copying example to /tmp/krc-stage131-review.service reported the unresolved `REPLACE_WITH_REVIEWED_FULL_SHA` binary path, expected for review-only sample. NOT installation-ready. No production unit loaded.
- Stage126 krc-research-v2 ACTIVE PID37979 NRestarts0; Sentinel Stage127 INACTIVE MainPID0 at observation; no claim of recovery.

Full isolated source regression `PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q --disable-warnings tests`: **985 passed, 10 failed, 17 skipped in 40.44s**. Known 10 failures are public GPT Builder/Skill exact snapshots/limit and 2 PDF inventory tests. Nonzero test result; no full PASS claimed. Focused Stage131 permission/security tests previously 18/18 PASS.

## Next independent KRC gates
1. Resolve 2 PDF inventory tests after checking traceback/environment dependency, never bypass security.
2. Pin immutable /opt/krc-stage131/<SHA> and venv dependencies, verify systemd on fully populated isolated candidate.
3. Determine UID988 access to Stage131 config/secret only **after** root-controlled files are explicitly created/reviewed; never borrow Stage126 keys.
4. No Stage131 start, consent issuance, or Sentinel external HTTP GET until individual approval/acceptance.
