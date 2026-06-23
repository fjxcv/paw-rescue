# -*- coding: utf-8 -*-
"""Fix remaining mojibake by exact codepoint replacement."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Known wrong -> correct sequences (GBK mis-decoded as UTF-8)
GLOBAL_REPLACEMENTS = [
    ('\u6d93\u5b29\u7af4\u5bee\ufffd', '\u4e0b\u4e00\u5f20'),
    ('\u6d93\u5b29\u7af4\u5bee', '\u4e0b\u4e00\u5f20'),
    ('\u6d93\u5a41\u7d36\u6fb6\u8fab\u89e6', '\u4e0a\u4f20\u5931\u8d25'),
    ('\u93c6\u50cd\u6a3b\u93b4\u5b08\u3064\u6d78\u2103\u4f05', '\u6682\u65e0\u62a5\u5931\u4fe1\u606f'),
    ('\u93c6\u50cd\u6a3b\u7ec7\u6237\u6afb\u6587\u7ae0', '\u6682\u65e0\u79d1\u666e\u6587\u7ae0'),
    ('\u93c6\u50cd\u6a3b\u934f\ue010\u6186', '\u6682\u65e0\u516c\u544a'),
    ('\u93c6\u50cd\u6a3b\u934f\ufffd\u6186', '\u6682\u65e0\u516c\u544a'),
    ('\u6d93\u5a41\u7d36\u6fb6\u8fab\u89e6', '\u4e0a\u4f20\u5931\u8d25'),
    ('\u7039\u72b5\u589f\u934f\u5236\u9851', '\u5ba0\u7269\u5206\u7c7b'),
    ('\u69d0\ufeff\u6c41\u9521\ufffd', '\u8f6e\u64ad\u56fe'),
]

MOJIBAKE_RE = re.compile(
    r'[\u6d80-\u6dff\u7000-\u7040\u7500-\u757f\u8f00-\u8fff\u9300-\u9400\ue000-\uf8ff\ufffd]'
)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in GLOBAL_REPLACEMENTS:
        text = text.replace(old, new)
    # LostFoundList partial comment
    text = text.replace('// \u60a9\u8d4f\u7b5b\n', '// \u60a9\u8d4f\u7b5b\u9009\n')
    if text != original:
        path.write_text(text, encoding='utf-8', newline='\n')
        return True
    return False


def scan_mojibake(path: Path) -> list[int]:
    lines = path.read_text(encoding='utf-8').splitlines()
    bad = []
    for i, line in enumerate(lines, 1):
        if MOJIBAKE_RE.search(line):
            bad.append(i)
    return bad


def fix_portal_models(path: Path) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('"""') and 'Carousel' in lines[i + 1] if i + 1 < len(lines) else False:
            pass
        if line.strip().startswith('"""') and i < 10:
            lines[i] = '    """\u9996\u9875\u8f6e\u64ad\u56fe"""'
            break
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    home = ROOT / 'frontend/src/pages/Home.js'
    fix_file(home)
    fix_file(ROOT / 'frontend/src/pages/LostFoundList.js')
    fix_portal_models(ROOT / 'backend/portal/models.py')

    remaining = []
    for base in [ROOT / 'frontend/src', ROOT / 'backend']:
        for path in base.rglob('*'):
            if path.suffix not in {'.js', '.jsx', '.py'}:
                continue
            if 'node_modules' in str(path) or 'migrations' in str(path):
                continue
            bad_lines = scan_mojibake(path)
            if bad_lines:
                remaining.append((str(path.relative_to(ROOT)), bad_lines[:5]))

    if remaining:
        print('Remaining suspicious lines:')
        for p, lines in remaining:
            print(p, lines)
    else:
        print('No mojibake patterns detected')
    print('done')
