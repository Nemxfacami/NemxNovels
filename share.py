from pathlib import Path
import re
import shutil

# ============================================================
# SETTINGS
# ============================================================

ROOT_FOLDER = Path(".")

CREATE_BACKUPS = True


# ============================================================
# SHARE MENU OPTION
# ============================================================

SHARE_OPTION = '''


  <div class="option">
     <a class="options-link" href="#" onclick="sharePage(); return false;">
         <div class="option-box-style">
             <div id="option-icon-circle">
                 <img class="option-icon" src="share.png" loading="lazy"/>
             </div>

             <div id="option-detail-box">
                 <p id="option-detail">
                     Share
                 </p>
             </div>
         </div>
     </a>
  </div>
'''


# ============================================================
# SHARE JAVASCRIPT
# ============================================================

SHARE_JS = '''

function sharePage() {

    const shareData = {
        title: document.title,
        text: "Read this on NemxNovels",
        url: window.location.href
    };

    if (navigator.share) {

        navigator.share(shareData)
            .catch((error) => {
                console.log("Sharing cancelled:", error);
            });

    } else {

        navigator.clipboard.writeText(window.location.href)
            .then(() => {
                alert("Link copied!");
            })
            .catch(() => {
                alert("Unable to copy the link.");
            });

    }
}
'''


# ============================================================
# PROCESS FILE
# ============================================================

def process_file(file_path):

    try:
        content = file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        print(f"[SKIP] Encoding problem: {file_path}")
        return

    original = content

    # --------------------------------------------------------
    # CHECK FOR MENU
    # --------------------------------------------------------

    menu_start = content.find('<div id="menu">')

    if menu_start == -1:
        print(f"[SKIP] No menu: {file_path}")
        return

    # --------------------------------------------------------
    # ADD SHARE BUTTON
    # --------------------------------------------------------

    if 'onclick="sharePage(); return false;"' not in content:

        # Find the closing div of the menu.
        #
        # We use a small HTML div-depth scanner rather than
        # looking for a particular option such as Chapters.

        div_pattern = re.compile(r'</?div\b[^>]*>', re.IGNORECASE)

        depth = 0
        menu_end = None

        for match in div_pattern.finditer(content, menu_start):

            tag = match.group(0)

            if tag.startswith("</"):
                depth -= 1

                if depth == 0:
                    menu_end = match.start()
                    break

            else:
                depth += 1

        if menu_end is not None:

            content = (
                content[:menu_end]
                + SHARE_OPTION
                + content[menu_end:]
            )

            print(f"[SHARE ADDED] {file_path}")

        else:
            print(f"[WARNING] Could not find menu closing div: {file_path}")

    else:

        print(f"[SHARE EXISTS] {file_path}")


    # --------------------------------------------------------
    # ADD SHARE JAVASCRIPT
    # --------------------------------------------------------

    if "function sharePage()" not in content:

        # Find the last closing script tag.
        script_positions = list(
            re.finditer(r'</script\s*>', content, re.IGNORECASE)
        )

        if script_positions:

            last_script = script_positions[-1]

            content = (
                content[:last_script.start()]
                + SHARE_JS
                + "\n"
                + content[last_script.start():]
            )

            print(f"[JS ADDED] {file_path}")

        else:

            print(f"[WARNING] No script element found: {file_path}")

    else:

        print(f"[JS EXISTS] {file_path}")


    # --------------------------------------------------------
    # SAVE ONLY IF CHANGED
    # --------------------------------------------------------

    if content != original:

        if CREATE_BACKUPS:

            backup_path = file_path.with_suffix(
                file_path.suffix + ".bak"
            )

            shutil.copy2(file_path, backup_path)

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        print(f"[UPDATED] {file_path}")
        print()

    else:

        print(f"[UNCHANGED] {file_path}")
        print()


# ============================================================
# SCAN ALL HTML FILES
# ============================================================

html_files = list(ROOT_FOLDER.rglob("*.html"))

print("=" * 60)
print(f"Found {len(html_files)} HTML files")
print("=" * 60)
print()

for html_file in html_files:
    process_file(html_file)

print("=" * 60)
print("DONE")
print("=" * 60)
