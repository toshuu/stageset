# StageSet

StageSet is a planning-first workspace system for software projects built with AI.

A capable model plans the work. It records decisions in `Ideas/` and writes file-level blueprints in `Skeletons/`. A smaller coding agent implements those blueprints in the configured code folder.

The planner and coder share evidence. The coder records exact commands and observed results in `.stageset/runs/`. The planner reads those reports. Verified environment facts live in `.stageset/facts.md`.

## Start a new workspace

```bash
git clone https://github.com/toshuu/stageset.git my-workspace
cd my-workspace
```

Then:

1. Read `.stageset/DIGEST.md`.
2. Edit `.stageset/config.yml` to match your folder layout.
3. Read `STAGESET.md`.
4. Read `CHATGPT.md` before planning in the ChatGPT app.
5. Read `ideations-rules.md` before planning in ChatGPT or Claude.
6. Read `coder-rules.md` before coding with an agent.
7. Use `PLANNER-START.md` to start a planning chat.
8. Run `python scripts/stageset-status.py` to see ready work.

Important: ChatGPT mobile and web apps do not automatically read `CHATGPT.md` from GitHub. Attach the file or provide repository access. Claude Code can use `CLAUDE.md`. Coding agents can use `AGENTS.md`.

## Folder layout

```text
my-workspace/
├── AGENTS.md
├── CHATGPT.md
├── CLAUDE.md
├── PLANNER-START.md
├── STAGESET.md
├── ideations-rules.md
├── coder-rules.md
├── Ideas/
├── Skeletons/
│   └── Probes/
├── Code/                         # Default real source folder
├── .stageset/
│   ├── config.yml
│   ├── DIGEST.md                 # Generated
│   ├── facts.md                  # Verified facts
│   ├── formats.md
│   ├── sessions-tracker.md       # Generated
│   ├── sessions/                 # One file per session event
│   ├── runs/                     # One report per run
│   ├── escalations/              # Built after 3 failed attempts
│   └── templates/
└── scripts/
    └── stageset-status.py
```

## Custom project folder

If your real code and StageSet folders live inside `custom-hyper/`, use:

```yaml
workspace:
  root: "custom-hyper"
  code_dir: "."
  ideas_dir: "Ideas"
  skeletons_dir: "Skeletons"
```

The folder names are configurable. The `.stageset/` and `scripts/` folders stay at the repository root.

## Evidence IDs

Run reports use timestamp IDs in the format `YYYYMMDD-HHMMSS-RUN`. Generate a new ID with:

```bash
python scripts/stageset-status.py --new-run-id
```

Escalation files use `YYYYMMDD-HHMMSS-ESCALATION`. The script adds a numeric suffix when it finds a same-second ID. Run reports, escalation files, and session events use timestamp-based IDs. There is no global sequential counter.

## Revision rule

The coder finds work by comparing revisions:

```text
status is READY or IN_PROGRESS
AND
spec_revision > implemented_revision
```

This identifies the skeletons that contain new work. It does not depend on a manual session-number comparison.

## Evidence workflow

1. The planner writes an idea and a detailed skeleton.
2. The skeleton defines exact checks and predicted output.
3. The coder verifies assumptions before it relies on them.
4. The coder runs each check and saves one report per attempt.
5. The coder records verified facts with links to run reports.
6. After three failed attempts, the coder stops and creates an escalation file.
7. The planner resolves the evidence and updates the skeleton revision.

A probe is a small read-only task. It can verify a library version, tensor shape, GPU feature, or API behavior.

## Useful commands

```bash
python scripts/stageset-status.py
python scripts/stageset-status.py --json
python scripts/stageset-status.py --sync
python scripts/stageset-status.py --digest
python scripts/stageset-status.py --validate
python scripts/stageset-status.py --escalate CHECK-ID
```

The script uses only the Python standard library. It does not run project code. The `--sync` command generates the session tracker and digest. Do not edit those generated files by hand.

## Rollback

The pre-evidence version is preserved on `backup/pre-evidence-workflow-2026-11-01`. Inspect it with:

```bash
git fetch origin
git switch --track origin/backup/pre-evidence-workflow-2026-11-01
```

Use Git commits to compare or revert later changes. Do not force-push over shared history.

See `STAGESET.md` for the full protocol.
