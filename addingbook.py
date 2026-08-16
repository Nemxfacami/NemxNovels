from pathlib import Path
import re
import shutil

ROOT = Path(".")

SOMEONE_WHO_STAYS = '''
             <div id ="mobile-book-cover">
                  <a href ="ravenport/someonewhostays/">
                 <img class ="mobile-book-cover" src ="someonewhostays-cover.webp"/>
                  </a>
             </div>
'''

DAGGER_OF_LIGHT = '''
             <div id ="mobile-book-cover">
                  <a href ="havenfall/daggeroflight/">
                 <img class ="mobile-book-cover" src ="daggeroflight-cover.webp"/>
                  </a>
             </div>
'''

html_files = list(ROOT.rglob("*.html"))

print("=" * 60)
print(f"Root folder: {ROOT.resolve()}")
print(f"HTML files found: {len(html_files)}")
print("=" * 60)

changed = 0
lists_found = 0

for html_file in html_files:

    if ".git" in html_file.parts:
        continue

    try:
        content = html_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] {html_file}: {e}")
        continue

    # --------------------------------------------------------
    # Find ALL mobile-header-book-list opening tags
    # Allows:
    #
    # class="..."
    # class ="..."
    # class= "..."
    # class = "..."
    # --------------------------------------------------------

    pattern = re.compile(
        r'<section\s+class\s*=\s*["\']mobile-header-book-list["\'][^>]*>',
        re.IGNORECASE
    )

    matches = list(pattern.finditer(content))

    if not matches:
        continue

    lists_found += len(matches)

    print(f"\nFOUND: {html_file}")
    print(f"  Mobile book lists: {len(matches)}")

    # Work backwards so inserting text doesn't mess up
    # the positions of the other matches.
    for match in reversed(matches):

        opening_end = match.end()

        # Find closing section
        closing = content.find("</section>", opening_end)

        if closing == -1:
            print("  [WARNING] No closing </section> found.")
            continue

        section_content = content[opening_end:closing]

        has_someone = "someonewhostays-cover.webp" in section_content
        has_dagger = "daggeroflight-cover.webp" in section_content

        additions = ""

        if not has_someone:
            additions += SOMEONE_WHO_STAYS

        if not has_dagger:
            additions += DAGGER_OF_LIGHT

        if not additions:
            print("  Both books already exist.")
            continue

        # ----------------------------------------------------
        # Create backup once
        # ----------------------------------------------------

        backup = html_file.with_suffix(".html.bak")

        if not backup.exists():
            shutil.copy2(html_file, backup)

        # ----------------------------------------------------
        # Insert books before </section>
        # ----------------------------------------------------

        content = (
            content[:closing]
            + additions
            + content[closing:]
        )

        changed += 1

        if not has_someone:
            print("  + Someone Who Stays")

        if not has_dagger:
            print("  + Dagger of Light")

    html_file.write_text(content, encoding="utf-8")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

print(f"HTML files found:       {len(html_files)}")
print(f"Book lists found:       {lists_found}")
print(f"Sections modified:      {changed}")

if changed == 0:
    print("\nNothing needed to be changed.")

input("\nPress Enter to exit...")