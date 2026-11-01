#!/usr/bin/env python3
"""Find StageSet skeletons that need implementation and summarize activity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = re.compile(r"@stageset\s+([a-z_]+):\s*(.*?)\s*$")
EVENT = re.compile(r"^\|\s*(SS-\d{6})\s*\|\s*(IDEATION|CODING|PUSH|MAINTENANCE)\s*\|", re.I)


def config_values(path: Path) -> dict[str, str]:
    """Read the simple workspace and tracking sections in config.yml."""
    if not path.is_file():
        raise ValueError(f"Config file not found: {path}")
    result: dict[str, str] = {}
    section = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        indent, key, value = match.groups()
        value = value.split(" #", 1)[0].strip().strip("\\\"'")
        if not indent:
            section = key if not value else ""
        elif len(indent) == 2 and section == "workspace":
            result[key] = value
        elif len(indent) == 2 and section == "tracking":
            result[f"tracking.{key}"] = value
    return result


def inside_repo(base: Path, value: str, label: str) -> Path:
    path = (base / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the repository: {value}") from exc
    return path


def read_skeleton(path: Path) -> dict:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:80]:
        match = META.search(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    required = ("target", "source_idea", "status", "priority", "spec_revision",
                "implemented_revision", "planned_in", "last_updated_in", "implemented_in")
    missing = [key for key in required if not fields.get(key)]
    relative = path.relative_to(ROOT).as_posix()
    if missing:
        return {"file": relative, "error": "missing metadata: " + ", ".join(missing)}
    target = Path(fields["target"])
    if target.is_absolute() or ".." in target.parts:
        return {"file": relative, "error": "target must be a safe relative path"}
    try:
        spec = int(fields["spec_revision"])
        implemented = int(fields["implemented_revision"])
    except ValueError:
        return {"file": relative, "error": "revision values must be integers"}
    return {
        "file": relative, "target": fields["target"],
        "source_idea": fields["source_idea"], "status": fields["status"].upper(),
        "priority": fields["priority"].upper(), "spec_revision": spec,
        "implemented_revision": implemented, "planned_in": fields["planned_in"],
        "last_updated_in": fields["last_updated_in"], "implemented_in": fields["implemented_in"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    try:
        cfg = config_values(ROOT / ".stageset" / "config.yml")
        workspace = inside_repo(ROOT, cfg.get("root", "."), "workspace.root")
        code = inside_repo(workspace, cfg.get("code_dir", "Code"), "workspace.code_dir")
        skeleton_dir = inside_repo(workspace, cfg.get("skeletons_dir", "Skeletons"), "workspace.skeletons_dir")
        tracker = inside_repo(ROOT, cfg.get("tracking.sessions_tracker", ".stageset/sessions-tracker.md"), "sessions_tracker")
        if not skeleton_dir.is_dir():
            raise ValueError(f"Skeleton directory not found: {skeleton_dir}")

        items = [read_skeleton(p) for p in sorted(skeleton_dir.rglob("*")) if p.is_file() and p.name != "README.md"]
        metadata_issues = [x for x in items if "error" in x]
        valid = [x for x in items if "error" not in x]
        pending = [x for x in valid if x["status"] in {"READY", "IN_PROGRESS"} and x["spec_revision"] > x["implemented_revision"]]
        blocked = [x for x in valid if x["status"] == "BLOCKED"]
        revision_issues = [x for x in valid if
            (x["status"] == "DONE" and x["spec_revision"] > x["implemented_revision"]) or
            (x["status"] in {"READY", "IN_PROGRESS"} and x["spec_revision"] <= x["implemented_revision"])]

        events = []
        if tracker.is_file():
            for line in tracker.read_text(encoding="utf-8").splitlines():
                match = EVENT.match(line)
                if match:
                    events.append({"id": match.group(1), "type": match.group(2).upper()})
        counts = Counter(x["type"] for x in events)
        latest = {}
        for event in events:
            latest[event["type"]] = event

        data = {
            "workspace_root": workspace.relative_to(ROOT).as_posix() or ".",
            "code_root": code.relative_to(ROOT).as_posix() or ".",
            "skeleton_root": skeleton_dir.relative_to(ROOT).as_posix() or ".",
            "last_event": events[-1] if events else None,
            "latest_by_type": latest,
            "event_counts": dict(sorted(counts.items())),
            "pending": pending, "blocked": blocked,
            "metadata_issues": metadata_issues, "revision_status_issues": revision_issues,
        }
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("StageSet status")
            print(f"Workspace: {data['workspace_root']} | Code: {data['code_root']}")
            print(f"Skeletons: {data['skeleton_root']}")
            print("Events: " + (", ".join(f"{k}={v}" for k, v in data["event_counts"].items()) or "none"))
            if latest:
                print("Latest events: " + ", ".join(f"{k}={v['id']}" for k, v in sorted(latest.items())))
            print(f"\nPending skeletons: {len(pending)}")
            for item in pending:
                print(f"- [{item['priority']}] {item['file']} -> {item['target']} (spec {item['spec_revision']}, implemented {item['implemented_revision']})")
            print(f"\nBlocked: {len(blocked)} | Metadata issues: {len(metadata_issues)} | Revision issues: {len(revision_issues)}")
            for issue in metadata_issues + revision_issues:
                print(f"- {issue['file']}: {issue.get('error', 'status and revision values conflict')}")
            if not pending:
                print("No ready skeleton revision is waiting for implementation.")
        return 1 if metadata_issues or revision_issues else 0
    except (OSError, ValueError) as exc:
        print(f"StageSet error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
