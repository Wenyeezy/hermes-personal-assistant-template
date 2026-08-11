#!/usr/bin/env python3
"""Create and verify a private Markdown workspace from the public template."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = REPO_ROOT / "private" / "AI_Knowledge_Base"
TEMPLATE_ROOT = REPO_ROOT / "templates"


PLACEHOLDER_FILES = {
    "Profile/user_core_profile.md": """# User Core Profile\n\n> Fill locally. Do not add secrets or raw identity documents.\n\n## Stable Context\n\n- Preferred name: [optional]\n- Preferred language: [fill locally]\n- Time zone: [fill locally]\n""",
    "Profile/response_preferences.md": """# Response Preferences\n\n- Default language: [fill locally]\n- Preferred answer length: [fill locally]\n- Ask before external writes: yes\n- Ask before saving sensitive memory: yes\n""",
    "Current_State/current_state.md": """# Current State\n\n## Priorities\n\n- [Add one current priority]\n\n## Open Questions\n\n- [Add only what is useful now]\n""",
    "Decision_Logs/decision_log_index.md": """# Decision Log Index\n\n| Date | Decision | Rationale | Status |\n|---|---|---|---|\n""",
    "Projects/local_ai_system.md": """# Local AI System\n\n## Goal\n\n[Describe the desired outcome without credentials or private data.]\n\n## Current Phase\n\nScaffold created; integrations not yet authorized.\n\n## Next Step\n\nChoose one small, privacy-safe setup task.\n""",
    "Life_Updates/daily_logs/README.md": """# Daily Logs\n\nOptional owner-reviewed summaries belong here. Do not save raw chat by default.\n""",
    "Life_Updates/weekly_reviews/README.md": """# Weekly Reviews\n\nUse short reviewed summaries, decisions, and next steps.\n""",
    "Index/master_index.md": """# Master Index\n\n- [Core profile](../Profile/user_core_profile.md)\n- [Response preferences](../Profile/response_preferences.md)\n- [Current state](../Current_State/current_state.md)\n- [Decision log](../Decision_Logs/decision_log_index.md)\n- [Local AI system](../Projects/local_ai_system.md)\n- [Memory policy](../Workflows/personal_memory_policy.md)\n- [Memory triage](../Workflows/personal_memory_triage.md)\n""",
}


COPY_TEMPLATES = {
    "START_HERE.template.md": "START_HERE.md",
    "personal_memory_policy.template.md": "Workflows/personal_memory_policy.md",
    "personal_memory_triage.template.md": "Workflows/personal_memory_triage.md",
}


def resolved_target(raw: str | None) -> Path:
    target = Path(raw).expanduser() if raw else DEFAULT_TARGET
    return target.resolve()


def display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def planned_files(target: Path) -> dict[Path, str]:
    files: dict[Path, str] = {}
    for source_name, destination in COPY_TEMPLATES.items():
        source = TEMPLATE_ROOT / source_name
        files[target / destination] = source.read_text(encoding="utf-8")
    for destination, content in PLACEHOLDER_FILES.items():
        files[target / destination] = content
    state = {
        "schema": "hermes.easy-setup.v1",
        "phase": "scaffolded",
        "contains_credentials": False,
        "integrations_authorized": [],
    }
    files[target / ".easy-setup-state.json"] = json.dumps(
        state, indent=2, sort_keys=True
    ) + "\n"
    return files


def init_workspace(target: Path, *, dry_run: bool, force: bool) -> int:
    files = planned_files(target)
    existing = [path for path in files if path.exists()]
    if existing and not force:
        print("Refusing to overwrite existing setup files:", file=sys.stderr)
        for path in existing:
            print(f"- {path}", file=sys.stderr)
        print("Review them first; use --force only intentionally.", file=sys.stderr)
        return 2

    for path in files:
        print(f"{'would create' if dry_run else 'create'}: {display_path(path)}")
    if dry_run:
        return 0

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"Easy Setup scaffold ready: {display_path(target)}")
    print("Next local runtime step: python3 scripts/hermes.py init")
    return 0


def check_workspace(target: Path) -> int:
    public_required = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "START_HERE.md",
        REPO_ROOT / "docs" / "easy-setup.md",
        REPO_ROOT / ".gitignore",
    ]
    missing_public = [path for path in public_required if not path.is_file()]
    if missing_public:
        print("Public template is incomplete:", file=sys.stderr)
        for path in missing_public:
            print(f"- {path}", file=sys.stderr)
        return 1

    if not target.exists():
        print("Public template: OK")
        print(f"Private scaffold: not initialized ({display_path(target)})")
        print("Next: python3 scripts/easy_setup.py init")
        return 0

    missing_private = [path for path in planned_files(target) if not path.is_file()]
    if missing_private:
        print("Private scaffold is incomplete:", file=sys.stderr)
        for path in missing_private:
            print(f"- {path}", file=sys.stderr)
        return 1

    try:
        state = json.loads(
            (target / ".easy-setup-state.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Invalid setup state: {exc}", file=sys.stderr)
        return 1
    if state.get("schema") != "hermes.easy-setup.v1":
        print("Unsupported setup-state schema.", file=sys.stderr)
        return 1

    print("Public template: OK")
    print("Private scaffold: OK")
    print(f"Location: {display_path(target)}")
    print("Integrations authorized: none by default")
    print("Runtime check: python3 scripts/hermes.py doctor")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create the private scaffold")
    init_parser.add_argument("--target", help="owner-selected private location")
    init_parser.add_argument("--dry-run", action="store_true")
    init_parser.add_argument("--force", action="store_true")

    check_parser = subparsers.add_parser("check", help="verify template/scaffold")
    check_parser.add_argument("--target", help="owner-selected private location")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target = resolved_target(args.target)
    if args.command == "init":
        return init_workspace(target, dry_run=args.dry_run, force=args.force)
    return check_workspace(target)


if __name__ == "__main__":
    raise SystemExit(main())
