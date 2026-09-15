#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import argparse
import re
import sys
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

SITE_URL = "https://nemxnovels.site"

PROJECT_ROOT = Path(__file__).resolve().parent
SITEMAP_FILE = PROJECT_ROOT / "sitemap.xml"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
}


# ============================================================
# HTML META PARSER
# ============================================================

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "link" and tag.lower() != "meta":
            return

        attrs_dict = {
            key.lower(): value
            for key, value in attrs
            if key and value is not None
        }

        # ----------------------------------------------------
        # Canonical
        # ----------------------------------------------------
        if tag.lower() == "link":
            rel = attrs_dict.get("rel", "").lower()

            if "canonical" in rel:
                href = attrs_dict.get("href")

                if href:
                    self.canonical = href.strip()

        # ----------------------------------------------------
        # Open Graph URL
        # ----------------------------------------------------
        elif tag.lower() == "meta":
            prop = attrs_dict.get("property", "").lower()

            if prop == "og:url":
                content = attrs_dict.get("content")

                if content:
                    self.og_url = content.strip()


# ============================================================
# HELPERS
# ============================================================

def is_html_file(path: Path):
    return path.suffix.lower() == ".html"


def should_skip(path: Path):
    return any(part in EXCLUDED_DIRS for part in path.parts)


def normalize_url(url):
    """
    Normalize URLs enough for sitemap comparison.

    Does NOT alter legitimate URL paths such as:
        /ravenport/back&forth/

    XML escaping is handled later by ElementTree.
    """

    if not url:
        return None

    url = url.strip()

    if not url:
        return None

    # Only accept URLs belonging to this website.
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return None

    if parsed.netloc.lower() != "nemxnovels.site":
        return None

    # Remove fragments because sitemap URLs should not contain them.
    url = url.split("#", 1)[0]

    # Remove query strings from sitemap URLs.
    url = url.split("?", 1)[0]

    # Normalize trailing slash for the root.
    if url == SITE_URL:
        return SITE_URL + "/"

    return url


def canonicalize_index_url(url):
    """
    If a URL ends in /index.html, convert it to the directory URL.

    Example:
        https://nemxnovels.site/ravenport/original-story/index.html

    becomes:

        https://nemxnovels.site/ravenport/original-story/
    """

    if not url:
        return url

    if url.endswith("/index.html"):
        return url[:-10] + "/"

    if url.endswith("/index.htm"):
        return url[:-9] + "/"

    if url == SITE_URL + "/index.html":
        return SITE_URL + "/"

    return url


def get_relative_html_files():
    """
    Scan the repository recursively for HTML files.
    """

    html_files = []

    for path in PROJECT_ROOT.rglob("*.html"):

        if should_skip(path):
            continue

        html_files.append(path)

    return sorted(html_files)


def parse_html_file(path):
    """
    Extract canonical and og:url from one HTML file.
    """

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None, None, f"Could not read file: {e}"

    parser = MetaParser()

    try:
        parser.feed(text)
    except Exception as e:
        return None, None, f"Could not parse HTML: {e}"

    return parser.canonical, parser.og_url, None


# ============================================================
# EXISTING SITEMAP READER
# ============================================================

def load_existing_sitemap():
    """
    Read the current sitemap and store metadata by URL.

    The old sitemap is NOT used as the source of URLs.

    It is only used to preserve:
        lastmod
        changefreq
        priority
    """

    metadata = {}

    if not SITEMAP_FILE.exists():
        print("[INFO] No existing sitemap.xml found.")
        return metadata

    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
    except Exception as e:
        print(f"[WARNING] Could not parse existing sitemap.xml: {e}")
        return metadata

    namespace = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
    }

    for url_node in root.findall("sm:url", namespace):

        loc_node = url_node.find("sm:loc", namespace)

        if loc_node is None or not loc_node.text:
            continue

        old_url = normalize_url(loc_node.text)

        if not old_url:
            continue

        # Make old /index.html entries comparable to the new
        # clean directory canonical URLs.
        old_url = canonicalize_index_url(old_url)

        data = {}

        for tag in ("lastmod", "changefreq", "priority"):
            node = url_node.find(f"sm:{tag}", namespace)

            if node is not None and node.text:
                data[tag] = node.text.strip()

        # Keep the first valid metadata set.
        if old_url not in metadata:
            metadata[old_url] = data

    return metadata


