from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
VOTES_PATH = ROOT / "arena" / "votes.jsonl"
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

    matchups_parser = subparsers.add_parser(
        "matchups",
        help="List pairwise submission matchups for a challenge.",
    )
    matchups_parser.add_argument("challenge_id", help="Challenge id to match.")

    vote_parser = subparsers.add_parser(
        "vote",
        help="Record a pairwise arena vote.",
    )
    vote_parser.add_argument("challenge_id", help="Challenge id being evaluated.")
    vote_parser.add_argument("left_submission_id", help="Left submission id.")
    vote_parser.add_argument("right_submission_id", help="Right submission id.")
    vote_parser.add_argument(
        "--votes-path",
        default=str(VOTES_PATH.relative_to(ROOT)),
        help="JSONL vote log path. Defaults to arena/votes.jsonl.",
    )

    leaderboard_parser = subparsers.add_parser(
        "leaderboard",
        help="Show aggregate arena results.",
    )
    leaderboard_parser.add_argument(
        "challenge_id",
        nargs="?",
        help="Optional challenge id to filter results.",
    )
    leaderboard_parser.add_argument(
        "--votes-path",
        default=str(VOTES_PATH.relative_to(ROOT)),
        help="JSONL vote log path. Defaults to arena/votes.jsonl.",
    )

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
    elif args.command == "matchups":
        list_matchups(args.challenge_id)
    elif args.command == "vote":
        vote(
            args.challenge_id,
            args.left_submission_id,
            args.right_submission_id,
            Path(args.votes_path),
        )
    elif args.command == "leaderboard":
        leaderboard(args.challenge_id, Path(args.votes_path))
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


def list_matchups(challenge_id: str) -> None:
    submissions = _submissions_for_challenge(challenge_id)
    if len(submissions) < 2:
        raise SystemExit(
            f"Need at least two submissions for {challenge_id}; found {len(submissions)}."
        )

    for index, (left, right) in enumerate(_pairs(submissions), start=1):
        print(f"{index}. {left['id']} ({left['model']}) vs {right['id']} ({right['model']})")
        print(f"   left:  {left['title']} - {left['play_url']}")
        print(f"   right: {right['title']} - {right['play_url']}")


def vote(
    challenge_id: str,
    left_submission_id: str,
    right_submission_id: str,
    votes_path: Path,
) -> None:
    submissions = {
        submission["id"]: submission
        for submission in _submissions_for_challenge(challenge_id)
    }
    missing = [
        submission_id
        for submission_id in [left_submission_id, right_submission_id]
        if submission_id not in submissions
    ]
    if missing:
        raise SystemExit(f"Unknown submission id(s) for {challenge_id}: {', '.join(missing)}")

    left = submissions[left_submission_id]
    right = submissions[right_submission_id]

    print_matchup_details(left, right)
    record = {
        "created_at": datetime.now(UTC).isoformat(),
        "challenge_id": challenge_id,
        "left_submission_id": left_submission_id,
        "right_submission_id": right_submission_id,
        "preferred_replay": _prompt_choice("Which game would you rather play again?"),
        "preferred_interest": _prompt_choice(
            "Which game felt more intellectually interesting?"
        ),
        "preferred_challenge_fit": _prompt_choice(
            "Which game better matched the challenge?"
        ),
        "preferred_clarity": _prompt_choice("Which game had clearer rules?"),
        "preferred_novelty": _prompt_choice("Which game felt more novel?"),
        "notes": input("Optional notes: ").strip(),
    }

    target = votes_path if votes_path.is_absolute() else ROOT / votes_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\n")

    print(f"Recorded vote in {_display_path(target)}")


def leaderboard(challenge_id: str | None, votes_path: Path) -> None:
    target = votes_path if votes_path.is_absolute() else ROOT / votes_path
    if not target.exists():
        raise SystemExit(f"No vote log found at {target}")

    votes = _load_votes(target)
    if challenge_id is not None:
        votes = [vote for vote in votes if vote.get("challenge_id") == challenge_id]
    if not votes:
        raise SystemExit("No votes found.")

    submissions = _load_submissions_by_id()
    submission_scores: Counter[str] = Counter()
    model_scores: Counter[str] = Counter()
    dimensions = [
        "preferred_replay",
        "preferred_interest",
        "preferred_challenge_fit",
        "preferred_clarity",
        "preferred_novelty",
    ]

    for vote_record in votes:
        for dimension in dimensions:
            winner = _winner_submission_id(vote_record, dimension)
            if winner is None:
                continue
            submission_scores[winner] += 1
            model = submissions.get(winner, {}).get("model")
            if isinstance(model, str):
                model_scores[model] += 1

    print(f"Votes: {len(votes)}")
    print("\nSubmissions")
    for submission_id, score in submission_scores.most_common():
        title = submissions.get(submission_id, {}).get("title", "unknown title")
        model = submissions.get(submission_id, {}).get("model", "unknown model")
        print(f"{score:>3}  {submission_id} ({model}) - {title}")

    print("\nModels")
    for model, score in model_scores.most_common():
        print(f"{score:>3}  {model}")


def print_matchup_details(left: dict[str, Any], right: dict[str, Any]) -> None:
    print("LEFT")
    print(f"  id:          {left['id']}")
    print(f"  title:       {left['title']}")
    print(f"  model:       {left['model']}")
    print(f"  play_url:    {left['play_url']}")
    print(f"  description: {left['description']}")
    print()
    print("RIGHT")
    print(f"  id:          {right['id']}")
    print(f"  title:       {right['title']}")
    print(f"  model:       {right['model']}")
    print(f"  play_url:    {right['play_url']}")
    print(f"  description: {right['description']}")
    print()


def _prompt_choice(question: str) -> str:
    while True:
        answer = input(f"{question} [left/right/tie]: ").strip().lower()
        if answer in {"left", "right", "tie"}:
            return answer
        print("Please enter left, right, or tie.")


def _submissions_for_challenge(challenge_id: str) -> list[dict[str, Any]]:
    submissions = [
        submission
        for submission in _load_submissions()
        if submission.get("challenge_id") == challenge_id
    ]
    return sorted(submissions, key=lambda submission: submission["id"])


def _load_submissions() -> list[dict[str, Any]]:
    submissions: list[dict[str, Any]] = []
    for file in _submission_files(ROOT / "submissions"):
        errors = _validate_submission_file(file)
        if errors:
            raise SystemExit(
                f"Invalid submission file {file.relative_to(ROOT)}: {'; '.join(errors)}"
            )
        submissions.append(json.loads(file.read_text(encoding="utf-8")))
    return submissions


def _load_submissions_by_id() -> dict[str, dict[str, Any]]:
    return {submission["id"]: submission for submission in _load_submissions()}


def _pairs(submissions: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    pairs = []
    for left_index, left in enumerate(submissions):
        for right in submissions[left_index + 1 :]:
            pairs.append((left, right))
    return pairs


def _load_votes(path: Path) -> list[dict[str, Any]]:
    votes: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            vote_record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSONL vote at line {line_number}: {exc}") from exc
        if not isinstance(vote_record, dict):
            raise SystemExit(f"Vote at line {line_number} must be a JSON object.")
        votes.append(vote_record)
    return votes


def _winner_submission_id(vote_record: dict[str, Any], dimension: str) -> str | None:
    preference = vote_record.get(dimension)
    if preference == "left":
        winner = vote_record.get("left_submission_id")
    elif preference == "right":
        winner = vote_record.get("right_submission_id")
    else:
        return None

    return winner if isinstance(winner, str) else None


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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
