# MEDIA BETA A7 Controlled Tester Rollout

Version: 1.1
Status: READY_FOR_TESTER1
Updated: 2026-08-20

## Purpose

Prepare and control the first external closed-beta tester rollout after owner A5/A6 acceptance while preserving the production/public isolation boundary.

The rollout remains limited to the owner plus up to three invited testers. The public K-Research & Critic GPT, VoiceBridge production service, `main` branches, and draft PR merge state remain unchanged.

## Current rollout gate

Owner Builder captions-first end-to-end flow is accepted.

Both controlled tester media paths are now READY:

1. `CAPTIONS_FIRST` - READY and preferred.
2. `AUDIO_FALLBACK` - READY after AssemblyAI EU/no-training deployment and live validation.

Canonical EU acceptance:
`subprojects/media_beta/20_A7_EU_AUDIO_PRIVACY_GATE_ACCEPTANCE.md`

## AssemblyAI privacy boundary

The isolated MEDIA BETA client-assisted Audio fallback is configured with:

`KRC_MEDIA_ASSEMBLYAI_BASE_URL=https://api.eu.assemblyai.com`

The accepted isolated deployment used VoiceBridge commit:

`7a61790221b6f75c14293360002794208efd813f`

Render deploy:

`dep-da3f2te417fc73e600ng`

Current AssemblyAI documentation states that files submitted through its European servers are not used for model training. The live EU fallback acceptance completed successfully with Universal-2 and provider deletion confirmed.

Accepted EU job:

`KRCC_a79ad701-d5a0-40ca-91f8-6fbdfc6c3bc6`

Accepted result:

```text
status=COMPLETED
transcript_source=assemblyai_stt
provider=assemblyai
provider_model=universal-2
provider_data_deleted=true
detected_language=uk
duration_seconds=122.292
stt_seconds_charged=123
segment_count=3
error=null
```

Quota validation:

```text
used before=422
used after=545
delta=123
stt_seconds_charged=123
```

Production VoiceBridge was not targeted.

## Tester prerequisites

Each invited tester receives only:
- unlisted `K-Research & Critic - MEDIA BETA` GPT link;
- one unique tester beta code;
- KRC MEDIA BETA Helper 0.2.2 installation package/instructions;
- short operating procedure;
- failure-report template.

Never provide testers:
- `KRC_MEDIA_ACTION_TOKEN`;
- `ASSEMBLYAI_API_KEY`;
- `RENDER_API_KEY`;
- Render dashboard access;
- another tester's beta code.

## Tester operating procedure

1. Open the beta GPT through the private/unlisted link.
2. Send a public YouTube URL and request analysis/fact-check/research.
3. When requested, provide the assigned tester beta code in that chat only.
4. The GPT creates a `KRCC_...` job and returns the Job ID.
5. Open the same YouTube video in Chrome or Edge.
6. Open KRC MEDIA BETA Helper 0.2.2.
7. Enter the KRCC Job ID and assigned tester code.
8. Press `Use subtitles` first.
9. If subtitles complete successfully, return to the beta GPT and send `continue`.
10. If captions are unavailable/unusable, use `Audio fallback`, capture only the intended YouTube tab at normal speed, then wait for completion.
11. Return to the beta GPT and send `continue`.
12. Review the DRAFT CriticProfile.
13. Use `1 / APPROVE`, `2 / EDIT`, or `3 / REJECT`.
14. On approval, allow Research -> Critic -> final output to complete.

## Minimum Tester 1 matrix

Tester 1 should complete at least:
- one Ukrainian auto-caption video;
- one additional public YouTube video selected independently by the tester;
- one normal CriticProfile approval flow;
- one EDIT or REJECT gate interaction if practical;
- Audio fallback only when captions are unavailable/unusable, not merely to consume STT quota.

At least one controlled external tester should eventually complete an Audio fallback case before A7 is closed, if a suitable captions-unavailable source is encountered during the tester window.

## Failure report template

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
- AssemblyAI Audio fallback remains routed through the accepted EU path when used;
- observed reliability/resource use is acceptable for continuing the closed beta.

## Current decision

`A7_CAPTIONS_FIRST_TESTER_ROLLOUT_READY`

`A7_EU_AUDIO_FALLBACK_PRIVACY_GATE_PASS`

`A7_TESTER1_READY`
