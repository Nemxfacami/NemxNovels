import os

# Start scanning from the folder where this script is located
site_folder = os.path.dirname(os.path.abspath(__file__))

old_name = "wall3.png"
new_name = "wall3.webp"

changed_files = 0
changed_references = 0

for root, dirs, files in os.walk(site_folder):

    # Skip common folders that shouldn't be modified
    dirs[:] = [d for d in dirs if d not in {
        ".git",
        ".github",
        "node_modules"
    }]

    for filename in files:

        # Only scan files that can contain website code
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

            # Replace every wall3.png reference
            count = content.count(old_name)

            if count > 0:
                new_content = content.replace(old_name, new_name)

                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)

                changed_files += 1
                changed_references += count

                print(f"Updated: {filepath}")
                print(f"  Replaced {count} reference(s)")

        except UnicodeDecodeError:
            print(f"Skipped (not UTF-8): {filepath}")

print("\n================================")
print("DONE")
print("================================")
print(f"Files changed: {changed_files}")
print(f"References replaced: {changed_references}")