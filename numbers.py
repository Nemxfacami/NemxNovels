import os
import re

# New number of books
NEW_NUMBER = "13"

# Patterns for the different book-count structures
patterns = [

    # mobile-asidenav-books-number
    re.compile(
        r'(<div\s+id\s*=\s*"mobile-asidenav-books-number"[^>]*>\s*'
        r'<p\s+id\s*=\s*"mobile-asidenav-books-number"[^>]*>)\s*\d+\s*(</p>)',
        re.IGNORECASE | re.DOTALL
    ),

    # asidenav-books-number
    re.compile(
        r'(<div\s+id\s*=\s*"asidenav-books-number"[^>]*>\s*'
        r'<p\s+id\s*=\s*"asidenav-books-number"[^>]*>)\s*\d+\s*(</p>)',
        re.IGNORECASE | re.DOTALL
    ),

    # number-of-books
    re.compile(
        r'(<div\s+id\s*=\s*"number-of-books"[^>]*>\s*)\d+(\s*</div>)',
        re.IGNORECASE | re.DOTALL
    ),
]

changed_files = 0
total_changes = 0

# Scan current folder and every subfolder
for root, dirs, files in os.walk("."):

    for filename in files:

        # Only HTML files
        if not filename.lower().endswith((".html", ".htm")):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            file_changes = 0

            # Apply every pattern
            for pattern in patterns:

                def replace_number(match):
                    return match.group(1) + NEW_NUMBER + match.group(2)

                content, changes = pattern.subn(
                    replace_number,
                    content
                )

                file_changes += changes

            # Only write if something actually changed
            if content != original:

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                changed_files += 1
                total_changes += file_changes

                print(f"[UPDATED] {filepath} ({file_changes} change(s))")

        except UnicodeDecodeError:
            print(f"[SKIPPED - ENCODING] {filepath}")

        except Exception as e:
            print(f"[ERROR] {filepath} -> {e}")


print("\n================================")
print(f"Files updated : {changed_files}")
print(f"Total changes : {total_changes}")
print("New book count: 13")
print("================================")