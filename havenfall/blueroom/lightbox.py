from pathlib import Path
import re

# ============================================================
# SETTINGS
# ============================================================

ROOT_FOLDER = Path(".")


# ============================================================
# REMOVE LIGHTBOX CSS
# ============================================================

def remove_lightbox_css(html):
    """
    Removes CSS blocks specifically belonging to #lightbox.
    """

    # #lightbox { ... }
    html = re.sub(
        r'\s*#lightbox\s*\{.*?\}',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # #lightbox.open { ... }
    html = re.sub(
        r'\s*#lightbox\.open\s*\{.*?\}',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # #lightbox .lightbox-inner { ... }
    html = re.sub(
        r'\s*#lightbox\s+\.lightbox-inner\s*\{.*?\}',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    return html


# ============================================================
# REMOVE LIGHTBOX HTML
# ============================================================

def remove_lightbox_html(html):
    """
    Removes:

    <div id="lightbox">
        ...
    </div>

    including everything inside it.
    """

    html = re.sub(
        r'\s*<div\s+id=["\']lightbox["\'][^>]*>.*?</div>\s*',
        '\n',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    return html


# ============================================================
# REMOVE LIGHTBOX JAVASCRIPT
# ============================================================

def remove_lightbox_js(html):
    """
    Removes JavaScript responsible for opening and closing
    the lightbox.
    """

    # --------------------------------------------------------
    # Remove the click event that opens the lightbox
    # --------------------------------------------------------

    html = re.sub(
        r'\s*imgMsg\.addEventListener\(\s*[\'"]click[\'"]\s*,\s*\(\)\s*=>\s*\{\s*'
        r'document\.getElementById\(\s*[\'"]lightbox[\'"]\s*\)\.classList\.add\(\s*[\'"]open[\'"]\s*\)\s*;?\s*'
        r'\}\s*\)\s*;?',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --------------------------------------------------------
    # Remove lightbox close event
    # --------------------------------------------------------

    html = re.sub(
        r'\s*document\.getElementById\(\s*[\'"]lightbox[\'"]\s*\)'
        r'\.addEventListener\(\s*[\'"]click[\'"]\s*,\s*function\s*\(\)\s*\{'
        r'.*?'
        r'\}\s*\)\s*;?',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --------------------------------------------------------
    # Remove any standalone references to lightbox that may
    # have survived.
    # --------------------------------------------------------

    html = re.sub(
        r'\s*document\.getElementById\(\s*[\'"]lightbox[\'"]\s*\)'
        r'(?:\.[a-zA-Z]+(?:\([^;]*\))?)*\s*;?',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    return html


# ============================================================
# REMOVE LIGHTBOX COMMENTS
# ============================================================

def remove_lightbox_comments(html):

    html = re.sub(
        r'\s*/\*\s*-*\s*Lightbox.*?\*/',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    html = re.sub(
        r'\s*/\*\s*-*\s*Lightbox close.*?\*/',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    return html


# ============================================================
# PROCESS FILE
# ============================================================

def process_file(file_path):

    try:
        html = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"[ERROR] Could not read: {file_path}")
        return

    original = html

    # --------------------------------------------------------
    # Only bother with files that actually contain lightbox
    # references.
    # --------------------------------------------------------

    if not re.search(
        r'lightbox',
        html,
        re.IGNORECASE
    ):
        print(f"[SKIP - NO LIGHTBOX] {file_path}")
        return

    # --------------------------------------------------------
    # Remove all lightbox components
    # --------------------------------------------------------

    html = remove_lightbox_css(html)
    html = remove_lightbox_html(html)
    html = remove_lightbox_js(html)
    html = remove_lightbox_comments(html)

    # --------------------------------------------------------
    # Safety check:
    # Warn if the word "lightbox" still exists.
    # --------------------------------------------------------

    if re.search(
        r'lightbox',
        html,
        re.IGNORECASE
    ):
        print(
            f"[WARNING - LIGHTBOX REFERENCE REMAINS] "
            f"{file_path}"
        )

    # --------------------------------------------------------
    # Save only if something changed
    # --------------------------------------------------------

    if html == original:
        print(f"[NO CHANGE] {file_path}")
        return

    file_path.write_text(
        html,
        encoding="utf-8"
    )

    print(f"[CLEANED] {file_path}")


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
        process_file(file_path)

    print("\nLightbox cleanup complete.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()