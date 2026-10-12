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
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "github-issues.csv"

PRIORITY_LABEL = {
    "Must have": "priority:must",
    "Should have": "priority:should",
    "Could have": "priority:could",
}


def epic_label(epic_name: str) -> str:
    return "epic:" + epic_name.lower().replace(" ", "-").replace(
        "(", "").replace(")", "").replace(",", "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be created; create nothing.")
    parser.add_argument("--only", nargs="*", default=None,
                        help="Only create these story IDs, e.g. US01 US02.")
    args = parser.parse_args()

    if not CSV_PATH.exists():
        sys.exit(f"Can't find {CSV_PATH}. Run this from the repo root, "
                 "or check docs/github-issues.csv exists.")

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

    print(f"{'Would create' if args.dry_run else 'Creating'} "
          f"{len(rows)} issue(s)...\n")

    for row in rows:
        labels = [PRIORITY_LABEL.get(row["priority"], "priority:must"),
                  epic_label(row["epic"])]
        if args.dry_run:
            print(f"- {row['title']}  [{', '.join(labels)}]")
            continue

        cmd = ["gh", "issue", "create", "--title", row["title"],
               "--body", row["body"]]
        for label in labels:
            cmd += ["--label", label]

        print(f"Creating {row['id']}: {row['title']}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  FAILED: {result.stderr.strip()}", file=sys.stderr)
            print("  (Labels must already exist in the repo - create "
                  "priority:must/should/could and the epic:* labels "
                  "first, or drop --label and add them manually.)",
                  file=sys.stderr)
        else:
            print(f"  {result.stdout.strip()}")

    if args.dry_run:
        print("\nDry run only - nothing was created. Remove --dry-run "
              "to actually create these issues.")


if __name__ == "__main__":
    main()
