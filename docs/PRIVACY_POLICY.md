# PRIVACY_POLICY
Політика конфіденційності додаткового режиму обробки відеопосилань у K-Research & Critic.

Version: 0.3
Status: CLOSED BETA / PREVIEW / RELEASE GATE
Effective candidate date: 2026-08-17

## 1. Scope

This policy applies to the optional Media Transcript Action and the separate closed-beta browser helper used by K-Research & Critic to obtain source text from a public video URL.

The normal text research workflow does not require this external media service.

The current rollout is a closed beta for a small tester group. The published production GPT and the validated production VoiceBridge translation extension remain separate and unchanged.

## 2. Current A4.2 Data Flow

The direct Render/datacenter YouTube-download path is not the current beta acceptance path because live testing confirmed YouTube anti-bot blocking from that cloud ingress.

The current client-assisted flow is:

```text
public YouTube URL
 -> beta GPT creates KRCC_ job
 -> separate KRC MEDIA BETA browser helper captures audio from the same active YouTube tab
 -> helper uploads captured audio to isolated VoiceBridge MEDIA BETA
 -> VoiceBridge normalizes audio for speech transcription
 -> AssemblyAI async transcription
 -> timestamped transcript returned to K-Research & Critic
```

A reliable transcript/caption already available through current built-in/web capabilities may be preferred without using the browser-audio path. Client-side caption extraction by the helper is not implemented in A4.2 and must not be claimed as current behavior.

## 3. Data Processed by the Media Path

For client-assisted transcription the path may process:

- the public YouTube URL supplied by the user;
- a closed-beta tester access code used for authorization and client-job ownership;
- technical request/job identifiers;
- the active-tab YouTube URL sent by the helper for same-source validation;
- compressed audio captured from the active YouTube tab;
- derived duration and quota metadata;
- transcript text, timestamps, detected/source language information, and transcription confidence.

Unrelated ChatGPT conversation content must not be sent to the Media Transcript service.

## 4. Closed-Beta Access Code

The beta tester code is separate from the GPT Action bearer secret and provider API keys.

The beta GPT must never echo, quote, summarize, include, or store the tester code in reports or checkpoints.

For A4.2 client jobs, the backend does not persist the plaintext tester code in public job state. It may hold a one-way SHA-256 digest in process memory during the job lifetime to enforce per-tester job ownership.

The current developer-mode browser helper may store the tester code in that extension's local browser storage for closed-beta convenience. This is a beta-only local credential convenience and must be reviewed before any public extension distribution. Testers should use the helper only on a trusted browser profile/device.

If a tester code is disclosed, it should be replaced in the VoiceBridge beta environment configuration.

## 5. Processing Services

The current A4.2 browser-audio path uses:

- the separate KRC MEDIA BETA browser helper for active-tab audio capture on the tester device/network path;
- the isolated VoiceBridge MEDIA BETA service as the media-ingestion adapter;
- AssemblyAI Universal-2 for async speech-to-text of helper audio;
- YouTube as the public source viewed by the tester in their browser.

Third-party processing is also subject to applicable provider privacy, security, and data-processing terms.

## 6. Data Minimization

The helper captures audio only, not video frames.

The current helper records Opus audio at approximately 32 kbps and uploads only after the tester stops capture. VoiceBridge then normalizes the uploaded audio to speech-oriented mono 16 kHz audio at approximately 32 kbps for provider transcription.

The helper validates that the active tab is YouTube. The backend checks that the active-tab source identifies the same YouTube video as the KRCC job before accepting audio.

Current closed-beta limits include a 32 MiB client-audio upload guard and a 60-minute captured-audio duration limit.

Media data is processed only to obtain source text, preserve timestamps/confidence for traceability, and enable later claim verification after CriticProfile approval.

The transcript itself is not treated as independent evidence that a factual claim is true.

## 7. VoiceBridge and Browser Retention

The closed-beta configuration follows these rules:

- captured audio is buffered temporarily by the helper until upload/Stop completes;
- backend uploaded/normalized media is stored only in a temporary working directory;
- the temporary backend media directory is deleted after the transcription attempt finishes;
- completed transcript segments and job metadata are held in backend process memory only;
- the default in-memory job retention is approximately one hour;
- the media route does not intentionally write transcript content or plaintext tester access codes to the VoiceBridge database or operational logs;
- the full transcript and tester access code are not stored in K-Research & Critic checkpoints.

The browser helper currently stores endpoint, job ID, and tester code in extension local storage. The tester may remove this local beta data by removing/resetting the helper extension or clearing its extension storage.

A server restart may remove in-memory jobs earlier.

The daily beta STT usage counter is also process-memory beta state. A restart may reset that safety counter; this is acceptable only for trusted closed-beta testing and is not sufficient as a future public anti-abuse mechanism.

## 8. Speech-to-Text Provider Deletion

After a transcript result is obtained, VoiceBridge requests deletion of the corresponding AssemblyAI transcript. AssemblyAI documents that deleting a transcript also deletes audio uploaded through its upload endpoint.

The media job exposes `provider_data_deleted` so the service can distinguish successful provider deletion from a cleanup failure.

If provider deletion fails, provider-side retention is governed by AssemblyAI's then-current data-retention policy. K-Research & Critic must not claim third-party deletion succeeded when `provider_data_deleted` is not true.

## 9. Resource Limits

The current closed beta intentionally limits shared external-resource use:

- maximum captured audio duration: 60 minutes;
- maximum concurrent client media jobs: 1;
- maximum helper audio upload: 32 MiB;
- global AssemblyAI budget: 7200 seconds of captured audio per UTC day;
- helper audio uses the STT budget;
- direct reliable transcript/caption intake that does not invoke AssemblyAI does not use this beta STT budget.

These are beta safety controls and may change only through an explicit project decision.

## 10. Model-Training Release Gate

Before public production rollout of any AssemblyAI-backed media path, the AssemblyAI project used by this feature must be verified as opted out of provider model training or otherwise configured under terms that prohibit training on submitted media.

Until that configuration is verified, this document and the media feature remain PREVIEW / RELEASE GATE and must not be represented as a completed public privacy configuration.

## 11. User Responsibilities

Users should submit only media they are permitted to access and process. Users should avoid private or confidential media in this public-URL beta workflow.

The initial media mode supports public HTTPS YouTube URLs only.

During A4.2 browser capture, testers should capture only the intended YouTube tab and should stop capture when the relevant source content ends.

## 12. Security

The GPT Action uses a dedicated server-to-server bearer secret. The browser helper never receives that Action secret or the AssemblyAI API key.

The helper authenticates browser upload/status requests with the closed-beta tester code and sends the active-tab source URL so the backend can enforce same-video matching.

Developer/provider secrets must not be stored in prompts, checkpoints, transcripts, repository files, browser-helper fields, or user-visible reports.

Personal YouTube account cookies are not part of the approved A4.2 architecture.

## 13. Changes

Material changes to media processors, browser-helper behavior, retention, supported source types, access controls, or data use require a policy update and new release validation before public rollout.

## 14. Contact

Project and privacy questions may be raised with the repository owner through the public GitHub project `kolemasakar/K_Research_Critic`.
