#!/usr/bin/env python3
"""
Find links with no destination (href="" / src="") and show where they are.
Read-only: never changes any file.

  python3 find_empty_links.py .            # empty href="" / src=""
  python3 find_empty_links.py . --hash     # also include href="#" placeholders

Prints: file, line, the tag, and the link text/alt so you can tell what it is.
Also writes empty_links_report.csv.
"""
import os, re, sys, csv, html

TAG = re.compile(r'<(a|link|img|script|iframe|source|form)\b([^>]*)>', re.I | re.S)
ATTR = re.compile(r'\b(href|src|action)\s*=\s*(["\'])(.*?)\2', re.I | re.S)

def clean(s, n=70):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', ' ', html.unescape(s)).strip()
    return s if len(s) <= n else s[:n] + '...'

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    inc_hash = '--hash' in sys.argv
    root = os.path.abspath(args[0])
    rows = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != '.git' and 'backup' not in d.lower()]
        for f in sorted(fn):
            if not f.lower().endswith('.html'):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding='utf-8', errors='replace', newline='') as fh:
                text = fh.read()
            for m in TAG.finditer(text):
                name, attrs = m.group(1).lower(), m.group(2)
                a = ATTR.search(attrs)
                if not a:
                    continue
                val = a.group(3).strip()
                if val == '' or (inc_hash and val == '#' and name == 'a'):
                    line = text.count('\n', 0, m.start()) + 1
                    label = ''
                    if name == 'a':
                        end = text.find('</a>', m.end())
                        label = clean(text[m.end():end if end != -1 else m.end() + 300])
                    elif name == 'img':
                        alt = re.search(r'alt\s*=\s*(["\'])(.*?)\1', attrs, re.S)
                        label = 'alt: ' + (alt.group(2) if alt else '(none)')
                    rows.append((os.path.relpath(p, root).replace(os.sep, '/'), line, name, a.group(1), val or '(empty)', label, clean(m.group(0), 110)))
    for r in rows:
        print(f"{r[0]}:{r[1]}  <{r[2]} {r[3]}=\"{'' if r[4]=='(empty)' else r[4]}\">  text: {r[5] or '-'}")
    print(f"\nFound {len(rows)} empty link(s) in {len({r[0] for r in rows})} file(s).")
    with open('empty_links_report.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['file', 'line', 'tag', 'attribute', 'value', 'link_text', 'tag_html']); w.writerows(rows)
    print("Saved: empty_links_report.csv")
main()
