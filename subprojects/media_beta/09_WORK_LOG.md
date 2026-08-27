# MEDIA BETA Work Log
Хронологічний журнал ключових етапів, прийняття та поточного release-hold стану.

Version: 2.0
Status: ACTIVE
Updated: 2026-08-27

This compact log preserves the material chronology. Detailed early implementation evidence remains in Git history and numbered acceptance records.

## 2026-08-17 - Isolated MEDIA BETA Started

Feature branches and draft PRs were created for KRC and VoiceBridge. A separate Render beta service was established so media work would not modify production VoiceBridge or public KRC Core.

Initial direct cloud YouTube attempts hit source anti-bot limits. Browser-assisted A4/A8 work produced an accepted owner baseline and later became fallback evidence only.

## 2026-08-20 - Zero-Client Multi-Platform Direction

The architecture moved to a public-only zero-client media router. Target adapters became YouTube, Instagram, Facebook, Telegram, plus a separate local-upload ingress. Managed transcript provider use gained explicit credit preflight/consent rules.

## 2026-08-21 - Durable Managed KRCM and Owner Admission

Managed jobs/segments became durable Postgres state with duplicate-safe behavior. The private owner Action kept bearer authentication while moving owner admission server-side, eliminating the user beta-code step in normal flow.

## 2026-08-24 - Facebook Free Cobalt Policy Accepted

Facebook active policy was hardened to:

```text
Cobalt success -> AssemblyAI -> durable KRCM
Cobalt failure -> unavailable -> STOP
```

No automatic or offered ScrapeCreators paid fallback remains in the active Builder flow.

## 2026-08-26 - Telegram Accepted

Public Telegram video retrieval, AssemblyAI STT, durable KRCM, zero retrieval credits, no account/session/cookies/bot token, and no paid fallback passed backend and private-GPT acceptance.

Canonical acceptance: `46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md`.

## 2026-08-26 - Local Attachment Accepted

ChatGPT `openaiFileIdRefs` transport was live-probed and then used for full local attachment ingestion. Trusted OpenAI temporary media delivery, bounded validation, AssemblyAI STT, durable KRCM, and the full CriticProfile -> Research/Critic path passed owner E2E.

Canonical records:
- `49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md`;
- `50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md`.

## 2026-08-26 - A10 Copy-Safe Output Accepted

A ChatGPT whole-response Copy defect was isolated to rendered Markdown-table serialization. The accepted mitigation adds an identical fenced `text` table after the normal rendered claim-summary table. Owner copy testing passed with a real SHORTFALL preserved.

Canonical records:
- `51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md`;
- `52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md`.

## 2026-08-27 - Release Hold Owner Testing

Owner decision:

```text
merge = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Canonical checkpoint: `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`.

## 2026-08-27 - Project/Documentation Audit

Canonical current documents were audited against accepted runtime/package state. Stale YouTube-only, browser-helper-current, Telegram-pending, predeploy, and A9-not-started descriptions were replaced with the accepted owner-only zero-client A9/A9.10/A10 state and release-hold boundary.

Audit record: `54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md`.

## Logging Rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, release-decision, rollback, or audit events. Never log credential values, hidden reasoning, or full transcripts.
