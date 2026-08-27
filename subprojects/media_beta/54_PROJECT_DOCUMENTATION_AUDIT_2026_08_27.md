# MEDIA BETA Project and Documentation Audit - 2026-08-27
Аудит узгодженості проекту, документації та release-hold стану після прийняття A9-A10.

Version: 1.0
Status: AUDIT_APPLIED
Date: 2026-08-27

## Scope

Audited the KRC media feature branch, current media package/Action contract, current-state/checkpoint documents, operator documentation, and the VoiceBridge media feature-branch authority relevant to K-Research & Critic.

Audit baseline before this documentation synchronization:

```text
KRC branch: agent/video-url-research
KRC head: 3d6ff2a76c58f3bb4fe0168388b2ca850a36fc19
KRC last exact-head CI: Tests 33037053862 = SUCCESS
VoiceBridge branch: agent/krc-media-transcript
VoiceBridge head: 20afd2e54b87b4a2a8858961a03e22f78a565189
KRC PR #8: draft/open/unmerged
VoiceBridge PR #28: draft/open/unmerged
```

## Runtime/Package Authority Verified

The audit confirmed the current private package declares:
- owner-only private publication state;
- Builder package `0.9.1-beta-a10` applied;
- Action schema `0.6.0-a9.10`;
- accepted YouTube, Instagram, Facebook, Telegram, and local attachment ingress;
- Facebook free Cobalt failure -> unavailable;
- no active/offered Facebook paid fallback;
- Telegram zero retrieval credits/no auth/no paid fallback;
- local attachment `openaiFileIdRefs` transport, zero retrieval credits, 32 MiB max;
- durable managed KRCM state;
- A10 copy-safe claim table accepted;
- external tester rollout paused;
- merge to public product not allowed.

## Major Documentation Drift Found

### 1. Old predeploy/YouTube-only descriptions

Several documents still described MEDIA as a YouTube-only preview or predeploy beta. This contradicted accepted multi-platform/local-attachment A9/A9.10 state.

Action: replaced with current owner-only zero-client input matrix.

### 2. Browser Helper incorrectly described as current normal flow

Older privacy/runbook/handoff documents still described KRCC + Helper as the current path.

Action: moved Helper to historical A8 fallback-only status and documented KRCM managed zero-client flow as current.

### 3. Telegram still marked pending

The old operator runbook still showed Telegram Builder/private GPT E2E pending.

Action: changed to accepted A9.9 runtime state.

### 4. Local attachment still marked future/feasibility-only

Older architecture/handoff documents described local upload as future technical feasibility work.

Action: changed to accepted A9.10 transport + ingestion + private-GPT E2E, including trusted OpenAI delivery, 32 MiB max, zero retrieval credits, and no file-token exposure.

### 5. Old media Action schema/package references

Top-level docs referenced the historical public-preview `media_transcript_openapi.yaml` as if it were the current private media package and in one place pointed to production VoiceBridge.

Action: separated the published Core package from the private MEDIA BETA package and documented `gpt_store/actions/media_managed_beta_openapi.yaml` plus the dedicated beta backend.

### 6. A10 package-ready wording after runtime acceptance

Older documentation did not reflect that the copy-safe fenced-table mitigation passed owner runtime testing.

Action: synchronized current docs to `A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED` and retained the external ChatGPT Copy defect as a known limitation.

### 7. Release decision was not consistently represented

Older docs pointed directly from completed acceptance toward release work without the owner's later hold decision.

Action: synchronized current docs to `RELEASE_HOLD_OWNER_TESTING` and made merge, production promotion, external testers, and public rollout independent HOLD gates.

### 8. Project identity drift in test documentation

The top-level test plan still described the product as `K_Supervisor` even though that name now belongs to a separate successor project, except for stable compatibility identifiers.

Action: corrected the test-plan product identity to K-Research & Critic while preserving compatibility identifiers where required.

## Files Synchronized

```text
README.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/TEST_PLAN.md
docs/GPT_STORE_DEPLOYMENT.md
docs/GPT_STORE_PACKAGE.md
docs/VIDEO_INPUT_UPGRADE.md
docs/PRIVACY_POLICY.md
docs/MEDIA_BETA_RUNBOOK.md
subprojects/media_beta/README.md
subprojects/media_beta/00_INDEX.md
subprojects/media_beta/01_ARCHITECTURE.md
subprojects/media_beta/02_ROADMAP.md
subprojects/media_beta/03_CURRENT_STATE.md
subprojects/media_beta/04_OPERATIONS_RUNBOOK.md
subprojects/media_beta/05_TEST_PLAN.md
subprojects/media_beta/06_DECISION_LOG.md
subprojects/media_beta/07_FREE_MODE_TARGET.md
subprojects/media_beta/08_CHAT_HANDOFF.md
subprojects/media_beta/09_WORK_LOG.md
```

## Files Intentionally Frozen

No runtime package behavior was changed by this audit:

```text
prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
gpt_store/actions/media_managed_beta_openapi.yaml
VoiceBridge media implementation code
```

Reason: the current Builder/Action/backend path is already runtime accepted. A documentation audit must not force an unnecessary Builder re-apply or create a new runtime package version.

The canonical managed instruction reference may contain historical package-status wording; runtime authority remains the applied Builder package plus manifest/current-state acceptance. Change it only together with a deliberate Builder package revision.

## Decision Log Synchronization

Added compact current decisions for:
- Facebook free Cobalt-only active path;
- Telegram public zero-credit/no-auth route;
- accepted local `openaiFileIdRefs` ingestion;
- A10 copy-safe fenced-table mitigation;
- release hold owner testing;
- independence of the four release gates.

Older D001-D022 decisions remain represented as historical/current summaries with detailed rationale preserved in Git history and phase records.

## Documentation Standard

Top-level repository documentation remains compatible with the repository rule: one Ukrainian description line after the title, ASCII thereafter. The media subproject retains numbered immutable phase/checkpoint/audit records as a documented legacy ordering exception so stable historical links are not renamed.

## Release Boundary After Audit

```text
A9 = ACCEPTED
A9.10 = ACCEPTED
A10 = ACCEPTED
private owner testing = ACTIVE
merge = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

No production/main/public transition was performed by the audit.

## Post-Audit Validation Rule

The audit commit must pass the standard KRC `Tests` workflow. Exact post-audit commit/CI evidence is authoritative in GitHub Actions and should be cited in the next project checkpoint or handoff if work resumes after this audit.

## Audit Marker

`MEDIA_BETA_PROJECT_DOCUMENTATION_AUDIT_2026_08_27_APPLIED`
