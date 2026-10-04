
import os
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser


# ============================================================
# CONFIGURATION
# ============================================================

ROOT_FOLDER = "."
OUTPUT_FILE = "nemxnovels_link_problems.txt"


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

    return urlparse(link).scheme.lower() in {
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


def clean_path(link):

    return unquote(
        urlparse(link).path
    )


def resolve(source, link, root):

    path = clean_path(link)

    if not path:

        return None, None

    if path.startswith("/"):

        target = os.path.normpath(
            os.path.join(
                root,
                path.lstrip("/")
            )
        )

        return target, "ROOT-RELATIVE"

    target = os.path.normpath(
        os.path.join(
            os.path.dirname(source),
            path
        )
    )

    return target, "RELATIVE"


def relative(path, root):

    return os.path.relpath(
        path,
        root
    )


def find_html_files(root):

    files = []

    for current_root, dirs, filenames in os.walk(root):

        dirs[:] = [
            d for d in dirs
            if d not in {
                ".git",
                ".github",
                "node_modules",
                "__pycache__"
            }
        ]

        for filename in filenames:

            if filename.lower().endswith(
                (".html", ".htm")
            ):

                files.append(
                    os.path.normpath(
                        os.path.join(
                            current_root,
                            filename
                        )
                    )
                )

    return sorted(files)


# ============================================================
# MAIN
# ============================================================

def main():

    root = os.path.abspath(ROOT_FOLDER)

    html_files = find_html_files(root)

    problems = []

    # Counters
    broken = 0
    root_relative = 0
    anchors = 0
    parent_paths = 0
    empty = 0
    directories = 0
    suspicious_index = 0

    # --------------------------------------------------------
    # SCAN
    # --------------------------------------------------------

    for html_file in html_files:

        try:

            with open(
                html_file,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                content = file.read()

        except Exception as error:

            problems.append({
                "category": "READ ERROR",
                "source": html_file,
                "line": "?",
                "link": "",
                "details": str(error)
            })

            continue

        parser = LinkParser()

        try:

            parser.feed(content)

        except Exception as error:

            problems.append({
                "category": "HTML PARSE ERROR",
                "source": html_file,
                "line": "?",
                "link": "",
                "details": str(error)
            })

            continue

        for item in parser.links:

            link = item["value"]

            # ------------------------------------------------
            # EMPTY
            # ------------------------------------------------

            if not link:

                empty += 1

                problems.append({
                    "category": "EMPTY LINK",
                    "source": html_file,
                    "line": item["line"],
                    "link": link,
                    "details":
                        "href/src contains no destination."
                })

                continue

            # ------------------------------------------------
            # EXTERNAL
            # ------------------------------------------------

            if is_external(link):

                continue

            # ------------------------------------------------
            # SPECIAL
            # ------------------------------------------------

            if is_special(link):

                if link.startswith("#"):

                    anchors += 1

                    problems.append({
                        "category": "ANCHOR",
                        "source": html_file,
                        "line": item["line"],
                        "link": link,
                        "details":
                            "Check that the target ID exists on this page."
                    })

                continue

            # ------------------------------------------------
            # RESOLVE
            # ------------------------------------------------

            target, path_type = resolve(
                html_file,
                link,
                root
            )

            if target is None:

                continue

            # ------------------------------------------------
            # ROOT-RELATIVE
            # ------------------------------------------------

            if path_type == "ROOT-RELATIVE":

                root_relative += 1

                problems.append({
                    "category": "ROOT-RELATIVE LINK",
                    "source": html_file,
                    "line": item["line"],
                    "link": link,
                    "details":
                        "Starts with '/'. Verify that the website root matches the project root."
                })

            # ------------------------------------------------
            # PARENT DIRECTORY
            # ------------------------------------------------

            if ".." in link:

                parent_paths += 1

                problems.append({
                    "category": "PARENT-DIRECTORY LINK",
                    "source": html_file,
                    "line": item["line"],
                    "link": link,
                    "details":
                        "Contains '..'. Verify the number of directory levels."
                })

            # ------------------------------------------------
            # MISSING TARGET
            # ------------------------------------------------

            if not os.path.exists(target):

                broken += 1

                problems.append({
                    "category": "BROKEN LOCAL LINK",
                    "source": html_file,
                    "line": item["line"],
                    "link": link,
                    "details":
                        f"Resolves to '{relative(target, root)}' but that target does not exist."
                })

                continue

            # ------------------------------------------------
            # DIRECTORY
            # ------------------------------------------------

            if os.path.isdir(target):

                directories += 1

                index_inside = os.path.join(
                    target,
                    "index.html"
                )

                if os.path.isfile(index_inside):

                    problems.append({
                        "category": "DIRECTORY WITH INDEX",
                        "source": html_file,
                        "line": item["line"],
                        "link": link,
                        "details":
                            f"Link resolves to directory '{relative(target, root)}' which contains index.html."
                    })

                else:

                    problems.append({
                        "category": "DIRECTORY TARGET",
                        "source": html_file,
                        "line": item["line"],
                        "link": link,
                        "details":
                            f"Link resolves to directory '{relative(target, root)}' with no index.html."
                    })

            # ------------------------------------------------
            # SUSPICIOUS INDEX
            # ------------------------------------------------

            if (
                os.path.basename(target).lower()
                == "index.html"
            ):

                source_directory = os.path.dirname(
                    html_file
                )

                target_directory = os.path.dirname(
                    target
                )

                # Same directory index
                if source_directory == target_directory:

                    suspicious_index += 1

                    problems.append({
                        "category": "SAME-DIRECTORY INDEX",
                        "source": html_file,
                        "line": item["line"],
                        "link": link,
                        "details":
                            "Link points to index.html in the same directory. Verify this is intentional."
                    })


    # ========================================================
    # BUILD REPORT
    # ========================================================

    report = []

    report.append("=" * 90)
    report.append("NEMXNOVELS LINK PROBLEMS & SUSPICIOUS LINKS")
    report.append("=" * 90)
    report.append("")

    report.append(
        f"PROJECT ROOT: {root}"
    )

    report.append(
        f"HTML FILES SCANNED: {len(html_files)}"
    )

    report.append("")

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    report.append("=" * 90)
    report.append("SUMMARY")
    report.append("=" * 90)
    report.append("")

    report.append(
        f"Potential issues found: {len(problems)}"
    )

    report.append(
        f"Broken local links:      {broken}"
    )

    report.append(
        f"Root-relative links:     {root_relative}"
    )

    report.append(
        f"Parent-directory links:  {parent_paths}"
    )

    report.append(
        f"Empty links:             {empty}"
    )

    report.append(
        f"Anchor links:            {anchors}"
    )

    report.append(
        f"Directory targets:       {directories}"
    )

    report.append(
        f"Same-directory indexes:  {suspicious_index}"
    )

    report.append("")

    # --------------------------------------------------------
    # PROBLEMS
    # --------------------------------------------------------

    categories = [
        "BROKEN LOCAL LINK",
        "ROOT-RELATIVE LINK",
        "PARENT-DIRECTORY LINK",
        "DIRECTORY WITH INDEX",
        "DIRECTORY TARGET",
        "EMPTY LINK",
        "ANCHOR",
        "SAME-DIRECTORY INDEX",
        "READ ERROR",
        "HTML PARSE ERROR"
    ]

    for category in categories:

        category_items = [
            p for p in problems
            if p["category"] == category
        ]

        if not category_items:

            continue

        report.append("")
        report.append("")
        report.append("=" * 90)
        report.append(category)
        report.append("=" * 90)

        for number, problem in enumerate(
            category_items,
            start=1
        ):

            report.append("")
            report.append(
                f"[{number}]"
            )

            report.append(
                f"SOURCE: {relative(problem['source'], root)}"
            )

            report.append(
                f"LINE:   {problem['line']}"
            )

            report.append(
                f"LINK:   {problem['link']}"
            )

            report.append(
                f"DETAIL: {problem['details']}"
            )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    output = os.path.join(
        root,
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
    print("PROBLEM SCAN COMPLETE")
    print("=" * 60)
    print()
    print(f"HTML files scanned: {len(html_files)}")
    print(f"Potential issues:   {len(problems)}")
    print(f"Broken links:       {broken}")
    print(f"Root-relative:      {root_relative}")
    print(f"Parent paths:       {parent_paths}")
    print(f"Output:             {output}")
    print()


if __name__ == "__main__":
    main()

