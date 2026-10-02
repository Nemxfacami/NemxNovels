from pathlib import Path
import shutil
from datetime import datetime

# ============================================================
# DEAR DIARY TYPO FIXER
# ============================================================

FOLDER = Path(__file__).parent

BACKUP_FOLDER = FOLDER / (
    "typo-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
)

OLD = "deadiary"
NEW = "deardiary"


def fix_file(file):
    print(f"\nChecking: {file.name}")

    try:
        html = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("  [SKIPPED] Could not read as UTF-8")
        return False

    if OLD not in html:
        print("  [OK] No typo found")
        return False

    # Count occurrences
    count = html.count(OLD)

    # Replace
    fixed_html = html.replace(OLD, NEW)

    # Backup original
    backup_file = BACKUP_FOLDER / file.name
    backup_file.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(file, backup_file)

    # Save fixed version
    file.write_text(fixed_html, encoding="utf-8")

    print(f"  [FIXED] {count} occurrence(s)")
    print(f"  {OLD} -> {NEW}")

    return True


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

print("=" * 60)
print("DEAR DIARY TYPO FIXER")
print("=" * 60)

html_files = list(FOLDER.glob("*.html"))

changed = 0

for file in sorted(html_files):

    # Don't process files inside backup folders
    if "typo-backup-" in str(file):
        continue

    if fix_file(file):
        changed += 1


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

print(f"\nHTML files scanned: {len(html_files)}")
print(f"HTML files changed: {changed}")

if changed:
    print(f"\nBackups created in:")
    print(BACKUP_FOLDER)

input("\nPress Enter to exit...")