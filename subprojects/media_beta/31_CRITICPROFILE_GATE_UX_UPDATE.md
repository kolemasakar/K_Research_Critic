# CriticProfile Gate UX Update

Version: 1.0
Date: 2026-08-23
Status: IMPLEMENTED_IN_BRANCH_PENDING_RUNTIME_ACCEPTANCE

## Goal

Reduce the default interaction cost of K-Research & Critic without removing the CriticProfile approval boundary.

The system must create the full CriticProfile before independent research, but must not display it automatically.

## First gate

After successful profile creation, show exactly:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

Behavior:

- `1` approves the internally created current profile and immediately starts research;
- `2` displays the complete current profile and enters the displayed-profile gate;
- `3` cancels the research and stops.

No independent research may start before explicit `1`.

## Displayed-profile gate

After the user selects `2`, show the complete current CriticProfile and then show exactly:

```text
1 - прийняти профіль, виконати дослідження.
2 - редагувати профіль.
3 - скасувати дослідження.
```

Behavior:

- `1` approves the displayed profile and immediately starts research;
- `2` requests or accepts profile edits, keeps the profile in `REVIEW_REQUIRED`, displays the revised profile, and repeats the same displayed-profile menu;
- `3` cancels the research and stops.

Direct natural-language changes while the profile is displayed are treated as edit requests.

## Approval state

On approval:

```text
status = APPROVED
approved_by = user
approved_at = current ISO-8601 timestamp
```

The profile may not be described as approved before explicit option `1`.

## Scope

This UX rule applies to:

- ordinary text research;
- media research after media intake is complete;
- recovered `PROFILE_REVIEW_REQUIRED` checkpoints.

Media credit-consent gates remain separate and unchanged.

## Invariants

- CriticProfile is still mandatory before independent research.
- Direct execution does not bypass CriticProfile creation; it only bypasses automatic display.
- User can always inspect/edit the profile through option `2`.
- Material profile changes after approval require a new approval gate.
- Hidden chain-of-thought is never displayed.

## Acceptance tests

PASS requires:

1. A new text-research request creates the profile but does not display it before the first menu.
2. First-menu `1` starts research using an approved profile.
3. First-menu `2` displays the profile and the second menu.
4. Second-menu `2` allows edits and redisplays the revised profile with the second menu.
5. Either-menu `3` stops without research.
6. Media workflow preserves all transcript/provider credit gates before this profile gate.
7. Ukrainian remains the default user-facing language and report/verdict localization remains unchanged.

## Production boundary

Implemented only in `agent/video-url-research` / draft PR #8 until separate runtime acceptance and explicit promotion decision.

Public GPT, `main`, and production VoiceBridge are unchanged.
