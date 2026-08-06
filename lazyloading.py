import os
import re

folder = "."  # Current folder

# Matches any <img ...> tag that does NOT already have loading=
img_pattern = re.compile(r'<img\b(?![^>]*\bloading=)([^>]*?)(/?)>', re.IGNORECASE)

files_changed = 0
images_updated = 0

for root, dirs, files in os.walk(folder):
    for filename in files:
        if filename.endswith(".html"):
            path = os.path.join(root, filename)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            def add_lazy(match):
                global images_updated
                images_updated += 1
                attrs = match.group(1).rstrip()
                closing = match.group(2)
                return f'<img{attrs} loading="lazy"{closing}>'

            new_content = img_pattern.sub(add_lazy, content)

            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                files_changed += 1
                print(f"✓ Updated: {path}")

print(f"\nDone!")
print(f"Files modified: {files_changed}")
print(f"Images updated: {images_updated}")