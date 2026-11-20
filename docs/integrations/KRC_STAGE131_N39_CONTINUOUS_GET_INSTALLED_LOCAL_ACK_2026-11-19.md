# N39 continuous GET installed and local lifecycle PASS
Date: 2026-11-19
Disposition: CONTINUOUS_STAGING_ON / LOCAL_LIFECYCLE_PASS / EXTERNAL_RECOVERY_AND_BOOT_ACCEPTANCE_PENDING.

Owner supplied actual root operator output:
original.json: OK
original-read.service: OK
original-drop.conf: OK
config-mode: OK
CONTINUOUS_GET_ON_LOCAL_LIFECYCLE_PASS
EXTERNAL_AUTHENTICATED_RECOVERY_AND_BOOT_ACCEPTANCE_PENDING

KRC independently verified actual host at 05:39:48 UTC:
- Read service active PID162911, Type=notify, Restart=on-failure, NRestarts=0, enabled, continuous working directory.
- Sentinel active PID162881, exact b2a8064027c887065522b4b96f846c3d0540194f working directory, Restart=on-failure, NRestarts=0, enabled.
- Both multi-user.target wants links point to designated units. Existing Sentinel Requires includes tailscaled and Research v2, not read service.
- Stage131 PID46327 and Research v2 PID37979 unchanged and active.
- Lease timer inactive; no routine OFF.
- Runtime reader directory UID1002:GID984 mode0750, socket 1002:984:0660, nonce DB 1002:984:0600, key directory 0:984:0750.
- Canonical unauthenticated GET401 UNAUTHENTICATED. Nonce DB 12 rows quick_check ok. Science replay DB one row quick_check ok. No additional science dispatch observed.

Owner-approved persistent STAGING configuration is now installed and active. Root script local reader stop/start and listener check passed as evidenced by operator output; systemd auto-restart configured, not yet proven by controlled crash or boot. No reboot performed or authorized. No production release.

Remaining: Science rerun existing enabled GET probe on main against new continuous pins (GET enabled, other POST flags false); Sentinel correlate server evidence, coordinate real authenticated outage 503 and fresh recovery 200 SHA, POST during outage, durable replay and boot/start-limit acceptance. Do not interrupt live reader without a coordinated test plan; no new research/provider execution. Full N01-N40 matrix remains incomplete. Permanent normal operation ON; rollback only on failure or owner request. Audit recurring publisher remains pending.
