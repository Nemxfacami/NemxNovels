import re
from pathlib import Path

ROOT = Path(".")

BASE_URL = "https://nemxnovels.site/"

# ---------------------------------------------------------
# 1. Remove the Raphaasylum mobile book block
# ---------------------------------------------------------

raphaasylum_pattern = re.compile(
    r'<div\b[^>]*\bid\s*=\s*["\']mobile-book-cover["\'][^>]*>'
    r'\s*<a\b[^>]*href\s*=\s*["\']ravenport/raphaasylum/["\'][^>]*>'
    r'.*?'
    r'</a>\s*'
    r'</div>',
    re.IGNORECASE | re.DOTALL
)

# ---------------------------------------------------------
# 2. Seven Steps replacement block
# ---------------------------------------------------------

seven_steps_block = '''<div id ="mobile-book-cover">
                  <a href ="https://nemxnovels.site/havenfall/sevensteps/">
                 <img class ="mobile-book-cover" src ="sevensteps-cover.webp"/>
                  </a>
             </div>'''

# ---------------------------------------------------------
# 3. Find mobile-book-cover links and make them absolute
# ---------------------------------------------------------

mobile_link_pattern = re.compile(
    r'(<div\b[^>]*\bid\s*=\s*["\']mobile-book-cover["\'][^>]*>'
    r'.*?<a\b[^>]*\bhref\s*=\s*)'
    r'(["\'])(?!https?://)([^"\']+)(\2)',
    re.IGNORECASE | re.DOTALL
)

# ---------------------------------------------------------
# Process every HTML file recursively
# ---------------------------------------------------------

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if file.suffix.lower() not in [".html", ".htm"]:
        continue

    try:
        content = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file.read_text(encoding="utf-8-sig")

    original = content

    # -----------------------------------------------------
    # Remove Raphaasylum
    # -----------------------------------------------------

    content, removed = raphaasylum_pattern.subn("", content)

    # -----------------------------------------------------
    # Add Seven Steps where Raphaasylum was removed
    # -----------------------------------------------------

    if removed:
        # Put Seven Steps where the Raphaasylum block used to be
        content = content.replace(
            '<div id ="mobile-book-cover">\n                  <a href ="https://nemxnovels.site/havenfall/sevensteps/">',
            '<div id ="mobile-book-cover">\n                  <a href ="https://nemxnovels.site/havenfall/sevensteps/">',
            1
        )

        # Since the block was removed above, insert Seven Steps
        # before the next mobile-book-cover block.
        # Find the first mobile-book-cover after the location
        # where Raphaasylum used to be.
        #
        # Simpler and safer: place Seven Steps immediately before
        # the first mobile-book-cover that follows Bird's Hugs.
        bird_pattern = re.compile(
            r'(<div\b[^>]*\bid\s*=\s*["\']mobile-book-cover["\'][^>]*>'
            r'.*?birdshugs-cover\.webp.*?</div>)',
            re.IGNORECASE | re.DOTALL
        )

        match = bird_pattern.search(content)

        if match:
            insert_position = match.end()
            content = (
                content[:insert_position]
                + "\n             "
                + seven_steps_block
                + content[insert_position:]
            )
        else:
            print(f"Warning: Could not find insertion point in {file}")

    # -----------------------------------------------------
    # Make all mobile book links absolute
    # -----------------------------------------------------

    def make_absolute(match):
        prefix = match.group(1)
        quote = match.group(2)
        href = match.group(3)

        # Avoid accidentally modifying anchors, fragments, etc.
        if href.startswith(("#", "mailto:", "javascript:")):
            return match.group(0)

        return prefix + '"' + BASE_URL + href.lstrip("/") + '"'

    content = mobile_link_pattern.sub(make_absolute, content)

    # -----------------------------------------------------
    # Write only if something actually changed
    # -----------------------------------------------------

    if content != original:
        file.write_text(content, encoding="utf-8")

        print(f"Updated: {file}")

print("\nDone.")