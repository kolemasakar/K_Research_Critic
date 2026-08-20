# MEDIA BETA Current State

Canonical implementation checkpoint for continuation without reconstruction.

Version: 3.4
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-20

## Executive state

Current phase state:

`A4_COMPLETE / A5_COMPLETE / A6_COMPLETE / A7_READY_FOR_TESTER1`

Accepted phase markers:

`A4_CAPTIONS_FIRST_PASS / A4_AUDIO_FALLBACK_PASS / A4_GUARD_MATRIX_PASS / A4_LANGUAGE_SOURCE_MATRIX_PASS / A4_RESTART_DURABILITY_PASS / A4_DURABLE_QUOTA_LEDGER_RESTART_PASS / A4_ACTIVE_AUDIO_RETRY_SAFE_FAILURE_PASS / A4_STT_TEXT_QUALITY_DISPOSITION_PASS / A5_GPT_BUILDER_CONFIGURATION_PASS / A5_BUILDER_ACTION_START_PASS / A5_BUILDER_CAPTIONS_FIRST_PROFILE_GATE_PASS / A6_OWNER_OPERATOR_E2E_USING_TESTER1_CREDENTIAL_PASS / A7_CAPTIONS_FIRST_TESTER_ROLLOUT_READY / A7_EU_AUDIO_FALLBACK_PRIVACY_GATE_PASS / A7_TESTER1_READY`

Credential-attribution correction:
- all prior MEDIA BETA live tests were executed by the owner/operator using the access code designated for `Tester 1`;
- the separate owner-designated beta code has not yet been independently live-validated;
- this does not revoke any technical A4/A5/A6/A7 acceptance result;
- the owner-operated runs do not count as an independent external Tester 1 human rollout;
- canonical correction: `subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`.

The approved MEDIA BETA architecture remains captions-first browser-assisted YouTube ingestion. Direct Render/datacenter YouTube acquisition remains unsuitable because of YouTube anti-bot enforcement. Browser audio plus AssemblyAI is fallback only when usable captions are unavailable.

Production VoiceBridge and the published K-Research & Critic GPT remain unchanged. PR #8 and PR #28 remain draft and unmerged.

## Repositories

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

## Dedicated Render beta

Service:
`voicebridge-krc-media-beta-kolemasakar`

Service ID:
`srv-da1kic5bedkc73d6fk60`

Endpoint:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Verified controls:
- free Render beta service isolated from production;
- max duration 3600 sec;
- max concurrent jobs 1;
- AssemblyAI fallback budget 7200 sec per UTC day;
- language hints auto/uk/ru/en;
- Helper required for client-assisted ingestion;
- durable Postgres job state;
- restart-resilient waiting/completed jobs;
- durable STT quota ledger;
- active-audio hard process loss returns explicit retry-safe terminal failure;
- client-assisted AssemblyAI fallback routed through `https://api.eu.assemblyai.com` in the accepted A7 beta deployment.

## Approved media flow

```text
YouTube URL
 -> MEDIA BETA GPT Action creates durable KRCC job
 -> AWAITING_CLIENT
 -> Helper 0.2.2 on the same YouTube tab
 -> Use subtitles first
      -> direct timed-text when usable
      -> transcript-panel fallback otherwise
      -> COMPLETED / youtube_captions / STT=0
 -> if captions unavailable/unusable
      -> Audio fallback
      -> tab capture
      -> server normalization
      -> duration/quota reservation
      -> AssemblyAI EU Universal-2
      -> timestamped transcript
      -> provider delete request on normal completion
 -> GPT status + paginated segments
 -> material claim inventory
 -> DRAFT CriticProfile
 -> explicit user APPROVE/EDIT/REJECT
 -> independent Research
 -> Critic / revision loop
 -> FINAL REPORT / CLAIM VERIFICATION / REVIEW PROTOCOL
```

Transcript text is evidence of what the video represents as being said, not independent evidence that factual claims are true.

## Browser helper

Current helper:
`KRC MEDIA BETA Helper 0.2.2`

Accepted helper functions:
- captions-first extraction;
- transcript-panel fallback;
- timestamped segment extraction;
- Audio fallback;
- active-tab source validation;
- immediate Job ID persistence;
- stale terminal-state isolation;
- no Action bearer token or AssemblyAI key stored in the extension.

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

Key accepted evidence:
- UK auto captions: 227/227 segments, STT=0;
- RU auto captions: 524 segments, STT=0;
- EN manual captions: 247 segments, STT=0;
- AUTO selected IT manual track correctly;
- audio fallback completed through AssemblyAI Universal-2 with measured quota accounting and normal provider cleanup;
- invalid code/source mismatch/concurrency/>60 min/quota guards passed;
- durable waiting/completed state and immutable `created_at` survived required restarts;
- real STT charge restored from durable quota ledger after restart;
- forced process loss during TRANSCRIBING returned `FAILED / MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED / retryable=true` on the same durable Job ID;
- interrupted 249.444-second job charged exactly 250 seconds with no duplicate charge;
- historical U+FFFD anomaly was not reproduced in two fresh successful STT controls and is dispositioned as non-reproducible quality anomaly, not an A4 blocker.

All of these live runs used the Tester 1 credential operated by the owner unless a specific record states otherwise.

Residual hardening:
- hard process death may leave `provider_data_deleted=null`; orphan-provider cleanup remains a release-hardening item.

## A5 - Separate GPT Builder beta

Status: PASS / COMPLETE.

Separate Builder identity:
`K-Research & Critic - MEDIA BETA`

