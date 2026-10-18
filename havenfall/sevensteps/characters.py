import re
from pathlib import Path

NEW_LINK = "loverscase-quiz.html"

# Matches href="#" followed by the Characters onclick alert, plus any stray
# leftover text (like the doubled "Characters are not available yet...") up to the tag's closing >
pattern = re.compile(
    r'''href\s*=\s*"#"\s*'''
    r'''onclick\s*=\s*"alert\('Characters are not available yet\.'\);\s*return false;"'''
    r'''[^>]*>''',
    re.IGNORECASE,
)

replacement = f'href="{NEW_LINK}">'

for file in Path(".").glob("*.html"):
    text = file.read_text(encoding="utf-8")
    new_text, count = pattern.subn(replacement, text)

    if count:
        file.write_text(new_text, encoding="utf-8")
        print(f"Updated {file.name} ({count} replacement{'s' if count > 1 else ''})")
    else:
        print(f"No match in {file.name}")