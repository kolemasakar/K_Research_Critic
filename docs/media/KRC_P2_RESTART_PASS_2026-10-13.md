# P2 completed Instagram job — post-restart PASS

Render VoiceBridge lifecycle on 2026-10-13 UTC: service_stopping 20:48:37.170, service_started 21:00:13.746.

Before and after stop/start, R3C and connected Neon returned same job identity KRCM_0b6d30b2-5cad-4a7c-9410-593d990e8263, status COMPLETED, 1 segment, 331 characters, timecodes 720–34780 ms, 42 charged STT seconds and 0 credits. Post-restart status request aa07dc55-a4ea-4f02-a85e-2677fb115612. Post-restart Neon check 21:05:51 UTC. Expiry 21:32:53 UTC, so verified before TTL.

PASS: durability of a completed Instagram reel job across actual Render sleep/wake. Not tested: recovery while PROCESSING, abnormal crash, Facebook replay, provider lost response, TTL purge timing. No new media start or deployment. FREE_ONLY and R4 acceptance HOLD.