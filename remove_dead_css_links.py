#!/usr/bin/env python3
"""
Remove <link> tags that point at stylesheets which don't exist.
Only touches the filenames listed in TARGETS below. Dry run by default.

  python3 remove_dead_css_links.py .            # report only
  python3 remove_dead_css_links.py . --apply    # rewrite files
"""
import os, re, sys, csv

TARGETS = ['mobile-article-view-style.css', 'aside-pc-style.css']

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        sys.exit(__doc__)
    root = os.path.abspath(args[0])
    names = '|'.join(re.escape(t) for t in TARGETS)
    # a whole line containing just the <link> tag, or the tag alone inline
    tag = r'<link\b[^>]*href\s*=\s*["\'](?:[^"\']*/)?(?:%s)(?:\?[^"\']*)?["\'][^>]*>' % names
    line_re = re.compile(r'^[ \t]*' + tag + r'[ \t]*\r?\n', re.I | re.M)
    inline_re = re.compile(tag, re.I)
    rows = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != '.git']
        for f in fn:
            if not f.lower().endswith('.html'):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding='utf-8', newline='') as fh:
                text = fh.read()
            new, n1 = line_re.subn('', text)
            new, n2 = inline_re.subn('', new)
            if n1 + n2:
                rows.append((os.path.relpath(p, root).replace(os.sep, '/'), n1 + n2))
                if apply:
                    with open(p, 'w', encoding='utf-8', newline='') as fh:
                        fh.write(new)
    with open('remove_dead_css_report.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['file', 'tags_removed']); w.writerows(rows)
    print(f"{'REMOVED' if apply else 'WOULD REMOVE'} {sum(r[1] for r in rows)} tags in {len(rows)} files.")
    print("Details: remove_dead_css_report.csv" + ("" if apply else "   (dry run - add --apply)"))
main()
