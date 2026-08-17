# PRIVACY_POLICY
Політика конфіденційності додаткового режиму обробки відеопосилань у K-Research & Critic.

Version: 0.2
Status: CLOSED BETA / PREVIEW / RELEASE GATE
Effective candidate date: 2026-08-17

## 1. Scope

This policy applies to the optional Media Transcript Action used by K-Research & Critic to obtain source text from a public video URL.

The normal text research workflow does not require this external media service.

The current rollout is a closed beta for a small tester group. The published production GPT remains separate and unchanged.

## 2. Data Sent to the Media Service

When the user explicitly provides a supported public media URL for analysis, the media path may process:

- the supplied public media URL;
- a closed-beta tester access code used only for allowlist authorization;
- public video metadata such as title, channel, duration, and canonical URL;
- YouTube caption data when usable source-language captions are available;
- audio derived from the public video only when speech-to-text fallback is required;
- transcript text, timestamps, language information, and transcription confidence;
- technical request/job identifiers needed to operate the service.

Unrelated ChatGPT conversation content must not be sent to the Media Transcript service.

## 3. Closed-Beta Access Code

The beta tester code is separate from the GPT Action bearer secret and from provider API keys.

VoiceBridge hashes configured beta codes for comparison and does not place the submitted code into media job state. The beta GPT must not echo, quote, include, or store the tester code in reports or checkpoints.

The tester code should be treated as a limited beta credential. If it is disclosed, it should be replaced in the VoiceBridge environment configuration.

## 4. Processing Services

The closed beta uses:

- VoiceBridge Cloud as the media-ingestion adapter;
- YouTube captions as the preferred transcript source when suitable source-language captions are available;
- AssemblyAI as the speech-to-text fallback provider only when captions are not available;
- the source media platform, initially YouTube, to retrieve the public media selected by the user.

Third-party processing is also subject to the applicable provider privacy, security, and data-processing terms.

## 5. Data Minimization

The media path is subtitle-first.

If usable captions are available, VoiceBridge does not need to send video audio to AssemblyAI for that job.

If STT fallback is required, VoiceBridge converts source audio to speech-oriented mono audio at 16 kHz and approximately 32 kbps before upload. This reduces provider transfer volume and transient memory/network use.

Media data is processed only to obtain a transcript, identify statements for verification, and preserve timestamps/confidence for traceability.

The transcript itself is not treated as independent evidence that a factual claim is true.

## 6. VoiceBridge Retention

The closed-beta configuration follows these rules:

- downloaded media is stored only in a temporary working directory;
- the temporary media directory is deleted after the transcription attempt finishes;
- completed transcript segments and job metadata are held in process memory only;
- the default in-memory job retention is one hour;
- the media route does not intentionally write transcript content or tester access codes to the VoiceBridge database or operational logs;
- the full transcript and tester access code are not stored in K-Research & Critic checkpoints.

A server restart may remove in-memory jobs earlier.

The daily beta STT usage counter is also in process memory. A restart may reset that safety counter; this is acceptable for the trusted closed beta but is not sufficient as a future public anti-abuse mechanism.

## 7. Speech-to-Text Provider Deletion

After the transcript result has been obtained, VoiceBridge requests deletion of the corresponding AssemblyAI transcript. AssemblyAI documents that deleting a transcript also deletes an audio file uploaded through its upload endpoint.

The media job exposes `provider_data_deleted` so the service can distinguish successful provider deletion from a cleanup failure.

If provider deletion fails, provider-side retention is governed by AssemblyAI's then-current data-retention policy. K-Research & Critic must not claim that third-party deletion succeeded when `provider_data_deleted` is not true.

For YouTube-caption jobs, `provider_data_deleted` may be null because AssemblyAI was not used.

## 8. Resource Limits

The closed beta intentionally limits shared external-resource use:

- maximum video duration: 60 minutes;
- maximum concurrent media jobs: 1;
- global AssemblyAI fallback budget: 7200 seconds per UTC day;
- caption-backed jobs do not consume the STT budget.

These limits are beta safety controls and may change after measured testing.

## 9. Model-Training Release Gate

Before public production rollout of the Media Transcript Action, the AssemblyAI project used by this feature must be verified as opted out of provider model training or otherwise configured under terms that prohibit training on submitted media.

Until that configuration is verified, this document and the media feature remain PREVIEW / RELEASE GATE and must not be represented as a completed public privacy configuration.

## 10. User Responsibilities

Users should submit only media they are permitted to access and process. Users should avoid supplying private or confidential media through a public-URL workflow.

The initial media mode accepts public HTTPS YouTube URLs only.

## 11. Security

The GPT Action uses a dedicated server-to-server bearer secret. Users are not asked to provide the developer's AssemblyAI key or the action bearer secret.

The closed-beta tester code is an access-control credential, not a provider API key.

Developer/provider secrets must not be stored in prompts, checkpoints, transcripts, repository files, or user-visible reports.

## 12. Changes

Material changes to media processors, retention, supported source types, access controls, or data use require a policy update and a new release validation before public rollout.

## 13. Contact

Project and privacy questions may be raised with the repository owner through the public GitHub project `kolemasakar/K_Research_Critic`.
