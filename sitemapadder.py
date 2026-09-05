
from pathlib import Path
import re
from datetime import date
from xml.sax.saxutils import escape


# ============================================================
# NEMXNOVELS SITEMAP GENERATOR + OG URL VALIDATOR
# ============================================================

DOMAIN = "https://nemxnovels.site"

# Folder containing this script / website
SCRIPT_FOLDER = Path(__file__).resolve().parent

# Sitemap output file
SITEMAP_FILE = SCRIPT_FOLDER / "sitemap.xml"


# ============================================================
# EXTRACT OG URL
# ============================================================

def get_og_url(html):
    """
    Extracts:

    <meta property="og:url" content="https://nemxnovels.site/page.html">

    Returns the URL or None.
    """

    pattern = re.compile(
        r'<meta\b'
        r'(?=[^>]*\bproperty\s*=\s*["\']og:url["\'])'
        r'[^>]*\bcontent\s*=\s*["\']([^"\']+)["\']'
        r'[^>]*>',
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(html)

    if not match:
        return None

    return match.group(1).strip()


# ============================================================
# CONVERT FILE PATH TO EXPECTED WEBSITE URL
# ============================================================

def get_expected_url(html_file):
    """
    Converts:

    ./ravenport-blogs/page-2/page2.html

    into:

    https://nemxnovels.site/ravenport-blogs/page-2/page2.html
    """

    relative_path = html_file.relative_to(
        SCRIPT_FOLDER
    )

    # Convert Windows \ into /
    relative_url = str(
        relative_path
    ).replace("\\", "/")

    return f"{DOMAIN}/{relative_url}"


# ============================================================
# NORMALIZE URL FOR COMPARISON
# ============================================================

def normalize_url(url):
    """
    Makes URL comparison reliable.

    Example:

    https://nemxnovels.site/page.html
    https://nemxnovels.site/page.html/

    can be compared consistently.

    Does NOT remove meaningful path structure.
    """

    url = url.strip()

    # Remove trailing slash except for domain root
    if url != DOMAIN and url.endswith("/"):
        url = url.rstrip("/")

    # Remove accidental double slashes after domain
    url = re.sub(
        r'(?<!:)//+',
        '/',
        url
    )

    return url


# ============================================================
# DETERMINE LAST MODIFIED DATE
# ============================================================

def get_last_modified(html_file):
    """
    Uses the actual HTML file modification date.

    This means the sitemap automatically gets the date
    the file was last changed.
    """

    timestamp = html_file.stat().st_mtime

    return date.fromtimestamp(
        timestamp
    ).isoformat()


# ============================================================
# DETERMINE CHANGE FREQUENCY
# ============================================================

def get_changefreq(html_file):
    """
    Basic automatic rules.

    You can customize these later.
    """

    name = html_file.name.lower()

    # Homepage
    if name == "index.html":
        return "daily"

    # News
    if name.startswith("news-") or name.startswith("hnews-"):
        return "weekly"

    # Articles / blogs
    if "blog" in str(html_file).lower():
        return "monthly"

    # Default
    return "monthly"


# ============================================================
# DETERMINE PRIORITY
# ============================================================

def get_priority(html_file):
    """
    Basic sitemap priority rules.
    """

    name = html_file.name.lower()

    # Homepage
    if name == "index.html":
        return "1.0"

    # Main news page
    if name == "news-page.html":
        return "0.9"

    # News articles
    if name.startswith("news-") or name.startswith("hnews-"):
        return "0.8"

    # Everything else
    return "0.7"


# ============================================================
# CREATE SITEMAP ENTRY
# ============================================================

def create_url_entry(
    url,
    lastmod,
    changefreq,
    priority
):

    return (
        "    <url>\n"
        f"        <loc>{escape(url)}</loc>\n"
        f"        <lastmod>{lastmod}</lastmod>\n"
        f"        <changefreq>{changefreq}</changefreq>\n"
        f"        <priority>{priority}</priority>\n"
        "    </url>\n"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 80)
    print("NEMXNOVELS SITEMAP GENERATOR")
    print("=" * 80)

    print()
    print("Website folder:")
    print(SCRIPT_FOLDER)

    print()
    print("Scanning all HTML files...")
    print()

    # --------------------------------------------------------
    # Find every HTML file recursively
    # --------------------------------------------------------

    html_files = sorted(
        SCRIPT_FOLDER.rglob("*.html")
    )

    print(
        f"Found {len(html_files)} HTML file(s)."
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    valid_entries = []

    missing_og_url = []
    incorrect_og_url = []
    unreadable_files = []

    # --------------------------------------------------------
    # Scan every HTML file
    # --------------------------------------------------------

    for html_file in html_files:

        try:

            html = html_file.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            unreadable_files.append(
                str(
                    html_file.relative_to(
                        SCRIPT_FOLDER
                    )
                )
            )

            continue

        # ----------------------------------------------------
        # Get OG URL
        # ----------------------------------------------------

        og_url = get_og_url(html)

        if not og_url:

            missing_og_url.append(
                str(
                    html_file.relative_to(
                        SCRIPT_FOLDER
                    )
                )
            )

            continue

        # ----------------------------------------------------
        # Expected URL from actual file path
        # ----------------------------------------------------

        expected_url = get_expected_url(
            html_file
        )

        # ----------------------------------------------------
        # Compare
        # ----------------------------------------------------

        if normalize_url(og_url) != normalize_url(
            expected_url
        ):

            incorrect_og_url.append(
                (
                    str(
                        html_file.relative_to(
                            SCRIPT_FOLDER
                        )
                    ),
                    og_url,
                    expected_url
                )
            )

            continue

        # ----------------------------------------------------
        # CORRECT
        # ----------------------------------------------------

        print(
            f"[OK] {html_file.relative_to(SCRIPT_FOLDER)}"
        )

        valid_entries.append(
            create_url_entry(
                og_url,
                get_last_modified(html_file),
                get_changefreq(html_file),
                get_priority(html_file)
            )
        )

    # ========================================================
    # CREATE SITEMAP
    # ========================================================

    sitemap_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "\n"
        + "\n".join(valid_entries)
        + "\n"
        "</urlset>\n"
    )

    try:

        SITEMAP_FILE.write_text(
            sitemap_content,
            encoding="utf-8"
        )

        sitemap_created = True

    except Exception as error:

        sitemap_created = False

        print()
        print("[ERROR] Could not create sitemap.xml")
        print(error)

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print()
    print("=" * 80)
    print("SCAN COMPLETE")
    print("=" * 80)

    print()
    print(f"HTML FILES SCANNED:       {len(html_files)}")
    print(f"VALID SITEMAP ENTRIES:    {len(valid_entries)}")
    print(f"MISSING OG URL:           {len(missing_og_url)}")
    print(f"INCORRECT OG URL:         {len(incorrect_og_url)}")
    print(f"UNREADABLE FILES:         {len(unreadable_files)}")

    # ========================================================
    # MISSING OG URLS
    # ========================================================

    if missing_og_url:

        print()
        print("=" * 80)
        print("FILES WITHOUT OG:URL")
        print("=" * 80)

        for file in missing_og_url:
            print()
            print(f"FILE: {file}")
            print("OG URL: NOT FOUND")

    # ========================================================
    # INCORRECT OG URLS
    # ========================================================

    if incorrect_og_url:

        print()
        print("=" * 80)
        print("FILES WITH INCORRECT OG:URL")
        print("=" * 80)

        for file, og_url, expected_url in incorrect_og_url:

            print()
            print(f"FILE: {file}")
            print(f"OG URL:       {og_url}")
            print(f"EXPECTED URL: {expected_url}")

    # ========================================================
    # UNREADABLE FILES
    # ========================================================

    if unreadable_files:

        print()
        print("=" * 80)
        print("FILES THAT COULD NOT BE READ")
        print("=" * 80)

        for file in unreadable_files:

            print()
            print(f"FILE: {file}")

    # ========================================================
    # SITEMAP RESULT
    # ========================================================

    print()
    print("=" * 80)

    if sitemap_created:

        print("SITEMAP CREATED SUCCESSFULLY")
        print()
        print(f"FILE: {SITEMAP_FILE}")
        print(f"ENTRIES: {len(valid_entries)}")

    else:

        print("SITEMAP CREATION FAILED")

    print("=" * 80)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()

