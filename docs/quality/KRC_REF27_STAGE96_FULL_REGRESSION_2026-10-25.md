# KRC №96 — isolated full regression and REF-27 scientific gate
Date: 2026-10-25

## Actual execution on krc-cobalt
Connected with authorized Remote Desktop Commander to online `krc-cobalt`, using research-only checkout `/tmp/krc-p0-offline-20261025`. Ran:
```bash
PYTHONPATH=src .venv/bin/python -m pytest -q tests/
```
**253 passed in 2.05 s**, exit code **0**, on host (shell wrapper runtime ~3.2 s). This supersedes previous isolated full baseline of 249 passed. No deployment performed, no service restarted, production/MEDIA/public endpoints unchanged.

The test count concerns tests in the isolated KRC research checkout. Standalone locally generated stage93–95 script tests were not automatically included in this repository-level suite; their separate 11/11 PASS remains an isolated prior result.

## REF-27 scientific gate
Owner-uploaded reference source `pub16677.pdf`, 8 pages, SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`, matches original institutional file; the same canonical PDF is present on isolated host at `/tmp/krc-ext-s04-acceptance/ref27_rtu_original_2013.pdf`. Fig. 1/2 are extracted at isolated host.

Automated scholarly Critic from stage95: REVISE, final scientific gate NO_GO (recorded local prior result, not claimed to be a new independent human review). Unresolved:
- independently verified two-person axis tick and curve point readings;
- original graph series ↔ nine individual Table I specimens/aggregation attribution;
- plotted early 2-hour 270-m/s change origin and reference;
- full uncertainty budget with manufacturer device stated max ±1% separated from assumed pixel localization;
- external scientific reviewer and author approval at final gate.

## Decision
Engineering regression: **PASS 253/253**. Full scholarly/ref27 figure claim verification: **SHORTFALL**. Publication authorization: **NO_GO**. FREE_ONLY preserved.
