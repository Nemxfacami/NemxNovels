from pathlib import Path
import re
import shutil
from datetime import datetime

# ============================================================
# NEMXNOVELS MOBILE BOOK LIST FIXER
# ============================================================

ROOT = Path(__file__).parent

BACKUP_FOLDER = ROOT / (
    "book-list-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
)

# ------------------------------------------------------------
# Dagger of Light block
# ------------------------------------------------------------

DAGGER_PATTERN = re.compile(
    r'\s*<div\s+id\s*=\s*["\']mobile-book-cover["\']>\s*'
    r'<a\s+href\s*=\s*["\']havenfall/daggeroflight/["\']>\s*'
    r'<img\s+class\s*=\s*["\']mobile-book-cover["\']\s+'
    r'src\s*=\s*["\']daggeroflight-cover\.webp["\']\s*/?>\s*'
    r'</a>\s*'
    r'</div>',
    re.IGNORECASE
)

# ------------------------------------------------------------
# Dear Diary block
# ------------------------------------------------------------

DEAR_DIARY_BLOCK = '''             <div id ="mobile-book-cover">
                  <a href ="havenfall/deardiary/">
                 <img class ="mobile-book-cover" src ="deardiary-cover.webp"/>
                  </a>
             </div>

'''

# ------------------------------------------------------------
# Bird's Hugs block
# ------------------------------------------------------------

BIRDS_HUGS_PATTERN = re.compile(
    r'(\s*<div\s+id\s*=\s*["\']mobile-book-cover["\']>\s*'
    r'<a\s+href\s*=\s*["\']ravenport/birdshugs/["\'])',
    re.IGNORECASE
)


def fix_file(file):
    print(f"\nChecking: {file}")

    try:
        html = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("  [SKIPPED] Not UTF-8")
        return False

    original = html

    # ========================================================
    # 1. Remove Dagger of Light
    # ========================================================

    html, dagger_count = DAGGER_PATTERN.subn("", html)

    if dagger_count:
        print("  [REMOVED] Dagger of Light")

    # ========================================================
    # 2. Remove an existing Dear Diary entry
    #
    # This prevents duplicates if the script is run again.
    # ========================================================

    dear_diary_pattern = re.compile(
        r'\s*<div\s+id\s*=\s*["\']mobile-book-cover["\']>\s*'
        r'<a\s+href\s*=\s*["\']havenfall/deardiary/["\']>\s*'
        r'<img\s+class\s*=\s*["\']mobile-book-cover["\']\s+'
        r'src\s*=\s*["\']deardiary-cover\.webp["\']\s*/?>\s*'
        r'</a>\s*'
        r'</div>',
        re.IGNORECASE
    )

    html, diary_count = dear_diary_pattern.subn("", html)

    if diary_count:
        print("  [FOUND] Existing Dear Diary entry removed for repositioning")

    # ========================================================
    # 3. Put Dear Diary directly before Bird's Hugs
    # ========================================================

    match = BIRDS_HUGS_PATTERN.search(html)

    if match:
        insertion = DEAR_DIARY_BLOCK + match.group(1)

        html = (
            html[:match.start(1)]
            + insertion
            + html[match.end(1):]
        )

        print("  [ADDED] Dear Diary before Bird's Hugs")

    else:
        print("  [WARNING] Bird's Hugs mobile-book entry not found")
        return False

    # ========================================================
    # 4. Save only if changed
    # ========================================================

    if html != original:

        backup_file = BACKUP_FOLDER / file.relative_to(ROOT)
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file, backup_file)

        file.write_text(html, encoding="utf-8")

        print("  [FIXED] File updated")
        return True

    print("  [OK] No changes needed")
    return False


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

print("=" * 65)
print("NEMXNOVELS MOBILE BOOK LIST FIXER")
print("=" * 65)

html_files = list(ROOT.rglob("*.html"))

# Don't scan backup folders
html_files = [
    f for f in html_files
    if "book-list-backup-" not in str(f)
]

print(f"\nFound {len(html_files)} HTML files.")

changed = 0

for file in sorted(html_files):

    # Don't modify this script obviously
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
    print(f"\nBackups created here:")
    print(BACKUP_FOLDER)

print("\nDear Diary is now positioned before Bird's Hugs.")
input("\nPress Enter to exit...")