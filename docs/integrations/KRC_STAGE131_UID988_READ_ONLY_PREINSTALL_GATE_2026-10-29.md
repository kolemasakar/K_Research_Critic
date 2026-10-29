# Stage131 UID988 preinstall gate and dependency policy — 2026-10-29

**STAGING ONLY / FREE_ONLY / Production NO-GO**

## Dependency policy
The previously completed Pillow13/pytest9 remediation remains a separate Stage131 test-only lock `locks/stage131-remediation-cp312-linux-x86_64.requirements.txt` (19 hashes, scan 0 advisories at audit time). Main requirements constrain pytest<9 and legacy test requirements Pillow<13, so the remediated lock is not promoted to general dependencies. Preserve public plugin package baseline; no automatic install or service activation.

## New read-only operator gate
`scripts/stage131_preinstall_audit.py --service-uid 988` checks lstat metadata only, never reads the contents of keys or config and makes no system changes. It reports ownership and exact modes of dedicated Stage131 private config/state, runtime 0750 and three expected private config/key files 0600. Exact key basenames are provisional until reviewed config is issued. Does not test effective execution/ACL/traversal as UID988 or verify signatures.
`tests/test_stage131_preinstall_audit.py` plus runtime permissions tests: **4/4 PASS** on krc-cobalt.

Actual operator read-only run: **6 NOT_READY**, no Stage131 paths/config/keys provisioned; exit code 2, not installation-ready. This is deliberately fail-closed. Service UID988 verified in prior incident evidence; actual key access not demonstrated. Production remains NO-GO.

## Remaining gates
- Define root-controlled delivery and owner-reviewed private config/secrets to service UID988 without sharing Stage126 keys; after provisioning test effective UID988 access while not disclosing secrets.
- Verify root-owned immutable /opt release and version-pinned venv; systemd verify actual installed ExecStart; no enable/start without reviewed authorization.
- Review independent package publisher provenance / signatures and security advisories, beyond hash integrity.
- Stage127 external GET/OIDC/replay/T4 acceptance and science E2E separately owned and NOT inferred from transport availability.
