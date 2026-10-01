# E2 diagnostics deployed: read-only acceptance

Date: 2026-10-01. Existing Render E2 `srv-dan7vsijnfac73fmrtl0` deployment `dep-davajuvlk1mc739an6mg` reached **live** at 18:44:52 UTC with commit `c3147f2ed8daf2eb52114c6fadccf6f3dd1f6e1f`. Previous deployment deactivated. Owner explicitly approved deployment. No environment/credential changes, no real media provider work.

After live, executed **two** read-only `media_instagram_preflight` calls through connected R3E2 app for `https://www.instagram.com/reel/Dcea3BiPTBm/`. Both returned success with `can_continue=true`, `provider=cobalt`, `stt_provider=assemblyai`, `automatic_paid_fallback=false`, `estimated_retrieval_credits=0`, `consent_required=false`. Request IDs: `fcb4315b-81d2-4fc6-ad25-d811e52bf546`, `fb75bc47-bb9a-43ce-a06e-6b46a2ba7819`.

HTTP 429 did not reproduce during these two checks, so the precise earlier 429 origin remains unverified. These read-only checks do NOT verify a live Instagram provider start, STT quota, Neon persistence, or full E2E success. Probe-only mode and automatic paid fallback were not changed.
