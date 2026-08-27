# MEDIA BETA Operations Runbook
Операційна інструкція для owner-only тестування без merge або production promotion.

Version: 2.0
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## 1. Active Boundaries

```text
KRC branch: agent/video-url-research
VoiceBridge branch: agent/krc-media-transcript
private GPT: K-Research & Critic - MEDIA BETA
beta backend: voicebridge-krc-media-beta-kolemasakar
```

Do not target KRC `main` or production VoiceBridge during the hold.

## 2. Accepted Package

```text
Builder instructions: prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
Action schema: gpt_store/actions/media_managed_beta_openapi.yaml
Builder version: 0.9.1-beta-a10
Action version: 0.6.0-a9.10
```

The current package is already applied. Do not re-import it for documentation-only changes.

## 3. Normal Test Procedure

1. Open a NEW chat in the private MEDIA BETA GPT for a clean runtime test.
2. Provide one supported public URL or one local audio/video attachment.
3. Specify the requested mode if needed.
4. Observe source acquisition and any legitimate provider-credit consent gate.
5. Confirm the CriticProfile gate appears only after transcript availability.
6. Approve/review/cancel explicitly.
7. Inspect final claim-level evidence, cross-check counts, SHORTFALL handling, transcript metadata, and copy-safe table.
8. Record only material defects/evidence; never record secrets or full transcripts in project checkpoints.

## 4. Route Expectations

YouTube/Instagram: preflight before billable provider work; no automatic AI spend.

Facebook: free Cobalt success continues; Cobalt failure is unavailable/STOP; no paid offer/fallback.

Telegram: public web/embed route, zero retrieval credits, no account/session/cookies/bot token/paid fallback.

Local attachment: current-conversation file reference only, trusted OpenAI delivery, max 32 MiB, zero retrieval credits, no Helper/file token request.

## 5. Failure Handling

- never fabricate transcript content;
- no blind retry of terminal source failures;
- no automatic retry when `credit_charge_uncertain=true`;
- report unavailable when the accepted adapter cannot obtain usable media/transcript;
- keep failures isolated from public text Core.

## 6. Defect Workflow

```text
reproduce
 -> classify owner: KRC package | VoiceBridge | provider/source | ChatGPT UI
 -> fix only on owning feature branch
 -> add regression test where practical
 -> full relevant CI
 -> live private retest when runtime behavior changed
 -> update current-state/audit evidence
```

## 7. A10 Copy Check

The normal rendered claim table may copy incorrectly because of the ChatGPT UI. The fenced copy-safe duplicate must remain correct and must match the rendered values. If the fenced duplicate fails, reopen A10 regression work; if only the known rendered-header Copy defect persists, keep A10 accepted.

## 8. Rollback

If a new Builder package breaks private runtime, restore the last accepted package and diagnose on the feature branch. Do not use production deployment or a `main` merge as rollback.

## 9. Release Hold

All release gates remain HOLD until explicit owner authorization:
- merge;
- production promotion;
- external testers;
- public rollout.

## 10. Recovery Order

```text
00_INDEX.md
03_CURRENT_STATE.md
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
02_ROADMAP.md
06_DECISION_LOG.md
05_TEST_PLAN.md
```

Then verify live KRC/VoiceBridge heads and PR states before writing.
