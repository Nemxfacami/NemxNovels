import os

ROOT = os.path.dirname(os.path.abspath(__file__))

BOOKS = """
             <div id ="mobile-book-cover">
                  <a href ="ravenport/behindthecurse/">
                 <img class ="mobile-book-cover" src ="behindthecurse-cover.webp"/>
                  </a>
             </div>

             <div id ="mobile-book-cover">
                  <a href ="ravenport/back&forth/">
                 <img class ="mobile-book-cover" src ="backnforth-cover.webp"/>
                  </a>
             </div>
"""

def process_html_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read {filepath}: {e}")
        return

    # Find the mobile header book list
    start_marker = '<section class ="mobile-header-book-list">'

    if start_marker not in content:
        return

    # Don't add the books if they are already present
    has_behind_the_curse = 'ravenport/behindthecurse/' in content
    has_back_and_forth = 'ravenport/back&forth/' in content

    if has_behind_the_curse and has_back_and_forth:
        print(f"[SKIP] Already contains both books: {filepath}")
        return

    start = content.find(start_marker)

    # Find the closing </section> belonging to the book list.
    # Since the mobile-header-book-list section contains divs rather
    # than nested sections, the next </section> is its closing tag.
    end = content.find("</section>", start)

    if end == -1:
        print(f"[WARNING] Could not find closing section: {filepath}")
        return

    # Only add whichever books are missing
    additions = ""

    if not has_behind_the_curse:
        additions += """
             <div id ="mobile-book-cover">
                  <a href ="ravenport/behindthecurse/">
                 <img class ="mobile-book-cover" src ="behindthecurse-cover.webp"/>
                  </a>
             </div>
"""

    if not has_back_and_forth:
        additions += """
             <div id ="mobile-book-cover">
                  <a href ="ravenport/back&forth/">
                 <img class ="mobile-book-cover" src ="backnforth-cover.webp"/>
                  </a>
             </div>
"""

    # Insert immediately before the closing </section>
    content = content[:end] + additions + content[end:]

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[UPDATED] {filepath}")

    except Exception as e:
        print(f"[ERROR] Could not write {filepath}: {e}")


def scan_directory():
    for root, dirs, files in os.walk(ROOT):

        # Don't scan Git's internal files
        dirs[:] = [d for d in dirs if d != ".git"]

        for filename in files:
            if filename.lower().endswith((".html", ".htm")):
                filepath = os.path.join(root, filename)
                process_html_file(filepath)


if __name__ == "__main__":
    print("Scanning NemxNovels for mobile book lists...\n")
    scan_directory()
    print("\nDone.")