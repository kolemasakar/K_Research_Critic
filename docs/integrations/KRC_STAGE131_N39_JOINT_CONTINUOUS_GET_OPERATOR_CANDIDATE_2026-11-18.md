# N39 joint continuous GET operator candidate
Date: 2026-11-18
Disposition: JOINT SOURCE CANDIDATES READY / ROOT OPERATOR PROCEDURE STAGED AND STATICALLY VERIFIED / NO PERMANENT RUNTIME SWITCH.
Owner target: continuous GET ON after accepted release; no routine manual OFF.

## Accepted source inputs and actual host baseline
- KRC 549d44868f188c6f6715bd9224c6fa4de29b05cf, full 1206 PASS / 18 SKIP / 0 FAIL, independent Sentinel 3/3 lifecycle tests.
- Sentinel b2a8064027c887065522b4b96f846c3d0540194f, independently reported 44/44 isolation regression and repeated package test. See PR29 #6991661621, Sentinel report ef09686c9b649e22ec418d17d3b77414f93fec82.
- Actual external Science enabled run 44397533267 completed success: five receiver SHA/size checks, 17 observed checks. Full N01-N40 and permanent boot/start-limit acceptance still pending (not inferred from this run).
- Read and Sentinel remain on the previous temporary pins, active PID159498/159524. Timer active, expiry 21:21:26 UTC. No interruption or cancellation performed.
- Actual Sentinel unit static, no multi-user.target boot link; Research v2 unit disabled, required by Sentinel, tailscaled enabled. Proposed explicit boot link for Sentinel plus independent KRC reader link. Existing Requires=tailscaled.service krc-research-v2.service retained; no new fatal read dependency. Stage131 and Research v2 not restarted by candidate preparation. Existing Research v2 Type=simple readiness on boot and actual boot ordering still need runtime acceptance.
- Actual installed baseline hashes:
  - KRC temporary unit e46d43f62b1b2bfd45dd4a81c86656fb6a4d963db9365045bdf87c104b84c571
  - Sentinel base ec212137efb8801f6ca8df19ec9805f3bcbd9be77990cfe912c4d3efa4b56f44
  - Sentinel 10 recovery 8e6cc4b2ba1fd324c301d66fb1b6c79f4790bdb280b864e4bce485a33dabf5d6
  - Sentinel 20 current drop-in 77a8952a29c8c92f66fd20ef54070940704e3efa58700ea13da35030c67f6d54

## Exact staged procedure, not root-executed
- Source script deploy/stage131/operator_joint_continuous_get.sh commit 1e898768b410b0d687478df30f3921e0423fda39, blob 433daa62534c2045a1db699c1a324109539e5f28, SHA256 b5f69060c0bc7295c07bd9d1f2e3dc2cc09c95ea87dc852545b5636ea7fbcfc8.
- Actual server file /home/krcops/krc-project-n39-read-release-20261118/operator_joint_continuous_get.sh.
- KRC archive at same directory continuous-candidate.tar SHA256 b2d993847b103561323e914ecb1a08ca96f762be77b9af1ebf924e6cb09edbae, 101 members.
- Sentinel archive /home/krcops/stage127-get-continuous-20261118/stage127-continuous.tar SHA256 97318fb098a8b683e68ea938eda58594dc957b630c60a8e19117ada378618e55, 19 members.
- Both hashes rechecked on actual host. Script bash -n, 3 embedded Python blocks compile, unprivileged refusal77, both archive allowlists, extracted full byte equality with exact authentic archives, 18/18 Sentinel SHA256SUMS and four lease guard cases PASS. No real privileged install, switch, boot enable, rollback or service restart attempted.

Modes:
1. stage: copies root-held verified archives, immutable fresh KRC and Sentinel directories, exact byte parity/import checks only; no config, marker, unit, listener or PID change. Can run during temporary lease after source review. Refuses pre-existing destinations; preserve partial staging for investigation if failure.
2. switch: only after temporary lease actually closed (timer/service inactive and temporary marker absent), joint release decision and partner source review; verify exact old units, preserve private config/metadata, root-only hashed backup and original KRC unit/Sentinel drop-in. Install continuous unit and replacement 20 drop-in, preserve base + recovery, daemon-reload, restart only Sentinel, validate default OFF HTTP404. Real external POST T3 required before on; no new execution.
3. on: only after accepted switch and actual POST regression plus authorized joint STAGING release; check exact staged units/config, establish persistent root marker, start KRC notify reader, verify actual socket/ready, enable GET and restart only Sentinel. Controlled local reader stop/start while Sentinel stays at same PID and no-bearer401, then explicit boot links for independent reader and existing static Sentinel. Does not prove authenticated GET503 or POST during outage; separate coordinated external runner tests are needed. Boot links proposed, no reboot in script. Runtime boot/start-limit and authenticated recovery evidence must be obtained before production or unconditional permanent acceptance.
4. rollback: not routine OFF; only failed deployment, integrity/access regression or operator request. Restores exact saved OFF config and prior unit/drop-in, removes only transaction-created boot links and marker, stops new read, restores previous Sentinel and verifies 404. Preserve releases, continuous link, private backup, all keys, nonce/JTI, producer, audit. If restoration cannot verify OFF, fail closed/stop ingress as coded, operator investigates. One transaction; do not blindly rerun after partial failure. No forced reboot or unrelated restart. 

Root-held invocation (REVIEW ONLY until source review and operator decision; stage has no runtime effect):
```bash
sudo install -o root -g root -m 0600 \
 /home/krcops/krc-project-n39-read-release-20261118/operator_joint_continuous_get.sh \
 /var/backups/krc-n39-continuous.sh &&
echo 'b5f69060c0bc7295c07bd9d1f2e3dc2cc09c95ea87dc852545b5636ea7fbcfc8  /var/backups/krc-n39-continuous.sh' |
 sudo sha256sum -c - &&
sudo bash /var/backups/krc-n39-continuous.sh stage
```
Expected CONTINUOUS_FILES_STAGED_NO_RUNTIME_CHANGE.
After joint gate and lease closure, separate commands switch/on as described above; do not issue on prematurely. Script cannot prove external POST evidence itself, so operator must verify it before on. Root execution unavailable in existing remote tool. No additional identity/read grants, no providers, no science execution.

## Joint acceptance work
Sentinel review exact joint script and actual static service boot finding, confirm baseline/boot links/dependency policy, arrange external POST and GET503/read recovery test and per-case audit. Science verify external receiver and coordinate fresh OIDC reads during outage/recovery, report matrix dispositions. KRC stage approved immutable files and verify UID/GID, nonce and read/POST lifecycle after actual root action. No permanent install until joint stage gates. Existing temporary lease automatically closes under its previously approved timer; this is not the normal operating mode. No manual OFF issued. Production NO-GO. Recurring audit publisher still pending; no server credential added.
