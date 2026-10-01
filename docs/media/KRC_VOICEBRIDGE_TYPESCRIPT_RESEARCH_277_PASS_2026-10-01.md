# VoiceBridge isolated TypeScript peer diagnostics — validated research checkpoint

Date: 2026-10-01. Companion repository `kolemasakar/VoiceBridge`, branch `research/krc-peer-observation-isolated`, checkpoint commit `0ea6e5662c479d35dc97158c83b330cba885f268`. This branch was based on deployed VoiceBridge SHA `d3873bf13e60c4932ab08cae449c924051be4a37` and contains only research-only peer observation module/tests and checkpoint; no live server import or rate-limiter change.

On `krc-cobalt` authorized isolated checkout, Node v24.21.0: `npm ci --ignore-scripts --no-audit --no-fund` PASS, `npm run build` PASS, focused peer observation 7/7 PASS, full `npm run check` **277/277 PASS**, 0 failed, exit 0 (87.52s test runtime). The earlier partial full-suite output was superseded by final success.

Remaining security/design gaps: TypeScript prototype validates but does not canonicalize equivalent textual IPv6 addresses, unlike the earlier Python prototype; no raw IP/header/key returned but per-period HMAC tags remain linkable. Render proxy chain and actual 429 root cause remain unverified. Do not deploy without separate owner approval and review of privacy, normalization, bounded retention and server integration tests.

Authoritative companion checkpoint: https://github.com/kolemasakar/VoiceBridge/blob/research/krc-peer-observation-isolated/docs/KRC_PEER_OBSERVATION_RESEARCH_CHECKPOINT_2026-10-01.md
