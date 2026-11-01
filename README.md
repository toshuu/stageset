# StageSet

StageSet is a planning-first workspace system for software projects built with AI.

It keeps three layers separate:

| Folder | Purpose |
| --- | --- |
| `Ideas/` | What the project needs and why. |
| `Skeletons/` | How each planned source file must work. |
| Configured code folder | The real implementation. |

A strong model can help with exploration and design. It records decisions in `Ideas/` and prepares detailed file-level blueprints in `Skeletons/`. A smaller coding model can then implement those blueprints without repeating the full design process.

## Start a new workspace

Clone this repository into a new project workspace:

```bash
git clone https://github.com/toshuu/stageset.git my-workspace
cd my-workspace
```

Then:

1. Read [`STAGESET.md`](STAGESET.md).
2. Edit [`.stageset/config.yml`](.stageset/config.yml) to match your folder layout.
3. Read [`ideations-rules.md`](ideations-rules.md) before planning with ChatGPT or Claude.
4. Read [`coder-rules.md`](coder-rules.md) before coding with an agent.
5. Use [`PLANNER-START.md`](PLANNER-START.md) to start a planning chat.
6. Run `python scripts/stageset-status.py` to see which skeletons need implementation.

To make the workspace its own GitHub repository, create an empty repository for the project and change the `origin` remote before the first push. Keep this StageSet repository as the reusable base.

## Folder layout

```text
my-workspace/
├── AGENTS.md                 # General coding-agent entry point
├── CLAUDE.md                 # Claude Code entry point
├── STAGESET.md               # Complete system guide
├── ideations-rules.md        # Rules for ChatGPT, Claude, and planners
├── coder-rules.md            # Rules for implementation agents
├── PLANNER-START.md          # Prompt for a planning chat
├── Ideas/                    # Project decisions and plans
├── Skeletons/                # File-level implementation blueprints
├── Code/                     # Default real source folder
├── .stageset/
│   ├── config.yml            # Workspace paths and shared settings
│   ├── sessions-tracker.md   # One global activity log
│   ├── formats.md            # IDs, revisions, and file formats
│   └── templates/            # New idea, skeleton, and session templates
└── scripts/
    └── stageset-status.py    # Find ready skeletons and summarize sessions
```

The `Code/` folder is only the default. You can change it to any folder or use `.` as the code root.

## Existing project folder

If your project code lives in `custom-hyper/` and you want `Ideas/` and `Skeletons/` inside that folder, set:

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

Keep `.stageset/` and `scripts/` at the repository root. The tracker path is relative to the repository root. The other workspace paths are relative to `workspace.root`.

## Key rule: revisions, not guesswork

Each skeleton has two revision numbers:

- `spec_revision`: the latest planned version.
- `implemented_revision`: the version that the real code fully implements.

A skeleton is waiting for work when its status is `READY` or `IN_PROGRESS` and:

```text
spec_revision > implemented_revision
```

Run the status helper to find this work:

```bash
python scripts/stageset-status.py
python scripts/stageset-status.py --json
```

The helper does not edit files. It uses only the Python standard library.

## Session history

`.stageset/sessions-tracker.md` records ideation, coding, confirmed remote pushes, and maintenance events in one global sequence. The IDs look like `SS-000001`. The event type identifies the activity. The helper calculates totals from the tracker. Do not maintain separate counters by hand.

## Important boundaries

- Brainstorming does not change files. Save only when the user asks.
- Planners write intent in `Ideas/` and implementation plans in `Skeletons/`.
- Coding agents change real source files and update skeleton implementation metadata only after checks pass.
- A local commit is not a remote push.
- Do not invent timestamps, test results, commit IDs, or push results.
- Use ASD-STE100-style English in project documents, comments, and session summaries.

See [`STAGESET.md`](STAGESET.md) for the complete workflow and rules.
