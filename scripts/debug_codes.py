# -*- coding: utf-8 -*-
from pathlib import Path
lines = Path('frontend/src/pages/Home.js').read_text(encoding='utf-8').splitlines()
for n in [107, 153, 230, 237, 359]:
    s = lines[n-1]
    codes = ' '.join(f'U+{ord(c):04X}' for c in s if ord(c) > 127)
    Path('scripts/_debug_codes.txt').write_text(
        (Path('scripts/_debug_codes.txt').read_text(encoding='utf-8') if Path('scripts/_debug_codes.txt').exists() else '')
        + f'L{n}: {codes}\n',
        encoding='utf-8',
    )
