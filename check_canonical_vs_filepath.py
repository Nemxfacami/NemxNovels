#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from collections import defaultdict

SITE_URL = "https://nemxnovels.site"
PROJECT_ROOT = Path(__file__).resolve().parent

OUTPUT_FILE = PROJECT_ROOT / "canonical-vs-filepath.txt"
SITEMAP_FILE = PROJECT_ROOT / "sitemap.xml"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
}


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag not in ("link", "meta"):
            return

        attrs_dict = {
            key.lower(): value
            for key, value in attrs
            if key and value is not None
        }

        if tag == "link":
            rel = attrs_dict.get("rel", "").lower()

            if "canonical" in rel:
                href = attrs_dict.get("href")

                if href:
                    self.canonical = href.strip()

        elif tag == "meta":
            prop = attrs_dict.get("property", "").lower()

            if prop == "og:url":
                content = attrs_dict.get("content")

                if content:
                    self.og_url = content.strip()


def should_skip(path: Path):
    return any(part in EXCLUDED_DIRS for part in path.parts)


def get_html_files():
    files = []

    for path in PROJECT_ROOT.rglob("*.html"):
        if should_skip(path):
            continue

        files.append(path)

    return sorted(files)


def normalize_url(url):
    if not url:
        return None

    url = url.strip()

    if not url:
        return None

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return None

    if parsed.netloc.lower() != "nemxnovels.site":
        return None

    # Remove query strings and fragments.
    url = url.split("#", 1)[0]
    url = url.split("?", 1)[0]

    # Normalize root.
    if url == SITE_URL:
        return SITE_URL + "/"

    return url


def normalize_index_url(url):
    if not url:
        return url

    if url.endswith("/index.html"):
        return url[:-10] + "/"

    if url.endswith("/index.htm"):
        return url[:-9] + "/"

    if url == SITE_URL + "/index.html":
        return SITE_URL + "/"

    return url


def expected_canonical(path):
    """
    Calculate what the canonical SHOULD be
    based entirely on the HTML filepath.
    """

    relative = path.relative_to(PROJECT_ROOT)
    parts = list(relative.parts)

    filename = parts[-1]

    # Root index.html
    if filename.lower() == "index.html":
        if len(parts) == 1:
            return SITE_URL + "/"

        directory = "/".join(parts[:-1])

        return f"{SITE_URL}/{directory}/"

    # Normal HTML page
    relative_url = "/".join(parts)

    return f"{SITE_URL}/{relative_url}"


def parse_html(path):
    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace"
        )
    except Exception as e:
        return None, None, f"Could not read file: {e}"

    parser = MetaParser()

    try:
        parser.feed(text)
    except Exception as e:
        return None, None, f"Could not parse HTML: {e}"

    canonical = normalize_url(parser.canonical)
    canonical = normalize_index_url(canonical)

    og_url = normalize_url(parser.og_url)
    og_url = normalize_index_url(og_url)

    return canonical, og_url, None


def load_sitemap():
    """
    Load sitemap URLs and normalize them exactly the same
    way as the HTML canonical URLs.
    """

    urls = set()

    if not SITEMAP_FILE.exists():
        return urls, "sitemap.xml does not exist."

    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
    except Exception as e:
        return urls, f"Could not parse sitemap.xml: {e}"

    namespace = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
    }

    for url_node in root.findall("sm:url", namespace):
        loc_node = url_node.find("sm:loc", namespace)

        if loc_node is None or not loc_node.text:
            continue

        url = normalize_url(loc_node.text)
        url = normalize_index_url(url)

        if url:
            urls.add(url)

    return urls, None


def write_line(lines, text=""):
    lines.append(text)


