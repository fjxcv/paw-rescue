# -*- coding: utf-8 -*-
from pathlib import Path

t = open('frontend/src/constants/site.js', encoding='utf-8').read()
line = t.split('\n')[0]
val = line.split("'")[1]
print('before:', val)
for method in ['gbk', 'gb18030', 'latin1', 'cp1252']:
    try:
        fixed = val.encode(method).decode('utf-8')
        print(method, '->', fixed)
    except Exception as e:
        print(method, 'FAIL', type(e).__name__)
