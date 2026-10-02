from pathlib import Path
import re
import shutil
from datetime import datetime

# ============================================================
# DEAR DIARY METADATA FIXER
# ============================================================

BASE_URL = "https://nemxnovels.site/havenfall/deardiary/"

# The folder containing this script
FOLDER = Path(__file__).parent

# Backup folder
BACKUP_FOLDER = FOLDER / (
    "metadata-backup-" + datetime.now().strftime("%Y%m%d-%H%M%S")
)

def get_page_url(filename):
    """
    Builds the correct canonical/OG URL.

    index.html:
        https://nemxnovels.site/havenfall/deardiary/

    Other HTML files:
        https://nemxnovels.site/havenfall/deardiary/file.html
    """

    if filename.lower() == "index.html":
        return BASE_URL

    return BASE_URL + filename


def replace_meta(html, pattern, replacement, name):
    """
    Replace an existing metadata tag.
    Returns modified HTML and whether it was changed.
    """

    new_html, count = re.subn(
        pattern,
        replacement,
        html,
        flags=re.IGNORECASE
    )

    if count == 0:
        print(f"  [WARNING] Could not find {name}")
        return html, False

    return new_html, new_html != html


def fix_file(file):
    print(f"\nProcessing: {file.name}")

    # --------------------------------------------------------
    # Read
    # --------------------------------------------------------

    try:
        html = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("  [SKIPPED] Could not read as UTF-8")
        return

    original_html = html

    # --------------------------------------------------------
    # Correct URL
    # --------------------------------------------------------

    page_url = get_page_url(file.name)

    # --------------------------------------------------------
    # Canonical
    # --------------------------------------------------------

    html, _ = replace_meta(
        html,
        r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*/?>',
        f'<link rel="canonical" href="{page_url}">',
        "canonical"
    )

    # --------------------------------------------------------
    # OG URL
    # --------------------------------------------------------

    html, _ = replace_meta(
        html,
        r'<meta\s+property=["\']og:url["\']\s+content=["\'][^"\']*["\']\s*/?>',
        f'<meta property="og:url" content="{page_url}">',
        "og:url"
    )

    # --------------------------------------------------------
    # Fix Ravenport → Havenfall in title
    # --------------------------------------------------------

    html, _ = re.subn(
        r'(<title>.*?NemxNovels\s*[—-]\s*A\s+)[^<]*?(Story</title>)',
        r'\1Havenfall \2',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    # --------------------------------------------------------
    # Backup if something changed
    # --------------------------------------------------------

    if html != original_html:

        backup_file = BACKUP_FOLDER / file.name
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file, backup_file)

        file.write_text(html, encoding="utf-8")

        print("  [FIXED]")
        print(f"  Canonical/OG URL → {page_url}")

    else:
        print("  [OK] Nothing needed changing")


# ============================================================
# START
# ============================================================

print("=" * 60)
print("DEAR DIARY METADATA FIXER")
print("=" * 60)

html_files = [
    file for file in FOLDER.glob("*.html")
    if file.name.lower() != Path(__file__).name.lower()
]

if not html_files:
    print("\nNo HTML files found.")
    input("\nPress Enter to exit...")
    raise SystemExit


print(f"\nFound {len(html_files)} HTML files.")

for file in sorted(html_files):
    fix_file(file)


print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

if BACKUP_FOLDER.exists():
    print(f"\nBackups created in:")
    print(BACKUP_FOLDER)

print("\nYour Dear Diary metadata has been checked.")
input("\nPress Enter to exit...")