def main():

    html_files = get_html_files()

    sitemap_urls, sitemap_error = load_sitemap()

    results = []
    canonical_to_files = defaultdict(list)

    missing_canonical = []
    wrong_canonical = []
    wrong_og = []
    sitemap_missing = []
    sitemap_extra = []
    file_errors = []

    # ---------------------------------------------------------
    # SCAN HTML
    # ---------------------------------------------------------

    for path in html_files:

        relative = path.relative_to(PROJECT_ROOT)

        expected = expected_canonical(path)

        actual, og_url, error = parse_html(path)

        if error:
            file_errors.append((relative, error))

            results.append({
                "url": expected,
                "file": str(relative),
                "expected": expected,
                "actual": None,
                "og_url": None,
                "status": "ERROR",
                "sitemap": "UNKNOWN",
            })

            continue

        # Track canonical duplicates.
        if actual:
            canonical_to_files[actual].append(relative)

        # Canonical status.
        if not actual:
            status = "MISSING CANONICAL"
            missing_canonical.append(relative)

        elif actual != expected:
            status = "WRONG CANONICAL"
            wrong_canonical.append(
                (relative, expected, actual)
            )

        else:
            status = "OK"

        # og:url status.
        if actual and og_url != actual:
            og_status = "MISMATCH"

            wrong_og.append(
                (relative, actual, og_url)
            )

        elif actual and og_url == actual:
            og_status = "OK"

        elif not og_url:
            og_status = "MISSING"

        else:
            og_status = "NO CANONICAL"

        # Sitemap status.
        sitemap_status = (
            "IN SITEMAP"
            if expected in sitemap_urls
            else "NOT IN SITEMAP"
        )

        if expected not in sitemap_urls:
            sitemap_missing.append(expected)

        results.append({
            "url": expected,
            "file": str(relative),
            "expected": expected,
            "actual": actual,
            "og_url": og_url,
            "status": status,
            "og_status": og_status,
            "sitemap": sitemap_status,
        })

    # ---------------------------------------------------------
    # FIND SITEMAP URLS THAT DON'T MATCH ANY EXPECTED FILE URL
    # ---------------------------------------------------------

    expected_urls = {
        item["expected"]
        for item in results
    }

    sitemap_extra = sorted(
        sitemap_urls - expected_urls
    )

    # ---------------------------------------------------------
    # SORT EVERYTHING ALPHABETICALLY BY URL
    # ---------------------------------------------------------

    results.sort(
        key=lambda item: item["url"].lower()
    )

    # ---------------------------------------------------------
    # BUILD REPORT
    # ---------------------------------------------------------

    lines = []

    write_line(lines, "=" * 100)
    write_line(lines, "NEMXNOVELS — CANONICAL VS FILEPATH AUDIT")
    write_line(lines, "=" * 100)
    write_line(lines)

    write_line(
        lines,
        f"Project root: {PROJECT_ROOT}"
    )

    write_line(
        lines,
        f"HTML files scanned: {len(html_files)}"
    )

    write_line(
        lines,
        f"Sitemap URLs found: {len(sitemap_urls)}"
    )

    write_line(lines)

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    write_line(lines, "-" * 100)
    write_line(lines, "SUMMARY")
    write_line(lines, "-" * 100)

    write_line(
        lines,
        f"Correct canonicals       : {len(html_files) - len(missing_canonical) - len(wrong_canonical) - len(file_errors)}"
    )

    write_line(
        lines,
        f"Missing canonicals       : {len(missing_canonical)}"
    )

    write_line(
        lines,
        f"Wrong canonicals         : {len(wrong_canonical)}"
    )

    write_line(
        lines,
        f"og:url mismatches        : {len(wrong_og)}"
    )

    write_line(
        lines,
        f"Expected URLs missing from sitemap : {len(sitemap_missing)}"
    )

    write_line(
        lines,
        f"Sitemap URLs without matching HTML filepath : {len(sitemap_extra)}"
    )

    write_line(
        lines,
        f"Duplicate canonical URLs : {sum(1 for files in canonical_to_files.values() if len(files) > 1)}"
    )

    write_line(
        lines,
        f"File errors              : {len(file_errors)}"
    )

    if sitemap_error:
        write_line(lines)
        write_line(
            lines,
            f"SITEMAP ERROR: {sitemap_error}"
        )

    write_line(lines)

    # ---------------------------------------------------------
    # MAIN TABLE
    # ---------------------------------------------------------

    write_line(lines, "=" * 100)
    write_line(lines, "FULL FILEPATH / CANONICAL / SITEMAP COMPARISON")
    write_line(lines, "=" * 100)
    write_line(lines)

    for item in results:

        write_line(lines, "-" * 100)

        write_line(
            lines,
            f"URL:              {item['url']}"
        )

        write_line(
            lines,
            f"FILEPATH:          {item['file']}"
        )

        write_line(
            lines,
            f"EXPECTED:          {item['expected']}"
        )

        write_line(
            lines,
            f"ACTUAL CANONICAL:  {item['actual'] or '[MISSING]'}"
        )

        write_line(
            lines,
            f"og:url:            {item['og_url'] or '[MISSING]'}"
        )

        write_line(
            lines,
            f"CANONICAL STATUS:  {item['status']}"
        )

        write_line(
            lines,
            f"og:url STATUS:     {item.get('og_status', 'UNKNOWN')}"
        )

        write_line(
            lines,
            f"SITEMAP STATUS:    {item['sitemap']}"
        )

    # ---------------------------------------------------------
    # WRONG / MISSING CANONICALS
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — MISSING CANONICALS")
    write_line(lines, "=" * 100)

    if not missing_canonical:
        write_line(lines, "NONE")
    else:
        for path in sorted(missing_canonical):
            write_line(lines, str(path))

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — WRONG CANONICALS")
    write_line(lines, "=" * 100)

    if not wrong_canonical:
        write_line(lines, "NONE")
    else:
        for path, expected, actual in sorted(
            wrong_canonical,
            key=lambda x: x[1].lower()
        ):
            write_line(lines)
            write_line(lines, f"FILE:     {path}")
            write_line(lines, f"EXPECTED: {expected}")
            write_line(lines, f"ACTUAL:   {actual}")

    # ---------------------------------------------------------
    # OG URL PROBLEMS
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — og:url MISMATCHES")
    write_line(lines, "=" * 100)

    if not wrong_og:
        write_line(lines, "NONE")
    else:
        for path, canonical, og_url in sorted(
            wrong_og,
            key=lambda x: x[1].lower()
        ):
            write_line(lines)
            write_line(lines, f"FILE:       {path}")
            write_line(lines, f"CANONICAL:  {canonical}")
            write_line(
                lines,
                f"og:url:     {og_url or '[MISSING]'}"
            )

    # ---------------------------------------------------------
    # SITEMAP MISSING
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — EXPECTED CANONICAL NOT IN SITEMAP")
    write_line(lines, "=" * 100)

    if not sitemap_missing:
        write_line(lines, "NONE")
    else:
        for url in sorted(sitemap_missing, key=str.lower):
            write_line(lines, url)

    # ---------------------------------------------------------
    # SITEMAP EXTRA
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — SITEMAP URL WITHOUT MATCHING HTML FILEPATH")
    write_line(lines, "=" * 100)

    if not sitemap_extra:
        write_line(lines, "NONE")
    else:
        for url in sitemap_extra:
            write_line(lines, url)

    # ---------------------------------------------------------
    # DUPLICATE CANONICALS
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "PROBLEMS — DUPLICATE CANONICAL URLS")
    write_line(lines, "=" * 100)

    duplicates = {
        url: files
        for url, files in canonical_to_files.items()
        if len(files) > 1
    }

    if not duplicates:
        write_line(lines, "NONE")
    else:
        for url in sorted(duplicates, key=str.lower):

            write_line(lines)
            write_line(lines, f"CANONICAL: {url}")

            for file in sorted(
                duplicates[url],
                key=lambda x: str(x).lower()
            ):
                write_line(lines, f"  - {file}")

    # ---------------------------------------------------------
    # FILE ERRORS
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "FILE ERRORS")
    write_line(lines, "=" * 100)

    if not file_errors:
        write_line(lines, "NONE")
    else:
        for path, error in file_errors:
            write_line(lines)
            write_line(lines, f"FILE: {path}")
            write_line(lines, f"ERROR: {error}")

    # ---------------------------------------------------------
    # FINAL VERDICT
    # ---------------------------------------------------------

    write_line(lines)
    write_line(lines)
    write_line(lines, "=" * 100)
    write_line(lines, "FINAL AUDIT VERDICT")
    write_line(lines, "=" * 100)

    if (
        not missing_canonical
        and not wrong_canonical
        and not sitemap_missing
        and not sitemap_extra
        and not duplicates
        and not file_errors
    ):
        write_line(lines)
        write_line(
            lines,
            "PASS — filepath, canonical URLs, and sitemap URLs are aligned."
        )
    else:
        write_line(lines)
        write_line(
            lines,
            "ATTENTION — differences were found. Review the sections above."
        )

    write_line(lines)
    write_line(lines, "=" * 100)

    # ---------------------------------------------------------
    # WRITE FILE
    # ---------------------------------------------------------

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("=" * 70)
    print("NemxNovels Canonical vs Filepath Audit")
    print("=" * 70)
    print(f"HTML files scanned : {len(html_files)}")
    print(f"Sitemap URLs       : {len(sitemap_urls)}")
    print(f"Output             : {OUTPUT_FILE}")
    print()
    print(f"Missing canonicals : {len(missing_canonical)}")
    print(f"Wrong canonicals   : {len(wrong_canonical)}")
    print(f"og:url mismatches  : {len(wrong_og)}")
    print(f"Sitemap missing    : {len(sitemap_missing)}")
    print(f"Sitemap extras     : {len(sitemap_extra)}")
    print(f"Duplicate canonicals: {len(duplicates)}")
    print(f"File errors        : {len(file_errors)}")
    print()
    print("Audit complete.")
    print(f"Open: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()