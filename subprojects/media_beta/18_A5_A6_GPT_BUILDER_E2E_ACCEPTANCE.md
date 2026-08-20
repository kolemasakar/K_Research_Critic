# MEDIA BETA A5/A6 GPT Builder End-to-End Acceptance

Version: 1.1
Status: PASS
Acceptance date: 2026-08-20

## Scope

This record captures owner/operator acceptance of the separate `K-Research & Critic - MEDIA BETA` GPT Builder configuration and the first full captions-first media workflow through the CriticProfile approval gate into the Research/Critic finalization path.

The published K-Research & Critic GPT, production VoiceBridge service, and repository `main` branches were not modified.

## Credential attribution

The owner/operator confirmed after the original acceptance that the live runs documented here used the access code designated for `Tester 1`, not the separate owner-designated code.

Therefore:
- the technical A5/A6 acceptance remains valid;
- the human operator was the owner;
- the credential exercised was the Tester 1 credential;
- this does not count as an independent external Tester 1 human rollout;
- the separate owner-designated credential has not yet been independently live-validated.

Canonical correction:
`subprojects/media_beta/21_CREDENTIAL_ATTRIBUTION_CORRECTION.md`

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
- the GPT instructed the owner/operator to use KRC MEDIA BETA Helper 0.2.2 on the same YouTube source.

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

## Manual Builder Action validation

All three GPT-facing Builder Actions were manually exercised through the Builder test interface.

Accepted operations:

```text
startMediaBetaClientTranscription        PASS
getMediaBetaClientTranscriptionStatus    PASS
getMediaBetaClientTranscriptSegments     PASS
```

The status test returned the completed captions-backed job with:

```text
status=COMPLETED
source=YouTube auto-generated captions
language=uk
segment_count=227
duration_seconds=663
stt_seconds_charged=0
```

The segment operation was then manually paginated with `limit=50` across the complete transcript:

```text
cursor=0   -> segments 0-49   -> next_cursor=50
cursor=50  -> segments 50-99  -> next_cursor=100
cursor=100 -> segments 100-149 -> next_cursor=150
cursor=150 -> segments 150-199 -> next_cursor=200
cursor=200 -> segments 200-226 -> next_cursor=null
```

Result:

`A5_BUILDER_MANUAL_3_ACTIONS_PASS`

`A5_BUILDER_MANUAL_PAGINATION_227_OF_227_PASS`

## CriticProfile gate acceptance

After the owner/operator sent `continue`, the GPT returned a DRAFT CriticProfile with:
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

## A6 owner/operator-approved end-to-end continuation

The owner/operator entered `1`.

Observed behavior:
- CriticProfile changed to `APPROVED`;
- `approved_by=user` was recorded;
- the GPT proceeded into transcript retrieval and independent verification;
- the Action segment route was invoked with pagination beginning at `cursor=0, limit=50`;
- the owner/operator allowed the Action read calls to continue;
- the owner/operator reported the full run completed successfully.

The accepted target workflow is therefore exercised through:

```text
YouTube URL
 -> beta access
 -> Builder Action creates KRCC job
 -> Helper captions-first completion
 -> GPT status/segment retrieval
 -> material claim inventory
 -> DRAFT CriticProfile
 -> explicit user APPROVE
 -> independent web research
 -> Critic/revision path
 -> finalization
```

The final completed output was owner-observed in Builder Preview. This record does not reproduce the full final report text and does not persist the full transcript or tester beta code.

## Acceptance conclusion

A5 status: PASS / COMPLETE.

A6 status: PASS / COMPLETE for the first owner-operated end-to-end captions-first Builder workflow using the Tester 1 credential.

Confirmed:
- separate beta GPT Builder identity works;
- Builder-safe instructions fit the current 8000-character field limit;
- Action authentication and OpenAPI wiring work;
- all three intended GPT-facing Action operations are recognized and manually tested;
- tester-code gate works before Action start;
- Builder-created job interoperates with Helper 0.2.2;
- captions-first path returns 227 segments with zero STT charge;
- manual segment pagination covers all 227/227 segments and terminates with `next_cursor=null`;
- CriticProfile gate blocks independent research before approval;
- standalone `1` approval transitions the profile to APPROVED;
- the workflow continues into independent Research/Critic finalization after approval;
- public GPT, production VoiceBridge, and `main` remain unchanged.

## Next phase

A7 - Controlled tester rollout.

The A7 provider privacy/EU fallback gate is separately accepted. Independent external tester evidence is still required before A7 can be marked COMPLETE.

Acceptance markers:

`A5_GPT_BUILDER_CONFIGURATION_PASS`

`A5_BUILDER_ACTION_START_PASS`

`A5_BUILDER_CAPTIONS_FIRST_PROFILE_GATE_PASS`

`A5_BUILDER_MANUAL_3_ACTIONS_PASS`

`A5_BUILDER_MANUAL_PAGINATION_227_OF_227_PASS`

`A6_OWNER_OPERATOR_E2E_USING_TESTER1_CREDENTIAL_PASS`
