import re
from pathlib import Path

folder = Path(".")

for file in folder.glob("*.html"):
    content = file.read_text(encoding="utf-8")

    # Find the <a> opening tag containing the Characters unavailable message
    pattern = re.compile(
        r'<a\b[^>]*Characters\s+are\s+not\s+available\s+yet\.[^>]*>',
        re.IGNORECASE
    )

    def fix_link(match):
        tag = match.group(0)

        # Replace the existing href
        tag = re.sub(
            r'\bhref\s*=\s*["\'][^"\']*["\']',
            'href="havenfall-character-cyrus.html"',
            tag,
            count=1,
            flags=re.IGNORECASE
        )

        # Remove onclick and everything following it in the opening tag
        tag = re.sub(
            r'\s+onclick\s*=\s*["\'][^>]*',
            '',
            tag,
            count=1,
            flags=re.IGNORECASE
        )

        # Make sure the tag closes properly
        if not tag.rstrip().endswith(">"):
            tag = tag.rstrip() + ">"

        return tag

    new_content, count = pattern.subn(fix_link, content)

    if count:
        file.write_text(new_content, encoding="utf-8")
        print(f"Updated: {file.name} — {count} link(s)")

print("Done.")