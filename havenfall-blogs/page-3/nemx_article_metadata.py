#!/usr/bin/env python3
"""
NemxNovels Article Metadata Cleanup
------------------------------------
Scans article-*.html and harticle-*.html files and injects/updates
<title>, og:title, og:description, og:image and og:type tags based on
the metadata already present in each article's own markup (header
title, subtitle, type, identifier, and header image).

Does NOT touch: og:url, links, hrefs, folders, sitemap, CSS files,
or the article body/content. Only the <head> of each matched file is
modified, and only within a clearly marked, idempotent block.

Usage:
    python3 nemx_article_metadata.py --dir /path/to/site            # dry run (default)
    python3 nemx_article_metadata.py --dir /path/to/site --apply    # actually write changes

Options:
    --dir PATH        Directory to scan (default: current directory)
    --recursive       Also scan subdirectories
    --apply           Write changes to disk (default is preview/dry-run only)
    --base-url URL    Site base URL used to build absolute og:image URLs
                       (default: https://nemxnovels.site/)
    --no-backup       Skip creating .bak backups (not recommended)
"""

import argparse
import glob
import html
import os
import re
import sys
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("This script needs BeautifulSoup4. Install it with:")
    print("    pip install beautifulsoup4 --break-system-packages")
    sys.exit(1)

MARK_START = "<!-- NEMXNOVELS ARTICLE META START (auto-generated — do not hand-edit) -->"
MARK_END = "<!-- NEMXNOVELS ARTICLE META END -->"

SMALL_WORDS = {
    "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to",
    "for", "with", "from", "by", "is", "as", "&"
}


# ---------- text helpers ----------

def clean_text(s):
    """Strip whitespace, curly/straight quotes, and collapse spaces."""
    if not s:
        return ""
    s = html.unescape(s)
    s = s.strip()
    s = s.strip("\u201c\u201d\u2018\u2019\"'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def smart_title_case(s):
    """Title-case a string without shouting small words, unless first/last."""
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        if not w:
            continue
        lw = w.lower()
        if 0 < i < len(words) - 1 and lw in SMALL_WORDS:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:])
    return " ".join(out)


def esc(s):
    """Escape text for safe use inside a double-quoted HTML attribute."""
    return html.escape(s, quote=True)


# ---------- extraction ----------

class ArticleMeta:
    def __init__(self):
        self.title = ""
        self.subtitle = ""
        self.kind = ""       # e.g. "Poem"
        self.identifier = "" # e.g. "ZEKE VERSE 01"
        self.image_src = ""


def extract_metadata(soup):
    """
    Returns (meta, status, reason)
    status is one of: "ok", "skip", "error"
    """
    title_el = soup.find(id="article-header-title")
    subtitle_el = soup.find(id="article-header-subtitle")
    kind_el = soup.find(class_="article-header-link")
    # kind_el above may match the wrapping <div id="article-header-link">
    # as well as the <a class="article-header-link">; prefer an <a> if any.
    kind_a = soup.find("a", class_="article-header-link")
    if kind_a is not None:
        kind_el = kind_a
    identifier_el = soup.find(class_="article-header-bottom")
    image_el = soup.find("img", class_="article-image")
    body_el = soup.find("article", class_="article-text")

    # Nothing that looks like our article structure at all -> not recognized
    if not any([title_el, subtitle_el, kind_el, identifier_el, body_el]):
        return None, "skip", "article structure not recognized"

    meta = ArticleMeta()
    meta.title = clean_text(title_el.get_text()) if title_el else ""
    meta.subtitle = clean_text(subtitle_el.get_text()) if subtitle_el else ""
    meta.kind = clean_text(kind_el.get_text()) if kind_el else ""
    meta.identifier = clean_text(identifier_el.get_text()) if identifier_el else ""

    if not meta.title:
        return None, "error", "could not determine title"

    if image_el is None or not image_el.get("src"):
        return None, "skip", "missing article image"

    meta.image_src = image_el.get("src").strip()

    return meta, "ok", None


# ---------- building the tags ----------

def build_description(meta):
    kind = smart_title_case(meta.kind) if meta.kind else "Story"
    subtitle_disp = smart_title_case(meta.subtitle) if meta.subtitle else ""
    identifier_disp = smart_title_case(meta.identifier) if meta.identifier else ""

    if subtitle_disp:
        text = f'A {kind} from {subtitle_disp} \u2014 "{meta.title.title()}"'
    else:
        text = f'A {kind} \u2014 "{meta.title.title()}"'
    if identifier_disp:
        text += f" ({identifier_disp})"
    text += ". Read it on NemxNovels."
    return text


