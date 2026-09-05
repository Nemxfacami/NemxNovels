import os
import re

# Website folder
ROOT_FOLDER = "."

# The 6 required meta tags
REQUIRED_TAGS = {
    "description": re.compile(
        r'<meta\s+name=["\']description["\']\s+content=["\']',
        re.IGNORECASE
    ),

    "og:title": re.compile(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']',
        re.IGNORECASE
    ),

    "og:description": re.compile(
        r'<meta\s+property=["\']og:description["\']\s+content=["\']',
        re.IGNORECASE
    ),

    "og:image": re.compile(
        r'<meta\s+property=["\']og:image["\']\s+content=["\']',
        re.IGNORECASE
    ),

    "og:url": re.compile(
        r'<meta\s+property=["\']og:url["\']\s+content=["\']',
        re.IGNORECASE
    ),

    "og:type": re.compile(
        r'<meta\s+property=["\']og:type["\']\s+content=["\']',
        re.IGNORECASE
    )
}

total_html = 0
complete_files = 0
incomplete_files = 0
less_than_3_files = 0

print("=" * 80)
print("NEMXNOVELS META TAG SCANNER")
print("=" * 80)

for root, dirs, files in os.walk(ROOT_FOLDER):

    for file in files:

        if not file.lower().endswith(".html"):
            continue

        total_html += 1

        filepath = os.path.join(root, file)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        except UnicodeDecodeError:
            print(f"\nCOULD NOT READ: {filepath}")
            continue

        found_tags = []
        missing_tags = []

        # Check every required tag
        for tag_name, pattern in REQUIRED_TAGS.items():

            if pattern.search(content):
                found_tags.append(tag_name)
            else:
                missing_tags.append(tag_name)

        count = len(found_tags)

        # Completely correct
        if count == 6:
            complete_files += 1
            continue

        incomplete_files += 1

        # Only highlight files with fewer than 3
        if count < 3:
            less_than_3_files += 1

            print("\n" + "-" * 80)
            print(f"FILE: {filepath}")
            print(f"FOUND: {count}/6")
            print(f"MISSING: {len(missing_tags)}")

            print("\nFOUND TAGS:")
            for tag in found_tags:
                print(f"  ✓ {tag}")

            print("\nMISSING TAGS:")
            for tag in missing_tags:
                print(f"  ✗ {tag}")

        # Files with 3-5 are also reported separately
        else:
            print("\n" + "-" * 80)
            print(f"INCOMPLETE FILE: {filepath}")
            print(f"FOUND: {count}/6")
            print("MISSING:")

            for tag in missing_tags:
                print(f"  ✗ {tag}")


print("\n" + "=" * 80)
print("SCAN COMPLETE")
print("=" * 80)

print(f"TOTAL HTML FILES:       {total_html}")
print(f"COMPLETE (6/6):         {complete_files}")
print(f"INCOMPLETE:             {incomplete_files}")
print(f"LESS THAN 3 TAGS:       {less_than_3_files}")

print("=" * 80)
