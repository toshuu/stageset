---
type: MAINTENANCE
time: PENDING
summary: Add automated GitHub Actions validation for StageSet syntax, generated files, and workspace rules.
paths: .github/workflows/stageset-validation.yml
related: -
commit: -
remote: -
branch: main
---

# Session notes

## Goal

Run StageSet validation automatically after a push or pull request.

## Outcome

The workflow checks Python syntax. It generates the session tracker and digest. It validates the StageSet workspace.
