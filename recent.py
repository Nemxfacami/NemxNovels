import os
import re

# The new mobile book list
NEW_BOOK_LIST = '''<section class ="mobile-header-book-list">
          <div id ="mobile-book-cover">
                  <a href ="ravenport/birdshugs/">
                 <img class ="mobile-book-cover" src ="birdshugs-cover.webp"/>
                  </a>
             </div>
              <div id ="mobile-book-cover">
                  <a href ="occult-arcana/">
                 <img class ="mobile-book-cover" src ="occultarcana-cover.webp"/>
                  </a>
             </div>   
          <div id ="mobile-book-cover">
                  <a href ="ravenport/original-story/">
                 <img class ="mobile-book-cover" src ="ravenport-cover.webp"/>
                  </a>
             </div>
             <div id ="mobile-book-cover">
                  <a href ="havenfall/original-story/">
                 <img class ="mobile-book-cover" src ="havenfall-cover.webp"/>
                  </a>
             </div>
             
            <div id ="mobile-book-cover">
                  <a href ="ravenport/raphaasylum/">
                 <img class ="mobile-book-cover" src ="raphaasylum-cover.webp"/>
                  </a>
             </div>
        
             <div id ="mobile-book-cover">
                  <a href ="ravenport/someonewhostays/">
                 <img class ="mobile-book-cover" src ="someonewhostays-cover.webp"/>
                  </a>
             </div>

             <div id ="mobile-book-cover">
                  <a href ="havenfall/daggeroflight/">
                 <img class ="mobile-book-cover" src ="daggeroflight-cover.webp"/>
                  </a>
             </div>

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

             <div id ="mobile-book-cover">
                  <a href ="ravenport/motelbloodbath/">
                 <img class ="mobile-book-cover" src ="motelbloodbath-cover.webp"/>
                  </a>
             </div>
</section>'''

# Matches the entire section, from <section ...> to </section>
pattern = re.compile(
    r'<section\s+class\s*=\s*"mobile-header-book-list".*?</section>',
    re.DOTALL | re.IGNORECASE
)

changed = 0
skipped = 0

# Scan current folder + every subfolder
for root, dirs, files in os.walk("."):
    for filename in files:

        # Only modify HTML files
        if not filename.lower().endswith((".html", ".htm")):
            continue

        filepath = os.path.join(root, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check whether this file contains the book list
            if not pattern.search(content):
                skipped += 1
                continue

            # Replace the existing book list
            new_content, replacements = pattern.subn(
                NEW_BOOK_LIST,
                content,
                count=1
            )

            if replacements > 0:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                changed += 1
                print(f"[UPDATED] {filepath}")

        except UnicodeDecodeError:
            print(f"[SKIPPED - ENCODING] {filepath}")

        except Exception as e:
            print(f"[ERROR] {filepath} -> {e}")

print("\n--------------------------------")
print(f"Files updated : {changed}")
print(f"Files skipped : {skipped}")
print("--------------------------------")