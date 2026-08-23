# CriticProfile Gate Runtime Acceptance

Version: 1.0
Date: 2026-08-23
Status: PASS / RUNTIME_ACCEPTED

## Scope

Owner runtime acceptance of the two-stage CriticProfile gate in the actual private `K-Research & Critic - MEDIA BETA` Custom GPT after Builder Instructions synchronization.

This acceptance covers the text-research route. Media provider-credit gates were not exercised in this test and remain unchanged.

## Test request

```text
Досліди, чи справді холодний душ покращує імунітет.
```

Domain/risk resolved by the GPT as medicine / health, `CRITICAL`.

## Observed sequence

### Gate 1

PASS.

The GPT created the CriticProfile internally and did not display it automatically. It displayed:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

No independent research started before user approval.

### Profile review

The owner selected `2`.

PASS.

The complete profile was displayed with `approved_by=null` and `approved_at=null`, followed by:

```text
1 - прийняти профіль, виконати дослідження.
2 - редагувати профіль.
3 - скасувати дослідження.
```

### Profile edit

The owner selected `2` and requested:

- increase cross-check depth to three independent sources;
- require systematic reviews or meta-analyses when available.

PASS.

The GPT produced CriticProfile version 2, kept `status=REVIEW_REQUIRED`, kept `approved_by=null` and `approved_at=null`, incorporated the requested evidence requirements, and repeated the displayed-profile gate.

### Approval and research

The owner selected `1`.

PASS.

The GPT approved CriticProfile `CP-COLD-SHOWER-IMMUNITY-001`, version 2, started Research -> Critic without another approval prompt, and produced a Ukrainian final report.

Observed final protocol:

- approved profile version: 2;
- critic iterations: 2;
- critic decision: `PASS`;
- reliability score: `0.89`;
- final status: `COMPLETED_WITH_LIMITATIONS` because of evidence-base limitations;
- media transcript: not used;
- managed media credits charged: `0`.

## Acceptance result

The two-stage CriticProfile presentation/approval UX is `RUNTIME_ACCEPTED` for the private owner beta.

Validated behaviors:

1. internal profile creation without automatic display;
2. first `1/2/3` gate;
3. option `2` profile display;
4. edit without premature approval;
5. profile version increment after edit;
6. repeated displayed-profile gate after edit;
7. option `1` approval of the edited profile;
8. immediate Research -> Critic execution after approval;
9. Ukrainian final report and protocol;
10. approved profile version preserved in the protocol.

## Quality observation: cross-check visibility

The runtime report declared the approved requirement of three independent cross-checks, but individual claim rows did not always make three-source compliance visible. This does not invalidate the gate UX acceptance, but it exposes a verification/auditability weakness.

Remediation approved by the owner:

- enforce `required_cross_checks` as a material-claim/conclusion requirement rather than a general aspiration;
- count independent underlying evidence sources, not duplicate publications, syndications, or the source media itself;
- when the required number of independent sources does not exist, explicitly report the shortfall, reduce confidence, and record a limitation;
- require Critic to check cross-check compliance before PASS;
- include required/achieved cross-checks and exceptions in the review protocol.

## Production boundary

This acceptance applies to the private owner beta only. Draft PR #8 remains unmerged. `main`, the published GPT, external tester rollout, and production VoiceBridge remain unchanged pending a separate explicit owner decision.