Accepted Builder configuration:
- Builder-safe instructions file `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md` within the current 8000-character Builder limit;
- web search enabled;
- image generation disabled;
- code interpreter/data analysis enabled;
- API Key / Bearer Action authentication using the dedicated beta Action secret;
- OpenAPI schema `gpt_store/actions/media_beta_openapi.yaml`;
- Action server restricted to the isolated beta Render endpoint;
- privacy policy URL configured;
- Builder recognized exactly the intended GPT-facing operations:
  - `startMediaBetaClientTranscription`;
  - `getMediaBetaClientTranscriptionStatus`;
  - `getMediaBetaClientTranscriptSegments`.

The Builder preview correctly enforced `MEDIA BETA ACCESS REQUIRED` before Action start when no tester beta code was supplied.

Accepted Builder-created job:
`KRCC_8945357e-d6cf-4483-b7ca-178b81729665`

Credential used for the accepted live run:
`Tester 1 credential`, operated by the owner.

The same job completed through Helper 0.2.2:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
language=uk
segment_count=227
stt_seconds_charged=0
```

After `continue`, the GPT returned a DRAFT CriticProfile with `status=REVIEW_REQUIRED`, CRITICAL medical risk, source/cross-check requirements, transcription uncertainty handling, and the mandatory `1-APPROVE / 2-EDIT / 3-REJECT` stop. No independent research occurred before approval.

## A6 - Owner/operator end-to-end beta acceptance

Status: PASS / COMPLETE for the first owner-operated captions-first Builder workflow using the Tester 1 credential.

The owner/operator entered `1` at the profile gate.

Observed continuation:
- profile transitioned to APPROVED;
- `approved_by=user` recorded;
- GPT retrieved transcript segments through the Action path;
- independent web research began only after approval;
- Critic/revision/finalization path completed successfully in Builder Preview;
- owner/operator confirmed completion as OK.

Canonical acceptance:
`subprojects/media_beta/18_A5_A6_GPT_BUILDER_E2E_ACCEPTANCE.md`

Credential-attribution correction:
`subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`

This acceptance validates the workflow with a valid allowlisted Tester 1 credential but does not constitute an independent external Tester 1 human run.

## A7 - Controlled tester rollout

Status: READY_FOR_TESTER1.

Canonical rollout record:
`subprojects/media_beta/19_A7_CONTROLLED_TESTER_ROLLOUT.md`

Canonical EU Audio acceptance:
`subprojects/media_beta/20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md`

Credential-attribution correction:
`subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`

Current readiness:
- captions-first: READY for controlled external tester use;
- Audio fallback: READY for controlled external tester use when captions are unavailable/unusable;
- Tester 1 credential: already live-used extensively by the owner/operator;
- independent external Tester 1 human onboarding/run: NOT YET PERFORMED;
- owner-designated credential: NOT YET independently live-validated.

Accepted EU Audio fallback deployment:

```text
KRC_MEDIA_ASSEMBLYAI_BASE_URL=https://api.eu.assemblyai.com
VoiceBridge commit=7a61790221b6f75c14293360002794208efd813f
Render deploy=dep-da3f2te417fc73e600ng
status=live
```

Accepted EU live job:

`KRCC_a79ad701-d5a0-40ca-91f8-6fbdfc6c3bc6`

This job was executed by the owner/operator using the Tester 1 credential.

Final result:

```text
status=COMPLETED
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
detected_language=uk
language_confidence=0.695
duration_seconds=122.292
stt_seconds_charged=123
transcript_characters=1608
segment_count=3
error=null
```

Quota:

```text
used before=422
used after=545
delta=123
```

The quota delta equals `stt_seconds_charged` and `ceil(122.292)`.

Current AssemblyAI documentation states that files submitted through its European servers are not used for model training. This routing/privacy gate is therefore accepted for the controlled beta. Re-verification remains required before future public promotion.

## Backend routes

Action-facing:
```text
POST /api/v1/media/client-transcriptions
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/segments
```

Browser-only:
```text
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/captions
POST /api/v1/media/client-transcriptions/{KRCC_job_id}/audio
GET  /api/v1/media/client-transcriptions/{KRCC_job_id}/client-status
```

Browser-only routes remain intentionally absent from the GPT Action schema.

## Next phase action

Invite the actual external Tester 1 using the already designated Tester 1 code and Helper 0.2.2 onboarding package.

Require at least:
- one independent captions-first end-to-end flow performed by Tester 1 without owner intervention beyond onboarding;
- one additional tester-selected video;
- normal CriticProfile approval behavior;
- failure report if any issue occurs.

The separate owner-designated credential may be smoke-tested independently, but its lack of prior use does not invalidate the accepted technical workflow.

Do not mark A7 COMPLETE until external tester evidence exists and rollout reliability/resource use is acceptable.

## Release-hardening items after/alongside A7

- orphan-provider cleanup strategy after hard process loss;
- hosted/publicly stable privacy policy URL if required by sharing mode;
- Free-plan/paid runtime compatibility tests before public promotion;
- Free Postgres lifecycle/expiry management and future migration;
- continued monitoring for recurrent STT text-quality artifacts.

## Known beta limitations

- YouTube browser caption interfaces may change;
- direct timed-text may be empty even when captions exist;
- transcript-panel fallback is part of the accepted browser path;
- audio fallback requires normal-speed playback for timestamp alignment;
- Free Postgres is temporary beta infrastructure;
- hard process death can leave provider cleanup state unconfirmed;
- AssemblyAI remains a finite-credit beta fallback and is not the intended mandatory sustainable public free dependency.

Do not merge PR #8 or PR #28, modify the public GPT, add personal YouTube cookies, or introduce paid residential proxy ingress merely to continue the beta.
