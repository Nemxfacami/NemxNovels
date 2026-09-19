import os

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

            count = content.count("amonaly.jpg")

            if count:
                content = content.replace("amonaly.jpg", "entity.webp")

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                changed_files += 1
                total_replacements += count

                print(f"{filepath}: {count} replacement(s)")

        except Exception as e:
            print(f"Error reading {filepath}: {e}")

print("\n-----------------------------")
print(f"HTML files changed: {changed_files}")
print(f"Total replacements: {total_replacements}")
print("-----------------------------")