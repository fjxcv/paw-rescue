# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'frontend/src/pages/Home.js'
lines = p.read_text(encoding='utf-8').splitlines()
for i, line in enumerate(lines):
    if 'aria-label={`' in line and 'index + 1' in line:
        lines[i] = "                aria-label={`\u7b2c ${index + 1} \u5f20`}"
    if line.strip().startswith('{/*') and i + 1 < len(lines) and 'col-md-4' in lines[i + 1]:
        if '\u7d27\u6025' not in line:
            lines[i] = '            {/* \u7d27\u6025\u5bfb\u4e3b */}'
p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('fixed')
