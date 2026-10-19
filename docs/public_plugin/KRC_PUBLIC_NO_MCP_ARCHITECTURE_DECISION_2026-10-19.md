# KRC Public — Owner-approved NO_MCP architecture decision
Date: 2026-10-19
Status: APPROVED by owner (option 1).

## Decision
- Remove self-hosted MCP as a mandatory dependency of K-Research & Critic public offering.
- Primary implementation: ChatGPT-native KRC instructions, CriticProfile, research methodology and Core Skill where plan eligibility and sharing permit it.
- Seek one-time setup or connection inside ChatGPT for other Plus users; independently verify current Plus distribution/install eligibility before any public availability claim.
- Optional external HTTPS API/Actions only for capabilities demonstrably unavailable natively; it is not part of baseline.
- Keep existing MCP source code, offline tests, operational reports, and deployment manifests as an archival fallback, not the public release path.
- Preserve Cobalt MEDIA and production services unchanged; no new public MCP exposure, endurance tests, load tests, or server modifications as part of this architecture decision.
- FIFO server queue, guest capabilities, SQLite retention and disk quota are no longer baseline requirements unless optional server work is separately reapproved.

## Delivery plan
1. Audit and synchronize Core Skill with agreed CriticProfile and evidence/report methodology.
2. Verify existing KRC GPT/plugin editing, sharing, installation, and access for a separate Plus user without external MCP.
3. Choose compatible distribution: existing shared GPT or supported Plugin Directory package; do not assume a personal private plugin is publicly installable.
4. Run functional research and safety tests via the actual recipient-side ChatGPT interface.
5. Publish only once distribution and permissions are verified.

This document records a product decision, not a claim that a new public Plus access channel is already available.
