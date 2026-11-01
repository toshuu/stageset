# StageSet formats and conventions

## Global event IDs

Use `SS-` followed by six digits. Start at `SS-000001`.

The sequence covers ideation, coding, pushes, and maintenance. The sequence does not restart for a new event type.

## Idea IDs

Use `IDEA-` followed by four digits. Find the highest existing ID in idea front matter. Add one to get the next ID.

## Skeleton metadata

Use the exact fields in `templates/skeleton-template.txt`. Place the fields in the first comment block of the skeleton. Use the normal comment syntax for the target language.

## Revisions

Increase `spec_revision` when the planned behavior or structure changes. Do not increase it for spelling or formatting changes that do not change the plan.

Set `implemented_revision` only when the real code implements that full revision and the required checks pass.

A skeleton is actionable when:

```text
status is READY or IN_PROGRESS
AND
spec_revision > implemented_revision
```

## Timestamps

Use ISO 8601 with the UTC offset. The default timezone is `Asia/Kolkata`.

Example format: `2026-11-01T21:00:00+05:30`.

Use the actual time. Do not copy the example timestamp into a real event.

## Priority

- `P0` — urgent. Blocks a release or core use.
- `P1` — high priority.
- `P2` — normal priority.
- `P3` — low priority.

## Skeleton file names

When the target language supports comments, use the same relative path and file name as the target source file. Put the `@stageset` metadata in the first comment block.

When the target format does not support comments, use a Markdown sidecar file. Add `.skeleton.md` after the target file name. Example: `Skeletons/config/settings.json.skeleton.md` targets `config/settings.json`. Set `@stageset target` to `config/settings.json`. The directory path must still mirror the target directory path.

## Global sequence rules

Reserve one global event ID at the start of each focused session. Use it in files changed during that session. Add one tracker row when the session ends. Re-read the tracker before saving if another writer may have changed it. Never reuse an ID.
