#!/usr/bin/env python3
"""Bulk-create GitHub issues from docs/github-issues.csv.

Optional helper for Agile methodology step 3 in the README. Reads the
CSV safely with the csv module (handles the multi-line issue bodies,
which a plain bash loop cannot), then shells out to the GitHub CLI
(`gh`) once per story.

Requires: `gh auth login` already done, and this run from a directory
where `gh` knows which repo to target (inside the cloned repo is
simplest).

Usage:
    python scripts/create_github_issues.py                  # create everything
    python scripts/create_github_issues.py --dry-run         # preview only
    python scripts/create_github_issues.py --only US01 US02  # just these
"""
import argparse
import csv
# Runs the GitHub CLI with a fixed list of arguments and no shell.
import subprocess  # nosec B404
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "github-issues.csv"

# Shown when gh refuses an issue, usually because a label is missing.
LABEL_HINT = "  (Create the priority:* and epic:* labels in the repo first.)"

PRIORITY_LABEL = {
    "Must have": "priority:must",
    "Should have": "priority:should",
    "Could have": "priority:could",
}


def epic_label(epic_name: str) -> str:
    """Turn an epic name such as "Card reviews" into "epic:card-reviews"."""
    slug = epic_name.lower().replace(" ", "-")
    for character in "(),":
        slug = slug.replace(character, "")
    return "epic:" + slug


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    dry_run_help = "Print what would be created; create nothing."
    only_help = "Only create these story IDs, e.g. US01 US02."
    parser.add_argument("--dry-run", action="store_true", help=dry_run_help)
    parser.add_argument("--only", nargs="*", default=None, help=only_help)
    args = parser.parse_args()

    if not CSV_PATH.exists():
        sys.exit(f"Can't find {CSV_PATH}. Run this from the repo root.")

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if args.only:
        wanted = set(args.only)
        rows = [r for r in rows if r["id"] in wanted]
        missing = wanted - {r["id"] for r in rows}
        if missing:
            sys.exit(f"Unknown story id(s): {', '.join(sorted(missing))}")

    if not rows:
        sys.exit("Nothing to create.")

    action = "Would create" if args.dry_run else "Creating"
    print(f"{action} {len(rows)} issue(s)...\n")

    for row in rows:
        priority = PRIORITY_LABEL.get(row["priority"], "priority:must")
        labels = [priority, epic_label(row["epic"])]
        if args.dry_run:
            print(f"- {row['title']}  [{', '.join(labels)}]")
            continue

        cmd = ["gh", "issue", "create", "--title", row["title"]]
        cmd += ["--body", row["body"]]
        for label in labels:
            cmd += ["--label", label]

        print(f"Creating {row['id']}: {row['title']}")
        result = subprocess.run(cmd, capture_output=True, text=True)  # nosec
        if result.returncode != 0:
            print(f"  FAILED: {result.stderr.strip()}", file=sys.stderr)
            print(LABEL_HINT, file=sys.stderr)
        else:
            print(f"  {result.stdout.strip()}")

    if args.dry_run:
        print("\nDry run only: nothing was created.")


if __name__ == "__main__":
    main()
