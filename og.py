#!/usr/bin/env python3
"""
Fix the og:image paths that are clearly typos / wrong folder. Dry run by default.
Run from anywhere inside the site (it finds the root by the .git folder),
or pass --root /path/to/site.

  python3 fix_og_paths.py            # DRY RUN
  python3 fix_og_paths.py --apply

Only the content="..." of <meta property="og:image"> is touched, only when it
equals one of the OLD paths below, and only if the NEW file really exists.
"""
import os, re, sys, csv
from urllib.parse import urlparse

DOMAIN = 'https://nemxnovels.site'
FIXES = {   # old path -> new path
    '/havenfa/sevensteps/sevensteps-og.webp':   '/havenfall/sevensteps/sevensteps-og.webp',
    '/havenfall/daggeroflight-og.webp':         '/havenfall/daggeroflight/daggeroflight-og.webp',
    '/ravenport/motelbloodbath-og.webp':        '/ravenport/motelbloodbath/motelbloodbath-og.webp',
    '/nemxnovels-hiring-og.webp':               '/ravenport/jobless/nemxnovels-hiring-og.webp',
    '/occult-arcana/assets/occult-arcana-og.webp': '/occult-arcana/occult-arcana-og.webp',
}
META = re.compile(r'<meta\b[^>]*>', re.I | re.S)
OG = re.compile(r'''property\s*=\s*["']og:image["']''', re.I)
CONTENT = re.compile(r'''(content\s*=\s*)(["'])(.*?)\2''', re.I | re.S)

def find_root():
    argv = sys.argv[1:]
    if '--root' in argv:
        return os.path.abspath(argv[argv.index('--root') + 1])
    p = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(p, '.git')): return p
        up = os.path.dirname(p)
        if up == p: sys.exit("Site root not found (no .git above). Use --root /path/to/site")
        p = up

def main():
    apply = '--apply' in sys.argv
    root = find_root()
    print(f"Site root: {root}\n")
    rows = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != '.git' and 'backup' not in d.lower()]
        for f in sorted(fn):
            if not f.lower().endswith('.html'): continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, '/')
            with open(p, encoding='utf-8', errors='replace', newline='') as fh:
                text = fh.read()
            changed = False
            def sub(m):
                nonlocal changed
                tag = m.group(0)
                if not OG.search(tag): return tag
                c = CONTENT.search(tag)
                if not c: return tag
                path = urlparse(c.group(3).strip()).path
                if path not in FIXES: return tag
                new = FIXES[path]
                line = text.count('\n', 0, m.start()) + 1
                if not os.path.isfile(os.path.join(root, new.lstrip('/'))):
                    rows.append((rel, line, path, new, 'SKIPPED - new file does not exist'))
                    return tag
                rows.append((rel, line, path, new, 'fixed' if apply else 'would fix'))
                changed = True
                return tag[:c.start(3)] + DOMAIN + new + tag[c.end(3):]
            new_text = META.sub(sub, text)
            if apply and changed:
                with open(p, 'w', encoding='utf-8', newline='') as fh: fh.write(new_text)
    with open('fix_og_paths_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'old', 'new', 'result']); w.writerows(rows)
    for r in rows: print(f"{r[4]:34} {r[0]}:{r[1]}\n    {r[2]}  ->  {r[3]}")
    n = sum(1 for r in rows if r[4] in ('fixed', 'would fix'))
    print(f"\n{'FIXED' if apply else 'WOULD FIX'} {n} og:image paths.  Report: fix_og_paths_report.csv" + ("" if apply else "   (dry run - add --apply)"))
main()