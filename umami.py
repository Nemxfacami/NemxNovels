
#!/usr/bin/env python3
"""
Add Umami Analytics to every HTML file in the NemxNovels folder.

Features:
- Automatically uses the folder containing this script.
- Recursively scans .html and .htm files.
- Skips files that already contain Umami tracking.
- Inserts the script before </head> where possible.
- Falls back to </body>, or appends to the file.
- Does NOT create backup files.
- Supports dry-run preview mode.

Usage:
    python add_umami.py
    python add_umami.py --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

WEBSITE_ID = "05269fdc-32b3-4cc2-b684-37fbe9b10cf5"

SCRIPT_TAG = (
    '<script defer src="https://cloud.umami.is/script.js" '
    f'data-website-id="{WEBSITE_ID}"></script>'
)


def insert_script(html: str) -> tuple[str, str]:
    """Return (updated_html, action)."""

    if WEBSITE_ID in html or "cloud.umami.is/script.js" in html:
        return html, "skipped_already_present"

    head_match = re.search(r"</head\s*>", html, re.IGNORECASE)

    if head_match:
        pos = head_match.start()
        updated = html[:pos] + "    " + SCRIPT_TAG + "\n" + html[pos:]
        return updated, "inserted_before_head_close"

    body_match = re.search(r"</body\s*>", html, re.IGNORECASE)

    if body_match:
        pos = body_match.start()
        updated = html[:pos] + "    " + SCRIPT_TAG + "\n" + html[pos:]
        return updated, "inserted_before_body_close"

    return html.rstrip() + "\n" + SCRIPT_TAG + "\n", "appended"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add Umami Analytics to NemxNovels HTML files."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying any files.",
    )

    args = parser.parse_args()

    # Use the folder where this Python script is located.
    root = Path(__file__).resolve().parent

    html_files = sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and p.suffix.lower() in {".html", ".htm"}
        and not any(
            "backup" in part.lower()
            for part in p.relative_to(root).parts
        )
        and not p.name.lower().endswith(
            (".bak.html", ".backup.html")
        )
    )

    if not html_files:
        print(f"No HTML files found under:\n{root}")
        return 0

    updated_count = 0
    skipped_count = 0
    error_count = 0

    print(f"Website folder: {root}")
    print(f"HTML files found: {len(html_files)}")

    if args.dry_run:
        print("DRY RUN: no files will be changed.\n")
    else:
        print("Backup creation is disabled.\n")

    for file_path in html_files:
        try:
            original = file_path.read_text(encoding="utf-8")
            updated, action = insert_script(original)
            relative_path = file_path.relative_to(root)

            if action == "skipped_already_present":
                skipped_count += 1
                print(f"SKIP   {relative_path} (Umami already present)")
                continue

            if args.dry_run:
                updated_count += 1
                print(f"WOULD  {relative_path} ({action})")
                continue

            file_path.write_text(updated, encoding="utf-8", newline="")
            updated_count += 1
            print(f"ADDED  {relative_path} ({action})")

        except (OSError, UnicodeError) as exc:
            error_count += 1
            print(f"ERROR  {file_path}: {exc}", file=sys.stderr)

    print("\nSummary")
    print(f"  Updated / would update: {updated_count}")
    print(f"  Already had Umami:      {skipped_count}")
    print(f"  Errors:                 {error_count}")

    if args.dry_run:
        print("\nIf everything looks correct, run: python add_umami.py")
    else:
        print("\nDone. Review a few pages and commit/push your changes.")

    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
