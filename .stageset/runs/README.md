# Run reports

Store one report for every check attempt, probe, or implementation verification.

Use `.stageset/templates/run-report-template.md`. Use IDs in the format `YYYYMMDD-HHMMSS-RUN`. Generate one with `python scripts/stageset-status.py --new-run-id`. The command reserves the ID. Save the report as `<id>.md`, then delete `.stageset/runs/.<id>.reserve`. Do not delete the reservation before the report exists. This prevents concurrent agents from claiming the same ID. Never overwrite a report.

Record exact commands and observed output. Separate facts from guesses. A `FAIL` report counts as one failed check attempt.
