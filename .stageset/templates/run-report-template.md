---
id: YYYYMMDD-HHMMSS-RUN
type: CHECK
time: PENDING
result: FAIL
skeleton: Skeletons/src/example.ts
check_id: CHECK-EXAMPLE-01
attempt: 1
spec_revision: 1
command: "python -m pytest -q tests/test_example.py"
---

# Run report

Before you create a report, run `python scripts/stageset-status.py --new-run-id` and use its output for `id` and the file name. This command reserves the ID. After you save the report, delete `.stageset/runs/.<id>.reserve`. Do not delete the reservation before the report exists.

## Goal

State the exact check or probe goal.

## Commands

Record every exact command. Include the working directory and relevant environment details.

```text
python -m pytest -q tests/test_example.py
```

## Observed output (trimmed)

Paste the actual output. Keep relevant error lines. State when you trim output.

```text
Paste actual output here.
```

## Result

Use one value: `PASS`, `FAIL`, or `BLOCKED`.

## Facts

Record only observations that the command or output proves.

## Guesses

Record guesses separately. Do not treat a guess as a fact.

## Assumptions checked

For each assumption, record its ID, result (`CONFIRMED` or `REFUTED`), command, and evidence.

## Tried

List each action that you tried. State the result.

## Open question for planner

State the smallest decision or clarification that you need. Write `None` when no question remains.

## Attempt diff

Compare this attempt with the prior attempt. State what changed and why.

## Smallest repro

Give the smallest command, input, or file set that reproduces the failure. Write `None` when this does not apply.
