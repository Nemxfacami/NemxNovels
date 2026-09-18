from pathlib import Path
import re
import html


ROOT_FOLDER = Path(".")


# ============================================================
# FIND CONTACT NAME
# ============================================================

def find_contact_name(content):
    """
    Looks for:

    <div class="msgr-header-name">Name</div>

    OR:

    <a class="header-name" href="#">Name</a>

    msgr-header-name is given priority if both exist.
    """

    # --------------------------------------------------------
    # 1. msgr-header-name
    # --------------------------------------------------------

    match = re.search(
        r'<[^>]*class=["\'][^"\']*\bmsgr-header-name\b[^"\']*["\'][^>]*>'
        r'\s*(.*?)\s*'
        r'</[^>]+>',
        content,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        name = re.sub(r'<[^>]+>', '', match.group(1))
        name = html.unescape(name).strip()

        if name:
            return name


    # --------------------------------------------------------
    # 2. header-name
    # --------------------------------------------------------

    match = re.search(
        r'<[^>]*class=["\'][^"\']*\bheader-name\b[^"\']*["\'][^>]*>'
        r'\s*(.*?)\s*'
        r'</[^>]+>',
        content,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        name = re.sub(r'<[^>]+>', '', match.group(1))
        name = html.unescape(name).strip()

        if name:
            return name


    # Nothing found
    return None


# ============================================================
# UPDATE TITLE
# ============================================================

def update_title(file_path):

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"[ERROR] Could not read: {file_path}")
        return


    # --------------------------------------------------------
    # Find the contact name
    # --------------------------------------------------------

    name = find_contact_name(content)

    if not name:
        print(f"[SKIP - NO HEADER NAME] {file_path}")
        return


    # --------------------------------------------------------
    # Find existing <title>
    # --------------------------------------------------------

    title_pattern = re.compile(
        r'<title\b[^>]*>.*?</title>',
        re.IGNORECASE | re.DOTALL
    )


    new_title = f"<title>Messenger Chat - {name}</title>"


    # --------------------------------------------------------
    # Replace existing title
    # --------------------------------------------------------

    if title_pattern.search(content):

        updated_content = title_pattern.sub(
            new_title,
            content,
            count=1
        )

    else:

        # If there is no title, add one after <head>
        head_match = re.search(
            r'<head\b[^>]*>',
            content,
            re.IGNORECASE
        )

        if not head_match:
            print(f"[SKIP - NO HEAD] {file_path}")
            return

        position = head_match.end()

        updated_content = (
            content[:position]
            + "\n    "
            + new_title
            + content[position:]
        )


    # --------------------------------------------------------
    # Save only if something actually changed
    # --------------------------------------------------------

    if updated_content == content:
        print(f"[NO CHANGE] {file_path}")
        return


    file_path.write_text(
        updated_content,
        encoding="utf-8"
    )


    print(
        f"[UPDATED] {file_path}\n"
        f"          Name  : {name}\n"
        f"          Title : Messenger Chat - {name}\n"
    )


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

def main():

    html_files = list(
        ROOT_FOLDER.rglob("*.html")
    )

    print(
        f"\nFound {len(html_files)} HTML files.\n"
    )

    for file_path in html_files:
        update_title(file_path)

    print("\nScan complete.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()