# ============================================================
# FILE-BASED FALLBACK METADATA
# ============================================================

def file_last_modified_date(path):
    """
    Fallback lastmod based on the actual file modification date.

    This is only used when the old sitemap has no metadata
    for a newly discovered URL.
    """

    try:
        timestamp = path.stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d")


# ============================================================
# SCAN HTML
# ============================================================

def scan_html_files():
    """
    Scan all HTML files and return sitemap candidates.
    """

    files = get_relative_html_files()

    results = []

    missing_canonical = []
    missing_og = []
    errors = []

    for path in files:

        canonical, og_url, error = parse_html_file(path)

        relative = path.relative_to(PROJECT_ROOT)

        if error:
            errors.append((relative, error))
            continue

        canonical_normalized = normalize_url(canonical)
        og_normalized = normalize_url(og_url)

        canonical_normalized = canonicalize_index_url(
            canonical_normalized
        )

        og_normalized = canonicalize_index_url(
            og_normalized
        )

        if not canonical_normalized:
            missing_canonical.append(relative)

        if not og_normalized:
            missing_og.append(relative)

        # ----------------------------------------------------
        # SOURCE OF TRUTH
        #
        # Canonical wins.
        # OG URL is only fallback.
        # ----------------------------------------------------

        sitemap_url = canonical_normalized or og_normalized

        if sitemap_url:

            results.append({
                "file": relative,
                "url": sitemap_url,
                "canonical": canonical_normalized,
                "og_url": og_normalized,
            })

    return results, missing_canonical, missing_og, errors


# ============================================================
# BUILD UNIQUE URL DATA
# ============================================================

def build_url_data(results, old_metadata):
    """
    Deduplicate URLs and attach sitemap metadata.
    """

    urls = {}

    duplicates = []

    for item in results:

        url = item["url"]

        if url in urls:
            duplicates.append(
                (url, urls[url]["file"], item["file"])
            )
            continue

        metadata = old_metadata.get(url, {})

        data = {
            "url": url,
            "file": item["file"],
            "lastmod": metadata.get(
                "lastmod",
                file_last_modified_date(
                    PROJECT_ROOT / item["file"]
                )
            ),
            "changefreq": metadata.get(
                "changefreq",
                "monthly"
            ),
            "priority": metadata.get(
                "priority",
                "0.7"
            ),
        }

        urls[url] = data

    return urls, duplicates


# ============================================================
# VALIDATION
# ============================================================

def validate_urls(urls):
    problems = []

    for url in urls:

        if not url.startswith(SITE_URL + "/"):
            problems.append(
                f"Outside site: {url}"
            )

        if "/index.html" in url:
            problems.append(
                f"/index.html still present: {url}"
            )

        if "://" not in url:
            problems.append(
                f"Malformed URL: {url}"
            )

    return problems


# ============================================================
# CREATE SITEMAP XML
# ============================================================

def create_sitemap(urls):
    """
    Completely rebuild sitemap.xml from the newly scanned URLs.
    """

    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")

    root = ET.Element(
        "urlset",
        {
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"
        }
    )

    # Sort URLs alphabetically for predictable output.
    for url in sorted(urls.keys()):

        data = urls[url]

        url_node = ET.SubElement(root, "url")

        loc = ET.SubElement(url_node, "loc")
        loc.text = data["url"]

        if data.get("lastmod"):
            lastmod = ET.SubElement(url_node, "lastmod")
            lastmod.text = data["lastmod"]

        if data.get("changefreq"):
            changefreq = ET.SubElement(url_node, "changefreq")
            changefreq.text = data["changefreq"]

        if data.get("priority"):
            priority = ET.SubElement(url_node, "priority")
            priority.text = data["priority"]

    tree = ET.ElementTree(root)

    ET.indent(tree, space="  ")

    return tree


