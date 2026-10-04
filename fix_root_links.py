#!/usr/bin/env python3
"""
Fix folder-relative links (e.g. href="news-page.html" inside /news/ pages)
by adding a leading "/" when the target exists at the site root but NOT
relative to the page's own folder.

Usage (run from anywhere):
  python3 fix_root_links.py /path/to/nemxnovels            # DRY RUN, changes nothing
  python3 fix_root_links.py /path/to/nemxnovels --apply    # actually rewrite files
Writes fix_root_links_report.csv next to the script's working dir.
"""
import os, re, sys, csv, html
from urllib.parse import unquote

ATTR = re.compile(r'''(\b(?:href|src|action|poster|data-src)\s*=\s*)(["'])(.*?)\2''', re.I | re.S)
SKIP_PREFIX = ('http:', 'https:', '//', 'mailto:', 'tel:', 'javascript:', 'data:', '#', '/', 'sms:')

def exists(root, rel):
    rel = rel.split('#')[0].split('?')[0]
    if not rel:
        return True
    p = os.path.normpath(os.path.join(root, rel))
    if os.path.isdir(p):
        return os.path.isfile(os.path.join(p, 'index.html'))
    return os.path.isfile(p)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    changes, total_files = [], 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != '.git' and 'backup' not in d.lower()]
        for f in fn:
            if not f.lower().endswith('.html'):
                continue
            path = os.path.join(dp, f)
            relsrc = os.path.relpath(path, root).replace(os.sep, '/')
            with open(path, 'r', encoding='utf-8', newline='') as fh:
                text = fh.read()
            total_files += 1
            def sub(m):
                prefix, q, link = m.groups()
                raw = link.strip()
                if not raw or raw.lower().startswith(SKIP_PREFIX):
                    return m.group(0)
                dec = unquote(html.unescape(raw))
                if exists(dp, dec):
                    return m.group(0)          # already fine from its own folder
                if exists(root, dec):          # exists at site root -> add "/"
                    line = text.count('\n', 0, m.start()) + 1
                    new = '/' + raw
                    changes.append((relsrc, line, raw, new))
                    return f'{prefix}{q}{new}{q}'
                return m.group(0)              # truly missing: leave for a human
            new_text = ATTR.sub(sub, text)
            if apply and new_text != text:
                with open(path, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(new_text)
    with open('fix_root_links_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'old', 'new']); w.writerows(changes)
    files_changed = len({c[0] for c in changes})
    print(f"Scanned {total_files} HTML files.")
    print(f"{'FIXED' if apply else 'WOULD FIX'} {len(changes)} links in {files_changed} files.")
    print("Details: fix_root_links_report.csv" + ("" if apply else "   (dry run - nothing was changed; add --apply)"))

main()
