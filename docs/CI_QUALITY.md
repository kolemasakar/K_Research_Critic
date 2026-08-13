# CI_QUALITY
Документ визначає автоматизовані перевірки якості, покриття, типізації та CI для K_Supervisor.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines the Phase 12 repository quality gates.

The goal is to convert previously manual quality expectations into reproducible checks that run on pushes and pull requests without adding a paid provider dependency.

## 2. CI Matrix

The reference workflow validates the supported engineering runtime on:

```text
Python 3.13
Python 3.14
```

Both matrix entries run the full deterministic pytest suite.

The quality job uses Python 3.13 as the stable baseline for lint, type, coverage, repository-policy, and GPT Store package validation.

## 3. Action Baseline

The workflow uses Node 24 generation GitHub Actions:

```text
actions/checkout@v6
actions/setup-python@v6
```

This removes the known Node 20 deprecation warning from the previous v4/v5 workflow baseline.

## 4. Lint Gate

Ruff is the repository lint engine.

The initial hard gate intentionally focuses on correctness-sensitive rules rather than forcing a broad formatting rewrite in the same phase:

```text
E9
F63
F7
F82
```

These classes catch syntax/runtime-risk and undefined-name failures. Broader style rules may be enabled later in small reviewed increments.

## 5. Type Gate

Mypy validates the most contract-sensitive typed boundaries first:

```text
models/
config/
gpt_store/
```

This scope covers canonical data contracts, frozen configuration, configuration snapshots, and Store checkpoint contracts. The scope is a ratchet: it should expand over time and should not be reduced merely to make CI green.

## 6. Coverage Gate

The quality job collects branch coverage across the source packages.

Initial minimum:

```text
70.0 percent
```

This is a baseline floor, not a target ceiling. A future change should raise the floor when measured coverage and test quality support a stable higher threshold.

Coverage does not count manual ChatGPT UI checks as automated PASS conditions.

## 7. Repository Policy Validation

`scripts/validate_repository.py` checks source-controlled repository invariants including:

- ASCII tracked filenames;
- project-document encoding rules;
- no ambiguous stable-document revision suffixes;
- no tracked `.env`;
- no obvious private keys or common live credential formats;
- no stale `.gitkeep` in directories that already contain tracked files;
- required GPT Store manifest and instruction assets remain tracked.

The validator intentionally scans tracked files rather than local runtime directories.

## 8. GPT Store Release Regression Gate

The CI quality job runs:

```text
python -m scripts.validate_store_package
```

This keeps the Store-first invariants under regression coverage:

```text
no developer API key
no mandatory external backend
no pinned model
Apps disabled
Actions disabled
mandatory CriticProfile approval gate
checkpoint schema validation
```

Real Free-account, paid-account, model-picker, Builder Profile, category, and Publish checks remain manual because repository CI cannot honestly prove ChatGPT UI/account behavior.

## 9. Dependency Maintenance

Dependabot is configured for weekly updates of:

```text
pip dependencies
GitHub Actions
```

Runtime dependencies remain in `requirements.txt`.

Development-only quality dependencies are isolated in:

```text
requirements-dev.txt
```

## 10. Pull Request Behavior

The workflow runs on both pushes and pull requests and uses read-only repository permissions.

Concurrency cancellation prevents obsolete runs for the same ref from consuming CI time after a newer commit arrives.

A merge policy may require the named CI jobs as branch-protection checks through GitHub repository settings. Branch-protection configuration itself is an administrative repository setting and is not silently changed by application code.

## 11. Local Commands

Reference commands:

```text
python -m pip install -r requirements-dev.txt
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
python -m pytest --cov --cov-report=term-missing --cov-fail-under=70
```

## 12. Quality Policy

A Phase 12 quality gate must fail explicitly when its invariant is violated.

Do not hide a critical failure through `continue-on-error`, blanket ignores, or permanent expected failures.

Any temporary exclusion must be narrow, documented, and reviewed for removal.
