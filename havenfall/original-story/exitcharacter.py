import re
from pathlib import Path

folder = Path(".")

pattern = re.compile(
    r'(<div\b[^>]*\bid\s*=\s*["\']exit-characters["\'][^>]*>'
    r'.*?<a\b[^>]*\bhref\s*=\s*)["\']Havenfall-characters\.html["\']',
    re.IGNORECASE | re.DOTALL
)

for file in folder.glob("*.html"):
    content = file.read_text(encoding="utf-8")

    new_content, count = pattern.subn(
        r'\1"Havenfall-wherewereyou.html"',
        content
    )

    if count:
        file.write_text(new_content, encoding="utf-8")
        print(f"Updated: {file.name} — {count} link(s)")

print("Done.")