#!/usr/bin/env python3
"""
remove_lightbox.py

Scans a folder (recursively) for .html files and strips out the
"click image -> full-screen lightbox" code block:
  - the #lightbox / .lightbox-inner CSS rules
  - the <div id="lightbox">...</div> markup
  - the JS listener that opens it (imgMsg click -> classList.add('open'))
  - the JS listener that closes it (#lightbox click -> classList.remove('open'))

Usage:
    Drop this script into the folder you want cleaned, then run:
        python remove_lightbox.py
    (it defaults to scanning the folder it's sitting in, recursively)

    Options still work if you want them:
        python remove_lightbox.py --no-backup
        python remove_lightbox.py --dry-run
        python remove_lightbox.py /some/other/folder   (optional override)

By default it writes a .bak copy of every file it changes before
overwriting it, so you can always undo.
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Regex patterns (DOTALL so "." matches newlines too)
# ---------------------------------------------------------------------------

PATTERNS = [
    # 1) CSS block: the "Lightbox" comment header + every #lightbox rule
    #    that follows it, up to (but not including) the next comment
    #    header or the closing </style> tag.
    re.compile(
        r"[ \t]*/\*\s*-+\s*Lightbox\s*-+\s*\*/.*?(?=(/\*\s*-+|</style>))",
        re.DOTALL | re.IGNORECASE,
    ),

    # 1b) fallback: any standalone #lightbox{...} / #lightbox.open{...} /
    #     #lightbox .lightbox-inner{...} rules that survive without a
    #     comment header above them.
    re.compile(
        r"[ \t]*#lightbox(?:\.\w+|\s+\.[\w-]+)?\s*\{[^}]*\}\s*",
        re.DOTALL | re.IGNORECASE,
    ),

    # 2) HTML markup: <div id="lightbox"> ... </div> (one level of nesting)
    re.compile(
        r"[ \t]*<div\s+id=[\"']lightbox[\"']\s*>[\s\S]*?</div>\s*</div>\s*",
        re.IGNORECASE,
    ),

    # 3) JS: the click handler on the image that opens the lightbox
    #    (imgMsg.addEventListener('click', ...) { ... classList.add('open') ... })
    re.compile(
        r"[ \t]*imgMsg\.addEventListener\(\s*['\"]click['\"]\s*,\s*(?:\(\)\s*=>|function\s*\([^)]*\))\s*\{[\s\S]*?\}\s*\)\s*;\s*",
        re.IGNORECASE,
    ),

    # 4) JS: the click handler on the lightbox overlay itself that closes it
    #    (optionally preceded by its own comment header)
    re.compile(
        r"[ \t]*(?:/\*\s*-+\s*Lightbox close\s*-+\s*\*/\s*)?"
        r"document\.getElementById\(\s*['\"]lightbox['\"]\s*\)\.addEventListener\("
        r"\s*['\"]click['\"]\s*,\s*function\s*\([^)]*\)\s*\{[\s\S]*?\}\s*\)\s*;\s*",
        re.IGNORECASE,
    ),
]

# Collapse 3+ blank lines left behind by removals down to 1 blank line
BLANK_RUN = re.compile(r"\n{3,}")


def strip_lightbox(text: str) -> tuple[str, int]:
    """Apply all removal patterns. Returns (new_text, number_of_hits)."""
    hits = 0
    for pattern in PATTERNS:
        text, n = pattern.subn("", text)
        hits += n
    text = BLANK_RUN.sub("\n\n", text)
    return text, hits


def process_folder(folder: Path, make_backup: bool, dry_run: bool) -> None:
    html_files = sorted(folder.rglob("*.html"))

    if not html_files:
        print(f"No .html files found under {folder}")
        return

    changed = 0
    for path in html_files:
        original = path.read_text(encoding="utf-8")
        updated, hits = strip_lightbox(original)

        if hits == 0:
            print(f"  skip   {path}  (no lightbox code found)")
            continue

        changed += 1
        if dry_run:
            print(f"  would change  {path}  ({hits} block(s) removed)")
            continue

        if make_backup:
            backup_path = path.with_suffix(path.suffix + ".bak")
            backup_path.write_text(original, encoding="utf-8")

        path.write_text(updated, encoding="utf-8")
        print(f"  changed {path}  ({hits} block(s) removed)")

    print(f"\nDone. {changed}/{len(html_files)} file(s) modified.")
    if changed and not dry_run and make_backup:
        print("Original versions saved next to each file as *.html.bak")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "folder",
        type=str,
        nargs="?",
        default=None,
        help="Folder to scan (recursively) for .html files. "
             "Defaults to the folder this script is sitting in.",
    )
    parser.add_argument("--no-backup", action="store_true", help="Do not write .bak backup files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing anything")
    args = parser.parse_args()

    if args.folder is None:
        folder = Path(__file__).resolve().parent
    else:
        folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        sys.exit(1)

    process_folder(folder, make_backup=not args.no_backup, dry_run=args.dry_run)


if __name__ == "__main__":
    main()