#!/usr/bin/env python3

import os
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://nemxnovels.site"

# The script lives inside the NemxNovels root folder.
PROJECT_ROOT = Path(__file__).resolve().parent

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
}

EXCLUDED_FILES = {
    Path(__file__).name,
}


# ============================================================
# FIND HTML FILES
# ============================================================

def find_html_files():
    """Find every HTML file inside the NemxNovels project."""

    html_files = []

    for current_root, dirs, files in os.walk(PROJECT_ROOT):

        # Don't enter excluded directories.
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in files:

            if filename in EXCLUDED_FILES:
                continue

            if filename.lower().endswith(".html"):
                html_files.append(
                    Path(current_root) / filename
                )

    return sorted(html_files)


# ============================================================
# CONVERT FILE PATH → PUBLIC URL
# ============================================================

def get_public_url(file_path):
    """
    Convert a local HTML file into its public NemxNovels URL.

    Examples:

        index.html
        →
        https://nemxnovels.site/

        ravenport/original-story/index.html
        →
        https://nemxnovels.site/ravenport/original-story/

        ravenport/original-story/Ravenport-chapter2.html
        →
        https://nemxnovels.site/ravenport/original-story/Ravenport-chapter2.html
    """

    relative_path = file_path.relative_to(PROJECT_ROOT)

    parts = list(relative_path.parts)

    filename = parts[-1]

    # --------------------------------------------------------
    # INDEX.HTML
    # --------------------------------------------------------

    if filename.lower() == "index.html":

        directory_parts = parts[:-1]

        # Main homepage
        if not directory_parts:
            return f"{BASE_URL}/"

        directory = "/".join(directory_parts)

        return f"{BASE_URL}/{directory}/"

    # --------------------------------------------------------
    # NORMAL HTML PAGE
    # --------------------------------------------------------

    relative_url = "/".join(parts)

    return f"{BASE_URL}/{relative_url}"


# ============================================================
# FIX / CREATE CANONICAL
# ============================================================

def fix_canonical(html, canonical_url):
    """
    Replace an existing canonical tag.

    If no canonical exists, create one immediately after <head>.
    """

    canonical_pattern = re.compile(
        r'<link\b'
        r'(?=[^>]*\brel\s*=\s*["\']canonical["\'])'
        r'[^>]*>',
        re.IGNORECASE
    )

    match = canonical_pattern.search(html)

    # --------------------------------------------------------
    # EXISTING CANONICAL
    # --------------------------------------------------------

    if match:

        old_tag = match.group(0)

        # Replace only the href value.
        new_tag = re.sub(
            r'(\bhref\s*=\s*["\'])[^"\']*(["\'])',
            rf'\g<1>{canonical_url}\g<2>',
            old_tag,
            count=1,
            flags=re.IGNORECASE
        )

        if new_tag == old_tag:
            return html, False, "canonical already correct"

        new_html = (
            html[:match.start()]
            + new_tag
            + html[match.end():]
        )

        return new_html, True, "canonical corrected"

    # --------------------------------------------------------
    # NO CANONICAL — CREATE ONE
    # --------------------------------------------------------

    head_pattern = re.compile(
        r'<head\b[^>]*>',
        re.IGNORECASE
    )

    head_match = head_pattern.search(html)

    if not head_match:
        return html, False, "ERROR: <head> tag not found"

    canonical_tag = (
        f'\n     <link rel="canonical" href="{canonical_url}">'
    )

    insert_position = head_match.end()

    new_html = (
        html[:insert_position]
        + canonical_tag
        + html[insert_position:]
    )

    return new_html, True, "canonical created"


# ============================================================
# FIX OG:URL
# ============================================================

def fix_og_url(html, canonical_url):
    """
    Fix an existing og:url.

    We do NOT create og:url if the page doesn't already have one.
    """

    og_pattern = re.compile(
        r'<meta\b'
        r'(?=[^>]*\bproperty\s*=\s*["\']og:url["\'])'
        r'[^>]*>',
        re.IGNORECASE
    )

    match = og_pattern.search(html)

    if not match:
        return html, False, "og:url not present"

    old_tag = match.group(0)

    new_tag = re.sub(
        r'(\bcontent\s*=\s*["\'])[^"\']*(["\'])',
        rf'\g<1>{canonical_url}\g<2>',
        old_tag,
        count=1,
        flags=re.IGNORECASE
    )

    if new_tag == old_tag:
        return html, False, "og:url already correct"

    new_html = (
        html[:match.start()]
        + new_tag
        + html[match.end():]
    )

    return new_html, True, "og:url corrected"


# ============================================================
# PROCESS ONE FILE
# ============================================================

