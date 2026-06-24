# -*- coding: utf-8 -*-
"""Find lines with typical mojibake codepoints (93xx, E0xx private, FFFD)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'frontend/src'
BAD = lambda c: ord(c) in range(0x9300, 0x9440) or ord(c) == 0xFFFD or 0xE000 <= ord(c) <= 0xF8FF

found = []
for path in sorted(ROOT.rglob('*.js')):
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if any(BAD(c) for c in line):
            found.append(f'{path.relative_to(ROOT.parent.parent)}:{i}')

out = ROOT.parent / 'scripts' / 'mojibake_lines.txt'
out.write_text('\n'.join(found) if found else 'CLEAN', encoding='utf-8')
print(len(found), 'lines' if found else 'clean')
