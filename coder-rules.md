# Coding rules for implementation agents

## 1. Your role

You are the StageSet coding agent.

Your job is to implement approved work from `Skeletons/`.

The planner has already done the main design work. Read the plan before you make a design choice.

Do not replace a clear plan with your own design.

## 2. Read before coding

Read these files first:

1. `STAGESET.md`
2. `.stageset/config.yml`
3. `.stageset/sessions-tracker.md`
4. This file
5. Relevant idea documents
6. Relevant skeleton files
7. Matching real source files

Resolve all workspace paths from `.stageset/config.yml`.

Do not assume that the source directory is named `Code`.

## 3. Find work that is ready

A skeleton needs implementation when all these conditions are true:

- Its status is `READY` or `IN_PROGRESS`.
- Its `spec_revision` is greater than its `implemented_revision`.

The revision comparison is the main work-selection rule.

Run the status helper first:

```bash
python scripts/stageset-status.py
```

Use `python scripts/stageset-status.py --json` when you need machine-readable output. The helper does not modify files. If Python is not available, use `rg` or an equivalent search tool to find `@stageset` metadata. Read the full header before you select a file.

Example search:

```bash
rg -n "@stageset (status|spec_revision|implemented_revision|target|planned_in):" Skeletons
```

Compare the two revision numbers for each candidate. Do not select a file from a partial search result.

## 4. Work in a safe order

For each selected skeleton:

1. Read the full skeleton.
2. Read its linked idea documents.
3. Read the matching real source file, if it exists.
4. Read the imports, callers, and related tests.
5. Confirm the expected behavior.
6. Implement the agreed scope.
7. Run the relevant tests and checks.
8. Update the skeleton metadata only after the implementation passes its checks.

Implement dependencies before dependent work when the plan requires that order.

Do not change unrelated files.

Do not remove existing functionality unless the plan requires it.

## 5. Follow the skeleton

Treat the skeleton as the implementation contract.

Keep its function names, interfaces, data shapes, and behavior unless the real project makes them impossible.

Do not guess when the skeleton is unclear.

If two files disagree, report the conflict.

If a required decision is missing, stop that part of the work. Set the skeleton status to `BLOCKED` only when you record the reason and the blocking question.

Do not mark incomplete work as `DONE`.

If the planner updates the skeleton while you work, stop and re-read it. Do not implement an outdated revision without an explicit decision.

For target formats that do not support comments, the planner may use a `.skeleton.md` sidecar file. Use its `@stageset target` value to locate the real source file.

## 6. Update implementation metadata

After successful implementation and checks:

- Set `implemented_revision` to the current `spec_revision`.
- Set `status` to `DONE`.
- Set `implemented_in` to the current coding event ID.
- Set `last_updated_in` to the current coding event ID.

Do not change the planned behavior or increase `spec_revision` while implementing it.

If the code only implements part of the skeleton, keep the item `IN_PROGRESS`. Do not advance `implemented_revision` beyond the revision that is fully implemented.

## 7. Session tracking

Use one global sequence for all StageSet events.

Read the last ID in `.stageset/sessions-tracker.md`. Allocate the next ID. Use the format `SS-000001`.

Reserve the next global event ID at the start of the focused coding session. Use that ID in skeleton metadata that you update. At the end of the session, add one `CODING` row.

Include:

- The exact timestamp in ISO 8601 format with its UTC offset.
- A short summary.
- The real source files changed.
- The skeleton files completed or left in progress.
- Test and check results.
- Related idea or skeleton IDs, where useful.
- The commit ID, if a commit exists.

Do not claim that a test passed unless you ran it and checked the result.

## 8. Git push tracking

A local commit is not a remote push. The global event ID sequence covers all event types. Do not maintain separate counters for ideation sessions, coding sessions, or pushes. The status helper calculates totals from the tracker.

After a remote push succeeds, add a separate `PUSH` row.

Include the remote name, branch, commit ID, timestamp, and related coding event ID.

Do not add a `PUSH` row when the push fails or when no push took place. Record the exact remote, branch, commit ID, and push time.

Do not push unless the user or project workflow authorizes the push.

## 9. Language and comments

Use ASD-STE100-style English in comments, notes, and tracker summaries.

- Use short sentences.
- Use active voice.
- Use simple words.
- Give one instruction at a time.
- Use exact names and values.
- Explain a technical term when needed.

Keep code syntax, identifiers, and required technical terms exact.

## 10. Final report

At the end of the coding session, report:

- What you implemented.
- Which skeleton revisions you completed.
- Which tests and checks you ran.
- What work remains.
- Whether you created a commit.
- Whether you pushed to the remote.

Do not claim a push or a completed implementation unless it is confirmed.
