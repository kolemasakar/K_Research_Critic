# MEDIA_BETA_RUNBOOK
Інструкція оператора для поточного owner-only zero-client MEDIA BETA у режимі release hold.

Version: 1.0-a10
Status: RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## 1. Authority and Isolation

```text
KRC repo:        kolemasakar/K_Research_Critic
KRC branch:      agent/video-url-research
KRC draft PR:    #8
VoiceBridge repo: kolemasakar/VoiceBridge
VoiceBridge branch: agent/krc-media-transcript
VoiceBridge draft PR: #28
beta backend:    https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

Do not merge either draft PR, modify public KRC `main`, or promote to production VoiceBridge during the current hold.

## 2. Current Private GPT Package

```text
Name: K-Research & Critic - MEDIA BETA
Builder instructions: prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md
canonical reference: prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md
Action schema: gpt_store/actions/media_managed_beta_openapi.yaml
Builder version: 0.9.1-beta-a10
Action schema version: 0.6.0-a9.10
```

The accepted Builder package is already applied. Documentation-only maintenance does not require re-importing the schema or instructions.

## 3. Normal Owner Flow

```text
supported public media URL OR one local attachment
 -> private Action
 -> transcript acquisition
 -> CriticProfile gate
 -> explicit owner approval
 -> Research
 -> Critic
 -> final report in same conversation
```

Do not ask for a beta code, provider key, platform cookies/session, Helper, file ID, signed URL, or KRCM Job ID.

## 4. Platform Routing

### YouTube / Instagram

Use managed native preflight before any billable native request. Show the provider credit estimate and require explicit approval. Instagram AI generation requires a separate preflight and a new approval.

### Facebook

Call the free Cobalt path. On success, use the returned durable transcript. On Cobalt failure, report media unavailable and stop. Never call or offer the reserved paid Facebook operations in the active flow.

### Telegram

Use the public Telegram transcription operation without retrieval-credit preflight. No Telegram login/cookies/session/bot token/paid fallback. Terminal unavailable/no-speech stops the route.

### Local attachment

Use the current-conversation attachment operation. Do not ask the user to copy a file reference. The backend validates trusted OpenAI delivery and media constraints. Retrieval credits are zero; STT accounting is separate.

## 5. Job Handling

- hide KRCM Job IDs;
- bounded status reads only;
- fetch all segment pages until complete;
- reuse durable completed jobs when returned as reused;
- never auto-retry uncertain-charge work;
- never invent transcript or job state.

## 6. Research/Critic Gate

After transcript availability, create the CriticProfile before independent research. The first user gate remains direct run / review-edit / cancel. Explicit option `1` approves the current profile and starts research.

Cross-check floors:

```text
LOW>=0 MEDIUM>=1 HIGH>=2 CRITICAL>=3
```

Every material factual claim must expose required/achieved/exception accounting and preserve SHORTFALL.

## 7. A10 Output Rule

Always keep the accepted claim-summary behavior:
- normal rendered four-column table;
- immediately followed by the copy-safe fenced `text` duplicate;
- identical rows/values;
- literal pipe delimiters in the fenced copy.

## 8. Owner Testing During Hold

Use fresh chats for meaningful regressions. Test varied supported sources and failure cases. Record only material defects and acceptance evidence; do not record secrets or full transcripts.

When a defect is found:
1. reproduce it;
2. determine whether it is KRC package, VoiceBridge, provider, source-platform, or ChatGPT UI behavior;
3. fix only in the isolated feature branch that owns the defect;
4. add regression coverage where practical;
5. run full relevant CI;
6. repeat private runtime acceptance when Builder/backend behavior changed.

## 9. Known Accepted Limitation

Whole-response Copy may collapse the visually correct rendered Markdown table header. The fenced duplicate is the accepted mitigation. Do not reopen A10 solely because the external UI defect persists while the copy-safe block remains correct.

## 10. Rollback

If a new private package change breaks runtime behavior:
- restore the last accepted private Builder package when Builder content changed;
- keep diagnosis/fix on the feature branch;
- do not use production deployment or public Core changes as rollback mechanisms.

## 11. Release Hold

Current owner decision:

```text
merge = HOLD
production promotion = HOLD
external testers = HOLD
public rollout = HOLD
```

Release decisions are independent. Wait for explicit authorization before any transition.

## 12. Recovery

Start recovery from:

```text
subprojects/media_beta/00_INDEX.md
subprojects/media_beta/03_CURRENT_STATE.md
subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
subprojects/media_beta/54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
```
