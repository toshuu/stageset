---
type: IDEATION
time: PENDING
summary: Short summary of this focused session.
paths: Ideas/example.md; Skeletons/src/example.ts
related: IDEA-0001; RUN-000001
commit: -
remote: -
branch: -
---

# Session notes

## Decisions

- Record important decisions.

## Outcomes

- Record the useful result.

## Follow-up

- Record the next action.

Use a new file name for every event. Use lower-case kebab-case.
Use `time: PENDING` when the app cannot read the local clock. The status script resolves it from the Git commit time after the file is committed.
For a PUSH event, set `remote`, `branch`, and `commit` to the confirmed values.
