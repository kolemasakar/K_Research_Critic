# KRC R4 Limited Private — archive verification and Plugin Creator handoff

Date: 2026-10-14. Owner ordered continuation. This note records what was actually performed, without claiming plugin creation.

## Archive verified on authorized krc-cobalt
- Path: `/tmp/krc_r4_limited_private_20261014.zip`
- Length: 5621 bytes.
- SHA-256: `2dc1e71be561912a29df52df063b333fdf2fb8bf45c9cbad3764a217b60828d8`.
- Entries: `plugin.json`, `.app.json`, `.codex-plugin/plugin.json`, `skills/krc-core/SKILL.md`.
- Parsed all JSON manifests; matching manifest names, correct relative apps/skill pointers.
- Exactly four registered apps: R3C `asdk_app_6aaaf8ca113c8191a4ac53f8793833a4`, E1 `asdk_app_6ab26b061fb4819180fa096638f1e4df`, E2 `asdk_app_6aaeae197c9081918b90e46f5bb09615`, E3 `asdk_app_6aaf262767d8819199146dc84b8e1ee8`. **No E4 Telegram mapping.**
- Core Skill exact content SHA-256 `9b154eb926195743d9d0e710f2a884ed04528994bc5ccf863af6f3e17074747b`. Snapshot markers present.
- Validation status: **LOCAL STRUCTURE PASS**, not official Plugin Creator schema acceptance.

## Installation dependency
- Attempted `Plugin_Creator.create_plugin(archive='/tmp/krc_r4_limited_private_20261014.zip')`; host rejected it with `UNREGISTERED_FILE_REFERENCE` because archive path belongs to remote krc-cobalt rather than upload-capable ChatGPT host.
- No private plugin was created or updated by that attempt; no public listing and no existing plugin mutation.
- Need an upload-capable local copy/attachment of this exact ZIP to pass to Plugin Creator. Verify hash after materializing/uploading, then invoke **create_plugin** (PRIVATE) once, inspect result and run only an R3C read-only smoke; no E4 or provider work.
- Do not bypass the archive control by fabricating a sandbox path or interpreting a remote machine path as host-local.

## Release constraints
PRIVATE ONLY, FREE_ONLY, no paid fallback, E2/E3 short reels/posts, E1 explicit Gemini Free consent, Telegram LIVE blocked, original R4 5-app package preserved. Public R4/HOLD unchanged.
