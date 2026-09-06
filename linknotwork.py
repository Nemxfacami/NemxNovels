from pathlib import Path
import re
import shutil

ROOT_FOLDER = Path(".")
CREATE_BACKUPS = True

ALERTS = {
    "Home Map": "Home Map is not available yet.",
    "City Map": "City Map is not available yet.",
    "Characters": "Characters are not available yet."
}


def process_file(file_path):

    try:
        content = file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        print(f"[SKIP] Encoding problem: {file_path}")
        return

    # Only process pages containing the menu
    if not re.search(
        r'<div\s+id\s*=\s*["\']menu["\']',
        content,
        re.IGNORECASE
    ):
        return

    print(f"\n[CHECKING] {file_path}")

    changed = False

    for option_name, alert_message in ALERTS.items():

        # Find the option text.
        # Allows spaces around =
        text_pattern = re.compile(
            rf'<p\s+id\s*=\s*["\']option-detail["\']\s*>\s*'
            rf'{re.escape(option_name)}'
            rf'\s*</p>',
            re.IGNORECASE
        )

        text_match = text_pattern.search(content)

        if not text_match:
            print(f"  [NOT FOUND] {option_name}")
            continue

        # Find the nearest <a ...> before this option
        before = content[:text_match.start()]

        a_start = before.rfind("<a")

        if a_start == -1:
            print(f"  [WARNING] No <a> found for {option_name}")
            continue

        # Find the opening <a> tag
        a_match = re.search(
            r'<a\b[^>]*>',
            content[a_start:],
            re.IGNORECASE
        )

        if not a_match:
            print(f"  [WARNING] No opening <a> tag for {option_name}")
            continue

        a_tag_start = a_start
        a_tag_end = a_start + a_match.end()

        a_tag = content[a_tag_start:a_tag_end]

        # Get href
        href_match = re.search(
            r'\bhref\s*=\s*["\']([^"\']*)["\']',
            a_tag,
            re.IGNORECASE
        )

        if not href_match:
            print(f"  [WARNING] No href for {option_name}")
            continue

        href = href_match.group(1).strip()

        # IMPORTANT:
        # If it already has a real working link, leave it alone.
        if href != "#":
            print(f"  [WORKING] {option_name} -> {href}")
            continue

        # Don't add the alert twice
        if re.search(r'\bonclick\s*=\s*["\'][^"\']*alert\s*\(', a_tag, re.IGNORECASE):
            print(f"  [ALREADY DONE] {option_name}")
            continue

        # Add the alert
        new_a_tag = re.sub(
            r'(<a\b[^>]*href\s*=\s*["\']#["\'])',
            rf'\1 onclick="alert(\'{alert_message}\'); return false;"',
            a_tag,
            count=1,
            flags=re.IGNORECASE
        )

        if new_a_tag == a_tag:
            print(f"  [WARNING] Could not modify {option_name}")
            continue

        content = (
            content[:a_tag_start]
            + new_a_tag
            + content[a_tag_end:]
        )

        changed = True

        print(f"  [ALERT ADDED] {option_name}")

    if not changed:
        print("[NO CHANGES]")
        return

    # Backup original
    if CREATE_BACKUPS:
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        shutil.copy2(file_path, backup_path)

    file_path.write_text(content, encoding="utf-8")

    print(f"[UPDATED] {file_path}")


# --------------------------------------------------
# Scan all HTML files
# --------------------------------------------------

html_files = list(ROOT_FOLDER.rglob("*.html"))

print("=" * 70)
print(f"Found {len(html_files)} HTML files")
print("Checking Home Map, City Map and Characters...")
print("Working links will NOT be changed.")
print("Chapters will NOT be touched.")
print("=" * 70)

for html_file in html_files:
    process_file(html_file)

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
