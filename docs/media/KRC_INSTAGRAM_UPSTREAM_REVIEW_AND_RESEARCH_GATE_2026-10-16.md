# KRC Instagram upstream/research gate — 2026-10-16

## Handoff
K_Sentinel access work COMPLETE. KRC owns adapter research. Production changes NOT AUTHORIZED. FREE_ONLY, public HOLD, Telegram LIVE BLOCKED. No cookies/credentials added.

## Production identity and upstream comparison
Earlier authorized local API reported version 11.7.1, commit a636575b09de1fc55d9b8cd98cac88f5f2f16b42. Fresh git ls-remote upstream HEAD equals that commit. Local exact baseline Instagram adapter therefore equals current upstream main. Exact production container image reference and immutable digest are not exposed by current summary helper and remain NOT VERIFIED; API-reported git commit is not an image digest or on-disk adapter hash.

## Upstream candidates reviewed
- https://github.com/imputnet/cobalt/pull/1554 : OPEN/unmerged, head 27a1089e1f5d2c7f6a3cea4b1aa4750ed1f129a3. GraphQL before embed; motivation incomplete video data in carousel embed. Does not prove resolution of this host's anonymous retrieval failure.
- https://github.com/imputnet/cobalt/pull/1577 : OPEN/unmerged, head 4355a7a4fa7e9354f530230bd72861c0eccee960, updated2026-10-14. Same adapter reorder plus unrelated Railway Dockerfile changes. Do not adopt unrelated infrastructure changes.
- https://github.com/imputnet/cobalt/pull/1241 : CLOSED/unmerged. Contains stage catches but also media.title access without guarding media. Not accepted wholesale.
- https://github.com/imputnet/cobalt/issues/1587 : carousel returned as JPEG on current image; relevant output-type regression risk.
- https://github.com/imputnet/cobalt/issues/1509 : zero-byte Instagram downloads; a different symptom, no proof of our cause.
- https://github.com/imputnet/cobalt/issues/1579 : business-account stories fail with configured cookies; different endpoint/scope, not a fix for public reels.

## Research tests
Exact baseline and local candidate tested via actual adapter source with mocked fetch and dependency boundaries, no network/STT. 10/10 PASS, syntax/diff checks PASS. Coverage: mobile success skips later stages; no media_id skips mobile; valid embed success; missing initializer; empty context; mobile transport failure; oEmbed exception; malformed context; all-stage failure; GraphQL no-data. Comparative test proves order-only PR approach suppresses embed fallback if GraphQL throws. Local per-stage recovery passes these cases. This is NOT a full upstream test suite or live retrieval acceptance. Local candidate has only prior anonymous host probe, which still failed; no guaranteed recovery claim.

## Corrected helper prepared, not installed
scripts/diagnostics/cobalt_instagram_stage_v2_20261016.cjs: numeric HTTP status, follow redirects, extracted/synthetic LSD distinction, 24s total budget, <=4s request/body budget, <=2MiB response. Fixed source and existing output sanitation retained. Not exact live-handler tracing: independent diagnostic stages remain approximations. Mock check PASS for numeric statuses, redirect option, synthetic LSD, no private sentinel, five requests when mobile skipped. Host syntax check PASS.

Remote candidate /tmp/krc-cobalt-instagram-stage-v2.js SHA256 452b97842180a5537319485704eee0f4b3b436f017110e5972eccc22ba29b970 matches tested local copy. /tmp/install-krc-stage-helper-v2.py verifies hash and root-owned target, makes backup and atomically installs root:root0644 helper only. Not executed: current KRC channel cannot perform administrative writes. No systemd rights broadened. Existing helper remains live until operator runs installer.

## Rollout plan and gates
1. Administrator may install diagnostic helper v2 via existing channel: sudo python3 /tmp/install-krc-stage-helper-v2.py. This is helper maintenance, not production adapter rollout.
2. KRC runs one approved systemd instagram diagnostic, verifies result freshness and exact statuses. Obtain exact image/digest and adapter file hash via similarly bounded approved metadata output before production candidate selection.
3. Retain upstream-order candidate and local fallback candidate separately; expand mixed/carousel/photo and media-type regression tests before adapter admission. Nonempty video/audio validation required before STT.
4. Research live candidate must demonstrate usable audio asset on fixed known short public reel without STT, preserving no-cookie scope. Current tests do not clear this gate.
5. Only after separate owner production authorization: pin candidate image/digest, preserve old deployment and config, one bounded rollout and health/read-only checks, then one explicitly authorized short end-to-end test. Roll back to recorded previous image if regression; no automated provider retries.

Current gate: research candidate PARTIAL, live retrieval FAIL, production adapter unchanged. Do not interpret wrapper-observed manual-redirect chain as a literal production handler trace.