# ============================================================
# WRITE SITEMAP
# ============================================================

def write_sitemap(tree):
    """
    Write the freshly generated sitemap.
    """

    tree.write(
        SITEMAP_FILE,
        encoding="UTF-8",
        xml_declaration=True
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Scan NemxNovels HTML canonical/og:url values "
            "and rebuild sitemap.xml."
        )
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually replace sitemap.xml."
    )

    args = parser.parse_args()

    print()
    print("=" * 70)
    print("NemxNovels Sitemap Rebuilder")
    print("=" * 70)
    print()

    print(f"Project root : {PROJECT_ROOT}")
    print(f"Sitemap      : {SITEMAP_FILE}")
    print()

    # --------------------------------------------------------
    # 1. Read old sitemap metadata
    # --------------------------------------------------------

    print("[1/5] Reading existing sitemap metadata...")

    old_metadata = load_existing_sitemap()

    print(
        f"       Existing metadata records: "
        f"{len(old_metadata)}"
    )

    # --------------------------------------------------------
    # 2. Scan HTML
    # --------------------------------------------------------

    print()
    print("[2/5] Scanning HTML files...")

    results, missing_canonical, missing_og, errors = scan_html_files()

    print(
        f"       HTML files scanned: {len(get_relative_html_files())}"
    )

    print(
        f"       Sitemap candidates found: {len(results)}"
    )

    # --------------------------------------------------------
    # 3. Build unique URLs
    # --------------------------------------------------------

    print()
    print("[3/5] Building URL list...")

    urls, duplicates = build_url_data(
        results,
        old_metadata
    )

    print(
        f"       Unique sitemap URLs: {len(urls)}"
    )

    print(
        f"       Duplicate URLs removed: {len(duplicates)}"
    )

    # --------------------------------------------------------
    # 4. Validate
    # --------------------------------------------------------

    print()
    print("[4/5] Validating URLs...")

    problems = validate_urls(urls)

    if problems:
        print()
        print("       VALIDATION PROBLEMS:")

        for problem in problems:
            print(f"       - {problem}")

    else:
        print("       No sitemap URL problems found.")

    # --------------------------------------------------------
    # REPORT DUPLICATES
    # --------------------------------------------------------

    if duplicates:

        print()
        print("       DUPLICATE URLS:")

        for url, first_file, duplicate_file in duplicates:

            print(f"       URL: {url}")
            print(f"         first : {first_file}")
            print(f"         second: {duplicate_file}")
            print()

    # --------------------------------------------------------
    # REPORT MISSING CANONICAL
    # --------------------------------------------------------

    if missing_canonical:

        print()
        print(
            f"       HTML FILES WITHOUT CANONICAL: "
            f"{len(missing_canonical)}"
        )

        for path in missing_canonical:
            print(f"       - {path}")

    # --------------------------------------------------------
    # REPORT MISSING OG
    # --------------------------------------------------------

    if missing_og:

        print()
        print(
            f"       HTML FILES WITHOUT og:url: "
            f"{len(missing_og)}"
        )

        for path in missing_og:
            print(f"       - {path}")

    # --------------------------------------------------------
    # REPORT ERRORS
    # --------------------------------------------------------

    if errors:

        print()
        print(
            f"       FILE ERRORS: {len(errors)}"
        )

        for path, error in errors:
            print(f"       - {path}: {error}")

    # --------------------------------------------------------
    # 5. Create sitemap
    # --------------------------------------------------------

    print()
    print("[5/5] Generating new sitemap...")

    tree = create_sitemap(urls)

    if args.apply:

        write_sitemap(tree)

        print()
        print("       sitemap.xml REPLACED.")
        print()
        print(f"       Total URLs: {len(urls)}")

    else:

        print()
        print("       DRY RUN ONLY.")
        print("       sitemap.xml was NOT changed.")
        print()
        print(
            "       Run with --apply to replace sitemap.xml:"
        )
        print()
        print("       python3 rebuild_sitemap.py --apply")

    print()
    print("=" * 70)
    print("Finished")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()