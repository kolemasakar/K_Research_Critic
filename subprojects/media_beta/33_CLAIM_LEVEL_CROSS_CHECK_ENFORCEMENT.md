# Claim-Level Cross-Check Enforcement

Version: 1.1
Date: 2026-08-23
Status: RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA

## Trigger

Runtime testing of the CRITICAL medical query `Досліди, чи справді холодний душ покращує імунітет.` first showed that the profile-level requirement `required_cross_checks >= 3` was created correctly, but individual material claims could still rely on one study while the protocol returned an unconditional `PASS`.

The contract was then hardened claim-by-claim and the actual private `K-Research & Critic - MEDIA BETA` Builder was resynchronized. A repeated runtime test passed the required behavior.

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

## Runtime acceptance evidence

Repeated owner-only private-GPT test after Builder synchronization produced:
- `risk_level=CRITICAL`;
- `required_cross_checks=3` per material claim;
- visible claim-level `Cross-check: achieved/required - PASS|SHORTFALL`;
- a concrete `1/3 - SHORTFALL` for the claim interpreting the 29% sick-leave result;
- an explicit reason for the shortfall;
- no false claim that 3/3 had been achieved for that claim;
- final status `COMPLETED_WITH_LIMITATIONS` rather than unconditional `PASS`.

Canonical runtime record: `34_CLAIM_LEVEL_CROSS_CHECK_RUNTIME_ACCEPTANCE.md`.

## Regression protection

Automated tests assert:
- Builder remains within the 8000-character limit;
- claim-level ledger fields are present;
- shortfall behavior is mandatory;
- unconditional PASS on hidden/unqualified shortfall is forbidden;
- claim output exposes achieved/required status;
- manifest records claim-level runtime acceptance after live PASS.

## Production boundary

Accepted only in the private owner `K-Research & Critic - MEDIA BETA` and branch `agent/video-url-research` / draft PR #8.

Public GPT, `main`, and production VoiceBridge remain unchanged pending a separate owner decision.
