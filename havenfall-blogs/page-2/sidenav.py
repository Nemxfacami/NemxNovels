import os
import re

ROOT_FOLDER = "."

NAV_LINKS = {
    "index.html": "https://nemxnovels.site/index.html",
    "landing-ravenport-blog.html": "https://nemxnovels.site/landing-ravenport-blog.html",
    "landing-havenfall-blog.html": "https://nemxnovels.site/landing-havenfall-blog.html",
    "videos-page-raven.html": "https://nemxnovels.site/videos-page-raven.html",
    "videos-page-haven.html": "https://nemxnovels.site/videos-page-haven.html",
    "stories-page.html": "https://nemxnovels.site/stories-page.html",
    "aboutnn.html": "https://nemxnovels.site/aboutnn.html",
    "profilepage.html": "https://nemxnovels.site/profilepage.html",
}


def replace_navigation_links(content):

    for relative, absolute in NAV_LINKS.items():

        # href="..."
        content = re.sub(
            rf'(href\s*=\s*["\']){re.escape(relative)}(["\'])',
            rf'\g<1>{absolute}\g<2>',
            content
        )

        # value="..."
        content = re.sub(
            rf'(value\s*=\s*["\']){re.escape(relative)}(["\'])',
            rf'\g<1>{absolute}\g<2>',
            content
        )

    return content


def process_html_file(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = replace_navigation_links(content)

    if new_content != content:

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Updated: {filepath}")


for root, dirs, files in os.walk(ROOT_FOLDER):

    for filename in files:

        if filename.lower().endswith((".html", ".htm")):

            filepath = os.path.join(root, filename)

            process_html_file(filepath)


print("\nDone.")
