# -*- coding: utf-8 -*-
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
lines_out = []
for f in ['frontend/public/index.html', 'frontend/src/components/Navbar.js', 'frontend/src/constants/site.js']:
    t = (ROOT / f).read_text(encoding='utf-8')
    lines_out.append('FILE ' + f)
    for i, l in enumerate(t.splitlines()[:15], 1):
        if any(ord(c) > 127 for c in l):
            codes = ' '.join(f'U+{ord(c):04X}' for c in l if ord(c) > 127)
            lines_out.append(f'  L{i}: {codes}')
(ROOT / 'scripts' / 'verify.txt').write_text('\n'.join(lines_out), encoding='utf-8')
print('written')
