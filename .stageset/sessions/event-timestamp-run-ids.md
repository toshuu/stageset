---
type: MAINTENANCE
time: PENDING
summary: Replace sequential run IDs with timestamp IDs and make skeleton deviations explicit blockers.
paths: README.md; coder-rules.md; STAGESET.md; ideations-rules.md; AGENTS.md; .stageset/formats.md; .stageset/templates/run-report-template.md; .stageset/templates/escalation-template.md; .stageset/templates/session-event-template.md; .stageset/runs/README.md; .stageset/escalations/README.md; scripts/stageset-status.py
related: -
commit: -
remote: -
branch: main
---

# Session notes

## Decisions

- Use timestamp-based IDs for run reports and escalation files.
- Generate run IDs with the status script.
- Keep a numeric suffix for same-second collisions.
- Read the digest first and inspect only task-relevant files.
- Treat an impossible skeleton step as a blocker. Record evidence in a run report.

## Outcome

Update the README, templates, formats, coder rules, and status script. Keep the existing backup branch and Git history.
