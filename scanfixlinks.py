
import os
import re
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser

# ============================================================
# CONFIGURATION
# ============================================================

# Leave this as "." to scan the folder where the script is run.
# Or change it to a specific folder.
ROOT_FOLDER = "."

OUTPUT_FILE = "nemxnovels_link_audit.txt"


# ============================================================
# HTML LINK PARSER
# ============================================================

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # Normal page/resource links
        if "href" in attrs:
            self.links.append({
                "type": "href",
                "tag": tag,
                "value": attrs["href"],
                "line": self.getpos()[0]
            })

        # Also capture src attributes because they can reveal
        # broken paths in images/scripts/iframes/etc.
        if "src" in attrs:
            self.links.append({
                "type": "src",
                "tag": tag,
                "value": attrs["src"],
                "line": self.getpos()[0]
            })


# ============================================================
# HELPERS
# ============================================================

def is_external_url(link):
    parsed = urlparse(link)
    return parsed.scheme in [
        "http",
        "https",
        "ftp",
        "ftps"
    ]


def is_special_link(link):
    lower = link.lower()

    return (
        lower.startswith("#")
        or lower.startswith("mailto:")
        or lower.startswith("tel:")
        or lower.startswith("javascript:")
        or lower.startswith("data:")
    )


def clean_link(link):
    """
    Remove URL fragments and query strings when checking
    local files.

    Example:
        chapter.html#part2
        becomes:
        chapter.html
    """

    parsed = urlparse(link)

    path = unquote(parsed.path)

    return path


def resolve_local_path(source_file, link, root_folder):
    """
    Resolve a local HTML link against the file containing it.

    Handles:

        chapter.html
        ../chapter.html
        ../../havenfall/index.html
        /havenfall/index.html
    """

    clean_path = clean_link(link)

    if not clean_path:
        return None, None

    # --------------------------------------------------------
    # ROOT-RELATIVE LINKS
    #
    # /havenfall/index.html
    #
    # We interpret "/" as the root folder being scanned.
    # --------------------------------------------------------

    if clean_path.startswith("/"):
        relative_target = clean_path.lstrip("/")

        target = os.path.normpath(
            os.path.join(root_folder, relative_target)
        )

        return target, "ROOT-RELATIVE"

    # --------------------------------------------------------
    # NORMAL RELATIVE LINK
    # --------------------------------------------------------

    source_directory = os.path.dirname(source_file)

    target = os.path.normpath(
        os.path.join(source_directory, clean_path)
    )

    return target, "RELATIVE"


def relative_to_root(path, root_folder):
    try:
        return os.path.relpath(path, root_folder)
    except ValueError:
        return path


def find_index_files(root_folder):
    """
    Find every index.html in the entire project.
    """

    index_files = []

    for current_root, dirs, files in os.walk(root_folder):

        # Ignore common folders that should not be scanned.
        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                ".github",
                "node_modules",
                "__pycache__"
            }
        ]

        for file in files:
            if file.lower() == "index.html":
                full_path = os.path.join(current_root, file)

                index_files.append(
                    os.path.normpath(full_path)
                )

    return sorted(index_files)


