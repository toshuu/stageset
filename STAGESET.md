# StageSet system guide

## 1. Purpose

StageSet separates planning from implementation. A strong planner can design the work first. A smaller coding model can then implement that plan.

StageSet stores four kinds of information:

| Location | Purpose |
| --- | --- |
| `Ideas/` | What the project needs and why. |
| `Skeletons/` | How one source file or one probe must work. |
| Configured code folder | The real application code. |
| `.stageset/` | Rules, evidence, facts, run reports, and session history. |

The planner and coder use the same files and rules. The run reports connect their work. A planner does not need to run code to review evidence. A coder does not need to repeat the full design process.

## 2. Roles

### Planner

The planner can be ChatGPT, Claude, or another chat model.

The planner:

- Reads the current digest, facts, ideas, skeletons, and relevant source code.
- Discusses ideas with the user.
- Records approved decisions in `Ideas/`.
- Writes detailed implementation skeletons in `Skeletons/`.
- Writes small read-only probe tasks when it needs verified facts.
- Reads run reports when the coder finds a blocker.
- Does not claim that a test passed without a run report.

### Coder

The coder is an agent that can inspect files and run commands.

The coder:

- Reads the digest, facts, and approved skeletons.
- Checks assumptions before it relies on them.
- Runs the exact checks in each skeleton.
- Saves one run report for every check attempt or probe.
- Updates facts only when a run report proves them.
- Stops after three failed attempts for one check.
- Does not redesign a feature when a skeleton is unclear.

## 3. The three workspace areas

| Area | Purpose | Content |
| --- | --- | --- |
| `Ideas/` | Explain what and why | Requirements, decisions, research, risks, and open questions. |
| `Skeletons/` | Explain how code should work | Pseudo-code, types, function outlines, data shapes, checks, and edge cases. |
| Configured code folder | Hold the actual implementation | Working application source code. |

Do not put real application code in `Skeletons/`. Do not use `Ideas/` as a substitute for a code blueprint.

## 4. Folder layout

The default layout is:

```text
my-workspace/
├── AGENTS.md
├── CHATGPT.md
├── CLAUDE.md
├── PLANNER-START.md
├── README.md
├── STAGESET.md
├── ideations-rules.md
├── coder-rules.md
├── Ideas/
├── Skeletons/
│   └── Probes/
├── Code/
├── .stageset/
│   ├── config.yml
│   ├── DIGEST.md                 # Generated
│   ├── facts.md                  # Verified facts
│   ├── formats.md
│   ├── sessions-tracker.md       # Generated
│   ├── sessions/                 # One event file per session
│   ├── runs/                     # One report per command run
│   ├── escalations/              # Generated after 3 failed attempts
│   └── templates/
└── scripts/
    └── stageset-status.py
```

The `Code/` folder is only the default. You can change it to any folder or use `.` as the code root.

## 5. Custom workspace paths

Edit `.stageset/config.yml` to set `workspace.root`, `code_dir`, `ideas_dir`, and `skeletons_dir`.

All four values are paths. `workspace.root` is relative to the repository root. The other three paths are relative to `workspace.root`.

If your project code lives in `custom-hyper/` and you want `Ideas/` and `Skeletons/` inside it, use:

```yaml
workspace:
  root: "custom-hyper"
  code_dir: "."
  ideas_dir: "Ideas"
  skeletons_dir: "Skeletons"
```

The result is:

```text
my-workspace/
├── .stageset/
├── scripts/
└── custom-hyper/
    ├── Ideas/
    ├── Skeletons/
    ├── src/
    └── ...real project files...
```

If the code lives in `custom-hyper/` but planning folders stay at the repository root, use:

```yaml
workspace:
  root: "."
  code_dir: "custom-hyper"
  ideas_dir: "Ideas"
  skeletons_dir: "Skeletons"
```

Keep `.stageset/` and `scripts/` at the repository root. The tracking and evidence paths in the config are relative to the repository root.

## 6. File path and skeleton rules

An implementation skeleton mirrors the path of its target source file.

Example:

```text
Code/src/audio/router.ts
Skeletons/src/audio/router.ts
```

The skeleton at `Skeletons/src/audio/router.ts` describes `Code/src/audio/router.ts`.

