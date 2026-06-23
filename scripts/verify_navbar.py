# -*- coding: utf-8 -*-
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
t = (ROOT / 'frontend/src/components/Navbar.js').read_text(encoding='utf-8')
for i in [58, 59, 106]:
    l = t.splitlines()[i-1]
    codes = ' '.join(f'U+{ord(c):04X}' for c in l if ord(c) > 127)
    Path(ROOT / 'scripts/verify_nav.txt').write_text(
        (Path(ROOT / 'scripts/verify_nav.txt').read_text(encoding='utf-8') if (ROOT / 'scripts/verify_nav.txt').exists() else '')
        + f'L{i}: {codes}\n',
        encoding='utf-8',
    )
print('ok')
