import os
import re

# Current folder
folder = "."

# File extensions and their target folders
folders = {
    ".css": "css",
    ".js": "js",
}

image_extensions = (
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".svg", ".ico", ".bmp", ".avif"
)

# Match src="..." and href="..."
attribute_pattern = re.compile(
    r'(?P<attr>\b(?:src|href)\s*=\s*)(?P<quote>["\'])(?P<path>.*?)(?P=quote)',
    re.IGNORECASE
)

def fix_path(path):
    path = path.strip()

    # Don't touch URLs, anchors, data, protocol-relative paths, etc.
    if (
        not path
        or path.startswith(("http://", "https://", "//", "#", "data:", "mailto:", "tel:"))
    ):
        return path

    # Separate query string / fragment
    match = re.match(r'([^?#]*)(.*)', path)
    clean_path = match.group(1)
    suffix = match.group(2)

    # Don't touch paths that already have the correct folder
    if clean_path.startswith(("images/", "css/", "js/")):
        return path

    filename = os.path.basename(clean_path)

    # Images
    if filename.lower().endswith(image_extensions):
        return "images/" + clean_path + suffix

    # CSS / JS
    extension = os.path.splitext(filename)[1].lower()

    if extension in folders:
        return folders[extension] + "/" + clean_path + suffix

    return path


# Process every HTML file in the current folder
for filename in os.listdir(folder):

    if not filename.lower().endswith((".html", ".htm")):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    new_content = attribute_pattern.sub(
        lambda m: m.group("attr") +
                  m.group("quote") +
                  fix_path(m.group("path")) +
                  m.group("quote"),
        content
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)

        print(f"Updated: {filename}")
    else:
        print(f"No changes: {filename}")

print("\nDone.")