Set `@stageset target` to the path relative to the configured code directory. A target can be new and does not need to exist yet.

For a target that does not support comments, use a Markdown sidecar file. Add `.skeleton.md` after the target file name. For example, `Skeletons/config/settings.json.skeleton.md` describes `Code/config/settings.json`.

Keep one target source file per implementation skeleton. If one source file is too large to plan as a whole, limit the skeleton to one function in that file. State the function name in `Purpose` and `Contract`. Split unrelated files into separate skeletons. Keep each skeleton small and precise.

Treat the skeleton as the implementation contract. If a required step is impossible in the real project, the coder must not deviate silently. The coder must stop the affected work, write a run report with the exact conflict and observed evidence, set the skeleton to `BLOCKED`, set `blocker_ref` to that report, and ask the planner to revise the skeleton.

## 7. Revisions and implementation state

Each implementation skeleton has two revision numbers:

- `spec_revision` — the latest planned version.
- `implemented_revision` — the version that the real code fully implements.

A skeleton is ready for coding when:

```text
status is READY or IN_PROGRESS
AND
spec_revision > implemented_revision
```

After the coder implements and verifies the complete revision:

- Set `implemented_revision` to `spec_revision`.
- Set `status` to `DONE`.
- Set `implemented_in` to the coding event file path.

When the planner changes a skeleton:

- Increase `spec_revision` by one.
- Keep `implemented_revision` unchanged.
- Set `status` to `READY` when the plan is clear.
- Update `planned_in` and `last_updated_in` with the session event file path.
- Keep the implementation history.

Never mark a skeleton as `DONE` before the checks pass.

## 8. Checks are test contracts

Every implementation skeleton must include a `## Checks` section.

Each check must have a unique ID across the workspace. Use a name such as `CHECK-AUDIO-ROUTER-01`.

Each check must state:

- The exact command.
- The predicted output.
- The pass condition.
- The fail condition.

A check must prove a clear result. Do not use vague checks such as "works correctly".

The coder records the exact command and observed output in a run report. The planner compares the report with the predicted output.

## 9. Assumptions and verified facts

Use `ASSUMPTION:` for a claim that is not yet verified. Give it an ID.

Example:

```text
ASSUMPTION: A-01 — The installed library returns a tensor with shape [1, 80, 300]. [UNVERIFIED]
```

Before the coder relies on the assumption, it must check it. Use a cheap, read-only command where possible.

The coder records the result in a run report. Use `CONFIRMED` or `REFUTED`. Include the exact command and evidence. If an assumption is refuted, the coder stops the affected work and marks the skeleton as blocked. The planner must resolve it.

Only confirmed facts belong in `.stageset/facts.md`. Each fact must link to a run report. Do not record guesses as facts.

## 10. Probes

A probe is a small, read-only task. Use it when the planner needs a fact that it cannot get from the repository alone.

Examples:

- Print library versions.
- Inspect tensor shapes.
- Check whether a device supports a data type.
- Test a read-only API call.
- Inspect an installed command or configuration.

Store probe skeletons in `Skeletons/Probes/`. Use `kind: PROBE` and `target: -`.

A probe must not change project files, databases, services, or external state. It must not expose credentials or secrets.

The coder runs the probe and saves a `PROBE` run report. The planner uses the result to make an informed decision.

## 11. Run reports and evidence

Store one report for each check attempt or probe in `.stageset/runs/`.

Use a timestamp ID in the format `YYYYMMDD-HHMMSS-RUN`. Generate it with `python scripts/stageset-status.py --new-run-id`. Save the report as `.stageset/runs/<id>.md`. The script adds a numeric suffix if the same-second ID already exists. Never overwrite a report. Set `spec_revision` to the exact skeleton revision that the report checks. Start `attempt` at 1 for each check and skeleton revision.

Use `.stageset/templates/run-report-template.md`. Every report must include:

- Goal.
- Exact commands.
- Observed output.
- Result: `PASS`, `FAIL`, or `BLOCKED`.
- Facts.
- Guesses.
- Assumptions checked.
- Actions tried.
- Open question for the planner.
- Attempt diff.
- Smallest reproduction, when relevant.

Keep facts and guesses separate. Trim output only when necessary. State when you trim it.

The coder must not report a pass without the actual result. The planner must not treat a guess as evidence.

