# VIDEO_INPUT_UPGRADE
Архітектура додаткового режиму дослідження тверджень із відео без зміни базового текстового workflow.

Version: 0.1
Status: PREVIEW
Date: 2026-08-17

## 1. Objective

Add a video-URL intake path to K-Research & Critic without replacing or weakening the existing production text-research path.

Initial target:

```text
public YouTube URL
source language: auto / uk / ru / en
-> timestamped transcript
-> material claim inventory
-> existing CriticProfile approval gate
-> existing Research -> Critic -> revision loop
-> FINAL REPORT + REVIEW PROTOCOL
```

## 2. Non-Regression Rule

The existing workflow remains valid and unchanged for ordinary text tasks:

```text
User task
-> CriticProfile
-> user approval/edit/reject
-> Research
-> Critic
-> autonomous revision
-> FINAL REPORT
-> REVIEW PROTOCOL
```

Media ingestion is an optional adapter before the profile gate. It is not a replacement Supervisor, ResearchAgent, CriticAgent, report format, checkpoint contract, or web-search path.

## 3. Architecture

```text
USER VIDEO URL
      |
      v
K-Research & Critic media intake
      |
      +-- built-in accessible transcript/captions when reliable
      |
      +-- Media Transcript Action when configured
              |
              v
       VoiceBridge Cloud
              |
              +-- URL allowlist / limits
              +-- yt-dlp public-media fetch
              +-- temporary audio
              +-- AssemblyAI async STT
              +-- provider delete request
              v
       timestamped transcript segments
      |
      v
claim inventory
      |
      v
CriticProfile approval gate
      |
      v
existing Research/Critic pipeline
```

## 4. Evidence Boundary

The media transcript is a primary source for what the speaker said.

It is not independent evidence that the statement is correct.

A factual claim from the media must be checked against independent sources under the approved CriticProfile. Repetition of the same video or speaker does not count as an independent cross-check.

## 5. Claim Types

Media intake separates:

```text
FACTUAL_CLAIM
OPINION
PREDICTION
RECOMMENDATION
RHETORICAL_OR_NON_CHECKABLE
TRANSCRIPTION_UNCERTAIN
```

Material factual claims should retain a timestamp or transcript segment reference whenever available.

## 6. Factual Verdicts

The final media report may use:

```text
VERIFIED
PARTLY_SUPPORTED
UNSUPPORTED
CONTRADICTED
MISLEADING
UNVERIFIABLE
```

`UNSUPPORTED` does not automatically mean false. Opinions, predictions, and recommendations are identified separately when they are not suitable for a factual verdict.

## 7. Language Baseline

Initial explicit language set:

```text
uk - Ukrainian
ru - Russian
en - English
auto - provider language detection
```

The report language remains controlled by the normal K-Research & Critic language rules and may differ from source language.

## 8. VoiceBridge Reuse

The upgrade reuses VoiceBridge cloud/provider experience but does not depend on its browser-extension capture path.

A new prerecorded-media route is isolated from the existing streaming translation workflow.

The VoiceBridge change is developed on:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
```

The K-Research & Critic integration is developed on:

```text
repository: kolemasakar/K_Research_Critic
branch: agent/video-url-research
```

## 9. Security and Privacy

Required controls:

- accept only allowlisted public HTTPS media hosts;
- use a dedicated Action bearer secret separate from VoiceBridge test access;
- never expose AssemblyAI credentials to GPT users;
- delete temporary local media after processing;
- retain transcript/job state in memory only for a bounded TTL;
- request deletion of the provider transcript/audio after processing;
- do not store the full transcript in K-Research & Critic checkpoints;
- keep the media feature in PREVIEW until provider model-training opt-out is verified;
- publish a valid privacy-policy URL before Store rollout.

## 10. Failure Handling

If the media path cannot obtain a reliable transcript:

```text
try reliable built-in/web-accessible captions
-> try configured Media Transcript Action
-> if unavailable/failed, request user transcript/audio/file
-> never infer or fabricate unavailable video content
```

An asynchronous transcription job may outlive one GPT tool-call window. If bounded status checks do not reach COMPLETED, the user may explicitly continue the same job in the next turn.

## 11. Store Package Changes

Planned package boundary:

```text
core text mode:
  external_backend_required: false
  developer_api_key_required: false

media URL mode:
  external_backend_required: true
  developer_provider_key_required: true
  user_api_key_required: false
```

The Action schema is:

```text
gpt_store/actions/media_transcript_openapi.yaml
```

The privacy document is:

```text
docs/PRIVACY_POLICY.md
```

## 12. Release Gates

Do not merge/publish media mode as complete until all applicable gates pass:

```text
VoiceBridge TypeScript build
VoiceBridge existing tests
VoiceBridge media unit tests
K-Research & Critic full pytest
repository validation
Store package validation
Action schema import in GPT Builder
Action bearer authentication test
real YouTube transcription: uk
real YouTube transcription: ru
real YouTube transcription: en
automatic language detection test
claim extraction / timestamp traceability test
Research -> Critic REVISE/PASS test
Free-plan live test
paid-plan live test
provider model-training opt-out verified
privacy-policy public URL configured
production smoke test
```

Only after these gates pass should `media_input.rollout_state` move from `PREVIEW_REQUIRED` to a production state and its production smoke-test flag become true.
