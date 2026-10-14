# KRC R4 Limited Private — Plugin Creator creation and post-create read-only acceptance
Date: 2026-10-14. Owner supplied archive through the chat, authorized continuation. **PRIVATE ONLY; global public release HOLD.**

## Input and archive integrity
- Chat-attached archive `krc_r4_limited_private_20261014.zip` had 5621 bytes and SHA-256 `2dc1e71be561912a29df52df063b333fdf2fb8bf45c9cbad3764a217b60828d8`, exact previously frozen krc-cobalt package hash.
- ZIP entries: `plugin.json`, `.app.json`, `.codex-plugin/plugin.json`, `skills/krc-core/SKILL.md`. All JSON files parsed. Exactly four registered apps; Telegram omitted.

## Official private plugin creation
- `Plugin_Creator.create_plugin` accepted the attached host-side archive successfully.
- Returned **status=created**, name `k-research-critic-r4-limited-private`, version `0.1.0`, plugin_id `plugins_6acef8a60d708191bf37778f71e4562d`, release_id `pluginrel_6acef8a752448191babda35a0bd39cd2`, `scope=USER`, `discoverability=PRIVATE`.
- Private URL: `https://chatgpt.com/plugins/plugins_6acef8a60d708191bf37778f71e4562d`.
- Plugin Creator metadata and file inspection independently confirmed four files and exactly these mappings:
  - R3C `krc-media-readonly`;
  - E1 `krc-youtube`;
  - E2 `krc-instagram`;
  - E3 `krc-facebook`.
- E4 Telegram mapping is **absent from this package**. Its separate legacy connector may still exist globally; package exclusion is not a global uninstallation.
- Core Skill and plugin.json content readable through Plugin Creator. No update to the earlier five-app candidate, no public/unlisted publication.

## R3C post-create read-only backend smoke
- The R3C connector `media_get_capabilities` returned request `09fc5400-9b71-49ac-bfa2-2ef2f8b94d24`, configured true, postgres durable, restart-resilient, duplicate-start reuse, automatic_paid_fallback=false, paid retrieval fallback=false, paid STT fallback=false.
- The backend still advertises platforms YouTube, Instagram, Facebook, Telegram, which is **backend capability, not package app mapping**. The package does not expose Telegram.
- The current capabilities response reports `youtube_gemini_model=gemini-3.8-flash`, in contrast to a previously recorded `gemini-3.7-flash`. This is observed configuration drift; a separate exact backend/environment audit is required before attributing its cause or certifying E1 provider starts. No YouTube POST was executed.
- Caveat: this smoke used the already connected R3C connector, not an invocation selected from the new plugin's UI session. **New plugin UI binding/selection smoke remains OPEN** until the user opens the private plugin in a new conversation.

## Acceptance
- Archive integrity = PASS.
- Plugin Creator PRIVATE creation = PASS.
- Release metadata and 4 app mappings = PASS.
- Telegram excluded from limited plugin = PASS.
- R3C existing backend read-only = PASS.
- New-plugin UI selected R3C smoke = NOT TESTED.
- E1 model drift explanation = OPEN.
- Overall public KRC R4 release = HOLD. Preserve FREE_ONLY, no paid fallback, no Telegram LIVE, no new long Instagram/Facebook provider starts.
