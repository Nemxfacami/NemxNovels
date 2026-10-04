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

    # Find all .option blocks by their starting positions.
    option_starts = list(re.finditer(
        r'<div\s+class\s*=\s*["\']option["\']\s*>',
        content,
        re.IGNORECASE
    ))

    if not option_starts:
        return

    original = content
    changes = []

    # Process backwards so changing one block doesn't affect
    # the positions of blocks we haven't processed yet.
    for i in range(len(option_starts) - 1, -1, -1):

        start = option_starts[i].start()

        if i + 1 < len(option_starts):
            end = option_starts[i + 1].start()
        else:
            # Last option: end at the closing menu
            menu_end = re.search(
                r'</div>\s*(?:</body>|<script)',
                content[start:],
                re.IGNORECASE
            )

            if menu_end:
                end = start + menu_end.start()
            else:
                end = len(content)

        option = content[start:end]

        # Identify the option by its displayed text
        text_match = re.search(
            r'<p\s+id\s*=\s*["\']option-detail["\']\s*>\s*'
            r'([^<]+?)'
            r'\s*</p>',
            option,
            re.IGNORECASE
        )

        if not text_match:
            continue

        option_name = text_match.group(1).strip()

        # We only care about these four here
        if option_name not in [
            "Home Map",
            "City Map",
            "Characters",
            "Chapters"
        ]:
            continue

        # Find the opening <a>
        a_match = re.search(
            r'<a\b([^>]*)>',
            option,
            re.IGNORECASE
        )

        if not a_match:
            print(f"[WARNING] No <a> found: {file_path} -> {option_name}")
            continue

        old_a_tag = a_match.group(0)

        # --------------------------------------------------
        # HOME MAP
        # --------------------------------------------------

        if option_name == "Home Map":

            new_a_tag = re.sub(
                r'\s+href\s*=\s*["\'][^"\']*["\']',
                ' href="#"',
                old_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            # Remove any existing onclick
            new_a_tag = re.sub(
                r'\s+onclick\s*=\s*["\'][^"\']*["\']',
                '',
                new_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            # Add correct alert
            new_a_tag = new_a_tag[:-1] + (
                ' onclick="alert(\'Home Map is not available yet.\'); return false;">'
            )

            if new_a_tag != old_a_tag:
                option = (
                    option[:a_match.start()]
                    + new_a_tag
                    + option[a_match.end():]
                )

                content = content[:start] + option + content[end:]

                # Recalculate the changed length
                difference = len(option) - (end - start)

                for j in range(i):
                    pass

                changes.append("Home Map fixed")

        # --------------------------------------------------
        # CITY MAP
        # --------------------------------------------------

        elif option_name == "City Map":

            new_a_tag = re.sub(
                r'\s+href\s*=\s*["\'][^"\']*["\']',
                ' href="#"',
                old_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            new_a_tag = re.sub(
                r'\s+onclick\s*=\s*["\'][^"\']*["\']',
                '',
                new_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            new_a_tag = new_a_tag[:-1] + (
                ' onclick="alert(\'City Map is not available yet.\'); return false;">'
            )

            if new_a_tag != old_a_tag:
                option = (
                    option[:a_match.start()]
                    + new_a_tag
                    + option[a_match.end():]
                )

                content = content[:start] + option + content[end:]

                changes.append("City Map fixed")

        # --------------------------------------------------
        # CHAPTERS
        # --------------------------------------------------

        elif option_name == "Chapters":

            # Force Chapters to the correct page
            new_a_tag = re.sub(
                r'\s+href\s*=\s*["\'][^"\']*["\']',
                f' href="{CHAPTERS_LINK}"',
                old_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            # Remove any onclick from Chapters
            new_a_tag = re.sub(
                r'\s+onclick\s*=\s*["\'][^"\']*["\']',
                '',
                new_a_tag,
                count=1,
                flags=re.IGNORECASE
            )

            if new_a_tag != old_a_tag:
                option = (
                    option[:a_match.start()]
                    + new_a_tag
                    + option[a_match.end():]
                )

                content = content[:start] + option + content[end:]

                changes.append(
                    f"Chapters -> {CHAPTERS_LINK}"
                )

    if not changes:
        return

    # Backup
    if CREATE_BACKUPS:
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")

        if not backup_path.exists():
            shutil.copy2(file_path, backup_path)

    file_path.write_text(content, encoding="utf-8")

    print(f"\n[UPDATED] {file_path}")

    for change in changes:
        print(f"  [FIXED] {change}")


# --------------------------------------------------
# Scan this folder
# --------------------------------------------------

html_files = list(ROOT_FOLDER.rglob("*.html"))

print("=" * 65)
print(f"Found {len(html_files)} HTML files")
print("Repairing Behind The Curse menu...")
print("=" * 65)

for html_file in html_files:
    process_file(html_file)

print("\n" + "=" * 65)
print("DONE")
print("=" * 65)
