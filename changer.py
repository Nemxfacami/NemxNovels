import os
import re

# Scan the current directory and every folder inside it
ROOT_DIR = "."

files_changed = 0

for root, dirs, files in os.walk(ROOT_DIR):

    for filename in files:

        if not filename.lower().endswith(".html"):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original = content

            # ==========================================================
            # 1. FIX TYPO
            # ENTITY DESIGNATIOM -> ENTITY DESIGNATION
            # ==========================================================

            content = re.sub(
                r"ENTITY\s+DESIGNATIOM",
                "ENTITY DESIGNATION",
                content,
                flags=re.IGNORECASE
            )

            # ==========================================================
            # 2. MOBILE BOOK NUMBER
            # mobile-asidenav-books-number: 9 -> 10
            # Handles spaces around =
            # ==========================================================

            content = re.sub(
                r'(<p\s+id\s*=\s*["\']mobile-asidenav-books-number["\']\s*>\s*)9(\s*</p>)',
                r'\g<1>10\g<2>',
                content,
                flags=re.IGNORECASE
            )

            # ==========================================================
            # 3. DESKTOP BOOK NUMBER
            # asidenav-books-number: 3 -> 10
            # ==========================================================

            content = re.sub(
                r'(<p\s+id\s*=\s*["\']asidenav-books-number["\']\s*>\s*)3(\s*</p>)',
                r'\g<1>10\g<2>',
                content,
                flags=re.IGNORECASE
            )

            # ==========================================================
            # 4. MAIN BOOK NUMBER
            # number-of-books: 9 -> 10
            # Handles:
            # <div id ="number-of-books">9</div>
            # <div id="number-of-books">9</div>
            # ==========================================================

            content = re.sub(
                r'(<div\s+id\s*=\s*["\']number-of-books["\']\s*>\s*)9(\s*</div>)',
                r'\g<1>10\g<2>',
                content,
                flags=re.IGNORECASE
            )

            # ==========================================================
            # SAVE ONLY IF SOMETHING CHANGED
            # ==========================================================

            if content != original:

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                files_changed += 1
                print(f"FIXED: {filepath}")

        except Exception as e:
            print(f"ERROR: {filepath}")
            print(f"       {e}")


print()
print("=" * 60)
print(f"Finished. Modified {files_changed} HTML file(s).")
print("=" * 60)
