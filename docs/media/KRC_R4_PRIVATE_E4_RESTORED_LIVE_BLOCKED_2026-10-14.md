# KRC R4 Private — E4 mapping restored with LIVE BLOCKED guard (2026-10-14)

## Owner decision
Owner approved option 1 to **restore the Telegram E4 registered app mapping** into the existing *private* R4 plugin, without changing the operational **Telegram LIVE BLOCKED** policy. Prior exclusion had incorrectly conflated connector integration with permission for live processing.

## Changes actually executed
- Read existing private plugin `plugins_6acef8a60d708191bf37778f71e4562d`, release `pluginrel_6acef8a752448191babda35a0bd39cd2`, previously version 0.1.0 and four app mappings.
- Created replacement version 0.1.1 archive locally: `krc_r4_private_e4_guarded_20261014.zip`; SHA-256 `7438a6f420622f3c0369fc4c40783b09f1af1bff75a6d4c69d96671fa459dab2`.
- Included all five registered apps under `.app.json`:
  - R3C read-only `asdk_app_6aaaf8ca113c8191a4ac53f8793833a4`
  - E1 YouTube `asdk_app_6ab26b061fb4819180fa096638f1e4df`
  - E2 Instagram `asdk_app_6aaeae197c9081918b90e46f5bb09615`
  - E3 Facebook `asdk_app_6aaf262767d8819199146dc84b8e1ee8`
  - **E4 Telegram** `asdk_app_6aaf292e653481918c75767dea004c5c`
- Both V1 and V2 manifest prompts explicitly say Telegram registered for read-only capabilities, status and segments, **never call `media_telegram_start`** pending separate owner approval. Also preserve FREE_ONLY, consent for Gemini Free, no paid fallback, no blind consequential replay.
- Core Skill snapshot copied byte-identically from previous package, not rewritten.
- `Plugin_Creator.update_plugin` returned **status=updated**, `version=0.1.1`, release `pluginrel_6acefb01efc08191a91d448928c57e47`, scope `USER`, discoverability `PRIVATE`.
- Post-update `get_plugin_files` independently confirmed **all five mappings**, E4 exact ID, version parity between manifests and matching `LIVE BLOCKED` prompt.
- URL unchanged: `https://chatgpt.com/plugins/plugins_6acef8a60d708191bf37778f71e4562d`.
- Original historical five-app R4 candidate, connected provider integrations, Render deployment, public main and public GPT not changed.

## Important technical limit
The instruction `NEVER call media_telegram_start` in the package prompt is an **instruction-level gate**, not a provider-enforced access-control or server-side kill switch. Because E4 connector exports `media_telegram_start`, **full technical prevention of Telegram LIVE has not been demonstrated**. Before lifting the global HOLD or treating E4 as safe for unrestricted users, implement and verify a server-side action denial/permission restriction. Until then do not use E4 consequential operation; no E4 live test was performed.

## Acceptance
- Five-app PRIVATE registration: **PASS**.
- E4 diagnostic/read-only capability in app mapping: **PRESENT**, UI invocation via newly updated plugin needs a separate new-chat test.
- E4 LIVE: **BLOCKED BY POLICY**, no actual provider request performed; not a hardened server-side technical block.
- Full R4 public release: **HOLD**.
