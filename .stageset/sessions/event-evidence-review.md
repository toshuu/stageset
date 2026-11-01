---
type: MAINTENANCE
time: PENDING
summary: Complete and review the evidence workflow. Add ChatGPT app instructions and improve StageSet validation.
paths: README.md; STAGESET.md; CHATGPT.md; coder-rules.md; ideations-rules.md; .stageset/config.yml; .stageset/formats.md; .stageset/facts.md; .stageset/templates/; .stageset/runs/; .stageset/escalations/; .stageset/sessions/; Skeletons/Probes/; scripts/stageset-status.py
related: -
commit: -
remote: -
branch: main
---

# Session notes

## Decisions

- Add a manual ChatGPT app entry point. ChatGPT apps do not automatically read repository instruction files.
- Keep planner and coder rules in separate files.
- Use run reports as evidence for commands, checks, and probes.
- Generate the session tracker and digest from event files.
- Keep the pre-evidence version on a separate backup branch.

## Outcome

Add a shared evidence workflow for planners and coding agents. Add validation for idea metadata and generated views. Keep rollback through normal Git history.
