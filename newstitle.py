import os
import re

# Go through every HTML file in this folder
for filename in os.listdir("."):

    # Only process news-1.html, news-2.html...
    # and hnews-1.html, hnews-2.html...
    if not re.match(r"^(news|hnews)-\d+\.html$", filename, re.IGNORECASE):
        continue

    print(f"Processing {filename}...")

    # Read file
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    # Find og:title
    match = re.search(
        r'<meta\s+property\s*=\s*["\']og:title["\']\s+content\s*=\s*["\'](.*?)["\']',
        html,
        re.IGNORECASE
    )

    if not match:
        print(f"   ❌ No og:title found in {filename}")
        continue

    # Get article title
    article_title = match.group(1).strip()

    # Remove existing NemxNovels suffix
    article_title = re.sub(
        r"\s*\|\s*NemxNovels\s*$",
        "",
        article_title,
        flags=re.IGNORECASE
    ).strip()

    # Create browser title
    new_title = f"{article_title} | Ravenport News NemxNovels"

    # Find the title tag
    title_pattern = r"<title\b[^>]*>.*?</title>"

    if re.search(title_pattern, html, re.IGNORECASE | re.DOTALL):

        # Replace existing title
        html = re.sub(
            title_pattern,
            f"<title>{new_title}</title>",
            html,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )

    else:

        # If no title tag exists, add one after <head>
        head_pattern = r"<head\b[^>]*>"

        if re.search(head_pattern, html, re.IGNORECASE):

            html = re.sub(
                head_pattern,
                lambda m: m.group(0) + f'\n\n     <title>{new_title}</title>',
                html,
                count=1,
                flags=re.IGNORECASE
            )

        else:
            print(f"   ❌ No <head> tag found in {filename}")
            continue

    # Save file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"   ✅ {new_title}")


print("\n================================")
print("DONE")
print("================================")
