# KRC MEDIA — R3 Builder Preview Regression Plan — 2026-09-16
План фіксує точний порядок preview-перевірки після стабільного відкриття Builder/editor; публікація та production-активація не входять у цей етап.

Status: PREPARED / EXECUTION_WAITING_FOR_STABLE_BUILDER_ENTRY / PUBLICATION_HOLD

## Preconditions

- Owner approval covers Builder Preview only.
- `K-Research & Critic` is opened in the authenticated owner Builder session.
- Capture read-only snapshot of current Instructions, Actions and visible configuration before any edit.
- Core instructions are `prompts/GPT_STORE_INSTRUCTIONS.md` and must not be replaced.
- Candidate Action is `gpt_store/actions/media_public_r3_openapi.yaml`.
- Candidate addendum is `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`.
- No Render change, `main` merge, PR #22 merge or VoiceBridge PR #45 merge is allowed.

## Builder integration order

1. Confirm current public KRC identity and Core configuration from the read-only snapshot.
2. Import the R3 OpenAPI schema as the MEDIA Action using the existing authorized bearer configuration; never expose the bearer value in evidence.
3. Append the R3 MEDIA addendum to the existing Core instructions; do not rewrite or replace Core.
4. Confirm the Builder accepts the combined instructions and schema without requiring Publish/Update.
5. Run the preview regressions below.
6. Record results and STOP before Publish/Update.

## Regression matrix

### Core isolation

- Run an ordinary non-media KRC fact-check/research request.
- Expected: normal Core flow works; MEDIA Action is not required.
- Any MEDIA failure must not block Core.

### YouTube

- Use a supported public YouTube test URL selected at execution time.
- Run Gemini Free preflight first.
- Expected before provider work: data-use notice returned and explicit user approval required.
- Without approval: no start.
- With explicit approval: send `gemini_free_consent`; use Gemini Free direct only.
- Confirm no Cobalt, AssemblyAI, paid Gemini, Supadata, ScrapeCreators, cookies/login or paid proxy fallback.

### Instagram

- Preferred accepted control: `https://www.instagram.com/reel/DF1CIrPSVmf/` if still publicly available.
- Expected route: self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon state.
- Confirm no paid/Supadata/ScrapeCreators/cookie/login fallback.

### Facebook

- Preferred accepted control: `https://www.facebook.com/reel/636216875539019` if still publicly available.
- Expected route: Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2.
- The unsupported Cobalt only-audio route must not become canonical.

### Telegram

- Success control: `https://t.me/techcrimes/12107` if still publicly available.
- Failure/retry fixture: `https://t.me/techcrimes/12101`.
- Expected route: public Telegram web -> AssemblyAI universal-2.
- `COMPLETED` and in-flight `PROCESSING` reuse durable state.
- A prior `FAILED` free-only job may create a fresh deterministic job only on a new explicit retry request; never auto-loop.
- Paid or `credit_charge_uncertain` replay remains blocked.

## Evidence to capture

For every preview case record only non-secret evidence:
- platform and test URL;
- operation/route selected;
- status and provider mode;
- retrieval provider;
- retrieval credits / paid credits where returned;
- `credit_charge_uncertain` where returned;
- transcript presence/segment count where applicable;
- Core health/isolation result;
- whether any unexpected fallback appeared.

Never store bearer tokens, API keys, signed media URLs, Browser Context Profile identifiers, cookies or session material in repository evidence.

## Immediate STOP conditions

Stop the preview and make no further Builder mutation if any of the following occurs:
- Builder requires Publish/Update to continue preview integration;
- current Core instructions cannot be preserved exactly as the base instruction set;
- Action auth cannot be confirmed without exposing or replacing secrets;
- any route attempts paid retrieval/STT/proxy or an unapproved fallback;
- `credit_charge_uncertain=true` appears on a replay path;
- YouTube attempts Cobalt or AssemblyAI fallback;
- Facebook attempts to make Cobalt only-audio the canonical route;
- Core service becomes unavailable because of MEDIA;
- any unexpected Render, `main`, PR #22 or PR #45 mutation is required.

## Release boundary

```text
PUBLICATION=HOLD
PUBLIC_GPT_CHANGE=PREVIEW_ONLY
RENDER_CHANGE=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
STOP_BEFORE_PUBLISH_UPDATE=TRUE
```
