from pathlib import Path
import re
import shutil
import html as html_module


# ============================================================
# NEMXNOVELS NEWS ARTICLE OG METADATA AUTO ADDER
# ============================================================

DOMAIN = "https://nemxnovels.site"

# Folder containing this script
SCRIPT_FOLDER = Path(__file__).resolve().parent


# ============================================================
# EXTRACT ARTICLE TITLE
# ============================================================

def get_article_title(html):
    """
    Extracts the article title from:

    <p id ="article-header-title">City to Increase Patrols at Silion Park</p>

    Handles:
        id="..."
        id ="..."
        id= "..."
        id = "..."

    Also handles whitespace before the actual title.
    """

    pattern = (
        r'<p\b'
        r'(?=[^>]*\bid\s*=\s*["\']article-header-title["\'])'
        r'[^>]*>'
        r'\s*(.*?)\s*'
        r'</p>'
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    title = match.group(1)

    # Remove any accidental HTML tags inside the title
    title = re.sub(
        r'<[^>]+>',
        ' ',
        title
    )

    # Decode HTML entities
    title = html_module.unescape(title)

    # Clean whitespace
    title = re.sub(
        r'\s+',
        ' ',
        title
    ).strip()

    return title if title else None


# ============================================================
# EXTRACT ARTICLE IMAGE
# ============================================================

def get_article_image(html):
    """
    Finds the <img> element whose class contains
    article-image.

    This is intentionally flexible.

    It handles things like:

    <img class ="article-image" src ="news-silion.png">

    <img class="article-image" src="news-silion.png" loading="lazy">

    <img src="news-silion.png" class="article-image">

    <img
        class="article-image"
        src="news-silion.png"
        loading="lazy"
    >

    The original HTML is NEVER modified.
    """

    # Find every img tag
    img_tags = re.findall(
        r'<img\b[^>]*>',
        html,
        re.IGNORECASE | re.DOTALL
    )

    for img_tag in img_tags:

        # ----------------------------------------------------
        # Check whether this image has article-image class
        # ----------------------------------------------------

        class_match = re.search(
            r'\bclass\s*=\s*["\']([^"\']*)["\']',
            img_tag,
            re.IGNORECASE
        )

        if not class_match:
            continue

        classes = class_match.group(1).split()

        if not any(
            class_name.lower() == "article-image"
            for class_name in classes
        ):
            continue

        # ----------------------------------------------------
        # Find src
        # ----------------------------------------------------

        src_match = re.search(
            r'\bsrc\s*=\s*["\']([^"\']+)["\']',
            img_tag,
            re.IGNORECASE
        )

        if not src_match:
            continue

        image_path = src_match.group(1).strip()

        # ----------------------------------------------------
        # Already a full URL
        # ----------------------------------------------------

        if image_path.startswith("http://"):
            return image_path

        if image_path.startswith("https://"):
            return image_path

        # ----------------------------------------------------
        # Local image
        # ----------------------------------------------------

        # Remove ./ or leading /
        image_path = image_path.lstrip("./")

        return f"{DOMAIN}/{image_path}"

    return None


# ============================================================
# EXTRACT ARTICLE TEXT
# ============================================================

def get_article_description(html):
    """
    Extracts the text inside:

    <article class="article-text">
        ...
    </article>

    Converts it into a short OG description.
    """

    pattern = (
        r'<article\b'
        r'(?=[^>]*\bclass\s*=\s*["\'][^"\']*\barticle-text\b[^"\']*["\'])'
        r'[^>]*>'
        r'(.*?)'
        r'</article>'
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    article_text = match.group(1)

    # --------------------------------------------------------
    # Remove HTML tags
    # --------------------------------------------------------

    article_text = re.sub(
        r'<[^>]+>',
        ' ',
        article_text
    )

    # --------------------------------------------------------
    # Decode HTML entities
    # --------------------------------------------------------

    article_text = html_module.unescape(
        article_text
    )

    # --------------------------------------------------------
    # Clean whitespace
    # --------------------------------------------------------

    article_text = re.sub(
        r'\s+',
        ' ',
        article_text
    ).strip()

    if not article_text:
        return None

    # --------------------------------------------------------
    # Remove repeated article title if present
    # --------------------------------------------------------

    title = get_article_title(html)

    if title:
        if article_text.lower().startswith(
            title.lower()
        ):
            article_text = article_text[
                len(title):
            ].strip()

    if not article_text:
        return None

    # --------------------------------------------------------
    # Limit description length
    # --------------------------------------------------------

    max_length = 155

    if len(article_text) > max_length:

        shortened = article_text[:max_length]

        # Don't cut a word in half
        if " " in shortened:
            shortened = shortened.rsplit(
                " ",
                1
            )[0]

        article_text = shortened + "..."

    return article_text


# ============================================================
# CREATE OG METADATA
# ============================================================

def create_metadata(html_file, html):
    """
    Extracts the title, description and image,
    then creates the complete NemxNovels OG metadata block.
    """

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = get_article_title(html)

    if not title:
        print("[ERROR] Could not find article title.")
        return None

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image_url = get_article_image(html)

    if not image_url:
        print("[ERROR] Could not find article image.")
        return None

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    description = get_article_description(html)

    if not description:
        print("[ERROR] Could not extract article description.")
        return None

    # --------------------------------------------------------
    # Escape metadata values
    # --------------------------------------------------------

    safe_title = html_module.escape(
        title,
        quote=True
    )

    safe_description = html_module.escape(
        description,
        quote=True
    )

    safe_image = html_module.escape(
        image_url,
        quote=True
    )

    # --------------------------------------------------------
    # NEWS ARTICLES LIVE AT ROOT
    # --------------------------------------------------------

    og_url = f"{DOMAIN}/{html_file.name}"

    # --------------------------------------------------------
    # Build metadata block
    # --------------------------------------------------------

    metadata = (
        '<!-- NEMXNOVELS ARTICLE META START '
        '(auto-generated — do not hand-edit) -->\n'
        f'<meta property="og:title" '
        f'content="{safe_title} | NemxNovels">\n'
        f'<meta property="og:description" '
        f'content="{safe_description}">\n'
        f'<meta property="og:image" '
        f'content="{safe_image}">\n'
        '<meta property="og:type" content="article">\n'
        f'<meta property="og:url" content="{og_url}">\n'
        '<!-- NEMXNOVELS ARTICLE META END -->'
    )

    return metadata


# ============================================================
# PROCESS ONE NEWS ARTICLE
# ============================================================

def process_file(html_file):

    print()
    print("-" * 60)
    print(f"Scanning: {html_file.name}")

    # --------------------------------------------------------
    # Read HTML
    # --------------------------------------------------------

    try:

        html = html_file.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        print("[ERROR] Could not read file as UTF-8.")
        print("[SKIPPED]")
        return

    # --------------------------------------------------------
    # Check existing metadata block
    # --------------------------------------------------------

    existing_meta = re.search(
        r'<!--\s*NEMXNOVELS ARTICLE META START\b',
        html,
        re.IGNORECASE
    )

    if existing_meta:

        print(
            "[SKIPPED] OG metadata block already exists."
        )

        return

    # --------------------------------------------------------
    # Check existing og:url
    # --------------------------------------------------------

    existing_og_url = re.search(
        r'<meta\b'
        r'(?=[^>]*\bproperty\s*=\s*["\']og:url["\'])'
        r'[^>]*>',
        html,
        re.IGNORECASE | re.DOTALL
    )

    if existing_og_url:

        print(
            "[SKIPPED] og:url already exists."
        )

        return

    # --------------------------------------------------------
    # Create metadata
    # --------------------------------------------------------

    metadata = create_metadata(
        html_file,
        html
    )

    if not metadata:

        print(
            "[SKIPPED] File was not changed."
        )

        return

    # --------------------------------------------------------
    # Extract information for display
    # --------------------------------------------------------

    title = get_article_title(html)

    image_url = get_article_image(html)

    description = get_article_description(html)

    og_url = f"{DOMAIN}/{html_file.name}"

    print()
    print("Extracted metadata:")

    print()
    print("Title:")
    print(f"  {title}")

    print()
    print("Image:")
    print(f"  {image_url}")

    print()
    print("Description:")
    print(f"  {description}")

    print()
    print("OG URL:")
    print(f"  {og_url}")

    # --------------------------------------------------------
    # Find <head>
    # --------------------------------------------------------

    head_match = re.search(
        r'<head\b[^>]*>',
        html,
        re.IGNORECASE
    )

    if not head_match:

        print()
        print("[ERROR] Could not find <head>.")
        print("[SKIPPED] File was not changed.")

        return

    # --------------------------------------------------------
    # Insert metadata directly after <head>
    # --------------------------------------------------------

    insert_position = head_match.end()

    updated_html = (
        html[:insert_position]
        + "\n\n     "
        + metadata
        + "\n"
        + html[insert_position:]
    )

    # --------------------------------------------------------
    # Create backup
    # --------------------------------------------------------

    backup_file = html_file.with_name(
        html_file.name + ".backup"
    )

    try:

        shutil.copy2(
            html_file,
            backup_file
        )

    except Exception as error:

        print()
        print("[ERROR] Could not create backup.")
        print(error)
        print("[SKIPPED] File was not changed.")

        return

    # --------------------------------------------------------
    # Write updated HTML
    # --------------------------------------------------------

    try:

        html_file.write_text(
            updated_html,
            encoding="utf-8"
        )

    except Exception as error:

        print()
        print("[ERROR] Could not write HTML file.")
        print(error)
        print("[SKIPPED]")

        return

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print()
    print("[SUCCESS] OG metadata added.")
    print(
        f"Backup created: {backup_file.name}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("NEMXNOVELS NEWS OG METADATA AUTO ADDER")
    print("=" * 60)

    print()
    print("Folder:")
    print(SCRIPT_FOLDER)

    # --------------------------------------------------------
    # Find ONLY news-*.html
    # --------------------------------------------------------

    news_files = sorted(
        SCRIPT_FOLDER.glob("news-*.html")
    )

    # --------------------------------------------------------
    # Strictly allow only:
    #
    # news-1.html
    # news-2.html
    # news-15.html
    #
    # This automatically excludes:
    #
    # news-page.html
    # --------------------------------------------------------

    news_files = [
        file
        for file in news_files
        if re.match(
            r"^news-\d+\.html$",
            file.name,
            re.IGNORECASE
        )
    ]

    # --------------------------------------------------------
    # Nothing found
    # --------------------------------------------------------

    if not news_files:

        print()
        print("No news-X.html files found.")

        return

    print()
    print(
        f"Found {len(news_files)} news article(s)."
    )

    # --------------------------------------------------------
    # Process all news articles
    # --------------------------------------------------------

    for html_file in news_files:

        process_file(
            html_file
        )

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()