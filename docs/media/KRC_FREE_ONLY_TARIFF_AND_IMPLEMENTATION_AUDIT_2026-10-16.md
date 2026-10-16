# FREE_ONLY tariff and implementation audit — 2026-10-16

## Scope and verdict
Read-only source/configuration-policy audit of VoiceBridge live revision65737cfb7e3a89bdaaed95bdf5519d65abae0acf; clean local checkout. Public official documents retrieved2026-10-16. No provider execution, billing changes, credential access, production deploy or code changes in this audit.
Verdict: FREE_ONLY_INTENT=IMPLEMENTED; PROVIDER_BILLING_ENFORCEMENT=NOT_VERIFIED; YOUTUBE_ADMISSION_COVERAGE=FAIL; OVERALL=PARTIAL.
Earlier credits_charged=0 statements refer to KRC fields, not independently verified provider billing.

## Provider policy
- Gemini active model from capabilities: gemini-3.8-flash. Official Standard pricing: Free Tier input/output free; paid input$0.75/M tokens and output$3.75/M through2026-12-31, scheduled$1.50/$7.50 from2027-01-01. YouTube URL ingestion is separately described as preview at no charge; this does not establish all processing free on an arbitrary paid project. Free-tier content can be used to improve Google products.
- Gemini limits: RPM,TPM,RPD,per project rather than key; RPD resets midnight Pacific. Live account values only in AI Studio, not verified here. Public YouTube only, not unlisted/private; up to8hours/day on Free Tier. Supplied request matches documented Interactions REST video URI schema.503 service_unavailable is not proof of quota exhaustion or social login requirement.
- Gemini billing tier belongs to project/billing account, not an API request flag. Setting our boolean true does not downgrade a paid project. Actual project tier/billing linkage unverified.
- AssemblyAI async Universal-2 is$0.15/hour. New direct accounts get$50 nonexpiring free credits, finite allocation, not a monthly renewal. No-card/no-autopay accounts pause on exhausted balance. Auto-pay can charge a card; actual account balance, plan, paid deposits and auto-pay not verified. No dashboard session was accessed.
- AssemblyAI successful prerecorded STT consumes balance based on processed duration; failed transcriptions not charged per docs. For the tested167.275938s Facebook file, base-rate arithmetic is about$0.00697, roughly0.7US cent, deducted from whichever eligible balance funds the account. This is an estimate, not an invoice. Internal168s reservation is conservative rounding.
- Self-hosted Cobalt has no separate metered retrieval-provider call in this route; local repository license AGPL-3.0. Hosting/network resources remain distinct; no account-wide infrastructure-billing audit claimed.

## Implementation findings
1. HIGH: public_gemini_youtube.ts provider configured=Boolean(apiKey && freeTierOnly); free-tier flag comes from environment. No account billing verification or model tariff allowlist (model only regex validated). It is a declared policy, not a provider-enforced free tier.
2. HIGH: public_media_admission.ts only matches /api/v1/media/managed/transcriptions. Actual Gemini route is /api/v1/media/youtube-gemini/transcriptions; managed_server.ts calls admission first, but this path returns no lease. Thus its60RPM ceiling,1/sec spacing and single-request concurrency cap do not cover YouTube. Offline executable reproduction with compiled module:
   managed POST => managed=true,providerStart=true;
   youtube-gemini POST => managed=false,providerStart=false.
   No network/provider work in reproduction.
3. HIGH: YouTube start has no local RPM/TPM/RPD/video-duration ledger; no reservation of Google's8h/day YouTube allowance. It sends one public URI with120s fetch timeout. Missing output-token cap and token-usage accounting. Provider quotas remain ultimate upstream limits.
4. HIGH reporting: credits_charged=0,credits_remaining_estimate=0,credit_charge_uncertain=false are initialized constants in public job views. These are not queried provider financial balances. Provider monetary consumption can coexist with KRC credits0. Do not present them as verified no-charge evidence.
5. AssemblyAI: KRC_MEDIA_ASSEMBLYAI_FREE_TRIAL_ONLY is a required declaration in public mode, not an account entitlement query. Media provider checks presence of key; model universal-2 is pinned; reviewed async submits use formatting,punctuation and optional language detection, no diarization/medical add-ons. Provider balance/auto-pay not verified.
6. Positive: public mode requires free-tier declarations, rejects SCRAPECREATORS_API_KEY; paid retrieval fallback disabled. Non-YouTube duration-based STT reservation uses durable store when available and fails closed on store errors. Public configured STT daily ceiling7200s,default7200s,UTC day. This is a consumption cap, not financial proof, and does not apply to Gemini YouTube video hours.
7. Other limits: MEDIA_MAX_DURATION_SECONDS default3600,range60..21600; explicit enforcement confirmed in attachment pipeline, not a universal YouTube duration guard. Job TTL default3600s,range300..86400; TTL can explain some historical absence but specific404 cause remains unproven.
8. Retry handling deduplicates an active same-process same-source job, but failed starts can create successive jobs; no provider backoff/Retry-After scheduler in Gemini transcribe. No automatic provider retry loop. inFlight is process-local; don't claim distributed concurrency protection.

## Required follow-up
- Before more free-only acceptance starts, verify sanitized account-level facts: Gemini project Free and no billable project linkage for this key; AssemblyAI remaining free grant, no paid balance use/auto-pay. Never expose keys or card details.
- Extend admission coverage and dedicated E1 token coverage; add meaningful HTTP-level tests before rollout.
- Add bounded Gemini request/video/token accounting aligned with provider reset rules; unknown duration must have explicit bounded policy.
- Separate KRC credits from provider monetary/balance estimates; represent unknown provider cost as unknown.
- Document finite AssemblyAI grant exhaustion stop and periodically revalidate free eligibility. Do not switch models or paid plans automatically.
No fixes deployed by this report. Instagram PAUSED; Telegram LIVE BLOCKED; PUBLIC HOLD.

## Primary sources
https://ai.google.dev/gemini-api/docs/pricing
https://ai.google.dev/gemini-api/docs/billing
https://ai.google.dev/gemini-api/docs/rate-limits
https://ai.google.dev/gemini-api/docs/video-understanding
https://www.assemblyai.com/pricing
https://www.assemblyai.com/docs/billing-and-pricing

## Source files
VoiceBridge/src/cloud/src/public_gemini_youtube.ts
VoiceBridge/src/cloud/src/public_media_admission.ts
VoiceBridge/src/cloud/src/managed_server.ts
VoiceBridge/src/cloud/src/config.ts
VoiceBridge/src/cloud/src/media_beta.ts
VoiceBridge/src/cloud/src/public_cobalt_media.ts
VoiceBridge/src/cloud/src/media_transcription_provider.ts
VoiceBridge/src/cloud/src/facebook_managed_pipeline.ts
VoiceBridge/src/cloud/src/telegram_managed_pipeline.ts
VoiceBridge/src/cloud/src/attachment_managed_pipeline.ts
