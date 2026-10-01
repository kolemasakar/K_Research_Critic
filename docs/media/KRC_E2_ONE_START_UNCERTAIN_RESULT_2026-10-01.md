# KRC E2 one-start attempt and verified rollback — 2026-10-01

## Authorized scope
Owner approved temporary switch of existing Instagram E2 (`srv-dan7vsijnfac73fmrtl0`) to real processing and **one** free-only Instagram start on `https://www.instagram.com/reel/Dcea3BiPTBm/`, then return to probe mode.

## Actual execution
1. Render environment merged `KRC_R3E2_CONFIRMATION_PROBE_ONLY=false`; deploy `dep-dav94pp42hec7385v18g` became `live` at 17:04:14 UTC. Existing secrets and other variables were not replaced.
2. One `media_instagram_start` tool invocation was made, but the tool result was not available in the accessible conversation log. **Do not assert job created, provider work occurred, or zero cost. Do not blindly repeat start.**
3. Subsequent read-only Instagram lookup and R3C capabilities returned nested `voicebridge_http_error` HTTP 429 (retryable), consistent with earlier cold-start-correlated failures.
4. For safety, Render env merged `KRC_R3E2_CONFIRMATION_PROBE_ONLY=true`; rollback deploy `dep-dav9em1srm7s73eeh1gg` became `live` at 17:25:16 UTC.
5. Canonical VoiceBridge health warmed and returned HTTP 200. Read-only Instagram lookup for the URL then returned HTTP 404 nonretryable; no matching durable job was found through this lookup, but absence of a returned job does not conclusively prove the attempted start had no external side effects.
6. Existing E2 `/healthz` independently verified `status:ok`, `confirmation_probe_only:true`, `voicebridge_binding_configured:true` after rollback. No second start issued.

## Verdict
- Existing E2 rollback: **PASS**, independently verified.
- Instagram real E2E: **INCONCLUSIVE / NOT ACCEPTED**; no job ID, terminal state, segments, or billing delta verified.
- Provider cost: **UNKNOWN**; compare AssemblyAI usage/balance after attempt before considering another start.
- Unused extra isolated service `srv-dav8r9ou01pc738ro880`: still exists. Owner requested deletion **after verification**; since real E2E remains inconclusive, do not yet claim acceptance or deletion. Connected Render tool exposes no delete-service operation.

## Next steps
Check AssemblyAI spend delta, inspect canonical VoiceBridge application/provider logs or durable job records using supported read-only access, diagnose nested 429 at startup. Any new real start requires a fresh, explicit decision after reviewing these observations; do not automatically retry. Delete extra service through Render UI after agreed verification gate.
