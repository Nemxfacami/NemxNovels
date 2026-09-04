from pathlib import Path
import re
import shutil


# ============================================================
# NEMXNOVELS OG:URL AUTO ADDER
# ============================================================

# Your website
DOMAIN = "https://nemxnovels.site"

# This script scans the folder where the script itself is located
SCRIPT_FOLDER = Path(__file__).resolve().parent


def get_website_path():
    """
    Builds the website folder path from the location of this script.

    Example:
        C:/NemxNovels/ravenport-blogs/page-2/

    becomes:
        /ravenport-blogs/page-2/
    """

    # Find the NemxNovels site folder somewhere above this script
    parts = SCRIPT_FOLDER.parts

    try:
        site_index = next(
            i for i, part in enumerate(parts)
            if part.lower() == "nemxnovels"
        )

        website_parts = parts[site_index + 1:]

        if not website_parts:
            return ""

        return "/" + "/".join(website_parts)

    except StopIteration:
        # If the main NemxNovels folder isn't found,
        # use the folder name structure directly.
        return "/" + "/".join(SCRIPT_FOLDER.parts[-2:])


def create_og_url(filename):
    """
    Creates the full OG URL from the HTML filename.
    """

    website_path = get_website_path()

    return f"{DOMAIN}{website_path}/{filename}"


def process_file(html_file):
    """
    Adds og:url to one HTML file.
    """

    print(f"\nScanning: {html_file.name}")

    # Read the HTML
    html = html_file.read_text(encoding="utf-8")

    # --------------------------------------------------------
    # Check if og:url already exists
    # --------------------------------------------------------

    if re.search(
        r'<meta\s+property=["\']og:url["\']',
        html,
        re.IGNORECASE
    ):
        print("  [SKIPPED] og:url already exists.")
        return

    # --------------------------------------------------------
    # Make sure this is one of the article files
    # --------------------------------------------------------

    if not re.match(r"harticle-\d+\.html$", html_file.name, re.IGNORECASE):
        print("  [SKIPPED] Filename is not an harticle-X.html file.")
        return

    # --------------------------------------------------------
    # Create the URL
    # --------------------------------------------------------

    og_url = create_og_url(html_file.name)

    og_url_tag = (
        f'<meta property="og:url" content="{og_url}">'
    )

    # --------------------------------------------------------
    # Find the OG TYPE tag
    # --------------------------------------------------------

    pattern = (
        r'(<meta\s+property=["\']og:type["\']'
        r'\s+content=["\']article["\']\s*>)'
    )

    match = re.search(
        pattern,
        html,
        re.IGNORECASE
    )

    if not match:
        print("  [ERROR] Could not find the og:type tag.")
        print("  [SKIPPED] File was not changed.")
        return

    # --------------------------------------------------------
    # Create backup
    # --------------------------------------------------------

    backup_file = html_file.with_suffix(".html.backup")

    shutil.copy2(
        html_file,
        backup_file
    )

    # --------------------------------------------------------
    # Insert og:url immediately after og:type
    # --------------------------------------------------------

    replacement = (
        match.group(1)
        + "\n"
        + og_url_tag
    )

    updated_html = html[:match.start()] + replacement + html[match.end():]

    # --------------------------------------------------------
    # Save modified HTML
    # --------------------------------------------------------

    html_file.write_text(
        updated_html,
        encoding="utf-8"
    )

    print("  [ADDED]")
    print(f"  {og_url}")
    print(f"  Backup: {backup_file.name}")


def main():

    print("=" * 60)
    print("NEMXNOVELS OG:URL AUTO ADDER")
    print("=" * 60)

    print(f"\nFolder being scanned:")
    print(SCRIPT_FOLDER)

    print("\nWebsite path detected:")
    print(get_website_path())

    # --------------------------------------------------------
    # Find HTML files
    # --------------------------------------------------------

    html_files = sorted(
        SCRIPT_FOLDER.glob("harticle-*.html")
    )

    if not html_files:
        print("\nNo article-X.html files found.")
        return

    print(f"\nFound {len(html_files)} article file(s).")

    # --------------------------------------------------------
    # Process each article
    # --------------------------------------------------------

    for html_file in html_files:
        process_file(html_file)

    print("\n" + "=" * 60)
    print("SCAN COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
