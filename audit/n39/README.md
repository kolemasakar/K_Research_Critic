> **Personal project mode — owner-approved 2026-11-16/17.** The legacy INTENT/OUTCOME grant workflow below remains historical; in current single-owner mode it is replaced by [PROJECT_CHECKPOINT_FORMAT.json](PROJECT_CHECKPOINT_FORMAT.json) for observed private consent/execution/artifact state. The existing protected GitHub branch is accepted. Independent administrative custody, a second account, and separate human read grants are deferred, not acceptance blockers. No raw consent/profile/identity or artifact bytes in the public ledger. Each new hash-only checkpoint is append-only through PR, with exact content and ancestry verified before the separate local publication receipt. This is an observed snapshot, not a backdated event or authorization. No server GitHub credential is required for publication via the already connected trusted project tool. Local outbox failures must be reconciled without replaying research.

# KRC N39 audit anchor ledger

This is the **public GitHub checkpoint repository location**, not a source of scientific consent. It contains only audit-chain digests and nonsensitive metadata, never approval tickets, identities, tokens, HMAC keys, consent files or artifact content.

## State and limits

- Dedicated branch: `audit/n39-anchor-ledger`; directory: `audit/n39/`.
- Genesis represents an **empty** journal (`seq=0`, SHA-256 chain head = 64 zero characters). It is not an audit of a real grant.
- Each future checkpoint MUST be an immutable-name file `anchors/<journal_id>/<seq-padded>-<head_sha256>.json` committed exactly once. Never update or delete an existing checkpoint. Do not backdate events.
- Each checkpoint MUST include exact monotonic `seq`, `head_sha256`, `previous_checkpoint_commit`, `journal_id`, observed UTC time, and the digest of the KRC source version, with no personal identifiers.
- Checkpoints are accepted only after an independent reviewer verifies them against KRC's local event-chain hash and verifies that this GitHub commit is a descendant of the last previously witnessed checkpoint. Source code cannot self-declare its own issuer authority.
- Two phases for each authorization: (a) anchored INTENT **before** protected file installation and (b) independently anchored OUTCOME **after** install. If GitHub write/read fails, deny installation or activation.
- GitHub branch history is **not inherently WORM/immutable**. Administrators may rewrite or delete Git refs; a compromised maintainer may alter public objects. This branch is therefore an **external audit witness only**, with an ACTIVE GitHub ruleset but still awaiting a second independently controlled witness (K_Sentinel / K_Science or other retained checkpoint copy).
- No automatic GitHub token or network request has been added to the running KRC service. No grants are issued, signer/GET remain disabled, and no production authorization is implied.

## Verified branch rules and remaining controls (2026-11-15)
1. **VERIFIED** Ruleset `KRC-N39-AUDIT-PROTECTION` ID `27332825`, ACTIVE, exact target branch, no bypass, blocks deletions/force pushes, linear history, PR required (0 approvals because one repository contributor), rebase only. This does not amount to independent approval.
2. Restrict who can write this branch; disable direct pushes for operational accounts; enforce 2FA and use expiring fine-grained credentials only in the offline anchor publisher.
3. **PARTIAL** The protected synthetic-only chain commit `06bd981172118f273868da243a0faeea3ea01fed` and head `f1161aa6c54d8b629323af72057fe5726811c2a75d707d121eaaaf5a16d225e4` were copied into partner Git repositories: Sentinel commit `b1870f74ca5cf770a9e6d9a3d97d676722019588`, Science commit `b5758ef40c83fcd71633b9bfbbbad924b547f0c5`. All are controlled by the same GitHub owner; these are cross-repo copies, NOT independent administrative custody.
4. **PARTIAL** Isolated source exporter `tools/n39_github_anchor_export.py` verifies a real local audit chain and emits a synthetic-only manifest; GitHub PR #32 successfully merged an actual SHA-256 test checkpoint through the protected ruleset (PR #31 first merged ruleset metadata). Operational issuer and anchored outcome integration are NOT enabled. **ACTIVE RULESET / PROTECTED GIT HISTORY / INDEPENDENT IMMUTABILITY NOT ACCEPTED**.

Owner approval SOP (draft): [KRC proposal](https://github.com/kolemasakar/K_Research_Critic/blob/security/stage131-uds-bounds-20261101/docs/integrations/KRC_STAGE131_N39_OWNER_ISSUANCE_AUDIT_SOP_DRAFT_2026-11-15.md).
