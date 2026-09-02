import os
import re

# Start from the directory where the script is run
ROOT_DIR = "."

files_changed = 0

for root, dirs, files in os.walk(ROOT_DIR):
    for filename in files:
        if not filename.lower().endswith(".html"):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content

            # Fix typo: DESIGNATIOM -> DESIGNATION
            content = content.replace(
                "ENTITY DESIGNATIOM",
                "ENTITY DESIGNATION"
            )

            # Fix mobile book number:
            # <p id="mobile-asidenav-books-number">9</p>
            content = re.sub(
                r'(<p\s+id=["\']mobile-asidenav-books-number["\']\s*>\s*)9(\s*</p>)',
                r'\g<1>10\g<2>',
                content,
                flags=re.IGNORECASE
            )

            # Fix desktop book number:
            # <p id="asidenav-books-number">3</p>
            content = re.sub(
                r'(<p\s+id=["\']asidenav-books-number["\']\s*>\s*)3(\s*</p>)',
                r'\g<1>10\g<2>',
                content,
                flags=re.IGNORECASE
            )

            # Only write if something actually changed
            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                files_changed += 1
                print(f"Fixed: {filepath}")

        except Exception as e:
            print(f"ERROR: {filepath} -> {e}")

print()
print(f"Done. Modified {files_changed} HTML file(s).")
