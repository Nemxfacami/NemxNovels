import os
import re

folder = "."

NEW_NUMBER = "10"

for filename in os.listdir(folder):

    if not filename.lower().endswith(".html"):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    original_content = content

    # PC book counter
    content = re.sub(
        r'(<div\s+id\s*=\s*["\']number-of-books["\']\s*>).*?(</div>)',
        r'\g<1>' + NEW_NUMBER + r'\g<2>',
        content,
        flags=re.IGNORECASE
    )

    # Mobile book counter
    content = re.sub(
        r'(<p\s+id\s*=\s*["\']mobile-asidenav-books-number["\']\s*>).*?(</p>)',
        r'\g<1>' + NEW_NUMBER + r'\g<2>',
        content,
        flags=re.IGNORECASE
    )

    if content != original_content:

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Updated: {filename}")

    else:
        print(f"No change: {filename}")

print("\nDone.")
