# PRIVACY_POLICY
Політика конфіденційності додаткового режиму обробки відеопосилань у K-Research & Critic.

Version: 0.1
Status: PREVIEW / RELEASE GATE
Effective candidate date: 2026-08-17

## 1. Scope

This policy applies to the optional Media Transcript Action used by K-Research & Critic to obtain source text from a public video URL.

The normal text research workflow does not require this external media service.

## 2. Data Sent to the Media Service

When the user explicitly provides a supported public media URL for analysis, the media path may process:

- the supplied public media URL;
- public video metadata such as title, channel, duration, and canonical URL;
- audio derived from the public video for speech-to-text processing;
- transcript text, timestamps, language information, and transcription confidence;
- technical request/job identifiers needed to operate the service.

Unrelated ChatGPT conversation content must not be sent to the Media Transcript service.

## 3. Processing Services

The media path uses:

- VoiceBridge Cloud as the media-ingestion adapter;
- AssemblyAI as the speech-to-text provider;
- the source media platform, initially YouTube, to retrieve the public media selected by the user.

Third-party processing is also subject to the applicable provider privacy, security, and data-processing terms.

## 4. Purpose Limitation

Media data is processed only to obtain a transcript, identify statements for verification, and preserve timestamps/confidence for traceability.

The transcript itself is not treated as independent evidence that a factual claim is true.

## 5. VoiceBridge Retention

The planned production configuration follows these rules:

- downloaded media is stored only in a temporary working directory;
- the temporary media directory is deleted after the transcription attempt finishes;
- completed transcript segments and job metadata are held in process memory only;
- the default in-memory job retention is one hour;
- the media route does not intentionally write transcript content to the VoiceBridge database or operational logs;
- the full transcript is not stored in K-Research & Critic checkpoints.

A server restart may remove in-memory jobs earlier.

## 6. Speech-to-Text Provider Deletion

After the transcript result has been obtained, VoiceBridge requests deletion of the corresponding AssemblyAI transcript. AssemblyAI documents that deleting a transcript also deletes an audio file uploaded through its upload endpoint.

The media job exposes `provider_data_deleted` so the service can distinguish successful provider deletion from a cleanup failure.

If provider deletion fails, provider-side retention is governed by AssemblyAI's then-current data-retention policy. K-Research & Critic must not claim that third-party deletion succeeded when `provider_data_deleted` is not true.

## 7. Model-Training Release Gate

Before public production rollout of the Media Transcript Action, the AssemblyAI project used by this feature must be verified as opted out of provider model training or otherwise configured under terms that prohibit training on submitted media.

Until that configuration is verified, this document and the media feature remain PREVIEW / RELEASE GATE and must not be represented as a completed public privacy configuration.

## 8. User Responsibilities

Users should submit only media they are permitted to access and process. Users should avoid supplying private or confidential media through a public-URL workflow.

The initial media mode accepts public HTTPS YouTube URLs only.

## 9. Security

The GPT Action uses a dedicated server-to-server bearer secret. Users are not asked to provide the developer's AssemblyAI key or the action secret.

Secrets must not be stored in prompts, checkpoints, transcripts, repository files, or user-visible reports.

## 10. Changes

Material changes to media processors, retention, supported source types, or data use require a policy update and a new release validation before public rollout.

## 11. Contact

Project and privacy questions may be raised with the repository owner through the public GitHub project `kolemasakar/K_Research_Critic`.
