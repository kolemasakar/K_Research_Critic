# MEDIA BETA Decision Log

This file remains the compact decision index. Historical decisions D001-D035 are preserved in Git history and the numbered phase/acceptance records. The current active decision is recorded below.

Version: 3.0
Status: ACTIVE
Updated: 2026-09-16

## Historical decisions

D001-D035 remain accepted/historical exactly as recorded before this update. Their detailed text remains available in Git history and the numbered checkpoints through checkpoint 110.

Key retained policy decisions include:

```text
MEDIA is additive to Core KRC
MEDIA failure must not block Core
users do not provide provider API keys
paid retrieval fallback=false
paid STT fallback=false
paid proxy fallback=false
automatic retry loop=false
free-only routes fail closed
public KRC remains unchanged until a separate owner cutover gate
merge, deployment, publication, migration, and audience expansion are independent gates
```

## D036 - Plugin-First Post-Canary Roadmap Is Approved

Decision: **APPROVED_PLAN / R3-A_READY / IMPLEMENTATION_NOT_STARTED / PUBLICATION_HOLD**
Date: 2026-09-16

The bounded Remote Custom MCP canary sequence is accepted as complete:

```text
repository implementation
-> deployable package
-> isolated Render deployment
-> external MCP protocol validation
-> authenticated owner-account ChatGPT connection
-> exactly one discovered tool
-> one real ChatGPT-side read-only invocation
-> PASS
```

The proven migration candidate remains Remote Custom MCP / Plugin rather than legacy Custom Action expansion.

Target architecture:

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing free-only provider routes + durable state
```

The owner approved the following roadmap sequence:

```text
R3-A contract freeze / secure adapter baseline
R3-B inbound auth + secret-boundary hardening
R3-C 9-tool non-execution VoiceBridge binding
R3-D consequential-action confirmation semantics
R3-E staged four-route execution binding
R3-F full 13-operation parity regression
R3-G private operational hardening
R3-H migration/publication readiness
R4   separate owner-approved cutover/migration/publication
```

The current no-auth one-tool canary is evidence only. It must not receive VoiceBridge credentials or become the production MEDIA endpoint.

R3-A is the only next implementation gate considered ready. R3-A is repository-only and does not authorize deployment, VoiceBridge credentials, provider calls, real execution tools, public GPT changes, Plugin publication/sharing/migration, `main` mutation, PR #22 merge, or VoiceBridge PR #45 merge.

Canonical roadmap authority:

`111_POST_CANARY_PLUGIN_MEDIA_ROADMAP_DECISION_2026_09_16.md`

Current roadmap:

`02_ROADMAP.md` version 5.0

Current recovery authority:

`CURRENT_HANDOFF.md` version 11.0
