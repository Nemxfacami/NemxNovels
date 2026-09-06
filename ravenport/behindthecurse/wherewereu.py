from pathlib import Path
import re
import shutil

ROOT_FOLDER = Path(".")
CREATE_BACKUPS = True

CHAPTERS_LINK = "behindthecurse-wherewereyou.html"


def process_file(file_path):

    try:
        content = file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        print(f"[SKIP] Encoding problem: {file_path}")
        return

    # Find a Chapters option whose link is currently #
    pattern = re.compile(
        r'(<div\s+class\s*=\s*["\']option["\']>.*?'
        r'<a\b[^>]*href\s*=\s*["\'])(#)(["\'][^>]*>.*?'
        r'<p\s+id\s*=\s*["\']option-detail["\']\s*>\s*'
        r'Chapters\s*'
        r'</p>.*?</a>\s*</div>)',
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(content)

    if not match:
        print(f"[SKIP] No broken Chapters link: {file_path}")
        return

    new_content = (
        content[:match.start()]
        + match.group(1)
        + CHAPTERS_LINK
        + match.group(3)
        + content[match.end():]
    )

    if new_content == content:
        print(f"[NO CHANGE] {file_path}")
        return

    if CREATE_BACKUPS:
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        shutil.copy2(file_path, backup_path)

    file_path.write_text(new_content, encoding="utf-8")

    print(f"[UPDATED] {file_path}")
    print(f"         Chapters -> {CHAPTERS_LINK}")


html_files = list(ROOT_FOLDER.rglob("*.html"))

print("=" * 60)
print(f"Found {len(html_files)} HTML files")
print("Fixing broken Chapters links...")
print(f"Target: {CHAPTERS_LINK}")
print("Existing working Chapters links will NOT be changed.")
print("=" * 60)

for html_file in html_files:
    process_file(html_file)

print("=" * 60)
print("DONE")
print("=" * 60)
