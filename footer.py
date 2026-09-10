from pathlib import Path
import re

# ============================================================
# NEMXNOVELS ARTICLE FOOTER SCRIPT
# ============================================================

# NemxNovels root directory
ROOT = Path(__file__).resolve().parent

# Footer that will be inserted after each article
FOOTER_HTML = """<div id ="footer">
© 2026 NemxNovels. All rights reserved. Original content is protected by copyright unless otherwise stated.
</div>"""


# ============================================================
# GET CORRECT PATH TO footer.css
# ============================================================

def get_footer_css_path(html_file):
    """
    Calculate the relative path from the HTML file
    back to footer.css in the NemxNovels root.
    """

    relative_folder = html_file.parent.relative_to(ROOT)

    depth = len(relative_folder.parts)

    if depth == 0:
        return "footer.css"

    return "../" * depth + "footer.css"


# ============================================================
# ADD footer.css
# ============================================================

def add_footer_css(content, html_file):

    # Don't add footer.css twice
    if re.search(
        r'<link\b[^>]*href\s*=\s*["\'][^"\']*footer\.css["\']',
        content,
        re.IGNORECASE
    ):
        return content, False

    # Find <head>
    head_match = re.search(
        r'<head\b[^>]*>(.*?)</head>',
        content,
        re.IGNORECASE | re.DOTALL
    )

    if not head_match:
        print(f"WARNING: No <head> found: {html_file}")
        return content, False

    head_content = head_match.group(1)

    # Find ALL stylesheet links
    stylesheet_links = list(
        re.finditer(
            r'<link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*>',
            head_content,
            re.IGNORECASE
        )
    )

    if not stylesheet_links:
        print(f"WARNING: No stylesheet links found: {html_file}")
        return content, False

    # Get the LAST stylesheet link
    last_stylesheet = stylesheet_links[-1]

    css_path = get_footer_css_path(html_file)

    footer_link = (
        f'<link rel ="stylesheet" type ="text/css" href ="{css_path}">'
    )

    # Insert directly after the last stylesheet
    insert_position = last_stylesheet.end()

    new_head = (
        head_content[:insert_position]
        + "\n"
        + "     "
        + footer_link
        + head_content[insert_position:]
    )

    new_content = (
        content[:head_match.start(1)]
        + new_head
        + content[head_match.end(1):]
    )

    return new_content, True


# ============================================================
# FIND THE END OF AN ARTICLE
# ============================================================

def find_article_end(content, start_position):

    """
    Starting from an <article> opening tag, find its
    matching </article>.

    This safely handles nested elements inside the article.
    """

    article_tags = re.compile(
        r'<article\b[^>]*>|</article\s*>',
        re.IGNORECASE
    )

    depth = 0

    for match in article_tags.finditer(content, start_position):

        tag = match.group(0).lower()

        if tag.startswith("<article"):
            depth += 1

        else:
            depth -= 1

            if depth == 0:
                return match.end()

    return None


# ============================================================
# FIND ARTICLE TYPES
# ============================================================

def find_articles(content):

    """
    Find desktop article-text and mobile-article-text.

    Returns their positions.
    """

    pattern = re.compile(
        r'<article\b[^>]*class\s*=\s*["\']([^"\']*)["\'][^>]*>',
        re.IGNORECASE
    )

    articles = []

    for match in pattern.finditer(content):

        classes = match.group(1).split()

        if "article-text" in classes:
            articles.append(
                ("desktop", match.start())
            )

        elif "mobile-article-text" in classes:
            articles.append(
                ("mobile", match.start())
            )

    return articles


# ============================================================
# ADD FOOTERS AFTER ARTICLES
# ============================================================

def add_article_footers(content):

    articles = find_articles(content)

    if not articles:
        return content, 0

    added = 0

    # Work backwards so positions don't become invalid
    for article_type, article_start in reversed(articles):

        article_end = find_article_end(
            content,
            article_start
        )

        if article_end is None:
            print(
                f"WARNING: Could not find closing </article> "
                f"for {article_type} article."
            )
            continue

        # Look immediately after the article
        after_article = content[article_end:]

        # Don't add another footer if one already exists
        if re.match(
            r'\s*<div\s+id\s*=\s*["\']footer["\']',
            after_article,
            re.IGNORECASE
        ):
            continue

        # Add footer
        content = (
            content[:article_end]
            + "\n\n"
            + FOOTER_HTML
            + content[article_end:]
        )

        added += 1

    return content, added


# ============================================================
# PROCESS ONE HTML FILE
# ============================================================

def process_html_file(html_file):

    try:
        content = html_file.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:
        print(
            f"SKIPPED encoding problem: {html_file}"
        )
        return

    # ========================================================
    # ONLY PROCESS ARTICLE PAGES
    # ========================================================

    if not re.search(
        r'<article\b[^>]*class\s*=\s*["\'][^"\']*article-text',
        content,
        re.IGNORECASE
    ):
        return

    original_content = content

    # ========================================================
    # ADD footer.css
    # ========================================================

    content, css_added = add_footer_css(
        content,
        html_file
    )

    # ========================================================
    # ADD ARTICLE FOOTERS
    # ========================================================

    content, footers_added = add_article_footers(
        content
    )

    # ========================================================
    # SAVE
    # ========================================================

    if content != original_content:

        html_file.write_text(
            content,
            encoding="utf-8"
        )

        print(
            f"UPDATED: {html_file}"
        )

        print(
            f"    footer.css: "
            f"{'ADDED' if css_added else 'already exists'}"
        )

        print(
            f"    Footers added: {footers_added}"
        )

    else:

        print(
            f"ALREADY OK: {html_file}"
        )


# ============================================================
# FIND ALL HTML FILES
# ============================================================

html_files = list(
    ROOT.rglob("*.html")
)

print(
    f"\nFound {len(html_files)} HTML files."
)

print(
    "\nScanning for article pages...\n"
)


# ============================================================
# PROCESS FILES
# ============================================================

for html_file in html_files:

    process_html_file(html_file)


print(
    "\nFinished."
)