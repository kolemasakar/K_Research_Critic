# KRC MEDIA CI validation trigger

Date: 2026-09-19

Purpose: trigger the existing pull-request CI against the staged R3-E3 / R3-E4 / OAuth / R3-F candidate after confirming that the repositories are public and standard GitHub-hosted runner minutes are not billed against the private-repository quota.

Scope:
- staging branch only;
- no main mutation;
- no PR merge;
- no provider execution;
- no Facebook or Telegram live start;
- no publication or sharing change.

Expected validation surface:
- Python 3.13 tests;
- Python 3.14 tests;
- quality gates and coverage.
