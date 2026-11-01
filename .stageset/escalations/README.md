# Escalations

The status script creates an escalation file after three failed attempts for a check. Each file has a timestamp ID in the format `YYYYMMDD-HHMMSS-ESCALATION`. The script adds a numeric suffix if an ID for the same second already exists.

Run `python scripts/stageset-status.py --escalate CHECK-ID`.

Give the generated file and its run reports to the planner. Keep the escalation history.
