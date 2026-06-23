# -*- coding: utf-8 -*-
"""
Scan source trees and rewrite non-UTF-8 text files as UTF-8 (no BOM).

Usage (from repo root paw-rescue):
  backend\\venv\\Scripts\\python.exe scripts\\ensure_utf8.py
  backend\\venv\\Scripts\\python.exe scripts\\ensure_utf8.py --check   # exit 1 if fixes needed
"""
from __future__ import annotations

import argparse
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), '..')

SCAN_ROOTS = [
    os.path.join(ROOT, 'frontend', 'src'),
    os.path.join(ROOT, 'frontend', 'public'),
    os.path.join(ROOT, 'backend'),
]

SKIP_DIR_NAMES = {
    'node_modules', 'venv', '.venv', '__pycache__', 'build', 'dist',
    'migrations', '.git', 'media', 'staticfiles',
}

EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx', '.py', '.html', '.css', '.json', '.md'}


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIR_NAMES


def iter_files():
    for base in SCAN_ROOTS:
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                if ext in EXTENSIONS:
                    yield os.path.join(dirpath, fn)


def convert_file(path: str, dry_check: bool) -> str | None:
    with open(path, 'rb') as f:
        raw = f.read()
    if not raw:
        return None
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    try:
        raw.decode('utf-8')
        return None
    except UnicodeDecodeError:
        pass
    text = None
    used_enc = None
    for enc in ('gbk', 'gb18030', 'utf-16', 'utf-16-le'):
        try:
            text = raw.decode(enc)
            used_enc = enc
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        return 'unreadable'
    if dry_check:
        return f'needs conversion (was {used_enc})'
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    return f'converted from {used_enc}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Only report; exit 1 if any file needs conversion')
    args = parser.parse_args()
    changed = []
    for path in iter_files():
        rel = os.path.relpath(path, ROOT)
        result = convert_file(path, dry_check=args.check)
        if result:
            changed.append((rel, result))
            print(rel, '->', result)
    if args.check and changed:
        print(f'\n{len(changed)} file(s) not UTF-8. Run: python scripts/ensure_utf8.py')
        sys.exit(1)
    if not args.check:
        print(f'\nDone. Converted {len(changed)} file(s).')
    elif not changed:
        print('All scanned files are valid UTF-8.')


if __name__ == '__main__':
    main()
