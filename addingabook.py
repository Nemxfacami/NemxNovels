import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))


def process_html_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Reading: {filepath}")
        print(e)
        return

    # Find the actual profile books aside
    aside_pattern = re.compile(
        r'<aside\b[^>]*class\s*=\s*["\'][^"\']*aside-profile-books-section[^"\']*["\'][^>]*>'
        r'.*?'
        r'</aside>',
        re.IGNORECASE | re.DOTALL
    )

    aside_match = aside_pattern.search(content)

    if not aside_match:
        return

    profile_section = aside_match.group(0)

    # Find the placeholder book INSIDE this profile section.
    #
    # We specifically look for:
    # href="#"
    # and
    # ravenport-cover.webp
    #
    # This does NOT care about spacing or indentation.
    placeholder_pattern = re.compile(
        r'<div\b[^>]*class\s*=\s*["\']profile-book-box["\'][^>]*>'
        r'\s*'
        r'<a\b[^>]*href\s*=\s*["\']#["\'][^>]*>'
        r'\s*'
        r'<img\b[^>]*src\s*=\s*["\']ravenport-cover\.webp["\'][^>]*>'
        r'\s*'
        r'</a>'
        r'\s*'
        r'</div>',
        re.IGNORECASE | re.DOTALL
    )

    matches = list(placeholder_pattern.finditer(profile_section))

    if not matches:
        print(f"[NO PLACEHOLDER] {filepath}")
        return

    # Use the LAST placeholder.
    match = matches[-1]

    old_block = match.group(0)

    # Change only the href
    new_block = re.sub(
        r'href\s*=\s*["\']#["\']',
        'href ="ravenport/behindthecurse/"',
        old_block,
        count=1,
        flags=re.IGNORECASE
    )

    # Change only the cover
    new_block = re.sub(
        r'src\s*=\s*["\']ravenport-cover\.webp["\']',
        'src ="behindthecurse-cover.webp"',
        new_block,
        count=1,
        flags=re.IGNORECASE
    )

    # Replace the placeholder inside the profile section
    new_profile_section = (
        profile_section[:match.start()]
        + new_block
        + profile_section[match.end():]
    )

    # Replace the profile section in the original HTML
    new_content = (
        content[:aside_match.start()]
        + new_profile_section
        + content[aside_match.end():]
    )

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"[UPDATED] {filepath}")

    except Exception as e:
        print(f"[ERROR] Writing: {filepath}")
        print(e)


def scan_directory():
    print(f"Scanning root: {ROOT}\n")

    for root, dirs, files in os.walk(ROOT):

        # Never touch Git's internal files
        dirs[:] = [d for d in dirs if d != ".git"]

        for filename in files:

            if filename.lower().endswith((".html", ".htm")):

                filepath = os.path.join(root, filename)

                process_html_file(filepath)


if __name__ == "__main__":
    scan_directory()

    print("\nDone.")