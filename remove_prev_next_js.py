#!/usr/bin/env python3
"""
Remove the broken "previous"/"next" click handlers:

    document.getElementById("previous").addEventListener("click", function () {
        window.location.href = "#";
    });

They crash the page script (no element has that id), which stops the
scroll-position code below them from running. The Previous/Next buttons are
plain <a href> links and keep working without them.

Safety rules:
  - only removes the exact handler above (body = window.location.href = "#")
  - skips it if an element with id="previous"/"next" really exists on the page
  - leaves commented-out copies alone
  - never touches anything else

  python3 remove_prev_next_js.py .            # DRY RUN
  python3 remove_prev_next_js.py . --apply
Writes remove_prev_next_report.csv
"""
import os, re, sys, csv

HANDLER = re.compile(
    r'''[ \t]*document\.getElementById\(\s*["'](previous|next)["']\s*\)\s*\.addEventListener\(\s*["']click["']\s*,\s*'''
    r'''function\s*\(\s*\)\s*\{\s*window\.location\.href\s*=\s*["']#["']\s*;?\s*\}\s*\)\s*;?[ \t]*\r?\n?''')

def in_comment(text, pos):
    if text.rfind('/*', 0, pos) > text.rfind('*/', 0, pos):
        return True
    line_start = text.rfind('\n', 0, pos) + 1
    return '//' in text[line_start:pos]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    rows, notes, scanned, pages = [], [], 0, 0
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
            if 'getElementById' not in text:
                continue
            spans = []
            for m in HANDLER.finditer(text):
                name = m.group(1)
                line = text.count('\n', 0, m.start()) + 1
                if in_comment(text, m.start()):
                    continue
                if re.search(r'\bid\s*=\s*["\']%s["\']' % name, text, re.I):
                    notes.append((rel, line, f'element id="{name}" EXISTS - handler left in place'))
                    continue
                spans.append((m.start(), m.end()))
                rows.append((rel, line, name))
            # anything similar left over (different shape, not removed, no real id)? tell the user
            leftovers = []
            for m in re.finditer(r"""getElementById\(\s*["'](previous|next)["']\s*\)""", text):
                if in_comment(text, m.start()):
                    continue
                if any(a <= m.start() < b for a, b in spans):
                    continue
                if re.search(r'\bid\s*=\s*["\']%s["\']' % m.group(1), text, re.I):
                    continue
                line = text.count('\n', 0, m.start()) + 1
                leftovers.append((rel, line, f'getElementById("{m.group(1)}") present in a different form - check by hand'))
            notes.extend(leftovers)
            if spans:
                pages += 1
                if apply:
                    for a, b in reversed(spans):
                        text = text[:a] + text[b:]
                    with open(p, 'w', encoding='utf-8', newline='') as fh:
                        fh.write(text)
    with open('remove_prev_next_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'result', 'detail'])
        for r in rows: w.writerow([r[0], r[1], 'removed' if apply else 'would remove', r[2]])
        for r in notes: w.writerow([r[0], r[1], 'NOTE', r[2]])
    print(f"Scanned {scanned} HTML files.")
    print(f"{'REMOVED' if apply else 'WOULD REMOVE'} {len(rows)} handlers in {pages} files.")
    if notes:
        print(f"\n{len(notes)} note(s) to check by hand:")
        for r in notes: print(f"  {r[0]}:{r[1]}  - {r[2]}")
    print("\nReport: remove_prev_next_report.csv" + ("" if apply else "   (dry run - add --apply)"))
main()
