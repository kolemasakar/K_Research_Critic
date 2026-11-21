# KRC Stage133 controlled staging activation and cross-UID acceptance — 2026-11-21

Status: **STAGING_ACTIVATED / ROOT_CROSS_UID_NEGATIVE_SECURITY_CHECKS_PASS / NO_SCIENCE_E2E / PRODUCTION_NO_GO**.

## Release identity

- Repository: kolemasakar/K_Research_Critic, PR35 (draft), commit a9cb4b5f12930f89775f0d129ca4087295fd52b6 immediately before this acceptance document.
- Staged immutable source: /opt/krc-stage133-offline/d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6.
- Release archive SHA256: d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6.
- Root operator script SHA256: 0c1a6b6bae7d2a73c07901c549f95bf237b166e95ca8fbe19f0c0d554ca0367b.
- Root-owned staging and activation performed by owner in SSH (outside Desktop Commander; it cannot elevate).
- Stage134 bibliography source-only PR36 is **not** included in this release; no metadata API access was initiated.

## Operator sequence and observed results

1. Initial root `stage` completed with ARCHIVE_MANIFEST_PASS, BROKER_UID1002_DEFAULT_OFF_PASS, GATEWAY_UID988_DEFAULT_OFF_PASS, STAGE133_ROOT_STAGED_DEFAULT_OFF_NO_SERVICE_CHANGE_PASS.
2. First `activate` failed: UID1002 and UID988 opt-in checks passed but stage127 transport stopped as a dependency of krc-research-v2.service. Original auto-rollback restored broker/gateway Stage132 units but left stage127 transport inactive. This transient failed attempt is not accepted.
3. Source operator fix introduced explicit stage127 service restoration on activation/rollback and a non-disruptive `recover` mode. User executed `recover`, returning STAGE127_UNAUTHORIZED_GET_401_PASS and STAGE133_RECOVERY_STAGE132_FOUR_SERVICES_AND_GET401_PASS; independently verified all four services active and original Stage132 unit hashes intact.
4. User executed revised root `activate` again and provided exact terminal output:
   - BROKER_UID1002_STAGE133_OPTIN_PASS
   - GATEWAY_UID988_STAGE133_OPTIN_PASS
   - GATEWAY_UID988_TO_BROKER_UID1002_SOCKET_PASS
   - UID988_INVALID_MAC_DENIED_BEFORE_NONCE_OR_SCIENCE_DISPATCH_PASS
   - UNAUTHORIZED_NOBODY_SOCKET_DENIED_PASS
   - STAGE127_UNAUTHORIZED_GET_401_PASS
   - STAGE133_ACTIVATED_CROSS_UID_SOCKET_AND_AUTHORIZED_ROLE_GATES_PASS
5. Independent Desktop Commander read-only host checks at 2026-11-21 14:55 UTC confirmed four ACTIVE services, zero NRestarts, proper Stage133 invocation flags on broker and gateway and expected stage133 PYTHONPATH:
   - krc-project-n39-post.service: PID 19623, UID1002 (krcops), GROUP krc-sentinel-ipc GID984.
   - krc-research-v2.service: PID 19631, UID988 (krcresearch), GID984.
   - krc-project-n39-read.service: PID 5267, ACTIVE.
   - krc-sentinel-stage127.service: PID 19642, UID987, ACTIVE.
   - Broker systemd unit SHA256 c606a950caaeb194f10da26a76694ab12c80b5e2c4192f3f92d400c89cb4fc5a.
   - Gateway drop-in SHA256 9fa8d6a457f37b908ca643a246c41a061976bed1c4201291ba622196b40f77cb.
   - Both installed unit hashes exactly match immutable reviewed opt-in templates in Stage133 release.
   - The external unauthorized staging GET returns HTTP401 on host tailnet address port19017.
6. Independent rootless static acceptance after activation: archive SHA/allowlist, extracted byte parity, file permissions and Bash syntax PASS.

## What this proves

- The reviewed Stage133 immutable package is installed and running with both broker and gateway explicitly opting in to Stage133 offline research operations.
- Real Linux UID988 has been able to connect to a UID1002 broker socket, and kernel SO_PEERCRED verified the expected broker user and shared IPC group.
- A real UID988 connection carrying a deliberately invalid HMAC receives 403; a disallowed `nobody` user cannot connect to the broker socket. No approval token, valid secret, consent, or scientific execution was used.
- Stage127 remains transparently a transport component and rejected unauthorized HTTP GET with 401.
- Operator activation behavior is now consistent with documented gateway/Stage127 systemd dependency; rollback was actually required earlier and the recovery procedure completed.

## Remaining gates

- Operator `verify` after successful activation has not yet been separately executed by root. The activation script ran the same `verify_enabled_roles` function and PASSed.
- K_Science PR14 full pinned-schema tests, independent third-party or separate-owner-code review, operation-specific immutable profile approval and exact scientific result ACK remain pending.
- Two new authorized external E2E calls, one for research.evidence.preflight and one for research.inspection.review, remain NOT_RUN; no grants were issued or reused. Prior Science acceptance remains 2/48.
- research.bibliography.audit is not enabled in this Stage133 rollout; Stage134 PR36 stays source-only without provider network access.
- Production: NO-GO. Do not infer live scientific quality or completion of third-party security audit from these deployment checks.

## Rollback
Root operator retained at /var/backups/krc-stage133-operator-20261121.sh with mode0600 and rollback command:
`sudo bash /var/backups/krc-stage133-operator-20261121.sh rollback`
Rollback restores verified original Stage132 unit contents and explicitly restarts dependent Stage127 after gateway comes up, then requires 401 on the negative ingress probe. No autonomous rollback triggered by this report.
