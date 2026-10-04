import re
import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
DELETE = "--delete" in sys.argv

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico", ".avif", ".bmp"}
TEXT_EXT = {".html", ".htm", ".css", ".js"}

# 1. Read every html/css/js file in the folder (CSS and JS can reference images too)
text = ""
html_count = 0
for f in FOLDER.iterdir():
    if f.is_file() and f.suffix.lower() in TEXT_EXT and f.resolve() != Path(__file__).resolve():
        try:
            text += "\n" + f.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"Could not read {f.name}: {e}")
            sys.exit(1)
        if f.suffix.lower() in {".html", ".htm"}:
            html_count += 1

if html_count == 0:
    print("No HTML files found in this folder. Stopping so nothing is deleted.")
    sys.exit(1)

text = text.lower()


def is_used(name):
    # match the plain name or the URL-encoded form (e.g. "home%20(1).png")
    candidates = {name.lower(), name.lower().replace(" ", "%20")}
    for c in candidates:
        if re.search(r"(?<![\w.-])" + re.escape(c) + r"(?![\w-])", text):
            return True
    return False


# 2. Check each image in the folder
used, unused = [], []
for f in sorted(FOLDER.iterdir()):
    if f.is_file() and f.suffix.lower() in IMAGE_EXT:
        (used if is_used(f.name) else unused).append(f)

print(f"Scanned {html_count} HTML file(s).")
print(f"Images in use: {len(used)}")
print(f"Images not used: {len(unused)}\n")

for f in unused:
    print(("DELETING: " if DELETE else "WOULD DELETE: ") + f.name)

if DELETE:
    for f in unused:
        f.unlink()
    print(f"\nDeleted {len(unused)} file(s).")
else:
    print("\nDry run only, nothing was deleted. Run with --delete to remove them.")