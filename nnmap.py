
import os
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser


# ============================================================
# CONFIGURATION
# ============================================================

ROOT_FOLDER = "."
OUTPUT_FILE = "nemxnovels_link_map2.txt"


# ============================================================
# HTML PARSER
# ============================================================

class LinkParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):

        for name, value in attrs:

            if name.lower() in ("href", "src"):

                self.links.append({
                    "tag": tag,
                    "attribute": name.lower(),
                    "value": value if value is not None else "",
                    "line": self.getpos()[0]
                })


# ============================================================
# HELPERS
# ============================================================

def is_external(link):

    scheme = urlparse(link).scheme.lower()

    return scheme in {
        "http",
        "https",
        "ftp",
        "ftps"
    }


def is_special(link):

    lower = link.lower()

    return (
        lower.startswith("#")
        or lower.startswith("mailto:")
        or lower.startswith("tel:")
        or lower.startswith("javascript:")
        or lower.startswith("data:")
    )


def clean_local_path(link):

    parsed = urlparse(link)

    return unquote(parsed.path)


def resolve_path(source_file, link, root_folder):

    path = clean_local_path(link)

    if not path:

        return None, None

    # --------------------------------------------------------
    # ROOT-RELATIVE
    # Example:
    #
    # /havenfall/index.html
    # --------------------------------------------------------

    if path.startswith("/"):

        target = os.path.normpath(
            os.path.join(
                root_folder,
                path.lstrip("/")
            )
        )

        return target, "ROOT-RELATIVE"

    # --------------------------------------------------------
    # NORMAL RELATIVE
    # --------------------------------------------------------

    target = os.path.normpath(
        os.path.join(
            os.path.dirname(source_file),
            path
        )
    )

    return target, "RELATIVE"


def relative_path(path, root_folder):

    return os.path.relpath(
        path,
        root_folder
    )


def find_html_files(root_folder):

    results = []

    for current_root, dirs, files in os.walk(root_folder):

        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                ".github",
                "node_modules",
                "__pycache__"
            }
        ]

        for filename in files:

            if filename.lower().endswith(
                (".html", ".htm")
            ):

                results.append(
                    os.path.normpath(
                        os.path.join(
                            current_root,
                            filename
                        )
                    )
                )

    return sorted(results)


def find_index_files(root_folder):

    results = []

    for current_root, dirs, files in os.walk(root_folder):

        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                ".github",
                "node_modules",
                "__pycache__"
            }
        ]

        for filename in files:

            if filename.lower() == "index.html":

                results.append(
                    os.path.normpath(
                        os.path.join(
                            current_root,
                            filename
                        )
                    )
                )

    return sorted(results)


# ============================================================
# MAIN
# ============================================================

def main():

    root_folder = os.path.abspath(ROOT_FOLDER)

    html_files = find_html_files(root_folder)

    index_files = find_index_files(root_folder)

    report = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    report.append("=" * 90)
    report.append("NEMXNOVELS COMPLETE LINK MAP")
    report.append("=" * 90)
    report.append("")

    report.append(f"PROJECT ROOT:")
    report.append(root_folder)
    report.append("")

    report.append(
        f"HTML FILES: {len(html_files)}"
    )

    report.append(
        f"INDEX.HTML FILES: {len(index_files)}"
    )

    report.append("")
    report.append("=" * 90)
    report.append("INDEX.HTML MAP")
    report.append("=" * 90)
    report.append("")

    # --------------------------------------------------------
    # INDEX MAP
    # --------------------------------------------------------

    for index_file in index_files:

        report.append(
            relative_path(
                index_file,
                root_folder
            )
        )

    report.append("")

    report.append("=" * 90)
    report.append("HTML FILE LINK MAP")
    report.append("=" * 90)

    total_links = 0

    # --------------------------------------------------------
    # EVERY HTML FILE
    # --------------------------------------------------------

    for html_file in html_files:

        relative_source = relative_path(
            html_file,
            root_folder
        )

        report.append("")
        report.append("")
        report.append("#" * 90)

        report.append(
            f"SOURCE FILE: {relative_source}"
        )

        report.append(
            f"FULL PATH:   {html_file}"
        )

        report.append("#" * 90)

        try:

            with open(
                html_file,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                content = file.read()

        except Exception as error:

            report.append(
                f"READ ERROR: {error}"
            )

            continue

        parser = LinkParser()

        try:

            parser.feed(content)

        except Exception as error:

            report.append(
                f"HTML PARSE ERROR: {error}"
            )

            continue

        if not parser.links:

            report.append(
                "NO LINKS FOUND"
            )

            continue

        for link in parser.links:

            total_links += 1

            raw_link = link["value"]

            report.append("")
            report.append("-" * 90)

            report.append(
                f"LINE:       {link['line']}"
            )

            report.append(
                f"TAG:        <{link['tag']}>"
            )

            report.append(
                f"ATTRIBUTE:  {link['attribute']}"
            )

            report.append(
                f"LINK:       {raw_link}"
            )

            # ------------------------------------------------
            # EXTERNAL
            # ------------------------------------------------

            if is_external(raw_link):

                report.append(
                    "TYPE:       EXTERNAL URL"
                )

                report.append(
                    "TARGET:     Not checked locally"
                )

                continue

            # ------------------------------------------------
            # SPECIAL
            # ------------------------------------------------

            if is_special(raw_link):

                if raw_link.startswith("#"):

                    report.append(
                        "TYPE:       PAGE ANCHOR"
                    )

                elif raw_link.lower().startswith(
                    "mailto:"
                ):

                    report.append(
                        "TYPE:       MAILTO"
                    )

                elif raw_link.lower().startswith(
                    "tel:"
                ):

                    report.append(
                        "TYPE:       TELEPHONE"
                    )

                elif raw_link.lower().startswith(
                    "javascript:"
                ):

                    report.append(
                        "TYPE:       JAVASCRIPT"
                    )

                elif raw_link.lower().startswith(
                    "data:"
                ):

                    report.append(
                        "TYPE:       DATA URL"
                    )

                continue

            # ------------------------------------------------
            # LOCAL PATH
            # ------------------------------------------------

            target, path_type = resolve_path(
                html_file,
                raw_link,
                root_folder
            )

            if target is None:

                report.append(
                    "TYPE:       EMPTY / UNRESOLVED"
                )

                continue

            report.append(
                f"TYPE:       {path_type}"
            )

            report.append(
                f"RESOLVED:   {relative_path(target, root_folder)}"
            )

            if os.path.isfile(target):

                report.append(
                    "STATUS:     EXISTS"
                )

                if os.path.basename(
                    target
                ).lower() == "index.html":

                    report.append(
                        "INDEX:      YES"
                    )

                else:

                    report.append(
                        "INDEX:      NO"
                    )

            else:

                report.append(
                    "STATUS:     DOES NOT EXIST"
                )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    report.append("")
    report.append("")
    report.append("=" * 90)
    report.append("SUMMARY")
    report.append("=" * 90)
    report.append("")

    report.append(
        f"HTML files scanned: {len(html_files)}"
    )

    report.append(
        f"index.html files:   {len(index_files)}"
    )

    report.append(
        f"Total links found:  {total_links}"
    )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    output = os.path.join(
        root_folder,
        OUTPUT_FILE
    )

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report)
        )

    print()
    print("=" * 60)
    print("LINK MAP COMPLETE")
    print("=" * 60)
    print(f"HTML files: {len(html_files)}")
    print(f"index.html: {len(index_files)}")
    print(f"Output:     {output}")
    print()


if __name__ == "__main__":
    main()

