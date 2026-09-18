from pathlib import Path
import re
from urllib.parse import quote

# ============================================================
# SETTINGS
# ============================================================

ROOT_FOLDER = Path(".")

BASE_URL = "https://nemxnovels.site/havenfall/blueroom/"

OG_IMAGE = (
    "https://nemxnovels.site/havenfall/blueroom/"
    "nemxnovels-blueroom-og.webp"
)

# ============================================================
# DETECT EXISTING OG METADATA
# ============================================================

OG_META_PATTERN = re.compile(
    r'<meta\b[^>]*property\s*=\s*["\']og:[^"\']+["\'][^>]*>',
    re.IGNORECASE
)

# ============================================================
# PROFILE IMAGE SELECTORS
# Higher score = stronger indication that this is the
# CONTACT'S profile image.
# ============================================================

PROFILE_CLASSES = {
    "msgr-profile-photo": 100,
    "contact-avatar": 95,
    "contact-photo": 95,
    "profile-avatar": 90,
    "profile-photo": 90,
    "user-profile-photo": 90,
    "avatar": 80,

    # Lowest priority because this may be the current user's
    # own image rather than the contact's.
    "header-avatar": 40,
}

# ============================================================
# FIND PROFILE IMAGE
# ============================================================

def find_profile_image(html):
    """
    Scan every <img> in the HTML and score it based on its
    class name.

    This allows the script to work with different Blue
    Chatroom designs.
    """

    img_pattern = re.compile(
        r'<img\b([^>]*)>',
        re.IGNORECASE
    )

    candidates = []

    for match in img_pattern.finditer(html):

        attributes = match.group(1)

        # Find src
        src_match = re.search(
            r'\bsrc\s*=\s*["\']([^"\']+)["\']',
            attributes,
            re.IGNORECASE
        )

        if not src_match:
            continue

        src = src_match.group(1)

        # Find class
        class_match = re.search(
            r'\bclass\s*=\s*["\']([^"\']+)["\']',
            attributes,
            re.IGNORECASE
        )

        if not class_match:
            continue

        classes = class_match.group(1).split()

        score = 0
        matched_class = None

        for class_name in classes:
            if class_name in PROFILE_CLASSES:

                class_score = PROFILE_CLASSES[class_name]

                if class_score > score:
                    score = class_score
                    matched_class = class_name

        if score > 0:
            candidates.append(
                (score, src, matched_class)
            )

    if not candidates:
        return None

    # Highest scoring profile image wins
    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return candidates[0]


# ============================================================
# GENERATE METADATA
# ============================================================

def generate_metadata(og_url):

    return f'''    <meta name="description" content="Blue Chatroom — A fictional messaging experience from NemxNovels. Explore contacts, conversations, and the people behind the messages.">

    <meta name="author" content="NemxNovels">

    <meta name="keywords" content="NemxNovels, Blue Chatroom, fictional chat, messaging, interactive story, digital story, chatroom">

    <link rel="icon" type="image/png" href="favicon.png">

    <meta property="og:image" content="{OG_IMAGE}">
    <meta property="og:title" content="NemxNovels — Blue Chatroom">
    <meta property="og:description" content="A fictional messaging experience where conversations reveal more than they seem. Explore the contacts behind Blue Chatroom.">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="NemxNovels">
    <meta property="og:url" content="{og_url}">

    <meta name="robots" content="noindex, nofollow">

'''


# ============================================================
# PROCESS HTML FILE
# ============================================================

def process_file(file_path):

    try:
        html = file_path.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        print(f"[ERROR] Could not read: {file_path}")
        return

    # --------------------------------------------------------
    # STRICT RULE:
    # If there is EVEN ONE OG meta tag, skip the file.
    # --------------------------------------------------------

    if OG_META_PATTERN.search(html):

        print(f"[SKIP - OG EXISTS] {file_path}")
        return

    # --------------------------------------------------------
    # Find contact/profile image
    # --------------------------------------------------------

    profile = find_profile_image(html)

    if not profile:

        print(f"[NO PROFILE IMAGE] {file_path}")
        return

    score, image_src, matched_class = profile

    # --------------------------------------------------------
    # Extract filename
    # --------------------------------------------------------

    image_filename = Path(image_src.split("?")[0]).name

    image_stem = Path(image_filename).stem

    if not image_stem:

        print(f"[NO VALID IMAGE NAME] {file_path}")
        return

    # --------------------------------------------------------
    # Build OG URL
    #
    # lilith.webp -> lilith.html
    # emo-girl.webp -> emo-girl.html
    # --------------------------------------------------------

    og_url = (
        BASE_URL
        + quote(image_stem)
        + ".html"
    )

    metadata = generate_metadata(og_url)

    # --------------------------------------------------------
    # Insert metadata immediately after <head>
    # --------------------------------------------------------

    head_match = re.search(
        r'<head\b[^>]*>',
        html,
        re.IGNORECASE
    )

    if not head_match:

        print(f"[NO <HEAD>] {file_path}")
        return

    insert_position = head_match.end()

    updated_html = (
        html[:insert_position]
        + "\n\n"
        + metadata
        + html[insert_position:]
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    file_path.write_text(
        updated_html,
        encoding="utf-8"
    )

    print(
        f"[UPDATED] {file_path}\n"
        f"          Image : {image_filename}\n"
        f"          Class : {matched_class}\n"
        f"          OG URL: {og_url}\n"
    )


# ============================================================
# SCAN EVERYTHING
# ============================================================

def main():

    html_files = list(
        ROOT_FOLDER.rglob("*.html")
    )

    print(
        f"\nScanning {len(html_files)} HTML files...\n"
    )

    for file_path in html_files:

        process_file(file_path)

    print("\nScan complete.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()