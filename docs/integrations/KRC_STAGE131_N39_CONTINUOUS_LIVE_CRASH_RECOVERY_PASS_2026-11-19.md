# Continuous GET live crash recovery acceptance
Date: 2026-11-19
Disposition: LIVE_READER_CRASH_AUTO_RECOVERY_PASS / BOOT_AND_EXTERNAL_ACCEPTANCE_PENDING.

Owner executed reviewed root acceptance script crash mode. Actual reported markers:
LIVE_INTERNAL_BEFORE_CRASH_SHA_200_PASS
NONCE_AND_SCIENCE_DB_QUICK_CHECK_PASS (before and after)
KRC_CRASH_AUTO_RESTART_PASS
NO_BEARER_401_AND_SENTINEL_PID_STABLE
NONCE_AND_SCIENCE_STATE_UNCHANGED_ACROSS_RESTART
LIVE_INTERNAL_NONCE_REPLAY_AFTER_CRASH_403_PASS
LIVE_INTERNAL_FRESH_READ_SHA_200_PASS

Independent KRC post-crash host observation 05:57:55 UTC:
- Reader active enabled PID163631, NRestarts=1, Result=success (previous PID162911).
- Sentinel active enabled PID162881, NRestarts=0, unchanged.
- Stage131 PID46327, Research v2 PID37979 unchanged and active.
- Socket 1002:984 mode0660; no-bearer GET401; temporary timer inactive.
- Nonce DB quick_check ok, 14 rows (previous 12, consistent with two fresh signed reads); science replay DB quick_check ok, count1 unchanged.
- No failed systemd units. No new scientific dispatch observed.

Live internal signed-read and actual systemd crash recovery evidence accepted on KRC side. This is not external OIDC JTI replay or authenticated GET503/200 outage correlation. No full external N01-N40 promotion.
Next operator mode boot-before (snapshot), coordinated maintenance reboot, boot-after (verify changed boot ID, automatic reader/Sentinel/Research v2 readiness and restore legacy manual Stage131). No host reboot performed or authorized by this report. Coordinate no external signed traffic between snapshots. No routine GET OFF. Production NO-GO.
