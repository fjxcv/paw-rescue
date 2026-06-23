# -*- coding: utf-8 -*-
from pathlib import Path

s = Path('frontend/src/constants/site.js').read_text(encoding='utf-8')
name = s.split("'")[1]
print('chars', [hex(ord(c)) for c in name])

attempts = []
for enc in ['gbk', 'gb18030', 'big5', 'latin1', 'cp1252', 'iso8859-1']:
    try:
        b = name.encode(enc)
        for dec in ['utf-8', 'gbk', 'gb18030']:
            try:
                r = b.decode(dec)
                attempts.append((enc, dec, r))
            except Exception:
                pass
    except Exception:
        pass

for enc in ['utf-8', 'gbk']:
    try:
        b = name.encode(enc)
        for dec in ['utf-8', 'gbk', 'gb18030', 'latin1']:
            try:
                r = b.decode(dec)
                attempts.append(('enc='+enc, dec, r))
            except Exception:
                pass
    except Exception:
        pass

# fix_mojibake: utf-8 bytes were interpreted as cp1252/gbk chars
try:
    fixed = name.encode('raw_unicode_escape').decode('unicode_escape')
    attempts.append(('raw', 'unicode_escape', fixed))
except Exception as e:
    print('raw fail', e)

for a in attempts[:20]:
    print(a)
