# Sustainable Free Media Target
Цільова архітектура після закритої beta для мінімізації постійних платних або одноразово вичерпних зовнішніх ресурсів.

Version: 1.0
Status: PLANNED_AFTER_CLOSED_BETA
Updated: 2026-08-17

## 1. Objective

Preserve the user experience:

`paste YouTube URL -> receive K-Research & Critic analysis`

while removing AssemblyAI free credits as a mandatory long-term dependency.

The target is sustainable free operation, not a claim of literally unlimited capacity.

## 2. Target routing

```text
YouTube URL
   |
   v
Transcript Router
   |
   +--> usable source-language captions?
   |       |
   |       +--> YES -> normalized timestamped transcript
   |
   +--> NO -> renewable free cloud STT available?
           |
           +--> YES -> Cloudflare Workers AI Whisper
           |
           +--> NO -> owner-controlled local Whisper fallback

Normalized transcript
   -> existing K-Research & Critic claim workflow
```

## 3. Layer 1 - Captions

Priority: highest.

Advantages:

- no STT provider minutes;
- minimal Render outbound traffic;
- low latency;
- timestamps often directly available;
- no audio upload to STT provider.

Risks:

- captions may be absent;
- auto-captions can contain errors;
- YouTube extraction behavior can change;
- yt-dlp/YouTube PO-token and anti-bot changes remain an operational risk.

Requirement:

Always preserve transcription uncertainty and independently verify material names/numbers/dates when relevant.

## 4. Layer 2 - Cloudflare Workers AI Whisper

Purpose:

Renewable free cloud fallback before local compute.

Candidate models:

- `@cf/openai/whisper`;
- `@cf/openai/whisper-large-v3-turbo`.

Why considered:

- daily renewable Workers AI allocation rather than one-time STT credit;
- multilingual Whisper family;
- suitable for UK/RU/EN PoC;
- supports a path toward chunked longer-audio processing.

Beta-to-target validation required:

- current free quota must be re-verified before implementation;
- audio request/file limits must be checked;
- timestamp support and output contract must be validated;
- quality must be compared with AssemblyAI on the same media sample;
- actual daily capacity must be measured.

## 5. Layer 3 - Local Whisper fallback

Purpose:

Remove cloud STT quota as a hard final dependency.

Candidates:

- faster-whisper;
- whisper.cpp.

Possible topology:

```text
GPT Action / media router
    -> secure public HTTPS endpoint
    -> owner-controlled Windows/Linux media node
    -> yt-dlp / audio preprocessing
    -> local Whisper
    -> normalized transcript
```

Advantages:

- no STT API billing;
- no external STT minute quota;
- audio can remain on owner-controlled hardware after download;
- compute capacity can later be upgraded independently.

Limits:

- PC must be available;
- CPU/GPU speed limits throughput;
- electricity and Internet remain real costs/resources;
- public endpoint security and availability must be engineered;
- source-platform limits still apply.

## 6. Provider-neutral transcript contract

K-Research & Critic should not care whether transcript came from captions, AssemblyAI, Cloudflare, or local Whisper.

Normalized job metadata should expose at minimum:

```text
job_id
status
source_url
transcript_source
provider
provider_model
detected_language
language_confidence
media metadata
segment_count
transcript_characters
resource/quota diagnostics when applicable
error
```

Normalized segment:

```text
index
start_ms
end_ms
text
confidence
```

## 7. Migration strategy

Do not replace AssemblyAI during the first beta.

Recommended migration:

1. complete closed beta with AssemblyAI baseline;
2. build Cloudflare Whisper PoC;
3. compare transcript quality/latency/resource use;
4. introduce provider-neutral routing;
5. build local Whisper PoC;
6. add fallback routing;
7. rerun all media claim-research acceptance tests;
8. remove AssemblyAI as mandatory public dependency only after equivalence is demonstrated.

## 8. Success criteria

The sustainable free architecture is successful when:

- common caption-backed videos require no STT API;
- non-caption videos normally use renewable free cloud quota;
- exhaustion of cloud STT quota has a practical local fallback;
- no user provider API key is required;
- the same GPT workflow and claim-verification quality are preserved;
- production resource consumption is measurable and bounded;
- failure of any STT route degrades gracefully without corrupting text-mode research.