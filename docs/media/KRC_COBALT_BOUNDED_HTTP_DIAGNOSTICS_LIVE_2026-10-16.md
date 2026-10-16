# KRC — Cobalt bounded HTTP diagnostics deployment, 2026-10-16

## Confirmed facts
- Instagram FREE_ONLY Cobalt retrieval failed on two different reels `Dcea3BiPTBm` and `DF1CIrPSVmf`. Real persisted E2 job status and segments reads worked (FAILED with empty segments); successful transcript is not demonstrated by these checks.
- On authorized krc-cobalt machine, remote operator user `krcops` has UID 1002 and is not a member of `docker`; `/var/run/docker.sock` is root:docker mode 660 and `/opt/krc-cobalt` is ubuntu:ubuntu mode 700. Read-only Docker logs and configuration are inaccessible via this identity; no escalation, credential access, or privilege changes were attempted.
- Earlier Cobalt local and HTTPS GET status returned HTTP 200, version 11.7.1, Instagram advertised. Deliberately unauthenticated POST reported `error.api.auth.key.missing`, which does NOT demonstrate the authorized VoiceBridge request has a missing key.

## Bounded observable failure enhancement
On repo `kolemasakar/VoiceBridge`, integration branch `agent/krc-media-gemini-migration`:
- Code commit `07b00879b6b3145b89f05faa81efbf14b2115edf` extends safe error categories for Cobalt upstream HTTP 400, 404, 422, 429 and 5xx, retaining existing allowlisted authentication categories. No raw upstream response, tokens, URLs or provider error messages are forwarded.
- Tests commit `5cc92812ec93457d9aaf2723155ad8fbf4eef3ef`; follow-up expectation alignment `befff428d70c9ac65226dc2fb2754bb88b6a1ba4`.
- Exact HEAD `befff428d70c9ac65226dc2fb2754bb88b6a1ba4` compiled successfully; Cobalt targeted suite **11/11 PASS**, full VoiceBridge suite **282/282 PASS**, exit 0; no skips/fails.
- GitHub comparison with previous deployed VoiceBridge `38a30cac8e33194cefba04ea2771e91c99531f17`: ahead 3, behind 0; only `src/cloud/src/public_cobalt_media.ts` and its test file changed.

## Render production deployment
- Service `srv-da1kic5bedkc73d6fk60`, existing free plan, autodeploy off.
- Deploy `dep-db8ufh6i0phs7392g1i0`, exact commit `befff428d70c9ac65226dc2fb2754bb88b6a1ba4` finished `2026-10-16T09:02:05.705632Z`, **live**.
- Post-deploy R3C `media_get_capabilities` PASS, request `87a43c93-58f8-401c-96d2-19539bee56dc`: configured=true, durable_store=postgres, paid_retrieval_fallback=false, paid_stt_fallback=false.
- No new Instagram/YouTube/Facebook/Telegram MEDIA start was performed in this session; diagnostic remains unexercised against an actual newly authorized upstream Cobalt failure.

## Gate / next action
Need one authorized free-only short Instagram job **only after** finding a distinct suitable URL and confirming preflight, no pre-existing durable job, zero paid fallbacks, and meaningful service readiness; read the sanitized resulting category to distinguish HTTP status cases without broad Docker access. Do not bypass deduplication or repeat an uncertain start. Alternatively owner can provide narrow root/Docker read-only diagnostic or pre-sanitized logs. E4 Telegram LIVE blocked; R4 public release HOLD. Exact retrieval cause **not yet known**.
