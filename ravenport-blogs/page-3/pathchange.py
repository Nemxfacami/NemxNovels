import os
import re

# Current folder
folder = "."

# Match src="..." and href="..."
attribute_pattern = re.compile(
    r'(?P<attr>\b(?:src|href)\s*=\s*)(?P<quote>["\'])(?P<path>.*?)(?P=quote)',
    re.IGNORECASE
)

def remove_folder(path):
    # Don't touch URLs, anchors, data, etc.
    if (
        not path
        or path.startswith((
            "http://", "https://", "//",
            "#", "data:", "mailto:", "tel:"
        ))
    ):
        return path

    # Remove images/, css/, or js/
    if path.startswith("images/"):
        return path[len("images/"):]

    if path.startswith("css/"):
        return path[len("css/"):]

    if path.startswith("js/"):
        return path[len("js/"):]

    return path


# Process every HTML file in the current folder
for filename in os.listdir(folder):

    if not filename.lower().endswith((".html", ".htm")):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    new_content = attribute_pattern.sub(
        lambda m:
            m.group("attr")
            + m.group("quote")
            + remove_folder(m.group("path"))
            + m.group("quote"),
        content
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)

        print(f"Updated: {filename}")
    else:
        print(f"No changes: {filename}")

print("\nDone.")
