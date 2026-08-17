# K-Research & Critic MEDIA BETA
Окремий документаційний підпроєкт для відеоаналізу, закритого beta-тестування та подальшого сталого безкоштовного медіарежиму.

Version: 1.0
Status: CLOSED_BETA_PREDEPLOY
Updated: 2026-08-17

## Objective

Allow a user to provide a public YouTube URL and obtain the normal K-Research & Critic workflow over material claims from the video:

```text
YouTube URL
  -> transcript acquisition
  -> timestamped material claim inventory
  -> CriticProfile
  -> user APPROVE / EDIT / REJECT
  -> independent Research
  -> independent Critic
  -> autonomous REVISE / PASS loop
  -> FINAL REPORT
  -> CLAIM VERIFICATION
  -> REVIEW PROTOCOL
```

## Core evidence rule

A transcript proves what the speaker said. It does not independently prove that the statement is true.

Independent external verification starts only after CriticProfile approval.

## Current first-priority mode: CLOSED MEDIA BETA

Target group:

- project owner;
- up to three additional testers.

Resource controls:

- public YouTube only;
- source languages: Ukrainian, Russian, English, plus automatic detection;
- maximum video duration: 60 minutes;
- one active media job at a time;
- YouTube captions first;
- AssemblyAI only when usable captions are unavailable;
- global AssemblyAI fallback budget: 7200 source-audio seconds per UTC day;
- fallback audio: mono, 16 kHz, approximately 32 kbps;
- per-tester access codes;
- no user-supplied provider/API keys.

## Production isolation

The beta must not replace or modify the validated production services during testing.

Production VoiceBridge endpoint:

`https://voicebridge-cloud-us.onrender.com`

Dedicated beta target:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

The published K-Research & Critic text workflow remains production baseline.

## Repository implementation split

K-Research & Critic contains:

- GPT instructions and workflow semantics;
- beta Action OpenAPI schema;
- beta manifest;
- privacy and product documentation;
- package validation and regression tests.

VoiceBridge contains:

- URL validation;
- YouTube metadata and captions acquisition;
- audio download/optimization fallback;
- AssemblyAI asynchronous transcription;
- access-code enforcement;
- daily STT budget enforcement;
- transcript paging and temporary retention;
- provider cleanup attempt;
- Render beta deployment blueprint.

## Beta is not production

Code-level CI success is necessary but not sufficient. Media beta remains blocked from public production until all live release gates in `02_ROADMAP.md` and `05_TEST_PLAN.md` pass.

## Future direction

After beta validation, the target is a sustainable free media pipeline:

```text
captions first
  -> free cloud STT quota when required
  -> optional local Whisper fallback
```

AssemblyAI is a beta/reliability tool, not the intended permanent public free-tier dependency.