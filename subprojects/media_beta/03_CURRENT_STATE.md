# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 3.6
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-20

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_OWNER_ONLY_FINALIZATION_IN_PROGRESS`

Current product target:

`PRIVATE OWNER-ONLY MEDIA BETA`

The owner explicitly paused investigation of GPT public/link sharing and paused the external Tester 1 rollout. The project is now being completed for private owner-only use with GPT access set to `Only me`.

Canonical owner-only completion plan:
`subprojects/media_beta/22_OWNER_ONLY_COMPLETION_PLAN.md`

## Accepted technical state

The core media architecture is accepted:

```text
YouTube URL
 -> private MEDIA BETA GPT Action creates durable KRCC job
 -> AWAITING_CLIENT
 -> Helper 0.2.2 on the same YouTube tab
 -> captions first
      -> COMPLETED / youtube_captions / STT=0
 -> if captions unavailable/unusable
      -> Audio fallback
      -> AssemblyAI EU Universal-2
      -> timestamped transcript
      -> provider delete request on normal completion
 -> GPT status + all transcript pages
 -> material claim inventory
 -> DRAFT CriticProfile
 -> explicit owner APPROVE/EDIT/REJECT
 -> independent Research
 -> Critic/revision loop
 -> FINAL REPORT / CLAIM VERIFICATION / REVIEW PROTOCOL
```

Transcript text is evidence of what the video represents as being said, not independent evidence that its factual claims are true.

## Repositories and production boundary

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service and `main` unchanged.

Do not merge PR #8 or PR #28 as part of owner-only completion.

## Dedicated beta runtime

Service:
`voicebridge-krc-media-beta-kolemasakar`

Service ID:
`srv-da1kic5bedkc73d6fk60`

Endpoint:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Accepted controls:
- max duration 3600 sec;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec per UTC day;
- Helper required for client-assisted ingestion;
- durable Postgres job state;
- restart-resilient waiting/completed jobs;
- durable STT quota ledger;
- active-audio hard process loss returns retry-safe terminal failure;
- AssemblyAI fallback routed through `https://api.eu.assemblyai.com`.

## A4 - Live transcript validation

Status: PASS / COMPLETE.

Canonical records:
- `10_A4_2_CAPTIONS_ACCEPTANCE.md`;
- `11_A4_3_AUDIO_FALLBACK_ACCEPTANCE.md`;
- `12_A4_4_DURABILITY_ACCEPTANCE.md`;
- `13_A4_5_GUARD_MATRIX_ACCEPTANCE.md`;
- `14_A4_LANGUAGE_SOURCE_MATRIX_ACCEPTANCE.md`;
- `15_A4_QUOTA_LEDGER_RESTART_ACCEPTANCE.md`;
- `16_A4_ACTIVE_AUDIO_PROCESS_REPLACEMENT_ACCEPTANCE.md`;
- `17_A4_STT_TEXT_QUALITY_DISPOSITION.md`.

Accepted evidence includes UK/RU/EN/AUTO caption cases, captions STT=0, AssemblyAI Universal-2 fallback, exact duration/quota accounting, normal provider cleanup, durable restart state, durable quota restoration, retry-safe active-audio process-loss behavior, and U+FFFD non-reproducible disposition.

Residual limitation: a hard process death during active AssemblyAI work may leave `provider_data_deleted=null`.

## A5 - Separate GPT Builder beta

Status: PASS / COMPLETE.

Separate GPT:
`K-Research & Critic - MEDIA BETA`

Accepted Builder configuration:
- Builder-safe instructions within 8000-character limit;
- web search enabled;
- image generation disabled;
- code interpreter/data analysis enabled;
- API Key/Bearer Action authentication;
- Action server restricted to isolated beta runtime;
- privacy policy configured;
- all three GPT-facing operations manually tested PASS;
- manual transcript pagination confirmed 227/227 segments;
- CriticProfile gate blocks independent research before approval.

Canonical acceptance:
`subprojects/media_beta/18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md`

## A6 - Owner/operator E2E

Status: PASS / COMPLETE.

The owner/operator completed the captions-first Builder flow through CriticProfile approval, independent Research, Critic/revision and finalization.

Historical live runs used the credential designated for `Tester 1`, operated by the owner. This is a credential-attribution detail only and does not revoke technical acceptance.

Canonical correction:
`subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`

## A7 - External tester rollout

Status: PAUSED_BY_OWNER.

The external sharing restriction investigation, appeal path, private-link distribution, and Tester 1/2/3 onboarding are intentionally paused.

Previously accepted external-readiness evidence remains preserved, including the EU Audio privacy gate, but no independent external tester run is required for the current owner-only target.

## A8 - Owner-only product finalization

Status: IN_PROGRESS.

The private GPT has been created successfully and is currently set to `Only me`.

Remaining mandatory acceptance step:
- perform one clean post-create end-to-end smoke test through the actual private GPT, not Builder Preview.

Preferred credential for this final smoke test:
- the separately designated owner credential, so the final private-product evidence matches the owner-only operating model.

Required smoke path:

```text
private GPT
 -> public YouTube URL
 -> valid owner credential
 -> KRCC job
 -> Helper 0.2.2
 -> captions-first completion
 -> status + complete segments
 -> DRAFT CriticProfile
 -> owner APPROVE
 -> Research
 -> Critic
 -> final output
```

The accepted EU Audio fallback does not need to be repeated in this final smoke test unless captions are unavailable/unusable; it already passed live validation.

On PASS create a dedicated owner-only acceptance record and set:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_EXTERNAL_ROLLOUT_PAUSED / A8_OWNER_ONLY_COMPLETE`

## CI state

The KRC package validator was synchronized with the current media-beta v0.4 contract and AssemblyAI EU privacy wording. GitHub Actions run #469 completed successfully after the synchronization.

## Deferred items that do not block owner-only completion

- GPT public/link sharing and any appeal;
- external Tester 1/2/3 rollout;
- Free-plan compatibility;
- public Store promotion;
- sustainable public free-media Phase B/C work;
- merge to production `main`.

## Known private-beta limitations

- YouTube browser caption interfaces may change;
- captions remain preferred before Audio fallback;
- Audio fallback requires normal-speed playback for timestamp alignment;
- AssemblyAI fallback quota is finite;
- Free Postgres is temporary beta infrastructure;
- hard process death may leave provider cleanup unconfirmed.
