import os
import re

ROOT = os.path.abspath(".")

favicon_pattern = re.compile(
    r'<link[^>]+rel\s*=\s*["\']icon["\']',
    re.IGNORECASE
)

head_pattern = re.compile(
    r'(<head\b[^>]*>)',
    re.IGNORECASE
)

updated = 0
already_have = 0
no_head = 0

for root, dirs, files in os.walk(ROOT):

    for filename in files:

        if not filename.lower().endswith((".html", ".htm")):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # ------------------------------------------------
            # 1. Check if this page already has a favicon
            # ------------------------------------------------

            if favicon_pattern.search(content):
                already_have += 1
                print(f"[HAS FAVICON] {os.path.relpath(filepath, ROOT)}")
                continue

            # ------------------------------------------------
            # 2. Calculate relative path to root favicon
            # ------------------------------------------------

            relative_folder = os.path.relpath(root, ROOT)

            if relative_folder == ".":
                favicon_path = "favicon.png"
            else:
                depth = len(relative_folder.split(os.sep))
                favicon_path = "../" * depth + "favicon.png"

            favicon_link = (
                f'<link rel="icon" type="image/png" href="{favicon_path}">'
            )

            # ------------------------------------------------
            # 3. Insert favicon into <head>
            # ------------------------------------------------

            if head_pattern.search(content):

                new_content = head_pattern.sub(
                    lambda match: match.group(1) + "\n    " + favicon_link,
                    content,
                    count=1
                )

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                updated += 1

                print(
                    f"[ADDED] {os.path.relpath(filepath, ROOT)} "
                    f"-> {favicon_path}"
                )

            else:
                no_head += 1
                print(
                    f"[NO HEAD] {os.path.relpath(filepath, ROOT)}"
                )

        except UnicodeDecodeError:
            print(
                f"[SKIPPED - ENCODING] "
                f"{os.path.relpath(filepath, ROOT)}"
            )

        except Exception as e:
            print(
                f"[ERROR] {os.path.relpath(filepath, ROOT)} -> {e}"
            )


print("\n======================================")
print(f"Favicons added : {updated}")
print(f"Already present: {already_have}")
print(f"No <head>      : {no_head}")
print("======================================")