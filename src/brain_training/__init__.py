from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUIRED_SUBMISSION_FIELDS = {
    "id",
    "challenge_id",
    "title",
    "model",
    "harness",
    "skills_used",
    "play_url",
    "source_url",
    "intended_cognitive_skill",
    "session_length_minutes",
    "description",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="brain-training",
        description="Manage the brain-training game benchmark skeleton.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-challenges", help="List available challenges.")
    subparsers.add_parser("list-skills", help="List available skill files.")

    validate_parser = subparsers.add_parser(
        "validate-submissions",
        help="Validate submission metadata JSON files.",
    )
    validate_parser.add_argument(
        "path",
        nargs="?",
        default="submissions",
        help="Submission file or directory to validate. Defaults to submissions/.",
    )

    args = parser.parse_args()

    if args.command == "list-challenges":
        list_challenges()
    elif args.command == "list-skills":
        list_skills()
    elif args.command == "validate-submissions":
        validate_submissions(Path(args.path))


def list_challenges() -> None:
    challenge_files = sorted((ROOT / "challenges").glob("*/CHALLENGE.md"))
    if not challenge_files:
        print("No challenges found.")
        return

    for challenge_file in challenge_files:
        print(f"{challenge_file.parent.name}: {challenge_file.relative_to(ROOT)}")


def list_skills() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        print("No skills found.")
        return

    for skill_file in skill_files:
        print(f"{skill_file.parent.name}: {skill_file.relative_to(ROOT)}")


def validate_submissions(path: Path) -> None:
    target = path if path.is_absolute() else ROOT / path
    files = _submission_files(target)
    if not files:
        raise SystemExit(f"No submission JSON files found at {target}")

    failures = 0
    for file in files:
        errors = _validate_submission_file(file)
        if errors:
            failures += 1
            print(f"FAIL {file.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {file.relative_to(ROOT)}")

    if failures:
        raise SystemExit(1)


def _submission_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix == ".json":
        return [path]
    if path.is_dir():
        return sorted(
            file
            for file in path.glob("*.json")
            if file.name != "submission.schema.json"
        )
    return []


def _validate_submission_file(file: Path) -> list[str]:
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["Submission must be a JSON object."]

    errors = _missing_field_errors(data)
    errors.extend(_type_errors(data))
    errors.extend(_reference_errors(data))
    return errors


def _missing_field_errors(data: dict[str, Any]) -> list[str]:
    return [
        f"Missing required field: {field}"
        for field in sorted(REQUIRED_SUBMISSION_FIELDS - data.keys())
    ]


def _type_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_SUBMISSION_FIELDS - {"skills_used", "session_length_minutes"}:
        if field in data and not isinstance(data[field], str):
            errors.append(f"{field} must be a string.")

    if "skills_used" in data and not (
        isinstance(data["skills_used"], list)
        and all(isinstance(skill, str) for skill in data["skills_used"])
    ):
        errors.append("skills_used must be a list of strings.")

    if "session_length_minutes" in data and not isinstance(
        data["session_length_minutes"], int
    ):
        errors.append("session_length_minutes must be an integer.")

    return errors


def _reference_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    challenge_id = data.get("challenge_id")
    if isinstance(challenge_id, str):
        challenge_file = ROOT / "challenges" / challenge_id / "CHALLENGE.md"
        if not challenge_file.exists():
            errors.append(f"Unknown challenge_id: {challenge_id}")

    skills_used = data.get("skills_used")
    if isinstance(skills_used, list):
        for skill in skills_used:
            if isinstance(skill, str):
                skill_file = ROOT / "skills" / skill / "SKILL.md"
                if not skill_file.exists():
                    errors.append(f"Unknown skill: {skill}")

    return errors
