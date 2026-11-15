# KRC N39 audit anchor ledger

This is the **public GitHub checkpoint repository location**, not a source of scientific consent. It contains only audit-chain digests and nonsensitive metadata, never approval tickets, identities, tokens, HMAC keys, consent files or artifact content.

## State and limits

- Dedicated branch: `audit/n39-anchor-ledger`; directory: `audit/n39/`.
- Genesis represents an **empty** journal (`seq=0`, SHA-256 chain head = 64 zero characters). It is not an audit of a real grant.
- Each future checkpoint MUST be an immutable-name file `anchors/<journal_id>/<seq-padded>-<head_sha256>.json` committed exactly once. Never update or delete an existing checkpoint. Do not backdate events.
- Each checkpoint MUST include exact monotonic `seq`, `head_sha256`, `previous_checkpoint_commit`, `journal_id`, observed UTC time, and the digest of the KRC source version, with no personal identifiers.
- Checkpoints are accepted only after an independent reviewer verifies them against KRC's local event-chain hash and verifies that this GitHub commit is a descendant of the last previously witnessed checkpoint. Source code cannot self-declare its own issuer authority.
- Two phases for each authorization: (a) anchored INTENT **before** protected file installation and (b) independently anchored OUTCOME **after** install. If GitHub write/read fails, deny installation or activation.
- GitHub branch history is **not inherently WORM/immutable**. Administrators may rewrite or delete Git refs; a compromised maintainer may alter public objects. This branch is therefore an **external audit witness only**, pending GitHub branch ruleset and a second independently controlled witness (K_Sentinel / K_Science or other retained checkpoint copy).
- No automatic GitHub token or network request has been added to the running KRC service. No grants are issued, signer/GET remain disabled, and no production authorization is implied.

## Mandatory repository controls (currently NOT VERIFIED)
1. Repository Settings > Rules > Rulesets: apply to branch `audit/n39-anchor-ledger`, block deletion and force pushes, require a pull request with independent review, prevent bypass including repository administrators where supported.
2. Restrict who can write this branch; disable direct pushes for operational accounts; enforce 2FA and use expiring fine-grained credentials only in the offline anchor publisher.
3. Independently preserve each checkpoint Git commit SHA outside the KRC repo, and run digest/lineage verification before trusting it.
4. Implement a verified, narrow anchor publisher and enforce durable audit-to-install transaction order. Until these controls are live, this ledger is **CREATED / UNPROTECTED / NOT ACCEPTED AS IMMUTABLE**.

Owner approval SOP (draft): [KRC proposal](https://github.com/kolemasakar/K_Research_Critic/blob/security/stage131-uds-bounds-20261101/docs/integrations/KRC_STAGE131_N39_OWNER_ISSUANCE_AUDIT_SOP_DRAFT_2026-11-15.md).
