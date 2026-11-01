---
id: YYYYMMDD-HHMMSS-ESCALATION
time: YYYY-MM-DDTHH:MM:SS+05:30
---

# Escalation: CHECK-ID

This file records a check that failed three times. The status script generates this file from run reports. It assigns a timestamp ID and writes the file as `.stageset/escalations/<id>.md`. Do not reuse an ID.

## Skeleton

Link the affected skeleton.

## Failing check

State the check ID, command, and predicted output.

## Attempts

Link all three failed run reports. State what changed between attempts.

## Verified error

Paste the smallest useful observed error. Do not add guesses to this section.

## Attempt diff

State the changes between attempts.

## Smallest repro

Give the smallest command or input that reproduces the problem.

## Planner resolution

The planner must update the skeleton, increase `spec_revision`, set `status: READY`, clear `blocker_ref`, and set `resolution_of` to the latest run ID.

The coder must not redesign the feature.
