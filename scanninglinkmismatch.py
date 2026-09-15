#!/usr/bin/env python3

from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = PROJECT_ROOT / "canonical-vs-filepath.txt"
OUTPUT_FILE = PROJECT_ROOT / "canonical-link-problems.txt"


def extract_entries(text):
    """
    Extract each URL block from canonical-vs-filepath.txt.
    """

    blocks = re.split(
        r"-{20,}\n",
        text
    )

    entries = []

    for block in blocks:

        if "URL:" not in block:
            continue

        def get_value(label):
            pattern = rf"^{re.escape(label)}\s+(.*)$"

            match = re.search(
                pattern,
                block,
                re.MULTILINE
            )

            if match:
                return match.group(1).strip()

            return None

        url = get_value("URL:")
        filepath = get_value("FILEPATH:")
        actual = get_value("ACTUAL CANONICAL:")
        og_url = get_value("og:url:")

        if url:
            entries.append({
                "url": url,
                "filepath": filepath,
                "canonical": actual,
                "og_url": og_url,
            })

    return entries


def compare_entry(entry):
    """
    Compare the four important values.

    We treat the URL field as the expected public URL.
    """

    problems = []

    url = entry["url"]
    filepath = entry["filepath"]
    canonical = entry["canonical"]
    og_url = entry["og_url"]

    # ---------------------------------------------------------
    # URL vs canonical
    # ---------------------------------------------------------

    if canonical != url:
        problems.append(
            f"URL vs CANONICAL mismatch"
        )

    # ---------------------------------------------------------
    # URL vs og:url
    # ---------------------------------------------------------

    if og_url != url:

        if og_url == "[MISSING]":
            problems.append(
                "URL vs og:url mismatch — og:url is missing"
            )
        else:
            problems.append(
                "URL vs og:url mismatch"
            )

    # ---------------------------------------------------------
    # CANONICAL vs og:url
    # ---------------------------------------------------------

    if canonical != og_url:

        if canonical == "[MISSING]":
            problems.append(
                "CANONICAL vs og:url mismatch — canonical is missing"
            )

        elif og_url == "[MISSING]":
            problems.append(
                "CANONICAL vs og:url mismatch — og:url is missing"
            )

        else:
            problems.append(
                "CANONICAL vs og:url mismatch"
            )

    # ---------------------------------------------------------
    # Missing filepath
    # ---------------------------------------------------------

    if not filepath:
        problems.append(
            "FILEPATH is missing"
        )

    return problems


def build_report(entries):

    problems_found = []

    for entry in entries:

        problems = compare_entry(entry)

        if problems:
            problems_found.append({
                "entry": entry,
                "problems": problems,
            })

    return problems_found


def write_problem_file(problems):

    lines = []

    lines.append("=" * 100)
    lines.append("NEMXNOVELS — CANONICAL LINK PROBLEMS")
    lines.append("=" * 100)
    lines.append("")

    lines.append(
        f"Problematic entries: {len(problems)}"
    )

    lines.append("")

    lines.append(
        "Only entries where the important URLs do not match are shown."
    )

    lines.append("")

    for item in problems:

        entry = item["entry"]

        lines.append("-" * 100)

        lines.append(
            f"URL:              {entry['url']}"
        )

        lines.append(
            f"FILEPATH:          {entry['filepath'] or '[MISSING]'}"
        )

        lines.append(
            f"ACTUAL CANONICAL:  {entry['canonical'] or '[MISSING]'}"
        )

        lines.append(
            f"og:url:            {entry['og_url'] or '[MISSING]'}"
        )

        lines.append("")

        lines.append("PROBLEMS:")

        for problem in item["problems"]:
            lines.append(
                f"  - {problem}"
            )

        lines.append("")

    lines.append("=" * 100)

    OUTPUT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


def main():

    print("=" * 70)
    print("NemxNovels Canonical Problem Scanner")
    print("=" * 70)

    if not INPUT_FILE.exists():

        print()
        print(
            f"ERROR: {INPUT_FILE.name} was not found."
        )

        print(
            "Run the canonical-vs-filepath audit first."
        )

        return

    text = INPUT_FILE.read_text(
        encoding="utf-8",
        errors="replace"
    )

    entries = extract_entries(text)

    print()
    print(
        f"Entries scanned: {len(entries)}"
    )

    problems = build_report(entries)

    print(
        f"Problems found: {len(problems)}"
    )

    # ---------------------------------------------------------
    # CLEAN RESULT
    # ---------------------------------------------------------

    if not problems:

        # If an old problem file exists, remove it.
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()

        print()
        print("=" * 70)
        print("EVERYTHING MATCHES.")
        print("=" * 70)
        print()
        print(
            "No canonical/link problems were found."
        )
        print(
            "canonical-vs-filepath.txt is clean."
        )
        print()
        print(
            "No canonical-link-problems.txt was created."
        )
        print()

        return

    # ---------------------------------------------------------
    # PROBLEMS FOUND
    # ---------------------------------------------------------

    write_problem_file(problems)

    print()
    print("=" * 70)
    print("PROBLEMS FOUND")
    print("=" * 70)

    print()
    print(
        f"Problem entries: {len(problems)}"
    )

    print(
        f"Report created: {OUTPUT_FILE.name}"
    )

    print()
    print(
        "Only the problematic URLs were written to the report."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()