def parse_html_file(file_path):
    """
    Read and parse an HTML file.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as f:

            content = f.read()

        parser = LinkParser()
        parser.feed(content)

        return parser.links, None

    except Exception as e:
        return [], str(e)


# ============================================================
# MAIN SCANNER
# ============================================================

def main():

    root_folder = os.path.abspath(ROOT_FOLDER)

    print()
    print("=" * 70)
    print("NEMXNOVELS LINK AUDITOR")
    print("=" * 70)
    print()

    print(f"Scanning:")
    print(root_folder)
    print()

    # --------------------------------------------------------
    # FIND HTML FILES
    # --------------------------------------------------------

    html_files = []

    for current_root, dirs, files in os.walk(root_folder):

        # Skip folders that don't belong to the website.
        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                ".github",
                "node_modules",
                "__pycache__"
            }
        ]

        for file in files:

            if file.lower().endswith((".html", ".htm")):

                full_path = os.path.join(
                    current_root,
                    file
                )

                html_files.append(
                    os.path.normpath(full_path)
                )

    html_files.sort()

    print(f"HTML files found: {len(html_files)}")

    # --------------------------------------------------------
    # FIND INDEX FILES
    # --------------------------------------------------------

    index_files = find_index_files(root_folder)

    print(f"index.html files found: {len(index_files)}")
    print()

    # --------------------------------------------------------
    # SCAN FILES
    # --------------------------------------------------------

    total_links = 0
    broken_links = 0
    root_links = 0
    external_links = 0
    index_links = 0
    special_links = 0

    report = []

    report.append("=" * 80)
    report.append("NEMXNOVELS COMPLETE LINK AUDIT")
    report.append("=" * 80)
    report.append("")

    report.append("PROJECT ROOT")
    report.append("-" * 80)
    report.append(root_folder)
    report.append("")

    report.append("HTML FILES FOUND")
    report.append("-" * 80)
    report.append(f"Total HTML files: {len(html_files)}")
    report.append("")

    report.append("INDEX.HTML FILES")
    report.append("-" * 80)

    if index_files:

        for index_file in index_files:

            relative_index = relative_to_root(
                index_file,
                root_folder
            )

            report.append(
                f"index.html -> {relative_index}"
            )

    else:

        report.append("No index.html files found.")

    report.append("")
    report.append("=" * 80)
    report.append("LINK DETAILS")
    report.append("=" * 80)
    report.append("")

    # --------------------------------------------------------
    # EACH HTML FILE
    # --------------------------------------------------------

    for html_file in html_files:

        relative_source = relative_to_root(
            html_file,
            root_folder
        )

        links, error = parse_html_file(html_file)

        report.append("")
        report.append("#" * 80)
        report.append(f"SOURCE FILE: {relative_source}")
        report.append(f"FULL PATH:   {html_file}")
        report.append(f"LINK COUNT:  {len(links)}")
        report.append("#" * 80)
        report.append("")

        if error:

            report.append(
                f"ERROR READING FILE: {error}"
            )

            continue

        if not links:

            report.append("No href/src links found.")
            continue

        for link_info in links:

            total_links += 1

            link = link_info["value"]
            line = link_info["line"]
            link_type = link_info["type"]
            tag = link_info["tag"]

            report.append("-" * 80)

            report.append(
                f"LINE:       {line}"
            )

            report.append(
                f"TAG:        <{tag}>"
            )

            report.append(
                f"ATTRIBUTE:  {link_type}"
            )

            report.append(
                f"RAW LINK:   {link}"
            )

            # ------------------------------------------------
            # EMPTY LINKS
            # ------------------------------------------------

            if not link:

                report.append(
                    "STATUS:     ⚠ EMPTY LINK"
                )

                report.append(
                    "WARNING:    This link has no destination."
                )

                report.append("")

                continue

            # ------------------------------------------------
            # EXTERNAL LINKS
            # ------------------------------------------------

            if is_external_url(link):

                external_links += 1

                report.append(
                    "STATUS:     EXTERNAL URL"
                )

                report.append(
                    "CHECK:      Requires internet/browser check."
                )

                report.append("")

                continue

            # ------------------------------------------------
            # SPECIAL LINKS
            # ------------------------------------------------

            if is_special_link(link):

                special_links += 1

                if link.startswith("#"):

                    report.append(
                        "STATUS:     INTERNAL PAGE ANCHOR"
                    )

                    report.append(
                        "CHECK:      Anchor should exist on the same page."
                    )

                elif link.lower().startswith("mailto:"):

                    report.append(
                        "STATUS:     MAILTO LINK"
                    )

                elif link.lower().startswith("tel:"):

                    report.append(
                        "STATUS:     TELEPHONE LINK"
                    )

                elif link.lower().startswith("javascript:"):

                    report.append(
                        "STATUS:     JAVASCRIPT LINK"
                    )

                elif link.lower().startswith("data:"):

                    report.append(
                        "STATUS:     DATA URL"
                    )

                report.append("")

                continue

            # ------------------------------------------------
            # LOCAL LINK
            # ------------------------------------------------

            target, path_type = resolve_local_path(
                html_file,
                link,
                root_folder
            )

            if target is None:

                report.append(
                    "STATUS:     ⚠ COULD NOT RESOLVE"
                )

                report.append("")

                continue

            if path_type == "ROOT-RELATIVE":

                root_links += 1

                report.append(
                    "PATH TYPE:  ROOT-RELATIVE"
                )

                report.append(
                    "WARNING:    Starts with '/' — verify website root."
                )

            else:

                report.append(
                    "PATH TYPE:  RELATIVE"
                )

            relative_target = relative_to_root(
                target,
                root_folder
            )

            report.append(
                f"RESOLVES TO: {relative_target}"
            )

            # ------------------------------------------------
            # CHECK TARGET
            # ------------------------------------------------

            if os.path.isfile(target):

                report.append(
                    "STATUS:      ✓ TARGET EXISTS"
                )

                # ------------------------------------------------
                # CHECK IF INDEX.HTML
                # ------------------------------------------------

                if os.path.basename(
                    target
                ).lower() == "index.html":

                    index_links += 1

                    report.append(
                        "INDEX FILE:  ✓ YES"
                    )

                    report.append(
                        f"INDEX PATH:  {relative_target}"
                    )

                else:

                    report.append(
                        "INDEX FILE:  NO"
                    )

            else:

                broken_links += 1

                report.append(
                    "STATUS:      ✗ TARGET DOES NOT EXIST"
                )

                report.append(
                    "ACTION:      CHECK THIS LINK"
                )

                # ------------------------------------------------
                # POSSIBLE INDEX DIRECTORY
                # ------------------------------------------------

                possible_index = os.path.join(
                    target,
                    "index.html"
                )

                if os.path.isfile(possible_index):

                    report.append(
                        "POSSIBLE FIX: Target is a directory containing index.html."
                    )

                    report.append(
                        f"INDEX FOUND: {relative_to_root(possible_index, root_folder)}"
                    )

            report.append("")

    # ========================================================
    # SUMMARY
    # ========================================================

    report.append("")
    report.append("=" * 80)
    report.append("AUDIT SUMMARY")
    report.append("=" * 80)
    report.append("")

    report.append(
        f"HTML files scanned:       {len(html_files)}"
    )

    report.append(
        f"index.html files found:   {len(index_files)}"
    )

    report.append(
        f"Total links/references:   {total_links}"
    )

    report.append(
        f"Existing local targets:   {total_links - broken_links - external_links - special_links}"
    )

    report.append(
        f"Broken local targets:     {broken_links}"
    )

    report.append(
        f"Root-relative links:      {root_links}"
    )

    report.append(
        f"External URLs:            {external_links}"
    )

    report.append(
        f"Special links:            {special_links}"
    )

    report.append(
        f"Links to index.html:      {index_links}"
    )

    report.append("")

    # --------------------------------------------------------
    # INDEX FILE DIRECTORY MAP
    # --------------------------------------------------------

    report.append("=" * 80)
    report.append("INDEX.HTML DIRECTORY MAP")
    report.append("=" * 80)
    report.append("")

    for index_file in index_files:

        relative_index = relative_to_root(
            index_file,
            root_folder
        )

        index_directory = os.path.dirname(
            relative_index
        )

        if index_directory == "":
            index_directory = "/"

        report.append(
            f"INDEX: {relative_index}"
        )

        report.append(
            f"DIRECTORY: {index_directory}"
        )

        report.append("")

    # --------------------------------------------------------
    # WRITE REPORT
    # --------------------------------------------------------

    output_path = os.path.join(
        root_folder,
        OUTPUT_FILE
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(report))

    print("=" * 70)
    print("SCAN COMPLETE")
    print("=" * 70)
    print()
    print(f"Report created:")
    print(output_path)
    print()
    print(f"HTML files:       {len(html_files)}")
    print(f"Total links:      {total_links}")
    print(f"Broken targets:   {broken_links}")
    print(f"Root-relative:    {root_links}")
    print(f"External URLs:    {external_links}")
    print(f"index.html links: {index_links}")
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
