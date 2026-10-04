import re
import sys
from pathlib import Path

ROOT = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), "."))
DRY_RUN = "--dry" in sys.argv

SECTION_RE = re.compile(
    r'(<section\s+class\s*=\s*"mobile-header-book-list"\s*>)(.*?)(</section>)',
    re.S,
)
BLOCK_RE = re.compile(
    r'<div\s+id\s*=\s*"mobile-book-cover"\s*>.*?</div>',
    re.S,
)
TARGET = "/havenfall/sevensteps/"


def fix_section(m):
    open_tag, body, close_tag = m.groups()
    blocks = list(BLOCK_RE.finditer(body))
    if len(blocks) < 2:
        return m.group(0)

    idx = next((i for i, b in enumerate(blocks) if TARGET in b.group(0)), None)
    if idx is None or idx == 0:
        return m.group(0)  # not found, or already first

    target = blocks[idx]
    first = blocks[0]
    text = target.group(0)

    # remove the sevensteps block (it comes after the first block,
    # so first.start() is still valid afterwards)
    body = body[:target.start()] + body[target.end():]

    # keep the same indentation as the current first block
    line_start = body.rfind("\n", 0, first.start()) + 1
    indent = body[line_start:first.start()]
    if indent.strip():
        indent = ""

    body = body[:first.start()] + text + "\n\n" + indent + body[first.start():]
    return open_tag + body + close_tag


changed = 0
for path in ROOT.rglob("*.html"):
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            original = f.read()
    except UnicodeDecodeError:
        print(f"SKIP (encoding): {path}")
        continue

    updated = SECTION_RE.sub(fix_section, original)
    if updated != original:
        changed += 1
        print(f"{'WOULD UPDATE' if DRY_RUN else 'UPDATED'}: {path}")
        if not DRY_RUN:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(updated)

print(f"\nDone. {changed} file(s) {'would be ' if DRY_RUN else ''}changed.")