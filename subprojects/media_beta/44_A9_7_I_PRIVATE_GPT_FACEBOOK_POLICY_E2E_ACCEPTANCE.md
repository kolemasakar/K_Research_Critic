# A9.7-I Private GPT Facebook Policy E2E Acceptance
Фактична owner-only NEW-chat перевірка виправленої Facebook failure policy у приватному MEDIA BETA.

Status: ACCEPTED
Date: 2026-08-26
Scope: actual private `K-Research & Critic - MEDIA BETA` Custom GPT

## Acceptance input

A fresh NEW-chat owner test used the public Facebook Reel:

`https://www.facebook.com/reel/1114235920664408/`

Requested mode:

`fact/claim verification`

The test was intentionally run without extra routing hints so the Builder policy itself controlled the flow.

## Observed runtime result

The actual private GPT reported that the Reel could not be obtained through the available free route.

The response then stopped media intake and stated that the reserve paid Facebook route is not used in the active MEDIA BETA flow.

Observed credit result:

`credits charged: 0`

No fact-check research was started because retrieval/transcription had not succeeded.

## Policy assertions

PASS:
- Facebook request reached the free Facebook intake policy rather than a Supadata-first flow;
- Cobalt/free retrieval failure was treated as media retrieval unavailable;
- media intake stopped after the free retrieval failure;
- no paid Facebook retrieval offer was shown;
- no ScrapeCreators approval prompt was shown;
- no paid fallback continuation was initiated;
- reported charged credits were zero;
- no Helper, beta code, Job ID, cookies, login, or separate-media-opening request was shown;
- no independent fact-check started without successful retrieval/transcription.

## Relationship to positive-path acceptance

This NEW-chat test accepts the corrected private-GPT failure-policy behavior. It does not re-demonstrate a current successful Cobalt retrieval for the same Reel.

The positive backend path remains independently live-accepted by the canonical A9.7-H1 record:

`41_A9_7_FACEBOOK_COBALT_LIVE_ACCEPTANCE.md`

That evidence demonstrated:

`Facebook Reel -> Cobalt -> AssemblyAI -> durable KRCM -> COMPLETED`

with zero retrieval credits.

## Acceptance decision

A9.7-I private-GPT policy E2E is ACCEPTED.

Authoritative release markers after this acceptance:
- `builder_policy_fix_runtime_applied = true`;
- `a9_7_i_private_gpt_e2e_complete = true`;
- `rollout_state = A9_7_I_PRIVATE_GPT_E2E_ACCEPTED`.

This acceptance does not authorize:
- ScrapeCreators activation;
- paid Facebook fallback;
- external tester rollout;
- merge to the public product;
- production VoiceBridge changes.

## Next engineering boundary

The Facebook A9.7-I policy gate is closed. Remaining A9 zero-client expansion work is outside this acceptance and includes the not-started Telegram public adapter and the not-yet-accepted local upload path.
