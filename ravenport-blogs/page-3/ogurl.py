
from pathlib import Path
import re
import shutil


# ============================================================
# NEMXNOVELS OG:URL AUTO ADDER
# ============================================================

# Folder containing this script
SCRIPT_FOLDER = Path(__file__).resolve().parent


def get_og_image_url(html):
    """
    Finds the existing og:image URL.

    IMPORTANT:
    The og:image itself is NEVER modified.
    We only copy its directory path.
    """

    pattern = (
        r'<meta\s+property=["\']og:image["\']'
        r'\s+content=["\']([^"\']+)["\']'
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE
    )

    if not match:
        return None

    return match.group(1)


def create_og_url(html_file, html):
    """
    Creates the og:url by taking the directory path
    from og:image and replacing the image filename
    with the HTML filename.

    Example:

    og:image:
    https://nemxnovels.site/havenfall-blogs/page-2/future.webp

    HTML filename:
    article-5.html

    Result:
    https://nemxnovels.site/havenfall-blogs/page-2/article-5.html
    """

    og_image_url = get_og_image_url(html)

    if not og_image_url:
        return None

    # Make sure this is a NemxNovels URL
    if not og_image_url.startswith("https://nemxnovels.site/"):
        return None

    # Find the final slash.
    # Everything BEFORE the image filename is preserved.
    last_slash = og_image_url.rfind("/")

    if last_slash == -1:
        return None

    directory_path = og_image_url[:last_slash + 1]

    # Use the actual HTML filename
    filename = html_file.name

    return directory_path + filename


def process_file(html_file):
    """
    Process one article HTML file.
    """

    print()
    print("-" * 60)
    print(f"Scanning: {html_file.name}")

    # --------------------------------------------------------
    # Read HTML
    # --------------------------------------------------------

    try:
        html = html_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("[ERROR] Could not read file as UTF-8.")
        print("[SKIPPED]")
        return

    # --------------------------------------------------------
    # Check if og:url already exists
    # --------------------------------------------------------

    existing_og_url = re.search(
        r'<meta\s+property=["\']og:url["\']',
        html,
        re.IGNORECASE
    )

    if existing_og_url:
        print("[SKIPPED] og:url already exists.")
        return

    # --------------------------------------------------------
    # Make sure the article has an og:image
    # --------------------------------------------------------

    og_image_url = get_og_image_url(html)

    if not og_image_url:
        print("[ERROR] No og:image found.")
        print("[SKIPPED] File was not changed.")
        return

    print(f"Existing og:image:")
    print(f"  {og_image_url}")

    # --------------------------------------------------------
    # Create og:url
    # --------------------------------------------------------

    og_url = create_og_url(
        html_file,
        html
    )

    if not og_url:
        print("[ERROR] Could not create og:url.")
        print("[SKIPPED] File was not changed.")
        return

    print()
    print("Generated og:url:")
    print(f"  {og_url}")

    # --------------------------------------------------------
    # Find the NEMXNOVELS META block
    # --------------------------------------------------------

    meta_start = re.search(
        r'<!--\s*NEMXNOVELS ARTICLE META START\b.*?-->',
        html,
        re.IGNORECASE
    )

    meta_end = re.search(
        r'<!--\s*NEMXNOVELS ARTICLE META END\s*-->',
        html,
        re.IGNORECASE
    )

    if not meta_start or not meta_end:
        print()
        print("[ERROR] NEMXNOVELS ARTICLE META block not found.")
        print("[SKIPPED] File was not changed.")
        return

    # Make sure END comes after START
    if meta_end.start() <= meta_start.end():
        print()
        print("[ERROR] Invalid META block.")
        print("[SKIPPED] File was not changed.")
        return

    # --------------------------------------------------------
    # Find og:type INSIDE the metadata block
    # --------------------------------------------------------

    meta_block = html[
        meta_start.end():meta_end.start()
    ]

    og_type_match = re.search(
        r'<meta\s+property=["\']og:type["\']'
        r'\s+content=["\']article["\']\s*>',
        meta_block,
        re.IGNORECASE
    )

    if not og_type_match:
        print()
        print("[ERROR] og:type not found inside META block.")
        print("[SKIPPED] File was not changed.")
        return

    # --------------------------------------------------------
    # Create the new tag
    # --------------------------------------------------------

    og_url_tag = (
        f'<meta property="og:url" content="{og_url}">'
    )

    # Insert directly after og:type
    updated_meta_block = (
        meta_block[:og_type_match.end()]
        + "\n"
        + og_url_tag
        + meta_block[og_type_match.end():]
    )

    # Replace ONLY the metadata block contents
    updated_html = (
        html[:meta_start.end()]
        + updated_meta_block
        + html[meta_end.start():]
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
    print("[SUCCESS] og:url added.")
    print(f"Backup created: {backup_file.name}")


def main():

    print("=" * 60)
    print("NEMXNOVELS OG:URL AUTO ADDER")
    print("=" * 60)

    print()
    print("Folder:")
    print(SCRIPT_FOLDER)

    # --------------------------------------------------------
    # Find article files
    # --------------------------------------------------------

    article_files = sorted(
        SCRIPT_FOLDER.glob("article-*.html")
    )

    if not article_files:
        print()
        print("No article-*.html files found.")
        return

    print()
    print(f"Found {len(article_files)} article file(s).")

    # --------------------------------------------------------
    # Process every article
    # --------------------------------------------------------

    for html_file in article_files:
        process_file(html_file)

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

