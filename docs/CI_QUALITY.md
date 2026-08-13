# CI_QUALITY
Документ визначає автоматизовані перевірки якості, покриття, типізації та CI для K_Supervisor.

Version: 1.1
Status: ACTIVE

## 1. Purpose

This document defines the Phase 12 repository quality gates.

The goal is to make correctness, compatibility, package policy, and regression checks reproducible on pushes and pull requests without adding a paid provider dependency.

## 2. CI Matrix

The reference workflow validates the engineering runtime on:

```text
Python 3.13
Python 3.14
```

Both matrix entries run the full deterministic pytest suite.

The quality job uses Python 3.13 as the stable baseline for dependency integrity, lint, type, repository-policy, GPT Store package, and coverage validation.

## 3. Action Baseline

The workflow uses:

```text
actions/checkout@v6
actions/setup-python@v6
```

Checkout uses `persist-credentials: false` and the workflow has read-only repository permissions.

## 4. Dependency Integrity Gate

After installing development dependencies, CI runs:

```text
python -m pip check
```

The quality job fails when installed package requirements are internally inconsistent.

Runtime dependencies remain in `requirements.txt`. Development-only quality dependencies are isolated in `requirements-dev.txt`.

## 5. Ruff Correctness Gate

Ruff is the repository lint engine.

The current hard gate intentionally focuses on correctness-sensitive rule families rather than forcing a broad style rewrite:

```text
python -m ruff check . --select E9,F63,F7,F82
```

The selected families catch syntax/runtime-risk constructs and undefined-name failures. Broader formatting/style enforcement may be enabled later through reviewed incremental changes.

## 6. Mypy Typed Boundary Gate

Mypy validates the most contract-sensitive typed boundaries:

```text
python -m mypy models config gpt_store
```

This covers canonical data contracts, frozen configuration and task snapshots, and GPT Store checkpoint contracts.

The scope is a ratchet: it should expand over time and should not be reduced merely to make CI green.

## 7. Coverage Gate

The quality job runs:

```text
python -m pytest --cov --cov-report=term-missing --cov-fail-under=70
```

Current blocking floor:

```text
70 percent
```

The validated Phase 12 baseline is 85 percent total coverage. The floor is a minimum, not a target ceiling.

Coverage does not count manual ChatGPT UI/account checks as automated PASS conditions.

## 8. Repository Policy Validation

CI runs:

```text
python -m scripts.validate_repository
```

The validator checks tracked repository invariants including:

- ASCII tracked filenames;
- project-document encoding rules;
- no ambiguous stable-document revision suffixes;
- no tracked `.env`;
- no obvious private keys or common live credential formats;
- no stale `.gitkeep` in directories that already contain tracked files;
- required GPT Store manifest and instruction assets remain tracked.

The validator intentionally scans tracked files rather than local runtime directories.

## 9. GPT Store Release Regression Gate

CI runs:

```text
python -m scripts.validate_store_package
```

This protects Store-first invariants including:

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

## 10. Deterministic Reference Benchmark

The full pytest and coverage commands automatically execute:

```text
tests/test_reference_benchmark.py
```

Its fixture is:

```text
examples/reference_benchmark.json
```

The benchmark covers four end-to-end reference tasks across literary analysis, software engineering, medicine, and geodesy. It validates domain resolution, explicit profile approval, autonomous completion, evidence, reliability floors, PASS decisions, final artifacts, and the no-private-reasoning review-protocol boundary.

The benchmark is synthetic, local, offline, deterministic, and cost-free. It must not be changed into a live-provider dependency for normal repository CI.

## 11. Dependency and Action Maintenance

Dependabot is configured for weekly updates of:

```text
pip dependencies
GitHub Actions
```

Quality dependency versions are constrained in `requirements-dev.txt`; the project does not claim exact pinning where ranges are intentionally used.

## 12. Pull Request Behavior

The workflow runs on pushes and pull requests.

Concurrency cancellation prevents obsolete runs for the same workflow/ref from consuming CI time after a newer commit arrives.

A merge policy may require named CI jobs through branch protection. Branch-protection configuration is an administrative repository setting and is not silently changed by application code.

## 13. Local Commands

Install and run the same quality gates locally with:

```text
python -m pip install -r requirements-dev.txt
python -m pip check
python -m ruff check . --select E9,F63,F7,F82
python -m mypy models config gpt_store
python -m scripts.validate_repository
python -m scripts.validate_store_package
python -m pytest -q tests/test_reference_benchmark.py
python -m pytest --cov --cov-report=term-missing --cov-fail-under=70
```

## 14. Validated Phase 12 Baseline

The implementation baseline immediately before documentation close-out passed all three CI jobs:

```text
Python 3.13 full suite: 169 passed
Python 3.14 full suite: PASS
Quality gates: PASS
Dependency integrity: PASS
Ruff correctness gate: PASS
Mypy typed boundary gate: PASS
Repository policy validator: PASS
GPT Store package validator: PASS
Total coverage: 85 percent
Coverage floor: 70 percent
Reference benchmark cases: 4
```

The documentation close-out commit must pass the same workflow before Phase 12 is considered finalized.

## 15. Quality Policy

A quality gate must fail explicitly when its invariant is violated.

Do not hide critical failures through `continue-on-error`, blanket ignores, permanent expected failures, or removal of a gate solely to obtain a green workflow.

Temporary exclusions must be narrow, documented, and reviewed for removal.

Phase 12 is complete only when the final synchronized repository state passes the full Python 3.13/3.14 and quality workflow.
