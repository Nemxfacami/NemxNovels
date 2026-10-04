#!/usr/bin/env python3
"""
Fix menu links whose onclick has leftover junk after the closing quote:

  BAD : onclick="alert('Home Map is not available yet.'); return false;"Home Map is not available yet.\\'); return false;">
  GOOD: onclick="alert('Home Map is not available yet.'); return false;">

Works for any message (Home Map, City Map, ...). Only removes the junk text
between the correct onclick and the closing ">". Nothing else is touched.

  python3 fix_broken_onclick.py .            # DRY RUN
  python3 fix_broken_onclick.py . --apply
Writes fix_broken_onclick_report.csv
"""
import os, re, sys, csv

BAD = re.compile(
    r'''(onclick\s*=\s*"alert\('[^']*'\)\s*;\s*return\s+false\s*;?")'''   # the good onclick
    r'''([^<>"]*?\\'\)\s*;\s*return\s+false\s*;?")''')                    # leftover junk ending in \'); return false;"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    rows, files, scanned = [], 0, 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != '.git' and 'backup' not in d.lower()]
        for f in sorted(fn):
            if not f.lower().endswith('.html'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, '/')
            with open(p, encoding='utf-8', errors='replace', newline='') as fh:
                text = fh.read()
            scanned += 1
            found = list(BAD.finditer(text))
            if not found:
                continue
            files += 1
            for m in found:
                line = text.count('\n', 0, m.start()) + 1
                msg = re.search(r"alert\('([^']*)'", m.group(1)).group(1)
                rows.append((rel, line, msg))
            if apply:
                text = BAD.sub(lambda m: m.group(1), text)
                with open(p, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(text)
    with open('fix_broken_onclick_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'result', 'message'])
        for r in rows: w.writerow([r[0], r[1], 'fixed' if apply else 'would fix', r[2]])
    print(f"Scanned {scanned} HTML files.")
    print(f"{'FIXED' if apply else 'WOULD FIX'} {len(rows)} onclick attributes in {files} files.")
    print("Report: fix_broken_onclick_report.csv" + ("" if apply else "   (dry run - add --apply)"))
main()
