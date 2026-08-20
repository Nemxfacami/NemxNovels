import os

site_folder = os.path.dirname(os.path.abspath(__file__))

replacements = {
    "ravenport-cover.png": "ravenport-cover.webp",
    "havenfall-cover.png": "havenfall-cover.webp"
}

changed_files = 0
changed_references = 0

for root, dirs, files in os.walk(site_folder):

    # Don't scan Git or dependency folders
    dirs[:] = [
        d for d in dirs
        if d not in {".git", ".github", "node_modules"}
    ]

    for filename in files:

        # Website/code files only
        if not filename.lower().endswith((
            ".html",
            ".htm",
            ".css",
            ".js",
            ".php",
            ".xml",
            ".json"
        )):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            original_content = content
            file_replacements = 0

            for old_name, new_name in replacements.items():
                count = content.count(old_name)

                if count > 0:
                    content = content.replace(old_name, new_name)
                    file_replacements += count

            if content != original_content:

                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)

                changed_files += 1
                changed_references += file_replacements

                print(f"Updated: {filepath}")
                print(f"  Replaced: {file_replacements} reference(s)")

        except UnicodeDecodeError:
            print(f"Skipped (not UTF-8): {filepath}")

print("\n==============================")
print("DONE")
print("==============================")
print(f"Files changed: {changed_files}")
print(f"References replaced: {changed_references}")