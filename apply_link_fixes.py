#!/usr/bin/env python3
"""
Apply a fixed list of exact link fixes. Dry run by default.

  python3 apply_link_fixes.py .            # report only
  python3 apply_link_fixes.py . --apply    # rewrite files
"""
import os, sys, csv

H3 = 'havenfall-blogs/page-3/harticle-%d.html'
FIXES = []
# 1. typo: rapha-asylum -> raphaasylum (folder name has no dash)
for f in ['index.html', 'havenfall-blogs/page-2/page2.html', 'havenfall-blogs/page-3/page3.html',
          'ravenport-blogs/page-2/page2.html', 'ravenport-blogs/page-3/page3.html']:
    FIXES.append((f, 'ravenport/rapha-asylum/index.html', '/ravenport/raphaasylum/'))
# 2. page-3 articles linking to "page2.html" (only page2 in the Havenfall blog)
for n in range(12, 17):
    FIXES.append((H3 % n, 'page2.html', '/havenfall-blogs/page-2/page2.html'))
# 3. wrong path for an image that exists in the same folder
FIXES.append(('ravenport/original-story/Ravenport-character-Darkkid.html',
              '/lucienprofile.webp', '/ravenport/original-story/lucienprofile.webp'))
# 4. Birdshugs pages pointing at Behind The Curse's "where were you" page (copy-paste)
for f in ['ravenport/birdshugs/birdshugs-chapter2.html', 'ravenport/birdshugs/index.html']:
    FIXES.append((f, 'behindthecurse-wherewereyou.html', 'birdshugs-wherewereyou.html'))

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    rows, total = [], 0
    for rel, old, new in FIXES:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            rows.append((rel, old, new, 0, 'FILE NOT FOUND')); continue
        with open(p, encoding='utf-8', newline='') as fh:
            text = fh.read()
        n = 0
        for q in ('"', "'"):
            c = text.count(q + old + q)
            if c:
                text = text.replace(q + old + q, q + new + q); n += c
        rows.append((rel, old, new, n, 'ok' if n else 'NOT FOUND (already fixed?)'))
        total += n
        if apply and n:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
    with open('apply_link_fixes_report.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['file', 'old', 'new', 'count', 'status']); w.writerows(rows)
    for r in rows:
        print(f"{r[4]:28} {r[3]}x  {r[0]}")
    print(f"\n{'FIXED' if apply else 'WOULD FIX'} {total} links.  (report: apply_link_fixes_report.csv)")
    if not apply: print("Dry run - add --apply to change files.")
main()
