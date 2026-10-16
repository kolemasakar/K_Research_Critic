# KRC Public MCP — owner decisions, 2026-10-16

Status: APPROVED_POLICY / IMPLEMENTATION_PENDING.

- No separate user registration or KRC login. ChatGPT users are already signed into ChatGPT, but MCP must not assume ChatGPT passes a verified per-user identity.
- Use an opaque short-lived per-job capability to prevent cross-user access to temporary documents/results. It is not a separate sign-in. Do not use guessable sequential job IDs as access credentials. Never log or disclose capabilities to other sessions.
- Delivered results and related temporary materials: purge 10 hours after confirmed delivery.
- Undelivered results: purge 10 hours after job completion.
- Uploads with no completed jobs require a bounded cleanup policy; proposed 10 hours from upload, subject to protection for actively queued/running jobs.
- Eligible oldest completed document can be displaced when storage capacity requires; never evict queued/running documents silently.
- Keep >=10% of filesystem capacity available. Before accepting new payloads, apply conservative admission accounting for payload size, queued reservations, and filesystem usage. When unable to keep reserve, pause new uploads with explicit error; do not claim unlimited queuing.
- Implement and retest before deploy; existing prototype 24h undelivered retention does not satisfy this policy.
- KRC Cobalt primary, KGM reserved for KGM, K-Trader excluded. No production deployment authorized by this policy note.
