#!/usr/bin/env python3
"""
Find every sharePage() "shareData" object and make its title  document.title
(so each page shares its OWN title instead of a copy-pasted one).

  python3 fix_share_title.py .            # DRY RUN: report only
  python3 fix_share_title.py . --apply    # rewrite files

Only the `title:` line inside the shareData object is changed. Nothing else.
Also reports (never changes):
  - pages whose first <title> is empty/missing (document.title would be blank)
  - pages that use navigator.share but have no shareData object
  - pages whose shareData url is not window.location.href
Writes fix_share_title_report.csv
"""
import os, re, sys, csv

OBJ = re.compile(r'(\bshareData\s*=\s*\{)(.*?)(\})', re.S)
TITLE = re.compile(r'(\btitle\s*:\s*)("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`[^`]*`|[^,\n}]+?)(\s*(?:,|\n|$))')
URL = re.compile(r'\burl\s*:\s*([^,\n}]+)')
HTML_TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    changed, ok, notes, scanned = [], 0, [], 0
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
            m = OBJ.search(text)
            if not m:
                if 'navigator.share' in text:
                    notes.append((rel, '', 'uses navigator.share but no shareData object - check by hand'))
                continue
            body = m.group(2)
            tm = TITLE.search(body)
            line = text.count('\n', 0, m.start()) + 1
            if not tm:
                notes.append((rel, line, 'shareData has no title: line - check by hand'))
                continue
            old = tm.group(2).strip()
            um = URL.search(body)
            if um and um.group(1).strip() != 'window.location.href':
                notes.append((rel, line, f'shareData url is {um.group(1).strip()} (not window.location.href)'))
            pt = HTML_TITLE.search(text)
            if not pt or not pt.group(1).strip():
                notes.append((rel, '', 'first <title> is empty/missing: document.title would be blank'))
            if old == 'document.title':
                ok += 1
                continue
            changed.append((rel, line, old))
            if apply:
                new_body = body[:tm.start(2)] + 'document.title' + body[tm.end(2):]
                text = text[:m.start(2)] + new_body + text[m.end(2):]
                with open(p, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(text)
    with open('fix_share_title_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'type', 'detail'])
        for r in changed: w.writerow([r[0], r[1], 'title fixed' if apply else 'title would change', r[2]])
        for r in notes: w.writerow([r[0], r[1], 'NOTE', r[2]])
    print(f"Scanned {scanned} HTML files. Already correct: {ok}.")
    print(f"{'FIXED' if apply else 'WOULD FIX'} {len(changed)} share titles:")
    for r in changed: print(f"  {r[0]}:{r[1]}   was: {r[2]}")
    if notes:
        print(f"\n{len(notes)} note(s) for you to check by hand:")
        for r in notes: print(f"  {r[0]}{(':'+str(r[1])) if r[1] else ''}  - {r[2]}")
    print("\nReport: fix_share_title_report.csv" + ("" if apply else "   (dry run - add --apply)"))
main()
