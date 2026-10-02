from pathlib import Path
import re
import shutil
from datetime import datetime

# ============================================================
# DEAR DIARY ENTRY INDICATOR
# ============================================================

FOLDER = Path(__file__).parent

BACKUP_FOLDER = FOLDER / (
    "entry-indicator-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
)


def fix_file(file):
    print(f"\nChecking: {file.name}")

    try:
        html = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("  [SKIPPED] Could not read as UTF-8")
        return False

    # ========================================================
    # Find the entry number from the title
    # ========================================================

    title_match = re.search(
        r'<title>\s*Dear\s+Diary\s+Entry\s+(\d+)\s*\|',
        html,
        re.IGNORECASE
    )

    if not title_match:
        print("  [SKIPPED] No Dear Diary entry number found in title")
        return False

    entry_number = title_match.group(1)

    indicator = f'<div id="entry-indicator">Entry {entry_number}</div>'

    # ========================================================
    # Check whether this exact indicator already exists
    # ========================================================

    existing_indicator = re.search(
        r'<div\s+id\s*=\s*["\']entry-indicator["\']\s*>.*?</div>',
        html,
        re.IGNORECASE | re.DOTALL
    )

    if existing_indicator:

        existing_text = existing_indicator.group(0)

        # Already correct
        if existing_text.strip() == indicator:
            print(f"  [OK] Entry {entry_number} indicator already exists")
            return False

        # Wrong entry number — replace it
        html = (
            html[:existing_indicator.start()]
            + indicator
            + html[existing_indicator.end():]
        )

        print(f"  [FIXED] Corrected indicator to Entry {entry_number}")

    else:

        # ====================================================
        # Insert immediately after <body>
        # ====================================================

        body_match = re.search(
            r'<body\s*>',
            html,
            re.IGNORECASE
        )

        if not body_match:
            print("  [SKIPPED] No <body> tag found")
            return False

        insert_position = body_match.end()

        html = (
            html[:insert_position]
            + "\n"
            + indicator
            + html[insert_position:]
        )

        print(f"  [ADDED] Entry {entry_number} indicator")

    # ========================================================
    # Backup original
    # ========================================================

    backup_file = BACKUP_FOLDER / file.name
    backup_file.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(file, backup_file)

    # ========================================================
    # Save
    # ========================================================

    file.write_text(html, encoding="utf-8")

    return True


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

print("=" * 65)
print("DEAR DIARY ENTRY INDICATOR")
print("=" * 65)

html_files = list(FOLDER.glob("*.html"))

changed = 0

for file in sorted(html_files):

    # Don't process this script
    if file.name == Path(__file__).name:
        continue

    if fix_file(file):
        changed += 1


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("DONE")
print("=" * 65)

print(f"\nHTML files scanned: {len(html_files)}")
print(f"HTML files changed: {changed}")

if changed:
    print(f"\nBackups created in:")
    print(BACKUP_FOLDER)

input("\nPress Enter to exit...")