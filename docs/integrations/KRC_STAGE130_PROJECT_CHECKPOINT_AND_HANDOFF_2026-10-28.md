# KRC Stage130 — Project state and handoff checkpoint (2026-10-28)

**Staging only / FREE_ONLY / production NO-GO.** This is the canonical continuation checkpoint; do not infer live scientific success from synthetic tests.

## Repository and versioning
- Repo: `kolemasakar/K_Research_Critic`, branch `agent/krc-public-media-r3-integration`.
- Current verified code branch baseline before this checkpoint: `758a0929265d799e9f2c3235a5666ba7517bcd01`.
- Installed active KRC Stage126 under `/opt/krc-research-v2` originates from the separately archived old release commit `68ef138a449b81d1a222a453072e95b0a9ea6407`. **Stage128/129/130 changes have not been deployed to active daemon.** Runtime SHA is not independently measured after install; treat origin as installation provenance, not runtime attestation.
- Isolated tests on `/home/krcops/krc-stage128-test`: selected Stage130 regression **38/38 PASS** (8.25s), including selected signing/consent/UDS/replay/bibliography. Stage129 21/21 PASS and Stage128 30/30 PASS are subset checkpoints, not additional independent coverage.
- No real Crossref/Europe PMC external calls in Stage129/130 test suites. No verified human owner consent issued. No unpublished K_Science corpus accessed.

## Actual host invariants last verified
- `krc-research-v2.service`: `active`, PID `37979`, `NRestarts=0`, manual start/auto-enable disabled earlier. `krc-stage114.service`, `kscience-krc-gateway.service`, `krc-public-mcp.service`: all active.
- KRC process UID `988` `krcresearch`, group `krc-sentinel-ipc` GID 984; Sentinel UID 987. Active UDS `/run/krc-research-v2/backend.sock` was verified owner `krcresearch:krc-sentinel-ipc` mode 0660; positive `/healthz` via Sentinel UID 987 HTTP 200 staging; HMAC+valid transport admitted then deliberately invalid science returned 409; tampered transport 403.
- `/etc/krc-research-v2` owner root, group krc-sentinel-ipc mode 0750; `/etc/krc-research-v2/approvals` and `approvals-test` same. `/etc/krc-research-v2/staging.json` owner krcresearch, mode 0600, two key files krcresearch mode 0400, with credential access tested after parent changes. Do not print keys.
- `/opt/krc-consent-test/consent_custody128.py` root:root 0644, SHA256 `bc8ee4406a5628347ab24ef0f91a634394ab691276dea7c0bfe55fb0e3d228af`.
- Synthetic root-owned test grant `synthetic-consent-stage130-001` in `approvals-test`, no real owner approval. Separate test replay DB `/var/lib/krc-research-v2/consent-test/replay.sqlite` owner krcresearch:krc-sentinel-ipc mode 0600. Actual UID988 tests yielded changed payload denied, first use accepted, replay denied, reopen/restart replay denied, wrong principal denied, overall PASS. Synthetic grant is now **consumed**; do not re-use or treat as owner consent.

## Architecture decisions
1. K_Sentinel owns genuine GitHub OIDC RS256/JWKS + actual Tailnet peer/StableID and ACL, durable issuer+jti replay, UID987 transport key, HMAC only. Current v2 ingress remains not deployed; old gateway `:19015` is v1, not E2E v2. Claims mismatch (OIDC sub/full workflow_ref versus KRC K_Science/refs/heads/main) requires tested post-auth projection and contract alignment. Sentinel PR #38 remains Draft.
2. KRC alone holds Science HMAC; no transfer to K_Sentinel or K_Science. Opt-in internal signing candidate `science_signer127.py` + `staging_service123c.py` passes trusted request_id from `ResearchBoundary`; root-owned `consent_custody128.py` grants scope based on request_id,task_id,operation,principal,profile_ref,evidence_refs,payload_sha256 and consent_ref, with independent KRC SQLite one-time consumption. Not live deployed. Issuing a synthetic root-owned grant proves filesystem behavior only, not real human approval. Need audited out-of-band explicit owner-approval issuance before real science.
3. Bibliography metadata policy approved: read-only FREE_ONLY Crossref DOI/updates and Europe PMC; provider coverage caveat and no retraction clearance from absence of updates. `bibliography_bounded129.py` validates batches, throttles callback calls; `metadata_store130.py` adds private SQLite TTL cache and audit, tests 38 PASS. Actual live bibliography `bibliography_fn=None` remains disabled; no scientific evidence certification by metadata.
4. K_Science Draft PR #6: 29 scenario cases NOT_RUN, four unsigned synthetic operation packages; not final v2 wire. No unpublished materials sent. KRC current 4-operation input/output/error schemas are DRAFT, not approved final wire.
5. Production/public sharing/Media remains on pause; no service restarts/changes during this checkpoint.

## Gate matrix
| Gate | State |
|---|---|
| Stage126 service + UID/UDS + health | PASS |
| Transport HMAC positive+tampered negative | PASS subgate only |
| Real v2 ingress GitHub OIDC/Tailscale origin | NOT RUN |
| Root-owned synthetic consent filesystem/replay | PASS synthetic only |
| Independently documented **real owner** consent issuance and signature authorization | NOT DONE |
| Internal science signer isolated unit/UDS tests | PASS candidate only |
| New signer in active service | NOT DEPLOYED |
| Bibliography adapter/cache selected synthetic tests | PASS |
| Real DOI metadata backend with live rate/cache/audit | NOT RUN |
| Bibliographic full-text primary source and scientific evidence acceptance | NOT RUN |
| K_Science E2E-01 complete and E2E-02–05 | NOT RUN |
| Production readiness | NO-GO |

## Next executable plan
1. Finalize admin-only, independently logged human owner-grant issuance procedure, explicit CriticProfile/content digest and narrowly scoped consent, expiry and request/task binding. Negative tests in isolated UID988 runtime. Never silently mint grants on basis of K_Science payload bool.
2. Pin reviewed KRC source SHA and deploy **separate** opt-in disposable staging instance with different UDS path and state dir; avoid replacing active Stage126 process. Test owner-grant lifecycle, negative signatures, restart/rollback with immutable evidence. Keep active staging service unchanged.
3. Finish guarded Sentinel v2 ingress; mandatory durable OIDC replay and fail-closed claims bridge. Tailnet ACL and dedicated v2-only workflow; verify real OIDC provenance without JWT leaks.
4. Explicitly approve DOI-only outbound read-only provider configuration and verify cache/rate/error/audit on actual public DOI; metadata-only outputs never elevated to scientific proof.
5. Finalize machine-readable versioned KRC contract and K_Science PR #6 fixtures. Conduct 29 real E2E cases with precise result/HTTP/status/sha/run IDs, independently review Critic and research evidence. Keep Draft PRs until acceptance.
6. Preserve rollback and compare Stage114/v1/gateway/public MCP invariants after each deployment; production NO-GO unless all gates pass.

## Pointers
- Architecture: `docs/integrations/KRC_STAGE127_SCIENCE_HMAC_CUSTODY_DECISION_2026-10-28.md`
- Science PR6 handoff: `docs/integrations/KRC_STAGE127_KSCIENCE_PR6_SCIENCE_CONTRACT_HANDOFF_2026-10-28.md`
- Stage129 release criteria: `docs/integrations/KRC_STAGE129_OWNER_CONSENT_AND_BIBLIO_RELEASE_GATES_2026-10-28.md`
- PRs: `kolemasakar/Sentinel-Remote#38`, `kolemasakar/K_Science#6`.
