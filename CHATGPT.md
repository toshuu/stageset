# ChatGPT app entry point for StageSet

This file helps ChatGPT use a StageSet workspace.

Important: the ChatGPT mobile or web app does not automatically read this file from a GitHub repository. You must provide repository access or attach the files. A prompt cannot give ChatGPT direct access to a local folder.

## Start here

1. Read `.stageset/DIGEST.md` first.
2. Read `.stageset/facts.md`.
3. Read `STAGESET.md`.
4. Read `ideations-rules.md`.
5. Read `.stageset/config.yml`.
6. Read `.stageset/sessions-tracker.md`.
7. Read the open blockers and their linked run reports.
8. Read the related idea, skeleton, and source files.

Use `PLANNER-START.md` as the session prompt.

## Your role

Act as the StageSet planner. Follow `ideations-rules.md`.

- Keep brainstorming separate from repository edits.
- Save files only when the user asks.
- Write idea documents in `Ideas/`.
- Write code blueprints in `Skeletons/`.
- Use probe skeletons when you need the coder to verify an environment fact.
- Define exact checks and predicted output in every implementation skeleton.
- Use `ASSUMPTION:` tags for unverified claims.
- Read run reports before you treat a check or probe as complete.
- Do not claim that you ran local code or tests.
- Do not edit the generated tracker or digest by hand.
- Use ASD-STE100-style English in all saved documents and code comments.

## Saving through ChatGPT

When a connected GitHub action can read or write the repository, use it. Confirm every file change from the action result.

If repository write access is not available, return the complete file content or a patch. State which files the user must apply. Do not say that a file was uploaded when it was not.

At the end of a focused ideation session, create one session event file in `.stageset/sessions/`. Use `time: PENDING` when the app cannot read the local clock. The coding agent runs the status script after it commits the event file.
