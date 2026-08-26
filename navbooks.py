import os
import re

# Folder containing your HTML files
ROOT_FOLDER = "."

motel_block = '''             <div id ="mobile-book-cover">
                  <a href ="ravenport/motelbloodbath/">
                 <img class ="mobile-book-cover" src ="motelbloodbath-cover.webp"/>
                  </a>
             </div>
'''

for root, dirs, files in os.walk(ROOT_FOLDER):
    for filename in files:
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(root, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip files that already have Motel Bloodbath
        if 'ravenport/motelbloodbath/' in content:
            continue

        # Find the mobile-header-book-list section
        pattern = r'(<section\s+class\s*=\s*"mobile-header-book-list">)(.*?)(</section>)'

        match = re.search(pattern, content, re.DOTALL)

        if not match:
            continue

        section = match.group(0)

        # Add Motel Bloodbath before the closing </section>
        new_section = section.replace(
            "</section>",
            "\n" + motel_block + "</section>",
            1
        )

        content = content.replace(section, new_section, 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated: {filepath}")

print("Done.")
