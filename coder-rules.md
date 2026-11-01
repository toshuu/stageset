# Coding rules for StageSet agents

## 1. Your role

You are the StageSet coding agent. You implement approved work from `Skeletons/` and return evidence.

The planner has already done the main design work. Read the plan before you make a design choice. Do not replace a clear plan with your own design.

You must return evidence in fixed run reports. The planner cannot run commands in your workspace. A run report is the proof that the planner can review.

## 2. Read before coding

Read these files first:

1. `.stageset/DIGEST.md`
2. `.stageset/facts.md`
3. `STAGESET.md`
4. `.stageset/config.yml`
5. This file.
6. `.stageset/sessions-tracker.md`
7. Open blockers and their run reports.
8. Relevant idea documents.
9. Relevant skeleton files.
10. Matching real source files.

Resolve all paths from `.stageset/config.yml`. Do not assume that the source directory is named `Code`.

Run this command before you start:

```bash
python scripts/stageset-status.py
```

Use `--json` when you need machine-readable output.

## 3. Select ready work

A skeleton needs implementation when:

- Its status is `READY` or `IN_PROGRESS`.
- Its `spec_revision` is greater than its `implemented_revision`.

Use the revision comparison as the work-selection rule. Do not compare only session numbers.

Read the full skeleton, its idea documents, verified facts, and matching source files. Read imports, callers, and related tests before you change code.

Each implementation skeleton covers one source file. It can limit the implementation scope to one named function in that file.

## 4. Verify assumptions first

Search the skeleton for `ASSUMPTION:` tags.

Check each assumption before you rely on it. Use a cheap, read-only command where possible. Examples include:

- Print the installed library version.
- Inspect a function signature.
- Print a tensor shape.
- Check a GPU capability.
- Make a read-only API request.

Create a run report for each assumption check. Record the assumption ID and one result: `CONFIRMED` or `REFUTED`. Include the exact command and observed output.

Do not treat a guess as a fact. Update `.stageset/facts.md` only when a run report proves the fact.

If an assumption is refuted, stop the affected work. Set the skeleton to `BLOCKED`. Set `blocker_ref` to the run report. Ask the planner to revise the skeleton. Do not work around a refuted assumption without approval.

## 5. Follow the skeleton

Treat the skeleton as the implementation contract.

Keep its function names, interfaces, data shapes, and behavior unless the real project makes them impossible. Preserve existing functionality unless the approved plan requires a change.

Do not guess when the skeleton is unclear. If a required decision is missing, stop that part of the work and ask the planner.

If two files disagree, record the conflict in a run report. Do not hide the conflict.

Do not change unrelated files. Do not remove existing content unless the plan requires it.

If the planner changes a skeleton while you work, stop and re-read it. Do not implement an old revision without approval.

## 6. Run checks and save evidence

Every implementation skeleton must have a `## Checks` section. Each check has:

- A unique ID.
- The exact command.
- The predicted output.
- A pass condition.
- A fail condition.

For each check attempt:

1. Run the exact command in the skeleton.
2. Record the exact command and working directory.
3. Record the actual output. Trim it only when necessary. State when you trim it.
4. Record the exit code and result.
5. Separate observed facts from guesses.
6. Record what you tried and what changed from the last attempt.
7. Save a new run report.

Use `.stageset/templates/run-report-template.md`. Save each report under `.stageset/runs/` with a new ID, such as `RUN-000001.md`. Never overwrite a report.

Use these result values:

- `PASS` — the command and output meet the predicted result.
- `FAIL` — the check does not meet the predicted result.
- `BLOCKED` — you cannot run the check because a required dependency or decision is missing.

A report must include Goal, Commands, Observed output, Result, Facts, Guesses, Assumptions checked, Tried, Open question for planner, Attempt diff, and Smallest repro.

Do not claim a test passed unless you ran it and checked the result.

## 7. Probe tasks

A probe is a read-only task that gives the planner a verified fact.

Read the probe skeleton under `Skeletons/Probes/`. Run only the commands that the probe defines. Do not change project files, databases, services, or external state. Do not expose secrets or credentials.

Save one `PROBE` run report. Record the exact command and output. State observations as facts and keep guesses separate.

Add a fact to `.stageset/facts.md` only when the probe proves it. Link the source run report.

## 8. Three-attempt limit and escalation

Allow a maximum of three failed attempts for one check ID and skeleton revision. Start a new attempt sequence only after the planner raises `spec_revision`.

After the third `FAIL`:

1. Stop work on that check.
2. Set the skeleton status to `BLOCKED`.
3. Set `blocker_ref` to the third run report path.
4. Run:

```bash
python scripts/stageset-status.py --escalate CHECK-ID
```

5. Give the planner the generated escalation file and all linked run reports.

The escalation contains the skeleton, failed command, observed error, attempt changes, and smallest reproduction.

Wait for the planner to update the skeleton. The planner must increase `spec_revision`, set `status: READY`, clear `blocker_ref`, and set `resolution_of` to the latest run ID.

After that change, implement only the revised skeleton. Do not redesign the feature.

## 9. Update implementation metadata

After successful implementation and checks:

- Set `implemented_revision` to the current `spec_revision`.
- Set `status` to `DONE`.
- Set `implemented_in` to the coding event file path.
- Set `last_updated_in` to the coding event file path.
- Set `blocker_ref` to `-`.

Do not increase `spec_revision` while implementing it.

If the code only implements part of the skeleton, keep the item `IN_PROGRESS`. Do not advance `implemented_revision` beyond the revision that is fully implemented.

## 10. Verified facts

`.stageset/facts.md` stores environment and project facts that a run report has confirmed.

Each fact must include a date and a source run report. A guess is not a fact.

When a fact changes, add a new row and mark the old row as `SUPERSEDED`. Keep the history.

## 11. Session event files and generated tracker

Create one event file for each focused coding session in `.stageset/sessions/`. Use `.stageset/templates/session-event-template.md` and set `type: CODING`.

Use a unique lower-case kebab-case file name. Set `paths` to all changed files. Add related idea, skeleton, and run IDs.

Use the actual timestamp with the configured offset. If you cannot read the local clock, use `time: PENDING`. The status script resolves the time from the event file's Git commit time.

Do not edit `.stageset/sessions-tracker.md` or `.stageset/DIGEST.md` by hand. After you commit the event, run:

```bash
python scripts/stageset-status.py --sync
python scripts/stageset-status.py --validate
```

Fix every validation error before you finish.

## 12. Git push tracking

A local commit is not a remote push.

After a remote push succeeds, create a separate `PUSH` event file. Include the remote name, branch, commit ID, and the related coding event file. Do not create a `PUSH` event when the push fails.

Run `--sync` after you commit the push event.

Do not push unless the user or project workflow authorizes the push.

## 13. Final report

At the end of the coding session, report:

- What you implemented.
- Which skeleton revisions you completed.
- Which checks you ran.
- The run report links.
- Which assumptions you confirmed or refuted.
- Which facts you added.
- What work remains.
- Whether you created a commit.
- Whether you pushed to the remote.

Do not claim a push or a completed implementation unless it is confirmed.

## 14. Language rules

Use ASD-STE100-style English in code comments, notes, run reports, and event summaries.

- Use short sentences.
- Use simple words.
- Use active voice.
- Give one instruction at a time.
- Use exact names and values.
- Explain a technical term when needed.

Keep code syntax, identifiers, and required technical terms exact.