## 12. Blockers and escalation

Allow a maximum of three attempts for one check and skeleton revision. Start a new attempt sequence only after the planner raises `spec_revision`.

After the third failed attempt, the coder must:

1. Stop work on that check.
2. Set the skeleton status to `BLOCKED`.
3. Set `blocker_ref` to the third run report path.
4. Run `python scripts/stageset-status.py --escalate CHECK-ID`.
5. Send the generated escalation file and run reports to the planner.

The escalation file contains the skeleton, failed command, observed errors, attempt changes, and smallest reproduction. The script gives it a timestamp ID in the format `YYYYMMDD-HHMMSS-ESCALATION`, with a numeric suffix if needed.

The planner reads the evidence. The planner updates the skeleton to resolve the problem. The planner increases `spec_revision`, sets `status: READY`, sets `blocker_ref: -`, and sets `resolution_of` to the latest run ID.

The coder implements only the revised skeleton. The coder must not redesign the feature.

## 13. Session events and generated tracker

Store one event file for each focused session in `.stageset/sessions/`.

Use `.stageset/templates/session-event-template.md`. Allowed event types are:

- `IDEATION`
- `PROBE`
- `CODING`
- `PUSH`
- `MAINTENANCE`

A chat app that cannot read the local clock must set `time: PENDING`. After the event file is committed, the script reads the Git commit time.

The event file path is the stable reference used by skeleton metadata. The generated event ID uses `YYYYMMDD-HHMMSS-TYPE`. The script adds a numeric suffix only when IDs collide.

The script generates `.stageset/sessions-tracker.md`. Do not edit it by hand. The tracker is one view of the event files.

A local commit is not a push. Add a `PUSH` event only after the remote push succeeds. Include the remote, branch, and commit ID.

## 14. Digest and status commands

The digest is the first file that a phone planner should read. It shows:

- Ready skeletons.
- Open blockers.
- Failing checks.
- The last five sessions.
- Verified environment facts.

Run these commands from the repository root:

```bash
# Show ready work, blockers, and event totals.
python scripts/stageset-status.py

# Print machine-readable status.
python scripts/stageset-status.py --json

# Rebuild the tracker and digest after you add event, run, or skeleton files.
python scripts/stageset-status.py --sync

# Rebuild only the digest.
python scripts/stageset-status.py --digest

# Generate a timestamp-based ID for a new run report.
python scripts/stageset-status.py --new-run-id

# Check file formats, paths, statuses, reports, and generated files.
python scripts/stageset-status.py --validate

# Build an escalation file after three failed attempts.
python scripts/stageset-status.py --escalate CHECK-AUDIO-ROUTER-01
```

The script uses only the Python standard library. It does not run project code. `--validate` reports unresolved `PENDING` times when a file has no Git commit.

Run `--sync` after the new session or run files are committed. Then run `--validate`.

## 15. Rollback and history

StageSet changes are normal Git commits. Keep the base repository and its history. Do not delete old session events or run reports.

The repository maintains a pre-evidence snapshot branch named `backup/pre-evidence-workflow-2026-11-01`. To inspect that version in a clone:

```bash
git fetch origin
git switch -track origin/backup/pre-evidence-workflow-2026-11-01
```

To undo a later change on `main`, revert the relevant commit. Do not force-push over shared history.

## 16. Source of truth

- `Ideas/` records intent and decisions.
- `Skeletons/` records the planned code shape and test contract.
- The configured code directory records what is implemented.
- `.stageset/runs/` records observed command results.
- `.stageset/facts.md` records facts that run reports prove.
- `.stageset/sessions/` records the source event files.
- `.stageset/sessions-tracker.md` is a generated view of session events.
- `.stageset/DIGEST.md` is a generated summary for planners and coders.
- `.stageset/config.yml` records workspace paths and shared settings.

When two sources disagree, report the conflict. Resolve it before implementation.

## 17. Writing rules

Use ASD-STE100-style English in all project documents, comments, skeletons, run reports, and event summaries.

- Use short sentences.
- Use simple words.
- Use active voice.
- Give one instruction at a time.
- Use one name for one concept.
- Explain technical terms when the reader may not know them.
- State facts, assumptions, decisions, and questions separately.

Keep code syntax, identifiers, and required technical terms exact.
