# StageSet formats and conventions

## 1. Session event files

Store one Markdown file for each focused session in `.stageset/sessions/`.

Allowed event types:

- `IDEATION`
- `PROBE`
- `CODING`
- `PUSH`
- `MAINTENANCE`

Use `.stageset/templates/session-event-template.md`. Use a unique, descriptive lower-case kebab-case file name. Do not reuse a file name.

Use the timestamp format `YYYY-MM-DDTHH:mm:ss+05:30`. Use the configured timezone and its UTC offset. Do not invent a time.

A chat planner that cannot read the local clock must set `time: PENDING`. After the event file is committed, the script reads its Git commit time. The validator reports an unresolved time when the file has no Git commit.

The generated event ID uses `YYYYMMDD-HHMMSS-TYPE`. The script adds a numeric suffix only when two events have the same timestamp and type.

The event file path is the stable reference used by idea and skeleton metadata. For example, `planned_in` can contain `.stageset/sessions/ideation-auth-flow.md`.

Do not edit `.stageset/sessions-tracker.md` by hand. The script generates it from event files.

## 2. Idea IDs

Use `IDEA-` followed by four digits. Find the highest existing ID in idea front matter. Add one to get the next ID.

Use `.stageset/templates/idea-template.md`. Keep `created_in` and `updated_in` as paths to the relevant event files. Use ISO 8601 timestamps with an offset, or `PENDING` when the app cannot read the clock. The validator resolves `PENDING` from the linked event file.

## 3. Skeleton metadata

Use `.stageset/templates/skeleton-template.txt`. Put the metadata in the first comment block. Use the normal comment syntax for the target language.

Required metadata fields:

- `version`
- `kind`
- `target`
- `source_idea`
- `status`
- `priority`
- `spec_revision`
- `implemented_revision`
- `planned_in`
- `last_updated_in`
- `implemented_in`
- `blocker_ref`
- `resolution_of`

`kind` is `IMPLEMENTATION` or `PROBE`.

An implementation skeleton mirrors one source file. Set `target` to the path relative to the configured code directory. If the target does not support comments, use a `.skeleton.md` sidecar.

A probe is a small, read-only task. Store it under `Skeletons/Probes/`. Set `target` to `-`.

## 4. Revisions

Increase `spec_revision` when planned behavior or structure changes. Do not increase it for spelling or formatting changes.

Set `implemented_revision` only when the real code or probe fully completes that revision and the required checks pass.

A skeleton is actionable when:

```text
status is READY or IN_PROGRESS
AND
spec_revision > implemented_revision
```

After verified implementation, set `implemented_revision` to `spec_revision` and set `status` to `DONE`.

## 5. Status values

Skeleton status values: `DRAFT`, `READY`, `IN_PROGRESS`, `DONE`, `BLOCKED`, `SUPERSEDED`.

Idea status values: `DISCOVERY`, `CLARIFIED`, `DECIDED`, `READY_FOR_SKELETON`, `SKELETONIZED`, `IMPLEMENTED`, `PARKED`, `REJECTED`.

A `BLOCKED` skeleton must set `blocker_ref` to a real report under `.stageset/runs/`. A non-blocked skeleton must set `blocker_ref: -`.

After a planner resolves a blocker, the planner must increase `spec_revision`, set `status: READY`, set `blocker_ref: -`, and set `resolution_of` to the run ID that supplied the evidence. Keep previous run reports.

## 6. Check IDs and test contracts

Every implementation skeleton must contain a `## Checks` section. Add one or more check headings.

Use a unique check ID across the workspace. Use a name such as `CHECK-AUDIO-ROUTER-01`.

Each check must define:

- `Command` — the exact command to run.
- `Predicted output` — the output that proves success.
- `Pass condition` — a clear rule.
- `Fail condition` — a clear rule.

Do not use vague checks such as "works correctly". Prefer a command and an observable result.

## 7. Run report IDs and files

Use a new file for every run in `.stageset/runs/`. Use IDs in the format `YYYYMMDD-HHMMSS-RUN`. Generate an ID with `python scripts/stageset-status.py --new-run-id`. The command reserves the ID so concurrent agents do not claim it. Name the report `<id>.md`. After you save the report, delete `.stageset/runs/.<id>.reserve`. Do not delete the reservation before the report exists. Never overwrite a report.

Use `.stageset/templates/run-report-template.md`.

Allowed run types: `CHECK`, `PROBE`, `IMPLEMENTATION`.

Allowed results: `PASS`, `FAIL`, `BLOCKED`.

Record the exact command and the observed output. Trim output only when it is too long. State when you trim it. Keep observed facts separate from guesses.

Use one run report for one check attempt or one probe. Use type `IMPLEMENTATION` for a final integration check that does not belong to one named check. A final integration report does not replace the required PASS report for every check.

Set `spec_revision` to the exact skeleton revision under test. Start `attempt` at 1 for each check and skeleton revision. Increment the attempt number for each retry. Count only `FAIL` reports as failed attempts. Start a new sequence when the planner raises `spec_revision`.

## 8. Assumptions

Write assumptions with the exact tag `ASSUMPTION:`. Give each assumption an ID, such as `A-01`.

The coder must test every assumption before it relies on that assumption. Use a cheap, read-only command where possible. Record the result in a run report as `CONFIRMED` or `REFUTED`, with evidence.

Do not move an assumption into `.stageset/facts.md` until the evidence confirms it.

## 9. Verified facts

`.stageset/facts.md` stores verified facts about the environment and project.

Each fact must include a date and a source run report. A guess is not a fact.

Use this table format:

| Fact ID | Date | Verified fact | Scope | State | Source run |
| --- | --- | --- | --- | --- | --- |
| FACT-0001 | YYYY-MM-DD | Verified statement. | Environment or project scope. | CURRENT | `.stageset/runs/YYYYMMDD-HHMMSS-RUN.md` |

Use `CURRENT` or `SUPERSEDED` for State. If a fact changes, add a new fact and mark the old fact as `SUPERSEDED`. Keep the history. The source run must have a `PASS` result. Use a source path such as `.stageset/runs/YYYYMMDD-HHMMSS-RUN.md`.

## 10. Escalation

Allow a maximum of three failed attempts for one check.

After the third failed attempt:

1. Stop work on that check.
2. Set the skeleton status to `BLOCKED`.
3. Set `blocker_ref` to the third run report.
4. Run `python scripts/stageset-status.py --escalate CHECK-ID`.
5. Give the planner the generated escalation file.

The planner must resolve the design or instruction. The planner must raise `spec_revision` and set `resolution_of` to the run ID. The coder must not redesign the feature. Each generated escalation has a timestamp ID in the format `YYYYMMDD-HHMMSS-ESCALATION`, with a numeric suffix on collision.

## 11. Generated files

Run `python scripts/stageset-status.py --sync` after you add or update event, skeleton, or run files. It regenerates:

- `.stageset/sessions-tracker.md`
- `.stageset/DIGEST.md`

Do not edit these generated files by hand.

Run `python scripts/stageset-status.py --validate` before you finish a work session. It checks idea and skeleton fields, status values, mirror paths, blocker links, check contracts, run report structure, event times, and generated file freshness.

## 12. File size rule

Keep one target source file per implementation skeleton. Keep the plan focused. If one source file is too large to plan as a whole, limit the skeleton to one named function in that file. Split unrelated files into separate skeletons.

## 13. Rollback

StageSet changes are normal Git commits. The repository must keep its history.

Use Git commits to compare and revert changes. Do not force-push over shared history.
