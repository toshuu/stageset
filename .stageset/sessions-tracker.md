# StageSet sessions tracker

This file is the single activity log for this workspace.

Use one global ID for every row. Start with `SS-000001`. Increase the number by one for every new row. Never reuse an ID.

Allowed event types: `IDEATION`, `CODING`, `PUSH`, `MAINTENANCE`.

Use the timezone in `.stageset/config.yml`. Use an ISO 8601 timestamp with its UTC offset. Do not guess a timestamp.

Add one row for each completed focused session. Add a `PUSH` row only after a remote push succeeds. A local commit is not a push.

Keep each summary short. Use links or paths for detail. Do not delete old rows. Correct an error with a new `MAINTENANCE` row and a clear note.

The status helper calculates totals from the event types in this table. Do not maintain separate counters. Reserve the next global ID at the start of a focused session, then re-read this file before saving to avoid duplicate IDs.

| ID | Type | Timestamp | Summary | Changed paths | Related ID | Commit / Push |
| --- | --- | --- | --- | --- | --- | --- |
| SS-000001 | MAINTENANCE | 2026-11-01T21:00:00+05:30 | Initialize the StageSet starter workspace. | `README.md`; `STAGESET.md`; `AGENTS.md`; `CLAUDE.md`; `PLANNER-START.md`; `ideations-rules.md`; `coder-rules.md`; `LICENSE`; `Code/`; `Ideas/`; `Skeletons/`; `.stageset/`; `scripts/stageset-status.py` | - | - |
