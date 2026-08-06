import os
import re

folder = "."

eager_classes = {
    "hero",
    "tablet-profile",
    "profile-card",
    "header-covers",
    "mobile-profile-pic",
    "mobile-book-cover",
}

eager_ids = {
    "aside-profile-picture",
}

eager_srcs = {
    "nn-logo.png",
    "nemxnovels.png",
    "bluelogo.png",
    "blog.png",
    "newspaper-folderwhite.png",
    "videosblak.png",
    "fairy-talewhite.png",
    "aboutwhite.png",
    "anonymous-white.png",
    "right-arrow.png",
}

img_pattern = re.compile(r'<img\b[^>]*>', re.IGNORECASE)

files_changed = 0
images_changed = 0


def should_remove_lazy(tag):
    # Check src
    for src in eager_srcs:
        if f'src ="{src}"' in tag or f'src="{src}"' in tag:
            return True

    # Check class
    class_match = re.search(r'class\s*=\s*"([^"]+)"', tag)
    if class_match:
        classes = class_match.group(1).split()
        if any(c in eager_classes for c in classes):
            return True

    # Check id
    id_match = re.search(r'id\s*=\s*"([^"]+)"', tag)
    if id_match:
        if id_match.group(1) in eager_ids:
            return True

    return False


for root, dirs, files in os.walk(folder):
    for filename in files:
        if filename.endswith(".html"):
            path = os.path.join(root, filename)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            changed = [False]   # mutable flag

            def replace(match):
                global images_changed

                tag = match.group(0)

                if 'loading="lazy"' not in tag:
                    return tag

                if should_remove_lazy(tag):
                    changed[0] = True
                    images_changed += 1
                    return re.sub(r'\s*loading="lazy"', "", tag)

                return tag

            new_content = img_pattern.sub(replace, content)

            if changed[0]:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                files_changed += 1
                print(f"✓ {path}")

print("\nDone!")
print(f"Files modified: {files_changed}")
print(f"Images changed: {images_changed}")