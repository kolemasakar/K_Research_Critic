# Stage132 live switch local acceptance
Date: 2026-11-20
Disposition: INSTALLED_ACTIVE_LOCAL_PASS / EXTERNAL_TRANSPORT_ACCEPTANCE_PENDING / CLIENT_NO_SEND.

Owner executed exact staged operator switch and reported BROKER_CROSS_UID_MISSING_APPROVAL_403_PASS, ACTUAL_SIGNED_GATEWAY_PILOT_AND_TRANSPORT_DENIAL_PASS, broker boot link created, original five unit hashes OK, STAGE132_SWITCH_LOCAL_PASS_EXTERNAL_ACCEPTANCE_PENDING. One curl connection refusal during planned ingress restart was observed in owner output; readiness succeeded subsequently. No rollback reported.

Independent actual host 20:19:27Z and 20:20:15Z:
- Broker PID10179 active enabled Type=notify Restart=on-failure, actual UID1002 GID984, socket1002:984:0660, boot link correct, NRestarts0.
- Existing KRC gateway PID10271 active, new 20-project-pilot-post.conf identical to immutable release example; existing gateway unit remains disabled and is pulled in by Sentinel. Sentinel PID10278 active enabled NRestarts0, existing original source/config unchanged by operator.
- Reader PID5267 active enabled unchanged, socket1002:984:0660; legacy Stage131 PID2065 active unchanged; no failed units or pending systemd jobs.
- Actual unauthenticated external listener locally reached: GET401 UNAUTHENTICATED, POST403 UNAUTHORIZED. This is reachability and denial only, not externally authenticated delivery.
- Private requests1, science replay1, consent2 all quick_check ok; broker relay nonce2 rows quick_check ok, consistent with two local signed missing-approval probes. No new scientific dispatch observed. Actual pilot KS-2f5ca3707c62d707cbfb28fe4fc01a9d remains PROPOSED, digest95a78f606304733d216a632c12163811fe4854a204b285131e8ad60fe4ef2d0a.

Next run existing Science main attested workflow twice, sequential and no scientific dispatch:
1. T3: probe_stage127_negative=true, all other booleans false, artifact_get=none.
2. Existing GET enabled fixture: probe_stage127_artifact_get=enabled, all four booleans false. Existing approved 398-byte technical fixture expires 2026-11-24 18:09Z; verify before use. No outage/restart tests.
After actual T3/GET logs and state verification, review/merge K_Science PR12 default-off sender (draft head64653de6c75aa270b4fd93e6311fea29729aa6ba), then new exclusive deny mode against actual Stage132, no owner grant spent. Only then one explicit owner approval of displayed exact pilot, fresh execute workflow and SHA/size/task correlation. No local run; never redispatch ambiguous result. Existing connector lacks fresh workflow_dispatch; owner UI needed. No actual external test or client merge performed this turn. Broker auto-restart/boot configured, not independently crash/boot-tested. Production NO-GO; no new provider or public access.
