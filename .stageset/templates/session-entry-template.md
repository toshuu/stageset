# Deprecated session template

StageSet version 2 uses one event file per focused session.

Use `.stageset/templates/session-event-template.md` instead.

Do not add rows to `.stageset/sessions-tracker.md` by hand. The status script generates the tracker from files in `.stageset/sessions/`.

Use `time: PENDING` when the app cannot read the local clock. The status script resolves the time from the event file's Git commit time.
