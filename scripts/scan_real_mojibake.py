# -*- coding: utf-8 -*-
"""Scan frontend for real mojibake (wrong codepoints, not display artifacts)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'frontend/src'

# Codepoints common in GBK-misread-as-UTF8 mojibake, NOT normal UI Chinese
BAD_RANGES = [
    range(0x6D80, 0x6E00),
    range(0x7000, 0x7050),
    range(0x7500, 0x7580),
    range(0x9300, 0x9420),
    range(0xE000, 0xF900),
]
BAD_SINGLE = {0xFFFD}


def is_bad_char(c):
    o = ord(c)
    if o in BAD_SINGLE:
        return True
    for r in BAD_RANGES:
        if o in r:
            return True
    return False


def scan_file(path: Path):
    bad_lines = []
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if any(is_bad_char(c) for c in line):
            sample = ''.join(c if is_bad_char(c) else '' for c in line)[:40]
            bad_lines.append((i, sample))
    return bad_lines


def main():
    issues = []
    for path in sorted(ROOT.rglob('*.js')):
        bad = scan_file(path)
        if bad:
            rel = path.relative_to(ROOT.parent.parent)
            issues.append((str(rel), bad[:8]))

    if not issues:
        print('No mojibake codepoints found in frontend/src')
        return

    print(f'Found {len(issues)} files with mojibake:')
    for rel, lines in issues:
        print(f'  {rel}:')
        for ln, sample in lines:
            print(f'    L{ln}: U+{" U+".join(f"{ord(c):04X}" for c in sample)}')


if __name__ == '__main__':
    main()