def build_title_tag_text(meta):
    subtitle_disp = smart_title_case(meta.subtitle) if meta.subtitle else ""
    title_disp = meta.title.title()
    if subtitle_disp:
        return f"{title_disp} | NemxNovels \u2014 {subtitle_disp}"
    return f"{title_disp} | NemxNovels"


def build_meta_block(meta, base_url):
    title_disp = meta.title.title()
    og_title = f"{title_disp} | NemxNovels"
    description = build_description(meta)
    image_url = urljoin(base_url, meta.image_src)

    lines = [
        MARK_START,
        f'<meta property="og:title" content="{esc(og_title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:image" content="{esc(image_url)}">',
        '<meta property="og:type" content="article">',
        MARK_END,
    ]
    return "\n".join(lines)


# ---------- file-level read/write (regex, preserves original formatting) ----------

TITLE_TAG_RE = re.compile(r"<title[^>]*>.*?</title>", re.IGNORECASE | re.DOTALL)
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)
EXISTING_BLOCK_RE = re.compile(
    re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
    re.DOTALL,
)


def apply_changes_to_raw(raw, meta, base_url):
    new_title_tag = f"<title>{esc(build_title_tag_text(meta))}</title>"
    if TITLE_TAG_RE.search(raw):
        raw = TITLE_TAG_RE.sub(lambda m: new_title_tag, raw, count=1)
    else:
        # No <title> tag found at all — insert one before </head>
        raw = HEAD_CLOSE_RE.sub(new_title_tag + "\n</head>", raw, count=1)

    meta_block = build_meta_block(meta, base_url)

    if EXISTING_BLOCK_RE.search(raw):
        raw = EXISTING_BLOCK_RE.sub(lambda m: meta_block, raw, count=1)
    else:
        if not HEAD_CLOSE_RE.search(raw):
            return None  # can't find where to insert; caller treats as error
        raw = HEAD_CLOSE_RE.sub(meta_block + "\n</head>", raw, count=1)

    return raw


# ---------- main ----------

def find_article_files(directory, recursive):
    patterns = ["article-*.html", "harticle-*.html"]
    files = []
    for pattern in patterns:
        if recursive:
            files.extend(glob.glob(os.path.join(directory, "**", pattern), recursive=True))
        else:
            files.extend(glob.glob(os.path.join(directory, pattern)))
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(description="NemxNovels article metadata cleanup")
    parser.add_argument("--dir", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("--recursive", action="store_true", help="Also scan subdirectories")
    parser.add_argument("--apply", action="store_true", help="Write changes to disk (default: dry run)")
    parser.add_argument("--base-url", default="https://nemxnovels.site/havenfall-blogs/page-3/",
                         help="Site base URL for absolute og:image URLs")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating .bak backups")
    args = parser.parse_args()

    files = find_article_files(args.dir, args.recursive)

    updated, skipped, errors = [], [], []

    for path in files:
        name = os.path.basename(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception as e:
            errors.append((name, f"could not read file ({e})"))
            continue

        try:
            soup = BeautifulSoup(raw, "html.parser")
        except Exception as e:
            errors.append((name, f"could not parse HTML ({e})"))
            continue

        meta, status, reason = extract_metadata(soup)

        if status == "skip":
            skipped.append((name, reason))
            continue
        if status == "error":
            errors.append((name, reason))
            continue

        new_raw = apply_changes_to_raw(raw, meta, args.base_url)
        if new_raw is None:
            errors.append((name, "could not locate </head> to insert metadata"))
            continue

        if args.apply:
            if not args.no_backup:
                bak_path = path + ".bak"
                if not os.path.exists(bak_path):
                    with open(bak_path, "w", encoding="utf-8") as f:
                        f.write(raw)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_raw)

        updated.append(name)

    # ---------- report ----------
    print("NEMXNOVELS ARTICLE METADATA CLEANUP")
    if not args.apply:
        print("(dry run — no files were modified; use --apply to write changes)")
    print(f"Processed: {len(files)}")
    print(f"Updated:   {len(updated)}")
    print(f"Skipped:   {len(skipped)}")
    print(f"Errors:    {len(errors)}")
    print()

    if updated:
        print("Updated:")
        for name in updated:
            print(f"\u2713 {name}")
        print()

    if skipped:
        print("Skipped:")
        for name, reason in skipped:
            print(f"\u26a0 {name} \u2014 {reason}")
        print()

    if errors:
        print("Errors:")
        for name, reason in errors:
            print(f"\u2717 {name} \u2014 {reason}")
        print()


if __name__ == "__main__":
    main()
