# KRC R4 read-only 401 root cause and E2 exact-branch patch acceptance
Date 2026-10-14. Scope: R4 private composite read-only test follow-up; **no provider work, no MEDIA start, no production deployment**.

## Root cause analysis of two 401 classes
1. **E1 Instagram preflight/lookup HTTP 401:** R3-E1 imports the nine R3C read descriptors including Instagram methods, but calls use E1 YouTube credential. VoiceBridge Cobalt media handler authorizes `mediaActionToken`, R39 unified token and R3E2 Instagram token, not E1 YouTube token. This explains observed 401 as enforced credential separation, not an invalid app install. Do **not** elevate E1 credential to gain Instagram scope. Follow-up design: either present per-surface scoped capabilities accurately or stop advertising unsupported cross-scope read tools; requires separate compatibility review because R3-E1 currently contractually advertises nine read tools.
2. **E2 non-YouTube status HTTP 401 for syntactically valid nonexistent KRCM ID:** VoiceBridge `public_cobalt_media.ts` handles E2 scoped token but returns `false` when scoped job is absent, allowing a generic managed handler to pick up the same URL. Generic handler does not authorize the E2 token and emits 401. This is an incorrect fallback result for an absent job, not evidence of revoked E2 credentials.

## Minimal E2 correction committed
Branch `kolemasakar/VoiceBridge:agent/krc-media-gemini-migration`.
- Code commit `069126dc6cc87dac17daa4cfd63aca595849c52c`, `src/cloud/src/public_cobalt_media.ts`: when `r3e2_instagram` scope calls status/segments for missing job, return `MEDIA_TRANSCRIPT_NOT_FOUND` HTTP 404 instead of yielding handler control. All other scopes retain previous delegation/fallthrough, and successful E2 read path is untouched.
- Regression commit `cb0cbf250a60ba42b75fc4e55f8424b0fcfe1ad7`, `src/cloud/tests/public_cobalt_media.test.ts`: two nonexistent-job GETs, E2 bearer scoped, assert 404 and exact error code, no downstream generic handler, no retriever or STT calls; general auth still delegates as before.

## Tests and exact SHA
- Isolated prior checkout build PASS, targeted 9/9 PASS, full suite 272/272 PASS, but this is a **separate older checkout**, NOT the exact target HEAD.
- Fetched exact current VoiceBridge branch commit `cb0cbf250a60ba42b75fc4e55f8424b0fcfe1ad7` into independent detached worktree `/tmp/krc_e2_patched_exact_20261014`, built `src/cloud` TypeScript successfully.
- Targeted native Cobalt tests: **9/9 PASS**, zero failures.
- Full exact HEAD `npm test`: **280/280 PASS**, 0 fail, 0 skip, exit 0; duration 87261 ms; output `/tmp/krc_e2_exact_full_20261014.log`. These tests invoke local mock retriever/STT, not external providers.

## Authorization/security consequences
- No token values modified or disclosed.
- No broadening of E1 or E2 token scope.
- No access to another app's jobs added.
- Zero paid provider activity; Telegram E4 LIVE still BLOCKED.
- Previously observed expired job 404 and malformed job ID -32602 are separate conditions from scoped 401.

## Pending
- **Deployment to Render is NOT authorized/NOT EXECUTED by this engineering test.** Previous live service SHA may differ from current VoiceBridge branch HEAD.
- For live acceptance, obtain owner authorization for controlled deploy of exact `cb0cbf25`, verify Render commit after rollout, retry **read-only** E2 status/segments with a well-formed nonexistent KRCM ID and expect 404; run R3C capabilities/one E2 preflight, check paid fallback off.
- E1 advertised cross-route read tools still need a separate design decision; do not 'fix' by weakening credentials.
- Real retained job status/segments read through new composite R4 after new deploy remains separate from missing-ID regression; do not create media jobs solely to force this gate without consent.

Overall R4 private composite **PARTIAL** and public release **HOLD**.