def process_file(file_path, apply_changes=False):

    try:
        original = file_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except Exception as error:

        return {
            "file": file_path,
            "changed": False,
            "error": str(error),
        }

    canonical_url = get_public_url(file_path)

    modified = original
    actions = []

    # --------------------------------------------------------
    # CANONICAL
    # --------------------------------------------------------

    modified, changed, action = fix_canonical(
        modified,
        canonical_url
    )

    if changed:
        actions.append(action)

    # --------------------------------------------------------
    # OG:URL
    # --------------------------------------------------------

    modified, changed, action = fix_og_url(
        modified,
        canonical_url
    )

    if changed:
        actions.append(action)

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    changed = modified != original

    if changed and apply_changes:

        try:

            file_path.write_text(
                modified,
                encoding="utf-8"
            )

        except Exception as error:

            return {
                "file": file_path,
                "changed": False,
                "error": str(error),
            }

    return {
        "file": file_path,
        "changed": changed,
        "actions": actions,
        "canonical": canonical_url,
        "error": None,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print(" NemxNovels Canonical URL Fixer")
    print("=" * 70)
    print()

    print("Project root:")
    print(f"  {PROJECT_ROOT}")
    print()

    # --------------------------------------------------------
    # FIND FILES
    # --------------------------------------------------------

    html_files = find_html_files()

    print(f"HTML files found: {len(html_files)}")
    print()

    if not html_files:

        print("No HTML files were found.")
        return

    # --------------------------------------------------------
    # DRY RUN FIRST
    # --------------------------------------------------------

    print("Running in DRY-RUN mode.")
    print("No files will be modified.")
    print()

    results = []

    for file_path in html_files:

        result = process_file(
            file_path,
            apply_changes=False
        )

        results.append(result)

    changed_files = [
        result
        for result in results
        if result["changed"]
    ]

    errors = [
        result
        for result in results
        if result["error"]
    ]

    # --------------------------------------------------------
    # DISPLAY CHANGES
    # --------------------------------------------------------

    print("=" * 70)
    print(" FILES THAT WILL BE CHANGED")
    print("=" * 70)
    print()

    if not changed_files:

        print("Nothing needs to be changed.")
        print()

    else:

        for result in changed_files:

            relative = result["file"].relative_to(PROJECT_ROOT)

            print(f"FILE: {relative}")
            print(f"CANONICAL: {result['canonical']}")

            for action in result["actions"]:
                print(f"  → {action}")

            print()

    # --------------------------------------------------------
    # ERRORS
    # --------------------------------------------------------

    if errors:

        print("=" * 70)
        print(" ERRORS")
        print("=" * 70)
        print()

        for result in errors:

            relative = result["file"].relative_to(PROJECT_ROOT)

            print(f"{relative}")
            print(f"  {result['error']}")
            print()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("=" * 70)
    print(" SUMMARY")
    print("=" * 70)
    print()

    print(f"HTML files scanned:    {len(html_files)}")
    print(f"Files needing changes: {len(changed_files)}")
    print(f"Errors:                {len(errors)}")
    print()

    if changed_files:

        print("If the changes above look correct, run:")

        print()
        print("    python3 fix_canonicals.py --apply")
        print()

        print("That will apply the exact changes shown above.")

    else:

        print("Everything is already normalized.")

    print()


# ============================================================
# APPLY MODE
# ============================================================

if __name__ == "__main__":

    import sys

    if "--apply" in sys.argv:

        print()
        print("=" * 70)
        print(" NemxNovels Canonical URL Fixer — APPLY MODE")
        print("=" * 70)
        print()

        print(f"Project root:")
        print(f"  {PROJECT_ROOT}")
        print()

        html_files = find_html_files()

        changed_count = 0
        error_count = 0

        for file_path in html_files:

            result = process_file(
                file_path,
                apply_changes=True
            )

            if result["error"]:

                error_count += 1

                print(
                    f"[ERROR] "
                    f"{file_path.relative_to(PROJECT_ROOT)}"
                )

                print(
                    f"        {result['error']}"
                )

                continue

            if result["changed"]:

                changed_count += 1

                print(
                    f"[FIXED] "
                    f"{file_path.relative_to(PROJECT_ROOT)}"
                )

                print(
                    f"        → {result['canonical']}"
                )

                for action in result["actions"]:
                    print(f"        • {action}")

        print()
        print("=" * 70)
        print(" COMPLETE")
        print("=" * 70)
        print()

        print(f"HTML files scanned: {len(html_files)}")
        print(f"Files modified:     {changed_count}")
        print(f"Errors:             {error_count}")
        print()

        print("Sitemap was NOT modified.")
        print("That will be handled separately.")
        print()

    else:

        main()