# Request Log Public Disablement Decision

Date: 2026-08-23
Status: APPROVED / IMPLEMENTED IN REPOSITORY / MANUAL BUILDER SYNC PENDING
Scope: public K-Research & Critic

## Decision

Disable the automatic Request Log Action in the public Custom GPT.

## Reason

The request-log implementation worked technically, but ChatGPT displays an external Action consent prompt before sharing the generalized request topic with `script.google.com`.

For a non-essential owner analytics function, this consent interruption materially degrades the first-request UX. The GPT owner cannot pre-authorize this consent for every public user.

## Product target

```text
Public request -> CriticProfile gate -> Research -> Critic -> report
```

No automatic request-log Action occurs before the CriticProfile gate.

## Retained prototype

Do not delete the tested implementation:

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
Google Sheet: K-Research & Critic — Request Log
Apps Script deployment
```

Historical runtime acceptance remains valid as evidence that the prototype worked.

## Active Builder target

```text
Actions: disabled
REQUEST LOGGING instruction block: absent
privacy-policy URL required by active package: no
```

## Manual completion gate

Repository changes do not update the Custom GPT automatically. Completion requires:

1. remove the `logRequest` Action from the public Builder;
2. replace Builder Instructions with current `main/prompts/GPT_STORE_INSTRUCTIONS.md`;
3. save/update the GPT;
4. run a NEW-chat substantive request;
5. verify that no `script.google.com` consent screen appears and the CriticProfile gate appears directly;
6. then update manifest/docs to `repository_matches_current_public_builder=true` and mark disablement runtime accepted.

## Markers

```text
REQUEST_LOG_PROTOTYPE = IMPLEMENTED_TESTED
REQUEST_LOG_PUBLIC_TARGET = DISABLED
DISABLE_REASON = USER_CONSENT_UX
BUILDER_SYNC = PENDING
```
