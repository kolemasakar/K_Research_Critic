# PRIVACY_POLICY
Політика конфіденційності додаткового режиму обробки відеопосилань у K-Research & Critic.

Version: 0.6
Status: CLOSED BETA / A7 CONTROLLED TESTER ROLLOUT
Effective candidate date: 2026-08-20

## 1. Scope

This policy applies to the optional Media Transcript Action and the separate closed-beta browser helper used by K-Research & Critic to obtain source text from a public video URL.

The normal text research workflow does not require this external media service.

The current rollout is a closed beta for a small tester group. The published production GPT and the validated production VoiceBridge translation extension remain separate and unchanged.

## 2. Current Data Flow

The direct Render/datacenter YouTube-download path is not the current beta acceptance path because live testing confirmed YouTube anti-bot blocking from that cloud ingress.

The current client-assisted flow is captions-first:

```text
public YouTube URL
 -> beta GPT creates durable KRCC_ job
 -> separate KRC MEDIA BETA Helper 0.2.2 on the same active YouTube tab
 -> helper first attempts to read the YouTube caption track and timestamps through the tester browser
    -> if usable: timestamped caption text is uploaded to isolated VoiceBridge MEDIA BETA
    -> no AssemblyAI transcription is invoked
 -> if captions are unavailable/unusable:
    -> helper captures audio from the same active YouTube tab
    -> helper uploads captured audio to isolated VoiceBridge MEDIA BETA
    -> VoiceBridge normalizes audio for speech transcription
    -> AssemblyAI EU async transcription through https://api.eu.assemblyai.com
 -> timestamped transcript returned to K-Research & Critic
```

A reliable transcript/caption already available through current built-in/web capabilities may still be preferred without using the browser helper.

## 3. Data Processed by the Media Path

The path may process:

- the public YouTube URL supplied by the user;
- a closed-beta tester access code used for authorization and client-job ownership;
- technical request/job identifiers;
- the active-tab YouTube URL sent by the helper for same-source validation;
- YouTube caption-track metadata and timestamped caption text when the captions-first path succeeds;
- compressed audio captured from the active YouTube tab only when audio fallback is used;
- derived duration and quota metadata for audio fallback;
- transcript text, timestamps, detected/source language information, caption type, and transcription confidence where applicable.

Unrelated ChatGPT conversation content must not be sent to the Media Transcript service.

## 4. Closed-Beta Access Code

The beta tester code is separate from the GPT Action bearer secret and provider API keys.

The beta GPT must never echo, quote, summarize, include, or store the tester code in reports or checkpoints.

The backend does not persist the plaintext tester code. It stores a one-way SHA-256 digest with the durable client job to enforce per-tester job ownership.

The current developer-mode browser helper may store the tester code in that extension's local browser storage for closed-beta convenience. This is a beta-only local credential convenience and must be reviewed before any public extension distribution. Testers should use the helper only on a trusted browser profile/device.

If a tester code is disclosed, it should be replaced in the VoiceBridge beta environment configuration.

## 5. Processing Services

The current beta path uses:

- the separate KRC MEDIA BETA browser helper for caption extraction and optional active-tab audio capture on the tester device/network path;
- the isolated VoiceBridge MEDIA BETA service as the media-ingestion adapter;
- isolated Postgres storage for durable media-job state and STT charge accounting;
- YouTube as the public source and caption source viewed by the tester in their browser;
- AssemblyAI Universal-2 only when browser captions are unavailable/unusable and audio fallback is invoked;
- the AssemblyAI European Async STT endpoint `https://api.eu.assemblyai.com` for the accepted closed-beta Audio fallback path.

Current AssemblyAI documentation states that files submitted through its European servers are not used for model training. The isolated MEDIA BETA EU routing was live-validated on 2026-08-20 before enabling external-tester Audio fallback.

Third-party processing remains subject to applicable provider privacy, security, data-processing, and service terms. Provider terms/configuration must be re-checked before any future public production promotion.

## 6. Data Minimization

The helper prefers timestamped caption text over audio.

When captions are usable:
- no video frames are captured;
- no browser audio is uploaded;
- AssemblyAI is not called;
- `stt_seconds_charged=0`;
- only the selected caption language/type, timestamped text segments, active source URL, tester authorization code, and job metadata are sent to the isolated beta backend.

When audio fallback is required:
- the helper captures audio only, not video frames;
- the helper records Opus audio at approximately 32 kbps and uploads only after the tester stops capture;
- VoiceBridge normalizes the uploaded audio to speech-oriented mono 16 kHz audio at approximately 32 kbps for provider transcription;
- the accepted closed-beta provider request is routed through the AssemblyAI EU endpoint.

The helper validates that the active tab is YouTube. The backend checks that the active-tab source identifies the same YouTube video as the KRCC job before accepting captions or audio.

Current closed-beta limits include a 32 MiB client-audio upload guard, a 60-minute source/captured-audio limit, and bounded caption segment/text payloads.

Media data is processed only to obtain source text, preserve timestamps/source metadata for traceability, and enable later claim verification after CriticProfile approval.

The transcript itself is not treated as independent evidence that a factual claim is true.

