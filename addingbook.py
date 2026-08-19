import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))


def process_html_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")
        return

    original = content

    # --------------------------------------------------
    # Mobile side navigation book count
    # <div id="mobile-asidenav-books-number">
    #     <p id="mobile-asidenav-books-number">5</p>
    # </div>
    # --------------------------------------------------

    content = re.sub(
        r'(<div\s+id\s*=\s*["\']mobile-asidenav-books-number["\'][^>]*>'
        r'\s*<p\s+id\s*=\s*["\']mobile-asidenav-books-number["\'][^>]*>)'
        r'\s*5\s*'
        r'(</p>)',
        r'\g<1>9\g<2>',
        content,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # Number of books
    # <div class="number-of-books">
    #     <div id="number-of-books">5</div>
    # </div>
    # --------------------------------------------------

    content = re.sub(
        r'(<div\s+class\s*=\s*["\']number-of-books["\'][^>]*>'
        r'\s*<div\s+id\s*=\s*["\']number-of-books["\'][^>]*>)'
        r'\s*5\s*'
        r'(</div>)',
        r'\g<1>9\g<2>',
        content,
        flags=re.IGNORECASE
    )

    if content == original:
        return

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[UPDATED] {filepath}")

    except Exception as e:
        print(f"[ERROR] Writing {filepath}: {e}")


def scan_directory():
    print(f"Scanning: {ROOT}\n")

    for root, dirs, files in os.walk(ROOT):

        # Don't scan Git's internal files
        dirs[:] = [d for d in dirs if d != ".git"]

        for filename in files:
            if filename.lower().endswith((".html", ".htm")):
                process_html_file(os.path.join(root, filename))


if __name__ == "__main__":
    scan_directory()
    print("\nDone.")