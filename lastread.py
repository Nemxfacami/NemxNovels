from pathlib import Path
import re
import shutil

# ============================================================
# SETTINGS
# ============================================================

ROOT_FOLDER = Path(".")

CREATE_BACKUPS = True


# ============================================================
# SCROLL POSITION JAVASCRIPT
# ============================================================

SCROLL_JS = '''

// Per-page scroll position
const scrollPositionKey = "scroll-position-" + window.location.pathname;

window.addEventListener("scroll", function () {
    localStorage.setItem(scrollPositionKey, window.scrollY);
});

window.addEventListener("load", function () {

    const savedPosition = localStorage.getItem(scrollPositionKey);

    if (savedPosition !== null) {
        window.scrollTo(0, parseInt(savedPosition, 10));
    }

});
'''


# ============================================================
# PROCESS HTML FILE
# ============================================================

def process_file(file_path):

    try:
        content = file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        print(f"[SKIP] Encoding problem: {file_path}")
        return

    original = content

    # --------------------------------------------------------
    # IDENTIFY STORY / CHAPTER PAGE
    # --------------------------------------------------------

    if 'onclick="sharePage(); return false;"' not in content:
        print(f"[SKIP] No Share option: {file_path}")
        return

    print(f"[STORY FOUND] {file_path}")

    # --------------------------------------------------------
    # CHECK IF SCROLL CODE ALREADY EXISTS
    # --------------------------------------------------------

    if "scroll-position-" in content:

        print(f"[SCROLL EXISTS] {file_path}")
        return

    # --------------------------------------------------------
    # FIND EXISTING SCRIPT ELEMENT
    # --------------------------------------------------------

    script_positions = list(
        re.finditer(r'</script\s*>', content, re.IGNORECASE)
    )

    if not script_positions:

        print(f"[WARNING] No script element: {file_path}")
        return

    # --------------------------------------------------------
    # USE THE LAST SCRIPT ELEMENT
    # --------------------------------------------------------

    last_script = script_positions[-1]

    content = (
        content[:last_script.start()]
        + SCROLL_JS
        + "\n"
        + content[last_script.start():]
    )

    print(f"[SCROLL ADDED] {file_path}")

    # --------------------------------------------------------
    # CREATE BACKUP
    # --------------------------------------------------------

    if CREATE_BACKUPS:

        backup_path = file_path.with_suffix(
            file_path.suffix + ".bak"
        )

        shutil.copy2(file_path, backup_path)

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"[UPDATED] {file_path}")
    print()


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

html_files = list(ROOT_FOLDER.rglob("*.html"))

print("=" * 60)
print(f"Found {len(html_files)} HTML files")
print("Searching for story/chapter pages with Share...")
print("=" * 60)
print()

for html_file in html_files:
    process_file(html_file)

print("=" * 60)
print("DONE")
print("=" * 60)
