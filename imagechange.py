import os

REPLACEMENTS = {
    "eye1.jpg": "eye1.webp",
    "eye1.png": "eye1.webp",
    "immortal.png": "immortal.webp",
}

changed_files = 0
total_replacements = 0

for root, dirs, files in os.walk("."):
    for filename in files:
        if not filename.lower().endswith((".html", ".htm")):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content

            for old, new in REPLACEMENTS.items():
                count = content.count(old)

                if count:
                    content = content.replace(old, new)
                    total_replacements += count
                    print(f"{filepath}: {old} -> {new} ({count} replacements)")

            if content != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                changed_files += 1

        except UnicodeDecodeError:
            print(f"Skipped (not UTF-8): {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

print("\n-----------------------------")
print(f"HTML files changed: {changed_files}")
print(f"Total replacements: {total_replacements}")
print("-----------------------------")