#!/usr/bin/env python3
"""List actionable StageSet skeletons and summarize the session tracker.

This script uses only the Python standard library. It reads the simple YAML
structure in .stageset/config.yml. It does not modify workspace files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SECTION_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)$")
META_RE = re.compile(r"@stageset\s+(?P<key>[a-z_]+):\s*(?P<value>.*?)\s*$")
EVENT_RE = re.compile(r"^\|\s*(SS-\d{6})\s*\|\s*(IDEATION|CODING|PUSH|MAINTENANCE)\s*\|", re.I)


def scalar(value: str) -> str:
    value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_config(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise ValueError(f"Config file not found: {path}")

    values: dict[str, str] = {}
    current_section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = SECTION_RE.match(line)
        if not match:
            continue
        indent = len(match.group("indent").replace("\t", "  "))
        key = match.group("key")
        value = scalar(match.group("value"))
        if indent == 0:
            current_section = key if value == "" else None
        elif indent == 2 and current_section == "workspace":
            values[key] = value
        elif indent == 2 and current_section == "tracking":
            values[f"tracking.{key}"] = value
    return values


def safe_join(base: Path, relative: str, label: str) -> Path:
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the repository: {relative}") from exc
    return candidate


def parse_skeleton(path: Path) -> dict[str, Any]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:80]:
        match = META_RE.search(line)
        if match:
            fields[match.group("key")] = match.group("value").strip()

    required = (
        "target", "status", "spec_revision", "implemented_revision", "planned_in",
        "last_updated_in", "implemented_in", "source_idea", "priority",
    )
    missing = [name for name in required if not fields.get(name)]
    if missing:
        return {"file": path.relative_to(REPO_ROOT).as_posix(), "error": "missing metadata: " + ", ".join(missing)}

    try:
        spec_revision = int(fields["spec_revision"])
        implemented_revision = int(fields["implemented_revision"])
    except ValueError:
        return {"file": path.relative_to(REPO_ROOT).as_posix(), "error": "revision fields must be integers"}

    target = Path(fields["target"])
    if target.is_absolute() or ".." in target.parts:
        return {"file": path.relative_to(REPO_ROOT).as_posix(), "error": "target must be a safe relative path"}

    return {
        "file": path.relative_to(REPO_ROOT).as_posix(),
        "target": fields["target"],
        "source_idea": fields["source_idea"],
        "status": fields["status"].upper(),
        "priority": fields["priority"].upper(),
        "spec_revision": spec_revision,
        "implemented_revision": implemented_revision,
        "planned_in": fields["planned_in"],
        "last_updated_in": fields["last_updated_in"],
        "implemented_in": fields["implemented_in"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    try:
        config = read_config(REPO_ROOT / ".stageset" / "config.yml")
        workspace_root = safe_join(REPO_ROOT, config.get("root", "."), "workspace.root")
        code_root = safe_join(workspace_root, config.get("code_dir", "Code"), "workspace.code_dir")
        skeleton_root = safe_join(workspace_root, config.get("skeletons_dir", "Skeletons"), "workspace.skeletons_dir")
        tracker_path = safe_join(REPO_ROOT, config.get("tracking.sessions_tracker", ".stageset/sessions-tracker.md"), "tracking.sessions_tracker")

        if not skeleton_root.is_dir():
            raise ValueError(f"Skeleton directory not found: {skeleton_root}")

        skeletons = [
            parse_skeleton(path)
            for path in sorted(skeleton_root.rglob("*"))
            if path.is_file() and path.name != "README.md"
        ]
        issues = [item for item in skeletons if "error" in item]
        valid = [item for item in skeletons if "error" not in item]
        pending = [
            item for item in valid
            if item["status"] in {"READY", "IN_PROGRESS"}
            and item["spec_revision"] > item["implemented_revision"]
        ]
        blocked = [item for item in valid if item["status"] == "BLOCKED"]
        inconsistent = [
            item for item in valid
            if (
                item["status"] == "DONE"
                and item["spec_revision"] > item["implemented_revision"]
            ) or (
                item["status"] in {"READY", "IN_PROGRESS"}
                and item["spec_revision"] <= item["implemented_revision"]
            )
        ]

        events: list[dict[str, str]] = []
        if tracker_path.is_file():
            for line in tracker_path.read_text(encoding="utf-8").splitlines():
                match = EVENT_RE.match(line)
                if match:
                    events.append({"id": match.group(1), "type": match.group(2).upper()})
        counts = Counter(event["type"] for event in events)

        result = {
            "workspace_root": workspace_root.relative_to(REPO_ROOT).as_posix() or ".",
            "code_root": code_root.relative_to(REPO_ROOT).as_posix() or ".",
            "skeleton_root": skeleton_root.relative_to(REPO_ROOT).as_posix() or ".",
            "last_event": events[-1] if events else None,
            "event_counts": dict(sorted(counts.items())),
            "pending": pending,
            "blocked": blocked,
            "metadata_issues": issues,
            "revision_status_issues": inconsistent,
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("StageSet status")
            print(f"Workspace: {result['workspace_root']}")
            print(f"Code:      {result['code_root']}")
            print(f"Skeletons: {result['skeleton_root']}")
            if result["last_event"]:
                print(f"Last event: {result['last_event']['id']} ({result['last_event']['type']})")
            print("Events: " + (", ".join(f"{key}={value}" for key, value in result["event_counts"].items()) or "none"))
            print(f"\nPending skeletons: {len(pending)}")
            for item in pending:
                print(
                    f"- [{item['priority']}] {item['file']} -> {item['target']} "
                    f"(spec {item['spec_revision']}, implemented {item['implemented_revision']})"
                )
            print(f"\nBlocked skeletons: {len(blocked)}")
            for item in blocked:
                print(f"- {item['file']}")
            for label, entries in (("Metadata issues", issues), ("Revision status issues", inconsistent)):
                print(f"\n{label}: {len(entries)}")
                for item in entries:
                    print(f"- {item['file']}: {item.get('error', 'status and revision values conflict')}")
            if not pending:
                print("\nNo ready skeleton revision is waiting for implementation.")

        return 1 if issues or inconsistent else 0
    except (OSError, ValueError) as exc:
        print(f"StageSet error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
