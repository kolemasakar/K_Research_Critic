# Stage132 operator deployment and first real pilot preparation
Date: 2026-11-20
Disposition: ROOT_OPERATOR_READY / CLIENT_DRAFT_READY / ACTUAL_PROPOSAL_PROPOSED / LIVE_INSTALL_AND_E2E_PENDING.

Owner requested deployment, verification, client enablement and first E2E in sequence. Current privileged access is operator SSH only; Remote Desktop Commander krcops UID1002 cannot sudo. No privilege bypass. Host actual preflight 19:49–20:00 UTC confirms active unchanged gateway720, reader5267, Sentinel1454, legacy Stage131 2065, no unexpected drop-in, no new broker installed, prior live science replay count1 and DB integrity ok. Old gateway socket stat from UID1002 denied as expected; root verifies real role custody. No state or configuration change to running services.

## Exact release v2
Supersedes archive v1 only for gateway drop-in: remove ReadOnlyPaths bind mount of broker runtime directory, which could hold a stale inode namespace after broker restart. Existing ProtectSystem=strict remains; no ACL change. Source b77c237c850a8ce9382d1abda05637b4f9f86b85, four Stage132 Python sources unchanged since 19/19 isolated PASS, no new runtime test claimed. Candidate archive /home/krcops/stage132-post-candidate-20261120/stage132-post-release-candidate-v2.tar SHA e1e03b5afd04d22f033711c02272e9c4b3160fc1c8c642a73988bc5c5c750993. All ten member hashes passed; actual exact allowlist extractor exercised in disposable private directory, PASS.
Exact operator script deploy/stage132/operator_install_project_post.sh commit ec16054e613fd010009c78c3dfa6cb2499d2e64f, blob4612eb3f95e2776e9c61a2616aa1ca9b6aec2d3c, SHA256 18fe023d20e4f97b825a124ef9b97dd79e656343b961b05f94d7d2e2dfccc9bd. Actual staged path /home/krcops/stage132-post-candidate-20261120/operator_install_project_post.sh; bash -n and 8 embedded Python blocks compiled, UID1002 refusal77 verified. Stage checks exact existing unit hashes, root-held verified archive extraction, immutable allowlisted release, distinct key copies UID988/1002 mode0400, nonce DB creation, role imports/config/key separation and producer preflight, verifies broker unit and compares state counts. No service starts or stops in stage.
Switch: one authorized maintenance window; activate broker standalone and cross-UID missing-approval403 probe, custody and PID checks before old gateway stop; then explicit stop Sentinel and old gateway due Requires dependency, install only KRC gateway drop-in, start gateway then Sentinel, GET401, unchanged reader and legacy Stage131 PIDs, actual signed gateway pilot/transport denial under UID987, boot-enable broker; compare private consent/request/science counts, original units intact. Root rollback on failure removes own drop-in/marker, disables broker and restores old gateway/ingress; failure before cutover does not restart ingress. No provider, scientific dispatch, forced reboot, reader stop, Sentinel source/config/ACL change. Interrupts ingress briefly at intentional cutover; not a zero-downtime promise. Root stage/switch and actual runtime cross-UID tests NOT_RUN. Do not blindly repeat partially completed stage; inspect failure.

Owner commands:
sudo install -o root -g root -m 0600 /home/krcops/stage132-post-candidate-20261120/operator_install_project_post.sh /var/backups/krc-stage132-operator.sh
echo '18fe023d20e4f97b825a124ef9b97dd79e656343b961b05f94d7d2e2dfccc9bd  /var/backups/krc-stage132-operator.sh' | sudo sha256sum -c -
sudo bash /var/backups/krc-stage132-operator.sh stage
After actual staging and checks, switch mode. Then inspect live state and rerun no-science external T3/GET baseline and new unapproved pilot denial.

## Science client
K_Science draft PR12 https://github.com/kolemasakar/K_Science/pull/12 head64653de6c75aa270b4fd93e6311fea29729aa6ba; isolated exact sender blob06791456d393fce797167494b53306fe29645eb1/test e58d1057d09a9a3490e10504b4fea46ae080db90, 8/8 unittest PASS after adding missing existing dependency files to isolated test copy. Test mock wire, no live execution. Same attested workflow file, new mode none(default)/deny/execute, main/first attempt/exclusive, input approved proposal from trusted KRC channel; no input can grant server authority. One POST, fresh GET token, exact authoritative descriptor retained, result checked by PR11 receiver. No retry after uncertain POST/GET. Draft open; live workflow unchanged until actual installation and review. Deny mode unapproved random RID, execute mode requires approved exact proposal. No workflow dispatch performed; connector does not provide fresh workflow dispatch.

## Actual first proposal
Created via installed trusted private project wrapper propose only, verified show:
request_id KS-2f5ca3707c62d707cbfb28fe4fc01a9d
profile_sha256 95a78f606304733d216a632c12163811fe4854a204b285131e8ad60fe4ef2d0a
status PROPOSED
profile_id KS-STAGE127-PILOT-20261120, version v1, protocol KRC Core.
purpose: Technical end-to-end acceptance of ONE profile-validation operation for the K_Science concrete NDT research programme. No external source investigation, provider calls or scientific conclusions.
operation research.profile.validate; policy FREE_ONLY_OFFLINE.
topic: Non-destructive testing of concrete structures: geodetic methods, ultrasonic measurements and strength assessment.
expected task_id KS-2f5ca3707c62d707cbfb28fe4fc01a9d-task.
No explicit approval recorded yet; owner one specific approval after exact proposal display and live release gates. No local run, no POST. Existing live science replay remains1. First E2E and 48-case matrix remain NOT_RUN. Production NO-GO.
