import os
import re

folder = "."

rapha_card = '''        <div id ="mobile-book-cover">
             <a href ="ravenport/raphaasylum/">
             <img class ="mobile-book-cover" src ="raphaasylum-cover.webp"/>
             </a>
        </div>
'''

for filename in os.listdir(folder):
    if not filename.lower().endswith(".html"):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    original_content = content

    # Find the mobile book list section
    pattern = r'(<section\s+class\s*=\s*"mobile-header-book-list"\s*>)(.*?)(</section>)'

    match = re.search(pattern, content, flags=re.IGNORECASE | re.DOTALL)

    if not match:
        print(f"Skipped: {filename} (book list not found)")
        continue

    # Don't add it twice
    if "ravenport/raphaasylum/" in match.group(2):
        print(f"Skipped: {filename} (Rapha Asylum already exists)")
        continue

    # Insert Rapha Asylum before the closing </section>
    new_section = match.group(1) + match.group(2) + rapha_card + match.group(3)

    content = content[:match.start()] + new_section + content[match.end():]

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Updated: {filename}")

print("\nDone.")