from pathlib import Path
import re

# Start from the current folder
root = Path(".")

# Find the contents of a <title>...</title> tag
title_pattern = re.compile(
    r"<title\b[^>]*>(.*?)</title\s*>",
    re.IGNORECASE | re.DOTALL
)

missing_titles = []

# Scan current folder and ALL subfolders
for file in root.rglob("*"):
    if not file.is_file():
        continue

    # Only HTML files
    if file.suffix.lower() not in [".html", ".htm"]:
        continue

    try:
        content = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = file.read_text(encoding="utf-8-sig")
        except Exception:
            print(f"Could not read: {file}")
            continue

    match = title_pattern.search(content)

    # No title tag OR title tag is empty/only whitespace
    if not match or not match.group(1).strip():
        missing_titles.append(file)

# Display results
print("\nHTML FILES WITH MISSING OR EMPTY TITLES")
print("=" * 60)

if not missing_titles:
    print("All HTML files have a title containing text.")
else:
    for file in missing_titles:
        print(f"Name : {file.name}")
        print(f"Path : {file.resolve()}")
        print("-" * 60)

    print(f"\nTotal files with missing/empty titles: {len(missing_titles)}")