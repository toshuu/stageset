# StageSet system guide

## 1. Purpose

StageSet separates planning from implementation.

A planner uses a capable model to think through a feature. The planner records clear decisions in `Ideas/`. The planner also writes implementation blueprints in `Skeletons/`.

A coding agent reads the blueprints before it changes real code. The coding agent works in the configured code directory.

This lets a smaller coding model work from a clear plan. It does not need to repeat the full design process.

## 2. The three workspace areas

| Area | Purpose | Content |
| --- | --- | --- |
| `Ideas/` | Explain what and why | Markdown plans, requirements, decisions, research, and open questions |
| `Skeletons/` | Explain how code should work | Pseudo-code, interfaces, function outlines, data shapes, comments, and edge cases |
| Configured code folder | Hold the actual implementation | Working application source code |

Do not put real application code in `Skeletons/`. Do not use `Ideas/` as a substitute for a code blueprint.

## 3. Mirrored file paths

The relative directory path of a skeleton must match the relative directory path of its target source file.

Example:

```text
Code/
  src/
    audio/
      router.ts

Skeletons/
  src/
    audio/
      router.ts
```

The skeleton at `Skeletons/src/audio/router.ts` describes the real file at `Code/src/audio/router.ts`.

The configured workspace paths can change. The mirror rule does not change.

A skeleton can describe a new file that does not exist in the code directory yet.

## 4. Custom workspace paths

StageSet does not require the real source folder to be named `Code`.

Edit `.stageset/config.yml` to set `workspace.root`, `code_dir`, `ideas_dir`, and `skeletons_dir`.

All four values are paths relative to the repository root, except that the three directory values are resolved relative to `workspace.root`.

For a project folder named `custom-hyper`, where the real source files, `Ideas/`, and `Skeletons/` all live inside that folder, use:

```yaml
workspace:
  root: "custom-hyper"
  code_dir: "."
  ideas_dir: "Ideas"
  skeletons_dir: "Skeletons"
```

This means the layout is:

```text
custom-hyper/
  Ideas/
  Skeletons/
  ...real source files...
```

Keep `.stageset/` and `scripts/` at the repository root. The tracker path is relative to the repository root. The other workspace paths are relative to `workspace.root`.

### Alternative: code in a subfolder, planning folders at the repository root

If the code is in `custom-hyper/` but `Ideas/` and `Skeletons/` stay at the repository root, use:

```yaml
workspace:
  root: "."
  code_dir: "custom-hyper"
  ideas_dir: "Ideas"
  skeletons_dir: "Skeletons"
```

Choose one layout. Do not move the folders without updating the configuration.

## 5. The session tracker

`.stageset/sessions-tracker.md` is the shared activity record.

It records these event types:

- `IDEATION` — one focused planning session.
- `CODING` — one focused implementation session.
- `PUSH` — one confirmed push to a remote Git repository.
- `MAINTENANCE` — a StageSet structure or metadata change.

Every row gets one global ID. Start with `SS-000001`. Increase the number by one for every new row. Do not reuse an ID. Reserve the next ID at the start of a focused session. Re-read the tracker before saving if another person or agent may have changed it.

The tracker is the source of truth for session order. Use the status helper to count event types. Do not keep separate counters that can become inconsistent.

Use an ISO 8601 timestamp with the configured timezone and UTC offset. The default timezone is `Asia/Kolkata`.

Only add a `PUSH` row after the remote push succeeds. A local commit is not a push.

The helper `scripts/stageset-status.py` reads the tracker and calculates event totals. Do not keep separate manual totals. It also lists skeletons that need implementation.

## 6. Skeleton revision tracking

Each source skeleton has a small metadata header inside its normal language comments. Use the exact field names shown in `.stageset/templates/skeleton-template.txt`.

The most important fields are:

- `spec_revision` — the current version of the plan for this file.
- `implemented_revision` — the version that the real code currently implements.
- `status` — the current implementation state.

A coding agent must implement a skeleton when all these conditions are true:

```text
status is READY or IN_PROGRESS
AND
spec_revision > implemented_revision
```

