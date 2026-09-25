# Checkpoint 224 — Existing private Plugin late-return audit (2026-09-25)

Scope: read-only review; no Plugin release update, no MEDIA start/provider work, no production deploy.

## Verified private Plugin
- Owner's private USER-scope Plugin ID: plugin_bb3595f295708191a3f9e145ba1ff2d5; current version 0.19.6+portable.20260924.
- Current SKILL already routes YouTube to Gemini Free direct, Instagram to Cobalt + AssemblyAI, Facebook to Cobalt + ffmpeg + AssemblyAI, and Telegram to public web + AssemblyAI. All nine R3C read-only operations and four separate execution tools are named.
- YouTube already requires preflight then lookup, reuse COMPLETED/PROCESSING, fresh consent before new provider work, and no automatic retry. Do not recreate these capabilities.
- Gaps: no explicit late-return user-facing branch after missing/expired transcript; no explicit mandatory read-all-pages / integrity checks / active-chat delivery instruction. For non-YouTube, existing SKILL lists lookup/status/segments but does not fully specify the equivalent late-return policy.

## Proposed minimal SKILL-only extension (NOT applied to Plugin)
After the existing YouTube and platform routing text, add:

LATE RETURN / TEMPORARY MEDIA RESULT
When the user returns to a chat, first use the existing platform's read-only lookup/status, and if COMPLETED fetch all available transcript pages using the existing segments operation until next_cursor is null. Check job identity, page order, segment indexes, segment_count, and transcript_characters when compatible with the server's exact counting semantics. Do not claim a full original transcript unless verification succeeds. Present the verified complete transcript to the active chat, using a temporary chat attachment for large texts; do not permanently archive without a separate explicit user request.
If an earlier job/transcript is unavailable, distinguish expired temporary retention from other possible lookup/status failures as far as read-only evidence allows. Tell the user the earlier result is unavailable and offer to process the original video again. Never start or retry automatically. Require fresh explicit consent according to the existing platform execution contract, including the returned Gemini Free data-use notice for YouTube, before any new provider work. Reuse the existing four platform pipelines. HTTP 404 alone does not prove expiration; infrastructure HTTP 429 is retryable and does not authorize reprocessing.

## Runtime audit limitation
Attempted only R3C media_get_capabilities, which returned infrastructure HTTP 429 retryable=true. Did not call other MEDIA operations or *_start. This is not evidence that all four routes are down.

## VoiceBridge candidate status
Existing VoiceBridge pagination confirmed. Candidate code commit dabed98 preserves exact chunk boundary text; full isolated suite 279/279 PASS. Production remains on previous branch with health TTL 3600 seconds; candidate TTL 21600 seconds is not deployed.

## Next gate
Review the minimal Plugin SKILL extension, verify current connector access after rate limiting, and obtain separate explicit authorization before updating the owned private Plugin release. Preserve current mappings, visibility, all other skill content and public GPT.
