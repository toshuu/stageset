# Run reports

Store one report for every check attempt, probe, or implementation verification.

Use `.stageset/templates/run-report-template.md`. Use IDs in the format `YYYYMMDD-HHMMSS-RUN`. Generate one with `python scripts/stageset-status.py --new-run-id`. Save the file as `<id>.md`. The script adds a numeric suffix if it finds an existing ID for the same second. Never overwrite a report.

Record exact commands and observed output. Separate facts from guesses. A `FAIL` report counts as one failed check attempt.
