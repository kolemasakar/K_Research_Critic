# Claim-Level Cross-Check Enforcement

Version: 1.0
Date: 2026-08-23
Status: IMPLEMENTED_IN_BRANCH_PENDING_RUNTIME_ACCEPTANCE

## Trigger

Runtime test of the CRITICAL medical query `Досліди, чи справді холодний душ покращує імунітет.` showed that the profile-level requirement `required_cross_checks >= 3` was created correctly, but the final report only demonstrated three-source compliance for the overall conclusion. Some individual material claims were supported by one study while the protocol still returned an unconditional `PASS`.

## Required behavior

For EACH material factual claim, before a verdict is assigned, Research must maintain a cross-check ledger:

```text
required: approved required_cross_checks
achieved_independent: independent underlying evidence sources actually obtained
exception: NONE | SHORTFALL
```

Independence is based on underlying evidence, not URL count. Duplicates, syndication, repeated reporting of one study/source, and the source media/transcript do not count as separate cross-checks.

If `achieved_independent < required`:
- set `exception=SHORTFALL`;
- state why the requirement could not be met;
- lower confidence as appropriate;
- qualify the affected conclusion;
- never state that the cross-check requirement was met for that claim.

Critic must inspect this ledger claim-by-claim. An unconditional `PASS` is forbidden while any material claim has an unreported or unqualified `SHORTFALL`.

## User-facing auditability

For fact-check output, every material claim must include:

```text
Cross-check: achieved/required - PASS|SHORTFALL
```

If `SHORTFALL`, the exception/limitation must be named.

The review protocol must summarize per-claim `required / achieved_independent / exception` and unresolved limitations.

## Risk floors

- LOW >= 0
- MEDIUM >= 1
- HIGH >= 2
- CRITICAL >= 3

A user or approved CriticProfile may raise this value. It must never be silently lowered.

## Regression protection

Automated tests assert:
- Builder remains within the 8000-character limit;
- claim-level ledger fields are present;
- shortfall behavior is mandatory;
- unconditional PASS on hidden/unqualified shortfall is forbidden;
- claim output exposes achieved/required status;
- manifest marks claim-level runtime acceptance false until a new private-GPT runtime test passes.

## Production boundary

Implemented only in `agent/video-url-research` / draft PR #8.

The actual private `K-Research & Critic - MEDIA BETA` Builder must be synchronized again before runtime acceptance of this stronger contract. Public GPT, `main`, and production VoiceBridge remain unchanged.
