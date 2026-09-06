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


def fix_file(path):
    content = path.read_text(encoding="utf-8")
    original = content

    # Find every option block by its .option start.
    starts = list(re.finditer(
        r'<div\s+class\s*=\s*["\']option["\']\s*>',
        content,
        re.IGNORECASE
    ))

    replacements = []

    for i, match in enumerate(starts):

        start = match.start()
        end = starts[i + 1].start() if i + 1 < len(starts) else len(content)

        option = content[start:end]

        # Get THIS option's name
        name_match = re.search(
            r'<p\s+id\s*=\s*["\']option-detail["\']\s*>\s*([^<]+?)\s*</p>',
            option,
            re.IGNORECASE | re.DOTALL
        )

        if not name_match:
            continue

        name = name_match.group(1).strip()

        if name not in ALERTS:
            continue

        # Find THIS option's <a>
        a_match = re.search(
            r'<a\b[^>]*>',
            option,
            re.IGNORECASE
        )

        if not a_match:
            continue

        a_tag = a_match.group(0)

        # Get href
        href_match = re.search(
            r'\bhref\s*=\s*["\']([^"\']*)["\']',
            a_tag,
            re.IGNORECASE
        )

        if not href_match:
            continue

        href = href_match.group(1).strip()

        # Characters with a real link must remain untouched.
        if href != "#":
            continue

        message = ALERTS[name]

        # Remove ANY old/broken alert onclick from this link.
        clean_a_tag = re.sub(
            r'\s+onclick\s*=\s*["\'][^"\']*["\']',
            '',
            a_tag,
            flags=re.IGNORECASE
        )

        # Add the correct alert.
        new_a_tag = re.sub(
            r'(\bhref\s*=\s*["\']#["\'])',
            lambda m: (
                m.group(1)
                + f' onclick="alert(\'{message}\'); return false;"'
            ),
            clean_a_tag,
            count=1,
            flags=re.IGNORECASE
        )

        new_option = (
            option[:a_match.start()]
            + new_a_tag
            + option[a_match.end():]
        )

        replacements.append((start, end, new_option, name))

    # Apply backwards so positions stay valid.
    for start, end, new_option, name in reversed(replacements):
        content = content[:start] + new_option + content[end:]

    if content != original:

        backup = path.with_suffix(path.suffix + ".bak")

        if CREATE_BACKUPS and not backup.exists():
            shutil.copy2(path, backup)

        path.write_text(content, encoding="utf-8")

        print(f"FIXED: {path}")

    return content != original


changed = 0

for html_file in ROOT_FOLDER.rglob("*.html"):

    if html_file.name.endswith(".bak"):
        continue

    if fix_file(html_file):
        changed += 1

print()
print(f"Finished. Fixed {changed} HTML files.")
