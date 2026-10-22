# KRC 0.19.10 — Compact intake & Critic audit acceptance

Status: PRIVATE RELEASE UPDATED / STATIC PASS / BEHAVIORAL PENDING.

## Approved owner request
Do not display full CriticProfile automatically after receiving a research request. Present exactly four options:
1 Розпочати дослідження відразу (профіль за умовчуванням)
2 Наукове дослідження
3 Перегляд і редагування профілю дослідження
4 Скасувати дослідження

Option 1 approves detected/default CriticProfile and starts; option 2 selects scholarly protocol and approves revised default; option 3 displays full profile for review without research; option 4 stops. An explicit user request to see profile takes precedence. Manual route correction remains available. Default CORE for ambiguous research intent.

## Critic acceptance requirements
- Each material claim includes exact source identifiers S1/S2/... with title, citation, and inspected supporting passage or an explicit missing-access limitation.
- Upstream-origin independence must be established rather than assumed from separate URLs or papers; UNKNOWN sources cannot be counted as verified independent origins.
- Match every achieved/required cross-check tally to traceable, counted source origins. No hidden PASS.
- Each real Critic iteration logs its decision, issues, edits and unresolved SHORTFALL, without inventing iterations.
- Final audit includes approved_at with ISO 8601 timestamp and profile version.
- Explain reliability scoring; if no transparent reproducible method exists, use a qualitative assessment.

## Tests to run with private plugin
- M01 ordinary research -> only the four-choice menu, no profile and no research started.
- M02 choose 1 -> approve detected profile, research begins with correct route.
- M03 choose 2 -> scholarly mode explicitly, correct scientific rules and approval timestamp.
- M04 choose 3 -> full CriticProfile displayed, REVIEW_REQUIRED and no research.
- M05 choose 4 -> stop with no source acquisition.
- M06 explicitly ask to see profile in first request -> full profile visible without starting.
- M07 correct routing after profile review -> version increments and approval reset.
- E01 same DOI / common dataset appears twice -> counted once unless origins proven independent.
- E02 2/2 PASS requires two named inspected origins and exact source identifiers.
- E03 unresolved independence or paywalled full text -> SHORTFALL, not unsupported PASS.
- E04 no fake timestamps, fake iterations or probabilistic scoring.

## Release evidence
Repo commit for canonical instructions: 06104feb7e731829e9a95a78fe54f9603c7ef9d3.
Private plugin `plugin_bb3595f295708191a3f9e145ba1ff2d5`, version 0.19.10, release `pluginrel_6ada3c4fbecc8191892a3cb108d7c786`; Plugin Creator file read confirmed menu, Critic rules, FREE_ONLY and PRIVATE scope.
No end-to-end chat execution in the installed plugin for this release is claimed yet.
