# Instructions for coding agents

This workspace uses StageSet. Before you inspect or change project code, read:

1. `.stageset/DIGEST.md`.
2. `.stageset/facts.md`.
3. `STAGESET.md`.
4. `.stageset/config.yml`.
5. `coder-rules.md`.
6. `.stageset/sessions-tracker.md`.
7. Open blockers and their run reports.

Run `python scripts/stageset-status.py` to find ready skeletons. Read each full skeleton and its linked idea files before you implement it.

Follow the skeleton and its checks. Verify every `ASSUMPTION:` before you rely on it. Save one run report for each check attempt. Keep observed facts separate from guesses.

Stop after three failed attempts for one check. Set the skeleton to `BLOCKED`, set `blocker_ref` to the third run report, and create an escalation file with `--escalate CHECK-ID`. Do not redesign the feature.

After each focused coding session, create one event file in `.stageset/sessions/`. Run `python scripts/stageset-status.py --sync` and then `python scripts/stageset-status.py --validate`. Do not edit the generated tracker or digest by hand.

Record a `PUSH` event only after a remote push succeeds. Use ASD-STE100-style English in project documents, comments, run reports, and event summaries.
