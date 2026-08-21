# A9.5 Private GPT Zero-Client E2E Acceptance

Version: 1.0
Status: PASS / COMPLETE
Accepted: 2026-08-21

## Scope

This record closes the private owner-only YouTube zero-client acceptance gate for `K-Research & Critic - MEDIA BETA`.

Acceptance was executed from the actual private Custom GPT after the Builder was updated to the managed A9.5 Action schema and zero-client instructions.

Test source:

`https://www.youtube.com/watch?v=IzYyKRx7Qwg`

Requested mode:

`Перевірити факти/твердження`

## User-visible flow

Observed sequence in the actual private GPT:

```text
public YouTube URL + analysis mode
 -> managed credit preflight
 -> 98 credits available
 -> estimated native cost 1 credit
 -> estimated remaining balance 97
 -> explicit owner reply 1
 -> ChatGPT consequential-Action confirmation
 -> native transcript acquisition
 -> material-claim inventory with timestamps
 -> DRAFT CriticProfile
 -> owner approval 1
 -> independent research / critique
 -> final fact-check report in the same chat
```

No separate YouTube opening, Helper, browser audio capture, manual Job ID, user beta code, YouTube cookies, platform login/session state, provider API key or Action bearer credential was requested from the user.

The additional ChatGPT `Allow` confirmation was the platform confirmation for the consequential external Action and did not expose credentials or require opening the media separately.

## Managed transcript acceptance evidence

Observed after the approved native Action call:

```text
provider: Supadata
mode: native
source_language: ru
segment_count: 277
credits_charged: 1
provider_balance_before: 98
provider_balance_after: 97
```

The GPT also identified at least one probable transcription error and treated transcript text as evidence of what the video said rather than independent confirmation that the claims were true.

## Critic workflow acceptance

Before independent research the GPT:
- created a material-claim inventory with timestamps;
- separated factual claims from rhetoric/opinion;
- produced a `DRAFT CriticProfile` with `status: REVIEW_REQUIRED`;
- stopped at the required `1 - APPROVE / 2 - EDIT / 3 - REJECT` gate.

After explicit owner approval, the GPT:
- performed independent source research;
- assigned one verdict to each material claim;
- highlighted food-safety implications separately;
- produced a normal user-facing `ФІНАЛЬНИЙ ЗВІТ`;
- reported final fact-check reliability score `0.91`;
- documented unresolved limitations;
- recorded the managed transcript source/method and actual credit charge;
- ended with `PASS / COMPLETED`.

## Acceptance decision

`A9.5_PRIVATE_GPT_ZERO_CLIENT_E2E = PASS`

`OWNER_ONLY_ZERO_CLIENT_YOUTUBE = COMPLETE`

This closes the first complete owner-only zero-client media source path.

It does not authorize:
- public GPT rollout;
- external tester rollout;
- merge of PR #8 or PR #28;
- production VoiceBridge changes;
- automatic managed AI fallback;
- private/authenticated platform content;
- Instagram/Facebook/Telegram/local-upload support without separate adapter acceptance.

## Next gate

Proceed to independently validate additional source adapters, beginning with A9.6 multi-platform public adapters, while preserving the accepted YouTube owner-only zero-client path as the regression baseline.
