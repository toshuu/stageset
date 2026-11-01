---
type: MAINTENANCE
time: PENDING
summary: Add run evidence, probes, verified facts, digests, validation, and generated event tracking.
paths: README.md; STAGESET.md; CHATGPT.md; AGENTS.md; CLAUDE.md; PLANNER-START.md; ideations-rules.md; coder-rules.md; .stageset/; Skeletons/; scripts/stageset-status.py
related: -
commit: -
remote: -
branch: main
---

# Session notes

## Decisions

- Keep one immutable report for each run.
- Keep one immutable event file for each StageSet session.
- Generate the tracker and digest from the event, skeleton, and run files.
- Require evidence for checks and assumptions.
- Stop after three failed attempts for one check.

## Outcome

Add a common evidence workflow for planners and coding agents. Keep the earlier StageSet version on the backup branch.
