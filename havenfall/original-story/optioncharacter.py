import os
import re

# Folder containing your HTML files
folder = "."

for filename in os.listdir(folder):
    if not filename.lower().endswith(".html"):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    original_content = content

    # Disable both character-page links
    content = re.sub(
        r'href\s*=\s*["\'](?:Havenfal-characters|AngelsNotes-characters)\.html["\']',
        'href ="#"',
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