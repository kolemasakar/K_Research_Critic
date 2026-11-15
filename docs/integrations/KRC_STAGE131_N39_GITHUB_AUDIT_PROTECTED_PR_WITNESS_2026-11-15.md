# KRC N39 protected GitHub audit anchor: Ruleset, PR publication, passive integrity verification, cross-repo witness (2026-11-15)

Scope: no real human consent, new science, grant issuance, root-receipt creation, production service changes, or deployment. All checkpoint events below were synthetic-only. This document does NOT claim independent immutability or WORM storage.

## 1. Actual GitHub ruleset independently read back

- Repository: `kolemasakar/K_Research_Critic` (public).
- Ruleset `KRC-N39-AUDIT-PROTECTION` ID `27332825`: `enforcement=active`, target exactly `refs/heads/audit/n39-anchor-ledger`, empty bypass list, `current_user_can_bypass=never`.
- Rules returned by live GitHub API: `deletion`, `non_fast_forward`, `required_linear_history`, `pull_request`. Required approvals=0 (sole repository contributor), latest-push approval false, review-thread resolution true, merge method `rebase`.
- Source: `GET /repos/kolemasakar/K_Research_Critic/rulesets/27332825`.
- This confirms the configured prevention of deletion / forced non-fast-forward updates without attempting any destructive operation. No attempted DELETE, force push or ref rewrite occurred. Administrator ability to disable/change protection remains a release risk.

## 2. Protected-branch writes exercised via PR

- PR #31: verified Ruleset metadata written on a child branch then merged via required rebase PR into protected target; protected merge commit `bf36d01cce9566d5486023ea542deeef02d2eae5`.
- New read-only exporter `tools/n39_github_anchor_export.py`, pinned source `20f3dc1075f27e969d97c3cdf4f0f99ecb926449`, verifies local SQLite audit-chain sequence, exact canonical chained SHA-256, restricted local database mode and immutable-name public manifest. Rejects unapproved non-synthetic export, invalid SHA/ID and corrupt chain. No GitHub token or direct write, no grant issuance.
- On isolated krc-cobalt, generated a synthetic-only one-event `N39AuditJournal` and exported journal `n39-isolated-demo-20261115`, seq 1, SHA-256 head `f1161aa6c54d8b629323af72057fe5726811c2a75d707d121eaaaf5a16d225e4`, with no actual owner consent, scientific action, receipt or root-owned file.
- PR #32 appended the synthetic-only SHA-256 manifest via rebase into the protected branch; immutable Git merge commit `06bd981172118f273868da243a0faeea3ea01fed`. This commit is **one ahead** of the prior protected commit `bf36d01cce9566d5486023ea542deeef02d2eae5`, verified with GitHub compare API.
- PR #33 then updated the protected branch README to match the actual ruleset and witness limits; protected documentation commit `17dea84013392c0efda6bdb09f12d6f287283842`. It is **two commits ahead** of the `bf36d01...` prior checkpoint (one synthetic anchor and one README update). No rewriting detected in the compared lineage.
- Final protected HEAD: `17dea84013392c0efda6bdb09f12d6f287283842`.

## 3. Non-destructive controls

- GitHub API read: actual active ruleset + exact target + no bypass. PASS.
- GitHub API compare `bf36d01...` -> `06bd981...`: `status=ahead, ahead_by=1`, new synthetic anchor file. PASS.
- GitHub API compare `bf36d01...` -> `17dea840...`: `status=ahead, ahead_by=2` (anchor+README). PASS.
- Actual PR merging with configured Rebase succeeded in both tested cases. PASS.
- Destructive deletion/force-push controls **not actively tested**, as explicitly waived by non-destructive testing instructions; their policy presence is verified but no claim of empirically rejected destructive API request is made.
- GitHub cannot provide an independently controlled immutable append-only anchor merely through branch protection. Ruleset administrators can change protection. This remains a release hold.

## 4. Cross-repository durable copies

Two partner repository files record the exact **synthetic anchor** SHA-256 and protected commit as cross-repository witnesses (NOT independently administered immutable storage):
- Sentinel: `kolemasakar/Sentinel-Remote`, commit `b1870f74ca5cf770a9e6d9a3d97d676722019588`, `docs/integrations/KRC_N39_GITHUB_ANCHOR_CROSS_REPO_WITNESS_2026-11-15.json`.
- Science: `kolemasakar/K_Science`, commit `b5758ef40c83fcd71633b9bfbbbad924b547f0c5`, same relative file path.
- Both repositories belong to the same owner `kolemasakar`. This is physically/logically separate Git history, but **NOT** independent administrator/identity control. A truly independent custodian (or off-platform WORM) and verification service remain pending.
- These copies include NO real authorization, personal identifiers, keys or scientific artifact bytes.

## Release gates NOT satisfied

1. Independently held immutable commit witness beyond sole GitHub-owner control.
2. Owner-approved authentication, out-of-band issuance SOP and privileged operator.
3. Automatic trusted publisher + audit-to-root-installer transaction consistency and final negative E2E checks; the exporter and PR execution are isolated and manual.
4. K_Sentinel and K_Science independent acceptance of the new audit anchor path; external N01-N40 integration and installed parity.

GET/signer OFF. Stage127/131/Research v2 unchanged. 200 MiB load test OWNER_WAIVED/NOT_TESTED. Production NO-GO.

## Validation after exporter source update
- Isolated `krc-cobalt` source/test pin `20f3dc1075f27e969d97c3cdf4f0f99ecb926449`:
  - Focused audit + export: **11 PASS / 0 FAIL**.
  - Entire KRC source regression: **1157 PASS / 18 SKIP / 0 FAIL in 48.50s**.
- Documentation-only commit followed the tested source. No installed services changed.
