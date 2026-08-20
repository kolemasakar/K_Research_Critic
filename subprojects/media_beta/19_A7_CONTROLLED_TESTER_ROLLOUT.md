# MEDIA BETA A7 Controlled Tester Rollout

Version: 1.0
Status: IN_PROGRESS_PRIVACY_GATE
Updated: 2026-08-20

## Purpose

Prepare the first external closed-beta tester rollout after owner A5/A6 acceptance while preserving the production/public isolation boundary.

The rollout remains limited to the owner plus up to three invited testers. The public K-Research & Critic GPT, VoiceBridge production service, `main` branches, and draft PR merge state remain unchanged.

## Current rollout gate

Owner Builder captions-first end-to-end flow is accepted.

External tester rollout is split into two paths:

1. `CAPTIONS_FIRST` - READY for controlled tester use.
2. `AUDIO_FALLBACK` - BLOCKED pending AssemblyAI no-training/EU endpoint live validation.

## AssemblyAI privacy finding

Current VoiceBridge MEDIA BETA code uses the default AssemblyAI base URL:

`https://api.assemblyai.com`

AssemblyAI current documentation states:
- customers can opt out of model-improvement data sharing when their pricing plan supports it;
- paid customers can opt out in Data Controls;
- free users cannot opt out;
- files submitted through AssemblyAI European servers are not used for model training;
- Async / pre-recorded STT supports the EU base URL `https://api.eu.assemblyai.com`.

Therefore the controlled beta must not expose browser Audio fallback to external testers while the isolated MEDIA BETA runtime is still using the default US AssemblyAI endpoint on a free account.

Required remediation before enabling tester Audio fallback:
- route MEDIA BETA AssemblyAI Async STT through `https://api.eu.assemblyai.com`;
- preserve the same isolated beta key/resource/quota boundaries;
- deploy only to `voicebridge-krc-media-beta-kolemasakar`;
- live-test one browser Audio fallback job through the EU endpoint;
- confirm COMPLETED result, expected quota charge, provider cleanup, and no production regression;
- update privacy policy and this record with the accepted EU processing boundary.

Reference documentation:
- AssemblyAI, `Data retention and model training`;
- AssemblyAI, `How to Opt Out of Data Sharing for our Model Improvement Program`;
- AssemblyAI, `Cloud Endpoints and Data Residency / Select the Region`.

## Tester prerequisites

Each invited tester receives only:
- unlisted `K-Research & Critic - MEDIA BETA` GPT link;
- one unique tester beta code;
- KRC MEDIA BETA Helper 0.2.2 installation package/instructions;
- this short operating procedure;
- failure-report template.

Never provide testers:
- `KRC_MEDIA_ACTION_TOKEN`;
- `ASSEMBLYAI_API_KEY`;
- `RENDER_API_KEY`;
- Render dashboard access;
- another tester's beta code.

## Tester operating procedure - captions-first stage

1. Open the beta GPT through the private/unlisted link.
2. Send a public YouTube URL and request analysis/fact-check/research.
3. When requested, provide the assigned tester beta code in that chat only.
4. The GPT creates a `KRCC_...` job and returns the Job ID.
5. Open the same YouTube video in Chrome or Edge.
6. Open KRC MEDIA BETA Helper 0.2.2.
7. Enter the KRCC Job ID and assigned tester code.
8. Press `Use subtitles`.
9. If Helper returns `COMPLETED`, return to the beta GPT and send `continue`.
10. Review the DRAFT CriticProfile.
11. Use `1 / APPROVE`, `2 / EDIT`, or `3 / REJECT`.
12. On approval, allow the beta GPT to complete Research -> Critic -> final output.

During the current privacy-gate stage:
- if Helper reports captions unavailable/unusable, STOP that media test;
- do not use `Audio fallback` as an external tester until the EU endpoint gate is explicitly marked PASS;
- report `CAPTIONS_UNAVAILABLE_AUDIO_BLOCKED_BY_PRIVACY_GATE`.

## Minimum tester matrix

Tester 1 should complete at least:
- one Ukrainian auto-caption video;
- one additional public YouTube video selected independently by the tester;
- one normal CriticProfile approval flow;
- one EDIT or REJECT gate interaction if practical.

After Audio fallback is unblocked, at least one controlled tester should additionally complete:
- captions unavailable/unusable -> Audio fallback;
- normal-speed capture;
- AssemblyAI EU Async STT completion;
- GPT status/segments -> CriticProfile -> final workflow.

## Failure report template

Tester should provide:

```text
TESTER: T1/T2/T3
DATE/TIME + TIMEZONE:
VIDEO URL:
BROWSER: Chrome/Edge + version if known
HELPER VERSION: 0.2.2
STAGE: GPT_START / AWAITING_CLIENT / USE_SUBTITLES / AUDIO_FALLBACK / GPT_CONTINUE / CRITICPROFILE / RESEARCH / FINAL
VISIBLE STATUS OR ERROR:
KRCC JOB ID:
CAPTIONS EXPECTED: yes/no/unknown
AUDIO FALLBACK USED: yes/no
WHAT HAPPENED:
SCREENSHOT: optional, redact tester code
```

Never include the tester beta code, Action bearer secret, provider API key, or Render API key in a failure report.

## Monitoring during rollout

Track at minimum:
- total jobs by tester code identity only through non-secret operational labels where available;
- captions vs AssemblyAI fallback share;
- STT seconds charged per UTC day;
- Render beta health and abnormal restarts;
- provider cleanup state on normal AssemblyAI completions;
- `MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED` occurrences;
- caption extraction failures;
- recurrent `U+FFFD` text artifacts;
- Postgres job/ledger lifecycle;
- user-visible failures in CriticProfile, approval gate, Research, Critic, and final reporting.

## Pass criteria for A7

A7 can be marked COMPLETE only when:
- at least one external tester completes captions-first flow end-to-end without owner intervention beyond onboarding;
- unique tester-code isolation works as intended;
- failure reporting is usable;
- no beta/developer secrets are exposed;
- no production/public system is modified;
- AssemblyAI Audio fallback is either live-validated through the EU no-training path or remains explicitly disabled for testers;
- observed reliability/resource use is acceptable for continuing the closed beta.

## Current decision

`A7_CAPTIONS_FIRST_TESTER_ROLLOUT_READY`

`A7_AUDIO_FALLBACK_EXTERNAL_TESTER_BLOCKED_PENDING_EU_NO_TRAINING_VALIDATION`