## 7. VoiceBridge, Postgres, and Browser Retention

The closed-beta configuration follows these rules:

- caption text is read in the browser and sent to the beta backend only when the tester invokes the captions action;
- captured audio is buffered temporarily by the helper only when audio fallback is used and only until upload/Stop completes;
- backend uploaded/normalized audio is written only to a runtime temporary working directory and is not intended as durable storage;
- client job payload and transcript segments are stored in the isolated Postgres durable store so waiting/completed jobs remain readable across beta process replacement;
- the default job TTL is approximately one hour; expired job rows are excluded from normal reads and are deleted by the beta purge routine;
- plaintext tester access codes are not stored in durable job records; only a one-way ownership digest is stored;
- STT charge records are stored in a separate durable quota ledger keyed by job and UTC day;
- old STT charge ledger rows are purged after their short operational retention window; current code removes charge rows older than two days;
- the full transcript and tester access code are not stored in K-Research & Critic checkpoints.

The browser helper currently stores endpoint, job ID, and tester code in extension local storage. The tester may remove this local beta data by removing/resetting the helper extension or clearing its extension storage.

A beta web-process restart no longer resets waiting-job state or the current-day STT accounting because those states are restored from the isolated Postgres store while still within their applicable retention windows.

## 8. Speech-to-Text Provider Deletion

This section applies only when audio fallback invokes AssemblyAI.

After an AssemblyAI transcript result is obtained during normal completion, VoiceBridge requests deletion of the corresponding provider transcript. AssemblyAI documents that deleting a transcript also deletes audio uploaded through its upload endpoint.

The media job exposes `provider_data_deleted` so the service can distinguish successful provider deletion from a cleanup failure.

For `transcript_source=youtube_captions`, `provider_data_deleted=null` is normal because no AssemblyAI transcript was created.

The accepted A7 EU Audio fallback live job completed with `provider_data_deleted=true`.

A hard beta process loss while AssemblyAI transcription is active can leave `provider_data_deleted=null` because the killed process cannot complete or record the provider-delete request. The durable KRCC job then returns `MEDIA_CLIENT_INTERRUPTED_RETRY_REQUIRED` and must not be resumed. Provider-side orphan cleanup after such hard process loss remains a separate release-hardening item.

If AssemblyAI provider deletion fails or cannot be confirmed, provider-side retention is governed by AssemblyAI's then-current data-retention policy. K-Research & Critic must not claim third-party deletion succeeded when `provider_data_deleted` is not true.

## 9. Resource Limits

The current closed beta intentionally limits shared external-resource use:

- maximum source/captured audio duration: 60 minutes;
- maximum concurrent client media jobs: 1;
- maximum helper audio upload: 32 MiB;
- global AssemblyAI budget: 7200 seconds of captured audio per UTC day;
- captions-first ingestion uses `0` AssemblyAI STT seconds;
- audio fallback uses the STT budget;
- direct reliable transcript/caption intake that does not invoke AssemblyAI does not use this beta STT budget;
- STT charge accounting is durable across beta process replacement and does not intentionally double-charge an interrupted job on recovery.

These are beta safety controls and may change only through an explicit project decision.

## 10. Model-Training Gate

For the current controlled beta, the AssemblyAI-backed fallback path is configured to the provider's European Async STT endpoint:

`https://api.eu.assemblyai.com`

Current AssemblyAI documentation states that files submitted through its European servers are not used for model training.

The isolated MEDIA BETA EU routing was live-validated on 2026-08-20 with a normal completed Audio fallback job, measured quota accounting, and provider deletion confirmation. This closes the A7 provider-routing/model-training gate for controlled external beta testing.

This is not a permanent public-release waiver. Before any future public production rollout, the provider's then-current terms, endpoint behavior, retention, data-use rules, account configuration, and applicable privacy requirements must be verified again.

## 11. User Responsibilities

Users should submit only media they are permitted to access and process. Users should avoid private or confidential media in this public-URL beta workflow.

The initial media mode supports public HTTPS YouTube URLs only.

Testers should invoke `Use subtitles` only on the intended source tab. If audio fallback is required, testers should capture only the intended YouTube tab and stop capture when the relevant source content ends.

## 12. Security

The GPT Action uses a dedicated server-to-server bearer secret. The browser helper never receives that Action secret or the AssemblyAI API key.

The helper authenticates browser caption/audio/status requests with the closed-beta tester code and sends the active-tab source URL so the backend can enforce same-video matching.

Caption extraction is user-initiated and uses the active YouTube tab. It relies on best-effort access to YouTube player caption metadata; those player internals are not a stable public API.

Developer/provider secrets must not be stored in prompts, checkpoints, transcripts, repository files, browser-helper fields, or user-visible reports.

Personal YouTube account cookies are not part of the approved beta architecture.

## 13. Changes

Material changes to media processors, browser-helper behavior, retention, supported source types, access controls, data residency, or data use require a policy update and new release validation before public rollout.

## 14. Contact

Project and privacy questions may be raised with the repository owner through the public GitHub project `kolemasakar/K_Research_Critic`.
