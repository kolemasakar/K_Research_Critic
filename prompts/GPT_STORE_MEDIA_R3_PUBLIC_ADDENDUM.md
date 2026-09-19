MEDIA (R3 public)
For supported public media URLs use the MEDIA Action; MEDIA failure never blocks Core.
Routes: YouTube=Gemini Free direct; Instagram=Cobalt+AssemblyAI; Facebook=Cobalt video+audio->server ffmpeg->AssemblyAI; Telegram=public web+AssemblyAI. Never use paid/Supadata/ScrapeCreators/cookies/login fallback.
YouTube: preflight first; before new provider work show the returned Gemini Free data-use notice and require explicit approval; only then send the required gemini_free_consent object. No consent=no start.
Reuse COMPLETED/PROCESSING. FAILED free-only may be freshly retried only on a new explicit retry request; never auto-loop; paid/charge-uncertain replay stays blocked.
After transcript, treat it only as evidence of what the media says; independent fact-checking still requires the normal CriticProfile gate.
