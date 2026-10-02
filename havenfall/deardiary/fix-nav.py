from pathlib import Path
import re
import shutil
from datetime import datetime

# ============================================================
# DEAR DIARY NAVIGATION FIXER
# ============================================================

FOLDER = Path(__file__).parent

BACKUP_FOLDER = FOLDER / (
    "navigation-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
)


def fix_file(file):
    print(f"\nChecking: {file.name}")

    try:
        html = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("  [SKIPPED] Could not read as UTF-8")
        return False

    original = html

    # ========================================================
    # Find each navigation block
    # ========================================================

    pattern = re.compile(
        r'(<div\s+class\s*=\s*["\']nav-buttons["\']\s*>)(.*?)(</div>)',
        re.IGNORECASE | re.DOTALL
    )

    def fix_navigation(match):

        opening = match.group(1)
        content = match.group(2)
        closing = match.group(3)

        # Find the first button
        first_button = re.search(
            r'(<a\b[^>]*class\s*=\s*["\'][^"\']*\bbtn\b[^"\']*["\'][^>]*>)\s*'
            r'(Next|Previous)\s*'
            r'(</a>)',
            content,
            re.IGNORECASE
        )

        if not first_button:
            return match.group(0)

        current_text = first_button.group(2)

        if current_text.lower() == "previous":
            return match.group(0)

        # Replace only the first button's text
        new_content = (
            content[:first_button.start(2)]
            + "Previous"
            + content[first_button.end(2):]
        )

        print("  [FIXED] First navigation button: Next → Previous")

        return opening + new_content + closing

    html = pattern.sub(fix_navigation, html)

    # ========================================================
    # Save only if changed
    # ========================================================

    if html == original:
        print("  [OK] Nothing needed changing")
        return False

    # Backup
    backup_file = BACKUP_FOLDER / file.name
    backup_file.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(file, backup_file)

    # Save
    file.write_text(html, encoding="utf-8")

    return True


# ============================================================
# SCAN HTML FILES
# ============================================================

print("=" * 60)
print("DEAR DIARY NAVIGATION FIXER")
print("=" * 60)

html_files = list(FOLDER.glob("*.html"))

changed = 0

for file in sorted(html_files):

    if file.name == Path(__file__).name:
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