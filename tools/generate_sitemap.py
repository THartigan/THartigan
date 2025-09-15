#!/usr/bin/env python3
import os
import sys
import time
from urllib.parse import quote

BASE_URL = os.environ.get("SITEMAP_BASE", "https://hartigan.cc")

def is_hidden(path: str) -> bool:
    parts = path.split(os.sep)
    return any(p.startswith('.') for p in parts)

def rel_paths(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        # filter out hidden dirs in-place
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        if is_hidden(dirpath):
            continue
        for fn in filenames:
            if fn.startswith('.'):  # skip hidden files
                continue
            if not (fn.lower().endswith('.html') or fn.lower().endswith('.pdf')):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            yield rel

def url_for(relpath: str) -> str:
    # Percent-encode path segments but keep slashes
    # Keep safe chars used commonly in URLs
    return BASE_URL.rstrip('/') + '/' + quote(relpath.replace('\\', '/'), safe='/-._~')

def lastmod_for(path: str) -> str:
    ts = os.path.getmtime(path)
    # Format as YYYY-MM-DD in UTC
    return time.strftime('%Y-%m-%d', time.gmtime(ts))

def main() -> int:
    root = os.getcwd()

    files = sorted(rel_paths(root))

    # Build list, skipping top-level index.html (we'll include root '/')
    items = []
    index_lastmod = None
    for rel in files:
        if rel == 'index.html':
            try:
                index_lastmod = lastmod_for(os.path.join(root, rel))
            except OSError:
                index_lastmod = None
            continue
        items.append(rel)

    # Start XML
    out = []
    out.append('<?xml version="1.0" encoding="utf-8"?>')
    out.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Root URL
    out.append('  <url>')
    out.append(f'    <loc>{BASE_URL.rstrip("/")}/</loc>')
    if index_lastmod:
        out.append(f'    <lastmod>{index_lastmod}</lastmod>')
    out.append('  </url>')

    # Other URLs
    for rel in items:
        loc = url_for(rel)
        try:
            lm = lastmod_for(os.path.join(root, rel))
        except OSError:
            lm = None
        out.append('  <url>')
        out.append(f'    <loc>{loc}</loc>')
        if lm:
            out.append(f'    <lastmod>{lm}</lastmod>')
        out.append('  </url>')

    out.append('</urlset>')

    sys.stdout.write('\n'.join(out) + '\n')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

