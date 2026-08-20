# MEDIA BETA A5/A6 GPT Builder End-to-End Acceptance

Version: 1.0
Status: PASS
Acceptance date: 2026-08-20

## Scope

This record captures owner acceptance of the separate `K-Research & Critic - MEDIA BETA` GPT Builder configuration and the first full captions-first media workflow through the CriticProfile approval gate into the Research/Critic finalization path.

The published K-Research & Critic GPT, production VoiceBridge service, and repository `main` branches were not modified.

## A5 Builder configuration accepted

Separate GPT name:

`K-Research & Critic - MEDIA BETA`

Accepted Builder configuration:
- dedicated MEDIA BETA identity;
- Builder-safe instructions from `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
- web search enabled;
- image generation disabled;
- code interpreter/data analysis enabled;
- Action authentication configured as API key / Bearer using the beta backend Action secret;
- OpenAPI schema from `gpt_store/actions/media_beta_openapi.yaml`;
- Action server restricted to `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`;
- privacy policy field configured with the repository privacy-policy URL;
- three Action operations recognized by Builder:
  - `startMediaBetaClientTranscription`;
  - `getMediaBetaClientTranscriptionStatus`;
  - `getMediaBetaClientTranscriptSegments`.

The Builder instructions correctly enforced `MEDIA BETA ACCESS REQUIRED` before starting a media Action without a tester code.

## A5 live Action start test

Accepted Builder-created job:

`KRCC_8945357e-d6cf-4483-b7ca-178b81729665`

Observed Builder behavior:
- capability preflight reported `web_search=AVAILABLE`;
- media preflight reported `media_transcript=AVAILABLE`;
- the Action created a client-assisted job;
- returned state was `AWAITING_CLIENT`;
- the GPT instructed the owner to use KRC MEDIA BETA Helper 0.2.2 on the same YouTube source.

## Captions-first Helper completion

The same Job ID was used in Helper 0.2.2.

Accepted Helper result:

```text
status=COMPLETED
transcript_source=youtube_captions
caption_type=auto_generated
language=uk
segment_count=227
stt_seconds_charged=0
provider_cleanup=not applicable
```

This confirms the Builder-created job interoperates with the already accepted browser-helper captions path without consuming AssemblyAI STT quota.

## CriticProfile gate acceptance

After the owner sent `continue`, the GPT returned a DRAFT CriticProfile with:
- `status=REVIEW_REQUIRED`;
- medicine/nutrition/history domain classification;
- `risk_level=CRITICAL` because material medical claims were present;
- source hierarchy and cross-check requirements;
- explicit transcript/caption uncertainty handling;
- timestamp-to-claim traceability requirement;
- `approved_by=null` and `approved_at=null` before approval.

The GPT also identified a compact inventory of material claims from the video and explicitly stated that the transcript came from YouTube auto-generated captions and that STT fallback was not used.

The response stopped at the mandatory gate:

`1 - APPROVE, 2 - EDIT, 3 - REJECT`

No independent factual verification was performed before approval.

## A6 owner-approved end-to-end continuation

The owner entered `1`.

Observed behavior:
- CriticProfile changed to `APPROVED`;
- `approved_by=user` was recorded;
- the GPT proceeded into transcript retrieval and independent verification;
- the Action segment route was invoked with pagination beginning at `cursor=0, limit=50`;
- the owner allowed the Action read calls to continue;
- the owner reported the full run completed successfully.

The accepted target workflow is therefore exercised through:

```text
YouTube URL
 -> beta access
 -> Builder Action creates KRCC job
 -> Helper captions-first completion
 -> GPT status/segment retrieval
 -> material claim inventory
 -> DRAFT CriticProfile
 -> explicit owner APPROVE
 -> independent web research
 -> Critic/revision path
 -> finalization
```

The final completed output was owner-observed in Builder Preview. This record does not reproduce the full final report text and does not persist the full transcript or tester beta code.

## Acceptance conclusion

A5 status: PASS / COMPLETE.

A6 status: PASS / COMPLETE for the first owner end-to-end captions-first Builder workflow.

Confirmed:
- separate beta GPT Builder identity works;
- Builder-safe instructions fit the current 8000-character field limit;
- Action authentication and OpenAPI wiring work;
- all three intended GPT-facing Action operations are recognized;
- tester-code gate works before Action start;
- Builder-created job interoperates with Helper 0.2.2;
- captions-first path returns 227 segments with zero STT charge;
- CriticProfile gate blocks independent research before approval;
- standalone `1` approval transitions the profile to APPROVED;
- the workflow continues into independent Research/Critic finalization after approval;
- public GPT, production VoiceBridge, and `main` remain unchanged.

## Next phase

A7 - Controlled tester rollout.

Before broader/public promotion, separate release-hardening gates remain, including provider privacy/no-training verification, hard-process-loss orphan cleanup strategy, Free-plan/paid runtime compatibility, and Postgres lifecycle planning.

Acceptance markers:

`A5_GPT_BUILDER_CONFIGURATION_PASS`

`A5_BUILDER_ACTION_START_PASS`

`A5_BUILDER_CAPTIONS_FIRST_PROFILE_GATE_PASS`

`A6_OWNER_E2E_RESEARCH_CRITIC_FINALIZATION_PASS`