The normal ready state is `READY`. A coding agent can also continue an item with status `IN_PROGRESS`.

After it implements and verifies a revision, the coding agent sets `implemented_revision` to `spec_revision` and sets `status` to `DONE`.

When a planner changes a skeleton after implementation, the planner must increase `spec_revision`, set `status` to `READY`, and record the new planning session. The planner must not lower `implemented_revision`.

This revision check is more reliable than comparing only session numbers. It identifies the exact skeleton files that have new work.

## 7. Status values

Skeleton status values:

| Status | Meaning |
| --- | --- |
| `DRAFT` | The plan is not ready for implementation. |
| `READY` | The plan is clear and ready for implementation. |
| `IN_PROGRESS` | Implementation has started but is not complete. |
| `DONE` | The real code implements the current skeleton revision. |
| `BLOCKED` | A known issue prevents safe implementation. |
| `SUPERSEDED` | A newer plan replaces this skeleton. |

Idea status values:

| Status | Meaning |
| --- | --- |
| `DISCOVERY` | The idea is under discussion. |
| `CLARIFIED` | The problem and expected result are clear. |
| `DECIDED` | The main decision is approved. |
| `READY_FOR_SKELETON` | The idea is ready for code-level planning. |
| `SKELETONIZED` | The required skeletons exist. |
| `IMPLEMENTED` | The related implementation is complete. |
| `PARKED` | Work is paused. |
| `REJECTED` | The idea will not be implemented. |

## 8. Planning workflow

1. Read this file, the config, the session tracker, and relevant existing files.
2. Review the real code and related skeletons before making a new plan.
3. Discuss the idea. Do not write to the repository until the user asks to save or publish the result.
4. Create or update the relevant Markdown files in `Ideas/`.
5. When the design is clear, create or update the matching skeleton files in `Skeletons/`.
6. Update skeleton metadata and the related idea links.
7. Add one `IDEATION` row to the session tracker when the focused session is complete.

A planning session can create an idea without creating a skeleton. Do not mark unclear work as `READY`.

## 9. Coding workflow

1. Read this file, the config, `coder-rules.md`, and the latest session entries.
2. Find every skeleton with `spec_revision > implemented_revision` and status `READY` or `IN_PROGRESS`.
3. Read the related idea files and the matching real source files.
4. Implement only the agreed scope.
5. Run relevant checks and tests.
6. Update the skeleton metadata after successful implementation.
7. Add one `CODING` row to the tracker.
8. Add a separate `PUSH` row only after a successful remote push.

If a skeleton is unclear or conflicts with the real code, stop that part of the work. Record the blocker. Do not guess at a major design decision.

For files that do not support comments, use a Markdown sidecar skeleton. Name it by adding `.skeleton.md` after the target file name. For example, `Skeletons/config/settings.json.skeleton.md` can describe `Code/config/settings.json`. Keep the `@stageset target` value set to the exact target path. The folder path must still mirror the target folder path.

## 10. File and writing rules

- Use ASD-STE100-style English in all human-written project documents and comments.
- Use short sentences.
- Use one instruction per sentence.
- Prefer active voice.
- Use one name for one concept.
- Explain an acronym at first use.
- State assumptions and unresolved questions.
- Do not remove existing content unless the user approves the change.
- Do not invent timestamps, test results, commits, or push results.

Code syntax and required API names must remain exact. The writing rules do not change programming language syntax.

## 11. Status helper

Run the status helper before a coding session:

```bash
python scripts/stageset-status.py
```

Use `--json` when an agent needs machine-readable output. The helper does not change any file. It reads the configuration, scans skeleton metadata, and summarizes tracker events. If the helper reports a metadata or revision conflict, resolve that conflict before implementation.

## 12. Source of truth

- `Ideas/` records intent and decisions.
- `Skeletons/` records the planned code shape and expected behavior.
- The configured code directory records what is actually implemented.
- `.stageset/sessions-tracker.md` records the order of work and confirmed pushes.
- `.stageset/config.yml` records the workspace paths and shared settings.

When two sources disagree, do not hide the conflict. Report it and resolve it before implementation.
